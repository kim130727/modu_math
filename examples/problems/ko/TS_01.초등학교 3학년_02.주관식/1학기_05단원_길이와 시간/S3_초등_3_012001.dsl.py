"""ModuMath Problem DSL: 자 눈금 길이(8 mm) 쓰고 읽기 (S3_초등_3_012001)"""

from __future__ import annotations

from modu_math.dsl import (
    Canvas,
    LineSlot,
    PathSlot,
    ProblemTemplate,
    RectSlot,
    Region,
    TextBoxSlot,
)


PROBLEM_ID = "S3_초등_3_012001"
PROBLEM_TITLE = "밀리미터(mm) 길이 쓰고 읽기"


ANSWER = {
    "type": "short_answer",
    "value": ["8 mm", "8 밀리미터"],
    "unit": "",
    "values": ["8 mm", "8 밀리미터"],
    "choices": [],
    "blanks": [
        {
            "id": "slot.answer.input_write",
            "slot_id": "slot.answer.input_write",
            "expected": "8 mm",
        },
        {
            "id": "slot.answer.input_read",
            "slot_id": "slot.answer.input_read",
            "expected": "8 밀리미터",
        },
    ],
    "answer_key": [
        {
            "slot_id": "slot.answer.input_write",
            "value": "8 mm",
            "diagnostics": [
                {
                    "id": "diag.ruler_tick_count_error",
                    "condition": "answer_not_equals_8mm",
                    "concept": "밀리미터(mm) 읽기",
                    "reason": "0에서부터 작은 눈금 칸 수를 잘못 셈",
                    "feedback": "눈금 0에서부터 작은 눈금이 몇 칸인지 세어 보세요. 8칸이므로 8 mm입니다.",
                },
            ],
        },
        {
            "slot_id": "slot.answer.input_read",
            "value": "8 밀리미터",
            "diagnostics": [
                {
                    "id": "diag.unit_reading_error",
                    "condition": "answer_not_equals_8_millimeter",
                    "concept": "밀리미터(mm) 읽기",
                    "reason": "mm 단위를 한글로 '밀리미터'라고 읽지 못함",
                    "feedback": "기호 mm는 '밀리미터'라고 읽습니다. 따라서 '8 밀리미터'입니다.",
                },
            ],
        },
    ],
}


SEMANTIC = {
    "problem_id": PROBLEM_ID,
    "problem_type": "short_answer_length_unit_write_and_read",
    "metadata": {
        "school": "초등학교",
        "grade": 3,
        "semester": 1,
        "chapter": "05단원_길이와 시간",
        "subject": "수학",
        "language": "ko-KR",
    },
    "domain": {
        "objects": [
            {"id": "quantity.length", "type": "quantity", "label": "측정한 길이", "value": 8, "unit": "mm"},
        ],
        "relations": [
            {
                "id": "relation.unit_reading",
                "type": "written_and_read_as",
                "from_id": "quantity.length",
                "written": "8 mm",
                "read": "8 밀리미터",
            },
        ],
    },
    "answer": ANSWER,
}

SEMANTIC_OVERRIDE = SEMANTIC


def _ruler_slots() -> list[object]:
    # 0은 x=330, 1 cm = 100px (1mm = 10px), 막대 끝 x=410 (8mm)
    slots: list[object] = [
        RectSlot(
            id="slot.diagram.bar",
            prompt="",
            x=330,
            y=102,
            width=80,
            height=40,
            fill="#dbeafe",
            stroke="#93c5fd",
            stroke_width=1.2,
        ),
        PathSlot(
            id="slot.diagram.ruler_body",
            prompt="",
            d="M 310 142 L 475 142 Q 485 154 470 168 Q 455 182 475 196 Q 485 210 468 224 L 485 234 L 310 234 Z",
            fill="#ffffff",
            stroke="#111827",
            stroke_width=1.6,
        ),
    ]
    for mm in range(13):
        tx = 330 + mm * 10
        if mm in (0, 10):
            tick_len = 24
        elif mm == 5:
            tick_len = 18
        else:
            tick_len = 12
        slots.append(
            LineSlot(
                id=f"slot.diagram.ruler_tick_{mm}",
                prompt="",
                x1=tx,
                y1=142,
                x2=tx,
                y2=142 + tick_len,
                stroke="#111827",
                stroke_width=1.6 if mm in (0, 10) else 1.2,
            )
        )
    slots.extend(
        [
            TextBoxSlot(
                id="slot.diagram.ruler_num_0",
                prompt="",
                text="0",
                x=316,
                y=170,
                width=28,
                height=30,
                font_size=22,
                font_family='"Noto Sans KR", sans-serif',
                fill="#111827",
                align="center",
                valign="middle",
            ),
            TextBoxSlot(
                id="slot.diagram.ruler_num_1",
                prompt="",
                text="1",
                x=416,
                y=170,
                width=28,
                height=30,
                font_size=22,
                font_family='"Noto Sans KR", sans-serif',
                fill="#111827",
                align="center",
                valign="middle",
            ),
        ]
    )
    return slots


