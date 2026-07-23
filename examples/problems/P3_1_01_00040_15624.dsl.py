from __future__ import annotations

from modu_math.dsl import (
    BlankSlot,
    Canvas,
    ProblemTemplate,
    Region,
    TextBoxSlot,
)


PROBLEM_ID = "P3_1_01_00040_15624"
PROBLEM_TITLE = "숫자 카드로 만든 가장 큰 수와 가장 작은 수의 합"


def build_problem_template() -> ProblemTemplate:
    return ProblemTemplate(
        id=PROBLEM_ID,
        title=PROBLEM_TITLE,
        canvas=Canvas(
            width=960,
            height=225,
            coordinate_mode="logical",
        ),
        regions=(
            Region(
                id="region.stem",
                role="stem",
                flow="vertical",
                slot_ids=(
                    "slot.instruction",
                    "slot.question1",
                    "slot.answer1",
                    "slot.question2",
                    "slot.answer2",
                    "slot.question3",
                    "slot.answer3",
                ),
            ),
        ),
        slots=(
            TextBoxSlot(
                id="slot.instruction",
                x=20,
                y=12,
                width=920,
                height=48,
                text=(
                    "2, 4, 6의 숫자 카드를 한 번씩만 사용하여 세 자리 수를 만들려고 합니다. "
                    "만들 수 있는 가장 큰 수와 가장 작은 수의 합을 구하려고 할 때 물음에 답하시오."
                ),
                font_size=18,
                font_family="Noto Sans KR",
                fill="#202124",
                line_height=1.4,
                align="left",
                valign="top",
            ),
            TextBoxSlot(
                id="slot.question1",
                x=20,
                y=68,
                width=920,
                height=28,
                text="(1) 숫자 카드를 이용하여 만들 수 있는 가장 큰 세 자리 수를 쓰시오.",
                font_size=18,
                font_family="Noto Sans KR",
                fill="#202124",
                align="left",
                valign="middle",
            ),
            BlankSlot(
                id="slot.answer1",
                prompt="(1) 가장 큰 세 자리 수",
                answer_key="642",
                placeholder="",
            ),
            TextBoxSlot(
                id="slot.question2",
                x=20,
                y=105,
                width=920,
                height=28,
                text="(2) 숫자 카드를 이용하여 만들 수 있는 가장 작은 세 자리 수를 쓰시오.",
                font_size=18,
                font_family="Noto Sans KR",
                fill="#202124",
                align="left",
                valign="middle",
            ),
            BlankSlot(
                id="slot.answer2",
                prompt="(2) 가장 작은 세 자리 수",
                answer_key="246",
                placeholder="",
            ),
            TextBoxSlot(
                id="slot.question3",
                x=20,
                y=142,
                width=920,
                height=28,
                text=(
                    "(3) 숫자 카드를 이용하여 만들 수 있는 가장 큰 세 자리 수와 "
                    "가장 작은 세 자리 수의 합을 구하시오."
                ),
                font_size=18,
                font_family="Noto Sans KR",
                fill="#202124",
                align="left",
                valign="middle",
            ),
            BlankSlot(
                id="slot.answer3",
                prompt="(3) 가장 큰 수와 가장 작은 수의 합",
                answer_key="888",
                placeholder="",
            ),
        ),
        diagrams=(),
        groups=(),
        constraints=(),
        tags=(
            "grade-3",
            "three-digit-number",
            "number-cards",
            "place-value",
            "addition",
            "multi-answer",
        ),
    )


PROBLEM_TEMPLATE = build_problem_template()


ANSWER = {
    "type": "multi_numeric",
    "value": [642, 246, 888],
    "unit": "",
    "blanks": [
        {
            "id": "slot.answer1",
            "type": "number",
            "value": 642,
            "unit": "",
            "target_ref": "number.largest",
        },
        {
            "id": "slot.answer2",
            "type": "number",
            "value": 246,
            "unit": "",
            "target_ref": "number.smallest",
        },
        {
            "id": "slot.answer3",
            "type": "number",
            "value": 888,
            "unit": "",
            "target_ref": "quantity.sum_largest_smallest",
        },
    ],
    "choices": [],
    "answer_key": [
        {
            "blank_id": "slot.answer1",
            "value": 642,
            "unit": "",
        },
        {
            "blank_id": "slot.answer2",
            "value": 246,
            "unit": "",
        },
        {
            "blank_id": "slot.answer3",
            "value": 888,
            "unit": "",
        },
    ],
    "sentence": "가장 큰 수는 642, 가장 작은 수는 246이고 두 수의 합은 888입니다.",
}


