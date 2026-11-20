"""ModuMath Problem DSL: 반직선의 이름 쓰기 (S3_초등_3_011941)"""

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


PROBLEM_ID = "S3_초등_3_011941"
PROBLEM_TITLE = "반직선 ㄷㄹ의 이름 쓰기"


ANSWER = {
    "type": "short_answer",
    "value": "반직선 ㄷㄹ",
    "unit": "",
    "values": ["반직선 ㄷㄹ", "반직선ㄷㄹ"],
    "choices": [],
    "blanks": [
        {
            "id": "slot.answer.input",
            "slot_id": "slot.answer.input",
            "expected": "반직선 ㄷㄹ",
        },
    ],
    "answer_key": [
        {
            "slot_id": "slot.answer.input",
            "value": "반직선 ㄷㄹ",
            "diagnostics": [
                {
                    "id": "diag.reversed_ray_order",
                    "condition": "answer_equals_ray_rd",
                    "concept": "반직선의 이름 읽기",
                    "reason": "시작점이 아닌 지나는 점을 먼저 써서 반직선 ㄹㄷ으로 답함",
                    "feedback": "반직선의 이름은 시작하는 점을 먼저 씁니다. 점 ㄷ에서 시작하여 점 ㄹ을 지나므로 반직선 ㄷㄹ입니다.",
                },
                {
                    "id": "diag.line_segment_or_line_confusion",
                    "condition": "answer_not_ray",
                    "concept": "반직선의 정의",
                    "reason": "한쪽 끝으로만 길게 늘인 선을 선분이나 직선으로 혼동함",
                    "feedback": "점 ㄷ에서 시작하여 점 ㄹ 쪽으로 끝없이 늘인 곧은 선이므로 반직선입니다.",
                },
            ],
        },
    ],
}


SEMANTIC = {
    "problem_id": PROBLEM_ID,
    "problem_type": "short_answer_geometry_ray_naming",
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
            {"id": "point.d", "type": "point", "label": "점 ㄷ", "is_start_point": True},
            {"id": "point.r", "type": "point", "label": "점 ㄹ", "is_start_point": False},
            {"id": "ray.dr", "type": "ray", "label": "반직선 ㄷㄹ"},
        ],
        "relations": [
            {
                "id": "relation.ray_direction",
                "type": "ray_from_through",
                "from_id": "point.d",
                "to_id": "point.r",
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
        text="도형의 이름을 쓰세요.",
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

    label_d = TextBoxSlot(
        id="slot.diagram.label_d",
        prompt="",
        text="ㄷ",
        x=218,
        y=108,
        width=40,
        height=34,
        font_size=24,
        font_family='"Noto Sans KR", sans-serif',
        fill="#202124",
        align="center",
        valign="middle",
    )

    label_r = TextBoxSlot(
        id="slot.diagram.label_r",
        prompt="",
        text="ㄹ",
        x=562,
        y=108,
        width=40,
        height=34,
        font_size=24,
        font_family='"Noto Sans KR", sans-serif',
        fill="#202124",
        align="center",
        valign="middle",
    )

    ray_line = LineSlot(
        id="slot.diagram.ray_line",
        prompt="",
        x1=238,
        y1=160,
        x2=710,
        y2=160,
        stroke="#111827",
        stroke_width=2.0,
    )

    point_d = CircleSlot(
        id="slot.diagram.point_d",
        prompt="",
        cx=238,
        cy=160,
        r=4.2,
        fill="#111827",
        stroke="#111827",
        stroke_width=1.0,
    )

    point_r = CircleSlot(
        id="slot.diagram.point_r",
        prompt="",
        cx=582,
        cy=160,
        r=4.2,
        fill="#111827",
        stroke="#111827",
        stroke_width=1.0,
    )

    paren_left = TextBoxSlot(
        id="slot.answer.paren_left",
        prompt="",
        text="(",
        x=480,
        y=232,
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
        x=514,
        y=232,
        width=250,
        height=52,
        fill="#ffffff",
        stroke="#111827",
        stroke_width=1.4,
        interaction={
            "type": "input",
            "role": "answer",
            "value_type": "text",
            "max_length": 12,
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
        y=232,
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
        label_d,
        label_r,
        ray_line,
        point_d,
        point_r,
        paren_left,
        answer_input,
        paren_right,
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
