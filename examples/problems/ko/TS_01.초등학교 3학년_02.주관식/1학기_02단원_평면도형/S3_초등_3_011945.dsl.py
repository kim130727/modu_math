"""ModuMath Problem DSL: 직각의 수가 가장 많은 도형 찾기 (S3_초등_3_011945)"""

from __future__ import annotations

from modu_math.dsl import (
    Canvas,
    PolygonSlot,
    ProblemTemplate,
    RectSlot,
    Region,
    TextBoxSlot,
)


PROBLEM_ID = "S3_초등_3_011945"
PROBLEM_TITLE = "직각의 수가 가장 많은 도형 찾기"


ANSWER = {
    "type": "short_answer",
    "value": "ㄷ",
    "unit": "",
    "values": ["ㄷ", "㉢"],
    "choices": [],
    "blanks": [
        {
            "id": "slot.answer.input",
            "slot_id": "slot.answer.input",
            "expected": "ㄷ",
        },
    ],
    "answer_key": [
        {
            "slot_id": "slot.answer.input",
            "value": "ㄷ",
            "diagnostics": [
                {
                    "id": "diag.missed_rotated_right_angles",
                    "condition": "answer_in_ga_na",
                    "concept": "직각의 개수 세기",
                    "reason": "기울어진 사각형 ㄷ의 직각을 찾지 못함",
                    "feedback": "도형이 기울어져 있어도 삼각자의 직각 부분을 대어 확인하면 ㄷ에는 직각이 4개 있습니다.",
                },
            ],
        },
    ],
}


SEMANTIC = {
    "problem_id": PROBLEM_ID,
    "problem_type": "short_answer_geometry_right_angle_comparison",
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
            {"id": "shape.g", "type": "pentagon", "label": "ㄱ", "right_angle_count": 2},
            {"id": "shape.n", "type": "pentagon", "label": "ㄴ", "right_angle_count": 1},
            {"id": "shape.d", "type": "square", "label": "ㄷ", "right_angle_count": 4},
        ],
        "relations": [
            {
                "id": "relation.max_right_angles",
                "type": "has_most_right_angles",
                "from_id": "shape.d",
                "to_id": "concept.right_angle",
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
        text="직각의 수가 가장 많은 도형을 찾아 기호를 쓰세요.",
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

    box_outer = RectSlot(
        id="slot.diagram.box_outer",
        prompt="",
        x=70,
        y=84,
        width=760,
        height=236,
        fill="#ffffff",
        stroke="#bcd96b",
        stroke_width=2.2,
    )

    label_g = TextBoxSlot(
        id="slot.diagram.label_g",
        prompt="",
        text="㉠",
        x=112,
        y=110,
        width=36,
        height=36,
        font_size=24,
        font_family='"Noto Sans KR", sans-serif',
        fill="#202124",
        align="center",
        valign="middle",
    )

    # ㄱ: 아래 두 각이 직각인 오각형 (직각 2개)
    shape_g = PolygonSlot(
        id="slot.diagram.shape_g",
        prompt="",
        points=(
            (215.0, 128.0),
            (275.0, 168.0),
            (275.0, 272.0),
            (155.0, 272.0),
            (155.0, 168.0),
        ),
        fill="none",
        stroke="#111827",
        stroke_width=1.8,
    )

    label_n = TextBoxSlot(
        id="slot.diagram.label_n",
        prompt="",
        text="㉡",
        x=342,
        y=110,
        width=36,
        height=36,
        font_size=24,
        font_family='"Noto Sans KR", sans-serif',
        fill="#202124",
        align="center",
        valign="middle",
    )

    # ㄴ: 위쪽 꼭짓점만 직각인 오각형 (직각 1개)
    shape_n = PolygonSlot(
        id="slot.diagram.shape_n",
        prompt="",
        points=(
            (465.0, 114.0),
            (545.0, 194.0),
            (505.0, 276.0),
            (425.0, 276.0),
            (385.0, 194.0),
        ),
        fill="none",
        stroke="#111827",
        stroke_width=1.8,
    )

    label_d = TextBoxSlot(
        id="slot.diagram.label_d",
        prompt="",
        text="㉢",
        x=590,
        y=110,
        width=36,
        height=36,
        font_size=24,
        font_family='"Noto Sans KR", sans-serif',
        fill="#202124",
        align="center",
        valign="middle",
    )

    # ㄷ: 45도 기울어진 정사각형 (직각 4개)
    shape_d = PolygonSlot(
        id="slot.diagram.shape_d",
        prompt="",
        points=(
            (715.0, 114.0),
            (795.0, 194.0),
            (715.0, 274.0),
            (635.0, 194.0),
        ),
        fill="none",
        stroke="#111827",
        stroke_width=1.8,
    )

    paren_left = TextBoxSlot(
        id="slot.answer.paren_left",
        prompt="",
        text="(",
        x=560,
        y=346,
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
        x=594,
        y=346,
        width=170,
        height=52,
        fill="#ffffff",
        stroke="#111827",
        stroke_width=1.4,
        interaction={
            "type": "input",
            "role": "answer",
            "value_type": "text",
            "max_length": 4,
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
        y=346,
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
        label_g,
        shape_g,
        label_n,
        shape_n,
        label_d,
        shape_d,
        paren_left,
        answer_input,
        paren_right,
    )

    return ProblemTemplate(
        id=PROBLEM_ID,
        title=PROBLEM_TITLE,
        canvas=Canvas(
            width=900,
            height=420,
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
