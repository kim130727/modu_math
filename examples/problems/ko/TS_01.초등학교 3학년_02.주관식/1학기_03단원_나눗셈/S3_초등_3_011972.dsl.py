"""ModuMath Problem DSL: 공책 36권을 4권씩 나누어 주기 (S3_초등_3_011972)"""

from __future__ import annotations

from modu_math.dsl import (
    Canvas,
    ProblemTemplate,
    RectSlot,
    Region,
    TextBoxSlot,
)


PROBLEM_ID = "S3_초등_3_011972"
PROBLEM_TITLE = "공책 나누어 주기 식 쓰고 답 구하기"


ANSWER = {
    "type": "short_answer",
    "value": ["36 ÷ 4 = 9", 9],
    "unit": "명",
    "values": ["36 ÷ 4 = 9", 9],
    "choices": [],
    "blanks": [
        {
            "id": "slot.answer.input_expr",
            "slot_id": "slot.answer.input_expr",
            "expected": "36 ÷ 4 = 9",
        },
        {
            "id": "slot.answer.input_ans",
            "slot_id": "slot.answer.input_ans",
            "expected": 9,
        },
    ],
    "answer_key": [
        {
            "slot_id": "slot.answer.input_expr",
            "value": "36 ÷ 4 = 9",
            "diagnostics": [
                {
                    "id": "diag.wrong_expression",
                    "condition": "answer_not_equals_36_div_4_eq_9",
                    "concept": "나눗셈식 세우기",
                    "reason": "전체 36권을 4권씩 나누는 식을 올바르게 세우지 못함",
                    "feedback": "공책 36권을 한 명에게 4권씩 나누어 주므로 식은 36 ÷ 4 = 9입니다.",
                },
            ],
        },
        {
            "slot_id": "slot.answer.input_ans",
            "value": 9,
            "diagnostics": [
                {
                    "id": "diag.division_error",
                    "condition": "answer_not_equals_9",
                    "concept": "4의 단 곱셈구구",
                    "reason": "36 ÷ 4의 몫을 잘못 구함",
                    "feedback": "4 × □ = 36이 되는 수를 생각해 보세요. 4 × 9 = 36이므로 9명에게 나누어 줄 수 있습니다.",
                },
            ],
        },
    ],
}


SEMANTIC = {
    "problem_id": PROBLEM_ID,
    "problem_type": "short_answer_division_equation_and_answer",
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
            {"id": "quantity.total_notebooks", "type": "quantity", "label": "전체 공책 수", "value": 36, "unit": "권"},
            {"id": "quantity.per_person", "type": "quantity", "label": "한 명에게 주는 공책 수", "value": 4, "unit": "권"},
            {"id": "quantity.people", "type": "quantity", "label": "나누어 줄 수 있는 사람 수", "value": 9, "unit": "명"},
        ],
        "relations": [
            {
                "id": "relation.division",
                "type": "quotient_of",
                "dividend": "quantity.total_notebooks",
                "divisor": "quantity.per_person",
                "quotient": "quantity.people",
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
        text="공책이 36권 있습니다. 한 명에게 4권씩 나누어 주려고 합니다. 몇 명에게 나누어 줄 수 있는지 식을 쓰고, 답을 구하세요.",
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

    expr_label = TextBoxSlot(
        id="slot.answer.expr_label",
        prompt="",
        text="식 :",
        x=180,
        y=164,
        width=60,
        height=52,
        font_size=26,
        font_family='"Noto Sans KR", sans-serif',
        fill="#202124",
        align="right",
        valign="middle",
    )

    expr_input = RectSlot(
        id="slot.answer.input_expr",
        prompt="",
        x=252,
        y=164,
        width=360,
        height=52,
        fill="#ffffff",
        stroke="#111827",
        stroke_width=1.4,
        interaction={
            "type": "input",
            "role": "answer",
            "value_type": "text",
            "max_length": 20,
            "include_in_submission": True,
            "order": 0,
            "group_id": "final_answer",
            "auto_advance": False,
            "keyboard": "text",
        },
        input_style={
            "font_size_mode": "auto",
            "font_size_adjust": 0,
            "min_font_size": 16,
            "max_font_size": 26,
            "font_weight": 700,
            "horizontal_align": "center",
            "vertical_align": "middle",
            "padding": 6,
            "text_color": "#222222",
        },
    )

    ans_label = TextBoxSlot(
        id="slot.answer.ans_label",
        prompt="",
        text="답 :",
        x=180,
        y=236,
        width=60,
        height=52,
        font_size=26,
        font_family='"Noto Sans KR", sans-serif',
        fill="#202124",
        align="right",
        valign="middle",
    )

    ans_input = RectSlot(
        id="slot.answer.input_ans",
        prompt="",
        x=252,
        y=236,
        width=130,
        height=52,
        fill="#ffffff",
        stroke="#111827",
        stroke_width=1.4,
        interaction={
            "type": "input",
            "role": "answer",
            "value_type": "integer",
            "max_length": 3,
            "include_in_submission": True,
            "order": 1,
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
        text="명",
        x=392,
        y=236,
        width=40,
        height=52,
        font_size=26,
        font_family='"Noto Sans KR", sans-serif',
        fill="#202124",
        align="left",
        valign="middle",
    )

    slots = (
        stem_slot,
        expr_label,
        expr_input,
        ans_label,
        ans_input,
        unit_slot,
    )

    return ProblemTemplate(
        id=PROBLEM_ID,
        title=PROBLEM_TITLE,
        canvas=Canvas(
            width=900,
            height=320,
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
