"""ModuMath Problem DSL: 크기를 비교하여 더 큰 것 선택하기 (S3_초등_3_009167)"""

from __future__ import annotations

from modu_math.dsl import (
    Canvas,
    ProblemTemplate,
    RectSlot,
    Region,
    TextBoxSlot,
    TextSlot,
)


PROBLEM_ID = "S3_초등_3_009167"
PROBLEM_TITLE = "크기를 비교하여 더 큰 것 선택하기"

ANSWER = {
    "type": "choice",
    "value": "68 × 3",
    "unit": "",
    "answer_index": 0,
    "values": ["68 × 3"],
    "blanks": [],
    "choices": [
        {"id": "slot.choice.option_0", "slot_id": "slot.choice.option_0", "text": "68 × 3", "value": "68 × 3"},
        {"id": "slot.choice.option_1", "slot_id": "slot.choice.option_1", "text": "200", "value": "200"},
    ],
    "answer_key": [
        {
            "slot_id": "slot.choice.option_0",
            "value": "68 × 3",
        }
    ],
}

SEMANTIC_OVERRIDE = {
    "problem_id": PROBLEM_ID,
    "problem_type": "multiple_choice_multiplication_comparison",
    "metadata": {
        "grade": 3,
        "semester": 1,
        "subject": "수학",
        "chapter": "04단원_곱셈",
        "language": "ko-KR",
    },
    "domain": {
        "objects": [
            {"id": "expr.option_0", "type": "multiplication", "label": "68 × 3", "value": 204},
            {"id": "expr.option_1", "type": "number", "label": "200", "value": 200},
        ],
        "relations": [
            {
                "id": "relation.comparison",
                "type": "greater_than",
                "from_id": "expr.option_0",
                "to_id": "expr.option_1",
            }
        ],
    },
    "answer": ANSWER,
}


def build_problem_template() -> ProblemTemplate:
    stem_slot = TextBoxSlot(
        id="slot.stem.question",
        prompt="",
        text="28. 크기를 비교하여 더 큰 것을 선택하세요.",
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
        x=455,
        y=72,
        width=395,
        height=76,
        fill="#ffffff",
        stroke="#65a30d",
        stroke_width=1.5,
    )

    opt_0 = TextSlot(
        id="slot.choice.option_0",
        prompt="",
        text="68 × 3",
        x=565,
        y=110,
        font_size=24,
        font_family='"Noto Sans KR", sans-serif',
        fill="#111827",
        align="center",
        interaction={"type": "choice", "role": "answer", "choice_index": 0, "value": "68 × 3", "group_id": "slot.choice.group", "include_in_submission": True},
    )
    opt_1 = TextSlot(
        id="slot.choice.option_1",
        prompt="",
        text="200",
        x=745,
        y=110,
        font_size=24,
        font_family='"Noto Sans KR", sans-serif',
        fill="#111827",
        align="center",
        interaction={"type": "choice", "role": "answer", "choice_index": 1, "value": "200", "group_id": "slot.choice.group", "include_in_submission": True},
    )

    return ProblemTemplate(
        id=PROBLEM_ID,
        title=PROBLEM_TITLE,
        canvas=Canvas(width=886, height=170, coordinate_mode="logical"),
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
        {"ref": "expr.option_0", "value": "68 × 3"},
        {"ref": "expr.option_1", "value": 200},
    ],
    "target": {"ref": "slot.choice.option_0", "type": "choice"},
    "method": "compare_product_and_number",
    "steps": [
        {"id": "step.calc_0", "expr": "68 * 3", "value": 204, "explanation": "68 × 3 = 204입니다."},
        {"id": "step.compare", "expr": "204 > 200", "value": "68 × 3", "explanation": "204 > 200이므로 더 큰 것은 68 × 3입니다."},
    ],
    "answer": ANSWER,
    "diagnostics": {
        "skills": ["multiplication.two_by_one_with_carry", "multiplication.comparison"],
        "errors": {
            "200": "multiplication.calculation_error",
        },
    },
}
