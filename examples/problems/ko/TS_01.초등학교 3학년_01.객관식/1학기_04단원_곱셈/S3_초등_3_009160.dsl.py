"""ModuMath Problem DSL: 곱이 더 큰 식 선택하기 (S3_초등_3_009160)"""

from __future__ import annotations

from modu_math.dsl import (
    Canvas,
    ProblemTemplate,
    RectSlot,
    Region,
    TextBoxSlot,
    TextSlot,
)


PROBLEM_ID = "S3_초등_3_009160"
PROBLEM_TITLE = "곱이 더 큰 식 기호 선택하기"

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
            {"id": "expr.ga", "type": "multiplication", "label": "㉠", "equation": "71 × 4", "value": 284},
            {"id": "expr.na", "type": "multiplication", "label": "㉡", "equation": "39 × 4", "value": 156},
        ],
        "relations": [
            {
                "id": "relation.comparison",
                "type": "greater_than",
                "from_id": "expr.ga",
                "to_id": "expr.na",
            }
        ],
    },
    "answer": ANSWER,
}


def build_problem_template() -> ProblemTemplate:
    stem_slot = TextBoxSlot(
        id="slot.stem.question",
        prompt="",
        text="21. 곱이 더 큰 것을 선택하세요.",
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

    bg_box = RectSlot(
        id="slot.diagram.bg",
        prompt="",
        x=355,
        y=72,
        width=500,
        height=76,
        fill="#dce7b7",
        stroke="none",
        stroke_width=0,
    )

    opt_0 = TextSlot(
        id="slot.choice.option_0",
        prompt="",
        text="㉠ 71 × 4",
        x=470,
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
        text="㉡ 39 × 4",
        x=710,
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
            Region(id="region.diagram", role="diagram", flow="absolute", slot_ids=("slot.diagram.bg",)),
            Region(id="region.choices", role="choices", flow="absolute", slot_ids=("slot.choice.option_0", "slot.choice.option_1")),
        ),
        slots=(stem_slot, bg_box, opt_0, opt_1),
    )


PROBLEM_TEMPLATE = build_problem_template()

SOLVABLE = {
    "schema": "modu.solvable.v1.3",
    "problem_id": PROBLEM_ID,
    "given": [
        {"ref": "expr.ga", "value": "71 × 4"},
        {"ref": "expr.na", "value": "39 × 4"},
    ],
    "target": {"ref": "slot.choice.option_0", "type": "choice"},
    "method": "compare_products",
    "steps": [
        {"id": "step.calc_ga", "expr": "71 * 4", "value": 284, "explanation": "㉠ 71 × 4 = 284입니다."},
        {"id": "step.calc_na", "expr": "39 * 4", "value": 156, "explanation": "㉡ 39 × 4 = 156이므로 284 > 156, 곱이 더 큰 것은 ㉠입니다."},
    ],
    "answer": ANSWER,
    "diagnostics": {
        "skills": ["multiplication.two_by_one", "multiplication.comparison"],
        "errors": {
            "㉡": "multiplication.comparison_error",
        },
    },
}
