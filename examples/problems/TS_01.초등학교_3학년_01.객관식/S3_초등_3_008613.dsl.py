from __future__ import annotations
from modu_math.dsl import Canvas, ProblemTemplate, RectSlot, Region, TextSlot


def build_problem_template() -> ProblemTemplate:
    return ProblemTemplate(
        id="S3_초등_3_008613",
        title="나머지가 3이 나올 수 없는 식",
        canvas=Canvas(width=880, height=240, coordinate_mode="logical"),
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
                slot_ids=(),
            ),
        ),
        slots=(
            TextSlot(
                id="slot.q.no",
                prompt="",
                text="83.",
                style_role="question",
                x=44.0,
                y=28.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.q.text",
                prompt="",
                text="나머지가 3이 나올 수 없는 식을 찾아 선택해 보세요.",
                style_role="question",
                x=88.0,
                y=28.0,
                font_size=28,
            ),
            RectSlot(
                id="slot.choice.1.box",
                prompt="",
                x=124.0,
                y=50.0,
                width=182.0,
                height=80.0,
            ),
            TextSlot(
                id="slot.choice.1.text",
                prompt="",
                text="□ ÷ 3",
                style_role="choice",
                x=176.0,
                y=100.0,
                font_size=28,
            ),
            RectSlot(
                id="slot.choice.2.box",
                prompt="",
                x=350.0,
                y=50.0,
                width=182.0,
                height=80.0,
            ),
            TextSlot(
                id="slot.choice.2.text",
                prompt="",
                text="□ ÷ 5",
                style_role="choice",
                x=402.0,
                y=100.0,
                font_size=28,
            ),
            RectSlot(
                id="slot.choice.3.box",
                prompt="",
                x=576.0,
                y=50.0,
                width=182.0,
                height=80.0,
            ),
            TextSlot(
                id="slot.choice.3.text",
                prompt="",
                text="□ ÷ 7",
                style_role="choice",
                x=628.0,
                y=100.0,
                font_size=28,
            ),
        ),
        diagrams=(),
        groups=(),
        constraints=(),
        tags=("초등", "수학", "나눗셈", "나머지", "선택형"),
    )


PROBLEM_TEMPLATE = build_problem_template()

SEMANTIC_OVERRIDE = {
    "problem_id": "S3_초등_3_008613",
    "problem_type": "multiple_choice_division_remainder",
    "metadata": {
        "language": "ko",
        "question": "나머지가 3이 나올 수 없는 식을 찾아 선택해 보세요.",
        "instruction": "나머지가 3이 나올 수 없는 식을 찾아 선택해 보세요.",
    },
    "domain": {
        "objects": [
            {"id": "obj.choice.1", "type": "division_expression", "divisor": 3},
            {"id": "obj.choice.2", "type": "division_expression", "divisor": 5},
            {"id": "obj.choice.3", "type": "division_expression", "divisor": 7},
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
                "description": "각 보기에서 나머지 3이 가능한지 나누는 수와 비교해 본다.",
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
            "description": "나머지가 3이 나올 수 없는 식",
        },
        "value": 0,
        "unit": "",
    },
}

SOLVABLE = {
    "schema": "modu.solvable.v1.1",
    "problem_id": "S3_초등_3_008613",
    "problem_type": "multiple_choice_division_remainder",
    "inputs": {
        "total_ticks": 0,
        "target_label": "나머지가 3이 나올 수 없는 식",
        "target_ticks": 0,
        "target_count": 1,
        "unit": "",
    },
    "given": [
        {"ref": "obj.choice.1", "value": {"divisor": 3}},
        {"ref": "obj.choice.2", "value": {"divisor": 5}},
        {"ref": "obj.choice.3", "value": {"divisor": 7}},
    ],
    "target": {"ref": "answer.target", "type": "selected_expression"},
    "method": "compare_remainder_with_divisor",
    "plan": ["각 보기에서 나머지 3이 가능한지 나누는 수와 비교해 본다."],
    "steps": [
        {"id": "step.1", "expr": "나머지는 나누는 수보다 작아야 한다.", "value": 0},
        {"id": "step.2", "expr": "3 < 3 ?", "value": False},
        {"id": "step.3", "expr": "3 < 5 ?", "value": True},
        {"id": "step.4", "expr": "3 < 7 ?", "value": True},
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
            "description": "나머지가 3이 나올 수 없는 식",
        },
        "value": 0,
        "unit": "",
    },
}
