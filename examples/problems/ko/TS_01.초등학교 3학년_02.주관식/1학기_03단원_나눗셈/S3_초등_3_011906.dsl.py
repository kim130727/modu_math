"""ModuMath Problem DSL: 빈 병을 상자에 나누어 담기 (S3_초등_3_011906)"""

from __future__ import annotations

from modu_math.dsl import (
    Canvas,
    ProblemTemplate,
    RectSlot,
    Region,
    TextBoxSlot,
)


PROBLEM_ID = "S3_초등_3_011906"
PROBLEM_TITLE = "빈 병을 상자에 나누어 담기"


ANSWER = {
    "type": "short_answer",
    "value": 9,
    "unit": "상자",
    "values": [9],
    "choices": [],
    "blanks": [
        {
            "id": "slot.answer.input",
            "slot_id": "slot.answer.input",
            "expected": 9,
        },
    ],
    "answer_key": [
        {
            "slot_id": "slot.answer.input",
            "value": 9,
            "diagnostics": [
                {
                    "id": "diag.multiplication_instead_of_division",
                    "condition": "answer_equals_576",
                    "concept": "나눗셈의 의미",
                    "reason": "72를 8로 나누어야 하는데 곱셈을 함",
                    "feedback": "전체 72개를 8개씩 묶어 담는 상황이므로 나눗셈 72 ÷ 8을 계산해야 합니다.",
                },
                {
                    "id": "diag.multiplication_fact_error",
                    "condition": "answer_not_equals_9",
                    "concept": "8의 단 곱셈구구",
                    "reason": "72 ÷ 8의 몫을 잘못 구함",
                    "feedback": "8 × □ = 72가 되는 수를 8의 단 곱셈구구에서 찾아보세요.",
                },
            ],
        },
    ],
}


SEMANTIC = {
    "problem_id": PROBLEM_ID,
    "problem_type": "short_answer_division_word_problem",
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
            {"id": "quantity.total_bottles", "type": "quantity", "label": "전체 빈 병 수", "value": 72, "unit": "개"},
            {"id": "quantity.bottles_per_box", "type": "quantity", "label": "한 상자에 담는 빈 병 수", "value": 8, "unit": "개"},
            {"id": "quantity.box_count", "type": "quantity", "label": "필요한 상자 수", "value": 9, "unit": "상자"},
        ],
        "relations": [
            {
                "id": "relation.division",
                "type": "quotient_of",
                "dividend": "quantity.total_bottles",
                "divisor": "quantity.bottles_per_box",
                "quotient": "quantity.box_count",
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
        text="경수는 빈 병을 상자에 담으려고 합니다. 빈 병 72개를 한 상자에 8개씩 담는다면 몇 상자가 될까요?",
        x=32,
        y=24,
        width=836,
        height=96,
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
        x=520,
        y=154,
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
        x=552,
        y=154,
        width=120,
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
        text="상자",
        x=680,
        y=154,
        width=64,
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
        x=748,
        y=154,
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
            height=240,
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
