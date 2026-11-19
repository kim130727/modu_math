"""ModuMath Problem DSL: 35 ÷ 7의 몫을 구할 때 필요한 곱셈식 찾기 (S3_초등_3_009144)"""

from __future__ import annotations

from modu_math.dsl import (
    Canvas,
    ProblemTemplate,
    Region,
    TextBoxSlot,
    TextSlot,
)


PROBLEM_ID = "S3_초등_3_009144"
PROBLEM_TITLE = "35 ÷ 7의 몫을 구할 때 필요한 곱셈식 찾기"

ANSWER = {
    "type": "choice",
    "value": "③",
    "unit": "",
    "answer_index": 2,
    "values": ["③"],
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
            "slot_id": "slot.choice.option_2",
            "value": "③",
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
            {"id": "expr.division", "type": "division", "dividend": 35, "divisor": 7},
            {"id": "expr.opt0", "type": "multiplication", "label": "①", "equation": "7 × 3 = 21"},
            {"id": "expr.opt1", "type": "multiplication", "label": "②", "equation": "7 × 4 = 28"},
            {"id": "expr.opt2", "type": "multiplication", "label": "③", "equation": "7 × 5 = 35"},
            {"id": "expr.opt3", "type": "multiplication", "label": "④", "equation": "7 × 6 = 42"},
            {"id": "expr.opt4", "type": "multiplication", "label": "⑤", "equation": "7 × 7 = 49"},
        ],
        "relations": [
            {
                "id": "relation.inverse_multiplication",
                "type": "solves_division",
                "from_id": "expr.opt2",
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
        text="1. 35 ÷ 7의 몫을 구할 때 필요한 곱셈식은 어느 것일까요?",
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

    opt_0 = TextSlot(
        id="slot.choice.option_0",
        prompt="",
        text="① 7 × 3 = 21",
        x=50,
        y=82,
        font_size=22,
        font_family='"Noto Sans KR", sans-serif',
        fill="#111827",
        align="left",
        interaction={"type": "choice", "role": "answer", "choice_index": 0, "value": "①", "group_id": "slot.choice.group", "include_in_submission": True},
    )
    opt_1 = TextSlot(
        id="slot.choice.option_1",
        prompt="",
        text="② 7 × 4 = 28",
        x=520,
        y=82,
        font_size=22,
        font_family='"Noto Sans KR", sans-serif',
        fill="#111827",
        align="left",
        interaction={"type": "choice", "role": "answer", "choice_index": 1, "value": "②", "group_id": "slot.choice.group", "include_in_submission": True},
    )
    opt_2 = TextSlot(
        id="slot.choice.option_2",
        prompt="",
        text="③ 7 × 5 = 35",
        x=50,
        y=124,
        font_size=22,
        font_family='"Noto Sans KR", sans-serif',
        fill="#111827",
        align="left",
        interaction={"type": "choice", "role": "answer", "choice_index": 2, "value": "③", "group_id": "slot.choice.group", "include_in_submission": True},
    )
    opt_3 = TextSlot(
        id="slot.choice.option_3",
        prompt="",
        text="④ 7 × 6 = 42",
        x=520,
        y=124,
        font_size=22,
        font_family='"Noto Sans KR", sans-serif',
        fill="#111827",
        align="left",
        interaction={"type": "choice", "role": "answer", "choice_index": 3, "value": "④", "group_id": "slot.choice.group", "include_in_submission": True},
    )
    opt_4 = TextSlot(
        id="slot.choice.option_4",
        prompt="",
        text="⑤ 7 × 7 = 49",
        x=50,
        y=166,
        font_size=22,
        font_family='"Noto Sans KR", sans-serif',
        fill="#111827",
        align="left",
        interaction={"type": "choice", "role": "answer", "choice_index": 4, "value": "⑤", "group_id": "slot.choice.group", "include_in_submission": True},
    )

    return ProblemTemplate(
        id=PROBLEM_ID,
        title=PROBLEM_TITLE,
        canvas=Canvas(width=886, height=210, coordinate_mode="logical"),
        regions=(
            Region(id="region.stem", role="stem", flow="absolute", slot_ids=("slot.stem.question",)),
            Region(
                id="region.choices",
                role="choices",
                flow="absolute",
                slot_ids=(
                    "slot.choice.option_0",
                    "slot.choice.option_1",
                    "slot.choice.option_2",
                    "slot.choice.option_3",
                    "slot.choice.option_4",
                ),
            ),
        ),
        slots=(stem_slot, opt_0, opt_1, opt_2, opt_3, opt_4),
    )


PROBLEM_TEMPLATE = build_problem_template()

SOLVABLE = {
    "schema": "modu.solvable.v1.3",
    "problem_id": PROBLEM_ID,
    "given": [
        {"ref": "expr.division", "value": "35 ÷ 7"},
        {"ref": "expr.opt0", "value": "7 × 3 = 21"},
        {"ref": "expr.opt1", "value": "7 × 4 = 28"},
        {"ref": "expr.opt2", "value": "7 × 5 = 35"},
        {"ref": "expr.opt3", "value": "7 × 6 = 42"},
        {"ref": "expr.opt4", "value": "7 × 7 = 49"},
    ],
    "target": {"ref": "slot.choice.option_2", "type": "choice"},
    "method": "division_via_multiplication_table",
    "steps": [
        {
            "id": "step.find_multiplication",
            "expr": "7 * 5 = 35",
            "value": "③",
            "explanation": "7단 곱셈구구에서 곱이 35인 곱셈식은 7 × 5 = 35(③)입니다.",
        }
    ],
    "answer": ANSWER,
    "diagnostics": {
        "skills": ["division.multiplication_relation"],
        "errors": {
            "①": "multiplication.wrong_product",
            "②": "multiplication.wrong_product",
            "④": "multiplication.wrong_product",
            "⑤": "multiplication.wrong_product",
        },
    },
}
