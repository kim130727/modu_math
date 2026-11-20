"""ModuMath Problem DSL: 도형을 보고 사각형 개수 구하기 (S3_초등_3_011939)"""

from __future__ import annotations

from modu_math.dsl import (
    Canvas,
    PathSlot,
    PolygonSlot,
    ProblemTemplate,
    RectSlot,
    Region,
    TextBoxSlot,
)


PROBLEM_ID = "S3_초등_3_011939"
PROBLEM_TITLE = "여러 도형 중에서 사각형 개수 세기"


ANSWER = {
    "type": "short_answer",
    "value": 2,
    "unit": "개",
    "values": [2],
    "choices": [],
    "blanks": [
        {
            "id": "slot.answer.input",
            "slot_id": "slot.answer.input",
            "expected": 2,
        },
    ],
    "answer_key": [
        {
            "slot_id": "slot.answer.input",
            "value": 2,
            "diagnostics": [
                {
                    "id": "diag.counted_pentagon_as_quadrilateral",
                    "condition": "answer_equals_3",
                    "concept": "사각형의 정의",
                    "reason": "변이 5개인 오각형까지 사각형으로 셈",
                    "feedback": "사각형은 4개의 곧은 선으로 둘러싸인 도형입니다. 변의 개수가 5개인 도형은 제외하고 다시 세어 보세요.",
                },
                {
                    "id": "diag.missed_irregular_quadrilateral",
                    "condition": "answer_equals_1",
                    "concept": "사각형 찾기",
                    "reason": "직사각형만 사각형으로 보고 일반 사각형을 놓침",
                    "feedback": "네 각이 직각이 아니더라도 4개의 곧은 선으로 둘러싸인 도형은 모두 사각형입니다.",
                },
            ],
        },
    ],
}


SEMANTIC = {
    "problem_id": PROBLEM_ID,
    "problem_type": "short_answer_geometry_shape_counting",
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
            {"id": "shape.1", "type": "quadrilateral", "label": "도형 1 (직사각형)", "is_quadrilateral": True},
            {"id": "shape.2", "type": "triangle", "label": "도형 2 (삼각형)", "is_quadrilateral": False},
            {"id": "shape.3", "type": "sector", "label": "도형 3 (부채꼴)", "is_quadrilateral": False},
            {"id": "shape.4", "type": "triangle", "label": "도형 4 (삼각형)", "is_quadrilateral": False},
            {"id": "shape.5", "type": "triangle", "label": "도형 5 (직각삼각형)", "is_quadrilateral": False},
            {"id": "shape.6", "type": "quadrilateral", "label": "도형 6 (사각형)", "is_quadrilateral": True},
            {"id": "shape.7", "type": "semicircle", "label": "도형 7 (반원)", "is_quadrilateral": False},
            {"id": "shape.8", "type": "pentagon", "label": "도형 8 (오각형)", "is_quadrilateral": False},
            {"id": "quantity.quadrilateral_count", "type": "quantity", "label": "사각형의 개수", "value": 2, "unit": "개"},
        ],
        "relations": [
            {
                "id": "relation.quadrilateral_count",
                "type": "count_of",
                "from_id": "quantity.quadrilateral_count",
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
        height=252,
        fill="#fffaf6",
        stroke="#f3c6b6",
        stroke_width=2.0,
    )

    shape_1 = PolygonSlot(
        id="slot.diagram.shape_1",
        prompt="",
        points=((115.0, 108.0), (245.0, 108.0), (245.0, 178.0), (115.0, 178.0)),
        fill="#ffffff",
        stroke="#111827",
        stroke_width=1.8,
    )
    shape_2 = PolygonSlot(
        id="slot.diagram.shape_2",
        prompt="",
        points=((355.0, 104.0), (400.0, 178.0), (310.0, 178.0)),
        fill="#ffffff",
        stroke="#111827",
        stroke_width=1.8,
    )
    shape_3 = PathSlot(
        id="slot.diagram.shape_3",
        prompt="",
        d="M 475 104 L 475 178 L 549 178 A 74 74 0 0 0 475 104 Z",
        fill="#ffffff",
        stroke="#111827",
        stroke_width=1.8,
    )
    shape_4 = PolygonSlot(
        id="slot.diagram.shape_4",
        prompt="",
        points=((695.0, 104.0), (740.0, 178.0), (620.0, 178.0)),
        fill="#ffffff",
        stroke="#111827",
        stroke_width=1.8,
    )

    shape_5 = PolygonSlot(
        id="slot.diagram.shape_5",
        prompt="",
        points=((125.0, 214.0), (240.0, 292.0), (125.0, 292.0)),
        fill="#ffffff",
        stroke="#111827",
        stroke_width=1.8,
    )
    shape_6 = PolygonSlot(
        id="slot.diagram.shape_6",
        prompt="",
        points=((325.0, 218.0), (395.0, 246.0), (395.0, 292.0), (305.0, 292.0)),
        fill="#ffffff",
        stroke="#111827",
        stroke_width=1.8,
    )
    shape_7 = PathSlot(
        id="slot.diagram.shape_7",
        prompt="",
        d="M 455 292 A 62 62 0 0 1 579 292 Z",
        fill="#ffffff",
        stroke="#111827",
        stroke_width=1.8,
    )
    shape_8 = PolygonSlot(
        id="slot.diagram.shape_8",
        prompt="",
        points=((635.0, 218.0), (695.0, 218.0), (725.0, 255.0), (695.0, 292.0), (635.0, 292.0)),
        fill="#ffffff",
        stroke="#111827",
        stroke_width=1.8,
    )

    subquestion_slot = TextBoxSlot(
        id="slot.stem.subquestion",
        prompt="",
        text="(2) 사각형은 모두 몇 개일까요?",
        x=48,
        y=350,
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
        x=560,
        y=402,
        width=26,
        height=52,
        font_size=26,
        font_family='"Noto Sans KR", sans-serif',
        fill="#202124",
        align="center",
        valign="middle",
    )

    answer_input = RectSlot(
        id="slot.answer.input",
        prompt="",
        x=592,
        y=402,
        width=110,
        height=52,
        fill="#ffffff",
        stroke="#111827",
        stroke_width=1.4,
        interaction={
            "type": "input",
            "role": "answer",
            "value_type": "integer",
            "max_length": 2,
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
        text="개",
        x=710,
        y=402,
        width=36,
        height=52,
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
        x=750,
        y=402,
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
        box_outer,
        shape_1,
        shape_2,
        shape_3,
        shape_4,
        shape_5,
        shape_6,
        shape_7,
        shape_8,
        subquestion_slot,
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
            height=480,
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