def build_problem_template() -> ProblemTemplate:
    stem_slot = TextBoxSlot(
        id="slot.stem.question",
        prompt="",
        text="그림에서 나타내는 길이를 쓰고 읽어 보세요.",
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

    diagram_slots = _ruler_slots()

    write_badge = RectSlot(
        id="slot.answer.write_badge",
        prompt="",
        x=110,
        y=270,
        width=90,
        height=44,
        fill="#7dd3fc",
        stroke="#7dd3fc",
        stroke_width=1.0,
    )
    write_badge_text = TextBoxSlot(
        id="slot.answer.write_badge_text",
        prompt="",
        text="쓰기",
        x=110,
        y=270,
        width=90,
        height=44,
        font_size=22,
        font_family='"Noto Sans KR", sans-serif',
        fill="#ffffff",
        align="center",
        valign="middle",
    )
    write_paren_l = TextBoxSlot(
        id="slot.answer.write_paren_l",
        prompt="",
        text="(",
        x=212,
        y=266,
        width=26,
        height=52,
        font_size=26,
        font_family='"Noto Sans KR", sans-serif',
        fill="#202124",
        align="center",
        valign="middle",
    )
    write_input = RectSlot(
        id="slot.answer.input_write",
        prompt="",
        x=244,
        y=266,
        width=270,
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
            "padding": 6,
            "text_color": "#222222",
        },
    )
    write_paren_r = TextBoxSlot(
        id="slot.answer.write_paren_r",
        prompt="",
        text=")",
        x=520,
        y=266,
        width=26,
        height=52,
        font_size=26,
        font_family='"Noto Sans KR", sans-serif',
        fill="#202124",
        align="center",
        valign="middle",
    )

    read_badge = RectSlot(
        id="slot.answer.read_badge",
        prompt="",
        x=110,
        y=336,
        width=90,
        height=44,
        fill="#fdba74",
        stroke="#fdba74",
        stroke_width=1.0,
    )
    read_badge_text = TextBoxSlot(
        id="slot.answer.read_badge_text",
        prompt="",
        text="읽기",
        x=110,
        y=336,
        width=90,
        height=44,
        font_size=22,
        font_family='"Noto Sans KR", sans-serif',
        fill="#ffffff",
        align="center",
        valign="middle",
    )
    read_paren_l = TextBoxSlot(
        id="slot.answer.read_paren_l",
        prompt="",
        text="(",
        x=212,
        y=332,
        width=26,
        height=52,
        font_size=26,
        font_family='"Noto Sans KR", sans-serif',
        fill="#202124",
        align="center",
        valign="middle",
    )
    read_input = RectSlot(
        id="slot.answer.input_read",
        prompt="",
        x=244,
        y=332,
        width=270,
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
            "order": 1,
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
            "padding": 6,
            "text_color": "#222222",
        },
    )
    read_paren_r = TextBoxSlot(
        id="slot.answer.read_paren_r",
        prompt="",
        text=")",
        x=520,
        y=332,
        width=26,
        height=52,
        font_size=26,
        font_family='"Noto Sans KR", sans-serif',
        fill="#202124",
        align="center",
        valign="middle",
    )

    slots = (
        stem_slot,
        sub_label,
        *diagram_slots,
        write_badge,
        write_badge_text,
        write_paren_l,
        write_input,
        write_paren_r,
        read_badge,
        read_badge_text,
        read_paren_l,
        read_input,
        read_paren_r,
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
