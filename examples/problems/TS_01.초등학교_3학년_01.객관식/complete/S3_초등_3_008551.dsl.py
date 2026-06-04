from __future__ import annotations

from modu_math.dsl import Canvas, ProblemTemplate, RectSlot, Region, TextSlot


PROBLEM_ID = "S3_초등_3_008551"


def build_problem_template() -> ProblemTemplate:
    return ProblemTemplate(
        id=PROBLEM_ID,
        title="곱이 가장 큰 것 선택",
        canvas=Canvas(width=872, height=267, coordinate_mode="logical"),
        regions=(
            Region(
                id="region.stem",
                role="stem",
                flow="absolute",
                slot_ids=(
                    "slot.q.text",
                    "slot.choice.box",
                    "slot.choice.a",
                    "slot.choice.b",
                    "slot.choice.c",
                ),
            ),
        ),
        slots=(
            TextSlot(
                id="slot.q.text",
                prompt="",
                text="곱이 가장 큰 것을 선택하십시오.",
                style_role="question",
                x=60.0,
                y=29.0,
                font_size=28,
            ),
            RectSlot(
                id="slot.choice.box",
                prompt="",
                x=97.0,
                y=45.0,
                width=744.0,
                height=79.0,
                fill="#D9DDF3",
                stroke="#A79CDC",
                stroke_width=2.0,
            ),
            TextSlot(
                id="slot.choice.a",
                prompt="",
                text="83 × 60",
                style_role="choice",
                x=185.0,
                y=93.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.choice.b",
                prompt="",
                text="77 × 70",
                style_role="choice",
                x=426.0,
                y=93.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.choice.c",
                prompt="",
                text="95 × 40",
                style_role="choice",
                x=673.0,
                y=93.0,
                font_size=28,
            ),
        ),
        diagrams=(),
        groups=(),
        constraints=(),
        tags=("선택형", "곱셈비교"),
    )


PROBLEM_TEMPLATE = build_problem_template()


SEMANTIC_OVERRIDE = {
    "problem_id": PROBLEM_ID,
    "problem_type": "compare_products",
    "metadata": {
        "language": "ko",
        "question": "곱이 가장 큰 것을 선택하십시오.",
        "instruction": "곱이 가장 큰 곱셈식을 고른다.",
    },
    "domain": {
        "objects": [
            {
                "id": "obj.choice.a",
                "type": "multiplication_expression",
                "expression": "83 × 60",
            },
            {
                "id": "obj.choice.b",
                "type": "multiplication_expression",
                "expression": "77 × 70",
            },
            {
                "id": "obj.choice.c",
                "type": "multiplication_expression",
                "expression": "95 × 40",
            },
        ],
        "relations": [],
        "problem_solving": {
            "understand": {
                "given_refs": [
                    "obj.choice.a",
                    "obj.choice.b",
                    "obj.choice.c",
                ],
                "target_ref": "answer.target",
                "condition_refs": ["rel.compare.products"],
            },
            "plan": {
                "method": "compute_and_compare_products",
                "description": "각 곱셈식의 곱을 구한 뒤 가장 큰 값을 찾는다.",
            },
            "execute": {
                "expected_operations": [
                    "compute_products",
                    "compare_values",
                ],
            },
            "review": {
                "check_methods": ["largest_product_check"],
            },
        },
    },
    "answer": {
        "value": 5390,
        "unit": "",
        "derived_from": "step.2",
    },
}


SOLVABLE = {
    "schema": "modu.solvable.v1.1",
    "problem_id": PROBLEM_ID,
    "problem_type": "compare_products",
    "inputs": {
        "total_ticks": 3,
        "target_label": "가장 큰 곱",
        "target_ticks": 1,
        "target_count": 1,
        "unit": "",
    },
    "given": [
        {
            "ref": "obj.choice.a",
            "value": {"expression": "83 × 60"},
        },
        {
            "ref": "obj.choice.b",
            "value": {"expression": "77 × 70"},
        },
        {
            "ref": "obj.choice.c",
            "value": {"expression": "95 × 40"},
        },
    ],
    "target": {
        "ref": "answer.target",
        "type": "selected_expression",
    },
    "method": "compute_and_compare_products",
    "plan": [
        "각 식의 곱을 계산해 값을 비교한다.",
        "가장 큰 곱을 만든 식을 선택한다.",
    ],
    "steps": [
        {
            "id": "step.1",
            "expr": "83 × 60",
            "value": 4980,
        },
        {
            "id": "step.2",
            "expr": "77 × 70",
            "value": 5390,
        },
        {
            "id": "step.3",
            "expr": "95 × 40",
            "value": 3800,
        },
        {
            "id": "step.4",
            "expr": "5390 > 4980 > 3800",
            "value": "77 × 70",
        },
    ],
    "checks": [
        {
            "id": "check.1",
            "expr": "max(4980, 5390, 3800)",
            "expected": 5390,
            "actual": 5390,
            "pass": True,
        },
        {
            "id": "check.2",
            "expr": "selected_expression",
            "expected": "77 × 70",
            "actual": "77 × 70",
            "pass": True,
        },
    ],
    "answer": {
        "value": 5390,
        "unit": "",
        "derived_from": "step.2",
    },
}


SEMANTIC_ANSWER = SOLVABLE["answer"]
