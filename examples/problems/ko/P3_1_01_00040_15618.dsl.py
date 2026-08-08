from __future__ import annotations

from modu_math.dsl import (
    BlankSlot,
    Canvas,
    LineSlot,
    ProblemTemplate,
    Region,
    TextSlot,
)


PROBLEM_ID = "P3_1_01_00040_15618"
PROBLEM_TITLE = "두 세 자리 수의 덧셈"


ANSWER = {
    "type": "multi_numeric",
    "value": [788, 899],
    "unit": "",
    "values": [
        {
            "value": 788,
            "unit": "",
            "target_ref": "answer.addition_1",
            "derived_from": "step.add_375_413",
        },
        {
            "value": 899,
            "unit": "",
            "target_ref": "answer.addition_2",
            "derived_from": "step.add_607_292",
        },
    ],
}


SEMANTIC_OVERRIDE = {
    "problem_id": PROBLEM_ID,
    "problem_type": "multi_numeric_vertical_addition_problem",
    "metadata": {
        "grade": 3,
        "semester": 1,
        "subject": "수학",
        "topic": "세 자리 수의 덧셈",
        "language": "ko-KR",
        "question": "다음 덧셈을 하시오.",
        "instruction": "각 세로셈의 같은 자리 수끼리 더합니다.",
    },
    "domain": {
        "objects": [
            {
                "id": "operation.addition_1",
                "type": "vertical_addition",
                "label": "(1) 375 + 413",
                "addends": [375, 413],
                "sum": 788,
            },
            {
                "id": "operation.addition_2",
                "type": "vertical_addition",
                "label": "(2) 607 + 292",
                "addends": [607, 292],
                "sum": 899,
            },
            {
                "id": "answer.addition_1",
                "type": "quantity",
                "label": "첫 번째 덧셈의 합",
                "value": 788,
                "unit": "",
            },
            {
                "id": "answer.addition_2",
                "type": "quantity",
                "label": "두 번째 덧셈의 합",
                "value": 899,
                "unit": "",
            },
        ],
        "relations": [
            {
                "id": "relation.addition_1_result",
                "type": "result_of",
                "from_id": "answer.addition_1",
                "to_id": "operation.addition_1",
            },
            {
                "id": "relation.addition_2_result",
                "type": "result_of",
                "from_id": "answer.addition_2",
                "to_id": "operation.addition_2",
            },
        ],
        "problem_solving": {
            "understand": {
                "given_refs": [
                    "operation.addition_1",
                    "operation.addition_2",
                ],
                "target_ref": "answer.all",
            },
            "plan": {
                "method": "place_value_vertical_addition",
                "description": "각 식에서 일의 자리, 십의 자리, 백의 자리 순서로 더합니다.",
            },
            "execute": {
                "expected_operations": ["addition", "addition"],
            },
            "review": {
                "check_methods": ["inverse_subtraction", "estimation"],
            },
        },
    },
    "answer": ANSWER,
}


SOLVABLE = {
    "schema": "modu.solvable.v1.2",
    "problem_id": PROBLEM_ID,
    "problem_type": "multi_numeric_vertical_addition_problem",
    "inputs": {
        "target_label": "두 덧셈의 합",
        "unit": "",
        "expressions": [
            {
                "id": "operation.addition_1",
                "left": 375,
                "operator": "+",
                "right": 413,
            },
            {
                "id": "operation.addition_2",
                "left": 607,
                "operator": "+",
                "right": 292,
            },
        ],
    },
    "given": [
        {
            "ref": "operation.addition_1",
            "value": {
                "left": 375,
                "operator": "+",
                "right": 413,
            },
        },
        {
            "ref": "operation.addition_2",
            "value": {
                "left": 607,
                "operator": "+",
                "right": 292,
            },
        },
    ],
    "target": {
        "ref": "answer.all",
        "type": "number_pair",
    },
    "understanding": {
        "summary": "두 세로셈을 각각 계산하여 두 합을 구하는 문제입니다.",
        "facts": [
            {
                "ref": "operation.addition_1",
                "label": "첫 번째 덧셈식",
                "value": "375 + 413",
                "unit": "",
                "source": "explicit",
            },
            {
                "ref": "operation.addition_2",
                "label": "두 번째 덧셈식",
                "value": "607 + 292",
                "unit": "",
                "source": "explicit",
            },
        ],
        "unknowns": [
            {
                "ref": "answer.addition_1",
                "label": "375와 413의 합",
                "unit": "",
                "source": "unknown",
            },
            {
                "ref": "answer.addition_2",
                "label": "607과 292의 합",
                "unit": "",
                "source": "unknown",
            },
        ],
        "relation": {
            "type": "independent_additions",
            "statement": "각 세로셈에서 같은 자리의 수끼리 더하여 두 합을 각각 구합니다.",
            "symbolic": "375 + 413 = first; 607 + 292 = second",
            "uses": [
                "operation.addition_1",
                "operation.addition_2",
            ],
            "result": "answer.all",
        },
        "diagnostic_questions": [
            {
                "id": "understand.target",
                "type": "multiple_choice",
                "prompt": "이 문제에서 구해야 하는 것은 무엇인가요?",
                "choices": [
                    "두 덧셈식의 합",
                    "두 덧셈식의 차",
                    "네 수 중 가장 큰 수",
                ],
                "answer_index": 0,
            },
            {
                "id": "understand.alignment",
                "type": "multiple_choice",
                "prompt": "세로셈에서는 어떤 수끼리 더해야 하나요?",
                "choices": [
                    "같은 자리의 수끼리 더합니다.",
                    "가장 큰 숫자끼리만 더합니다.",
                    "위 수에서 아래 수를 뺍니다.",
                ],
                "answer_index": 0,
            },
        ],
    },
    "method": "각 세로셈에서 같은 자리의 수끼리 더합니다.",
    "plan": [
        "첫 번째 세로셈 375 + 413을 계산합니다.",
        "두 번째 세로셈 607 + 292를 계산합니다.",
        "뺄셈으로 각 합이 맞는지 확인합니다.",
    ],
    "steps": [
        {
            "id": "step.add_375_413",
            "goal": "첫 번째 덧셈의 합을 구합니다.",
            "uses": ["operation.addition_1"],
            "relation_expr": "첫 번째 합 = 375 + 413",
            "expr": "375 + 413",
            "value": 788,
            "explanation": "일의 자리 5+3=8, 십의 자리 7+1=8, 백의 자리 3+4=7이므로 합은 788입니다.",
        },
        {
            "id": "step.add_607_292",
            "goal": "두 번째 덧셈의 합을 구합니다.",
            "uses": ["operation.addition_2"],
            "relation_expr": "두 번째 합 = 607 + 292",
            "expr": "607 + 292",
            "value": 899,
            "explanation": "일의 자리 7+2=9, 십의 자리 0+9=9, 백의 자리 6+2=8이므로 합은 899입니다.",
        },
    ],
    "checks": [
        {
            "id": "check.addition_1_inverse",
            "expr": "788 - 413",
            "expected": 375,
            "actual": 375,
            "pass": True,
        },
        {
            "id": "check.addition_2_inverse",
            "expr": "899 - 292",
            "expected": 607,
            "actual": 607,
            "pass": True,
        },
        {
            "id": "check.addition_1_estimate",
            "expr": "round(375, -2) + round(413, -2)",
            "expected": 800,
            "actual": 800,
            "pass": True,
        },
        {
            "id": "check.addition_2_estimate",
            "expr": "round(607, -2) + round(292, -2)",
            "expected": 900,
            "actual": 900,
            "pass": True,
        },
    ],
    "answer": ANSWER,
}


