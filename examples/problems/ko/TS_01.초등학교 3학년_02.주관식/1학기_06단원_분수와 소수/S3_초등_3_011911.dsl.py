"""ModuMath Problem DSL: 2/5를 나타내는 도형 찾아 기호 쓰기 (S3_초등_3_011911)"""

from __future__ import annotations

import math

from modu_math.dsl import (
    Canvas,
    LineSlot,
    PathSlot,
    PolygonSlot,
    ProblemTemplate,
    RectSlot,
    Region,
    TextBoxSlot,
)


PROBLEM_ID = "S3_초등_3_011911"
PROBLEM_TITLE = "분수 2/5를 나타내는 그림 찾기"


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
                    "id": "diag.unequal_parts_confusion",
                    "condition": "answer_not_equals_da",
                    "concept": "분수의 의미 (전체와 부분)",
                    "reason": "전체를 똑같이 5로 나눈 것 중의 2를 찾지 못함",
                    "feedback": "전체를 똑같이 5조각으로 나눈 뒤 그중 2조각을 색칠한 그림은 원 모양인 '다'입니다.",
                },
            ],
        },
    ],
}


SEMANTIC = {
    "problem_id": PROBLEM_ID,
    "problem_type": "short_answer_fraction_representation",
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
            {"id": "figure.ga", "type": "fraction_model", "label": "가", "total_parts": 8, "shaded_parts": 2, "equal_parts": True},
            {"id": "figure.na", "type": "fraction_model", "label": "나", "total_parts": 9, "shaded_parts": 2, "equal_parts": True},
            {"id": "figure.da", "type": "fraction_model", "label": "다", "total_parts": 5, "shaded_parts": 2, "equal_parts": True},
            {"id": "figure.ra", "type": "fraction_model", "label": "라", "total_parts": 3, "shaded_parts": 3, "equal_parts": True},
            {"id": "figure.ma", "type": "fraction_model", "label": "마", "total_parts": 3, "shaded_parts": 2, "equal_parts": False},
            {"id": "figure.ba", "type": "fraction_model", "label": "바", "total_parts": 7, "shaded_parts": 3, "equal_parts": True},
        ],
        "relations": [
            {
                "id": "relation.represents_two_fifths",
                "type": "represents_fraction",
                "from_id": "figure.da",
                "fraction": "2/5",
            },
        ],
    },
    "answer": ANSWER,
}

SEMANTIC_OVERRIDE = SEMANTIC


def _pie_5_slots(cx: float, cy: float, r: float) -> list[object]:
    slots: list[object] = []
    # 5등분 원: 위쪽(-90도) 기준 대칭으로 2조각 색칠 (인덱스 0, 4)
    start_deg = -126.0
    for i in range(5):
        a1 = math.radians(start_deg + i * 72.0)
        a2 = math.radians(start_deg + (i + 1) * 72.0)
        x1, y1 = cx + r * math.cos(a1), cy + r * math.sin(a1)
        x2, y2 = cx + r * math.cos(a2), cy + r * math.sin(a2)
        shaded = i in (0, 1)
        slots.append(
            PathSlot(
                id=f"slot.diagram.da_slice_{i}",
                prompt="",
                d=f"M {cx:.1f} {cy:.1f} L {x1:.1f} {y1:.1f} A {r:.1f} {r:.1f} 0 0 1 {x2:.1f} {y2:.1f} Z",
                fill="#d1d5db" if shaded else "#ffffff",
                stroke="#6b7280",
                stroke_width=1.2,
            )
        )
    return slots


