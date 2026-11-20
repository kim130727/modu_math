"""ModuMath Problem DSL: 참외를 바구니에 똑같이 나누어 담기 (S3_초등_3_011967)"""

from __future__ import annotations

from modu_math.dsl import (
    Canvas,
    ProblemTemplate,
    RectSlot,
    Region,
    TextBoxSlot,
)


PROBLEM_ID = "S3_초등_3_011967"
PROBLEM_TITLE = "한 바구니에 담을 참외 수 구하기"


ANSWER = {
    "type": "short_answer",
    "value": 6,
    "unit": "개",
    "values": [6],
    "choices": [],
    "blanks": [
        {
            "id": "slot.answer.input",
            "slot_id": "slot.answer.input",
            "expected": 6,
        },
    ],
    "answer_key": [
        {
            "slot_id": "slot.answer.input",
            "value": 6,
            "diagnostics": [
                {
                    "id": "diag.division_error",
                    "condition": "answer_not_equals_6",
                    "concept": "똑같이 나누기",
                    "reason": "30 ÷ 5의 계산을 잘못함",
                    "feedback": "참외 30개를 5바구니에 똑같이 나누어 담으므로 30 ÷ 5를 계산해 보세요.",
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
            {"id": "quantity.total_melons", "type": "quantity", "label": "전체 참외 수", "value": 30, "unit": "개"},
            {"id": "quantity.baskets", "type": "quantity", "label": "바구니 수", "value": 5, "unit": "바구니"},
            {"id": "quantity.melons_per_basket", "type": "quantity", "label": "한 바구니에 담는 참외 수", "value": 6, "unit": "개"},
        ],
        "relations": [
            {
                "id": "relation.division",
                "type": "quotient_of",
                "dividend": "quantity.total_melons",
                "divisor": "quantity.baskets",
                "quotient": "quantity.melons_per_basket",
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
        text="참외 30개를 바구니에 똑같이 나누어 담으려면 5바구니가 필요합니다. 한 바구니에 몇 개씩 담아야 할까요?",
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
