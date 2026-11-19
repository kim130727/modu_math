"""ModuMath Problem DSL: 나눗셈의 몫이 7인 식 선택하기 (S3_초등_3_009137)"""

from __future__ import annotations

from modu_math.dsl import (
    Canvas,
    ProblemTemplate,
    RectSlot,
    Region,
    TextBoxSlot,
    TextSlot,
)


PROBLEM_ID = "S3_초등_3_009137"
PROBLEM_TITLE = "나눗셈의 몫이 7인 식 선택하기"

ANSWER = {
    "type": "choice",
    "value": "㉠",
    "unit": "",
    "answer_index": 0,
    "values": ["㉠"],
    "blanks": [],
    "choices": [
        {"id": "slot.choice.option_0", "slot_id": "slot.choice.option_0", "text": "㉠", "value": "㉠"},
        {"id": "slot.choice.option_1", "slot_id": "slot.choice.option_1", "text": "㉡", "value": "㉡"},
    ],
    "answer_key": [
        {
            "slot_id": "slot.choice.option_0",
            "value": "㉠",
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
            {"id": "expr.ga", "type": "division_equation", "label": "㉠", "dividend": 42, "divisor": 6, "quotient": 7},
            {"id": "expr.na", "type": "division_equation", "label": "㉡", "dividend": 35, "divisor": 7, "quotient": 5},
        ],
        "relations": [
            {
                "id": "relation.target_quotient",
                "type": "has_quotient",
                "from_id": "expr.ga",
                "to_id": "value.7",
            }
        ],
    },
    "answer": ANSWER,
}


def build_problem_template() -> ProblemTemplate:
    stem_slot = TextBoxSlot(
        id="slot.stem.question",
        prompt="",
        text="92. 나눗셈의 몫이 7인 것을 선택하세요.",
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
        x=220,
        y=76,
        width=630,
        height=76,
        fill="#ffffff",
        stroke="#f59e0b",
        stroke_width=1.8,
    )

    opt_0 = TextSlot(
        id="slot.choice.option_0",
        prompt="",
        text="㉠ 42 ÷ 6 = 7",
        x=365,
        y=114,
        font_size=24,
        font_family='"Noto Sans KR", sans-serif',
        fill="#111827",
        align="center",
        interaction={"type": "choice", "role": "answer", "choice_index": 0, "value": "㉠", "group_id": "slot.choice.group", "include_in_submission": True},
    )
    opt_1 = TextSlot(
        id="slot.choice.option_1",
        prompt="",
        text="㉡ 35 ÷ 7 = 5",
        x=685,
        y=114,
        font_size=24,
        font_family='"Noto Sans KR", sans-serif',
        fill="#111827",
        align="center",
        interaction={"type": "choice", "role": "answer", "choice_index": 1, "value": "㉡", "group_id": "slot.choice.group", "include_in_submission": True},
    )

    return ProblemTemplate(
        id=PROBLEM_ID,
        title=PROBLEM_TITLE,
        canvas=Canvas(width=886, height=180, coordinate_mode="logical"),
        regions=(
            Region(id="region.stem", role="stem", flow="absolute", slot_ids=("slot.stem.question",)),
            Region(id="region.diagram", role="diagram", flow="absolute", slot_ids=("slot.diagram.frame",)),
            Region(id="region.choices", role="choices", flow="absolute", slot_ids=("slot.choice.option_0", "slot.choice.option_1")),
        ),
        slots=(stem_slot, frame_box, opt_0, opt_1),
    )


PROBLEM_TEMPLATE = build_problem_template()

SOLVABLE = {
    "schema": "modu.solvable.v1.3",
    "problem_id": PROBLEM_ID,
    "given": [
        {"ref": "expr.ga", "value": "42 ÷ 6 = 7"},
        {"ref": "expr.na", "value": "35 ÷ 7 = 5"},
    ],
    "target": {"ref": "slot.choice.option_0", "type": "choice"},
    "method": "division_quotient_identification",
    "steps": [
        {
            "id": "step.check_quotient",
            "expr": "42 / 6 = 7",
            "value": "㉠",
            "explanation": "㉠의 몫은 7이고, ㉡의 몫은 5입니다. 따라서 몫이 7인 것은 ㉠입니다.",
        }
    ],
    "answer": ANSWER,
    "diagnostics": {
        "skills": ["division.quotient_meaning"],
        "errors": {
            "㉡": "division.confused_divisor_with_quotient",
        },
    },
}
