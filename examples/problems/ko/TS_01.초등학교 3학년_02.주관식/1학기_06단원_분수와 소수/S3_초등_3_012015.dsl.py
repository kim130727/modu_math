"""ModuMath Problem DSL: 색칠한 부분을 분수로 쓰고 읽기 (3/8) (S3_초등_3_012015)"""

from __future__ import annotations

from modu_math.dsl import (
    Canvas,
    LineSlot,
    PolygonSlot,
    ProblemTemplate,
    RectSlot,
    Region,
    TextBoxSlot,
)


PROBLEM_ID = "S3_초등_3_012015"
PROBLEM_TITLE = "색칠한 부분을 분수로 쓰고 읽기 (3/8)"


ANSWER = {
    "type": "short_answer",
    "value": ["3/8", "8분의 3"],
    "unit": "",
    "values": ["3/8", "8분의 3"],
    "choices": [],
    "blanks": [
        {
            "id": "slot.answer.input_write",
            "slot_id": "slot.answer.input_write",
            "expected": "3/8",
        },
        {
            "id": "slot.answer.input_read",
            "slot_id": "slot.answer.input_read",
            "expected": "8분의 3",
        },
    ],
    "answer_key": [
        {
            "slot_id": "slot.answer.input_write",
            "value": "3/8",
            "diagnostics": [
                {
                    "id": "diag.swapped_numerator_denominator",
                    "condition": "answer_equals_8_over_3",
                    "concept": "분모와 분자",
                    "reason": "분모와 분자의 위치를 바꾸어 씀",
                    "feedback": "전체 8조각 중 3조각을 색칠했으므로 전체(8)를 분모에, 부분(3)을 분자에 써서 3/8으로 나타냅니다.",
                },
            ],
        },
        {
            "slot_id": "slot.answer.input_read",
            "value": "8분의 3",
            "diagnostics": [
                {
                    "id": "diag.fraction_reading_order_error",
                    "condition": "answer_equals_3_over_8_read",
                    "concept": "분수 읽기",
                    "reason": "분자부터 읽어 '3분의 8'이라고 답함",
                    "feedback": "분수는 분모부터 읽습니다. 3/8은 '8분의 3'이라고 읽습니다.",
                },
            ],
        },
    ],
}


