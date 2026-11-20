"""ModuMath Problem DSL: 똑같이 나누어진 피자 모두 찾기 (S3_초등_3_012092)"""

from __future__ import annotations

import math

from modu_math.dsl import (
    Canvas,
    CircleSlot,
    LineSlot,
    ProblemTemplate,
    RectSlot,
    Region,
    TextBoxSlot,
)


PROBLEM_ID = "S3_초등_3_012092"
PROBLEM_TITLE = "똑같이 나누어진 피자 모두 찾기"


ANSWER = {
    "type": "short_answer",
    "value": "ㄱ, ㄴ, ㅁ, ㅂ",
    "unit": "",
    "values": ["ㄱ, ㄴ, ㅁ, ㅂ", "㉠, ㉡, ㉤, ㉥"],
    "choices": [],
    "blanks": [
        {
            "id": "slot.answer.input",
            "slot_id": "slot.answer.input",
            "expected": "ㄱ, ㄴ, ㅁ, ㅂ",
        },
    ],
    "answer_key": [
        {
            "slot_id": "slot.answer.input",
            "value": "ㄱ, ㄴ, ㅁ, ㅂ",
            "diagnostics": [
                {
                    "id": "diag.included_unequal_pizza",
                    "condition": "answer_contains_d_or_r",
                    "concept": "똑같이 나누기",
                    "reason": "모양이나 크기가 다르게 나누어진 ㄷ 또는 ㄹ을 포함함",
                    "feedback": "ㄷ은 마주 보는 두 쌍의 삼각형 모양이 서로 다르고, ㄹ은 가운데와 가장자리 조각의 모양과 크기가 다릅니다.",
                },
            ],
        },
    ],
}


SEMANTIC = {
    "problem_id": PROBLEM_ID,
    "problem_type": "short_answer_fraction_equal_division",
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
            {"id": "pizza.g", "type": "pizza", "label": "ㄱ", "equal_parts": True},
            {"id": "pizza.n", "type": "pizza", "label": "ㄴ", "equal_parts": True},
            {"id": "pizza.d", "type": "pizza", "label": "ㄷ", "equal_parts": False},
            {"id": "pizza.r", "type": "pizza", "label": "ㄹ", "equal_parts": False},
            {"id": "pizza.m", "type": "pizza", "label": "ㅁ", "equal_parts": True},
            {"id": "pizza.b", "type": "pizza", "label": "ㅂ", "equal_parts": True},
        ],
        "relations": [
            {
                "id": "relation.equal_pizzas",
                "type": "equally_divided",
                "items": ["pizza.g", "pizza.n", "pizza.m", "pizza.b"],
            },
        ],
    },
    "answer": ANSWER,
}

SEMANTIC_OVERRIDE = SEMANTIC


def _rect_pizza(prefix: str, x: float, y: float, w: float, h: float) -> list[RectSlot]:
    return [
        RectSlot(id=f"slot.diagram.{prefix}_crust", prompt="", x=x, y=y, width=w, height=h, fill="#eab308", stroke="#78350f", stroke_width=1.3),
        RectSlot(id=f"slot.diagram.{prefix}_cheese", prompt="", x=x + 7, y=y + 7, width=w - 14, height=h - 14, fill="#fef08a", stroke="#ca8a04", stroke_width=1.0),
    ]


def _round_pizza(prefix: str, cx: float, cy: float, r: float) -> list[CircleSlot]:
    return [
        CircleSlot(id=f"slot.diagram.{prefix}_crust", prompt="", cx=cx, cy=cy, r=r, fill="#eab308", stroke="#78350f", stroke_width=1.3),
        CircleSlot(id=f"slot.diagram.{prefix}_cheese", prompt="", cx=cx, cy=cy, r=r - 6, fill="#fef08a", stroke="#ca8a04", stroke_width=1.0),
    ]


