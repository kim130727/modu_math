from __future__ import annotations
from modu_math.dsl import Canvas, ProblemTemplate, RectSlot, Region, TextSlot


def build_problem_template() -> ProblemTemplate:
    return ProblemTemplate(
        id="S3_초등_3_008614",
        title="나머지가 6이 나올 수 없는 식",
        canvas=Canvas(width=872, height=240, coordinate_mode="logical"),
        regions=(
            Region(
                id="region.stem",
                role="stem",
                flow="absolute",
                slot_ids=("slot.q.no", "slot.q.text"),
            ),
            Region(
                id="region.choices",
                role="choices",
                flow="absolute",
                slot_ids=(
                    "slot.choice.1.box",
                    "slot.choice.1.text",
                    "slot.choice.2.box",
                    "slot.choice.2.text",
                    "slot.choice.3.box",
                    "slot.choice.3.text",
                ),
            ),
            Region(
                id="region.answer_explanation",
                role="explanation",
                flow="absolute",
                slot_ids=("slot.answer.box",),
            ),
        ),
        slots=(
            TextSlot(
                id="slot.q.no",
                prompt="",
                text="84.",
                style_role="question",
                x=8.0,
                y=18.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.q.text",
                prompt="",
                text="84. 나머지가 6이 나올 수 없는 식을 찾아 선택해 보세요.",
                style_role="question",
                x=28.0,
                y=18.0,
                font_size=28,
            ),
            RectSlot(
                id="slot.choice.1.box",
                prompt="",
                x=85.0,
                y=47.0,
                width=180.0,
                height=78.0,
            ),
            TextSlot(
                id="slot.choice.1.text",
                prompt="",
                text="□ ÷ 8",
                style_role="choice",
                x=142.0,
                y=98.0,
                font_size=28,
            ),
            RectSlot(
                id="slot.choice.2.box",
                prompt="",
                x=383.0,
                y=47.0,
                width=180.0,
                height=78.0,
            ),
            TextSlot(
                id="slot.choice.2.text",
                prompt="",
                text="□ ÷ 6",
                style_role="choice",
                x=440.0,
                y=98.0,
                font_size=28,
            ),
            RectSlot(
                id="slot.choice.3.box",
                prompt="",
                x=679.0,
                y=47.0,
                width=180.0,
                height=78.0,
            ),
            TextSlot(
                id="slot.choice.3.text",
                prompt="",
                text="□ ÷ 9",
                style_role="choice",
                x=736.0,
                y=98.0,
                font_size=28,
            ),
            RectSlot(
                id="slot.answer.box",
                prompt="",
                x=65.0,
                y=146.0,
                width=24.0,
                height=24.0,
            ),
        ),
        diagrams=(),
        groups=(),
        constraints=(),
        tags=("초등", "수학", "나눗셈", "나머지", "선택형"),
    )


PROBLEM_TEMPLATE = build_problem_template()

SEMANTIC_OVERRIDE = {
    "problem_id": "S3_초등_3_008614",
    "problem_type": "multiple_choice_division_remainder",
    "metadata": {
        "language": "ko",
        "question": "나머지가 6이 나올 수 없는 식을 찾아 선택해 보세요.",
        "instruction": "나머지가 6이 나올 수 없는 식을 찾아 선택해 보세요.",
    },
    "domain": {
        "objects": [
            {"id": "obj.choice.1", "type": "division_expression", "divisor": 8},
            {"id": "obj.choice.2", "type": "division_expression", "divisor": 6},
            {"id": "obj.choice.3", "type": "division_expression", "divisor": 9},
        ],
        "relations": [],
        "problem_solving": {
            "understand": {
                "given_refs": ["obj.choice.1", "obj.choice.2", "obj.choice.3"],
                "target_ref": "answer.target",
                "condition_refs": ["rel.remainder_constraint"],
            },
            "plan": {
                "method": "compare_remainder_with_divisor",
                "description": "각 보기에서 나머지 6이 가능한지 나누는 수와 비교해 본다.",
            },
            "execute": {
                "expected_operations": [
                    "inspect_each_choice",
                    "apply_remainder_constraint",
                ]
            },
            "review": {
                "check_methods": ["unit_consistency_check", "remainder_range_check"]
            },
        },
    },
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {
            "type": "selected_expression",
            "description": "나머지가 6이 나올 수 없는 식",
        },
        "value": 0,
        "unit": "",
    },
}

SOLVABLE = {
    "schema": "modu.solvable.v1.1",
    "problem_id": "S3_초등_3_008614",
    "problem_type": "multiple_choice_division_remainder",
    "inputs": {
        "total_ticks": 0,
        "target_label": "나머지가 6이 나올 수 없는 식",
        "target_ticks": 0,
        "target_count": 1,
        "unit": "",
    },
    "given": [
        {"ref": "obj.choice.1", "value": {"divisor": 8}},
        {"ref": "obj.choice.2", "value": {"divisor": 6}},
        {"ref": "obj.choice.3", "value": {"divisor": 9}},
    ],
    "target": {"ref": "answer.target", "type": "selected_expression"},
    "method": "compare_remainder_with_divisor",
    "plan": ["각 보기에서 나머지 6이 가능한지 나누는 수와 비교해 본다."],
    "steps": [
        {"id": "step.1", "expr": "나머지는 나누는 수보다 작아야 한다.", "value": 0},
        {"id": "step.2", "expr": "6 < 8 ?", "value": True},
        {"id": "step.3", "expr": "6 < 6 ?", "value": False},
        {"id": "step.4", "expr": "6 < 9 ?", "value": True},
    ],
    "checks": [
        {
            "id": "check.1",
            "expr": "remainder_range_check",
            "expected": True,
            "actual": True,
            "pass": True,
        }
    ],
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {
            "type": "selected_expression",
            "description": "나머지가 6이 나올 수 없는 식",
        },
        "value": 0,
        "unit": "",
    },
}

