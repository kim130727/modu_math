"""ModuMath Problem DSL: km와 m 단위 환산하기 (S3_초등_3_012003)"""

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


PROBLEM_ID = "S3_초등_3_012003"
PROBLEM_TITLE = "도서관에서 학교까지의 거리를 m로 나타내기"


ANSWER = {
    "type": "short_answer",
    "value": 2300,
    "unit": "m",
    "values": [2300],
    "choices": [],
    "blanks": [
        {
            "id": "slot.answer.input",
            "slot_id": "slot.answer.input",
            "expected": 2300,
        },
    ],
    "answer_key": [
        {
            "slot_id": "slot.answer.input",
            "value": 2300,
            "diagnostics": [
                {
                    "id": "diag.km_to_m_zero_error",
                    "condition": "answer_equals_230",
                    "concept": "1 km = 1000 m",
                    "reason": "1 km를 100 m로 잘못 바꾸어 230 m로 답함",
                    "feedback": "1 km는 1000 m입니다. 따라서 2 km 300 m = 2000 m + 300 m = 2300 m입니다.",
                },
            ],
        },
    ],
}


SEMANTIC = {
    "problem_id": PROBLEM_ID,
    "problem_type": "short_answer_length_unit_conversion",
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
            {"id": "place.library", "type": "location", "label": "도서관"},
            {"id": "place.school", "type": "location", "label": "학교"},
            {"id": "quantity.distance_m", "type": "quantity", "label": "도서관에서 학교까지의 거리", "value": 2300, "unit": "m"},
        ],
        "relations": [
            {
                "id": "relation.distance",
                "type": "distance_between",
                "from_id": "place.library",
                "to_id": "place.school",
                "quantity": "quantity.distance_m",
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
        text="도서관에서 학교까지의 거리는 몇 m일까요?",
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

    lib_building = RectSlot(
        id="slot.diagram.lib_building",
        prompt="",
        x=72,
        y=120,
        width=116,
        height=88,
        fill="#e0f2fe",
        stroke="#0284c7",
        stroke_width=1.6,
    )
    lib_sign = RectSlot(
        id="slot.diagram.lib_sign",
        prompt="",
        x=92,
        y=96,
        width=76,
        height=24,
        fill="#fed7aa",
        stroke="#ea580c",
        stroke_width=1.2,
    )
    lib_sign_text = TextBoxSlot(
        id="slot.diagram.lib_sign_text",
        prompt="",
        text="도서관",
        x=92,
        y=96,
        width=76,
        height=24,
        font_size=14,
        font_family='"Noto Sans KR", sans-serif',
        fill="#7c2d12",
        align="center",
        valign="middle",
    )
    lib_label = TextBoxSlot(
        id="slot.diagram.lib_label",
        prompt="",
        text="도서관",
        x=70,
        y=216,
        width=120,
        height=34,
        font_size=24,
        font_family='"Noto Sans KR", sans-serif',
        fill="#111827",
        align="center",
        valign="middle",
    )

    school_building = RectSlot(
        id="slot.diagram.school_building",
        prompt="",
        x=705,
        y=136,
        width=120,
        height=72,
        fill="#ddd6fe",
        stroke="#7c3aed",
        stroke_width=1.6,
    )
    school_clock = CircleSlot(
        id="slot.diagram.school_clock",
        prompt="",
        cx=765,
        cy=154,
        r=10.0,
        fill="#ffffff",
        stroke="#111827",
        stroke_width=1.2,
    )
    school_label = TextBoxSlot(
        id="slot.diagram.school_label",
        prompt="",
        text="학교",
        x=705,
        y=216,
        width=120,
        height=34,
        font_size=24,
        font_family='"Noto Sans KR", sans-serif',
        fill="#111827",
        align="center",
        valign="middle",
    )

    dist_line = LineSlot(
        id="slot.diagram.dist_line",
        prompt="",
        x1=210,
        y1=200,
        x2=685,
        y2=200,
        stroke="#111827",
        stroke_width=1.8,
    )
    dot_left = CircleSlot(
        id="slot.diagram.dot_left",
        prompt="",
        cx=210,
        cy=200,
        r=4.0,
        fill="#111827",
        stroke="#111827",
        stroke_width=1.0,
    )
    dot_right = CircleSlot(
        id="slot.diagram.dot_right",
        prompt="",
        cx=685,
        cy=200,
        r=4.0,
        fill="#111827",
        stroke="#111827",
        stroke_width=1.0,
    )
    arc_dist = PathSlot(
        id="slot.diagram.arc_dist",
        prompt="",
        d="M 210 200 Q 447 120 685 200",
        fill="none",
        stroke="#ec4899",
        stroke_width=1.5,
        stroke_dasharray="5 4",
    )
    dist_label = TextBoxSlot(
        id="slot.diagram.dist_label",
        prompt="",
        text="2 km 300 m",
        x=340,
        y=118,
        width=215,
        height=40,
        font_size=28,
        font_family='"Noto Sans KR", sans-serif',
        fill="#111827",
        align="center",
        valign="middle",
    )

    paren_left = TextBoxSlot(
        id="slot.answer.paren_left",
        prompt="",
        text="(",
        x=520,
        y=278,
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
        y=278,
        width=160,
        height=54,
        fill="#ffffff",
        stroke="#111827",
        stroke_width=1.4,
        interaction={
            "type": "input",
            "role": "answer",
            "value_type": "integer",
            "max_length": 5,
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
        text="m",
        x=720,
        y=278,
        width=40,
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
        x=766,
        y=278,
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
        lib_building,
        lib_sign,
        lib_sign_text,
        lib_label,
        school_building,
        school_clock,
        school_label,
        dist_line,
        dot_left,
        dot_right,
        arc_dist,
        dist_label,
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
            height=364,
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
