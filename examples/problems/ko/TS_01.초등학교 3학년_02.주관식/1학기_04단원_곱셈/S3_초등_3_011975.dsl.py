"""ModuMath Problem DSL: 세발자전거 바퀴 수를 곱셈식으로 나타내기 (S3_초등_3_011975)"""

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


PROBLEM_ID = "S3_초등_3_011975"
PROBLEM_TITLE = "세발자전거 8대의 바퀴 수 곱셈식으로 나타내기"


ANSWER = {
    "type": "short_answer",
    "value": "3 × 8 = 24",
    "unit": "",
    "values": ["3 × 8 = 24", "3×8=24", "3 * 8 = 24"],
    "choices": [],
    "blanks": [
        {
            "id": "slot.answer.input",
            "slot_id": "slot.answer.input",
            "expected": "3 × 8 = 24",
        },
    ],
    "answer_key": [
        {
            "slot_id": "slot.answer.input",
            "value": "3 × 8 = 24",
            "diagnostics": [
                {
                    "id": "diag.wrong_wheels_per_tricycle",
                    "condition": "answer_not_equals_24",
                    "concept": "세발자전거의 바퀴 수",
                    "reason": "바퀴 수 3개 또는 대수 8대를 잘못 적용함",
                    "feedback": "세발자전거 1대에 바퀴가 3개씩 있고 모두 8대 있으므로 3 × 8 = 24입니다.",
                },
            ],
        },
    ],
}


SEMANTIC = {
    "problem_id": PROBLEM_ID,
    "problem_type": "short_answer_multiplication_modeling",
    "metadata": {
        "school": "초등학교",
        "grade": 3,
        "semester": 1,
        "chapter": "04단원_곱셈",
        "subject": "수학",
        "language": "ko-KR",
    },
    "domain": {
        "objects": [
            {"id": "quantity.wheels_per_tricycle", "type": "quantity", "label": "세발자전거 1대의 바퀴 수", "value": 3, "unit": "개"},
            {"id": "quantity.tricycles", "type": "quantity", "label": "세발자전거 수", "value": 8, "unit": "대"},
            {"id": "quantity.total_wheels", "type": "quantity", "label": "전체 바퀴 수", "value": 24, "unit": "개"},
        ],
        "relations": [
            {
                "id": "relation.multiplication",
                "type": "product_of",
                "multiplicand": "quantity.wheels_per_tricycle",
                "multiplier": "quantity.tricycles",
                "product": "quantity.total_wheels",
            },
        ],
    },
    "answer": ANSWER,
}

SEMANTIC_OVERRIDE = SEMANTIC


def _tricycle_slots(idx: int, cx: float, cy: float) -> list[object]:
    return [
        # 앞바퀴
        CircleSlot(
            id=f"slot.diagram.tri_{idx}_wheel_front",
            prompt="",
            cx=cx - 24,
            cy=cy + 18,
            r=16.0,
            fill="#ffffff",
            stroke="#111827",
            stroke_width=2.0,
        ),
        # 뒷바퀴 2개
        CircleSlot(
            id=f"slot.diagram.tri_{idx}_wheel_back1",
            prompt="",
            cx=cx + 14,
            cy=cy + 12,
            r=10.0,
            fill="#ffffff",
            stroke="#111827",
            stroke_width=1.8,
        ),
        CircleSlot(
            id=f"slot.diagram.tri_{idx}_wheel_back2",
            prompt="",
            cx=cx + 32,
            cy=cy + 20,
            r=10.0,
            fill="#ffffff",
            stroke="#111827",
            stroke_width=1.8,
        ),
        # 차체 프레임 & 핸들
        LineSlot(
            id=f"slot.diagram.tri_{idx}_frame_1",
            prompt="",
            x1=cx - 24,
            y1=cy + 18,
            x2=cx - 14,
            y2=cy - 24,
            stroke="#dc2626",
            stroke_width=3.2,
        ),
        LineSlot(
            id=f"slot.diagram.tri_{idx}_frame_2",
            prompt="",
            x1=cx - 16,
            y1=cy - 10,
            x2=cx + 22,
            y2=cy + 12,
            stroke="#dc2626",
            stroke_width=3.2,
        ),
        LineSlot(
            id=f"slot.diagram.tri_{idx}_handle",
            prompt="",
            x1=cx - 26,
            y1=cy - 24,
            x2=cx - 2,
            y2=cy - 24,
            stroke="#1e3a8a",
            stroke_width=3.0,
        ),
    ]


def build_problem_template() -> ProblemTemplate:
    stem_slot = TextBoxSlot(
        id="slot.stem.question",
        prompt="",
        text="세발자전거 8대가 있습니다. 바퀴는 모두 몇 개인지 곱셈식으로 나타내세요.",
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
        height=248,
        fill="#ffffff",
        stroke="#a799c8",
        stroke_width=2.0,
    )

    tri_slots: list[object] = []
    for idx in range(8):
        r = idx // 4
        c = idx % 4
        tri_slots.extend(_tricycle_slots(idx + 1, 170 + c * 182, 148 + r * 114))

    paren_left = TextBoxSlot(
        id="slot.answer.paren_left",
        prompt="",
        text="(",
        x=480,
        y=356,
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
        y=356,
        width=250,
        height=54,
        fill="#ffffff",
        stroke="#111827",
        stroke_width=1.4,
        interaction={
            "type": "input",
            "role": "answer",
            "value_type": "text",
            "max_length": 16,
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
        y=356,
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
        *tri_slots,
        paren_left,
        answer_input,
        paren_right,
    )

    return ProblemTemplate(
        id=PROBLEM_ID,
        title=PROBLEM_TITLE,
        canvas=Canvas(
            width=900,
            height=436,
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
