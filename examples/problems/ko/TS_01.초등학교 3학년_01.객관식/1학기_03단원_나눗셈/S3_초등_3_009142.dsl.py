"""ModuMath Problem DSL: 몫이 5인 나눗셈식 선택하기 (S3_초등_3_009142)"""

from __future__ import annotations

from modu_math.dsl import (
    Canvas,
    ProblemTemplate,
    RectSlot,
    Region,
    TextBoxSlot,
    TextSlot,
)


PROBLEM_ID = "S3_초등_3_009142"
PROBLEM_TITLE = "몫이 5인 나눗셈식 선택하기"

ANSWER = {
    "type": "choice",
    "value": "30 ÷ 6 = 5",
    "unit": "",
    "answer_index": 0,
    "values": ["30 ÷ 6 = 5"],
    "blanks": [],
    "choices": [
        {"id": "slot.choice.option_0", "slot_id": "slot.choice.option_0", "text": "30 ÷ 6 = 5", "value": "30 ÷ 6 = 5"},
        {"id": "slot.choice.option_1", "slot_id": "slot.choice.option_1", "text": "30 ÷ 5 = 6", "value": "30 ÷ 5 = 6"},
    ],
    "answer_key": [
        {
            "slot_id": "slot.choice.option_0",
            "value": "30 ÷ 6 = 5",
        }
    ],
}

SEMANTIC_OVERRIDE = {
    "problem_id": PROBLEM_ID,
    "problem_type": "multiple_choice_division_quotient",
    "metadata": {
        "grade": 3,
        "semester": 1,
        "subject": "수학",
        "chapter": "03단원_나눗셈",
        "language": "ko-KR",
    },
    "domain": {
        "objects": [
            {"id": "expr.option_0", "type": "division_equation", "label": "30 ÷ 6 = 5", "dividend": 30, "divisor": 6, "quotient": 5},
            {"id": "expr.option_1", "type": "division_equation", "label": "30 ÷ 5 = 6", "dividend": 30, "divisor": 5, "quotient": 6},
        ],
        "relations": [
            {
                "id": "relation.target_quotient",
                "type": "has_quotient",
                "from_id": "expr.option_0",
                "to_id": "value.5",
            }
        ],
    },
    "answer": ANSWER,
}


def build_problem_template() -> ProblemTemplate:
    stem_slot = TextBoxSlot(
        id="slot.stem.question",
        prompt="",
        text="97. 몫이 5인 나눗셈식을 선택하세요.",
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
        x=150,
        y=82,
        width=310,
        height=64,
        fill="#e6f4ea",
        stroke="#65a30d",
        stroke_width=1.5,
        interaction={"type": "choice", "role": "answer", "choice_index": 0, "value": "30 ÷ 6 = 5", "group_id": "slot.choice.group", "include_in_submission": True},
    )
    text_0 = TextSlot(id="slot.choice.label_0", prompt="", text="30 ÷ 6 = 5", x=305, y=114, font_size=24, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center")

    box_1 = RectSlot(
        id="slot.choice.option_1",
        prompt="",
        x=540,
        y=82,
        width=310,
        height=64,
        fill="#ffedd5",
        stroke="#f59e0b",
        stroke_width=1.5,
        interaction={"type": "choice", "role": "answer", "choice_index": 1, "value": "30 ÷ 5 = 6", "group_id": "slot.choice.group", "include_in_submission": True},
    )
    text_1 = TextSlot(id="slot.choice.label_1", prompt="", text="30 ÷ 5 = 6", x=695, y=114, font_size=24, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center")

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
        {"ref": "expr.option_0", "value": "30 ÷ 6 = 5"},
        {"ref": "expr.option_1", "value": "30 ÷ 5 = 6"},
    ],
    "target": {"ref": "slot.choice.option_0", "type": "choice"},
    "method": "division_quotient_identification",
    "steps": [
        {
            "id": "step.check_quotient",
            "expr": "30 / 6 = 5",
            "value": "30 ÷ 6 = 5",
            "explanation": "30 ÷ 6 = 5의 몫은 5이고, 30 ÷ 5 = 6의 몫은 6입니다.",
        }
    ],
    "answer": ANSWER,
    "diagnostics": {
        "skills": ["division.quotient_meaning"],
        "errors": {
            "30 ÷ 5 = 6": "division.confused_divisor_with_quotient",
        },
    },
}