def build_problem_template() -> ProblemTemplate:
    stem_slot = TextBoxSlot(
        id="slot.stem.question",
        prompt="",
        text="그림을 보고 물음에 답하세요.",
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
        y=76,
        width=760,
        height=248,
        fill="#ffffff",
        stroke="#9ca3af",
        stroke_width=1.8,
    )

    # 가: 8등분 직사각형 중 위쪽 2개 직각삼각형 색칠
    ga_lbl = TextBoxSlot(id="slot.diagram.ga_lbl", prompt="", text="가", x=104, y=94, width=32, height=30, font_size=22, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center", valign="middle")
    ga_rect = RectSlot(id="slot.diagram.ga_rect", prompt="", x=150, y=98, width=136, height=84, fill="#ffffff", stroke="#6b7280", stroke_width=1.3)
    ga_s1 = PolygonSlot(id="slot.diagram.ga_s1", prompt="", points=((150, 140), (218, 98), (218, 140)), fill="#d1d5db", stroke="#6b7280", stroke_width=1.0)
    ga_s2 = PolygonSlot(id="slot.diagram.ga_s2", prompt="", points=((218, 140), (286, 98), (286, 140)), fill="#d1d5db", stroke="#6b7280", stroke_width=1.0)
    ga_l1 = LineSlot(id="slot.diagram.ga_l1", prompt="", x1=218, y1=98, x2=218, y2=182, stroke="#6b7280", stroke_width=1.0, stroke_dasharray="3 3")
    ga_l2 = LineSlot(id="slot.diagram.ga_l2", prompt="", x1=150, y1=140, x2=286, y2=140, stroke="#6b7280", stroke_width=1.0, stroke_dasharray="3 3")
    ga_l3 = LineSlot(id="slot.diagram.ga_l3", prompt="", x1=150, y1=140, x2=218, y2=182, stroke="#6b7280", stroke_width=1.0, stroke_dasharray="3 3")
    ga_l4 = LineSlot(id="slot.diagram.ga_l4", prompt="", x1=218, y1=140, x2=286, y2=182, stroke="#6b7280", stroke_width=1.0, stroke_dasharray="3 3")

    # 나: 9등분 정삼각형 중 왼쪽 아래 2개 색칠
    na_lbl = TextBoxSlot(id="slot.diagram.na_lbl", prompt="", text="나", x=336, y=94, width=32, height=30, font_size=22, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center", valign="middle")
    na_tri = PolygonSlot(id="slot.diagram.na_tri", prompt="", points=((445, 92), (508, 190), (382, 190)), fill="#ffffff", stroke="#9ca3af", stroke_width=1.2)
    na_s1 = PolygonSlot(id="slot.diagram.na_s1", prompt="", points=((403, 157), (424, 190), (382, 190)), fill="#e5e7eb", stroke="#9ca3af", stroke_width=0.8)
    na_s2 = PolygonSlot(id="slot.diagram.na_s2", prompt="", points=((403, 157), (445, 157), (424, 190)), fill="#e5e7eb", stroke="#9ca3af", stroke_width=0.8)

    # 다: 5등분 원 중 2조각 색칠
    da_lbl = TextBoxSlot(id="slot.diagram.da_lbl", prompt="", text="다", x=566, y=94, width=32, height=30, font_size=22, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center", valign="middle")
    da_slots = _pie_5_slots(680.0, 142.0, 48.0)

    # 라: 정육면체
    ra_lbl = TextBoxSlot(id="slot.diagram.ra_lbl", prompt="", text="라", x=104, y=214, width=32, height=30, font_size=22, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center", valign="middle")
    ra_hex = PolygonSlot(id="slot.diagram.ra_hex", prompt="", points=((218, 206), (266, 232), (266, 286), (218, 312), (170, 286), (170, 232)), fill="#e5e7eb", stroke="#6b7280", stroke_width=1.3)
    ra_l1 = LineSlot(id="slot.diagram.ra_l1", prompt="", x1=218, y1=258, x2=170, y2=232, stroke="#6b7280", stroke_width=1.2, stroke_dasharray="3 3")
    ra_l2 = LineSlot(id="slot.diagram.ra_l2", prompt="", x1=218, y1=258, x2=266, y2=232, stroke="#6b7280", stroke_width=1.2, stroke_dasharray="3 3")
    ra_l3 = LineSlot(id="slot.diagram.ra_l3", prompt="", x1=218, y1=258, x2=218, y2=312, stroke="#6b7280", stroke_width=1.2, stroke_dasharray="3 3")

    # 마: 역삼각형 3분할 중 양쪽 2조각 색칠
    ma_lbl = TextBoxSlot(id="slot.diagram.ma_lbl", prompt="", text="마", x=336, y=214, width=32, height=30, font_size=22, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center", valign="middle")
    ma_tri = PolygonSlot(id="slot.diagram.ma_tri", prompt="", points=((388, 214), (502, 214), (445, 306)), fill="#ffffff", stroke="#9ca3af", stroke_width=1.2)
    ma_s1 = PolygonSlot(id="slot.diagram.ma_s1", prompt="", points=((388, 214), (422, 214), (422, 268)), fill="#e5e7eb", stroke="#9ca3af", stroke_width=1.0)
    ma_s2 = PolygonSlot(id="slot.diagram.ma_s2", prompt="", points=((468, 214), (502, 214), (468, 268)), fill="#e5e7eb", stroke="#9ca3af", stroke_width=1.0)

    # 바: ㄷ자 7칸 중 3칸 색칠
    ba_lbl = TextBoxSlot(id="slot.diagram.ba_lbl", prompt="", text="바", x=566, y=214, width=32, height=30, font_size=22, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center", valign="middle")
    ba_cells = [
        (0, 0, False), (1, 0, False), (2, 0, True),
        (0, 1, False), (1, 1, True),
        (0, 2, False), (1, 2, False), (2, 2, True),
    ]
    ba_slots: list[RectSlot] = []
    for col, row, shaded in ba_cells:
        ba_slots.append(
            RectSlot(
                id=f"slot.diagram.ba_cell_{row}_{col}",
                prompt="",
                x=628 + col * 32,
                y=210 + row * 32,
                width=32,
                height=32,
                fill="#d1d5db" if shaded else "#ffffff",
                stroke="#6b7280",
                stroke_width=1.1,
            )
        )

    subquestion_slot = TextBoxSlot(
        id="slot.stem.subquestion",
        prompt="",
        text="2/5를 나타내는 것을 찾아 기호를 쓰세요.",
        x=48,
        y=344,
        width=760,
        height=40,
        font_size=25,
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
        y=394,
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
        y=394,
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
        y=394,
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
        ga_lbl, ga_rect, ga_s1, ga_s2, ga_l1, ga_l2, ga_l3, ga_l4,
        na_lbl, na_tri, na_s1, na_s2,
        da_lbl, *da_slots,
        ra_lbl, ra_hex, ra_l1, ra_l2, ra_l3,
        ma_lbl, ma_tri, ma_s1, ma_s2,
        ba_lbl, *ba_slots,
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
            height=470,
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
