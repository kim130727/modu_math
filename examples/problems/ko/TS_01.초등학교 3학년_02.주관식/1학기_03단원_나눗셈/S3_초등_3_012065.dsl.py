"""ModuMath Problem DSL: 40 ÷ 8 계산하기 (S3_초등_3_012065)"""

from __future__ import annotations

from modu_math.dsl import (
    Canvas,
    ProblemTemplate,
    RectSlot,
    Region,
    TextBoxSlot,
)


PROBLEM_ID = "S3_초등_3_012065"
PROBLEM_TITLE = "나눗셈 계산하기 (40 ÷ 8)"


ANSWER = {
    "type": "short_answer",
    "value": 5,
    "unit": "",
    "values": [5],
    "choices": [],
    "blanks": [
        {
            "id": "slot.answer.input",
            "slot_id": "slot.answer.input",
            "expected": 5,
        },
    ],
    "answer_key": [
        {
            "slot_id": "slot.answer.input",
            "value": 5,
            "diagnostics": [
                {
                    "id": "diag.multiplication_fact_error",
                    "condition": "answer_not_equals_5",
                    "concept": "8의 단 곱셈구구",
                    "reason": "40 ÷ 8의 몫을 잘못 구함",
                    "feedback": "나누는 수 8을 보고 8의 단 곱셈구구를 떠올려 보세요. 8 × 5 = 40이므로 몫은 5입니다.",
                },
            ],
        },
    ],
}


SEMANTIC = {
    "problem_id": PROBLEM_ID,
    "problem_type": "short_answer_division_computation",
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
            {"id": "quantity.dividend", "type": "quantity", "label": "나누어지는 수", "value": 40},
            {"id": "quantity.divisor", "type": "quantity", "label": "나누는 수", "value": 8},
            {"id": "quantity.quotient", "type": "quantity", "label": "몫", "value": 5},
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
        text="나눗셈을 하세요.",
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

    expr_slot = TextBoxSlot(
        id="slot.stem.expression",
        prompt="",
        text="40 ÷ 8 =",
        x=240,
        y=114,
        width=230,
        height=60,
        font_size=36,
        font_family='"Noto Sans KR", sans-serif',
        fill="#111827",
        align="right",
        valign="middle",
    )

    answer_input = RectSlot(
        id="slot.answer.input",
        prompt="",
        x=486,
        y=114,
        width=110,
        height=60,
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
            "max_font_size": 34,
            "font_weight": 700,
            "horizontal_align": "center",
            "vertical_align": "middle",
            "padding": 6,
            "text_color": "#222222",
        },
    )

    slots = (
        stem_slot,
        expr_slot,
        answer_input,
    )

    return ProblemTemplate(
        id=PROBLEM_ID,
        title=PROBLEM_TITLE,
        canvas=Canvas(
            width=900,
            height=220,
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
