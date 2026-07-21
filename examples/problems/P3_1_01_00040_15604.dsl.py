from __future__ import annotations

from modu_math.dsl import (
    BlankSlot,
    Canvas,
    CircleSlot,
    LineSlot,
    ProblemTemplate,
    Region,
    TextSlot,
)


PROBLEM_ID = "P3_1_01_00040_15604"
PROBLEM_TITLE = "두 덧셈 결과의 크기 비교"


ANSWER = {
    "type": "text",
    "value": "<",
    "unit": "",
    "target_ref": "comparison.left_sum_right_sum",
    "derived_from": "step.compare_sums",
}


def build_problem_template() -> ProblemTemplate:
    return ProblemTemplate(
        id=PROBLEM_ID,
        title=PROBLEM_TITLE,
        canvas=Canvas(
            width=720,
            height=180,
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
                    "slot.left.top",
                    "slot.left.plus",
                    "slot.left.bottom",
                    "slot.left.line",
                    "slot.comparison.circle",
                    "slot.right.top",
                    "slot.right.plus",
                    "slot.right.bottom",
                    "slot.right.line",
                    "slot.answer",
                ),
            ),
        ),
        slots=(
            TextSlot(
                id="slot.question",
                prompt="",
                text="크기를 비교하여 ○ 안에 >, <, =를 알맞게 써넣으시오.",
                style_role="question",
                x=20,
                y=30,
                font_size=23,
                fill="#111111",
            ),
            TextSlot(
                id="slot.left.top",
                prompt="왼쪽 덧셈의 첫 번째 수",
                text="450",
                x=100,
                y=82,
                font_size=25,
                anchor="end",
                fill="#111111",
            ),
            TextSlot(
                id="slot.left.plus",
                prompt="덧셈 기호",
                text="+",
                x=45,
                y=128,
                font_size=25,
                anchor="middle",
                fill="#111111",
            ),
            TextSlot(
                id="slot.left.bottom",
                prompt="왼쪽 덧셈의 두 번째 수",
                text="146",
                x=100,
                y=128,
                font_size=25,
                anchor="end",
                fill="#111111",
            ),
            LineSlot(
                id="slot.left.line",
                prompt="왼쪽 세로셈의 밑줄",
                x1=28,
                y1=148,
                x2=110,
                y2=148,
                stroke="#111111",
                stroke_width=1.5,
            ),
            CircleSlot(
                id="slot.comparison.circle",
                prompt="두 덧셈 결과를 비교하는 기호를 쓰는 곳",
                cx=143,
                cy=113,
                r=16,
                fill="#ffffff",
                stroke="#111111",
                stroke_width=1.5,
            ),
            TextSlot(
                id="slot.right.top",
                prompt="오른쪽 덧셈의 첫 번째 수",
                text="347",
                x=226,
                y=82,
                font_size=25,
                anchor="end",
                fill="#111111",
            ),
            TextSlot(
                id="slot.right.plus",
                prompt="덧셈 기호",
                text="+",
                x=171,
                y=128,
                font_size=25,
                anchor="middle",
                fill="#111111",
            ),
            TextSlot(
                id="slot.right.bottom",
                prompt="오른쪽 덧셈의 두 번째 수",
                text="250",
                x=226,
                y=128,
                font_size=25,
                anchor="end",
                fill="#111111",
            ),
            LineSlot(
                id="slot.right.line",
                prompt="오른쪽 세로셈의 밑줄",
                x1=154,
                y1=148,
                x2=236,
                y2=148,
                stroke="#111111",
                stroke_width=1.5,
            ),
            BlankSlot(
                id="slot.answer",
                prompt="○ 안에 들어갈 비교 기호",
                answer_key="<",
                placeholder=">, <, =",
            ),
        ),
    )


PROBLEM_TEMPLATE = build_problem_template()


SEMANTIC_OVERRIDE = {
    "problem_id": PROBLEM_ID,
    "problem_type": "text_answer_compare_addition_sums",
    "metadata": {
        "grade": 3,
        "semester": 1,
        "subject": "수학",
        "topic": "세 자리 수의 덧셈과 크기 비교",
        "language": "ko-KR",
        "instruction": "두 덧셈의 결과를 비교하여 알맞은 기호를 고릅니다.",
    },
    "domain": {
        "objects": [
            {
                "id": "number.left_addend_1",
                "type": "number",
                "label": "왼쪽 첫 번째 수",
                "value": 450,
            },
            {
                "id": "number.left_addend_2",
                "type": "number",
                "label": "왼쪽 두 번째 수",
                "value": 146,
            },
            {
                "id": "quantity.left_sum",
                "type": "derived_number",
                "label": "왼쪽 덧셈의 결과",
                "value": 596,
            },
            {
                "id": "number.right_addend_1",
                "type": "number",
                "label": "오른쪽 첫 번째 수",
                "value": 347,
            },
            {
                "id": "number.right_addend_2",
                "type": "number",
                "label": "오른쪽 두 번째 수",
                "value": 250,
            },
            {
                "id": "quantity.right_sum",
                "type": "derived_number",
                "label": "오른쪽 덧셈의 결과",
                "value": 597,
            },
            {
                "id": "comparison.left_sum_right_sum",
                "type": "comparison_symbol",
                "label": "두 덧셈 결과의 비교 기호",
                "value": "<",
            },
        ],
        "relations": [
            {
                "id": "relation.left_addition",
                "type": "sum_of",
                "subject": "quantity.left_sum",
                "objects": [
                    "number.left_addend_1",
                    "number.left_addend_2",
                ],
            },
            {
                "id": "relation.right_addition",
                "type": "sum_of",
                "subject": "quantity.right_sum",
                "objects": [
                    "number.right_addend_1",
                    "number.right_addend_2",
                ],
            },
            {
                "id": "relation.compare_sums",
                "type": "less_than",
                "left": "quantity.left_sum",
                "right": "quantity.right_sum",
                "result": "comparison.left_sum_right_sum",
            },
        ],
    },
    "answer": ANSWER,
}


