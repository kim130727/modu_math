"""ModuMath Problem DSL: 자동차 바퀴 수 구하기 (S3_초등_3_011907)"""

from __future__ import annotations

from modu_math.dsl import (
    Canvas,
    ProblemTemplate,
    RectSlot,
    Region,
    TextBoxSlot,
)


PROBLEM_ID = "S3_초등_3_011907"
PROBLEM_TITLE = "주차장 자동차 바퀴 수 구하기"


ANSWER = {
    "type": "short_answer",
    "value": 72,
    "unit": "개",
    "values": [72],
    "choices": [],
    "blanks": [
        {
            "id": "slot.answer.input",
            "slot_id": "slot.answer.input",
            "expected": 72,
        },
    ],
    "answer_key": [
        {
            "slot_id": "slot.answer.input",
            "value": 72,
            "diagnostics": [
                {
                    "id": "diag.forgot_carry",
                    "condition": "answer_equals_42",
                    "concept": "올림이 있는 곱셈",
                    "reason": "8 × 4 = 32에서 십의 자리로 올린 3을 더하지 않음",
                    "feedback": "일의 자리 계산 8 × 4 = 32에서 올린 3을 십의 자리 계산 10 × 4 = 40에 꼭 더해 보세요.",
                },
            ],
        },
    ],
}


SEMANTIC = {
    "problem_id": PROBLEM_ID,
    "problem_type": "short_answer_multiplication_word_problem",
    "metadata": {
        "school": "초등학교",
        "grade": 3,
        "semester": 1,
        "chapter": "04단원_곱셈",
        "subject": "수학",
        "language": "ko-KR",
    },
    "domain": {
        "objects": [
            {"id": "quantity.cars", "type": "quantity", "label": "자동차 수", "value": 18, "unit": "대"},
            {"id": "quantity.wheels_per_car", "type": "quantity", "label": "자동차 1대의 바퀴 수", "value": 4, "unit": "개"},
            {"id": "quantity.total_wheels", "type": "quantity", "label": "전체 바퀴 수", "value": 72, "unit": "개"},
        ],
        "relations": [
            {
                "id": "relation.multiplication",
                "type": "product_of",
                "multiplicand": "quantity.cars",
                "multiplier": "quantity.wheels_per_car",
                "product": "quantity.total_wheels",
            },
        ],
    },
    "answer": ANSWER,
}

SEMANTIC_OVERRIDE = SEMANTIC


def build_problem_template() -> ProblemTemplate:
    stem_slot = TextBoxSlot(
        id="slot.stem.question",
        prompt="",
        text="주차장에 자동차가 18대 있습니다. 자동차의 바퀴는 4개씩입니다. 주차장에 있는 자동차의 바퀴는 모두 몇 개일까요?",
        x=32,
        y=24,
        width=836,
        height=104,
        font_size=26,
        font_family='"Noto Sans KR", sans-serif',
        fill="#202124",
        align="left",
        valign="top",
        line_height=1.5,
    )

    paren_left = TextBoxSlot(
        id="slot.answer.paren_left",
        prompt="",
        text="(",
        x=560,
        y=160,
        width=26,
        height=54,
        font_size=26,
        font_family='"Noto Sans KR", sans-serif',
        fill="#202124",
        align="center",
        valign="middle",
    )

    answer_input = RectSlot(
        id="slot.answer.input",
        prompt="",
        x=592,
        y=160,
        width=110,
        height=54,
        fill="#ffffff",
        stroke="#111827",
        stroke_width=1.4,
        interaction={
            "type": "input",
            "role": "answer",
            "value_type": "integer",
            "max_length": 3,
            "include_in_submission": True,
            "order": 0,
            "group_id": "final_answer",
            "auto_advance": False,
            "keyboard": "number",
        },
        input_style={
            "font_size_mode": "auto",
            "font_size_adjust": 0,
            "min_font_size": 16,
            "max_font_size": 28,
            "font_weight": 700,
            "horizontal_align": "center",
            "vertical_align": "middle",
            "padding": 6,
            "text_color": "#222222",
        },
    )

    unit_slot = TextBoxSlot(
        id="slot.answer.unit",
        prompt="",
        text="개",
        x=710,
        y=160,
        width=36,
        height=54,
        font_size=26,
        font_family='"Noto Sans KR", sans-serif',
        fill="#202124",
        align="left",
        valign="middle",
    )

    paren_right = TextBoxSlot(
        id="slot.answer.paren_right",
        prompt="",
        text=")",
        x=750,
        y=160,
        width=26,
        height=54,
        font_size=26,
        font_family='"Noto Sans KR", sans-serif',
        fill="#202124",
        align="center",
        valign="middle",
    )

    slots = (
        stem_slot,
        paren_left,
        answer_input,
        unit_slot,
        paren_right,
    )

    return ProblemTemplate(
        id=PROBLEM_ID,
        title=PROBLEM_TITLE,
        canvas=Canvas(
            width=900,
            height=246,
            coordinate_mode="logical",
        ),
        regions=(
            Region(
                id="region.stem",
                role="stem",
                flow="absolute",
                slot_ids=tuple(slot.id for slot in slots),
            ),
        ),
        slots=slots,
    )


PROBLEM_TEMPLATE = build_problem_template()
