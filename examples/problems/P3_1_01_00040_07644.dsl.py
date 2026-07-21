from __future__ import annotations

from modu_math.dsl import (
    BlankSlot,
    Canvas,
    ProblemTemplate,
    Region,
    TextBoxSlot,
)


PROBLEM_ID = "P3_1_01_00040_07644"
PROBLEM_TITLE = "상훈이가 산 100원짜리와 50원짜리 우표 수"


def build_problem_template() -> ProblemTemplate:
    return ProblemTemplate(
        id=PROBLEM_ID,
        title=PROBLEM_TITLE,
        canvas=Canvas(
            width=900,
            height=260,
            coordinate_mode="logical",
        ),
        regions=(
            Region(
                id="region.stem",
                role="stem",
                flow="vertical",
                slot_ids=("slot.question",),
            ),
        ),
        slots=(
            TextBoxSlot(
                id="slot.question",
                x=48,
                y=30,
                width=804,
                height=125,
                text=(
                    "상훈이는 1000원짜리 우표 1장을 사고, 100원짜리와 50원짜리 "
                    "두 종류의 우표를 합해서 20장을 샀습니다. 우표값으로 2550원을 "
                    "냈다면 상훈이는 100원짜리와 50원짜리 우표를 각각 몇 장 샀습니까?"
                ),
                font_size=24,
                font_family="Noto Sans KR",
                fill="#202124",
                line_height=1.5,
                align="left",
                valign="top",
            ),
            BlankSlot(
                id="slot.answer_100won",
                prompt="100원짜리 우표",
                answer_key="11",
                placeholder="장",
            ),
            BlankSlot(
                id="slot.answer_50won",
                prompt="50원짜리 우표",
                answer_key="9",
                placeholder="장",
            ),
        ),
    )


PROBLEM_TEMPLATE = build_problem_template()


SEMANTIC = {
    "problem_id": PROBLEM_ID,
    "problem_type": "multi_numeric_answer_stamp_count_problem",
    "metadata": {
        "grade": 3,
        "semester": 1,
        "subject": "수학",
        "topic": "덧셈과 뺄셈을 활용한 문제 해결",
        "language": "ko-KR",
    },
    "domain": {
        "objects": [
            {
                "id": "person.sanghoon",
                "type": "person",
                "label": "상훈이",
            },
            {
                "id": "stamp.1000won",
                "type": "stamp_type",
                "label": "1000원짜리 우표",
                "unit_price": 1000,
                "currency": "원",
            },
            {
                "id": "stamp.100won",
                "type": "stamp_type",
                "label": "100원짜리 우표",
                "unit_price": 100,
                "currency": "원",
            },
            {
                "id": "stamp.50won",
                "type": "stamp_type",
                "label": "50원짜리 우표",
                "unit_price": 50,
                "currency": "원",
            },
            {
                "id": "quantity.1000won_stamp_count",
                "type": "quantity",
                "label": "1000원짜리 우표 수",
                "value": 1,
                "unit": "장",
            },
            {
                "id": "quantity.100won_stamp_count",
                "type": "quantity",
                "label": "100원짜리 우표 수",
                "value": 11,
                "unit": "장",
            },
            {
                "id": "quantity.50won_stamp_count",
                "type": "quantity",
                "label": "50원짜리 우표 수",
                "value": 9,
                "unit": "장",
            },
            {
                "id": "quantity.100won_50won_total_count",
                "type": "quantity",
                "label": "100원짜리와 50원짜리 우표의 합계 수",
                "value": 20,
                "unit": "장",
            },
            {
                "id": "amount.total_payment",
                "type": "money",
                "label": "전체 우표값",
                "value": 2550,
                "unit": "원",
            },
            {
                "id": "amount.100won_50won_payment",
                "type": "money",
                "label": "100원짜리와 50원짜리 우표값",
                "value": 1550,
                "unit": "원",
            },
        ],
        "relations": [
            {
                "id": "relation.bought_1000won_stamp",
                "type": "purchased",
                "subject": "person.sanghoon",
                "object": "stamp.1000won",
                "quantity": "quantity.1000won_stamp_count",
            },
            {
                "id": "relation.bought_100won_stamp",
                "type": "purchased",
                "subject": "person.sanghoon",
                "object": "stamp.100won",
                "quantity": "quantity.100won_stamp_count",
            },
            {
                "id": "relation.bought_50won_stamp",
                "type": "purchased",
                "subject": "person.sanghoon",
                "object": "stamp.50won",
                "quantity": "quantity.50won_stamp_count",
            },
            {
                "id": "relation.two_stamp_counts_sum",
                "type": "sum_of",
                "subject": "quantity.100won_50won_total_count",
                "objects": [
                    "quantity.100won_stamp_count",
                    "quantity.50won_stamp_count",
                ],
            },
            {
                "id": "relation.remaining_payment",
                "type": "difference_of",
                "subject": "amount.100won_50won_payment",
                "minuend": "amount.total_payment",
                "subtrahend_value": 1000,
            },
        ],
    },
    "answer": {
        "type": "multi_numeric",
        "values": [
            {
                "value": 11,
                "unit": "장",
                "target_ref": "quantity.100won_stamp_count",
            },
            {
                "value": 9,
                "unit": "장",
                "target_ref": "quantity.50won_stamp_count",
            },
        ],
    },
}

