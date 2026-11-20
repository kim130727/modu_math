"""ModuMath Problem DSL: 색칠한 부분의 분수 크기가 다른 것 찾기 (S3_초등_3_012040)"""

from __future__ import annotations

import math

from modu_math.dsl import (
    Canvas,
    PathSlot,
    PolygonSlot,
    ProblemTemplate,
    RectSlot,
    Region,
    TextBoxSlot,
)


PROBLEM_ID = "S3_초등_3_012040"
PROBLEM_TITLE = "분수로 나타낼 때 다른 도형 찾기"


ANSWER = {
    "type": "short_answer",
    "value": "다",
    "unit": "",
    "values": ["다"],
    "choices": [],
    "blanks": [
        {
            "id": "slot.answer.input",
            "slot_id": "slot.answer.input",
            "expected": "다",
        },
    ],
    "answer_key": [
        {
            "slot_id": "slot.answer.input",
            "value": "다",
            "diagnostics": [
                {
                    "id": "diag.fraction_comparison_error",
                    "condition": "answer_in_ga_na",
                    "concept": "분수로 나타내기",
                    "reason": "가, 나, 다의 전체 등분 수와 색칠한 조각 수를 잘못 셈",
                    "feedback": "가와 나는 전체 6조각 중 5조각을 색칠하여 5/6이지만, 다는 전체 4조각 중 3조각을 색칠하여 3/4입니다.",
                },
            ],
        },
    ],
}


SEMANTIC = {
    "problem_id": PROBLEM_ID,
    "problem_type": "short_answer_fraction_odd_one_out",
    "metadata": {
        "school": "초등학교",
        "grade": 3,
        "semester": 1,
        "chapter": "06단원_분수와 소수",
        "subject": "수학",
        "language": "ko-KR",
    },
    "domain": {
        "objects": [
            {"id": "figure.ga", "type": "fraction_model", "label": "가", "fraction": "5/6"},
            {"id": "figure.na", "type": "fraction_model", "label": "나", "fraction": "5/6"},
            {"id": "figure.da", "type": "fraction_model", "label": "다", "fraction": "3/4"},
        ],
        "relations": [
            {
                "id": "relation.different_fraction",
                "type": "odd_one_out",
                "from_id": "figure.da",
                "to_id": "concept.fraction",
            },
        ],
    },
    "answer": ANSWER,
}

SEMANTIC_OVERRIDE = SEMANTIC


def _hex_6_slots(cx: float, cy: float, r: float) -> list[PolygonSlot]:
    slots: list[PolygonSlot] = []
    pts = [
        (round(cx + r * math.cos(math.radians(i * 60)), 1), round(cy + r * math.sin(math.radians(i * 60)), 1))
        for i in range(6)
    ]
    for i in range(6):
        shaded = i != 0  # 오른쪽 아래 1조각만 흰색 (인덱스 0)
        slots.append(
            PolygonSlot(
                id=f"slot.diagram.ga_tri_{i}",
                prompt="",
                points=((cx, cy), pts[i], pts[(i + 1) % 6]),
                fill="#fed7aa" if shaded else "#ffffff",
                stroke="#ea580c",
                stroke_width=1.1,
            )
        )
    return slots


def _circle_6_slots(cx: float, cy: float, r: float) -> list[PathSlot]:
    slots: list[PathSlot] = []
    for i in range(6):
        a1 = math.radians(i * 60 - 90)
        a2 = math.radians((i + 1) * 60 - 90)
        x1, y1 = cx + r * math.cos(a1), cy + r * math.sin(a1)
        x2, y2 = cx + r * math.cos(a2), cy + r * math.sin(a2)
        shaded = i != 0  # 오른쪽 위 1조각만 흰색
        slots.append(
            PathSlot(
                id=f"slot.diagram.na_slice_{i}",
                prompt="",
                d=f"M {cx:.1f} {cy:.1f} L {x1:.1f} {y1:.1f} A {r:.1f} {r:.1f} 0 0 1 {x2:.1f} {y2:.1f} Z",
                fill="#d9ead3" if shaded else "#ffffff",
                stroke="#6aa84f",
                stroke_width=1.1,
            )
        )
    return slots


def build_problem_template() -> ProblemTemplate:
    stem_slot = TextBoxSlot(
        id="slot.stem.question",
        prompt="",
        text="전체에 대하여 색칠한 부분의 크기를 분수로 나타낼 때 다른 것을 찾아 기호를 쓰세요.",
        x=32,
        y=24,
        width=836,
        height=88,
        font_size=26,
        font_family='"Noto Sans KR", sans-serif',
        fill="#202124",
        align="left",
        valign="top",
        line_height=1.5,
    )

    box_outer = RectSlot(
        id="slot.diagram.box_outer",
        prompt="",
        x=70,
        y=124,
        width=760,
        height=174,
        fill="#ffffff",
        stroke="#7dd3fc",
        stroke_width=2.0,
    )

    ga_lbl = TextBoxSlot(id="slot.diagram.ga_lbl", prompt="", text="가", x=106, y=148, width=36, height=34, font_size=24, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center", valign="middle")
    ga_slots = _hex_6_slots(228.0, 210.0, 62.0)

    na_lbl = TextBoxSlot(id="slot.diagram.na_lbl", prompt="", text="나", x=366, y=148, width=36, height=34, font_size=24, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center", valign="middle")
    na_slots = _circle_6_slots(470.0, 210.0, 56.0)

    da_lbl = TextBoxSlot(id="slot.diagram.da_lbl", prompt="", text="다", x=596, y=148, width=36, height=34, font_size=24, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center", valign="middle")
    # 다: 4등분 직각삼각형 중 3조각 색칠
    da_t1 = PolygonSlot(id="slot.diagram.da_t1", prompt="", points=((656, 152), (714, 210), (656, 210)), fill="#fca5a5", stroke="#dc2626", stroke_width=1.1)
    da_t2 = PolygonSlot(id="slot.diagram.da_t2", prompt="", points=((656, 210), (714, 268), (656, 268)), fill="#fca5a5", stroke="#dc2626", stroke_width=1.1)
    da_t3 = PolygonSlot(id="slot.diagram.da_t3", prompt="", points=((714, 210), (772, 268), (714, 268)), fill="#fca5a5", stroke="#dc2626", stroke_width=1.1)
    da_t4 = PolygonSlot(id="slot.diagram.da_t4", prompt="", points=((656, 210), (714, 210), (714, 268)), fill="#ffffff", stroke="#dc2626", stroke_width=1.1)

    paren_left = TextBoxSlot(
        id="slot.answer.paren_left",
        prompt="",
        text="(",
        x=560,
        y=324,
        width=28,
        height=54,
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
        y=324,
        width=170,
        height=54,
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
        y=324,
        width=28,
        height=54,
        font_size=28,
        font_family='"Noto Sans KR", sans-serif',
        fill="#202124",
        align="center",
        valign="middle",
    )

    slots = (
        stem_slot,
        box_outer,
        ga_lbl, *ga_slots,
        na_lbl, *na_slots,
        da_lbl, da_t1, da_t2, da_t3, da_t4,
        paren_left,
        answer_input,
        paren_right,
    )

    return ProblemTemplate(
        id=PROBLEM_ID,
        title=PROBLEM_TITLE,
        canvas=Canvas(
            width=900,
            height=404,
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
