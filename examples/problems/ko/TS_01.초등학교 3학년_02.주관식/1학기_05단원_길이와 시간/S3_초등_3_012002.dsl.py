"""ModuMath Problem DSL: 길이(2 km) 쓰고 읽기 (S3_초등_3_012002)"""

from __future__ import annotations

from modu_math.dsl import (
    Canvas,
    CircleSlot,
    LineSlot,
    PathSlot,
    ProblemTemplate,
    RectSlot,
    Region,
    TextBoxSlot,
)


PROBLEM_ID = "S3_초등_3_012002"
PROBLEM_TITLE = "킬로미터(km) 길이 쓰고 읽기"


ANSWER = {
    "type": "short_answer",
    "value": ["2 km", "2 킬로미터"],
    "unit": "",
    "values": ["2 km", "2 킬로미터"],
    "choices": [],
    "blanks": [
        {
            "id": "slot.answer.input_write",
            "slot_id": "slot.answer.input_write",
            "expected": "2 km",
        },
        {
            "id": "slot.answer.input_read",
            "slot_id": "slot.answer.input_read",
            "expected": "2 킬로미터",
        },
    ],
    "answer_key": [
        {
            "slot_id": "slot.answer.input_write",
            "value": "2 km",
            "diagnostics": [
                {
                    "id": "diag.km_sum_error",
                    "condition": "answer_not_equals_2km",
                    "concept": "킬로미터(km) 쓰기",
                    "reason": "1 km가 2번 이어진 전체 길이를 잘못 구함",
                    "feedback": "1 km가 2번 이어져 있으므로 전체 길이는 2 km입니다.",
                },
            ],
        },
        {
            "slot_id": "slot.answer.input_read",
            "value": "2 킬로미터",
            "diagnostics": [
                {
                    "id": "diag.unit_reading_error",
                    "condition": "answer_not_equals_2_kilometer",
                    "concept": "킬로미터(km) 읽기",
                    "reason": "km 단위를 한글로 '킬로미터'라고 읽지 못함",
                    "feedback": "기호 km는 '킬로미터'라고 읽습니다. 따라서 '2 킬로미터'입니다.",
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
            {"id": "quantity.length", "type": "quantity", "label": "전체 길이", "value": 2, "unit": "km"},
        ],
        "relations": [
            {
                "id": "relation.unit_reading",
                "type": "written_and_read_as",
                "from_id": "quantity.length",
                "written": "2 km",
                "read": "2 킬로미터",
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

    base_line = LineSlot(
        id="slot.diagram.base_line",
        prompt="",
        x1=180,
        y1=174,
        x2=700,
        y2=174,
        stroke="#111827",
        stroke_width=1.8,
    )
    dot_1 = CircleSlot(
        id="slot.diagram.dot_1",
        prompt="",
        cx=180,
        cy=174,
        r=4.0,
        fill="#111827",
        stroke="#111827",
        stroke_width=1.0,
    )
    dot_2 = CircleSlot(
        id="slot.diagram.dot_2",
        prompt="",
        cx=440,
        cy=174,
        r=4.0,
        fill="#111827",
        stroke="#111827",
        stroke_width=1.0,
    )
    dot_3 = CircleSlot(
        id="slot.diagram.dot_3",
        prompt="",
        cx=700,
        cy=174,
        r=4.0,
        fill="#111827",
        stroke="#111827",
        stroke_width=1.0,
    )

    arc_1 = PathSlot(
        id="slot.diagram.arc_1",
        prompt="",
        d="M 180 174 Q 310 112 440 174",
        fill="none",
        stroke="#6b7280",
        stroke_width=1.5,
        stroke_dasharray="5 4",
    )
    arc_2 = PathSlot(
        id="slot.diagram.arc_2",
        prompt="",
        d="M 440 174 Q 570 112 700 174",
        fill="none",
        stroke="#6b7280",
        stroke_width=1.5,
        stroke_dasharray="5 4",
    )

    label_1 = TextBoxSlot(
        id="slot.diagram.label_1",
        prompt="",
        text="1 km",
        x=260,
        y=108,
        width=100,
        height=36,
        font_size=24,
        font_family='"Noto Sans KR", sans-serif',
        fill="#111827",
        align="center",
        valign="middle",
    )
    label_2 = TextBoxSlot(
        id="slot.diagram.label_2",
        prompt="",
        text="1 km",
        x=520,
        y=108,
        width=100,
        height=36,
        font_size=24,
        font_family='"Noto Sans KR", sans-serif',
        fill="#111827",
        align="center",
        valign="middle",
    )

    write_badge = RectSlot(
        id="slot.answer.write_badge",
        prompt="",
        x=110,
        y=236,
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
        y=236,
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
        y=232,
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
        y=232,
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
        y=232,
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
        y=302,
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
        y=302,
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
        y=298,
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
        y=298,
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
        y=298,
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
        base_line,
        dot_1,
        dot_2,
        dot_3,
        arc_1,
        arc_2,
        label_1,
        label_2,
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
            height=380,
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