def build_problem_template() -> ProblemTemplate:
    stem_slot = TextBoxSlot(
        id="slot.stem.question",
        prompt="",
        text="똑같이 나누어진 피자를 모두 찾아보세요.",
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

    box_outer = RectSlot(
        id="slot.diagram.box_outer",
        prompt="",
        x=48,
        y=84,
        width=804,
        height=230,
        fill="#ffffff",
        stroke="#f3c6b6",
        stroke_width=2.0,
    )

    # 1행: ㄱ, ㄴ, ㄷ (사각 피자)
    lbl_g = TextBoxSlot(id="slot.diagram.lbl_g", prompt="", text="㉠", x=76, y=102, width=32, height=30, font_size=22, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center", valign="middle")
    pz_g = _rect_pizza("g", 116, 108, 120, 76)
    g_c1 = LineSlot(id="slot.diagram.g_c1", prompt="", x1=156, y1=108, x2=156, y2=184, stroke="#dc2626", stroke_width=1.6)
    g_c2 = LineSlot(id="slot.diagram.g_c2", prompt="", x1=196, y1=108, x2=196, y2=184, stroke="#dc2626", stroke_width=1.6)

    lbl_n = TextBoxSlot(id="slot.diagram.lbl_n", prompt="", text="㉡", x=316, y=102, width=32, height=30, font_size=22, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center", valign="middle")
    pz_n = _rect_pizza("n", 356, 108, 120, 76)
    n_c1 = LineSlot(id="slot.diagram.n_c1", prompt="", x1=416, y1=108, x2=416, y2=184, stroke="#dc2626", stroke_width=1.6)
    n_c2 = LineSlot(id="slot.diagram.n_c2", prompt="", x1=356, y1=146, x2=476, y2=146, stroke="#dc2626", stroke_width=1.6)

    lbl_d = TextBoxSlot(id="slot.diagram.lbl_d", prompt="", text="㉢", x=556, y=102, width=32, height=30, font_size=22, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center", valign="middle")
    pz_d = _rect_pizza("d", 596, 108, 120, 76)
    d_c1 = LineSlot(id="slot.diagram.d_c1", prompt="", x1=596, y1=108, x2=716, y2=184, stroke="#dc2626", stroke_width=1.6)
    d_c2 = LineSlot(id="slot.diagram.d_c2", prompt="", x1=716, y1=108, x2=596, y2=184, stroke="#dc2626", stroke_width=1.6)

    # 2행: ㄹ, ㅁ, ㅂ (원형 피자)
    lbl_r = TextBoxSlot(id="slot.diagram.lbl_r", prompt="", text="㉣", x=76, y=206, width=32, height=30, font_size=22, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center", valign="middle")
    pz_r = _round_pizza("r", 176.0, 252.0, 44.0)
    r_c1 = LineSlot(id="slot.diagram.r_c1", prompt="", x1=176, y1=208, x2=138, y2=274, stroke="#dc2626", stroke_width=1.6)
    r_c2 = LineSlot(id="slot.diagram.r_c2", prompt="", x1=176, y1=208, x2=214, y2=274, stroke="#dc2626", stroke_width=1.6)
    r_c3 = LineSlot(id="slot.diagram.r_c3", prompt="", x1=138, y1=274, x2=214, y2=274, stroke="#dc2626", stroke_width=1.6)

    lbl_m = TextBoxSlot(id="slot.diagram.lbl_m", prompt="", text="㉤", x=316, y=206, width=32, height=30, font_size=22, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center", valign="middle")
    pz_m = _round_pizza("m", 416.0, 252.0, 44.0)
    m_cuts: list[LineSlot] = []
    for k in range(3):
        ang = math.radians(k * 60 + 90)
        dx, dy = 44 * math.cos(ang), 44 * math.sin(ang)
        m_cuts.append(
            LineSlot(
                id=f"slot.diagram.m_c{k}",
                prompt="",
                x1=round(416 - dx, 1),
                y1=round(252 - dy, 1),
                x2=round(416 + dx, 1),
                y2=round(252 + dy, 1),
                stroke="#dc2626",
                stroke_width=1.6,
            )
        )

    lbl_b = TextBoxSlot(id="slot.diagram.lbl_b", prompt="", text="㉥", x=556, y=206, width=32, height=30, font_size=22, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center", valign="middle")
    pz_b = _round_pizza("b", 656.0, 252.0, 44.0)
    b_cuts: list[LineSlot] = []
    for k in range(5):
        ang = math.radians(k * 72 - 90)
        b_cuts.append(
            LineSlot(
                id=f"slot.diagram.b_c{k}",
                prompt="",
                x1=656.0,
                y1=252.0,
                x2=round(656 + 44 * math.cos(ang), 1),
                y2=round(252 + 44 * math.sin(ang), 1),
                stroke="#dc2626",
                stroke_width=1.6,
            )
        )

    paren_left = TextBoxSlot(
        id="slot.answer.paren_left",
        prompt="",
        text="(",
        x=480,
        y=340,
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
        x=514,
        y=340,
        width=250,
        height=54,
        fill="#ffffff",
        stroke="#111827",
        stroke_width=1.4,
        interaction={
            "type": "input",
            "role": "answer",
            "value_type": "text",
            "max_length": 20,
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
        y=340,
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
        lbl_g, *pz_g, g_c1, g_c2,
        lbl_n, *pz_n, n_c1, n_c2,
        lbl_d, *pz_d, d_c1, d_c2,
        lbl_r, *pz_r, r_c1, r_c2, r_c3,
        lbl_m, *pz_m, *m_cuts,
        lbl_b, *pz_b, *b_cuts,
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
