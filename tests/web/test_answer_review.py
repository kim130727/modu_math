import ast
import json
import shutil
from copy import deepcopy
from pathlib import Path
from urllib.parse import quote

import pytest

from modu_math.dsl import BlankSlot, Canvas, ProblemTemplate
from modu_math_web.editor.services.answer_review import (
    normalize_review,
    review_with_slot_answer_keys,
)
from modu_math_web.editor.services.presentation import structure_presentation
from test_editor_api import _setup_django

pytestmark = pytest.mark.django_db


def test_circle_problem_grades_the_choice_values_sent_by_student_preview(tmp_path):
    client = _setup_django(tmp_path)
    from django.conf import settings

    root = Path(__file__).resolve().parents[2] / "examples" / "problems"
    source = next(root.rglob("*008636.dsl.py"))
    relative = source.relative_to(root)
    target = settings.PROBLEMS_ROOT / relative
    target.parent.mkdir(parents=True)
    for kind in ("dsl.py", "semantic.json", "layout.json", "renderer.json"):
        name = source.name.removesuffix("dsl.py") + kind
        shutil.copyfile(source.with_name(name), target.with_name(name))
    url = "/api/editor/problems/" + quote(relative.as_posix()) + "/student-preview/"
    preview = client.get(url).json()
    choices = preview["input_schema"]["fields"][0]["choices"]
    assert len(choices) == 2 and choices[0]["value"] == "slot.choice.copy4"
    for choice, expected in zip(choices, (True, False)):
        response = client.post(url, {
            "revision": preview["revision"], "answer": choice["value"],
        }, content_type="application/json")
        assert response.status_code == 200
        assert response.json()["correct"] is expected


def test_line_problem_hides_legacy_panel_punctuation_and_grades_slot_ids(tmp_path):
    client = _setup_django(tmp_path)
    from django.conf import settings

    root = Path(__file__).resolve().parents[2] / "examples" / "problems"
    source = next(root.rglob("*008974.dsl.py"))
    relative = source.relative_to(root)
    target = settings.PROBLEMS_ROOT / relative
    target.parent.mkdir(parents=True)
    for kind in ("dsl.py", "semantic.json", "layout.json", "renderer.json"):
        name = source.name.removesuffix("dsl.py") + kind
        shutil.copyfile(source.with_name(name), target.with_name(name))
    url = "/api/editor/problems/" + quote(relative.as_posix()) + "/student-preview/"
    preview = client.get(url).json()
    elements = preview["renderer_data"]["elements"]
    assert not any(e.get("text") in {"(", ")", ","} for e in elements)
    assert len([e for e in elements if e.get("source_ref", "").startswith("slot.diagram.label_")]) == 4
    choices = preview["input_schema"]["fields"][0]["choices"]
    assert len(choices) == 4
    for index, choice in enumerate(choices):
        response = client.post(url, {
            "revision": preview["revision"], "answer": choice["value"],
        }, content_type="application/json")
        assert response.status_code == 200
        assert response.json()["correct"] is (index == 2)


def test_two_rays_use_the_same_visible_canvas_and_viewport(tmp_path):
    client = _setup_django(tmp_path)
    from django.conf import settings

    root = Path(__file__).resolve().parents[2] / "examples" / "problems"
    source = next(root.rglob("*008977.dsl.py"))
    relative = source.relative_to(root)
    target = settings.PROBLEMS_ROOT / relative
    target.parent.mkdir(parents=True)
    for kind in ("dsl.py", "semantic.json", "layout.json", "renderer.json"):
        name = source.name.removesuffix("dsl.py") + kind
        shutil.copyfile(source.with_name(name), target.with_name(name))
    url = "/api/editor/problems/" + quote(relative.as_posix())
    editor = client.get(url + "/").json()
    student = client.get(url + "/student-preview/").json()

    assert {e["source_ref"] for e in student["renderer_data"]["elements"]} == {
        "slot.diagram.ray_top", "slot.diagram.ray_bottom",
    }
    assert set(editor["canvas_presentation"]["hidden_slot_ids"]) == {
        "slot.stem.question", "slot.choice.option_0", "slot.choice.option_1",
    }
    assert student["renderer_data"]["presentation_viewport"] == editor["canvas_presentation"]["viewport"]
    assert student["renderer_data"]["presentation_viewport"] == {
        "x": 390, "y": 56, "width": 222, "height": 130,
    }
    assert len(student["input_schema"]["fields"][0]["choices"]) == 2


