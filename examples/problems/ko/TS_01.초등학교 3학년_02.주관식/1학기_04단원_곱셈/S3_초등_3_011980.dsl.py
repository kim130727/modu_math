"""ModuMath Problem DSL: 한 줄에 20개씩 3줄 비스킷 개수 구하기 (S3_초등_3_011980)"""

from __future__ import annotations

from modu_math.dsl import (
    Canvas,
    ProblemTemplate,
    RectSlot,
    Region,
    TextBoxSlot,
)


PROBLEM_ID = "S3_초등_3_011980"
PROBLEM_TITLE = "비스킷 20개씩 3줄의 전체 개수 구하기"


ANSWER = {
    "type": "short_answer",
    "value": 60,
    "unit": "개",
    "values": [60],
    "choices": [],
    "blanks": [
        {
            "id": "slot.answer.input",
            "slot_id": "slot.answer.input",
            "expected": 60,
        },
    ],
    "answer_key": [
        {
            "slot_id": "slot.answer.input",
            "value": 60,
            "diagnostics": [
                {
                    "id": "diag.forgot_zero",
                    "condition": "answer_equals_6",
                    "concept": "몇십 곱하기 몇",
                    "reason": "2 × 3 = 6만 계산하고 0을 붙이지 않음",
                    "feedback": "20개씩 3줄이므로 20 × 3 = 60(개)입니다.",
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
            {"id": "quantity.biscuits_per_row", "type": "quantity", "label": "한 줄의 비스킷 수", "value": 20, "unit": "개"},
            {"id": "quantity.rows", "type": "quantity", "label": "줄 수", "value": 3, "unit": "줄"},
            {"id": "quantity.total_biscuits", "type": "quantity", "label": "전체 비스킷 수", "value": 60, "unit": "개"},
        ],
        "relations": [
            {
                "id": "relation.multiplication",
                "type": "product_of",
                "multiplicand": "quantity.biscuits_per_row",
                "multiplier": "quantity.rows",
                "product": "quantity.total_biscuits",
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
        text="비스킷이 한 줄에 20개씩 3줄 있습니다. 비스킷은 모두 몇 개일까요?",
        x=32,
        y=24,
        width=836,
        height=88,
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
        y=142,
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
        y=142,
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
        y=142,
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
        y=142,
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
            height=228,
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
