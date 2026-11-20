"""ModuMath Problem DSL: 5 cm 6 mm를 소수로 나타내기 (S3_초등_3_012018)"""

from __future__ import annotations

from modu_math.dsl import (
    Canvas,
    ProblemTemplate,
    RectSlot,
    Region,
    TextBoxSlot,
)


PROBLEM_ID = "S3_초등_3_012018"
PROBLEM_TITLE = "5 cm 6 mm를 cm 단위 소수로 나타내기"


ANSWER = {
    "type": "short_answer",
    "value": 5.6,
    "unit": "cm",
    "values": [5.6, "5.6"],
    "choices": [],
    "blanks": [
        {
            "id": "slot.answer.input",
            "slot_id": "slot.answer.input",
            "expected": 5.6,
        },
    ],
    "answer_key": [
        {
            "slot_id": "slot.answer.input",
            "value": 5.6,
            "diagnostics": [
                {
                    "id": "diag.mm_to_cm_decimal_error",
                    "condition": "answer_not_equals_5_6",
                    "concept": "소수로 나타내기 (1 mm = 0.1 cm)",
                    "reason": "6 mm를 0.6 cm로 바꾸어 더하지 못함",
                    "feedback": "1 mm = 0.1 cm이므로 6 mm = 0.6 cm입니다. 따라서 5 cm 6 mm = 5.6 cm입니다.",
                },
            ],
        },
    ],
}


SEMANTIC = {
    "problem_id": PROBLEM_ID,
    "problem_type": "short_answer_decimal_length_conversion",
    "metadata": {
        "school": "초등학교",
        "grade": 3,
        "semester": 1,
        "chapter": "06단원_분수와 소수",
        "subject": "수학",
        "language": "ko-KR",
    },
    "domain": {
        "objects": [
            {"id": "quantity.ribbon_length", "type": "quantity", "label": "리본 길이", "cm": 5, "mm": 6, "decimal_cm": 5.6},
        ],
        "relations": [
            {
                "id": "relation.unit_conversion",
                "type": "equals_decimal_cm",
                "from_id": "quantity.ribbon_length",
                "value": 5.6,
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
        text="은혜가 리본의 길이를 재어 보았더니 5 cm 6 mm였습니다. 이 리본의 길이는 몇 cm일까요?",
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
        x=540,
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
        x=572,
        y=160,
        width=130,
        height=54,
        fill="#ffffff",
        stroke="#111827",
        stroke_width=1.4,
        interaction={
            "type": "input",
            "role": "answer",
            "value_type": "text",
            "max_length": 6,
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
        text="cm",
        x=710,
        y=160,
        width=50,
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
        x=766,
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