SOLVABLE = {
    "schema": "modu.solvable.v1.2",
    "problem_id": PROBLEM_ID,
    "problem_type": "text_answer_compare_addition_sums",
    "inputs": {
        "target_label": "두 덧셈 결과를 비교하는 기호",
        "unit": "",
        "left_expression": {
            "first": 450,
            "operator": "+",
            "second": 146,
        },
        "right_expression": {
            "first": 347,
            "operator": "+",
            "second": 250,
        },
        "allowed_symbols": [">", "<", "="],
    },
    "given": [
        {
            "ref": "expression.left_addition",
            "value": {
                "expression": "450 + 146",
                "result": 596,
            },
        },
        {
            "ref": "expression.right_addition",
            "value": {
                "expression": "347 + 250",
                "result": 597,
            },
        },
    ],
    "target": {
        "ref": "comparison.left_sum_right_sum",
        "type": "text",
    },
    "understanding": {
        "summary": "두 덧셈을 각각 계산하고 그 결과의 크기를 비교하는 문제입니다.",
        "facts": [
            {
                "ref": "expression.left_addition",
                "label": "왼쪽 덧셈",
                "value": "450 + 146",
                "unit": "",
                "source": "explicit",
            },
            {
                "ref": "expression.right_addition",
                "label": "오른쪽 덧셈",
                "value": "347 + 250",
                "unit": "",
                "source": "explicit",
            },
        ],
        "unknowns": [
            {
                "ref": "comparison.left_sum_right_sum",
                "label": "○ 안에 들어갈 비교 기호",
                "unit": "",
            },
        ],
        "relation": {
            "type": "compare_computed_sums",
            "statement": "왼쪽 덧셈의 결과와 오른쪽 덧셈의 결과를 비교합니다.",
            "symbolic": "(450 + 146) ○ (347 + 250)",
            "uses": [
                "expression.left_addition",
                "expression.right_addition",
            ],
            "result": "comparison.left_sum_right_sum",
        },
        "diagnostic_questions": [
            {
                "id": "understand.left_sum",
                "type": "multiple_choice",
                "prompt": "450+146의 계산 결과는 얼마인가요?",
                "choices": ["595", "596", "597"],
                "answer_index": 1,
            },
            {
                "id": "understand.right_sum",
                "type": "multiple_choice",
                "prompt": "347+250의 계산 결과는 얼마인가요?",
                "choices": ["596", "597", "607"],
                "answer_index": 1,
            },
            {
                "id": "understand.comparison",
                "type": "multiple_choice",
                "prompt": "596과 597의 크기를 비교한 것은 무엇인가요?",
                "choices": ["596 > 597", "596 < 597", "596 = 597"],
                "answer_index": 1,
            },
        ],
    },
    "method": "두 덧셈을 각각 계산한 뒤 두 계산 결과의 크기를 비교합니다.",
    "plan": [
        "450과 146을 더해 왼쪽 결과를 구합니다.",
        "347과 250을 더해 오른쪽 결과를 구합니다.",
        "두 결과를 비교하여 알맞은 기호를 고릅니다.",
    ],
    "steps": [
        {
            "id": "step.calculate_left_sum",
            "expr": "450 + 146",
            "value": 596,
            "explanation": "450과 146을 더하면 596입니다.",
        },
        {
            "id": "step.calculate_right_sum",
            "expr": "347 + 250",
            "value": 597,
            "explanation": "347과 250을 더하면 597입니다.",
        },
        {
            "id": "step.compare_sums",
            "expr": "596 < 597",
            "value": "<",
            "explanation": "596은 597보다 작으므로 ○ 안에는 <를 씁니다.",
        },
    ],
    "checks": [
        {
            "id": "check.left_sum",
            "expr": "596 - 146",
            "expected": 450,
            "actual": 450,
            "pass": True,
        },
        {
            "id": "check.right_sum",
            "expr": "597 - 250",
            "expected": 347,
            "actual": 347,
            "pass": True,
        },
        {
            "id": "check.comparison",
            "expr": "596 < 597",
            "expected": True,
            "actual": True,
            "pass": True,
        },
    ],
    "answer": ANSWER,
}


SEMANTIC_ANSWER = SOLVABLE["answer"]
