"""ModuMath Problem DSL: 직각삼각형 모두 찾아 쓰기 (S3_초등_3_011946)"""

from __future__ import annotations

from modu_math.dsl import (
    Canvas,
    PolygonSlot,
    ProblemTemplate,
    RectSlot,
    Region,
    TextBoxSlot,
)


PROBLEM_ID = "S3_초등_3_011946"
PROBLEM_TITLE = "직각삼각형 모두 찾아 쓰기"


ANSWER = {
    "type": "short_answer",
    "value": "가, 라",
    "unit": "",
    "values": ["가, 라", "가,라", "라, 가", "라,가"],
    "choices": [],
    "blanks": [
        {
            "id": "slot.answer.input",
            "slot_id": "slot.answer.input",
            "expected": "가, 라",
        },
    ],
    "answer_key": [
        {
            "slot_id": "slot.answer.input",
            "value": "가, 라",
            "diagnostics": [
                {
                    "id": "diag.missed_rotated_right_triangle",
                    "condition": "answer_equals_ga",
                    "concept": "직각삼각형",
                    "reason": "기울어져 있는 직각삼각형 라를 찾지 못함",
                    "feedback": "삼각형이 기울어져 있더라도 한 각이 직각이면 직각삼각형입니다. 라의 각을 삼각자로 확인해 보세요.",
                },
            ],
        },
    ],
}


SEMANTIC = {
    "problem_id": PROBLEM_ID,
    "problem_type": "short_answer_geometry_right_triangle_classification",
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
            {"id": "triangle.ga", "type": "right_triangle", "label": "가", "has_right_angle": True},
            {"id": "triangle.na", "type": "obtuse_triangle", "label": "나", "has_right_angle": False},
            {"id": "triangle.da", "type": "acute_triangle", "label": "다", "has_right_angle": False},
            {"id": "triangle.ra", "type": "right_triangle", "label": "라", "has_right_angle": True},
        ],
        "relations": [
            {
                "id": "relation.ga_is_right_triangle",
                "type": "is_right_triangle",
                "from_id": "triangle.ga",
                "to_id": "concept.right_triangle",
            },
            {
                "id": "relation.ra_is_right_triangle",
                "type": "is_right_triangle",
                "from_id": "triangle.ra",
                "to_id": "concept.right_triangle",
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
        text="도형을 보고 물음에 답하세요.",
        x=32,
        y=22,
        width=820,
        height=40,
        font_size=26,
        font_family='"Noto Sans KR", sans-serif',
        fill="#202124",
        align="left",
        valign="top",
        line_height=1.4,
    )

    box_outer = RectSlot(
        id="slot.diagram.box_outer",
        prompt="",
        x=70,
        y=78,
        width=760,
        height=158,
        fill="#ffffff",
        stroke="#f3a683",
        stroke_width=2.2,
    )

    # 가: 오른쪽 아래가 직각인 직각삼각형
    tri_ga = PolygonSlot(
        id="slot.diagram.tri_ga",
        prompt="",
        points=((230.0, 108.0), (230.0, 206.0), (102.0, 206.0)),
        fill="none",
        stroke="#111827",
        stroke_width=1.8,
    )
    label_ga = TextBoxSlot(
        id="slot.diagram.label_ga",
        prompt="",
        text="가",
        x=166,
        y=162,
        width=40,
        height=34,
        font_size=22,
        font_family='"Noto Sans KR", sans-serif',
        fill="#202124",
        align="center",
        valign="middle",
    )

    # 나: 둔각삼각형
    tri_na = PolygonSlot(
        id="slot.diagram.tri_na",
        prompt="",
        points=((295.0, 108.0), (420.0, 206.0), (325.0, 206.0)),
        fill="none",
        stroke="#111827",
        stroke_width=1.8,
    )
    label_na = TextBoxSlot(
        id="slot.diagram.label_na",
        prompt="",
        text="나",
        x=325,
        y=164,
        width=40,
        height=34,
        font_size=22,
        font_family='"Noto Sans KR", sans-serif',
        fill="#202124",
        align="center",
        valign="middle",
    )

    # 다: 예각삼각형
    tri_da = PolygonSlot(
        id="slot.diagram.tri_da",
        prompt="",
        points=((538.0, 108.0), (595.0, 206.0), (481.0, 206.0)),
        fill="none",
        stroke="#111827",
        stroke_width=1.8,
    )
    label_da = TextBoxSlot(
        id="slot.diagram.label_da",
        prompt="",
        text="다",
        x=518,
        y=162,
        width=40,
        height=34,
        font_size=22,
        font_family='"Noto Sans KR", sans-serif',
        fill="#202124",
        align="center",
        valign="middle",
    )

    # 라: 기울어진 직각삼각형 (오른쪽 위 꼭짓점이 직각: (755, 102)에서 (655, 127)과 (785, 222)가 수직)
    tri_ra = PolygonSlot(
        id="slot.diagram.tri_ra",
        prompt="",
        points=((655.0, 127.0), (755.0, 102.0), (785.0, 222.0)),
        fill="none",
        stroke="#111827",
        stroke_width=1.8,
    )
    label_ra = TextBoxSlot(
        id="slot.diagram.label_ra",
        prompt="",
        text="라",
        x=714,
        y=130,
        width=40,
        height=34,
        font_size=22,
        font_family='"Noto Sans KR", sans-serif',
        fill="#202124",
        align="center",
        valign="middle",
    )

    subquestion_slot = TextBoxSlot(
        id="slot.stem.subquestion",
        prompt="",
        text="(2) 직각삼각형을 모두 찾아 쓰세요.",
        x=48,
        y=260,
        width=760,
        height=40,
        font_size=24,
        font_family='"Noto Sans KR", sans-serif',
        fill="#202124",
        align="left",
        valign="top",
        line_height=1.4,
    )

    paren_left = TextBoxSlot(
        id="slot.answer.paren_left",
        prompt="",
        text="(",
        x=520,
        y=316,
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
        y=316,
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
        y=316,
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
        box_outer,
        tri_ga,
        label_ga,
        tri_na,
        label_na,
        tri_da,
        label_da,
        tri_ra,
        label_ra,
        subquestion_slot,
        paren_left,
        answer_input,
        paren_right,
    )

    return ProblemTemplate(
        id=PROBLEM_ID,
        title=PROBLEM_TITLE,
        canvas=Canvas(
            width=900,
            height=390,
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