def test_division_choices_stay_inside_diagram_cards_after_build(tmp_path):
    client = _setup_django(tmp_path)
    from django.conf import settings

    root = Path(__file__).resolve().parents[2] / "examples" / "problems"
    source = next(root.rglob("*009137.dsl.py"))
    relative = source.relative_to(root)
    target = settings.PROBLEMS_ROOT / relative
    target.parent.mkdir(parents=True)
    for kind in ("dsl.py", "editor_overrides.json"):
        name = source.name.removesuffix("dsl.py") + kind
        shutil.copyfile(source.with_name(name), target.with_name(name))
    url = "/api/editor/problems/" + quote(relative.as_posix())
    result = client.post(url + "/build/")
    assert result.status_code == 200, result.content
    editor = result.json()["canvas_presentation"]
    assert editor["hidden_slot_ids"] == ["slot.stem.question"]

    preview = client.get(url + "/student-preview/").json()
    elements = preview["renderer_data"]["elements"]
    assert sum(e["type"] == "rect" for e in elements) == 2
    labels = [e["text"] for e in elements if e["type"] == "text"]
    assert labels == ["㉠ 42 ÷ 6 = 7", "㉡ 35 ÷ 7 = 5"]
    assert preview["renderer_data"]["presentation_viewport"] == editor["viewport"]
    choices = preview["input_schema"]["fields"][0]["choices"]
    assert [choice["label"] for choice in choices] == labels
    for choice, expected in zip(choices, (True, False)):
        response = client.post(url + "/student-preview/", {
            "revision": preview["revision"], "answer": choice["value"],
        }, content_type="application/json")
        assert response.json()["correct"] is expected


def test_route_problem_saved_canvas_choice_reaches_student_grader(tmp_path):
    client = _setup_django(tmp_path)
    from django.conf import settings

    root = Path(__file__).resolve().parents[2] / "examples" / "problems"
    source = next(root.rglob("P3_1_01_00040_07646.dsl.py"))
    relative = source.relative_to(root)
    target = settings.PROBLEMS_ROOT / relative
    target.parent.mkdir(parents=True)
    shutil.copyfile(source, target)
    suffix = ".editor_overrides.json"
    shutil.copyfile(source.with_suffix("").with_suffix(suffix),
                    target.with_suffix("").with_suffix(suffix))
    url = "/api/editor/problems/" + quote(relative.as_posix())

    def post(path, data):
        response = client.post(url + path, data=data, content_type="application/json")
        assert response.status_code == 200, response.content
        return response.json()

    saved = post("/build/", {})["artifacts"]["semantic"]["answer"]["presentation"]["review"]
    correct_id, wrong_id = [choice["id"] for choice in saved["choices"]]

    def check(expected):
        preview = client.get(url + "/student-preview/").json()
        assert preview["presentation"]["mode"] == "canvas_select"
        assert [choice["value"] for choice in preview["presentation"]["canvas_choices"]] == [correct_id, wrong_id]
        for choice_id in (correct_id, wrong_id):
            result = post("/student-preview/", {"revision": preview["revision"], "answer": choice_id})
            assert result["correct"] is (choice_id == expected)

    check(correct_id)
    # Two diagram choices may share a label. Changing the key must still
    # change which physical choice the student grader accepts.
    for choice in saved["choices"]:
        choice["correct"] = choice["id"] == wrong_id
        choice["text"] = "Same label"
    post("/answer-review/", {"review": saved | {"status": "verified"}})
    post("/build/", {})
    check(wrong_id)


def review(mode="choice"):
    return {"mode": mode, "status": "needs_changes", "note": "복수 정답 확인 필요",
            "answers": [{"value": "O"}, {"value": "X"}, {"value": "O"}],
            "groups": [{"id": "g1", "label": "(1)", "choices": ["가", "나"], "correct_index": 1}, {"id": "g2", "label": "(2)", "choices": ["가", "나"], "correct_index": 1}],
            "choices": [{"id": "choice.a", "label": "①", "text": "진경", "correct": True},
                        {"id": "choice.b", "label": "②", "text": "현진", "correct": True}]}


