"""ModuMath Problem DSL: 동전 23원씩 2묶음 금액 구하기 (S3_초등_3_011981)"""

from __future__ import annotations

from modu_math.dsl import (
    Canvas,
    CircleSlot,
    ProblemTemplate,
    RectSlot,
    Region,
    TextBoxSlot,
)


PROBLEM_ID = "S3_초등_3_011981"
PROBLEM_TITLE = "동전 23원씩 2묶음의 전체 금액 구하기"


ANSWER = {
    "type": "short_answer",
    "value": 46,
    "unit": "원",
    "values": [46],
    "choices": [],
    "blanks": [
        {
            "id": "slot.answer.input",
            "slot_id": "slot.answer.input",
            "expected": 46,
        },
    ],
    "answer_key": [
        {
            "slot_id": "slot.answer.input",
            "value": 46,
            "diagnostics": [
                {
                    "id": "diag.multiplication_error",
                    "condition": "answer_not_equals_46",
                    "concept": "올림이 없는 (두 자리 수) × (한 자리 수)",
                    "reason": "23 × 2의 계산을 잘못함",
                    "feedback": "10원짜리 2개가 2묶음이므로 40원, 1원짜리 3개가 2묶음이므로 6원입니다. 모두 46원입니다.",
                },
            ],
        },
    ],
}


SEMANTIC = {
    "problem_id": PROBLEM_ID,
    "problem_type": "short_answer_multiplication_money",
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
            {"id": "quantity.amount_per_group", "type": "quantity", "label": "한 묶음의 금액", "value": 23, "unit": "원"},
            {"id": "quantity.groups", "type": "quantity", "label": "묶음 수", "value": 2, "unit": "묶음"},
            {"id": "quantity.total_amount", "type": "quantity", "label": "전체 금액", "value": 46, "unit": "원"},
        ],
        "relations": [
            {
                "id": "relation.multiplication",
                "type": "product_of",
                "multiplicand": "quantity.amount_per_group",
                "multiplier": "quantity.groups",
                "product": "quantity.total_amount",
            },
        ],
    },
    "answer": ANSWER,
}

SEMANTIC_OVERRIDE = SEMANTIC


def _coin_group_slots(group_idx: int, gx: float, gy: float) -> list[object]:
    slots: list[object] = [
        RectSlot(
            id=f"slot.diagram.group_{group_idx}_box",
            prompt="",
            x=gx,
            y=gy,
            width=230,
            height=154,
            fill="#ffffff",
            stroke="#a799c8",
            stroke_width=1.8,
        )
    ]
    # 10원 동전 2개
    for idx, dx in enumerate((76, 154), start=1):
        cx = gx + dx
        cy = gy + 46
        slots.append(
            CircleSlot(
                id=f"slot.diagram.group_{group_idx}_coin10_{idx}",
                prompt="",
                cx=cx,
                cy=cy,
                r=30.0,
                fill="#fed7aa",
                stroke="#9a3412",
                stroke_width=1.4,
            )
        )
        slots.append(
            TextBoxSlot(
                id=f"slot.diagram.group_{group_idx}_coin10_{idx}_label",
                prompt="",
                text="10",
                x=cx - 24,
                y=cy - 18,
                width=48,
                height=36,
                font_size=24,
                font_family='"Noto Sans KR", sans-serif',
                fill="#7c2d12",
                align="center",
                valign="middle",
            )
        )
    # 1원 동전 3개
    for idx, dx in enumerate((48, 115, 182), start=1):
        cx = gx + dx
        cy = gy + 114
        slots.append(
            CircleSlot(
                id=f"slot.diagram.group_{group_idx}_coin1_{idx}",
                prompt="",
                cx=cx,
                cy=cy,
                r=22.0,
                fill="#e5e7eb",
                stroke="#4b5563",
                stroke_width=1.4,
            )
        )
        slots.append(
            TextBoxSlot(
                id=f"slot.diagram.group_{group_idx}_coin1_{idx}_label",
                prompt="",
                text="1",
                x=cx - 18,
                y=cy - 15,
                width=36,
                height=30,
                font_size=20,
                font_family='"Noto Sans KR", sans-serif',
                fill="#1f2937",
                align="center",
                valign="middle",
            )
        )
    return slots


def build_problem_template() -> ProblemTemplate:
    stem_slot = TextBoxSlot(
        id="slot.stem.question",
        prompt="",
        text="동전이 23원씩 2묶음 있습니다. 모두 얼마일까요?",
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

    diagram_slots: list[object] = []
    diagram_slots.extend(_coin_group_slots(1, 190, 92))
    diagram_slots.extend(_coin_group_slots(2, 460, 92))

    paren_left = TextBoxSlot(
        id="slot.answer.paren_left",
        prompt="",
        text="(",
        x=560,
        y=276,
        width=26,
        height=54,
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
        y=276,
        width=110,
        height=54,
        fill="#ffffff",
        stroke="#111827",
        stroke_width=1.4,
        interaction={
            "type": "input",
            "role": "answer",
            "value_type": "integer",
            "max_length": 3,
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
        text="원",
        x=710,
        y=276,
        width=36,
        height=54,
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
        y=276,
        width=26,
        height=54,
        font_size=26,
        font_family='"Noto Sans KR", sans-serif',
        fill="#202124",
        align="center",
        valign="middle",
    )

    slots = (
        stem_slot,
        *diagram_slots,
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
