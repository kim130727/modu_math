from __future__ import annotations
from modu_math.dsl import Canvas, ProblemTemplate, Region, RectSlot, TextSlot


def build_problem_template() -> ProblemTemplate:
    return ProblemTemplate(
        id="S3_초등_3_008544",
        title="계산 결과가 큰 것부터 순서대로 나열한 것 고르기",
        canvas=Canvas(width=940, height=400, coordinate_mode="logical"),
        regions=(
            Region(
                id="region.stem",
                role="stem",
                flow="absolute",
                slot_ids=(
                    "slot.q.text",
                    "slot.box",
                    "slot.expr1.num",
                    "slot.expr1.body",
                    "slot.expr2.num",
                    "slot.expr2.body",
                    "slot.expr3.num",
                    "slot.expr3.body",
                    "slot.choice1.num",
                    "slot.choice1.body",
                    "slot.choice2.num",
                    "slot.choice2.body",
                    "slot.choice3.num",
                    "slot.choice3.body",
                    "slot.choice4.num",
                    "slot.choice4.body",
                    
                    
                ),
            ),
        ),
        slots=(
            TextSlot(
                id="slot.q.text",
                prompt="",
                text="계산 결과가 큰 것부터 순서대로 나열한 것을 고르세요.",
                style_role="question",
                x = 115, y = 35, font_size=28,
            ),
            RectSlot(
                id="slot.box", prompt="", x=128.0, y=60.0, width=690.0, height=78.0, fill="#D9DDF3",
                stroke="#A79CDC",
                stroke_width=2.0,
            ),
            TextSlot(
                id="slot.expr1.body",
                prompt="",
                text="ㄱ. 9 × 85",
                style_role="question",
                x = 205, y = 110, font_size=28,
            ),
            TextSlot(
                id="slot.expr2.body",
                prompt="",
                text="ㄴ. 8 × 65",
                style_role="question",
                x = 410, y = 110, font_size=28,
            ),
            TextSlot(
                id="slot.expr3.body",
                prompt="",
                text="ㄷ. 6 × 73",
                style_role="question",
                x = 605, y = 110, font_size=28,
            ),
            TextSlot(
                id="slot.choice1.num",
                prompt="",
                text="① ㄱ ㄴ ㄷ",
                style_role="question",
                x = 160, y = 180, font_size=28,
            ),
            TextSlot(
                id="slot.choice2.num",
                prompt="",
                text="② ㄷ ㄴ ㄱ",
                style_role="question",
                x = 535, y = 180, font_size=28,
            ),
            TextSlot(
                id="slot.choice3.num",
                prompt="",
                text="③ ㄷ ㄱ ㄴ",
                style_role="question",
                x = 160, y = 230, font_size=28,
            ),
            TextSlot(
                id="slot.choice4.num",
                prompt="",
                text="④ ㄴ ㄱ ㄷ",
                style_role="question",
                x = 535, y = 230, font_size=28,
            ),
        ),
        diagrams=(),
        groups=(),
        constraints=(),
        tags=(),
    )


PROBLEM_TEMPLATE = build_problem_template()

SEMANTIC_OVERRIDE = {
    "problem_id": "S3_초등_3_008544",
    "problem_type": "multiple_choice_ordering",
    "metadata": {
        "language": "ko",
        "question": "계산 결과가 큰 것부터 순서대로 나열한 것을 고르세요.",
        "instruction": "계산 결과의 크기를 비교하여 순서를 고른다.",
    },
    "domain": {
        "objects": [
            {
                "id": "obj.expr1",
                "type": "multiplication_expression",
                "expression": "9 × 85",
            },
            {
                "id": "obj.expr2",
                "type": "multiplication_expression",
                "expression": "8 × 65",
            },
            {
                "id": "obj.expr3",
                "type": "multiplication_expression",
                "expression": "6 × 73",
            },
        ],
        "relations": [],
        "problem_solving": {
            "understand": {
                "given_refs": ["obj.expr1", "obj.expr2", "obj.expr3"],
                "target_ref": "answer.target",
                "condition_refs": ["rel.compare_results"],
            },
            "plan": {
                "method": "compute_and_compare",
                "description": "각 곱셈식의 결과를 구한 뒤 크기를 비교한다.",
            },
            "execute": {
                "expected_operations": ["multiply", "compare", "order_from_largest"]
            },
            "review": {
                "check_methods": [
                    "compare_results",
                    "match_chosen_order_with_descending_values",
                ]
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
        "value": 1,
        "unit": "",
    },
}

SOLVABLE = {
    "schema": "modu.solvable.v1.1",
    "problem_id": "S3_초등_3_008544",
    "problem_type": "multiple_choice_ordering",
    "inputs": {
        "total_ticks": 3,
        "target_label": "계산 결과가 큰 것부터 순서대로 나열한 것",
        "target_ticks": 3,
        "target_count": 3,
        "unit": "",
    },
    "given": [
        {"ref": "obj.expr1", "value": {"expression": "9 × 85"}},
        {"ref": "obj.expr2", "value": {"expression": "8 × 65"}},
        {"ref": "obj.expr3", "value": {"expression": "6 × 73"}},
    ],
    "target": {"ref": "answer.target", "type": "choice_order"},
    "method": "compute_and_compare",
    "plan": ["각 곱셈식을 계산한다.", "계산 결과를 비교하여 큰 것부터 순서를 정한다."],
    "steps": [
        {"id": "step.1", "expr": "9 × 85", "value": 765},
        {"id": "step.2", "expr": "8 × 65", "value": 520},
        {"id": "step.3", "expr": "6 × 73", "value": 438},
        {"id": "step.4", "expr": "765 > 520 > 438", "value": [765, 520, 438]},
    ],
    "checks": [
        {
            "id": "check.1",
            "expr": "step.1 > step.2 > step.3",
            "expected": [765, 520, 438],
            "actual": [765, 520, 438],
            "pass": True,
        }
    ],
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {
            "type": "choice_order",
            "description": "계산 결과가 큰 것부터 순서대로 나열한 보기",
        },
        "value": 1,
        "unit": "",
    },
}
