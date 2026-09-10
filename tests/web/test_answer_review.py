import ast
import json
from copy import deepcopy
from pathlib import Path

import pytest

from modu_math.dsl import BlankSlot, Canvas, ProblemTemplate
from modu_math_web.editor.services.answer_review import (
    normalize_review,
    review_with_slot_answer_keys,
)
from modu_math_web.editor.services.presentation import structure_presentation
from test_editor_api import _setup_django


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
    base = Path('examples/problems/ko/S3_elem_3_008631')
    layout = json.loads(Path(str(base) + '.layout.json').read_text(encoding='utf-8'))
    semantic = json.loads(Path(str(base) + '.semantic.json').read_text(encoding='utf-8'))
    original = deepcopy((layout, semantic))
    result, updated, _ = structure_presentation(layout, semantic)
    assert [c['text'] for c in updated['answer']['choices']] == ['21', '22', '23', '24', '25']
    assert [c['label'] for c in updated['answer']['choices']] == list('①②③④⑤')
    assert all(len(c['source_refs']) == 2 for c in updated['answer']['choices'])
    assert structure_presentation(result, updated)[1] == updated
    assert (layout, semantic) == original


@pytest.mark.parametrize('patch', [
    {'mode': 'wrong'}, {'status': 'wrong'}, {'choices': []},
    {'mode': 'ox', 'answers': [{'value': 'maybe'}]},
    {'choices': [{'id': 'a', 'text': 'A', 'correct': False}]},
])
def test_invalid_review_is_rejected(patch):
    with pytest.raises(ValueError):
        normalize_review(review() | {'status': 'verified'} | patch)


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
