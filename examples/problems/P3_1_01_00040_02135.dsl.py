from __future__ import annotations

from modu_math.dsl import (
    Canvas,
    ProblemTemplate,
    Region,
    TextBoxSlot,
)


PROBLEM_ID = "P3_1_01_00040_02135"
PROBLEM_TITLE = "받아올림이 있는 세 자리 수의 덧셈"


def build_problem_template() -> ProblemTemplate:
    return ProblemTemplate(
        id=PROBLEM_ID,
        title=PROBLEM_TITLE,
        canvas=Canvas(
            width=900,
            height=320,
            coordinate_mode="logical",
        ),
        regions=(
            Region(
                id="region.stem",
                role="stem",
                flow="absolute",
                slot_ids=(
                    "slot.instruction",
                    "slot.carry_hundreds",
                    "slot.carry_tens",
                    "slot.first_number",
                    "slot.plus_sign",
                    "slot.second_number",
                    "slot.horizontal_line",
                    "slot.answer_hundreds",
                    "slot.answer_tens",
                    "slot.answer_ones",
                ),
            ),
        ),
        slots=(
            TextBoxSlot(
                id="slot.instruction",
                x=38,
                y=20,
                width=824,
                height=42,
                text="□ 안에 알맞은 수를 써넣으시오.",
                font_size=24,
                font_family="Noto Sans KR",
                fill="#202124",
                align="left",
                valign="middle",
            ),
            TextBoxSlot(
                id="slot.carry_hundreds",
                x=92,
                y=70,
                width=34,
                height=36,
                text="□",
                font_size=34,
                font_family="Noto Sans KR",
                fill="#111111",
                align="center",
                valign="middle",
            ),
            TextBoxSlot(
                id="slot.carry_tens",
                x=132,
                y=70,
                width=34,
                height=36,
                text="□",
                font_size=34,
                font_family="Noto Sans KR",
                fill="#111111",
                align="center",
                valign="middle",
            ),
            TextBoxSlot(
                id="slot.first_number",
                x=88,
                y=108,
                width=120,
                height=42,
                text="6 6 4",
                font_size=28,
                font_family="Noto Sans KR",
                fill="#202124",
                align="left",
                valign="middle",
            ),
            TextBoxSlot(
                id="slot.plus_sign",
                x=48,
                y=166,
                width=32,
                height=42,
                text="+",
                font_size=28,
                font_family="Noto Sans KR",
                fill="#202124",
                align="center",
                valign="middle",
            ),
            TextBoxSlot(
                id="slot.second_number",
                x=88,
                y=166,
                width=120,
                height=42,
                text="2 5 7",
                font_size=28,
                font_family="Noto Sans KR",
                fill="#202124",
                align="left",
                valign="middle",
            ),
            TextBoxSlot(
                id="slot.horizontal_line",
                x=48,
                y=204,
                width=160,
                height=24,
                text="────────",
                font_size=24,
                font_family="Noto Sans KR",
                fill="#111111",
                align="left",
                valign="middle",
            ),
            TextBoxSlot(
                id="slot.answer_hundreds",
                x=76,
                y=234,
                width=42,
                height=48,
                text="□",
                font_size=42,
                font_family="Noto Sans KR",
                fill="#111111",
                align="center",
                valign="middle",
            ),
            TextBoxSlot(
                id="slot.answer_tens",
                x=119,
                y=234,
                width=42,
                height=48,
                text="□",
                font_size=42,
                font_family="Noto Sans KR",
                fill="#111111",
                align="center",
                valign="middle",
            ),
            TextBoxSlot(
                id="slot.answer_ones",
                x=162,
                y=234,
                width=42,
                height=48,
                text="□",
                font_size=42,
                font_family="Noto Sans KR",
                fill="#111111",
                align="center",
                valign="middle",
            ),
        ),
    )


PROBLEM_TEMPLATE = build_problem_template()


SEMANTIC = {
    "problem_id": PROBLEM_ID,
    "problem_type": "multi_blank_vertical_addition",
    "metadata": {
        "grade": 3,
        "semester": 1,
        "subject": "수학",
        "topic": "받아올림이 있는 세 자리 수의 덧셈",
        "language": "ko-KR",
    },
    "domain": {
        "objects": [
            {
                "id": "number.addend_1",
                "type": "number",
                "label": "첫 번째 수",
                "value": 664,
            },
            {
                "id": "number.addend_2",
                "type": "number",
                "label": "두 번째 수",
                "value": 257,
            },
            {
                "id": "carry.ones_to_tens",
                "type": "carry",
                "label": "일의 자리에서 십의 자리로 받아올림한 수",
                "value": 1,
            },
            {
                "id": "carry.tens_to_hundreds",
                "type": "carry",
                "label": "십의 자리에서 백의 자리로 받아올림한 수",
                "value": 1,
            },
            {
                "id": "digit.answer_hundreds",
                "type": "place_value_digit",
                "label": "답의 백의 자리 숫자",
                "place": "hundreds",
                "value": 9,
            },
            {
                "id": "digit.answer_tens",
                "type": "place_value_digit",
                "label": "답의 십의 자리 숫자",
                "place": "tens",
                "value": 2,
            },
            {
                "id": "digit.answer_ones",
                "type": "place_value_digit",
                "label": "답의 일의 자리 숫자",
                "place": "ones",
                "value": 1,
            },
            {
                "id": "number.sum",
                "type": "number",
                "label": "664와 257의 합",
                "value": 921,
            },
        ],
        "relations": [
            {
                "id": "relation.sum_of_addends",
                "type": "sum_of",
                "subject": "number.sum",
                "objects": [
                    "number.addend_1",
                    "number.addend_2",
                ],
            },
            {
                "id": "relation.ones_carry",
                "type": "carry_to",
                "subject": "carry.ones_to_tens",
                "from_place": "ones",
                "to_place": "tens",
            },
            {
                "id": "relation.tens_carry",
                "type": "carry_to",
                "subject": "carry.tens_to_hundreds",
                "from_place": "tens",
                "to_place": "hundreds",
            },
        ],
    },
    "answer": {
        "value": [1, 1, 9, 2, 1],
        "unit": "",
        "expression": "664 + 257 = 921",
        "items": [
            {
                "id": "answer.carry_hundreds",
                "value": 1,
            },
            {
                "id": "answer.carry_tens",
                "value": 1,
            },
            {
                "id": "answer.hundreds",
                "value": 9,
            },
            {
                "id": "answer.tens",
                "value": 2,
            },
            {
                "id": "answer.ones",
                "value": 1,
            },
        ],
    },
}

