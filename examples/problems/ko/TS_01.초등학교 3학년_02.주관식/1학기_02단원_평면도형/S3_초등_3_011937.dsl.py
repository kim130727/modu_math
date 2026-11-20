"""ModuMath Problem DSL: 그림과 같은 도형의 이름 쓰기 (S3_초등_3_011937)"""

from __future__ import annotations

from modu_math.dsl import (
    Canvas,
    PolygonSlot,
    ProblemTemplate,
    RectSlot,
    Region,
    TextBoxSlot,
)


PROBLEM_ID = "S3_초등_3_011937"
PROBLEM_TITLE = "사각형의 이름 쓰기"


ANSWER = {
    "type": "short_answer",
    "value": "사각형",
    "unit": "",
    "values": ["사각형"],
    "choices": [],
    "blanks": [
        {
            "id": "slot.answer.input",
            "slot_id": "slot.answer.input",
            "expected": "사각형",
        },
    ],
    "answer_key": [
        {
            "slot_id": "slot.answer.input",
            "value": "사각형",
            "diagnostics": [
                {
                    "id": "diag.triangle_confusion",
                    "condition": "answer_equals_triangle",
                    "concept": "사각형",
                    "reason": "변과 꼭짓점의 개수를 세지 않고 삼각형으로 답함",
                    "feedback": "도형의 변과 꼭짓점이 각각 몇 개인지 세어 보세요. 4개의 곧은 선으로 둘러싸인 도형은 사각형입니다.",
                },
            ],
        },
    ],
}


SEMANTIC = {
    "problem_id": PROBLEM_ID,
    "problem_type": "short_answer_geometry_shape_naming",
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
            {"id": "shape.quad_1", "type": "quadrilateral", "label": "정사각형 모양 사각형", "sides": 4, "vertices": 4},
            {"id": "shape.quad_2", "type": "quadrilateral", "label": "사다리꼴 모양 사각형", "sides": 4, "vertices": 4},
            {"id": "shape.quad_3", "type": "quadrilateral", "label": "평행사변형 모양 사각형", "sides": 4, "vertices": 4},
        ],
        "relations": [
            {
                "id": "relation.common_shape_name",
                "type": "has_shape_name",
                "from_id": "shape.quad_1",
                "to_id": "concept.quadrilateral",
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
        text="그림과 같은 도형의 이름을 쓰세요.",
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

    quad_1 = PolygonSlot(
        id="slot.diagram.quad_1",
        prompt="",
        points=(
            (150.0, 100.0),
            (290.0, 100.0),
            (290.0, 230.0),
            (150.0, 230.0),
        ),
        fill="none",
        stroke="#111827",
        stroke_width=2.0,
    )

    quad_2 = PolygonSlot(
        id="slot.diagram.quad_2",
        prompt="",
        points=(
            (405.0, 100.0),
            (525.0, 100.0),
            (565.0, 230.0),
            (365.0, 230.0),
        ),
        fill="none",
        stroke="#111827",
        stroke_width=2.0,
    )

    quad_3 = PolygonSlot(
        id="slot.diagram.quad_3",
        prompt="",
        points=(
            (635.0, 100.0),
            (745.0, 100.0),
            (780.0, 230.0),
            (670.0, 230.0),
        ),
        fill="none",
        stroke="#111827",
        stroke_width=2.0,
    )

    paren_left = TextBoxSlot(
        id="slot.answer.paren_left",
        prompt="",
        text="(",
        x=520,
        y=278,
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
        y=278,
        width=210,
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
        y=278,
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
        quad_1,
        quad_2,
        quad_3,
        paren_left,
        answer_input,
        paren_right,
    )

    return ProblemTemplate(
        id=PROBLEM_ID,
        title=PROBLEM_TITLE,
        canvas=Canvas(
            width=900,
            height=360,
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
