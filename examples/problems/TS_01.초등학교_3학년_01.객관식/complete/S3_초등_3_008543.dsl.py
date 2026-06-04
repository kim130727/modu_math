from __future__ import annotations
from modu_math.dsl import (
    Canvas,
    CircleSlot,
    ProblemTemplate,
    RectSlot,
    Region,
    TextSlot,
)


def build_problem_template() -> ProblemTemplate:
    return ProblemTemplate(
        id="S3_초등_3_008543",
        title="계산 결과가 큰 것부터 순서대로 나열한 것을 고르세요.",
        canvas=Canvas(width=944.0, height=392.0, coordinate_mode="logical"),
        regions=(
            Region(
                id="region.stem",
                role="stem",
                flow="absolute",
                slot_ids=(
                    "slot.q.text",
                    "slot.box",
                    "slot.box.eq1",
                    "slot.box.eq2",
                    "slot.box.eq3",
                ),
            ),
            Region(
                id="region.choices",
                role="choices",
                flow="absolute",
                slot_ids=(
                    "slot.choice.1",
                    "slot.choice.2",
                    "slot.choice.3",
                    "slot.choice.4",
                ),
            ),
            Region(
                id="region.answer",
                role="answer",
                flow="absolute",
                slot_ids=(
                    
                    
                ),
            ),
        ),
        slots=(
            TextSlot(
                id="slot.q.text",
                prompt="",
                text="계산 결과가 큰 것부터 순서대로 나열한 것을 고르세요.",
                style_role="question",
                x = 85, y = 35, font_size=28,
            ),
            RectSlot(
                id="slot.box",
                prompt="",
                x=92.0,
                y=58.0,
                width=792.0,
                height=78.0,
                fill="#D9DDF3",
                stroke="#A79CDC",
                stroke_width=2.0,
            ),
            TextSlot(
                id="slot.box.eq1",
                prompt="",
                text="ㄱ. 4 × 28",
                style_role="body",
                x = 220, y = 105, font_size=28,
            ),
            TextSlot(
                id="slot.box.eq2",
                prompt="",
                text="ㄴ. 3 × 34",
                style_role="body",
                x = 450, y = 105, font_size=28,
            ),
            TextSlot(
                id="slot.box.eq3",
                prompt="",
                text="ㄷ. 2 × 76",
                style_role="body",
                x=681.0,
                y=105.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.choice.1",
                prompt="",
                text="① ㄱ, ㄴ, ㄷ",
                style_role="choice",
                x = 95, y = 180, font_size=28,
            ),
            TextSlot(
                id="slot.choice.2",
                prompt="",
                text="② ㄷ, ㄴ, ㄱ",
                style_role="choice",
                x = 500, y = 180, font_size=28,
            ),
            TextSlot(
                id="slot.choice.3",
                prompt="",
                text="③ ㄷ, ㄱ, ㄴ",
                style_role="choice",
                x = 95, y = 230, font_size=28,
            ),
            TextSlot(
                id="slot.choice.4",
                prompt="",
                text="④ ㄴ, ㄱ, ㄷ",
                style_role="choice",
                x = 500, y = 230, font_size=28,
            ),
            
            
        ),
        diagrams=(),
        groups=(),
        constraints=(),
        tags=("초등3", "비교", "곱셈", "객관식"),
    )


PROBLEM_TEMPLATE = build_problem_template()

SEMANTIC_OVERRIDE = {
    "problem_id": "S3_초등_3_008543",
    "problem_type": "comparison_order",
    "metadata": {
        "language": "ko",
        "question": "계산 결과가 큰 것부터 순서대로 나열한 것을 고르세요.",
        "instruction": "계산 결과가 큰 것부터 순서대로 나열한 것을 고르세요.",
    },
    "domain": {
        "objects": [
            {
                "id": "obj.a",
                "type": "expression",
                "symbol": "ㄱ",
                "operation": "multiplication",
            },
            {
                "id": "obj.b",
                "type": "expression",
                "symbol": "ㄴ",
                "operation": "multiplication",
            },
            {
                "id": "obj.c",
                "type": "expression",
                "symbol": "ㄷ",
                "operation": "multiplication",
            },
        ],
        "relations": [],
        "problem_solving": {
            "understand": {
                "given_refs": ["obj.a", "obj.b", "obj.c"],
                "target_ref": "answer.target",
                "condition_refs": ["rel.order"],
            },
            "plan": {
                "method": "compare_expression_values",
                "description": "각 곱셈식의 계산 결과를 비교해 큰 것부터 순서를 찾는다.",
            },
            "execute": {
                "expected_operations": [
                    "compute_each_product",
                    "compare_values",
                    "select_matching_order",
                ]
            },
            "review": {
                "check_methods": ["descending_order_check", "choice_match_check"]
            },
        },
    },
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {
            "type": "choice_order",
            "description": "계산 결과가 큰 것부터 순서대로 나열한 보기",
        },
        "value": 3,
        "unit": "",
    },
}

SOLVABLE = {
    "schema": "modu.solvable.v1.1",
    "problem_id": "S3_초등_3_008543",
    "problem_type": "comparison_order",
    "inputs": {
        "total_ticks": 3,
        "target_label": "큰 것부터 순서",
        "target_ticks": 3,
        "target_count": 3,
        "unit": "",
    },
    "given": [
        {
            "ref": "obj.a",
            "value": {"symbol": "ㄱ", "left": 4, "right": 28, "operation": "×"},
        },
        {
            "ref": "obj.b",
            "value": {"symbol": "ㄴ", "left": 3, "right": 34, "operation": "×"},
        },
        {
            "ref": "obj.c",
            "value": {"symbol": "ㄷ", "left": 2, "right": 76, "operation": "×"},
        },
    ],
    "target": {"ref": "answer.target", "type": "choice_order"},
    "method": "compare_expression_values",
    "plan": ["각 식의 값을 계산한 뒤 큰 수부터 작은 수 순서로 비교한다."],
    "steps": [
        {"id": "step.1", "expr": "4 × 28", "value": 112},
        {"id": "step.2", "expr": "3 × 34", "value": 102},
        {"id": "step.3", "expr": "2 × 76", "value": 152},
        {"id": "step.4", "expr": "152 > 112 > 102", "value": ["ㄷ", "ㄱ", "ㄴ"]},
    ],
    "checks": [
        {
            "id": "check.1",
            "expr": "152 > 112 > 102",
            "expected": ["ㄷ", "ㄱ", "ㄴ"],
            "actual": ["ㄷ", "ㄱ", "ㄴ"],
            "pass": True,
        },
        {
            "id": "check.2",
            "expr": "보기 일치",
            "expected": "③",
            "actual": "③",
            "pass": True,
        },
    ],
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {
            "type": "choice_order",
            "description": "계산 결과가 큰 것부터 순서대로 나열한 보기",
        },
        "value": 3,
        "unit": "",
    },
}