SEMANTIC_OVERRIDE = SEMANTIC


SOLVABLE = {
    "schema": "modu.solvable.v1.1",
    "problem_id": PROBLEM_ID,
    "problem_type": "multi_blank_vertical_addition",
    "inputs": {
        "target_label": "받아올림한 수와 덧셈 결과의 각 자리 숫자",
        "unit": "",
        "answer_type": "digit_list",
        "quantities": {
            "first_addend": 664,
            "second_addend": 257,
        },
        "place_values": {
            "first_addend": {
                "hundreds": 6,
                "tens": 6,
                "ones": 4,
            },
            "second_addend": {
                "hundreds": 2,
                "tens": 5,
                "ones": 7,
            },
        },
        "conditions": [
            "일의 자리부터 차례대로 계산합니다.",
            "각 자리의 합이 10 이상이면 바로 윗자리로 1을 받아올림합니다.",
            "받아올림한 수와 계산 결과를 각 네모 안에 씁니다.",
        ],
    },
    "given": [
        {
            "ref": "number.addend_1",
            "value": 664,
        },
        {
            "ref": "number.addend_2",
            "value": 257,
        },
    ],
    "target": {
        "ref": "answer.vertical_addition_blanks",
        "type": "digit_list",
    },
    "method": "일의 자리부터 더하고 받아올림한 수를 다음 자리의 계산에 포함한다.",
    "plan": [
        "일의 자리의 숫자 4와 7을 더한다.",
        "일의 자리에서 생긴 받아올림을 십의 자리에 표시한다.",
        "십의 자리의 숫자 6과 5에 받아올림한 1을 더한다.",
        "십의 자리에서 생긴 받아올림을 백의 자리에 표시한다.",
        "백의 자리의 숫자 6과 2에 받아올림한 1을 더한다.",
        "계산 결과의 백의 자리, 십의 자리, 일의 자리 숫자를 쓴다.",
    ],
    "steps": [
        {
            "id": "step.add_ones",
            "expr": "4 + 7",
            "value": 11,
            "explanation": "일의 자리에서 4와 7을 더하면 11입니다.",
        },
        {
            "id": "step.write_ones_and_carry",
            "expr": "11 = 1 × 10 + 1",
            "value": {
                "carry": 1,
                "digit": 1,
            },
            "explanation": "일의 자리에 1을 쓰고 십의 자리로 1을 받아올림합니다.",
        },
        {
            "id": "step.add_tens",
            "expr": "6 + 5 + 1",
            "value": 12,
            "explanation": "십의 자리에서 6과 5에 받아올림한 1을 더하면 12입니다.",
        },
        {
            "id": "step.write_tens_and_carry",
            "expr": "12 = 1 × 10 + 2",
            "value": {
                "carry": 1,
                "digit": 2,
            },
            "explanation": "십의 자리에 2를 쓰고 백의 자리로 1을 받아올림합니다.",
        },
        {
            "id": "step.add_hundreds",
            "expr": "6 + 2 + 1",
            "value": 9,
            "explanation": "백의 자리에서 6과 2에 받아올림한 1을 더하면 9입니다.",
        },
        {
            "id": "step.compose_answer",
            "expr": "900 + 20 + 1",
            "value": 921,
            "explanation": "각 자리 숫자를 차례대로 쓰면 921입니다.",
        },
    ],
    "checks": [
        {
            "id": "check.ones_place",
            "expr": "4 + 7",
            "expected": 11,
            "actual": 11,
            "pass": True,
        },
        {
            "id": "check.tens_place",
            "expr": "6 + 5 + 1",
            "expected": 12,
            "actual": 12,
            "pass": True,
        },
        {
            "id": "check.hundreds_place",
            "expr": "6 + 2 + 1",
            "expected": 9,
            "actual": 9,
            "pass": True,
        },
        {
            "id": "check.total",
            "expr": "664 + 257",
            "expected": 921,
            "actual": 921,
            "pass": True,
        },
        {
            "id": "check.inverse_operation",
            "expr": "921 - 257",
            "expected": 664,
            "actual": 664,
            "pass": True,
        },
    ],
    "answer": {
        "value": [1, 1, 9, 2, 1],
        "unit": "",
        "expression": "664 + 257 = 921",
        "items": [
            {
                "id": "answer.carry_hundreds",
                "value": 1,
            },
            {
                "id": "answer.carry_tens",
                "value": 1,
            },
            {
                "id": "answer.hundreds",
                "value": 9,
            },
            {
                "id": "answer.tens",
                "value": 2,
            },
            {
                "id": "answer.ones",
                "value": 1,
            },
        ],
    },
}

SEMANTIC_ANSWER = SOLVABLE["answer"]