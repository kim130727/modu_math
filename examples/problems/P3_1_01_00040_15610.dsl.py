from __future__ import annotations

from modu_math.dsl import (
    BlankSlot,
    Canvas,
    CircleSlot,
    ProblemTemplate,
    RectSlot,
    Region,
    TextSlot,
)


PROBLEM_ID = "P3_1_01_00040_15610"
PROBLEM_TITLE = "덧셈식과 수의 크기 비교"


ANSWER = {
    "type": "text",
    "value": ">",
    "unit": "",
    "target_ref": "comparison.sum_and_number",
    "derived_from": "step.compare_values",
}


def build_problem_template() -> ProblemTemplate:
    return ProblemTemplate(
        id=PROBLEM_ID,
        title=PROBLEM_TITLE,
        canvas=Canvas(
            width=960,
            height=150,
            coordinate_mode="logical",
        ),
        regions=(
            Region(
                id="region.stem",
                role="stem",
                flow="absolute",
                slot_ids=("slot.question",),
            ),
            Region(
                id="region.comparison",
                role="diagram",
                flow="absolute",
                slot_ids=(
                    "slot.comparison.background",
                    "slot.left.expression",
                    "slot.comparison.circle",
                    "slot.right.number",
                    "slot.answer",
                ),
            ),
        ),
        slots=(
            TextSlot(
                id="slot.question",
                prompt="",
                text="○ 안에 >, =, <를 알맞게 써넣으시오.",
                style_role="question",
                x=20,
                y=24,
                font_size=22,
                fill="#111111",
            ),
            RectSlot(
                id="slot.comparison.background",
                prompt="비교식을 담는 상자",
                x=20,
                y=38,
                width=920,
                height=58,
                fill="#eeeeee",
                stroke="#111111",
                stroke_width=1,
            ),
            TextSlot(
                id="slot.left.expression",
                prompt="왼쪽 덧셈식",
                text="400+156",
                x=485,
                y=75,
                font_size=22,
                anchor="end",
                fill="#333333",
            ),
            CircleSlot(
                id="slot.comparison.circle",
                prompt="비교 기호를 쓰는 곳",
                cx=510,
                cy=68,
                r=15,
                fill="#ffffff",
                stroke="#111111",
                stroke_width=1.5,
            ),
            TextSlot(
                id="slot.right.number",
                prompt="오른쪽 수",
                text="501",
                x=533,
                y=75,
                font_size=22,
                fill="#333333",
            ),
            BlankSlot(
                id="slot.answer",
                prompt="○ 안에 들어갈 비교 기호",
                answer_key=">",
                placeholder=">, =, <",
            ),
        ),
    )


PROBLEM_TEMPLATE = build_problem_template()


SEMANTIC_OVERRIDE = {
    "problem_id": PROBLEM_ID,
    "problem_type": "text_answer_compare_addition_expression_and_number",
    "metadata": {
        "grade": 3,
        "semester": 1,
        "subject": "수학",
        "topic": "세 자리 수의 덧셈과 크기 비교",
        "language": "ko-KR",
        "instruction": "덧셈식의 결과와 주어진 수를 비교하여 알맞은 기호를 씁니다.",
    },
    "domain": {
        "objects": [
            {
                "id": "number.addend_1",
                "type": "number",
                "label": "첫 번째 더하는 수",
                "value": 400,
            },
            {
                "id": "number.addend_2",
                "type": "number",
                "label": "두 번째 더하는 수",
                "value": 156,
            },
            {
                "id": "quantity.sum",
                "type": "derived_number",
                "label": "400과 156의 합",
                "value": 556,
            },
            {
                "id": "number.comparison_value",
                "type": "number",
                "label": "비교할 수",
                "value": 501,
            },
            {
                "id": "comparison.sum_and_number",
                "type": "comparison_symbol",
                "label": "덧셈 결과와 501의 비교 기호",
                "value": ">",
            },
        ],
        "relations": [
            {
                "id": "relation.addition",
                "type": "sum_of",
                "subject": "quantity.sum",
                "objects": ["number.addend_1", "number.addend_2"],
            },
            {
                "id": "relation.compare",
                "type": "greater_than",
                "left": "quantity.sum",
                "right": "number.comparison_value",
                "result": "comparison.sum_and_number",
            },
        ],
    },
    "answer": ANSWER,
}


