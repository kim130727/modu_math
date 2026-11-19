"""ModuMath Problem DSL: 계산이 옳은 곱셈식 찾기 (S3_초등_3_009158)"""

from __future__ import annotations

from modu_math.dsl import (
    Canvas,
    ProblemTemplate,
    RectSlot,
    Region,
    TextBoxSlot,
    TextSlot,
)


PROBLEM_ID = "S3_초등_3_009158"
PROBLEM_TITLE = "계산이 옳은 곱셈식 기호 선택하기"

ANSWER = {
    "type": "choice",
    "value": "㉡",
    "unit": "",
    "answer_index": 1,
    "values": ["㉡"],
    "blanks": [],
    "choices": [
        {"id": "slot.choice.option_0", "slot_id": "slot.choice.option_0", "text": "㉠", "value": "㉠"},
        {"id": "slot.choice.option_1", "slot_id": "slot.choice.option_1", "text": "㉡", "value": "㉡"},
    ],
    "answer_key": [
        {
            "slot_id": "slot.choice.option_1",
            "value": "㉡",
        }
    ],
}

SEMANTIC_OVERRIDE = {
    "problem_id": PROBLEM_ID,
    "problem_type": "multiple_choice_multiplication_verification",
    "metadata": {
        "grade": 3,
        "semester": 1,
        "subject": "수학",
        "chapter": "04단원_곱셈",
        "language": "ko-KR",
    },
    "domain": {
        "objects": [
            {"id": "expr.ga", "type": "multiplication_claim", "label": "㉠", "lhs": "29 × 5", "claimed_rhs": 105, "actual_rhs": 145, "is_correct": False},
            {"id": "expr.na", "type": "multiplication_claim", "label": "㉡", "lhs": "48 × 4", "claimed_rhs": 192, "actual_rhs": 192, "is_correct": True},
        ],
        "relations": [
            {
                "id": "relation.correct_equation",
                "type": "is_valid_calculation",
                "from_id": "expr.na",
                "to_id": "concept.true_equation",
            }
        ],
    },
    "answer": ANSWER,
}


def build_problem_template() -> ProblemTemplate:
    stem_slot = TextBoxSlot(
        id="slot.stem.question",
        prompt="",
        text="18. 계산이 옳은 것을 찾아 기호를 선택하세요.",
        x=32,
        y=22,
        width=820,
        height=44,
        font_size=24,
        font_family='"Noto Sans KR", sans-serif',
        fill="#202124",
        align="left",
        valign="top",
        line_height=1.5,
    )

    frame_box = RectSlot(
        id="slot.diagram.frame",
        prompt="",
        x=380,
        y=76,
        width=480,
        height=110,
        fill="#ffffff",
        stroke="#f59e0b",
        stroke_width=1.8,
    )
    item_ga = TextSlot(
        id="slot.diagram.item_ga",
        prompt="",
        text="㉠ 29 × 5 = 105",
        x=620,
        y=108,
        font_size=24,
        font_family='"Noto Sans KR", sans-serif',
        fill="#111827",
        align="center",
    )
    item_na = TextSlot(
        id="slot.diagram.item_na",
        prompt="",
        text="㉡ 48 × 4 = 192",
        x=620,
        y=152,
        font_size=24,
        font_family='"Noto Sans KR", sans-serif',
        fill="#111827",
        align="center",
    )

    paren_l = TextSlot(id="slot.choice.paren_l", prompt="", text="(", x=545, y=220, font_size=24, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center")
    opt_0 = TextSlot(
        id="slot.choice.option_0",
        prompt="",
        text="㉠",
        x=585,
        y=220,
        font_size=22,
        font_family='"Noto Sans KR", sans-serif',
        fill="#111827",
        align="center",
        interaction={"type": "choice", "role": "answer", "choice_index": 0, "value": "㉠", "group_id": "slot.choice.group", "include_in_submission": True},
    )
    comma_1 = TextSlot(id="slot.choice.comma_1", prompt="", text=",", x=620, y=220, font_size=22, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center")
    opt_1 = TextSlot(
        id="slot.choice.option_1",
        prompt="",
        text="㉡",
        x=655,
        y=220,
        font_size=22,
        font_family='"Noto Sans KR", sans-serif',
        fill="#111827",
        align="center",
        interaction={"type": "choice", "role": "answer", "choice_index": 1, "value": "㉡", "group_id": "slot.choice.group", "include_in_submission": True},
    )
    paren_r = TextSlot(id="slot.choice.paren_r", prompt="", text=")", x=695, y=220, font_size=24, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center")

    return ProblemTemplate(
        id=PROBLEM_ID,
        title=PROBLEM_TITLE,
        canvas=Canvas(width=886, height=260, coordinate_mode="logical"),
        regions=(
            Region(id="region.stem", role="stem", flow="absolute", slot_ids=("slot.stem.question",)),
            Region(id="region.diagram", role="diagram", flow="absolute", slot_ids=("slot.diagram.frame", "slot.diagram.item_ga", "slot.diagram.item_na")),
            Region(
                id="region.choices",
                role="choices",
                flow="absolute",
                slot_ids=("slot.choice.paren_l", "slot.choice.option_0", "slot.choice.comma_1", "slot.choice.option_1", "slot.choice.paren_r"),
            ),
        ),
        slots=(stem_slot, frame_box, item_ga, item_na, paren_l, opt_0, comma_1, opt_1, paren_r),
    )


PROBLEM_TEMPLATE = build_problem_template()

SOLVABLE = {
    "schema": "modu.solvable.v1.3",
    "problem_id": PROBLEM_ID,
    "given": [
        {"ref": "expr.ga", "value": "29 × 5 = 105"},
        {"ref": "expr.na", "value": "48 × 4 = 192"},
    ],
    "target": {"ref": "slot.choice.option_1", "type": "choice"},
    "method": "verify_two_digit_multiplication",
    "steps": [
        {"id": "step.check_ga", "expr": "29 * 5", "value": 145, "explanation": "29 × 5 = 145이므로 ㉠(105)은 틀렸습니다."},
        {"id": "step.check_na", "expr": "48 * 4", "value": 192, "explanation": "48 × 4 = 192이므로 계산이 옳은 것은 ㉡입니다."},
    ],
    "answer": ANSWER,
    "diagnostics": {
        "skills": ["multiplication.two_by_one_with_carry"],
        "errors": {
            "㉠": "multiplication.carry_omission",
        },
    },
}
