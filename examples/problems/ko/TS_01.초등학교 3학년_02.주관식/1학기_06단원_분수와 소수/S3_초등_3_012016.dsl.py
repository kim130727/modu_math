"""ModuMath Problem DSL: 색칠한 부분을 분수로 쓰고 읽기 (6/10) (S3_초등_3_012016)"""

from __future__ import annotations

from modu_math.dsl import (
    Canvas,
    ProblemTemplate,
    RectSlot,
    Region,
    TextBoxSlot,
)


PROBLEM_ID = "S3_초등_3_012016"
PROBLEM_TITLE = "색칠한 부분을 분수로 쓰고 읽기 (6/10)"


ANSWER = {
    "type": "short_answer",
    "value": ["6/10", "10분의 6"],
    "unit": "",
    "values": ["6/10", "10분의 6"],
    "choices": [],
    "blanks": [
        {
            "id": "slot.answer.input_write",
            "slot_id": "slot.answer.input_write",
            "expected": "6/10",
        },
        {
            "id": "slot.answer.input_read",
            "slot_id": "slot.answer.input_read",
            "expected": "10분의 6",
        },
    ],
    "answer_key": [
        {
            "slot_id": "slot.answer.input_write",
            "value": "6/10",
            "diagnostics": [
                {
                    "id": "diag.swapped_numerator_denominator",
                    "condition": "answer_equals_10_over_6",
                    "concept": "분모와 분자",
                    "reason": "분모와 분자의 위치를 바꾸어 씀",
                    "feedback": "전체 10칸 중 6칸을 색칠했으므로 전체(10)를 분모에, 부분(6)을 분자에 써서 6/10으로 나타냅니다.",
                },
            ],
        },
        {
            "slot_id": "slot.answer.input_read",
            "value": "10분의 6",
            "diagnostics": [
                {
                    "id": "diag.fraction_reading_order_error",
                    "condition": "answer_equals_6_over_10_read",
                    "concept": "분수 읽기",
                    "reason": "분자부터 읽어 '6분의 10'이라고 답함",
                    "feedback": "분수는 분모부터 읽습니다. 6/10은 '10분의 6'이라고 읽습니다.",
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
            {"id": "figure.grid", "type": "fraction_model", "label": "10등분된 도형", "total_parts": 10, "shaded_parts": 6},
        ],
        "relations": [
            {
                "id": "relation.fraction_value",
                "type": "represents_fraction",
                "from_id": "figure.grid",
                "written": "6/10",
                "read": "10분의 6",
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
        text="(2)",
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

    # 10칸 도형: (row, col, shaded)
    cells = [
        (0, 1, True), (0, 2, False), (0, 3, False),
        (1, 0, True), (1, 1, False), (1, 2, True), (1, 3, False), (1, 4, True),
        (2, 1, True), (2, 3, True),
    ]
    cell_slots: list[RectSlot] = []
    for row, col, shaded in cells:
        cell_slots.append(
            RectSlot(
                id=f"slot.diagram.cell_{row}_{col}",
                prompt="",
                x=325 + col * 50,
                y=104 + row * 50,
                width=50,
                height=50,
                fill="#e7d8cf" if shaded else "#ffffff",
                stroke="#7f1d1d",
                stroke_width=1.4,
            )
        )

    write_lbl = TextBoxSlot(
        id="slot.answer.write_lbl",
        prompt="",
        text="쓰기 (",
        x=90,
        y=292,
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
        y=292,
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
        y=292,
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
        y=292,
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
        y=292,
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
        y=292,
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
        *cell_slots,
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
            height=374,
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
