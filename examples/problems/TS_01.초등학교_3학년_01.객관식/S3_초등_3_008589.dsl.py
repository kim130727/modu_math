from __future__ import annotations
from modu_math.dsl import Canvas, ProblemTemplate, Region, RectSlot, TextSlot


def build_problem_template() -> ProblemTemplate:
    return ProblemTemplate(
        id="S3_초등_3_008589",
        title="나머지가 더 큰 것을 선택하세요.",
        canvas=Canvas(width=720, height=352, coordinate_mode="logical"),
        regions=(
            Region(
                id="region.stem",
                role="stem",
                flow="absolute",
                slot_ids=("slot.q1", "slot.q2", "slot.q3", "slot.q7"),
            ),
        ),
        slots=(
            TextSlot(
                id="slot.q1",
                prompt="",
                text="56. 나머지가 더 큰 것을 선택하세요.",
                style_role="question",
                x=12.0,
                y=28.0,
                font_size=28,
            ),
            RectSlot(
                id="slot.box.left", prompt="", x=180.0, y=48.0, width=190.0, height=80.0
            ),
            RectSlot(
                id="slot.box.right",
                prompt="",
                x=440.0,
                y=48.0,
                width=190.0,
                height=80.0,
            ),
            TextSlot(
                id="slot.q2",
                prompt="",
                text="24 ÷ 7",
                style_role="question",
                x=233.0,
                y=96.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.q3",
                prompt="",
                text="49 ÷ 5",
                style_role="question",
                x=493.0,
                y=96.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.q7",
                prompt="",
                text="",
                style_role="note",
                x=0.0,
                y=0.0,
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
    "problem_id": "S3_초등_3_008589",
    "problem_type": "division_remainder_compare",
    "metadata": {
        "language": "ko",
        "question": "나머지가 더 큰 것을 선택하세요.",
        "instruction": "두 나눗셈의 나머지를 비교하여 더 큰 것을 고르세요.",
    },
    "domain": {
        "objects": [
            {
                "id": "obj.left_division",
                "type": "division_expression",
                "expression": "24 ÷ 7",
            },
            {
                "id": "obj.right_division",
                "type": "division_expression",
                "expression": "49 ÷ 5",
            },
            {"id": "obj.left_remainder", "type": "remainder", "value": 3},
            {"id": "obj.right_remainder", "type": "remainder", "value": 4},
        ],
        "relations": [],
        "problem_solving": {
            "understand": {
                "given_refs": ["obj.left_division", "obj.right_division"],
                "target_ref": "answer.target",
                "condition_refs": ["rel.compare_remainder"],
            },
            "plan": {
                "method": "compare_remainders",
                "description": "각 나눗셈의 나머지를 비교하여 더 큰 쪽을 선택한다.",
            },
            "execute": {
                "expected_operations": [
                    "find_remainder_of_each_division",
                    "compare_two_remainders",
                    "select_larger_remainder_expression",
                ]
            },
            "review": {
                "check_methods": [
                    "remainder_comparison_check",
                    "selection_consistency_check",
                ]
            },
        },
    },
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {
            "type": "selected_expression",
            "description": "나머지가 더 큰 나눗셈식",
        },
        "value": "49 ÷ 5",
        "unit": "",
    },
}

SOLVABLE = {
    "schema": "modu.solvable.v1.1",
    "problem_id": "S3_초등_3_008589",
    "problem_type": "division_remainder_compare",
    "inputs": {
        "total_ticks": 0,
        "target_label": "selected_expression",
        "target_ticks": 0,
        "target_count": 1,
        "unit": "",
    },
    "given": [
        {"ref": "obj.left_division", "value": {"expression": "24 ÷ 7"}},
        {"ref": "obj.right_division", "value": {"expression": "49 ÷ 5"}},
    ],
    "target": {"ref": "answer.target", "type": "selected_expression"},
    "method": "compare_remainders",
    "plan": ["각 나눗셈의 나머지를 비교하여 더 큰 나머지를 가진 식을 선택한다."],
    "steps": [
        {"id": "step.1", "expr": "24 ÷ 7의 나머지 확인", "value": 3},
        {"id": "step.2", "expr": "49 ÷ 5의 나머지 확인", "value": 4},
        {"id": "step.3", "expr": "4 > 3", "value": True},
        {"id": "step.4", "expr": "나머지가 더 큰 식 선택", "value": "49 ÷ 5"},
    ],
    "checks": [
        {
            "id": "check.1",
            "expr": "선택한 식의 나머지가 더 큰가",
            "expected": True,
            "actual": True,
            "pass": True,
        },
        {
            "id": "check.2",
            "expr": "49 ÷ 5의 나머지가 24 ÷ 7의 나머지보다 큰가",
            "expected": True,
            "actual": True,
            "pass": True,
        },
    ],
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {
            "type": "selected_expression",
            "description": "나머지가 더 큰 나눗셈식",
        },
        "value": "49 ÷ 5",
        "unit": "",
    },
}

