from __future__ import annotations
from modu_math.dsl import Canvas, ProblemTemplate, Region, RectSlot, TextSlot


def build_problem_template() -> ProblemTemplate:
    return ProblemTemplate(
        id="S3_초등_3_008554",
        title="곱이 더 큰 것의 기호를 선택해 보세요.",
        canvas=Canvas(width=500.0, height=280.0, coordinate_mode="logical"),
        regions=(
            Region(
                id="region.stem",
                role="stem",
                flow="absolute",
                slot_ids=("slot.q1", "slot.box", "slot.opt1", "slot.opt2"),
            ),
            Region(
                id="region.answer_explanation",
                role="explanation",
                flow="absolute",
                slot_ids=(
                    "slot.answer",
                    "slot.explain1",
                    "slot.arrow",
                    "slot.explain2",
                ),
            ),
        ),
        slots=(
            TextSlot(
                id="slot.q1",
                prompt="",
                text="곱이 더 큰 것의 기호를 선택해 보세요.",
                style_role="question",
                x=18.002,
                y=45,
                font_size=28,
                fill="#111111",
            ),
            RectSlot(
                id="slot.box",
                prompt="",
                x=50,
                y=100,
                width=364,
                height=76,
                fill="none",
                stroke="#f6b7c3",
                stroke_width=1.5,
            ),
            TextSlot(
                id="slot.opt1",
                prompt="",
                text="① 6 × 65",
                style_role="question",
                x=100,
                y=150,
                font_size=28,
                fill="#111111",
            ),
            TextSlot(
                id="slot.opt2",
                prompt="",
                text="② 7 × 55",
                style_role="question",
                x=250,
                y=150,
                font_size=28,
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
    "problem_id": "S3_초등_3_008554",
    "problem_type": "compare_products",
    "metadata": {
        "language": "ko",
        "question": "곱이 더 큰 것의 기호를 선택해 보세요.",
        "instruction": "보기의 곱을 비교하여 더 큰 기호를 고른다.",
        "points": 1,
    },
    "domain": {
        "objects": [
            {"id": "obj.option1", "type": "expression", "label": "① 6 × 65"},
            {"id": "obj.option2", "type": "expression", "label": "② 7 × 55"},
            {"id": "obj.answer_mark", "type": "choice", "label": "①"},
        ],
        "relations": [],
        "problem_solving": {
            "understand": {
                "given_refs": ["obj.option1", "obj.option2"],
                "target_ref": "answer.target",
                "condition_refs": ["rel.compare_products"],
            },
            "plan": {
                "method": "product_comparison",
                "description": "각 보기의 곱을 비교하여 더 큰 쪽의 기호를 고른다.",
            },
            "execute": {
                "expected_operations": [
                    "calculate_each_product",
                    "compare_results",
                    "select_larger_choice",
                ]
            },
            "review": {"check_methods": ["compare_two_values", "match_with_printed_answer"]},
        },
    },
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {"type": "choice_symbol", "description": "곱이 더 큰 것의 기호"},
        "value": "①",
        "unit": "",
    },
}

SOLVABLE = {
    "schema": "modu.solvable.v1.1",
    "problem_id": "S3_초등_3_008554",
    "problem_type": "compare_products",
    "inputs": {
        "total_ticks": 2,
        "target_label": "곱이 더 큰 것의 기호",
        "target_ticks": 1,
        "target_count": 1,
        "unit": "",
    },
    "given": [
        {"ref": "obj.option1", "value": {"expression": "6 × 65"}},
        {"ref": "obj.option2", "value": {"expression": "7 × 55"}},
    ],
    "target": {"ref": "answer.target", "type": "choice_symbol"},
    "method": "product_comparison",
    "plan": [
        "두 보기의 곱을 각각 계산한다.",
        "계산 결과를 비교한다.",
        "더 큰 곱에 해당하는 기호를 선택한다.",
    ],
    "steps": [
        {"id": "step.1", "expr": "6 × 65", "value": 390},
        {"id": "step.2", "expr": "7 × 55", "value": 385},
        {"id": "step.3", "expr": "390 > 385", "value": True},
        {"id": "step.4", "expr": "더 큰 곱에 해당하는 기호 선택", "value": "①"},
    ],
    "checks": [
        {
            "id": "check.1",
            "expr": "390 > 385",
            "expected": True,
            "actual": True,
            "pass": True,
        },
        {
            "id": "check.2",
            "expr": "printed_answer == '①'",
            "expected": "①",
            "actual": "①",
            "pass": True,
        },
    ],
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {"type": "choice_symbol", "description": "곱이 더 큰 것의 기호"},
        "value": "①",
        "unit": "",
    },
}
