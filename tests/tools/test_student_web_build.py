import importlib.util
from pathlib import Path

import pytest

path = Path(__file__).resolve().parents[2] / "apps/mobile/scripts/build_student_web.py"
spec = importlib.util.spec_from_file_location("student_web_build", path)
build = importlib.util.module_from_spec(spec)
spec.loader.exec_module(build)


def test_student_stage_excludes_authored_artifacts_and_environment(tmp_path):
    source, stage = tmp_path / "source", tmp_path / "stage"
    for folder in (
        "lib",
        "web",
        "assets/i18n",
        "assets/characters",
        "generated/examples",
    ):
        (source / folder).mkdir(parents=True)
    (source / "generated/examples/private.solvable.json").write_text('{"answer":42}')
    (source / ".env").write_text("PRIVATE_TOKEN=secret")
    (source / "pubspec.yaml").write_text(
        "flutter:\n  assets:\n    - assets/i18n/\n    - generated/examples/\n"
    )
    build.prepare_project(source, stage)
    assert not (stage / "generated").exists()
    assert not (stage / ".env").exists()
    assert "generated/" not in (stage / "pubspec.yaml").read_text()


def test_student_bundle_check_rejects_problem_artifacts(tmp_path):
    (tmp_path / "main.dart.js").write_text("student app")
    build.verify_bundle(tmp_path)
    (tmp_path / "private.renderer.json").write_text("{}")
    with pytest.raises(RuntimeError, match="Private problem artifact"):
        build.verify_bundle(tmp_path)


def test_student_shell_has_no_problem_data(client, monkeypatch, tmp_path):
    from modu_math_web.editor_next import views

    monkeypatch.setattr(views, "_STUDENT_ASSET_ROOT", tmp_path)
    assert client.get("/student/").status_code == 503
    (tmp_path / "index.html").write_text(
        '<base href="/static/editor_next/student_app/">'
    )
    response = client.get("/student/")
    assert response.status_code == 200
    assert response["Cache-Control"] == "no-cache"
