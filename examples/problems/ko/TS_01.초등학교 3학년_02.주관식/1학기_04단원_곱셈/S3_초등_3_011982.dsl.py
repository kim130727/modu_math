"""ModuMath Problem DSL: 곱셈식 41 × □ = 82에서 □ 구하기 (S3_초등_3_011982)"""

from __future__ import annotations

from modu_math.dsl import (
    Canvas,
    ProblemTemplate,
    RectSlot,
    Region,
    TextBoxSlot,
)


PROBLEM_ID = "S3_초등_3_011982"
PROBLEM_TITLE = "41 × □ = 82에서 □ 구하기"


ANSWER = {
    "type": "short_answer",
    "value": 2,
    "unit": "",
    "values": [2],
    "choices": [],
    "blanks": [
        {
            "id": "slot.answer.input",
            "slot_id": "slot.answer.input",
            "expected": 2,
        },
    ],
    "answer_key": [
        {
            "slot_id": "slot.answer.input",
            "value": 2,
            "diagnostics": [
                {
                    "id": "diag.missing_multiplier_error",
                    "condition": "answer_not_equals_2",
                    "concept": "몇십몇 × 몇의 역산",
                    "reason": "41에 곱해서 82가 되는 수를 잘못 구함",
                    "feedback": "40 × □ = 80, 1 × □ = 2를 만족하는 수를 생각해 보세요. □ = 2입니다.",
                },
            ],
        },
    ],
}


SEMANTIC = {
    "problem_id": PROBLEM_ID,
    "problem_type": "short_answer_multiplication_missing_factor",
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
            {"id": "quantity.multiplicand", "type": "quantity", "label": "곱해지는 수", "value": 41},
            {"id": "quantity.multiplier", "type": "quantity", "label": "곱하는 수 □", "value": 2},
            {"id": "quantity.product", "type": "quantity", "label": "곱", "value": 82},
        ],
        "relations": [
            {
                "id": "relation.multiplication",
                "type": "product_of",
                "multiplicand": "quantity.multiplicand",
                "multiplier": "quantity.multiplier",
                "product": "quantity.product",
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
        text="□ 안에 알맞은 수를 구하세요.",
        x=32,
        y=24,
        width=820,
        height=44,
        font_size=26,
        font_family='"Noto Sans KR", sans-serif',
        fill="#202124",
        align="left",
        valign="top",
        line_height=1.45,
    )

    equation_box = RectSlot(
        id="slot.diagram.equation_box",
        prompt="",
        x=230,
        y=92,
        width=440,
        height=96,
        fill="#ffffff",
        stroke="#86c57a",
        stroke_width=2.2,
    )

    equation_left = TextBoxSlot(
        id="slot.diagram.equation_left",
        prompt="",
        text="41 ×",
        x=290,
        y=112,
        width=110,
        height=58,
        font_size=36,
        font_family='"Noto Sans KR", sans-serif',
        fill="#111827",
        align="right",
        valign="middle",
    )

    blank_square = RectSlot(
        id="slot.diagram.blank_square",
        prompt="",
        x=410,
        y=114,
        width=54,
        height=54,
        fill="#ffffff",
        stroke="#9ca3af",
        stroke_width=2.4,
    )

    equation_right = TextBoxSlot(
        id="slot.diagram.equation_right",
        prompt="",
        text="= 82",
        x=472,
        y=112,
        width=110,
        height=58,
        font_size=36,
        font_family='"Noto Sans KR", sans-serif',
        fill="#111827",
        align="left",
        valign="middle",
    )

    paren_left = TextBoxSlot(
        id="slot.answer.paren_left",
        prompt="",
        text="(",
        x=560,
        y=220,
        width=28,
        height=54,
        font_size=28,
        font_family='"Noto Sans KR", sans-serif',
        fill="#202124",
        align="center",
        valign="middle",
    )

    answer_input = RectSlot(
        id="slot.answer.input",
        prompt="",
        x=594,
        y=220,
        width=170,
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

    paren_right = TextBoxSlot(
        id="slot.answer.paren_right",
        prompt="",
        text=")",
        x=770,
        y=220,
        width=28,
        height=54,
        font_size=28,
        font_family='"Noto Sans KR", sans-serif',
        fill="#202124",
        align="center",
        valign="middle",
    )

    slots = (
        stem_slot,
        equation_box,
        equation_left,
        blank_square,
        equation_right,
        paren_left,
        answer_input,
        paren_right,
    )

    return ProblemTemplate(
        id=PROBLEM_ID,
        title=PROBLEM_TITLE,
        canvas=Canvas(
            width=900,
            height=300,
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
