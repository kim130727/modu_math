from __future__ import annotations
from modu_math.dsl import Canvas, ProblemTemplate, Region, RectSlot, TextSlot


def build_problem_template() -> ProblemTemplate:
    return ProblemTemplate(
        id="S3_초등_3_008578",
        title="계산 결과가 가장 작은 것을 찾아 선택하세요.",
        canvas=Canvas(width=808, height=340, coordinate_mode="logical"),
        regions=(
            Region(
                id="region.stem",
                role="stem",
                flow="absolute",
                slot_ids=(
                    "slot.q1",
                    "slot.choice1_box",
                    "slot.choice1_text",
                    "slot.choice2_box",
                    "slot.choice2_text",
                    "slot.choice3_box",
                    "slot.choice3_text",
                ),
            ),
        ),
        slots=(
            TextSlot(
                id="slot.q1",
                prompt="",
                text="계산 결과가 가장 작은 것을 찾아 선택하세요.",
                style_role="question",
                x=51.002,
                y=73,
                font_size=30,
                fill="#111111",
            ),
            RectSlot(
                id="slot.choice1_box",
                prompt="",
                x=116.014,
                y=161,
                width=165,
                height=70,
                fill="#ffffff",
                stroke="#111111",
                stroke_width=1.5,
            ),
            TextSlot(
                id="slot.choice1_text",
                prompt="",
                text="328 × 8",
                style_role="question",
                x=141.014,
                y=206,
                font_size=30,
                fill="#111111",
            ),
            RectSlot(
                id="slot.choice2_box",
                prompt="",
                x=326.014,
                y=161,
                width=165,
                height=70,
                fill="#ffffff",
                stroke="#111111",
                stroke_width=1.5,
            ),
            TextSlot(
                id="slot.choice2_text",
                prompt="",
                text="524 × 5",
                style_role="question",
                x=356.014,
                y=206,
                font_size=30,
                fill="#111111",
            ),
            RectSlot(
                id="slot.choice3_box",
                prompt="",
                x=536.014,
                y=161,
                width=165,
                height=70,
                fill="#ffffff",
                stroke="#111111",
                stroke_width=1.5,
            ),
            TextSlot(
                id="slot.choice3_text",
                prompt="",
                text="752 × 3",
                style_role="question",
                x=561.014,
                y=206,
                font_size=30,
                fill="#111111",
            ),
        ),
        diagrams=(),
        groups=(),
        constraints=(),
        tags=(),
    )


PROBLEM_TEMPLATE = build_problem_template()

SEMANTIC_OVERRIDE = {
    "problem_id": "S3_초등_3_008578",
    "problem_type": "comparison_selection",
    "metadata": {
        "language": "ko",
        "question": "계산 결과가 가장 작은 것을 찾아 선택하세요.",
        "instruction": "곱셈식의 계산 결과를 비교하여 가장 작은 것을 고른다.",
    },
    "domain": {
        "objects": [
            {
                "id": "obj.expr1",
                "type": "multiplication_expression",
                "expression": "328 × 8",
            },
            {
                "id": "obj.expr2",
                "type": "multiplication_expression",
                "expression": "524 × 5",
            },
            {
                "id": "obj.expr3",
                "type": "multiplication_expression",
                "expression": "752 × 3",
            },
        ],
        "relations": [],
        "problem_solving": {
            "understand": {
                "given_refs": ["obj.expr1", "obj.expr2", "obj.expr3"],
                "target_ref": "answer.target",
                "condition_refs": ["rel.compare_results", "rel.minimum_selection"],
            },
            "plan": {
                "method": "compare_products",
                "description": "각 곱셈식의 결과를 비교하여 가장 작은 식을 찾는다.",
            },
            "execute": {
                "expected_operations": [
                    "multiply_each_expression",
                    "compare_results",
                    "select_minimum",
                ]
            },
            "review": {"check_methods": ["check_smallest_result", "check_selected_expression"]},
        },
    },
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {
            "type": "selected_expression",
            "description": "계산 결과가 가장 작은 곱셈식",
        },
        "value": 2256,
        "unit": "",
    },
}

SOLVABLE = {
    "schema": "modu.solvable.v1.1",
    "problem_id": "S3_초등_3_008578",
    "problem_type": "comparison_selection",
    "inputs": {
        "total_ticks": 3,
        "target_label": "가장 작은 것",
        "target_ticks": 1,
        "target_count": 1,
        "unit": "",
    },
    "given": [
        {"ref": "obj.expr1", "value": {"expression": "328 × 8"}},
        {"ref": "obj.expr2", "value": {"expression": "524 × 5"}},
        {"ref": "obj.expr3", "value": {"expression": "752 × 3"}},
    ],
    "target": {"ref": "answer.target", "type": "selected_expression"},
    "method": "compare_products",
    "plan": ["각 곱셈식의 결과를 구한 뒤, 가장 작은 결과를 가진 식을 찾는다."],
    "steps": [
        {"id": "step.1", "expr": "328 × 8", "value": 2624},
        {"id": "step.2", "expr": "524 × 5", "value": 2620},
        {"id": "step.3", "expr": "752 × 3", "value": 2256},
        {"id": "step.4", "expr": "min(2624, 2620, 2256)", "value": 2256},
    ],
    "checks": [
        {
            "id": "check.1",
            "expr": "2256 < 2620 and 2256 < 2624",
            "expected": True,
            "actual": True,
            "pass": True,
        },
        {
            "id": "check.2",
            "expr": "selected_expression == '752 × 3'",
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
            "description": "계산 결과가 가장 작은 곱셈식",
        },
        "value": 2256,
        "unit": "",
    },
}