def slot_answer_key(source, slot_id):
    module = ast.parse(source)
    for node in ast.walk(module):
        if not isinstance(node, ast.Call) or not isinstance(node.func, ast.Name):
            continue
        keywords = {item.arg: item.value for item in node.keywords if item.arg}
        if "id" not in keywords or "answer_key" not in keywords:
            continue
        if ast.literal_eval(keywords["id"]) == slot_id:
            return ast.literal_eval(keywords["answer_key"])
    raise AssertionError(f"answer slot not found: {slot_id}")


@pytest.mark.parametrize("mode", ["choice", "ox", "panel_input", "grouped_choice"])
def test_review_save_build_reopen_is_persistent(tmp_path, mode):
    client = _setup_django(tmp_path)
    assert client.post('/api/editor/problems/create/', data=json.dumps({"problem_id": "review-test"}), content_type='application/json').status_code == 200
    response = client.post('/api/editor/problems/review-test/answer-review/', data=json.dumps({"review": review(mode)}), content_type='application/json')
    assert response.status_code == 200, response.content
    for _ in range(2):
        built = client.post('/api/editor/problems/review-test/build/')
        assert built.status_code == 200 and built.json()['ok'], built.content
        detail = client.get('/api/editor/problems/review-test/').json()
        for artifact in ('semantic', 'solvable'):
            answer = detail[artifact]['answer']
            assert answer['presentation']['review'] == normalize_review(review(mode))
            assert answer['presentation']['editor_managed'] is True
            assert len(answer['answer_key']) == (2 if mode in {'choice', 'grouped_choice'} else 3)
    assert 'EDITOR_ANSWER_REVIEW' in detail['dsl']


def test_8631_marker_and_value_form_five_choices():
    from modu_math_web.editor.services.content_store import paths_for, read_content
    content = read_content(paths_for(Path('examples/problems'), 'ko/S3_elem_3_008631.dsl.py'))
    layout, semantic = content['layout'], content['semantic']
    original = deepcopy((layout, semantic))
    result, updated, _ = structure_presentation(layout, semantic)
    assert [c['text'] for c in updated['answer']['choices']] == ['21', '22', '23', '24', '25']
    assert [c['label'] for c in updated['answer']['choices']] == list('①②③④⑤')
    assert all(len(c['source_refs']) == 2 for c in updated['answer']['choices'])
    assert structure_presentation(result, updated)[1] == updated
    assert (layout, semantic) == original


def test_authored_answer_units_save_build_and_reopen(tmp_path):
    client = _setup_django(tmp_path)
    assert client.post('/api/editor/problems/create/', data=json.dumps({"problem_id": "unit-test"}), content_type='application/json').status_code == 200
    settings = review("panel_input") | {"answers": [{"value": "12", "unit": "cm"}, {"value": "8", "unit": "개"}], "choices": []}
    response = client.post('/api/editor/problems/unit-test/answer-review/', data=json.dumps({"review": settings}), content_type='application/json')
    assert response.status_code == 200, response.content
    assert client.post('/api/editor/problems/unit-test/build/').status_code == 200
    detail = client.get('/api/editor/problems/unit-test/').json()
    for artifact in ('semantic', 'solvable'):
        assert detail[artifact]['answer']['answer_key'] == settings['answers']
        assert detail[artifact]['answer']['presentation']['review']['answers'] == settings['answers']


@pytest.mark.parametrize('unit', [12, None, 'x' * 101])
def test_invalid_answer_unit_is_rejected(unit):
    with pytest.raises(ValueError):
        normalize_review(review("panel_input") | {"answers": [{"value": "12", "unit": unit}]})


