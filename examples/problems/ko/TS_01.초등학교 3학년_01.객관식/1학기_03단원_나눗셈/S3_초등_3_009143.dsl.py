"""ModuMath Problem DSL: 나눗셈식을 동수누감으로 나타내기 (S3_초등_3_009143)"""

from __future__ import annotations

from modu_math.dsl import (
    Canvas,
    ProblemTemplate,
    RectSlot,
    Region,
    TextBoxSlot,
    TextSlot,
)


PROBLEM_ID = "S3_초등_3_009143"
PROBLEM_TITLE = "나눗셈식을 뺄셈식으로 바르게 나타낸 것 선택하기"

ANSWER = {
    "type": "choice",
    "value": "20 - 5 - 5 - 5 - 5 = 0",
    "unit": "",
    "answer_index": 0,
    "values": ["20 - 5 - 5 - 5 - 5 = 0"],
    "blanks": [],
    "choices": [
        {"id": "slot.choice.option_0", "slot_id": "slot.choice.option_0", "text": "20 - 5 - 5 - 5 - 5 = 0", "value": "20 - 5 - 5 - 5 - 5 = 0"},
        {"id": "slot.choice.option_1", "slot_id": "slot.choice.option_1", "text": "20 - 4 - 4 - 4 - 4 - 4 = 0", "value": "20 - 4 - 4 - 4 - 4 - 4 = 0"},
    ],
    "answer_key": [
        {
            "slot_id": "slot.choice.option_0",
            "value": "20 - 5 - 5 - 5 - 5 = 0",
        }
    ],
}

SEMANTIC_OVERRIDE = {
    "problem_id": PROBLEM_ID,
    "problem_type": "multiple_choice_division_repeated_subtraction",
    "metadata": {
        "grade": 3,
        "semester": 1,
        "subject": "수학",
        "chapter": "03단원_나눗셈",
        "language": "ko-KR",
    },
    "domain": {
        "objects": [
            {"id": "expr.given", "type": "division_equation", "label": "20 ÷ 5 = 4", "dividend": 20, "divisor": 5, "quotient": 4},
            {"id": "expr.option_0", "type": "repeated_subtraction", "label": "20 - 5 - 5 - 5 - 5 = 0", "subtrahend": 5, "count": 4},
            {"id": "expr.option_1", "type": "repeated_subtraction", "label": "20 - 4 - 4 - 4 - 4 - 4 = 0", "subtrahend": 4, "count": 5},
        ],
        "relations": [
            {
                "id": "relation.repeated_subtraction",
                "type": "represents_division",
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
        text="99. 20 ÷ 5 = 4를 바르게 나타낸 것을 선택하세요.",
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
        x=70,
        y=82,
        width=360,
        height=64,
        fill="#ffffff",
        stroke="#f59e0b",
        stroke_width=1.5,
        interaction={"type": "choice", "role": "answer", "choice_index": 0, "value": "20 - 5 - 5 - 5 - 5 = 0", "group_id": "slot.choice.group", "include_in_submission": True},
    )
    text_0 = TextSlot(id="slot.choice.label_0", prompt="", text="20 - 5 - 5 - 5 - 5 = 0", x=250, y=114, font_size=22, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center")

    box_1 = RectSlot(
        id="slot.choice.option_1",
        prompt="",
        x=480,
        y=82,
        width=360,
        height=64,
        fill="#ffffff",
        stroke="#f59e0b",
        stroke_width=1.5,
        interaction={"type": "choice", "role": "answer", "choice_index": 1, "value": "20 - 4 - 4 - 4 - 4 - 4 = 0", "group_id": "slot.choice.group", "include_in_submission": True},
    )
    text_1 = TextSlot(id="slot.choice.label_1", prompt="", text="20 - 4 - 4 - 4 - 4 - 4 = 0", x=660, y=114, font_size=22, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center")

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
        {"ref": "expr.given", "value": "20 ÷ 5 = 4"},
        {"ref": "expr.option_0", "value": "20 - 5 - 5 - 5 - 5 = 0"},
        {"ref": "expr.option_1", "value": "20 - 4 - 4 - 4 - 4 - 4 = 0"},
    ],
    "target": {"ref": "slot.choice.option_0", "type": "choice"},
    "method": "division_as_repeated_subtraction",
    "steps": [
        {
            "id": "step.repeated_subtraction",
            "expr": "20 - 5 - 5 - 5 - 5 = 0",
            "value": "20 - 5 - 5 - 5 - 5 = 0",
            "explanation": "20 ÷ 5 = 4는 20에서 5를 4번 빼면 0이 된다는 뜻이므로 20 - 5 - 5 - 5 - 5 = 0이 바른 식입니다.",
        }
    ],
    "answer": ANSWER,
    "diagnostics": {
        "skills": ["division.repeated_subtraction"],
        "errors": {
            "20 - 4 - 4 - 4 - 4 - 4 = 0": "division.swapped_divisor_and_quotient",
        },
    },
}
