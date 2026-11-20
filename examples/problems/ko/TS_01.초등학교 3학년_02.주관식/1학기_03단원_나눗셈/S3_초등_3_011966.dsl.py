"""ModuMath Problem DSL: 나눗셈식 읽기 (S3_초등_3_011966)"""

from __future__ import annotations

from modu_math.dsl import (
    Canvas,
    ProblemTemplate,
    RectSlot,
    Region,
    TextBoxSlot,
)


PROBLEM_ID = "S3_초등_3_011966"
PROBLEM_TITLE = "나눗셈식 읽기"


ANSWER = {
    "type": "short_answer",
    "value": "14 나누기 2는 7과 같습니다.",
    "unit": "",
    "values": ["14 나누기 2는 7과 같습니다.", "14 나누기 2는 7과 같습니다"],
    "choices": [],
    "blanks": [
        {
            "id": "slot.answer.input",
            "slot_id": "slot.answer.input",
            "expected": "14 나누기 2는 7과 같습니다.",
        },
    ],
    "answer_key": [
        {
            "slot_id": "slot.answer.input",
            "value": "14 나누기 2는 7과 같습니다.",
            "diagnostics": [
                {
                    "id": "diag.wrong_symbol_reading",
                    "condition": "answer_missing_nanugi",
                    "concept": "나눗셈식 읽기",
                    "reason": "÷ 기호를 '나누기'로 읽지 않음",
                    "feedback": "기호 ÷는 '나누기'라고 읽습니다. '14 나누기 2는 7과 같습니다.' 형태로 써 보세요.",
                },
            ],
        },
    ],
}


SEMANTIC = {
    "problem_id": PROBLEM_ID,
    "problem_type": "short_answer_division_equation_reading",
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
            {"id": "equation.div", "type": "equation", "label": "14 ÷ 2 = 7", "dividend": 14, "divisor": 2, "quotient": 7},
        ],
        "relations": [
            {
                "id": "relation.reading",
                "type": "verbal_reading_of",
                "from_id": "equation.div",
                "to_id": "concept.division_reading",
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
        text="나눗셈식을 읽어 보세요.",
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
        x=210,
        y=92,
        width=480,
        height=92,
        fill="#ffffff",
        stroke="#a799c8",
        stroke_width=2.2,
    )

    equation_text = TextBoxSlot(
        id="slot.diagram.equation_text",
        prompt="",
        text="14 ÷ 2 = 7",
        x=220,
        y=102,
        width=460,
        height=72,
        font_size=36,
        font_family='"Noto Sans KR", sans-serif',
        fill="#111827",
        align="center",
        valign="middle",
    )

    paren_left = TextBoxSlot(
        id="slot.answer.paren_left",
        prompt="",
        text="(",
        x=180,
        y=214,
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
        x=214,
        y=214,
        width=550,
        height=54,
        fill="#ffffff",
        stroke="#111827",
        stroke_width=1.4,
        interaction={
            "type": "input",
            "role": "answer",
            "value_type": "text",
            "max_length": 40,
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
            "max_font_size": 24,
            "font_weight": 700,
            "horizontal_align": "center",
            "vertical_align": "middle",
            "padding": 8,
            "text_color": "#222222",
        },
    )

    paren_right = TextBoxSlot(
        id="slot.answer.paren_right",
        prompt="",
        text=")",
        x=770,
        y=214,
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
        equation_text,
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
