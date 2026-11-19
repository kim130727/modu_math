"""ModuMath Problem DSL: 곱셈식을 나눗셈식으로 나타내기 (S3_초등_3_009140)"""

from __future__ import annotations

from modu_math.dsl import (
    Canvas,
    ProblemTemplate,
    RectSlot,
    Region,
    TextBoxSlot,
    TextSlot,
)


PROBLEM_ID = "S3_초등_3_009140"
PROBLEM_TITLE = "곱셈식을 나눗셈식으로 나타내기"

ANSWER = {
    "type": "choice",
    "value": "8 ÷ 2 = 4",
    "unit": "",
    "answer_index": 0,
    "values": ["8 ÷ 2 = 4"],
    "blanks": [],
    "choices": [
        {"id": "slot.choice.option_0", "slot_id": "slot.choice.option_0", "text": "8 ÷ 2 = 4", "value": "8 ÷ 2 = 4"},
        {"id": "slot.choice.option_1", "slot_id": "slot.choice.option_1", "text": "4 ÷ 2 = 2", "value": "4 ÷ 2 = 2"},
    ],
    "answer_key": [
        {
            "slot_id": "slot.choice.option_0",
            "value": "8 ÷ 2 = 4",
        }
    ],
}

SEMANTIC_OVERRIDE = {
    "problem_id": PROBLEM_ID,
    "problem_type": "multiple_choice_multiplication_to_division",
    "metadata": {
        "grade": 3,
        "semester": 1,
        "subject": "수학",
        "chapter": "03단원_나눗셈",
        "language": "ko-KR",
    },
    "domain": {
        "objects": [
            {"id": "expr.given", "type": "multiplication_equation", "label": "2 × 4 = 8", "factors": [2, 4], "product": 8},
            {"id": "expr.option_0", "type": "division_equation", "label": "8 ÷ 2 = 4", "dividend": 8, "divisor": 2, "quotient": 4},
            {"id": "expr.option_1", "type": "division_equation", "label": "4 ÷ 2 = 2", "dividend": 4, "divisor": 2, "quotient": 2},
        ],
        "relations": [
            {
                "id": "relation.inverse_equation",
                "type": "equivalent_division",
                "from_id": "expr.option_0",
                "to_id": "expr.given",
            }
        ],
    },
    "answer": ANSWER,
}


def build_problem_template() -> ProblemTemplate:
    stem_slot = TextBoxSlot(
        id="slot.stem.question",
        prompt="",
        text="95. 곱셈식 2 × 4 = 8을 나눗셈식으로 바르게 나타낸 것을 선택하세요.",
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

    box_0 = RectSlot(
        id="slot.choice.option_0",
        prompt="",
        x=230,
        y=82,
        width=220,
        height=64,
        fill="#fee2e2",
        stroke="#ef4444",
        stroke_width=1.5,
        interaction={"type": "choice", "role": "answer", "choice_index": 0, "value": "8 ÷ 2 = 4", "group_id": "slot.choice.group", "include_in_submission": True},
    )
    text_0 = TextSlot(id="slot.choice.label_0", prompt="", text="8 ÷ 2 = 4", x=340, y=114, font_size=24, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center")

    box_1 = RectSlot(
        id="slot.choice.option_1",
        prompt="",
        x=540,
        y=82,
        width=220,
        height=64,
        fill="#ffedd5",
        stroke="#f59e0b",
        stroke_width=1.5,
        interaction={"type": "choice", "role": "answer", "choice_index": 1, "value": "4 ÷ 2 = 2", "group_id": "slot.choice.group", "include_in_submission": True},
    )
    text_1 = TextSlot(id="slot.choice.label_1", prompt="", text="4 ÷ 2 = 2", x=650, y=114, font_size=24, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center")

    return ProblemTemplate(
        id=PROBLEM_ID,
        title=PROBLEM_TITLE,
        canvas=Canvas(width=886, height=180, coordinate_mode="logical"),
        regions=(
            Region(id="region.stem", role="stem", flow="absolute", slot_ids=("slot.stem.question",)),
            Region(id="region.choices", role="choices", flow="absolute", slot_ids=("slot.choice.option_0", "slot.choice.label_0", "slot.choice.option_1", "slot.choice.label_1")),
        ),
        slots=(stem_slot, box_0, text_0, box_1, text_1),
    )


PROBLEM_TEMPLATE = build_problem_template()

SOLVABLE = {
    "schema": "modu.solvable.v1.3",
    "problem_id": PROBLEM_ID,
    "given": [
        {"ref": "expr.given", "value": "2 × 4 = 8"},
        {"ref": "expr.option_0", "value": "8 ÷ 2 = 4"},
        {"ref": "expr.option_1", "value": "4 ÷ 2 = 2"},
    ],
    "target": {"ref": "slot.choice.option_0", "type": "choice"},
    "method": "multiplication_to_division_conversion",
    "steps": [
        {
            "id": "step.convert",
            "expr": "8 / 2 = 4",
            "value": "8 ÷ 2 = 4",
            "explanation": "곱셈식 2 × 4 = 8에서 곱인 8을 나누어지는 수로 하여 8 ÷ 2 = 4로 나타낼 수 있습니다.",
        }
    ],
    "answer": ANSWER,
    "diagnostics": {
        "skills": ["division.multiplication_relation"],
        "errors": {
            "4 ÷ 2 = 2": "division.wrong_dividend_from_multiplication",
        },
    },
}
