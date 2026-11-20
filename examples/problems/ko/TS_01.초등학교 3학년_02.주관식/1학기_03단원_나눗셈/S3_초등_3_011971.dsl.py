"""ModuMath Problem DSL: 연속 나눗셈 빈칸 채우기 (S3_초등_3_011971)"""

from __future__ import annotations

from modu_math.dsl import (
    Canvas,
    CircleSlot,
    PathSlot,
    ProblemTemplate,
    RectSlot,
    Region,
    TextBoxSlot,
)


PROBLEM_ID = "S3_초등_3_011971"
PROBLEM_TITLE = "연속 나눗셈에서 ㉠, ㉡ 구하기"


ANSWER = {
    "type": "short_answer",
    "value": [8, 4],
    "unit": "",
    "values": [8, 4],
    "choices": [],
    "blanks": [
        {
            "id": "slot.answer.input_g",
            "slot_id": "slot.answer.input_g",
            "expected": 8,
        },
        {
            "id": "slot.answer.input_n",
            "slot_id": "slot.answer.input_n",
            "expected": 4,
        },
    ],
    "answer_key": [
        {
            "slot_id": "slot.answer.input_g",
            "value": 8,
            "diagnostics": [
                {
                    "id": "diag.step1_division_error",
                    "condition": "answer_not_equals_8",
                    "concept": "나눗셈 계산 (48 ÷ 6)",
                    "reason": "48 ÷ 6의 몫을 잘못 계산함",
                    "feedback": "6 × □ = 48이 되는 수를 생각해 보세요. 6 × 8 = 48이므로 ㉠은 8입니다.",
                },
            ],
        },
        {
            "slot_id": "slot.answer.input_n",
            "value": 4,
            "diagnostics": [
                {
                    "id": "diag.step2_division_error",
                    "condition": "answer_not_equals_4",
                    "concept": "연속 나눗셈 (8 ÷ 2)",
                    "reason": "㉠의 결과를 2로 나누는 계산을 잘못함",
                    "feedback": "㉠에서 구한 8을 2로 나누어 보세요. 8 ÷ 2 = 4입니다.",
                },
            ],
        },
    ],
}


