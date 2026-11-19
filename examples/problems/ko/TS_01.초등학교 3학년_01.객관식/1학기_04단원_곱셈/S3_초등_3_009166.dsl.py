"""ModuMath Problem DSL: 계산 결과가 다른 하나 찾기 (S3_초등_3_009166)"""

from __future__ import annotations

from modu_math.dsl import (
    Canvas,
    ProblemTemplate,
    Region,
    TextBoxSlot,
    TextSlot,
)


PROBLEM_ID = "S3_초등_3_009166"
PROBLEM_TITLE = "계산 결과가 다른 곱셈식 찾기"

ANSWER = {
    "type": "choice",
    "value": "①",
    "unit": "",
    "answer_index": 0,
    "values": ["①"],
    "blanks": [],
    "choices": [
        {"id": "slot.choice.option_0", "slot_id": "slot.choice.option_0", "text": "①", "value": "①"},
        {"id": "slot.choice.option_1", "slot_id": "slot.choice.option_1", "text": "②", "value": "②"},
        {"id": "slot.choice.option_2", "slot_id": "slot.choice.option_2", "text": "③", "value": "③"},
        {"id": "slot.choice.option_3", "slot_id": "slot.choice.option_3", "text": "④", "value": "④"},
        {"id": "slot.choice.option_4", "slot_id": "slot.choice.option_4", "text": "⑤", "value": "⑤"},
    ],
    "answer_key": [
        {
            "slot_id": "slot.choice.option_0",
            "value": "①",
        }
    ],
}

SEMANTIC_OVERRIDE = {
    "problem_id": PROBLEM_ID,
    "problem_type": "multiple_choice_multiplication_odd_one_out",
    "metadata": {
        "grade": 3,
        "semester": 1,
        "subject": "수학",
        "chapter": "04단원_곱셈",
        "language": "ko-KR",
    },
    "domain": {
        "objects": [
            {"id": "expr.opt0", "type": "multiplication", "label": "①", "equation": "13 × 8", "value": 104},
            {"id": "expr.opt1", "type": "multiplication", "label": "②", "equation": "18 × 6", "value": 108},
            {"id": "expr.opt2", "type": "multiplication", "label": "③", "equation": "27 × 4", "value": 108},
            {"id": "expr.opt3", "type": "multiplication", "label": "④", "equation": "36 × 3", "value": 108},
            {"id": "expr.opt4", "type": "multiplication", "label": "⑤", "equation": "54 × 2", "value": 108},
        ],
        "relations": [
            {
                "id": "relation.odd_one_out",
                "type": "different_product",
                "from_id": "expr.opt0",
                "to_id": "value.108",
            }
        ],
    },
    "answer": ANSWER,
}


def build_problem_template() -> ProblemTemplate:
    stem_slot = TextBoxSlot(
        id="slot.stem.question",
        prompt="",
        text="27. 계산 결과가 다른 하나는 어느 것일까요?",
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

    opt_0 = TextSlot(id="slot.choice.option_0", prompt="", text="① 13 × 8", x=32, y=82, font_size=22, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="left", interaction={"type": "choice", "role": "answer", "choice_index": 0, "value": "①", "group_id": "slot.choice.group", "include_in_submission": True})
    opt_1 = TextSlot(id="slot.choice.option_1", prompt="", text="② 18 × 6", x=310, y=82, font_size=22, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="left", interaction={"type": "choice", "role": "answer", "choice_index": 1, "value": "②", "group_id": "slot.choice.group", "include_in_submission": True})
    opt_2 = TextSlot(id="slot.choice.option_2", prompt="", text="③ 27 × 4", x=590, y=82, font_size=22, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="left", interaction={"type": "choice", "role": "answer", "choice_index": 2, "value": "③", "group_id": "slot.choice.group", "include_in_submission": True})
    opt_3 = TextSlot(id="slot.choice.option_3", prompt="", text="④ 36 × 3", x=32, y=124, font_size=22, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="left", interaction={"type": "choice", "role": "answer", "choice_index": 3, "value": "④", "group_id": "slot.choice.group", "include_in_submission": True})
    opt_4 = TextSlot(id="slot.choice.option_4", prompt="", text="⑤ 54 × 2", x=310, y=124, font_size=22, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="left", interaction={"type": "choice", "role": "answer", "choice_index": 4, "value": "⑤", "group_id": "slot.choice.group", "include_in_submission": True})

    return ProblemTemplate(
        id=PROBLEM_ID,
        title=PROBLEM_TITLE,
        canvas=Canvas(width=886, height=170, coordinate_mode="logical"),
        regions=(
            Region(id="region.stem", role="stem", flow="absolute", slot_ids=("slot.stem.question",)),
            Region(id="region.choices", role="choices", flow="absolute", slot_ids=("slot.choice.option_0", "slot.choice.option_1", "slot.choice.option_2", "slot.choice.option_3", "slot.choice.option_4")),
        ),
        slots=(stem_slot, opt_0, opt_1, opt_2, opt_3, opt_4),
    )


PROBLEM_TEMPLATE = build_problem_template()

SOLVABLE = {
    "schema": "modu.solvable.v1.3",
    "problem_id": PROBLEM_ID,
    "given": [
        {"ref": "expr.opt0", "value": "13 × 8"},
        {"ref": "expr.opt1", "value": "18 × 6"},
        {"ref": "expr.opt2", "value": "27 × 4"},
        {"ref": "expr.opt3", "value": "36 × 3"},
        {"ref": "expr.opt4", "value": "54 × 2"},
    ],
    "target": {"ref": "slot.choice.option_0", "type": "choice"},
    "method": "compute_and_find_different_product",
    "steps": [
        {"id": "step.calc_0", "expr": "13 * 8", "value": 104, "explanation": "① 13 × 8 = 104입니다."},
        {"id": "step.calc_others", "expr": "18 * 6 = 27 * 4 = 36 * 3 = 54 * 2", "value": 108, "explanation": "②, ③, ④, ⑤의 계산 결과는 모두 108이므로 다른 하나는 ①입니다."},
    ],
    "answer": ANSWER,
    "diagnostics": {
        "skills": ["multiplication.two_by_one_with_carry"],
        "errors": {
            "②": "multiplication.calculation_error",
            "③": "multiplication.calculation_error",
            "④": "multiplication.calculation_error",
            "⑤": "multiplication.calculation_error",
        },
    },
}
