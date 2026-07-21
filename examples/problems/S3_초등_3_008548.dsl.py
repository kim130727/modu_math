from __future__ import annotations
from modu_math.dsl import Canvas, ProblemTemplate, Region, TextSlot, RectSlot


def build_problem_template() -> ProblemTemplate:
    return ProblemTemplate(
        id="S3_초등_3_008548",
        title="곱이 더 큰 것을 선택해 보세요.",
        canvas=Canvas(width=500, height=246, coordinate_mode="logical"),
        regions=(
            Region(
                id="region.stem",
                role="stem",
                flow="absolute",
                slot_ids=(
                    "slot.q2",
                    "slot.box",
                    "slot.choice1",
                    "slot.choice2",
                ),
            ),
            Region(
                id="region.answer_explanation",
                role="explanation",
                flow="absolute",
                slot_ids=(
                    
                    
                ),
            ),
        ),
        slots=(
            TextSlot(
                id="slot.q2",
                prompt="",
                text="곱이 더 큰 것을 선택해 보세요.",
                style_role="question",
                x=56.0,
                y=44.0,
                font_size=28,
            ),
            RectSlot(
                id="slot.box",
                prompt="",
                x = 45, y = 65, width=391.0,
                height=79.0,
                fill="none",
                stroke="#ffb6c1",
            ),
            TextSlot(
                id="slot.choice1",
                prompt="",
                text="① 5 × 63",
                style_role="answer_choice",
                x = 80, y = 115, font_size=28,
            ),
            TextSlot(
                id="slot.choice2",
                prompt="",
                text="② 7 × 42",
                style_role="answer_choice",
                x = 270, y = 115, font_size=28,
            ),
        ),
        diagrams=(),
        groups=(),
        constraints=(),
        tags=(),
    )


PROBLEM_TEMPLATE = build_problem_template()

SEMANTIC_OVERRIDE = {
    "problem_id": "S3_초등_3_008548",
    "problem_type": "compare_products",
    "metadata": {
        "language": "ko",
        "question": "곱이 더 큰 것을 선택해 보세요.",
        "instruction": "보기의 두 곱셈식의 결과를 비교하여 더 큰 것을 고른다.",
    },
    "domain": {
        "objects": [
            {
                "id": "obj.choice_1",
                "type": "multiplication_expression",
                "factors": [5, 63],
            },
            {
                "id": "obj.choice_2",
                "type": "multiplication_expression",
                "factors": [7, 42],
            },
        ],
        "relations": [],
        "problem_solving": {
            "understand": {
                "given_refs": ["obj.choice_1", "obj.choice_2"],
                "target_ref": "answer.target",
                "condition_refs": ["rel.compare_products"],
            },
            "plan": {
                "method": "compare_product_values",
                "description": "각 곱셈식의 값을 비교하여 더 큰 것을 고른다.",
            },
            "execute": {
                "expected_operations": [
                    "compute_product_1",
                    "compute_product_2",
                    "compare_results",
                ]
            },
            "review": {"check_methods": ["greater_than_check"]},
        },
    },
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {"type": "choice", "description": "곱이 더 큰 보기"},
        "value": 1,
        "unit": "",
    },
}

SOLVABLE = {
    "schema": "modu.solvable.v1.1",
    "problem_id": "S3_초등_3_008548",
    "problem_type": "compare_products",
    "inputs": {
        "total_ticks": 2,
        "target_label": "곱이 더 큰 보기",
        "target_ticks": 1,
        "target_count": 2,
        "unit": "",
    },
    "given": [
        {"ref": "obj.choice_1", "value": {"factors": [5, 63]}},
        {"ref": "obj.choice_2", "value": {"factors": [7, 42]}},
    ],
    "target": {"ref": "answer.target", "type": "choice"},
    "method": "compare_product_values",
    "plan": ["각 보기의 곱을 구한 뒤 더 큰 값을 선택한다."],
    "steps": [
        {"id": "step.1", "expr": "5 × 63", "value": 315},
        {"id": "step.2", "expr": "7 × 42", "value": 294},
        {"id": "step.3", "expr": "315 > 294", "value": True},
    ],
    "checks": [
        {
            "id": "check.1",
            "expr": "315 > 294",
            "expected": True,
            "actual": True,
            "pass": True,
        },
        {
            "id": "check.2",
            "expr": "선택한 보기 = ①",
            "expected": 1,
            "actual": 1,
            "pass": True,
        },
    ],
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {"type": "choice", "description": "곱이 더 큰 보기"},
        "value": 1,
        "unit": "",
    },
}