SEMANTIC_OVERRIDE = SEMANTIC


SOLVABLE = {
    "schema": "modu.solvable.v1.2",
    "problem_id": PROBLEM_ID,
    "problem_type": "multi_numeric_answer_stamp_count_problem",
    "inputs": {
        "target_label": "100원짜리와 50원짜리 우표의 수",
        "unit": "장",
        "quantities": {
            "1000won_stamp_price": 1000,
            "1000won_stamp_count": 1,
            "100won_stamp_price": 100,
            "50won_stamp_price": 50,
            "100won_50won_total_count": 20,
            "total_payment": 2550,
        },
        "conditions": [
            "1000원짜리 우표를 1장 샀습니다.",
            "100원짜리와 50원짜리 우표를 합하여 20장 샀습니다.",
            "모든 우표값은 2550원입니다.",
        ],
    },
    "given": [
        {
            "ref": "quantity.1000won_stamp_count",
            "value": {
                "count": 1,
                "unit": "장",
                "stamp": "stamp.1000won",
                "unit_price": 1000,
                "currency": "원",
            },
        },
        {
            "ref": "quantity.100won_50won_total_count",
            "value": {
                "count": 20,
                "unit": "장",
                "stamp_types": [
                    "stamp.100won",
                    "stamp.50won",
                ],
            },
        },
        {
            "ref": "amount.total_payment",
            "value": {
                "amount": 2550,
                "unit": "원",
            },
        },
    ],
    "target": {
        "refs": [
            "quantity.100won_stamp_count",
            "quantity.50won_stamp_count",
        ],
        "type": "number_pair",
    },
    "method": (
        "전체 금액에서 1000원짜리 우표값을 뺀 뒤, 나머지 20장이 모두 "
        "50원짜리라고 가정하여 100원짜리로 바뀐 우표 수를 구합니다."
    ),
    "plan": [
        "전체 우표값에서 1000원짜리 우표 1장의 값을 뺍니다.",
        "100원짜리와 50원짜리 우표 20장이 모두 50원짜리일 때의 값을 구합니다.",
        "실제 금액과 모두 50원짜리일 때의 금액 차이를 구합니다.",
        "우표 1장을 50원짜리에서 100원짜리로 바꾸면 50원씩 늘어남을 이용합니다.",
        "100원짜리 우표 수를 구한 뒤 전체 20장에서 빼서 50원짜리 우표 수를 구합니다.",
    ],
    "steps": [
        {
            "id": "step.remove_1000won_stamp_cost",
            "goal": "100원짜리와 50원짜리 우표의 금액만 구합니다.",
            "uses": [
                "amount.total_payment",
                "quantity.1000won_stamp_count",
            ],
            "relation_expr": "두 종류 우표값 = 전체 우표값 - 1000원짜리 우표값",
            "expr": "2550 - 1000",
            "value": 1550,
            "explanation": "전체 금액에서 1000원짜리 우표 1장의 값 1000원을 뺍니다.",
        },
        {
            "id": "step.assume_all_50won",
            "goal": "20장이 모두 50원짜리일 때의 금액을 구합니다.",
            "uses": ["quantity.100won_50won_total_count"],
            "relation_expr": "모두 50원짜리일 때의 금액 = 50 × 20",
            "expr": "50 * 20",
            "value": 1000,
            "explanation": "두 종류의 우표 20장이 모두 50원짜리라고 가정합니다.",
        },
        {
            "id": "step.find_amount_difference",
            "goal": "실제 금액과 가정한 금액의 차이를 구합니다.",
            "uses": ["amount.100won_50won_payment"],
            "relation_expr": "금액 차이 = 실제 금액 - 모두 50원짜리일 때의 금액",
            "expr": "1550 - 1000",
            "value": 550,
            "explanation": "100원짜리 우표가 섞여 있어서 실제 금액이 550원 더 큽니다.",
        },
        {
            "id": "step.find_100won_stamp_count",
            "goal": "100원짜리 우표 수를 구합니다.",
            "uses": [
                "stamp.100won",
                "stamp.50won",
            ],
            "relation_expr": "100원짜리 우표 수 = 금액 차이 ÷ 한 장을 바꿀 때 늘어나는 금액",
            "expr": "550 / (100 - 50)",
            "value": 11,
            "explanation": "50원짜리 한 장을 100원짜리로 바꿀 때마다 50원씩 늘어나므로 550을 50으로 나눕니다.",
        },
        {
            "id": "step.find_50won_stamp_count",
            "goal": "50원짜리 우표 수를 구합니다.",
            "uses": [
                "quantity.100won_50won_total_count",
                "quantity.100won_stamp_count",
            ],
            "relation_expr": "50원짜리 우표 수 = 두 종류의 전체 우표 수 - 100원짜리 우표 수",
            "expr": "20 - 11",
            "value": 9,
            "explanation": "두 종류의 우표는 모두 20장이므로 100원짜리 11장을 뺍니다.",
        },
    ],
    "checks": [
        {
            "id": "check.total_count",
            "description": "100원짜리와 50원짜리 우표 수의 합이 20장인지 확인합니다.",
            "expr": "11 + 9",
            "expected": 20,
            "actual": 20,
            "pass": True,
        },
        {
            "id": "check.total_payment",
            "description": "세 종류의 우표값을 모두 더하면 2550원인지 확인합니다.",
            "expr": "1000 * 1 + 100 * 11 + 50 * 9",
            "expected": 2550,
            "actual": 2550,
            "pass": True,
        },
    ],
    "answer": {
        "type": "multi_numeric",
        "values": [
            {
                "value": 11,
                "unit": "장",
                "target_ref": "quantity.100won_stamp_count",
            },
            {
                "value": 9,
                "unit": "장",
                "target_ref": "quantity.50won_stamp_count",
            },
        ],
    },
    "understanding": {
        "summary": (
            "전체 우표값에서 1000원짜리 우표값을 제외하고, 합계가 20장인 "
            "100원짜리와 50원짜리 우표의 수를 각각 구하는 문제입니다."
        ),
        "facts": [
            {
                "ref": "quantity.1000won_stamp_count",
                "label": "1000원짜리 우표 수",
                "value": 1,
                "unit": "장",
                "source": "explicit",
            },
            {
                "ref": "quantity.100won_50won_total_count",
                "label": "100원짜리와 50원짜리 우표의 합계 수",
                "value": 20,
                "unit": "장",
                "source": "explicit",
            },
            {
                "ref": "amount.total_payment",
                "label": "전체 우표값",
                "value": 2550,
                "unit": "원",
                "source": "explicit",
            },
            {
                "ref": "amount.100won_50won_payment",
                "label": "100원짜리와 50원짜리 우표값",
                "value": 1550,
                "unit": "원",
                "source": "derived",
            },
        ],
        "unknowns": [
            {
                "ref": "quantity.100won_stamp_count",
                "label": "100원짜리 우표 수",
                "unit": "장",
                "source": "unknown",
            },
            {
                "ref": "quantity.50won_stamp_count",
                "label": "50원짜리 우표 수",
                "unit": "장",
                "source": "unknown",
            },
        ],
        "relation": {
            "type": "count_and_value_system",
            "statement": (
                "100원짜리와 50원짜리 우표의 수를 합하면 20장이고, "
                "그 우표들의 금액을 합하면 1550원입니다."
            ),
            "symbolic": "x + y = 20, 100x + 50y = 1550",
            "uses": [
                "quantity.100won_stamp_count",
                "quantity.50won_stamp_count",
            ],
            "results": [
                "quantity.100won_stamp_count",
                "quantity.50won_stamp_count",
            ],
        },
        "diagnostic_questions": [
            {
                "id": "understand.exclude_1000won",
                "type": "multiple_choice",
                "prompt": "100원짜리와 50원짜리 우표값은 모두 얼마인가요?",
                "choices": [
                    "1000원",
                    "1550원",
                    "2550원",
                ],
                "answer_index": 1,
            },
            {
                "id": "understand.total_count",
                "type": "multiple_choice",
                "prompt": "20장은 어떤 우표들의 수를 합한 것인가요?",
                "choices": [
                    "세 종류 우표 전체",
                    "1000원짜리와 100원짜리 우표",
                    "100원짜리와 50원짜리 우표",
                ],
                "answer_index": 2,
            },
            {
                "id": "understand.replacement_difference",
                "type": "multiple_choice",
                "prompt": "50원짜리 우표 1장을 100원짜리로 바꾸면 우표값은 얼마 늘어나나요?",
                "choices": [
                    "50원",
                    "100원",
                    "150원",
                ],
                "answer_index": 0,
            },
        ],
        "student_restatement": {
            "prompt": "문제의 뜻을 말해 볼까요?",
            "template": (
                "전체 {total_payment}원에서 1000원짜리 우표값을 빼고, "
                "합해서 {total_count}장인 100원짜리와 50원짜리 우표의 수를 각각 구합니다."
            ),
            "answer": (
                "전체 2550원에서 1000원짜리 우표값을 빼고, 합해서 20장인 "
                "100원짜리와 50원짜리 우표의 수를 각각 구합니다."
            ),
        },
    },
}


SEMANTIC_ANSWER = SOLVABLE["answer"]