SEMANTIC_ANSWER = SOLVABLE["answer"]


def build_problem_template() -> ProblemTemplate:
    return ProblemTemplate(
        id=PROBLEM_ID,
        title=PROBLEM_TITLE,
        canvas=Canvas(
            width=900,
            height=230,
            coordinate_mode="logical",
        ),
        regions=(
            Region(
                id="region.stem",
                role="stem",
                flow="absolute",
                slot_ids=("slot.instruction",),
            ),
            Region(
                id="region.expressions",
                role="diagram",
                flow="absolute",
                slot_ids=(
                    "slot.expression_1.label",
                    "slot.expression_1.top",
                    "slot.expression_1.operator",
                    "slot.expression_1.bottom",
                    "slot.expression_1.line",
                    "slot.expression_2.label",
                    "slot.expression_2.top",
                    "slot.expression_2.operator",
                    "slot.expression_2.bottom",
                    "slot.expression_2.line",
                ),
            ),
        ),
        slots=(
            TextSlot(
                id="slot.instruction",
                prompt="",
                text="다음 덧셈을 하시오.",
                style_role="question",
                x=24,
                y=28,
                font_size=22,
                fill="#222222",
            ),
            TextSlot(
                id="slot.expression_1.label",
                prompt="",
                text="(1)",
                style_role="label",
                x=26,
                y=70,
                font_size=22,
                fill="#111111",
            ),
            TextSlot(
                id="slot.expression_1.top",
                prompt="",
                text="375",
                style_role="number",
                x=135,
                y=70,
                font_size=24,
                max_width=90,
                anchor="end",
                fill="#111111",
            ),
            TextSlot(
                id="slot.expression_1.operator",
                prompt="",
                text="+",
                style_role="operator",
                x=65,
                y=108,
                font_size=24,
                fill="#111111",
            ),
            TextSlot(
                id="slot.expression_1.bottom",
                prompt="",
                text="413",
                style_role="number",
                x=135,
                y=108,
                font_size=24,
                max_width=90,
                anchor="end",
                fill="#111111",
            ),
            LineSlot(
                id="slot.expression_1.line",
                prompt="",
                x1=58,
                y1=125,
                x2=142,
                y2=125,
                stroke="#111111",
                stroke_width=1.5,
            ),
            TextSlot(
                id="slot.expression_2.label",
                prompt="",
                text="(2)",
                style_role="label",
                x=185,
                y=70,
                font_size=22,
                fill="#111111",
            ),
            TextSlot(
                id="slot.expression_2.top",
                prompt="",
                text="607",
                style_role="number",
                x=295,
                y=70,
                font_size=24,
                max_width=90,
                anchor="end",
                fill="#111111",
            ),
            TextSlot(
                id="slot.expression_2.operator",
                prompt="",
                text="+",
                style_role="operator",
                x=225,
                y=108,
                font_size=24,
                fill="#111111",
            ),
            TextSlot(
                id="slot.expression_2.bottom",
                prompt="",
                text="292",
                style_role="number",
                x=295,
                y=108,
                font_size=24,
                max_width=90,
                anchor="end",
                fill="#111111",
            ),
            LineSlot(
                id="slot.expression_2.line",
                prompt="",
                x1=218,
                y1=125,
                x2=302,
                y2=125,
                stroke="#111111",
                stroke_width=1.5,
            ),
            BlankSlot(
                id="slot.answer_1",
                prompt="(1)",
                answer_key="788",
                placeholder="",
            ),
            BlankSlot(
                id="slot.answer_2",
                prompt="(2)",
                answer_key="899",
                placeholder="",
            ),
        ),
    )


PROBLEM_TEMPLATE = build_problem_template()
