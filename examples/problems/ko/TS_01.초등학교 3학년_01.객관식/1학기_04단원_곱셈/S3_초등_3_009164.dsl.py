"""ModuMath Problem DSL: 기준 곱보다 더 큰 식 찾기 (S3_초등_3_009164)"""

from __future__ import annotations

from modu_math.dsl import (
    Canvas,
    ProblemTemplate,
    RectSlot,
    Region,
    TextBoxSlot,
    TextSlot,
)


PROBLEM_ID = "S3_초등_3_009164"
PROBLEM_TITLE = "곱이 30 × 5보다 더 큰 것 선택하기"

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
            {"id": "expr.reference", "type": "multiplication", "label": "30 × 5", "value": 150},
            {"id": "expr.ga", "type": "multiplication", "label": "㉠", "equation": "71 × 2", "value": 142},
            {"id": "expr.na", "type": "multiplication", "label": "㉡", "equation": "42 × 4", "value": 168},
        ],
        "relations": [
            {
                "id": "relation.greater_than_ref",
                "type": "greater_than",
                "from_id": "expr.na",
                "to_id": "expr.reference",
            }
        ],
    },
    "answer": ANSWER,
}


def build_problem_template() -> ProblemTemplate:
    stem_slot = TextBoxSlot(
        id="slot.stem.question",
        prompt="",
        text="25. 곱이 30 × 5보다 더 큰 것을 찾아 선택하세요.",
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
        x=365,
        y=72,
        width=495,
        height=76,
        fill="#ffffff",
        stroke="#65a30d",
        stroke_width=1.5,
    )

    opt_0 = TextSlot(
        id="slot.choice.option_0",
        prompt="",
        text="㉠ 71 × 2",
        x=485,
        y=110,
        font_size=24,
        font_family='"Noto Sans KR", sans-serif',
        fill="#111827",
        align="center",
        interaction={"type": "choice", "role": "answer", "choice_index": 0, "value": "㉠", "group_id": "slot.choice.group", "include_in_submission": True},
    )
    opt_1 = TextSlot(
        id="slot.choice.option_1",
        prompt="",
        text="㉡ 42 × 4",
        x=725,
        y=110,
        font_size=24,
        font_family='"Noto Sans KR", sans-serif',
        fill="#111827",
        align="center",
        interaction={"type": "choice", "role": "answer", "choice_index": 1, "value": "㉡", "group_id": "slot.choice.group", "include_in_submission": True},
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
        {"ref": "expr.reference", "value": "30 × 5"},
        {"ref": "expr.ga", "value": "71 × 2"},
        {"ref": "expr.na", "value": "42 × 4"},
    ],
    "target": {"ref": "slot.choice.option_1", "type": "choice"},
    "method": "compare_products_against_reference",
    "steps": [
        {"id": "step.calc_ref", "expr": "30 * 5", "value": 150, "explanation": "30 × 5 = 150입니다."},
        {"id": "step.calc_ga", "expr": "71 * 2", "value": 142, "explanation": "㉠ 71 × 2 = 142로 150보다 작습니다."},
        {"id": "step.calc_na", "expr": "42 * 4", "value": 168, "explanation": "㉡ 42 × 4 = 168로 150보다 큽니다."},
    ],
    "answer": ANSWER,
    "diagnostics": {
        "skills": ["multiplication.two_by_one", "multiplication.comparison"],
        "errors": {
            "㉠": "multiplication.comparison_error",
        },
    },
}