SEMANTIC_OVERRIDE = {
    "problem_id": PROBLEM_ID,
    "problem_type": "number_card_extremes_and_sum_multi_answer",
    "metadata": {
        "grade": 3,
        "semester": 1,
        "subject": "수학",
        "topic": "세 자리 수의 덧셈",
        "language": "ko-KR",
        "question": (
            "2, 4, 6의 숫자 카드를 한 번씩 사용하여 만들 수 있는 가장 큰 세 자리 수, "
            "가장 작은 세 자리 수, 두 수의 합을 구합니다."
        ),
        "instruction": (
            "숫자의 크기를 비교하여 카드를 백의 자리부터 배열하고, "
            "만든 두 세 자리 수를 더합니다."
        ),
    },
    "domain": {
        "objects": [
            {
                "id": "card.digit_2",
                "type": "digit_card",
                "label": "숫자 카드 2",
                "value": 2,
            },
            {
                "id": "card.digit_4",
                "type": "digit_card",
                "label": "숫자 카드 4",
                "value": 4,
            },
            {
                "id": "card.digit_6",
                "type": "digit_card",
                "label": "숫자 카드 6",
                "value": 6,
            },
            {
                "id": "number.largest",
                "type": "derived_number",
                "label": "만들 수 있는 가장 큰 세 자리 수",
                "value": 642,
                "unit": "",
            },
            {
                "id": "number.smallest",
                "type": "derived_number",
                "label": "만들 수 있는 가장 작은 세 자리 수",
                "value": 246,
                "unit": "",
            },
            {
                "id": "quantity.sum_largest_smallest",
                "type": "derived_quantity",
                "label": "가장 큰 세 자리 수와 가장 작은 세 자리 수의 합",
                "value": 888,
                "unit": "",
            },
        ],
        "relations": [
            {
                "id": "relation.use_each_card_once",
                "type": "permutation_constraint",
                "card_ids": [
                    "card.digit_2",
                    "card.digit_4",
                    "card.digit_6",
                ],
                "usage_count_per_number": 1,
                "digit_count": 3,
            },
            {
                "id": "relation.largest_descending_order",
                "type": "descending_place_value_arrangement",
                "subject": "number.largest",
                "digit_order": [6, 4, 2],
                "equation": "6×100 + 4×10 + 2 = 642",
            },
            {
                "id": "relation.smallest_ascending_order",
                "type": "ascending_place_value_arrangement",
                "subject": "number.smallest",
                "digit_order": [2, 4, 6],
                "equation": "2×100 + 4×10 + 6 = 246",
            },
            {
                "id": "relation.sum_extremes",
                "type": "sum_of",
                "subject": "quantity.sum_largest_smallest",
                "objects": [
                    "number.largest",
                    "number.smallest",
                ],
                "equation": "642 + 246 = 888",
            },
        ],
        "problem_solving": {
            "understand": {
                "given_refs": [
                    "card.digit_2",
                    "card.digit_4",
                    "card.digit_6",
                ],
                "target_ref": "answer.all",
                "condition_refs": [
                    "relation.use_each_card_once",
                    "relation.largest_descending_order",
                    "relation.smallest_ascending_order",
                    "relation.sum_extremes",
                ],
            },
            "plan": {
                "method": "arrange_digits_by_place_value_then_add",
                "description": (
                    "큰 수는 큰 숫자부터, 작은 수는 작은 숫자부터 높은 자리에 놓고 "
                    "두 수를 더합니다."
                ),
            },
            "execute": {
                "expected_operations": [
                    "descending_arrangement",
                    "ascending_arrangement",
                    "addition",
                ],
            },
            "review": {
                "check_methods": [
                    "digit_usage_check",
                    "place_value_extreme_check",
                    "inverse_subtraction",
                ],
            },
        },
    },
    "answer": ANSWER,
}


