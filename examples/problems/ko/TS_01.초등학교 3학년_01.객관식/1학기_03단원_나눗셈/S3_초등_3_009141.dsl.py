"""ModuMath Problem DSL: 24 ÷ 4의 몫을 구할 때 필요한 곱셈식 선택하기 (S3_초등_3_009141)"""

from __future__ import annotations

from modu_math.dsl import (
    Canvas,
    ProblemTemplate,
    RectSlot,
    Region,
    TextBoxSlot,
    TextSlot,
)


PROBLEM_ID = "S3_초등_3_009141"
PROBLEM_TITLE = "24 ÷ 4의 몫을 구할 때 필요한 곱셈식 선택하기"

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
        {"id": "slot.choice.option_2", "slot_id": "slot.choice.option_2", "text": "㉢", "value": "㉢"},
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
    "problem_type": "multiple_choice_division_via_multiplication",
    "metadata": {
        "grade": 3,
        "semester": 1,
        "subject": "수학",
        "chapter": "03단원_나눗셈",
        "language": "ko-KR",
    },
    "domain": {
        "objects": [
            {"id": "expr.division", "type": "division", "dividend": 24, "divisor": 4},
            {"id": "expr.ga", "type": "multiplication", "label": "㉠", "equation": "3 × 8 = 24"},
            {"id": "expr.na", "type": "multiplication", "label": "㉡", "equation": "4 × 6 = 24"},
            {"id": "expr.da", "type": "multiplication", "label": "㉢", "equation": "4 × 7 = 28"},
        ],
        "relations": [
            {
                "id": "relation.inverse_multiplication",
                "type": "solves_division",
                "from_id": "expr.na",
                "to_id": "expr.division",
            }
        ],
    },
    "answer": ANSWER,
}


def build_problem_template() -> ProblemTemplate:
    stem_slot = TextBoxSlot(
        id="slot.stem.question",
        prompt="",
        text="96. 24 ÷ 4의 몫을 구할 때 필요한 곱셈식을 찾아 선택하세요.",
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
        x=110,
        y=76,
        width=740,
        height=76,
        fill="#ffffff",
        stroke="#f8b4a6",
        stroke_width=1.5,
    )

    opt_0 = TextSlot(
        id="slot.choice.option_0",
        prompt="",
        text="㉠ 3 × 8 = 24",
        x=245,
        y=114,
        font_size=22,
        font_family='"Noto Sans KR", sans-serif',
        fill="#111827",
        align="center",
        interaction={"type": "choice", "role": "answer", "choice_index": 0, "value": "㉠", "group_id": "slot.choice.group", "include_in_submission": True},
    )
    opt_1 = TextSlot(
        id="slot.choice.option_1",
        prompt="",
        text="㉡ 4 × 6 = 24",
        x=480,
        y=114,
        font_size=22,
        font_family='"Noto Sans KR", sans-serif',
        fill="#111827",
        align="center",
        interaction={"type": "choice", "role": "answer", "choice_index": 1, "value": "㉡", "group_id": "slot.choice.group", "include_in_submission": True},
    )
    opt_2 = TextSlot(
        id="slot.choice.option_2",
        prompt="",
        text="㉢ 4 × 7 = 28",
        x=715,
        y=114,
        font_size=22,
        font_family='"Noto Sans KR", sans-serif',
        fill="#111827",
        align="center",
        interaction={"type": "choice", "role": "answer", "choice_index": 2, "value": "㉢", "group_id": "slot.choice.group", "include_in_submission": True},
    )

    return ProblemTemplate(
        id=PROBLEM_ID,
        title=PROBLEM_TITLE,
        canvas=Canvas(width=886, height=180, coordinate_mode="logical"),
        regions=(
            Region(id="region.stem", role="stem", flow="absolute", slot_ids=("slot.stem.question",)),
            Region(id="region.diagram", role="diagram", flow="absolute", slot_ids=("slot.diagram.frame",)),
            Region(id="region.choices", role="choices", flow="absolute", slot_ids=("slot.choice.option_0", "slot.choice.option_1", "slot.choice.option_2")),
        ),
        slots=(stem_slot, frame_box, opt_0, opt_1, opt_2),
    )


PROBLEM_TEMPLATE = build_problem_template()

SOLVABLE = {
    "schema": "modu.solvable.v1.3",
    "problem_id": PROBLEM_ID,
    "given": [
        {"ref": "expr.division", "value": "24 ÷ 4"},
        {"ref": "expr.ga", "value": "3 × 8 = 24"},
        {"ref": "expr.na", "value": "4 × 6 = 24"},
        {"ref": "expr.da", "value": "4 × 7 = 28"},
    ],
    "target": {"ref": "slot.choice.option_1", "type": "choice"},
    "method": "division_via_multiplication_table",
    "steps": [
        {
            "id": "step.find_multiplication",
            "expr": "4 * 6 = 24",
            "value": "㉡",
            "explanation": "나누는 수가 4이므로 4의 단 곱셈구구에서 곱이 24인 식 4 × 6 = 24(㉡)를 찾습니다.",
        }
    ],
    "answer": ANSWER,
    "diagnostics": {
        "skills": ["division.multiplication_relation"],
        "errors": {
            "㉠": "division.wrong_multiplication_table",
            "㉢": "multiplication.wrong_product",
        },
    },
}