SOLVABLE = {
    "schema": "modu.solvable.v1.2",
    "problem_id": PROBLEM_ID,
    "problem_type": "text_answer_compare_addition_expression_and_number",
    "inputs": {
        "target_label": "덧셈 결과와 501을 비교하는 기호",
        "unit": "",
        "left_expression": {
            "first": 400,
            "operator": "+",
            "second": 156,
        },
        "right_value": 501,
        "allowed_symbols": [">", "=", "<"],
    },
    "given": [
        {
            "ref": "expression.left_addition",
            "value": {
                "expression": "400 + 156",
                "result": 556,
            },
        },
        {
            "ref": "number.comparison_value",
            "value": 501,
        },
    ],
    "target": {
        "ref": "comparison.sum_and_number",
        "type": "text",
    },
    "understanding": {
        "summary": "400과 156의 합을 구한 뒤 그 결과와 501의 크기를 비교하는 문제입니다.",
        "facts": [
            {
                "ref": "expression.left_addition",
                "label": "왼쪽 덧셈식",
                "value": "400 + 156",
                "unit": "",
                "source": "explicit",
            },
            {
                "ref": "number.comparison_value",
                "label": "오른쪽 수",
                "value": 501,
                "unit": "",
                "source": "explicit",
            },
        ],
        "unknowns": [
            {
                "ref": "comparison.sum_and_number",
                "label": "○ 안에 들어갈 비교 기호",
                "unit": "",
            },
        ],
        "relation": {
            "type": "compare_computed_sum_and_number",
            "statement": "400과 156의 합과 501의 크기를 비교합니다.",
            "symbolic": "(400 + 156) ○ 501",
            "uses": [
                "expression.left_addition",
                "number.comparison_value",
            ],
            "result": "comparison.sum_and_number",
        },
        "diagnostic_questions": [
            {
                "id": "understand.calculate_sum",
                "type": "multiple_choice",
                "prompt": "400+156의 계산 결과는 얼마인가요?",
                "choices": ["456", "556", "656"],
                "answer_index": 1,
            },
            {
                "id": "understand.compare",
                "type": "multiple_choice",
                "prompt": "556과 501의 크기를 바르게 비교한 것은 무엇인가요?",
                "choices": ["556 > 501", "556 = 501", "556 < 501"],
                "answer_index": 0,
            },
        ],
    },
    "method": "덧셈식의 값을 계산한 다음 501과 비교합니다.",
    "plan": [
        "400과 156을 더해 왼쪽 값을 구합니다.",
        "왼쪽 값과 501의 크기를 비교합니다.",
        "비교 결과에 맞는 기호를 고릅니다.",
    ],
    "steps": [
        {
            "id": "step.calculate_sum",
            "expr": "400 + 156",
            "value": 556,
            "explanation": "400과 156을 더하면 556입니다.",
        },
        {
            "id": "step.compare_values",
            "expr": "556 > 501",
            "value": ">",
            "explanation": "556은 501보다 크므로 ○ 안에는 >를 씁니다.",
        },
    ],
    "checks": [
        {
            "id": "check.sum_by_subtraction",
            "expr": "556 - 156",
            "expected": 400,
            "actual": 400,
            "pass": True,
        },
        {
            "id": "check.comparison",
            "expr": "556 > 501",
            "expected": True,
            "actual": True,
            "pass": True,
        },
    ],
    "answer": ANSWER,
}


SEMANTIC_ANSWER = SOLVABLE["answer"]
