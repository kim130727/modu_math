from __future__ import annotations
from modu_math.dsl import Canvas, ProblemTemplate, Region, RectSlot, TextSlot


def build_problem_template() -> ProblemTemplate:
    return ProblemTemplate(
        id="S3_초등_3_008793",
        title="들이가 100 mL보다 더 많은 것을 선택하세요",
        canvas=Canvas(width=849, height=457, coordinate_mode="logical"),
        regions=(
            Region(id="region.stem", role="stem", flow="absolute", slot_ids=("slot.q1", "slot.q2")),
            Region(
                id="region.example",
                role="diagram",
                flow="absolute",
                slot_ids=(
                    "slot.box",
                    "slot.box.title",
                    "slot.box.item",
                    "slot.box.label",
                    "slot.syringe",
                    "slot.bottle.top",
                ),
            ),
            Region(id="region.explanation", role="explanation", flow="absolute", slot_ids=()),
        ),
        slots=(
            TextSlot(
                id="slot.q1",
                prompt="",
                text="18.",
                style_role="question",
                x=11.0,
                y=31.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.q2",
                prompt="",
                text="들이가 100 mL보다 더 많은 것을 선택하세요.",
                style_role="question",
                x=55.0,
                y=31.0,
                font_size=28,
            ),
            RectSlot(
                id="slot.box",
                prompt="",
                x=159.0,
                y=47.0,
                width=238.0,
                height=183.0,
                fill="none",
                stroke="#8F8F8F",
                stroke_width=2.0,
            ),
            TextSlot(
                id="slot.box.title",
                prompt="",
                text="<보기>",
                style_role="label",
                x=174.0,
                y=90.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.box.item",
                prompt="",
                text="",
                style_role="label",
                x=256.0,
                y=138.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.box.label",
                prompt="",
                text="100 mL",
                style_role="label",
                x=245.0,
                y=209.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.syringe",
                prompt="",
                text="",
                style_role="label",
                x=449.0,
                y=141.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.bottle.top",
                prompt="",
                text="",
                style_role="label",
                x=683.0,
                y=111.0,
                font_size=28,
            ),
        ),
        diagrams=(),
        groups=(),
        constraints=(),
        tags=(),
    )


PROBLEM_TEMPLATE = build_problem_template()

SEMANTIC_OVERRIDE = {
    "problem_id": "S3_초등_3_008793",
    "problem_type": "comparison_selection",
    "metadata": {
        "language": "ko",
        "question": "들이가 100 mL보다 더 많은 것을 선택하세요.",
        "instruction": "100 mL보다 더 많은 대상을 고르는 문제이다.",
    },
    "domain": {
        "objects": [
            {"id": "obj.reference_capacity", "type": "capacity", "value": 100, "unit": "mL"},
            {
                "id": "obj.choice_container",
                "type": "container",
                "capacity_relation": "greater_than_reference",
            },
        ],
        "relations": [],
        "problem_solving": {
            "understand": {
                "given_refs": ["obj.reference_capacity"],
                "target_ref": "answer.target",
                "condition_refs": ["rel.compare_capacity"],
            },
            "plan": {
                "method": "capacity_comparison",
                "description": "기준인 100 mL보다 더 큰 대상을 고른다.",
            },
            "execute": {"expected_operations": ["compare_capacity"]},
            "review": {"check_methods": ["greater_than_100mL_check"]},
        },
    },
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {"type": "selected_object", "description": "100 mL보다 더 많은 것"},
        "value": 0,
        "unit": "",
    },
}

SOLVABLE = {
    "schema": "modu.solvable.v1.1",
    "problem_id": "S3_초등_3_008793",
    "problem_type": "comparison_selection",
    "inputs": {
        "total_ticks": 1,
        "target_label": "100 mL보다 더 많은 것",
        "target_ticks": 1,
        "target_count": 1,
        "unit": "mL",
    },
    "given": [{"ref": "obj.reference_capacity", "value": {"value": 100, "unit": "mL"}}],
    "target": {"ref": "answer.target", "type": "selected_object"},
    "plan": "100 mL와 각 대상을 비교하여 더 큰 용량을 고른다.",
    "method": "capacity_comparison",
    "steps": [
        {"id": "step.1", "expr": "기준 용량 확인", "value": 100},
        {"id": "step.2", "expr": "100 mL보다 큰 대상을 선택", "value": 0},
    ],
    "checks": [
        {
            "id": "check.1",
            "expr": "선택한 대상의 용량 > 100 mL",
            "expected": True,
            "actual": True,
            "pass": True,
        }
    ],
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {"type": "selected_object", "description": "100 mL보다 더 많은 것"},
        "value": 0,
        "unit": "",
    },
}
