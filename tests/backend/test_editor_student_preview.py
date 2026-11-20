from copy import deepcopy
from types import SimpleNamespace

import pytest
from django.test import override_settings

from modu_math_web.editor.services import student_preview
from modu_math_web.learning.models import Attempt, Problem
from modu_math_web.learning.services.assignments import student_problem

pytestmark = pytest.mark.django_db


@pytest.fixture
def saved_preview(monkeypatch, tmp_path):
    root = tmp_path / "problems"
    directory = root / "ko"
    directory.mkdir(parents=True)
    path = directory / "preview.dsl.py"
    path.write_text("# saved source")
    paths = SimpleNamespace(root_dir=root, dsl_path=path, artifact_base="preview")
    semantic = {
        "problem_id": "preview", "problem_type": "arithmetic",
        "metadata": {"instruction": "공유된 학생 문제"},
        "answer": {"value": 5},
    }
    detail = {"semantic": semantic, "solvable": {}, "layout": {}, "renderer": {
        "view_box": {"width": 400, "height": 180}, "elements": [],
    }}
    monkeypatch.setattr(student_preview, "resolve_problem_paths", lambda _: paths)
    monkeypatch.setattr(student_preview, "read_problem_detail", lambda _: deepcopy(detail))
    monkeypatch.setattr(student_preview, "source_publication", lambda _: None)
    return detail


@override_settings(DEBUG=True)
def test_preview_uses_student_contract_and_grader_without_persisting(client, saved_preview):
    url = "/api/editor/problems/ko/preview.dsl.py/student-preview/"
    response = client.get(url)
    assert response.status_code == 200
    content = response.json()
    problem, _, revision = student_preview.saved_student_preview("ko/preview.dsl.py")
    expected = student_problem(problem)
    expected["revision"] = revision
    assert content == expected
    assert "answer" not in content
    assert "no-store" in response["Cache-Control"]
    for answer in ["5", "6"]:
        response = client.post(url, {"answer": answer, "revision": revision}, content_type="application/json")
        assert response.status_code == 200
        assert response.json() == {"correct": problem.check_answer(answer)}
    assert Attempt.objects.count() == 0
    assert Problem.objects.count() == 0


@override_settings(DEBUG=True)
def test_preview_rejects_grading_after_saved_problem_changes(client, saved_preview):
    url = "/api/editor/problems/ko/preview.dsl.py/student-preview/"
    content = client.get(url).json()
    saved_preview["semantic"]["answer"]["value"] = 6
    response = client.post(url, {"answer": "5", "revision": content["revision"]}, content_type="application/json")
    assert response.status_code == 409
    assert Attempt.objects.count() == 0


@override_settings(DEBUG=False)
def test_preview_requires_editor_access_in_production(client):
    assert client.get("/api/editor/problems/ko/preview.dsl.py/student-preview/").status_code == 401