SOLVABLE = {
    "schema": "modu.solvable.v1.2",
    "problem_id": PROBLEM_ID,
    "problem_type": "number_card_extremes_and_sum_multi_answer",
    "inputs": {
        "target_label": "가장 큰 세 자리 수, 가장 작은 세 자리 수와 두 수의 합",
        "unit": "",
        "digits": [2, 4, 6],
        "conditions": [
            "2, 4, 6의 숫자 카드를 사용합니다.",
            "하나의 세 자리 수를 만들 때 각 숫자 카드는 한 번씩만 사용합니다.",
            "가장 큰 세 자리 수와 가장 작은 세 자리 수를 각각 만듭니다.",
            "마지막에 두 수를 더합니다.",
        ],
    },
    "given": [
        {
            "ref": "card.digit_2",
            "value": {
                "digit": 2,
                "usage_count_per_number": 1,
            },
        },
        {
            "ref": "card.digit_4",
            "value": {
                "digit": 4,
                "usage_count_per_number": 1,
            },
        },
        {
            "ref": "card.digit_6",
            "value": {
                "digit": 6,
                "usage_count_per_number": 1,
            },
        },
    ],
    "target": {
        "ref": "answer.all",
        "type": "number_list",
    },
    "understanding": {
        "summary": (
            "숫자 카드 2, 4, 6을 한 번씩 사용하여 가장 큰 세 자리 수와 "
            "가장 작은 세 자리 수를 만들고 두 수의 합을 구하는 문제입니다."
        ),
        "facts": [
            {
                "ref": "card.digit_2",
                "label": "사용할 숫자 카드",
                "value": 2,
                "unit": "",
                "source": "explicit",
            },
            {
                "ref": "card.digit_4",
                "label": "사용할 숫자 카드",
                "value": 4,
                "unit": "",
                "source": "explicit",
            },
            {
                "ref": "card.digit_6",
                "label": "사용할 숫자 카드",
                "value": 6,
                "unit": "",
                "source": "explicit",
            },
            {
                "ref": "condition.use_once",
                "label": "각 숫자 카드의 사용 횟수",
                "value": 1,
                "unit": "번",
                "source": "explicit",
            },
        ],
        "unknowns": [
            {
                "ref": "number.largest",
                "label": "만들 수 있는 가장 큰 세 자리 수",
                "unit": "",
                "source": "unknown",
            },
            {
                "ref": "number.smallest",
                "label": "만들 수 있는 가장 작은 세 자리 수",
                "unit": "",
                "source": "unknown",
            },
            {
                "ref": "quantity.sum_largest_smallest",
                "label": "가장 큰 수와 가장 작은 수의 합",
                "unit": "",
                "source": "unknown",
            },
        ],
        "relation": {
            "type": "digit_permutation_extremes_then_addition",
            "statement": (
                "가장 큰 수는 큰 숫자부터 높은 자리에 놓고, 가장 작은 수는 "
                "작은 숫자부터 높은 자리에 놓은 뒤 두 수를 더합니다."
            ),
            "symbolic": "largest(2,4,6)=642; smallest(2,4,6)=246; 642+246=888",
            "uses": [
                "card.digit_2",
                "card.digit_4",
                "card.digit_6",
            ],
            "result": "answer.all",
        },
        "diagnostic_questions": [
            {
                "id": "understand.use_once",
                "type": "multiple_choice",
                "prompt": "세 자리 수 하나를 만들 때 각 숫자 카드는 몇 번 사용하나요?",
                "choices": [
                    "한 번씩 사용합니다.",
                    "두 번씩 사용합니다.",
                    "사용 횟수에 제한이 없습니다.",
                ],
                "answer_index": 0,
            },
            {
                "id": "understand.largest_order",
                "type": "multiple_choice",
                "prompt": "가장 큰 수를 만들려면 백의 자리에 어떤 숫자를 놓아야 하나요?",
                "choices": [
                    "2",
                    "4",
                    "6",
                ],
                "answer_index": 2,
            },
            {
                "id": "understand.smallest_order",
                "type": "multiple_choice",
                "prompt": "가장 작은 수를 만들려면 백의 자리에 어떤 숫자를 놓아야 하나요?",
                "choices": [
                    "2",
                    "4",
                    "6",
                ],
                "answer_index": 0,
            },
        ],
        "student_restatement": {
            "prompt": "문제의 요지를 말해 볼까요?",
            "template": (
                "{digits}을 한 번씩 사용하여 가장 큰 수와 가장 작은 수를 만들고 "
                "두 수를 더합니다."
            ),
            "answer": (
                "2, 4, 6을 한 번씩 사용하여 가장 큰 수와 가장 작은 수를 만들고 "
                "두 수를 더합니다."
            ),
        },
    },
    "method": (
        "숫자 카드를 내림차순과 오름차순으로 각각 배열하여 가장 큰 수와 "
        "가장 작은 수를 만들고, 두 수를 더합니다."
    ),
    "plan": [
        "숫자 카드 2, 4, 6의 크기를 비교합니다.",
        "큰 숫자부터 백, 십, 일의 자리에 놓아 가장 큰 수를 만듭니다.",
        "작은 숫자부터 백, 십, 일의 자리에 놓아 가장 작은 수를 만듭니다.",
        "만든 가장 큰 수와 가장 작은 수를 더합니다.",
    ],
    "steps": [
        {
            "id": "step.order_digits",
            "goal": "숫자 카드의 크기 순서를 확인합니다.",
            "uses": [
                "card.digit_2",
                "card.digit_4",
                "card.digit_6",
            ],
            "relation_expr": "2 < 4 < 6",
            "expr": "2 < 4 < 6",
            "value": [2, 4, 6],
            "explanation": "숫자의 크기는 2, 4, 6의 순서입니다.",
        },
        {
            "id": "step.make_largest",
            "goal": "가장 큰 세 자리 수를 만듭니다.",
            "uses": [
                "card.digit_6",
                "card.digit_4",
                "card.digit_2",
            ],
            "relation_expr": "6×100 + 4×10 + 2",
            "expr": "600 + 40 + 2",
            "value": 642,
            "explanation": (
                "가장 큰 숫자 6을 백의 자리에, 4를 십의 자리에, "
                "2를 일의 자리에 놓으면 가장 큰 수는 642입니다."
            ),
        },
        {
            "id": "step.make_smallest",
            "goal": "가장 작은 세 자리 수를 만듭니다.",
            "uses": [
                "card.digit_2",
                "card.digit_4",
                "card.digit_6",
            ],
            "relation_expr": "2×100 + 4×10 + 6",
            "expr": "200 + 40 + 6",
            "value": 246,
            "explanation": (
                "가장 작은 숫자 2를 백의 자리에, 4를 십의 자리에, "
                "6을 일의 자리에 놓으면 가장 작은 수는 246입니다."
            ),
        },
        {
            "id": "step.add_extremes",
            "goal": "가장 큰 수와 가장 작은 수의 합을 구합니다.",
            "uses": [
                "number.largest",
                "number.smallest",
            ],
            "relation_expr": "합 = 가장 큰 수 + 가장 작은 수",
            "expr": "642 + 246",
            "value": 888,
            "explanation": "가장 큰 수 642와 가장 작은 수 246을 더하면 888입니다.",
        },
    ],
    "checks": [
        {
            "id": "check.largest_digit_usage",
            "expr": "sorted([6, 4, 2]) == [2, 4, 6]",
            "expected": True,
            "actual": True,
            "pass": True,
        },
        {
            "id": "check.smallest_digit_usage",
            "expr": "sorted([2, 4, 6]) == [2, 4, 6]",
            "expected": True,
            "actual": True,
            "pass": True,
        },
        {
            "id": "check.extreme_order",
            "expr": "642 > 246",
            "expected": True,
            "actual": True,
            "pass": True,
        },
        {
            "id": "check.inverse_subtraction",
            "expr": "888 - 642",
            "expected": 246,
            "actual": 246,
            "pass": True,
        },
    ],
    "answer": ANSWER,
}


SEMANTIC_ANSWER = SOLVABLE["answer"]