def test_authored_canvas_blank_keeps_answer_connection_after_build(tmp_path):
    client = _setup_django(tmp_path)
    assert client.post('/api/editor/problems/create/', data=json.dumps({"problem_id": "blank-test"}), content_type='application/json').status_code == 200
    slot_id = 'slot.konva_editor_answer_blank'
    interaction = {"type": "input", "role": "answer", "value_type": "text", "keyboard": "text", "max_length": 100,
                   "order": 0, "answer_key_index": 0, "answer_ref": slot_id, "include_in_submission": True}
    payload = {"format": False, "fast": True, "patches": [{"target": slot_id, "op": "add", "value": {
        "kind": "rect", "region_id": "region.diagram", "content": {"x": 80, "y": 80, "width": 100, "height": 56, "fill": "#ffffff", "stroke": "#6366f1", "stroke_width": 2, "interaction": interaction}}}]}
    response = client.post('/api/editor/problems/blank-test/layout-patch/', data=json.dumps(payload), content_type='application/json')
    assert response.status_code == 200, response.content
    settings = review("canvas_slots") | {"answers": [{"value": "12", "unit": "cm", "ref": slot_id}], "choices": []}
    response = client.post('/api/editor/problems/blank-test/answer-review/', data=json.dumps({"review": settings}), content_type='application/json')
    assert response.status_code == 200, response.content
    response = client.post('/api/editor/problems/blank-test/build/')
    assert response.status_code == 200 and response.json()['ok'], response.content
    detail = client.get('/api/editor/problems/blank-test/').json()
    slot = next(slot for slot in detail['layout']['slots'] if slot['id'] == slot_id)
    assert slot['content']['interaction']['answer_ref'] == slot_id
    assert detail['solvable']['answer']['answer_key'] == [{"value": "12", "unit": "cm", "slot_id": slot_id}]


def test_explicit_new_blank_reference_is_not_replaced_by_legacy_blank():
    problem = ProblemTemplate(id="two-blanks", title="", canvas=Canvas(width=100, height=100), regions=(),
                              slots=(BlankSlot(id="slot.old", answer_key="9"),))
    settings = review("canvas_slots") | {"answers": [{"value": "12", "unit": "cm", "ref": "slot.new"}], "choices": []}
    hydrated = review_with_slot_answer_keys(settings, problem)
    assert hydrated['answers'][0] == {"value": "12", "unit": "cm", "ref": "slot.new"}
    assert hydrated['answers'][1] == {"value": "9", "ref": "slot.old"}


@pytest.mark.parametrize('patch', [
    {'mode': 'wrong'}, {'status': 'wrong'}, {'choices': []},
    {'mode': 'ox', 'answers': [{'value': 'maybe'}]},
    {'choices': [{'id': 'a', 'text': 'A', 'correct': False}]},
])
def test_invalid_review_is_rejected(patch):
    with pytest.raises(ValueError):
        normalize_review(review() | {'status': 'verified'} | patch)


def test_canvas_visibility_defaults_to_visible_and_is_written_to_presentation():
    from modu_math_web.editor.services.answer_review import apply_answer_review

    normalized = normalize_review(review("panel_input"))
    assert normalized["show_canvas"] is True

    semantic, solvable = apply_answer_review(
        {"answer": {}},
        {"answer": {}},
        review("panel_input") | {"show_canvas": False},
    )
    assert semantic["answer"]["presentation"]["show_canvas"] is False
    assert solvable["answer"]["presentation"]["show_canvas"] is False


def test_canvas_slot_mode_cannot_hide_canvas():
    with pytest.raises(ValueError):
        normalize_review(review("canvas_slots") | {"show_canvas": False})


def test_unresolved_person_question_can_save_review_note_without_inventing_answer(tmp_path):
    client = _setup_django(tmp_path)
    client.post('/api/editor/problems/create/', data=json.dumps({"problem_id": "unresolved"}), content_type='application/json')
    unresolved = review() | {"choices": [], "answers": [], "note": "두 설명이 모두 맞는지 검토 필요"}
    response = client.post('/api/editor/problems/unresolved/answer-review/', data=json.dumps({"review": unresolved}), content_type='application/json')
    assert response.status_code == 200
    built = client.post('/api/editor/problems/unresolved/build/')
    assert built.status_code == 200 and built.json()['ok'], built.content
    saved = client.get('/api/editor/problems/unresolved/').json()['semantic']['answer']
    assert saved['presentation']['review']['note'] == unresolved['note']
    assert saved['answer_key'] == []


