"""ModuMath Problem DSL: 두 점을 곧게 이은 선의 이름 쓰기 (S3_초등_3_011940)"""

from __future__ import annotations

from modu_math.dsl import (
    Canvas,
    CircleSlot,
    LineSlot,
    ProblemTemplate,
    RectSlot,
    Region,
    TextBoxSlot,
)


PROBLEM_ID = "S3_초등_3_011940"
PROBLEM_TITLE = "두 점을 곧게 이은 선의 이름 쓰기"


ANSWER = {
    "type": "short_answer",
    "value": "선분",
    "unit": "",
    "values": ["선분"],
    "choices": [],
    "blanks": [
        {
            "id": "slot.answer.input",
            "slot_id": "slot.answer.input",
            "expected": "선분",
        },
    ],
    "answer_key": [
        {
            "slot_id": "slot.answer.input",
            "value": "선분",
            "diagnostics": [
                {
                    "id": "diag.straight_line_confusion",
                    "condition": "answer_equals_straight_line",
                    "concept": "선분의 정의",
                    "reason": "두 점을 곧게 이은 선을 직선으로 답함",
                    "feedback": "양쪽으로 끝없이 늘인 선이 아니라 두 점 사이를 곧게 이은 선이므로 선분입니다.",
                },
                {
                    "id": "diag.ray_confusion",
                    "condition": "answer_equals_ray",
                    "concept": "선분의 정의",
                    "reason": "두 점을 곧게 이은 선을 반직선으로 답함",
                    "feedback": "한쪽 끝으로 계속 뻗어 나가는 선이 아니라 두 점 사이에서 끝나는 선이므로 선분입니다.",
                },
            ],
        },
    ],
}


SEMANTIC = {
    "problem_id": PROBLEM_ID,
    "problem_type": "short_answer_geometry_line_naming",
    "metadata": {
        "school": "초등학교",
        "grade": 3,
        "semester": 1,
        "chapter": "02단원_평면도형",
        "subject": "수학",
        "language": "ko-KR",
    },
    "domain": {
        "objects": [
            {"id": "point.left", "type": "point", "label": "왼쪽 점"},
            {"id": "point.right", "type": "point", "label": "오른쪽 점"},
            {"id": "line.segment", "type": "line_segment", "label": "두 점을 곧게 이은 선"},
        ],
        "relations": [
            {
                "id": "relation.connects_points",
                "type": "line_segment_between",
                "from_id": "point.left",
                "to_id": "point.right",
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
        text="그림과 같이 두 점을 곧게 이은 선을 무엇이라고 할까요?",
        x=32,
        y=24,
        width=836,
        height=44,
        font_size=26,
        font_family='"Noto Sans KR", sans-serif',
        fill="#202124",
        align="left",
        valign="top",
        line_height=1.45,
    )

    bar_between = RectSlot(
        id="slot.diagram.bar_between",
        prompt="",
        x=235,
        y=130,
        width=430,
        height=24,
        fill="#e5e7eb",
        stroke="#cbd5e1",
        stroke_width=1.0,
    )

    pillar_left = RectSlot(
        id="slot.diagram.pillar_left",
        prompt="",
        x=170,
        y=95,
        width=65,
        height=175,
        fill="#bae6fd",
        stroke="#7dd3fc",
        stroke_width=1.2,
    )

    pillar_right = RectSlot(
        id="slot.diagram.pillar_right",
        prompt="",
        x=665,
        y=95,
        width=65,
        height=175,
        fill="#bae6fd",
        stroke="#7dd3fc",
        stroke_width=1.2,
    )

    segment_line = LineSlot(
        id="slot.diagram.segment_line",
        prompt="",
        x1=235,
        y1=130,
        x2=665,
        y2=130,
        stroke="#111827",
        stroke_width=2.2,
    )

    point_left = CircleSlot(
        id="slot.diagram.point_left",
        prompt="",
        cx=235,
        cy=130,
        r=4.2,
        fill="#111827",
        stroke="#111827",
        stroke_width=1.0,
    )

    point_right = CircleSlot(
        id="slot.diagram.point_right",
        prompt="",
        cx=665,
        cy=130,
        r=4.2,
        fill="#111827",
        stroke="#111827",
        stroke_width=1.0,
    )

    paren_left = TextBoxSlot(
        id="slot.answer.paren_left",
        prompt="",
        text="(",
        x=520,
        y=300,
        width=28,
        height=52,
        font_size=28,
        font_family='"Noto Sans KR", sans-serif',
        fill="#202124",
        align="center",
        valign="middle",
    )

    answer_input = RectSlot(
        id="slot.answer.input",
        prompt="",
        x=554,
        y=300,
        width=210,
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

    paren_right = TextBoxSlot(
        id="slot.answer.paren_right",
        prompt="",
        text=")",
        x=770,
        y=300,
        width=28,
        height=52,
        font_size=28,
        font_family='"Noto Sans KR", sans-serif',
        fill="#202124",
        align="center",
        valign="middle",
    )

    slots = (
        stem_slot,
        bar_between,
        pillar_left,
        pillar_right,
        segment_line,
        point_left,
        point_right,
        paren_left,
        answer_input,
        paren_right,
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
