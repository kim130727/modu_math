"""Regressions for editor timeouts caused by catalog import row locks."""
import json
from io import StringIO

import pytest
from django.core.management import call_command
from django.db import OperationalError, connection
from django.test import Client

from modu_math_web.editor.services.build import BuildResult
from modu_math_web.editor.services.content_store import paths_for
from modu_math_web.learning.models import Problem, ProblemPublication


@pytest.mark.django_db(transaction=True)
@pytest.mark.parametrize("dry_run", [False, True])
def test_import_releases_locks_before_reading_next_problem(tmp_path, monkeypatch, dry_run):
    from modu_math_web.editor.services import content_store

    directory = tmp_path / "ko"
    directory.mkdir()
    paths = []
    for name in ("first", "second"):
        (directory / f"{name}.dsl.py").write_text("# fixture", encoding="utf-8")
        (directory / f"{name}.renderer.json").write_text("{}", encoding="utf-8")
        paths.append(paths_for(tmp_path, f"ko/{name}.dsl.py"))
    monkeypatch.setattr(content_store, "list_content", lambda _: iter(paths))

    def read_content(path):
        # File IO and compilation must never extend a previous row's lock.
        assert connection.get_autocommit()
        if path == paths[1]:
            assert Problem.objects.filter(problem_id="first").exists() is not dry_run
            assert ProblemPublication.objects.count() == (0 if dry_run else 1)
        return {"semantic": {"answer": {"value": 1}}, "renderer": {"elements": []}}

    monkeypatch.setattr(content_store, "read_content", read_content)
    call_command("sync_problems", root=tmp_path, dry_run=dry_run, stdout=StringIO())
    assert Problem.objects.count() == (0 if dry_run else 2)


@pytest.mark.django_db(transaction=True)
def test_import_problem_and_publication_roll_back_together(tmp_path, monkeypatch):
    from modu_math_web.editor.services import content_store

    directory = tmp_path / "ko"
    directory.mkdir()
    (directory / "sample.dsl.py").write_text("# fixture", encoding="utf-8")
    (directory / "sample.renderer.json").write_text("{}", encoding="utf-8")
    path = paths_for(tmp_path, "ko/sample.dsl.py")
    monkeypatch.setattr(content_store, "list_content", lambda _: iter([path]))
    monkeypatch.setattr(content_store, "read_content", lambda _: {})

    def fail_publication(**kwargs):
        raise OperationalError("publication failed")

    monkeypatch.setattr(ProblemPublication.objects, "create", fail_publication)
    with pytest.raises(OperationalError, match="publication failed"):
        call_command("sync_problems", root=tmp_path, stdout=StringIO())
    assert not Problem.objects.exists()


@pytest.mark.django_db
def test_database_sync_failure_returns_json_and_can_be_retried(settings, tmp_path, monkeypatch):
    from modu_math_web.learning.services import authoring_access

    settings.DEBUG = True
    settings.PROBLEMS_ROOT = tmp_path
    directory = tmp_path / "ko"
    directory.mkdir()
    (directory / "sample.dsl.py").write_text("# fixture", encoding="utf-8")
    problem = Problem.objects.create(problem_id="sample", answer={"value": 1})
    publication = ProblemPublication.objects.create(problem=problem, source_path="ko/sample.dsl.py")
    artifacts = {"semantic": {"answer": {"value": 2}}, "renderer": {"elements": []}}
    monkeypatch.setattr("modu_math_web.editor.views.build_with_artifacts",
                        lambda _: (BuildResult(True, "build_ok", ""), artifacts))
    original = authoring_access.sync_authored_artifacts

    def locked(*args):
        raise OperationalError("canceling statement due to lock timeout")

    monkeypatch.setattr(authoring_access, "sync_authored_artifacts", locked)
    client = Client()
    url = "/api/editor/problems/ko/sample.dsl.py/build/"
    response = client.post(url)
    assert response.status_code == 503
    assert response.json()["stage"] == "database_sync"
    assert "retry" in response.json()["error"]
    assert response["Cache-Control"] == "private, no-store"
    problem.refresh_from_db()
    assert problem.answer == {"value": 1}
    monkeypatch.setattr(authoring_access, "sync_authored_artifacts", original)
    assert client.post(url).status_code == 200
    problem.refresh_from_db()
    assert problem.answer == {"value": 2}
    publication.refresh_from_db()
    assert publication.status == "draft"


def test_failed_build_does_not_read_stale_or_broken_artifacts(monkeypatch):
    from modu_math_web.editor.services import build

    monkeypatch.setattr(build, "run_problem_build", lambda _: BuildResult(False, "", "", "DSL error"))

    def stale(*args):
        pytest.fail("Failed builds must not read old artifacts")

    monkeypatch.setattr(build, "read_artifacts", stale)
    result, artifacts = build.build_with_artifacts("sample")
    assert not result.ok and result.error == "DSL error"
    assert artifacts == {}


def test_file_build_skips_svg_and_still_writes_renderer(settings, tmp_path, monkeypatch):
    from modu_math_web.editor.services import build

    settings.PROBLEMS_ROOT = tmp_path
    directory = tmp_path / "ko"
    directory.mkdir()
    source = directory / "sample.dsl.py"
    source.write_text('''from modu_math.dsl import Canvas, ProblemTemplate
PROBLEM_TEMPLATE = ProblemTemplate(id="sample", title="sample", canvas=Canvas(width=300, height=200), regions=(), slots=())
''', encoding="utf-8")

    def unnecessary_svg(*args):
        pytest.fail("File-backed editor builds must not generate a discarded SVG")

    monkeypatch.setattr(build, "render_svg", unnecessary_svg)
    assert build.run_problem_build("ko/sample.dsl.py").ok
    assert "elements" in json.loads((directory / "sample.renderer.json").read_text(encoding="utf-8"))