def test_review_save_updates_explicit_blank_slot_answer_key(tmp_path):
    client = _setup_django(tmp_path)
    assert client.post(
        "/api/editor/problems/create/",
        data=json.dumps({"problem_id": "slot-review"}),
        content_type="application/json",
    ).status_code == 200

    response = client.post(
        "/api/editor/problems/slot-review/answer-review/",
        data=json.dumps(
            {
                "review": {
                    "mode": "canvas_slots",
                    "status": "verified",
                    "note": "",
                    "answers": [{"value": "42", "ref": "slot.answer"}],
                    "choices": [],
                }
            }
        ),
        content_type="application/json",
    )

    assert response.status_code == 200, response.content
    detail = client.get("/api/editor/problems/slot-review/").json()
    assert slot_answer_key(detail["dsl"], "slot.answer") == "42"
    assert "EDITOR_ANSWER_REVIEW" in detail["dsl"]


def test_review_save_updates_choice_slot_answer_key(tmp_path, monkeypatch):
    from types import SimpleNamespace

    from modu_math_web.editor.services import answer_review

    dsl_path = tmp_path / "choice.dsl.py"
    dsl_path.write_text(
        'from modu_math.dsl import ChoiceSlot\n'
        'SLOT = ChoiceSlot(id="slot.choice", choices=("A", "B"), answer_key=("A",))\n',
        encoding="utf-8",
    )
    monkeypatch.setattr(
        answer_review,
        "resolve_problem_paths",
        lambda _problem_id: SimpleNamespace(dsl_path=dsl_path),
    )

    answer_review.save_answer_review(
        "choice",
        {
            "mode": "choice",
            "status": "verified",
            "note": "",
            "answers": [],
            "choices": [
                {
                    "id": "slot.choice.choice.1",
                    "label": "1",
                    "text": "A",
                    "correct": False,
                    "sourceRefs": ["slot.choice"],
                },
                {
                    "id": "slot.choice.choice.2",
                    "label": "2",
                    "text": "B",
                    "correct": True,
                    "sourceRefs": ["slot.choice"],
                },
            ],
        },
    )

    assert slot_answer_key(dsl_path.read_text(encoding="utf-8"), "slot.choice") == ("B",)


def test_explicit_slot_answer_key_overrides_stale_review_during_build(tmp_path):
    client = _setup_django(tmp_path)
    assert client.post(
        "/api/editor/problems/create/",
        data=json.dumps({"problem_id": "slot-source"}),
        content_type="application/json",
    ).status_code == 200
    saved = {
        "mode": "canvas_slots",
        "status": "verified",
        "note": "",
        "answers": [{"value": "7", "ref": "slot.answer"}],
        "choices": [],
    }
    assert client.post(
        "/api/editor/problems/slot-source/answer-review/",
        data=json.dumps({"review": saved}),
        content_type="application/json",
    ).status_code == 200

    from django.conf import settings

    dsl_path = settings.PROBLEMS_ROOT / "slot-source" / "problem.dsl.py"
    dsl = dsl_path.read_text(encoding="utf-8").replace(
        "answer_key = '7'", "answer_key = '9'"
    )
    dsl_path.write_text(dsl, encoding="utf-8")
    built = client.post("/api/editor/problems/slot-source/build/")

    assert built.status_code == 200 and built.json()["ok"], built.content
    detail = client.get("/api/editor/problems/slot-source/").json()
    assert detail["semantic"]["answer"]["presentation"]["review"]["answers"] == [
        {"value": "9", "ref": "slot.answer"}
    ]


def test_single_blank_replaces_legacy_answer_value_reference():
    problem = ProblemTemplate(
        id="single-blank",
        title="",
        canvas=Canvas(width=100, height=100),
        regions=(),
        slots=(BlankSlot(id="slot.answer", answer_key="9"),),
    )
    stale = {
        "mode": "panel_input",
        "status": "verified",
        "note": "",
        "answers": [{"value": "7", "ref": "answer.value"}],
        "choices": [],
    }

    hydrated = review_with_slot_answer_keys(stale, problem)

    assert hydrated["answers"] == [{"value": "9", "ref": "slot.answer"}]
