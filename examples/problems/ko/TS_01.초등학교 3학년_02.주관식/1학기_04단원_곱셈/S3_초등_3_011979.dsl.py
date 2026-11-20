"""ModuMath Problem DSL: 한 봉지에 10개씩 5봉지 배 개수 구하기 (S3_초등_3_011979)"""

from __future__ import annotations

from modu_math.dsl import (
    Canvas,
    ProblemTemplate,
    RectSlot,
    Region,
    TextBoxSlot,
)


PROBLEM_ID = "S3_초등_3_011979"
PROBLEM_TITLE = "배 10개씩 5봉지의 전체 개수 구하기"


ANSWER = {
    "type": "short_answer",
    "value": 50,
    "unit": "개",
    "values": [50],
    "choices": [],
    "blanks": [
        {
            "id": "slot.answer.input",
            "slot_id": "slot.answer.input",
            "expected": 50,
        },
    ],
    "answer_key": [
        {
            "slot_id": "slot.answer.input",
            "value": 50,
            "diagnostics": [
                {
                    "id": "diag.multiplication_error",
                    "condition": "answer_not_equals_50",
                    "concept": "몇십 곱하기 몇",
                    "reason": "10 × 5의 계산을 잘못함",
                    "feedback": "10개씩 5봉지이므로 10 × 5 = 50(개)입니다.",
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
            {"id": "quantity.pears_per_bag", "type": "quantity", "label": "한 봉지의 배 수", "value": 10, "unit": "개"},
            {"id": "quantity.bags", "type": "quantity", "label": "봉지 수", "value": 5, "unit": "봉지"},
            {"id": "quantity.total_pears", "type": "quantity", "label": "전체 배 수", "value": 50, "unit": "개"},
        ],
        "relations": [
            {
                "id": "relation.multiplication",
                "type": "product_of",
                "multiplicand": "quantity.pears_per_bag",
                "multiplier": "quantity.bags",
                "product": "quantity.total_pears",
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
        text="한 봉지에 배가 10개씩 들어 있습니다. 5봉지에 들어 있는 배는 모두 몇 개일까요?",
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