SEMANTIC = {
    "problem_id": PROBLEM_ID,
    "problem_type": "short_answer_fraction_write_and_read",
    "metadata": {
        "school": "초등학교",
        "grade": 3,
        "semester": 1,
        "chapter": "06단원_분수와 소수",
        "subject": "수학",
        "language": "ko-KR",
    },
    "domain": {
        "objects": [
            {"id": "figure.cross", "type": "fraction_model", "label": "8등분된 도형", "total_parts": 8, "shaded_parts": 3},
        ],
        "relations": [
            {
                "id": "relation.fraction_value",
                "type": "represents_fraction",
                "from_id": "figure.cross",
                "written": "3/8",
                "read": "8분의 3",
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
        text="색칠한 부분을 분수로 쓰고, 읽어 보세요.",
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

    sub_label = TextBoxSlot(
        id="slot.stem.sublabel",
        prompt="",
        text="(1)",
        x=48,
        y=96,
        width=50,
        height=40,
        font_size=26,
        font_family='"Noto Sans KR", sans-serif',
        fill="#202124",
        align="left",
        valign="middle",
    )

    # 십자 도형 (중심 450, 180) 8조각 중 3조각 색칠
    cross_bg = PolygonSlot(
        id="slot.diagram.cross_bg",
        prompt="",
        points=(
            (415, 95), (485, 95), (485, 145), (535, 145),
            (535, 215), (485, 215), (485, 265), (415, 265),
            (415, 215), (365, 215), (365, 145), (415, 145),
        ),
        fill="#ffffff",
        stroke="#a855f7",
        stroke_width=1.8,
    )
    shade_1 = PolygonSlot(
        id="slot.diagram.shade_1",
        prompt="",
        points=((450, 95), (485, 95), (485, 145), (450, 180)),
        fill="#f3e8ff",
        stroke="#a855f7",
        stroke_width=1.0,
    )
    shade_2 = PolygonSlot(
        id="slot.diagram.shade_2",
        prompt="",
        points=((365, 145), (415, 145), (450, 180), (365, 180)),
        fill="#f3e8ff",
        stroke="#a855f7",
        stroke_width=1.0,
    )
    shade_3 = PolygonSlot(
        id="slot.diagram.shade_3",
        prompt="",
        points=((450, 180), (535, 180), (535, 215), (485, 215)),
        fill="#f3e8ff",
        stroke="#a855f7",
        stroke_width=1.0,
    )
    div_v = LineSlot(id="slot.diagram.div_v", prompt="", x1=450, y1=95, x2=450, y2=265, stroke="#a855f7", stroke_width=1.2, stroke_dasharray="3 3")
    div_h = LineSlot(id="slot.diagram.div_h", prompt="", x1=365, y1=180, x2=535, y2=180, stroke="#a855f7", stroke_width=1.2, stroke_dasharray="3 3")
    div_d1 = LineSlot(id="slot.diagram.div_d1", prompt="", x1=415, y1=145, x2=485, y2=215, stroke="#a855f7", stroke_width=1.2, stroke_dasharray="3 3")
    div_d2 = LineSlot(id="slot.diagram.div_d2", prompt="", x1=485, y1=145, x2=415, y2=215, stroke="#a855f7", stroke_width=1.2, stroke_dasharray="3 3")

    write_lbl = TextBoxSlot(
        id="slot.answer.write_lbl",
        prompt="",
        text="쓰기 (",
        x=90,
        y=302,
        width=82,
        height=52,
        font_size=26,
        font_family='"Noto Sans KR", sans-serif',
        fill="#202124",
        align="right",
        valign="middle",
    )
    write_input = RectSlot(
        id="slot.answer.input_write",
        prompt="",
        x=180,
        y=302,
        width=180,
        height=52,
        fill="#ffffff",
        stroke="#111827",
        stroke_width=1.4,
        interaction={
            "type": "input",
            "role": "answer",
            "value_type": "text",
            "max_length": 10,
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
    write_paren_r = TextBoxSlot(
        id="slot.answer.write_paren_r",
        prompt="",
        text="),",
        x=366,
        y=302,
        width=36,
        height=52,
        font_size=26,
        font_family='"Noto Sans KR", sans-serif',
        fill="#202124",
        align="left",
        valign="middle",
    )

    read_lbl = TextBoxSlot(
        id="slot.answer.read_lbl",
        prompt="",
        text="읽기 (",
        x=430,
        y=302,
        width=82,
        height=52,
        font_size=26,
        font_family='"Noto Sans KR", sans-serif',
        fill="#202124",
        align="right",
        valign="middle",
    )
    read_input = RectSlot(
        id="slot.answer.input_read",
        prompt="",
        x=520,
        y=302,
        width=220,
        height=52,
        fill="#ffffff",
        stroke="#111827",
        stroke_width=1.4,
        interaction={
            "type": "input",
            "role": "answer",
            "value_type": "text",
            "max_length": 15,
            "include_in_submission": True,
            "order": 1,
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
    read_paren_r = TextBoxSlot(
        id="slot.answer.read_paren_r",
        prompt="",
        text=")",
        x=746,
        y=302,
        width=26,
        height=52,
        font_size=26,
        font_family='"Noto Sans KR", sans-serif',
        fill="#202124",
        align="left",
        valign="middle",
    )

    slots = (
        stem_slot,
        sub_label,
        cross_bg,
        shade_1,
        shade_2,
        shade_3,
        div_v,
        div_h,
        div_d1,
        div_d2,
        write_lbl,
        write_input,
        write_paren_r,
        read_lbl,
        read_input,
        read_paren_r,
    )

    return ProblemTemplate(
        id=PROBLEM_ID,
        title=PROBLEM_TITLE,
        canvas=Canvas(
            width=900,
            height=384,
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
