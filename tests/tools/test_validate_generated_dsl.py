from __future__ import annotations

import pytest

from modu_math.dsl import Canvas, ProblemTemplate, Region, TextSlot
from tools.validate_generated_dsl import (
    _assert_bundle_consistency,
    validate_answer_alignment_source,
    validate_required_layout_ids,
)


def _problem(problem_id: str = "p.test") -> ProblemTemplate:
    return ProblemTemplate(
        id=problem_id,
        title="t",
        canvas=Canvas(width=100, height=100),
        regions=(Region(id="region.stem", role="stem", slot_ids=("slot.a", "slot.b")),),
        slots=(
            TextSlot(id="slot.a", text="a"),
            TextSlot(id="slot.b", text="b"),
        ),
    )


def _layout() -> dict:
    return {
        "problem_id": "p.test",
        "canvas": {"width": 100, "height": 100, "dpi": 96},
        "regions": [{"id": "region.stem", "role": "stem", "slot_ids": ["slot.a", "slot.b"]}],
        "slots": [
            {"id": "slot.a", "kind": "text", "bbox": {"x": 0, "y": 0, "w": 1, "h": 1}},
            {"id": "slot.b", "kind": "text", "bbox": {"x": 0, "y": 0, "w": 1, "h": 1}},
        ],
        "diagrams": [],
    }


def test_bundle_consistency_accepts_matching_ids_and_answers() -> None:
    _assert_bundle_consistency(
        problem=_problem(),
        semantic_override={
            "problem_id": "p.test",
            "metadata": {"required_layout_ids": ["slot.a"]},
            "answer": {"value": ">"},
        },
        solvable={"problem_id": "p.test", "answer": {"value": ">"}},
        layout=_layout(),
    )


def test_bundle_consistency_rejects_template_override_id_mismatch() -> None:
    with pytest.raises(ValueError, match="ProblemTemplate.id must match SEMANTIC_OVERRIDE.problem_id"):
        _assert_bundle_consistency(
            problem=_problem("p.other"),
            semantic_override={"problem_id": "p.test", "answer": {"value": "1"}},
            solvable=None,
            layout=_layout(),
        )


def test_bundle_consistency_rejects_override_solvable_answer_value_mismatch() -> None:
    with pytest.raises(ValueError, match="SEMANTIC_OVERRIDE.answer.value must match SOLVABLE.answer.value"):
        _assert_bundle_consistency(
            problem=_problem(),
            semantic_override={"problem_id": "p.test", "answer": {"value": "<"}},
            solvable={"problem_id": "p.test", "answer": {"value": ">"}},
            layout=_layout(),
        )


def test_validate_required_layout_ids_accepts_empty_list() -> None:
    errors = validate_required_layout_ids(
        semantic={"metadata": {"required_layout_ids": []}},
        layout=_layout(),
    )
    assert errors == []


def test_validate_required_layout_ids_accepts_existing_id() -> None:
    errors = validate_required_layout_ids(
        semantic={"metadata": {"required_layout_ids": ["slot.a"]}},
        layout=_layout(),
    )
    assert errors == []


def test_validate_required_layout_ids_rejects_missing_id() -> None:
    errors = validate_required_layout_ids(
        semantic={"metadata": {"required_layout_ids": ["slot.answer"]}},
        layout=_layout(),
    )
    assert errors == [
        "semantic.metadata.required_layout_ids contains missing layout slot ids: slot.answer"
    ]


def test_validate_required_layout_ids_rejects_non_list() -> None:
    errors = validate_required_layout_ids(
        semantic={"metadata": {"required_layout_ids": "slot.a"}},
        layout=_layout(),
    )
    assert errors == ["semantic.metadata.required_layout_ids must be an array"]


def test_validate_answer_alignment_source_rejects_forbidden_direction() -> None:
    source = "SEMANTIC_OVERRIDE['answer'] = SOLVABLE['answer']\n"
    errors = validate_answer_alignment_source(source)
    assert errors == [
        "Forbidden answer alignment detected: "
        "SEMANTIC_OVERRIDE['answer'] = SOLVABLE['answer'] is not allowed."
    ]


def test_validate_answer_alignment_source_accepts_safe_alignment() -> None:
    source = (
        "_answer = dict(SEMANTIC_OVERRIDE['answer'])\n"
        "_answer.setdefault('blanks', [])\n"
        "SOLVABLE['answer'] = _answer\n"
    )
    errors = validate_answer_alignment_source(source)
    assert errors == []


def test_bundle_consistency_rejects_region_slot_not_in_layout_slots() -> None:
    broken_layout = _layout()
    broken_layout["slots"] = [broken_layout["slots"][0]]
    with pytest.raises(ValueError, match="references slot_ids not present in layout.slots"):
        _assert_bundle_consistency(
            problem=_problem(),
            semantic_override={"problem_id": "p.test", "answer": {"value": "x"}},
            solvable=None,
            layout=broken_layout,
        )
