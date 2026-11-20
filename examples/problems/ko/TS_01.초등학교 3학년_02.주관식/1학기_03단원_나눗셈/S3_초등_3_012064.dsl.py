"""ModuMath Problem DSL: 24 ÷ 3 계산하기 (S3_초등_3_012064)"""

from __future__ import annotations

from modu_math.dsl import (
    Canvas,
    ProblemTemplate,
    RectSlot,
    Region,
    TextBoxSlot,
)


PROBLEM_ID = "S3_초등_3_012064"
PROBLEM_TITLE = "나눗셈 계산하기 (24 ÷ 3)"


ANSWER = {
    "type": "short_answer",
    "value": 8,
    "unit": "",
    "values": [8],
    "choices": [],
    "blanks": [
        {
            "id": "slot.answer.input",
            "slot_id": "slot.answer.input",
            "expected": 8,
        },
    ],
    "answer_key": [
        {
            "slot_id": "slot.answer.input",
            "value": 8,
            "diagnostics": [
                {
                    "id": "diag.multiplication_fact_error",
                    "condition": "answer_not_equals_8",
                    "concept": "3의 단 곱셈구구",
                    "reason": "24 ÷ 3의 몫을 잘못 구함",
                    "feedback": "나누는 수 3을 보고 3의 단 곱셈구구를 떠올려 보세요. 3 × 8 = 24이므로 몫은 8입니다.",
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
            {"id": "quantity.dividend", "type": "quantity", "label": "나누어지는 수", "value": 24},
            {"id": "quantity.divisor", "type": "quantity", "label": "나누는 수", "value": 3},
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
        text="24 ÷ 3 =",
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
