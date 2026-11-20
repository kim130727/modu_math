"""ModuMath Problem DSL: 빵 36개를 6개씩 나누어 주기 (S3_초등_3_011968)"""

from __future__ import annotations

from modu_math.dsl import (
    Canvas,
    ProblemTemplate,
    RectSlot,
    Region,
    TextBoxSlot,
)


PROBLEM_ID = "S3_초등_3_011968"
PROBLEM_TITLE = "빵 36개를 6개씩 나누어 줄 사람 수 구하기"


ANSWER = {
    "type": "short_answer",
    "value": 6,
    "unit": "명",
    "values": [6],
    "choices": [],
    "blanks": [
        {
            "id": "slot.answer.input",
            "slot_id": "slot.answer.input",
            "expected": 6,
        },
    ],
    "answer_key": [
        {
            "slot_id": "slot.answer.input",
            "value": 6,
            "diagnostics": [
                {
                    "id": "diag.division_error",
                    "condition": "answer_not_equals_6",
                    "concept": "같은 수로 묶어 나누기",
                    "reason": "6개씩 묶인 묶음의 수를 잘못 구함",
                    "feedback": "빵 36개를 6개씩 묶은 상자가 모두 몇 묶음인지 세어 보세요. 36 ÷ 6 = 6입니다.",
                },
            ],
        },
    ],
}


SEMANTIC = {
    "problem_id": PROBLEM_ID,
    "problem_type": "short_answer_division_grouping",
    "metadata": {
        "school": "초등학교",
        "grade": 3,
        "semester": 1,
        "chapter": "03단원_나눗셈",
        "subject": "수학",
        "language": "ko-KR",
    },
    "domain": {
        "objects": [
            {"id": "quantity.total_breads", "type": "quantity", "label": "전체 빵 수", "value": 36, "unit": "개"},
            {"id": "quantity.breads_per_person", "type": "quantity", "label": "한 사람에게 줄 빵 수", "value": 6, "unit": "개"},
            {"id": "quantity.people", "type": "quantity", "label": "나누어 줄 수 있는 사람 수", "value": 6, "unit": "명"},
        ],
        "relations": [
            {
                "id": "relation.division",
                "type": "quotient_of",
                "dividend": "quantity.total_breads",
                "divisor": "quantity.breads_per_person",
                "quotient": "quantity.people",
            },
        ],
    },
    "answer": ANSWER,
}

SEMANTIC_OVERRIDE = SEMANTIC


def _build_bread_group_slots(group_idx: int, gx: float, gy: float) -> list[RectSlot]:
    slots: list[RectSlot] = [
        RectSlot(
            id=f"slot.diagram.group_{group_idx}_box",
            prompt="",
            x=gx,
            y=gy,
            width=210,
            height=110,
            fill="#ffffff",
            stroke="#86c57a",
            stroke_width=1.8,
        )
    ]
    for row in range(2):
        for col in range(3):
            bx = gx + 18 + col * 62
            by = gy + 16 + row * 46
            slots.append(
                RectSlot(
                    id=f"slot.diagram.group_{group_idx}_bread_{row}_{col}_body",
                    prompt="",
                    x=bx,
                    y=by + 10,
                    width=48,
                    height=22,
                    fill="#fef3c7",
                    stroke="#4b5563",
                    stroke_width=1.1,
                )
            )
            slots.append(
                RectSlot(
                    id=f"slot.diagram.group_{group_idx}_bread_{row}_{col}_top",
                    prompt="",
                    x=bx + 2,
                    y=by,
                    width=44,
                    height=12,
                    fill="#f59e0b",
                    stroke="#4b5563",
                    stroke_width=1.1,
                )
            )
    return slots


def build_problem_template() -> ProblemTemplate:
    stem_slot = TextBoxSlot(
        id="slot.stem.question",
        prompt="",
        text="빵 36개를 한 사람에게 6개씩 나누어 주려고 합니다. 모두 몇 명에게 나누어 줄 수 있을까요?",
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

    diagram_slots: list[RectSlot] = []
    for idx in range(6):
        r = idx // 3
        c = idx % 3
        diagram_slots.extend(_build_bread_group_slots(idx + 1, 95 + c * 250, 124 + r * 130))

    paren_left = TextBoxSlot(
        id="slot.answer.paren_left",
        prompt="",
        text="(",
        x=560,
        y=400,
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
        y=400,
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
        text="명",
        x=710,
        y=400,
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
        y=400,
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
