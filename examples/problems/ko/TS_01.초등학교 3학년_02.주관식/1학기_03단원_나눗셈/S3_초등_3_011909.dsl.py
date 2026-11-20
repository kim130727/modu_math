"""ModuMath Problem DSL: 닭과 강아지 다리 수 문제 (S3_초등_3_011909)"""

from __future__ import annotations

from modu_math.dsl import (
    Canvas,
    ProblemTemplate,
    RectSlot,
    Region,
    TextBoxSlot,
)


PROBLEM_ID = "S3_초등_3_011909"
PROBLEM_TITLE = "전체 다리 수로 닭의 수 구하기"


ANSWER = {
    "type": "short_answer",
    "value": 7,
    "unit": "마리",
    "values": [7],
    "choices": [],
    "blanks": [
        {
            "id": "slot.answer.input",
            "slot_id": "slot.answer.input",
            "expected": 7,
        },
    ],
    "answer_key": [
        {
            "slot_id": "slot.answer.input",
            "value": 7,
            "diagnostics": [
                {
                    "id": "diag.forgot_divide_by_2",
                    "condition": "answer_equals_14",
                    "concept": "닭의 다리 수로 나누기",
                    "reason": "닭의 다리 수(14개)를 닭의 마릿수로 그대로 답함",
                    "feedback": "14는 닭의 다리 수입니다. 닭 1마리의 다리는 2개이므로 14 ÷ 2를 계산해 보세요.",
                },
                {
                    "id": "diag.wrong_dog_leg_count",
                    "condition": "answer_not_equals_7",
                    "concept": "동물의 다리 수",
                    "reason": "강아지 다리 수를 잘못 계산하거나 뺄셈/나눗셈을 틀림",
                    "feedback": "강아지 4마리의 다리는 4 × 4 = 16개입니다. 전체 30개에서 16개를 뺀 뒤 2로 나누어 보세요.",
                },
            ],
        },
    ],
}


SEMANTIC = {
    "problem_id": PROBLEM_ID,
    "problem_type": "short_answer_multi_step_division_word_problem",
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
            {"id": "quantity.total_legs", "type": "quantity", "label": "전체 다리 수", "value": 30, "unit": "개"},
            {"id": "quantity.dogs", "type": "quantity", "label": "강아지 수", "value": 4, "unit": "마리"},
            {"id": "quantity.dog_legs", "type": "quantity", "label": "강아지 다리 수", "value": 16, "unit": "개"},
            {"id": "quantity.chicken_legs", "type": "quantity", "label": "닭 다리 수", "value": 14, "unit": "개"},
            {"id": "quantity.chickens", "type": "quantity", "label": "닭의 수", "value": 7, "unit": "마리"},
        ],
        "relations": [
            {
                "id": "relation.chicken_count",
                "type": "quotient_of",
                "dividend": "quantity.chicken_legs",
                "divisor": 2,
                "quotient": "quantity.chickens",
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
        text="마당에 닭과 강아지가 있습니다. 다리를 세어 보니 모두 30개였습니다. 강아지가 4마리라면 닭은 몇 마리일까요?",
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
        x=520,
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
        x=552,
        y=160,
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
        text="마리",
        x=680,
        y=160,
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
