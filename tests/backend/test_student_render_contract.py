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


def test_canvas_projection_keeps_diagram_symbols_and_canvas_choices():
    from modu_math_web.learning.services.canvas_presentation import project_canvas

    choice = {
        "id": "option.text", "source_ref": "option", "type": "text", "text": "○",
        "attributes": {"x": 30, "y": 40, "data-semantic-role": "choice"},
        "interaction": {"type": "choice", "role": "answer"},
    }
    frame = {
        "id": "frame.rect", "source_ref": "frame", "type": "rect",
        "attributes": {"x": 5, "y": 10, "width": 70, "height": 50},
    }
    diagram = {
        "id": "diagram.text", "source_ref": "diagram", "type": "text", "text": "○",
        "attributes": {"x": 155, "y": 40, "data-semantic-role": "symbol_label"},
    }
    layout = {"regions": [{"role": "choices", "slot_ids": ["option", "frame"]}]}
    schema = {"fields": [{"choices": [{"label": "○", "value": "option"}]}]}
    elements = [frame, choice, diagram]
    visible, canvas = project_canvas(elements, layout, {}, {"mode": "choice"}, schema, "")
    assert visible == [diagram]
    assert canvas["hidden_slot_ids"] == ["frame", "option"]

    visible, canvas = project_canvas(elements, layout, {}, {
        "mode": "canvas_select", "canvas_choices": [{"element_ids": ["option.text"]}],
    }, schema, "")
    assert visible == elements
    assert canvas["hidden_slot_ids"] == []


@pytest.mark.parametrize(("answer", "limit"), [(5, 1), (1124, 4), ("306", 3), (-1234567, None), ("7/8", None)])
def test_whole_answer_capacity_follows_integer_length(render_problem, answer, limit):
    render_problem.answer = {"value": answer}
    render_problem.renderer_data["elements"] = [{
        "id": "whole", "type": "rect",
        "attributes": {"x": 10, "y": 20, "width": 160, "height": 80},
        "interaction": {"type": "input", "role": "answer", "value_type": "integer", "max_length": 3},
    }]
    payload = student_problem(render_problem)
    assert payload["presentation"]["canvas_bindings"] == {"whole": 0}
    assert payload["input_schema"]["fields"][0].get("max_length") == limit
    assert payload["renderer_data"]["elements"][0]["interaction"]["max_length"] == (limit or 64)
    assert render_problem.renderer_data["elements"][0]["interaction"]["max_length"] == 3


def test_split_digit_cells_and_operator_constraints_remain_intact(render_problem):
    render_problem.answer = {"value": 1124}
    render_problem.renderer_data["elements"] = [{
        "id": f"digit-{i}", "type": "rect",
        "attributes": {"x": i * 30, "y": 20, "width": 25, "height": 40},
        "interaction": {"type": "input", "role": "answer", "value_type": "digit", "max_length": 1},
    } for i in range(4)]
    payload = student_problem(render_problem)
    assert set(payload["presentation"]["canvas_bindings"].values()) == {0}
    assert [e["interaction"]["max_length"] for e in payload["renderer_data"]["elements"]] == [1, 1, 1, 1]
    render_problem.renderer_data["elements"] = [{
        "id": "operator", "type": "rect",
        "attributes": {"x": 10, "y": 20, "width": 60, "height": 60},
        "interaction": {"type": "input", "role": "answer", "value_type": "operator", "max_length": 1},
    }]
    payload = student_problem(render_problem)
    assert payload["renderer_data"]["elements"][0]["interaction"]["max_length"] == 1


def test_misconfigured_digit_field_accepts_whole_answer_in_saved_assignments(render_problem):
    from copy import deepcopy
    from types import SimpleNamespace

    from modu_math_web.learning.services.assignments import _student_item_content

    render_problem.answer = {"value": [9, 490], "answer_key": [
        {"value": 9}, {"value": 490},
    ]}
    for element in render_problem.renderer_data["elements"]:
        element["interaction"].update(value_type="digit", max_length=1, auto_advance=True, keyboard="number")
    original = deepcopy(render_problem.renderer_data)
    payload = student_problem(render_problem)
    # Simulate an assignment saved before the capacity fix.
    snapshot = deepcopy(payload)
    for field in snapshot["input_schema"]["fields"]:
        field.pop("max_length")
    for element in snapshot["renderer_data"]["elements"]:
        element["interaction"].update(value_type="digit", max_length=1, auto_advance=True, keyboard="number")
    frozen = deepcopy(snapshot)
    resolved = _student_item_content(SimpleNamespace(public_content=snapshot, answer=render_problem.answer))
    for content in (payload, resolved):
        by_id = {e["id"]: e["interaction"] for e in content["renderer_data"]["elements"]}
        assert by_id["first-box"]["max_length"] == 1
        assert by_id["first-box"]["auto_advance"] is True
        assert by_id["second-box"]["max_length"] == 3
        assert by_id["second-box"]["auto_advance"] is False
        assert by_id["second-box"]["value_type"] == "integer"
        assert [field["max_length"] for field in content["input_schema"]["fields"]] == [1, 3]
        assert "490" not in json.dumps(content)
    assert snapshot == frozen
    assert render_problem.renderer_data == original


def test_individual_digit_fields_keep_capacity_and_bind_by_complete_authored_order(render_problem):
    # The stored array/slot IDs are in copy order; the authored order is the
    # intended sequence [carry, carry, hundreds, tens, units].
    render_problem.answer = {"value": [1, 1, 9, 2, 1], "answer_key": [
        {"slot_id": name, "value": value}
        for name, value in zip(["right-carry", "left-carry", "tens", "hundreds", "units"], [1, 1, 9, 2, 1])
    ]}
    render_problem.renderer_data["elements"] = [{
        "id": name, "type": "rect", "source_ref": name,
        "attributes": {"x": order * 25, "y": 20, "width": 19, "height": 19},
        "interaction": {"type": "input", "role": "answer", "value_type": "digit",
                        "max_length": 1, "auto_advance": True, "order": order},
    } for name, order in [("right-carry", 1), ("left-carry", 0), ("tens", 3), ("hundreds", 2), ("units", 4)]]
    payload = student_problem(render_problem)
    assert payload["presentation"]["canvas_bindings"] == {
        "right-carry": 1, "left-carry": 0, "tens": 3, "hundreds": 2, "units": 4,
    }
    assert all(e["interaction"]["value_type"] == "digit"
               and e["interaction"]["max_length"] == 1
               and e["interaction"]["auto_advance"]
               for e in payload["renderer_data"]["elements"])
    assert render_problem.check_answer(["1", "1", "9", "2", "1"])
    assert not render_problem.check_answer(["1", "1", "2", "9", "1"])
    # Explicit field bindings take precedence over legacy traversal order.
    render_problem.renderer_data["elements"][0]["interaction"]["answer_key_index"] = 0
    render_problem.renderer_data["elements"][1]["interaction"]["answer_key_index"] = 1
    assert student_problem(render_problem)["presentation"]["canvas_bindings"]["right-carry"] == 0


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