SEMANTIC = {
    "problem_id": PROBLEM_ID,
    "problem_type": "short_answer_chained_division",
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
            {"id": "quantity.start", "type": "quantity", "label": "처음 수", "value": 48},
            {"id": "quantity.g", "type": "quantity", "label": "㉠", "value": 8},
            {"id": "quantity.n", "type": "quantity", "label": "㉡", "value": 4},
        ],
        "relations": [
            {
                "id": "relation.step1",
                "type": "quotient_of",
                "dividend": "quantity.start",
                "divisor": 6,
                "quotient": "quantity.g",
            },
            {
                "id": "relation.step2",
                "type": "quotient_of",
                "dividend": "quantity.g",
                "divisor": 2,
                "quotient": "quantity.n",
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
        text="㉠, ㉡에 알맞은 수를 각각 구하세요.",
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

    arc_1 = PathSlot(
        id="slot.diagram.arc_1",
        prompt="",
        d="M 185 162 Q 315 80 445 162",
        fill="none",
        stroke="#ec4899",
        stroke_width=2.0,
    )
    arc_2 = PathSlot(
        id="slot.diagram.arc_2",
        prompt="",
        d="M 455 162 Q 585 80 715 162",
        fill="none",
        stroke="#ec4899",
        stroke_width=2.0,
    )

    op_1_bg = CircleSlot(
        id="slot.diagram.op_1_bg",
        prompt="",
        cx=315,
        cy=114,
        r=30.0,
        fill="#fda4af",
        stroke="#f43f5e",
        stroke_width=1.4,
    )
    op_1_text = TextBoxSlot(
        id="slot.diagram.op_1_text",
        prompt="",
        text="÷6",
        x=280,
        y=92,
        width=70,
        height=44,
        font_size=26,
        font_family='"Noto Sans KR", sans-serif',
        fill="#111827",
        align="center",
        valign="middle",
    )

    op_2_bg = CircleSlot(
        id="slot.diagram.op_2_bg",
        prompt="",
        cx=585,
        cy=114,
        r=30.0,
        fill="#fda4af",
        stroke="#f43f5e",
        stroke_width=1.4,
    )
    op_2_text = TextBoxSlot(
        id="slot.diagram.op_2_text",
        prompt="",
        text="÷2",
        x=550,
        y=92,
        width=70,
        height=44,
        font_size=26,
        font_family='"Noto Sans KR", sans-serif',
        fill="#111827",
        align="center",
        valign="middle",
    )

    box_start = RectSlot(
        id="slot.diagram.box_start",
        prompt="",
        x=115,
        y=166,
        width=140,
        height=64,
        fill="#ffffff",
        stroke="#9ca3af",
        stroke_width=2.5,
    )
    text_start = TextBoxSlot(
        id="slot.diagram.text_start",
        prompt="",
        text="48",
        x=115,
        y=166,
        width=140,
        height=64,
        font_size=30,
        font_family='"Noto Sans KR", sans-serif',
        fill="#111827",
        align="center",
        valign="middle",
    )

    box_g = RectSlot(
        id="slot.diagram.box_g",
        prompt="",
        x=380,
        y=166,
        width=140,
        height=64,
        fill="#ffffff",
        stroke="#9ca3af",
        stroke_width=2.5,
    )
    text_g = TextBoxSlot(
        id="slot.diagram.text_g",
        prompt="",
        text="㉠",
        x=380,
        y=166,
        width=140,
        height=64,
        font_size=28,
        font_family='"Noto Sans KR", sans-serif',
        fill="#111827",
        align="center",
        valign="middle",
    )

    box_n = RectSlot(
        id="slot.diagram.box_n",
        prompt="",
        x=645,
        y=166,
        width=140,
        height=64,
        fill="#ffffff",
        stroke="#9ca3af",
        stroke_width=2.5,
    )
    text_n = TextBoxSlot(
        id="slot.diagram.text_n",
        prompt="",
        text="㉡",
        x=645,
        y=166,
        width=140,
        height=64,
        font_size=28,
        font_family='"Noto Sans KR", sans-serif',
        fill="#111827",
        align="center",
        valign="middle",
    )

    ans_g_label = TextBoxSlot(
        id="slot.answer.label_g",
        prompt="",
        text="㉠ (",
        x=470,
        y=266,
        width=68,
        height=50,
        font_size=25,
        font_family='"Noto Sans KR", sans-serif',
        fill="#202124",
        align="right",
        valign="middle",
    )
    ans_g_input = RectSlot(
        id="slot.answer.input_g",
        prompt="",
        x=544,
        y=266,
        width=180,
        height=50,
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
            "max_font_size": 26,
            "font_weight": 700,
            "horizontal_align": "center",
            "vertical_align": "middle",
            "padding": 6,
            "text_color": "#222222",
        },
    )
    ans_g_paren = TextBoxSlot(
        id="slot.answer.paren_g",
        prompt="",
        text=")",
        x=730,
        y=266,
        width=26,
        height=50,
        font_size=25,
        font_family='"Noto Sans KR", sans-serif',
        fill="#202124",
        align="center",
        valign="middle",
    )

    ans_n_label = TextBoxSlot(
        id="slot.answer.label_n",
        prompt="",
        text="㉡ (",
        x=470,
        y=332,
        width=68,
        height=50,
        font_size=25,
        font_family='"Noto Sans KR", sans-serif',
        fill="#202124",
        align="right",
        valign="middle",
    )
    ans_n_input = RectSlot(
        id="slot.answer.input_n",
        prompt="",
        x=544,
        y=332,
        width=180,
        height=50,
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
            "max_font_size": 26,
            "font_weight": 700,
            "horizontal_align": "center",
            "vertical_align": "middle",
            "padding": 6,
            "text_color": "#222222",
        },
    )
    ans_n_paren = TextBoxSlot(
        id="slot.answer.paren_n",
        prompt="",
        text=")",
        x=730,
        y=332,
        width=26,
        height=50,
        font_size=25,
        font_family='"Noto Sans KR", sans-serif',
        fill="#202124",
        align="center",
        valign="middle",
    )

    slots = (
        stem_slot,
        arc_1,
        arc_2,
        op_1_bg,
        op_1_text,
        op_2_bg,
        op_2_text,
        box_start,
        text_start,
        box_g,
        text_g,
        box_n,
        text_n,
        ans_g_label,
        ans_g_input,
        ans_g_paren,
        ans_n_label,
        ans_n_input,
        ans_n_paren,
    )

    return ProblemTemplate(
        id=PROBLEM_ID,
        title=PROBLEM_TITLE,
        canvas=Canvas(
            width=900,
            height=410,
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
