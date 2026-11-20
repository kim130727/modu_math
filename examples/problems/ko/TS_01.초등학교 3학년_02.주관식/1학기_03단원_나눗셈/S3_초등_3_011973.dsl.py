"""ModuMath Problem DSL: 나눗셈식에서 □ 안에 알맞은 수 구하기 (S3_초등_3_011973)"""

from __future__ import annotations

from modu_math.dsl import (
    Canvas,
    ProblemTemplate,
    RectSlot,
    Region,
    TextBoxSlot,
)


PROBLEM_ID = "S3_초등_3_011973"
PROBLEM_TITLE = "□ ÷ 4 = 8에서 □ 구하기"


ANSWER = {
    "type": "short_answer",
    "value": 32,
    "unit": "",
    "values": [32],
    "choices": [],
    "blanks": [
        {
            "id": "slot.answer.input",
            "slot_id": "slot.answer.input",
            "expected": 32,
        },
    ],
    "answer_key": [
        {
            "slot_id": "slot.answer.input",
            "value": 32,
            "diagnostics": [
                {
                    "id": "diag.divided_instead_of_multiplied",
                    "condition": "answer_equals_2",
                    "concept": "곱셈과 나눗셈의 관계",
                    "reason": "8 ÷ 4를 계산하여 2라고 답함",
                    "feedback": "□ ÷ 4 = 8은 4 × 8 = □로 바꾸어 풀 수 있습니다. 4 × 8을 계산해 보세요.",
                },
                {
                    "id": "diag.multiplication_fact_error",
                    "condition": "answer_not_equals_32",
                    "concept": "곱셈과 나눗셈의 관계",
                    "reason": "4 × 8의 계산을 틀림",
                    "feedback": "4 × 8 = 32이므로 □ 안에 알맞은 수는 32입니다.",
                },
            ],
        },
    ],
}


SEMANTIC = {
    "problem_id": PROBLEM_ID,
    "problem_type": "short_answer_division_missing_dividend",
    "metadata": {
        "school": "초등학교",
        "grade": 3,
        "semester": 1,
        "chapter": "03단원_나눗셈",
        "subject": "수학",
        "language": "ko-KR",
    },
    "domain": {
        "objects": [
            {"id": "quantity.dividend", "type": "quantity", "label": "나누어지는 수 □", "value": 32},
            {"id": "quantity.divisor", "type": "quantity", "label": "나누는 수", "value": 4},
            {"id": "quantity.quotient", "type": "quantity", "label": "몫", "value": 8},
        ],
        "relations": [
            {
                "id": "relation.division",
                "type": "quotient_of",
                "dividend": "quantity.dividend",
                "divisor": "quantity.divisor",
                "quotient": "quantity.quotient",
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
        stroke="#f59e0b",
        stroke_width=2.2,
    )

    blank_square = RectSlot(
        id="slot.diagram.blank_square",
        prompt="",
        x=330,
        y=114,
        width=54,
        height=54,
        fill="#ffffff",
        stroke="#9ca3af",
        stroke_width=2.4,
    )

    equation_rest = TextBoxSlot(
        id="slot.diagram.equation_rest",
        prompt="",
        text="÷ 4 = 8",
        x=392,
        y=112,
        width=180,
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
        blank_square,
        equation_rest,
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
