from copy import deepcopy

import pytest

from modu_math_web.editor.services.answer_review_sync import (
    ReviewMappingError,
    map_review,
)


def review(mode="panel_input", **fields):
    return {
        "mode": mode,
        "status": "verified",
        "note": "source note",
        "answers": [],
        "choices": [],
        **fields,
    }


@pytest.mark.parametrize("value", ["7", "-2.5", "3/7", "1 2/3"])
def test_numeric_answers_are_copied_without_localizing(value):
    result = map_review(
        review(answers=[{"value": value, "ref": "answer.value"}]), None, {}, {}, {}
    )
    assert result["answers"] == [{"value": value, "ref": "answer.value"}]
    assert result["status"] == "verified"
    assert result["note"] == ""


def test_ox_preserves_repeated_answers_and_target_note():
    source = review("ox", answers=[{"value": v} for v in ["O", "X", "O"]])
    target = review(note="Translated reviewer note")
    result = map_review(source, target, {}, {}, {})
    assert result["mode"] == "ox"
    assert result["answers"] == source["answers"]
    assert result["note"] == target["note"]


def test_choices_use_identity_even_when_target_order_differs():
    source = review(
        "choice",
        choices=[
            {"id": "a", "label": "1", "text": "가", "correct": True},
            {"id": "b", "label": "2", "text": "나", "correct": False},
        ],
    )
    target = review(
        "choice",
        choices=[
            {"id": "b", "label": "B", "text": "Beta", "correct": True},
            {"id": "a", "label": "A", "text": "Alpha", "correct": False},
        ],
    )
    snapshot = deepcopy(target)
    result = map_review(source, target, {}, {}, {})
    assert [
        (c["id"], c["text"], c["label"], c["correct"]) for c in result["choices"]
    ] == [("a", "Alpha", "A", True), ("b", "Beta", "B", False)]
    assert target == snapshot


def test_new_choices_resolve_translated_slot_text_without_copying_source_text():
    source = review(
        "choice",
        choices=[
            {
                "id": "c1",
                "label": "1",
                "text": "진경",
                "sourceRefs": ["slot.name.a"],
                "correct": True,
            },
            {
                "id": "c2",
                "label": "2",
                "text": "현진",
                "sourceRefs": ["slot.name.b"],
                "correct": False,
            },
        ],
    )
    slots = {
        "slot.name.a": {"content": {"text": "Jingyeong"}},
        "slot.name.b": {"content": {"text": "Hyeonjin"}},
    }
    result = map_review(source, None, {}, {}, slots)
    assert [c["text"] for c in result["choices"]] == ["Jingyeong", "Hyeonjin"]
    with pytest.raises(ReviewMappingError):
        map_review(source, None, {}, {}, {})


def test_unmapped_text_answer_is_not_copied_into_translation():
    source = review(answers=[{"value": "진경"}])
    with pytest.raises(ReviewMappingError):
        map_review(source, None, {}, {}, {})
    source_slots = {"slot.name": {"content": {"text": "진경"}}}
    target_slots = {"slot.name": {"content": {"text": "Jingyeong"}}}
    assert (
        map_review(source, None, {}, source_slots, target_slots)["answers"][0]["value"]
        == "Jingyeong"
    )


def test_group_choices_resolve_correct_value_after_reordering():
    source = review(
        "grouped_choice",
        groups=[
            {"id": "g1", "label": "질문", "choices": ["1", "2"], "correct_index": 0}
        ],
    )
    target = review(
        "grouped_choice",
        groups=[
            {"id": "g1", "label": "Question", "choices": ["2", "1"], "correct_index": 0}
        ],
    )
    result = map_review(source, target, {}, {}, {})
    assert result["groups"][0]["label"] == "Question"
    assert result["groups"][0]["choices"] == ["2", "1"]
    assert result["groups"][0]["correct_index"] == 1
    with pytest.raises(ReviewMappingError):
        map_review(source, None, {}, {}, {})


def test_canvas_mode_requires_existing_connected_input():
    source = review("canvas_slots", answers=[{"value": "8", "ref": "slot.answer"}])
    with pytest.raises(ReviewMappingError):
        map_review(source, None, {}, {}, {"slot.answer": {"content": {}}})
    slots = {"slot.answer": {"content": {"interaction": {"type": "input"}}}}
    assert map_review(source, None, {}, {}, slots)["answers"] == source["answers"]


def test_existing_numbered_choices_do_not_duplicate_their_labels():
    source = review(
        "choice",
        choices=[
            {"id": "a", "label": "①", "text": "가", "correct": True},
            {"id": "b", "label": "②", "text": "나", "correct": False},
        ],
    )
    detail = {
        "semantic": {
            "answer": {
                "choices": [
                    {"id": "a", "text": "① Alpha"},
                    {"id": "b", "text": "② Beta"},
                ]
            }
        }
    }
    result = map_review(source, None, detail, {}, {})
    assert [(c["label"], c["text"]) for c in result["choices"]] == [
        ("①", "Alpha"),
        ("②", "Beta"),
    ]
