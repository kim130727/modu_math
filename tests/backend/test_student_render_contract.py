import json

import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient

from modu_math_web.learning.models import Attempt, Problem, ProblemPublication
from modu_math_web.learning.services.assignments import student_problem

pytestmark = pytest.mark.django_db


@pytest.fixture
def render_problem():
    problem = Problem.objects.create(
        problem_id="render-contract",
        answer={
            "value": "SECRET",
            "answer_key": [
                {"slot_id": "first", "value": "SECRET-A"},
                {"slot_id": "second", "value": "SECRET-B"},
            ],
            "presentation": {"mode": "canvas_slots"},
        },
        semantic_data={"metadata": {"question": "old prompt"}},
        layout_data={
            "slots": [
                {
                    "id": "instruction",
                    "content": {
                        "text": "새 풀이 지시문",
                        "semantic_role": "instruction",
                    },
                }
            ]
        },
        renderer_data={
            "view_box": {"width": 500, "height": 200},
            "elements": [
                {
                    "id": name,
                    "type": "rect",
                    "text": "SECRET",
                    "attributes": {
                        "x": i * 120,
                        "y": 50,
                        "width": 100,
                        "height": 60,
                        "data-semantic-role": "answer",
                    },
                    "interaction": {
                        "type": "input",
                        "role": "answer",
                        "answer_key_index": index,
                        "answer_ref": "SECRET-REF",
                        "default_value": "SECRET",
                    },
                    "input_style": {"font_size_mode": "fixed", "font_size": 24},
                }
                for i, (name, index) in enumerate([("second-box", 1), ("first-box", 0)])
            ],
        },
    )
    ProblemPublication.objects.create(
        problem=problem, status="published", visibility="public"
    )
    return problem


def test_student_contract_preserves_roles_styles_and_safe_answer_bindings(
    render_problem,
):
    payload = student_problem(render_problem)
    assert payload["prompt"] == "새 풀이 지시문"
    assert payload["presentation"]["mode"] == "canvas_slots"
    assert payload["presentation"]["canvas_bindings"] == {
        "second-box": 1,
        "first-box": 0,
    }
    assert payload["layout_data"]["slots"][0]["content"] == {
        "semantic_role": "instruction"
    }
    assert payload["renderer_data"]["elements"][0]["input_style"]["font_size"] == 24
    assert payload["renderer_data"]["elements"][0]["interaction"]["max_length"] == 64
    assert "SECRET" not in json.dumps(payload)
    assert payload["revision"] == render_problem.updated_at.isoformat()


def test_partial_canvas_bindings_fall_back_to_reachable_panel_fields(render_problem):
    render_problem.renderer_data["elements"].pop()
    payload = student_problem(render_problem)
    assert payload["presentation"]["mode"] == "panel_input"
    assert len(payload["input_schema"]["fields"]) == 2


def test_owner_also_gets_answer_free_student_presentation_and_revision_conflict(
    render_problem,
):
    admin = get_user_model().objects.create_user("render-admin", is_staff=True)
    api = APIClient()
    api.force_authenticate(admin)
    url = f"/api/v1/problems/{render_problem.pk}/"
    data = api.get(url, {"presentation": "student"}).data
    assert "answer" not in data and "presentation" in data
    old_revision = data["revision"]
    assert api.get(url + "version/").data["revision"] == old_revision
    render_problem.answer = {"value": "CHANGED"}
    render_problem.save()
    response = api.post(
        "/api/v1/attempts/",
        {
            "problem": render_problem.pk,
            "submitted_answer": "SECRET",
            "content_revision": old_revision,
        },
        format="json",
    )
    assert response.status_code == 409
    assert not Attempt.objects.exists()


def test_debug_legacy_editor_build_updates_public_db_but_not_assigned_snapshot(
    settings, tmp_path, monkeypatch
):
    settings.DEBUG = True
    settings.PROBLEMS_ROOT = tmp_path
    directory = tmp_path / "ko" / "day"
    directory.mkdir(parents=True)
    (directory / "legacy.dsl.py").write_text("# fixture", encoding="utf-8")
    problem = Problem.objects.create(
        problem_id="legacy",
        answer={"value": 1},
        catalog_data={"path": "examples/problems/ko/day", "filePrefix": "legacy"},
    )
    publication = ProblemPublication.objects.create(
        problem=problem, status="published", visibility="public"
    )
    from modu_math_web.learning.models import (
        Assignment,
        AssignmentRecipient,
        ProblemSet,
        StudentProfile,
    )
    from modu_math_web.learning.services.assignments import snapshot_item

    teacher = get_user_model().objects.create_user("render-teacher")
    profile = StudentProfile.objects.create(
        user=get_user_model().objects.create_user("render-student"), created_by=teacher
    )
    assignment = Assignment.objects.create(
        owner=teacher,
        title="snapshot",
        source_version=1,
        problem_set=ProblemSet.objects.create(owner=teacher, title="set"),
    )
    AssignmentRecipient.objects.create(assignment=assignment, student=profile)
    frozen = snapshot_item(assignment, problem, 0)
    from modu_math_web.editor.services.build import BuildResult

    artifacts = {
        "semantic": {"metadata": {"title": "수정됨"}, "answer": {"value": 2}},
        "renderer": {"elements": []},
        "layout": {},
        "solvable": {},
    }
    monkeypatch.setattr(
        "modu_math_web.editor.views.build_with_artifacts",
        lambda _: (BuildResult(True, "", ""), artifacts),
    )
    response = APIClient().post("/api/editor/problems/ko/day/legacy.dsl.py/build/")
    assert response.status_code == 200
    problem.refresh_from_db()
    publication.refresh_from_db()
    frozen.refresh_from_db()
    assert problem.answer == {"value": 2}
    assert frozen.answer == {"value": 1}
    assert publication.source_path == "ko/day/legacy.dsl.py"
    assert publication.visibility == "public" and publication.owner_id is None
