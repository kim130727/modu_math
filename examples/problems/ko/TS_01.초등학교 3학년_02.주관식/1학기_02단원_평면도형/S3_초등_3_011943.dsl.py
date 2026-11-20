"""ModuMath Problem DSL: 도형에서 선분 개수 세기 (S3_초등_3_011943)"""

from __future__ import annotations

from modu_math.dsl import (
    Canvas,
    PolygonSlot,
    ProblemTemplate,
    RectSlot,
    Region,
    TextBoxSlot,
)


PROBLEM_ID = "S3_초등_3_011943"
PROBLEM_TITLE = "도형에 있는 선분의 개수 세기"


ANSWER = {
    "type": "short_answer",
    "value": 4,
    "unit": "개",
    "values": [4],
    "choices": [],
    "blanks": [
        {
            "id": "slot.answer.input",
            "slot_id": "slot.answer.input",
            "expected": 4,
        },
    ],
    "answer_key": [
        {
            "slot_id": "slot.answer.input",
            "value": 4,
            "diagnostics": [
                {
                    "id": "diag.miscounted_segments",
                    "condition": "answer_not_equals_4",
                    "concept": "선분의 개수",
                    "reason": "도형을 둘러싼 선분의 개수를 잘못 셈",
                    "feedback": "도형의 꼭짓점과 꼭짓점을 곧게 이은 변이 모두 몇 개인지 하나씩 세어 보세요.",
                },
            ],
        },
    ],
}


SEMANTIC = {
    "problem_id": PROBLEM_ID,
    "problem_type": "short_answer_geometry_segment_counting",
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
            {"id": "shape.quad", "type": "quadrilateral", "label": "사각형", "segments": 4},
            {"id": "quantity.segment_count", "type": "quantity", "label": "선분의 개수", "value": 4, "unit": "개"},
        ],
        "relations": [
            {
                "id": "relation.has_segments",
                "type": "segment_count_of",
                "from_id": "shape.quad",
                "to_id": "quantity.segment_count",
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
        text="도형에는 선분이 몇 개 있을까요?",
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

    quad_slot = PolygonSlot(
        id="slot.diagram.quadrilateral",
        prompt="",
        points=(
            (350.0, 96.0),
            (545.0, 128.0),
            (610.0, 260.0),
            (285.0, 260.0),
        ),
        fill="none",
        stroke="#111827",
        stroke_width=2.0,
    )

    paren_left = TextBoxSlot(
        id="slot.answer.paren_left",
        prompt="",
        text="(",
        x=560,
        y=300,
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
        y=300,
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
        y=300,
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
        y=300,
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
        quad_slot,
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
