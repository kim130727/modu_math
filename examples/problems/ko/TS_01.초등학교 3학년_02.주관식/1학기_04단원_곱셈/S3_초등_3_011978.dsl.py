"""ModuMath Problem DSL: 수 모형을 곱셈식으로 나타내고 계산하기 (S3_초등_3_011978)"""

from __future__ import annotations

from modu_math.dsl import (
    Canvas,
    ProblemTemplate,
    RectSlot,
    Region,
    TextBoxSlot,
)


PROBLEM_ID = "S3_초등_3_011978"
PROBLEM_TITLE = "수 모형을 곱셈식으로 나타내고 계산하기"


ANSWER = {
    "type": "short_answer",
    "value": "30 × 3 = 90",
    "unit": "",
    "values": ["30 × 3 = 90", "30×3=90", "30 * 3 = 90"],
    "choices": [],
    "blanks": [
        {
            "id": "slot.answer.input",
            "slot_id": "slot.answer.input",
            "expected": "30 × 3 = 90",
        },
    ],
    "answer_key": [
        {
            "slot_id": "slot.answer.input",
            "value": "30 × 3 = 90",
            "diagnostics": [
                {
                    "id": "diag.wrote_tens_count_expression",
                    "condition": "answer_equals_3_times_3",
                    "concept": "몇십 곱하기 몇",
                    "reason": "십 모형 3개를 3으로 보고 3 × 3 = 9로 씀",
                    "feedback": "한 묶음은 30을 나타내므로 30개씩 3묶음을 나타내는 식 30 × 3 = 90으로 써 보세요.",
                },
            ],
        },
    ],
}


SEMANTIC = {
    "problem_id": PROBLEM_ID,
    "problem_type": "short_answer_multiplication_base_ten_blocks",
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
            {"id": "quantity.ones_per_group", "type": "quantity", "label": "한 묶음의 수", "value": 30},
            {"id": "quantity.groups", "type": "quantity", "label": "묶음 수", "value": 3},
            {"id": "quantity.total_value", "type": "quantity", "label": "전체 값", "value": 90},
        ],
        "relations": [
            {
                "id": "relation.multiplication",
                "type": "product_of",
                "multiplicand": "quantity.ones_per_group",
                "multiplier": "quantity.groups",
                "product": "quantity.total_value",
            },
        ],
    },
    "answer": ANSWER,
}

SEMANTIC_OVERRIDE = SEMANTIC


def _ten_rods_group(group_idx: int, gx: float, gy: float) -> list[RectSlot]:
    slots: list[RectSlot] = [
        RectSlot(
            id=f"slot.diagram.group_{group_idx}_box",
            prompt="",
            x=gx,
            y=gy,
            width=190,
            height=188,
            fill="#ffffff",
            stroke="#ec4899",
            stroke_width=1.6,
        )
    ]
    for rod in range(3):
        rx = gx + 24 + rod * 56
        for cell in range(10):
            ry = gy + 14 + cell * 16
            slots.append(
                RectSlot(
                    id=f"slot.diagram.group_{group_idx}_rod_{rod}_cell_{cell}",
                    prompt="",
                    x=rx,
                    y=ry,
                    width=24,
                    height=16,
                    fill="#e0f2fe",
                    stroke="#0284c7",
                    stroke_width=1.0,
                )
            )
    return slots


def build_problem_template() -> ProblemTemplate:
    stem_slot = TextBoxSlot(
        id="slot.stem.question",
        prompt="",
        text="수 모형을 보고 물음에 답하세요.",
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
        x=110,
        y=78,
        width=680,
        height=216,
        fill="#ffffff",
        stroke="#f472b6",
        stroke_width=2.0,
    )

    rod_slots: list[RectSlot] = []
    for idx in range(3):
        rod_slots.extend(_ten_rods_group(idx + 1, 135 + idx * 220, 92))

    subquestion_slot = TextBoxSlot(
        id="slot.stem.subquestion",
        prompt="",
        text="(3) 위 그림에 있는 수 모형을 곱셈식으로 나타내고 계산하세요.",
        x=48,
        y=316,
        width=820,
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
        x=480,
        y=372,
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
        y=372,
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
        y=372,
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
        *rod_slots,
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
            height=452,
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
