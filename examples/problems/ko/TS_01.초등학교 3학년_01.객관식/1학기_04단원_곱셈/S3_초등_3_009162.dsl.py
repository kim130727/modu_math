"""ModuMath Problem DSL: 바르게 계산한 세로셈 선택하기 (S3_초등_3_009162)"""

from __future__ import annotations

from modu_math.dsl import (
    Canvas,
    LineSlot,
    ProblemTemplate,
    RectSlot,
    Region,
    TextBoxSlot,
    TextSlot,
    columnar_number_slots,
)


PROBLEM_ID = "S3_초등_3_009162"
PROBLEM_TITLE = "곱셈 세로셈을 바르게 계산한 것 선택하기"

ANSWER = {
    "type": "choice",
    "value": "72 × 6 = 432",
    "unit": "",
    "answer_index": 1,
    "values": ["72 × 6 = 432"],
    "blanks": [],
    "choices": [
        {"id": "slot.choice.option_0", "slot_id": "slot.choice.option_0", "text": "28 × 5 = 100", "value": "28 × 5 = 100"},
        {"id": "slot.choice.option_1", "slot_id": "slot.choice.option_1", "text": "72 × 6 = 432", "value": "72 × 6 = 432"},
    ],
    "answer_key": [
        {
            "slot_id": "slot.choice.option_1",
            "value": "72 × 6 = 432",
        }
    ],
}

SEMANTIC_OVERRIDE = {
    "problem_id": PROBLEM_ID,
    "problem_type": "multiple_choice_vertical_multiplication",
    "metadata": {
        "grade": 3,
        "semester": 1,
        "subject": "수학",
        "chapter": "04단원_곱셈",
        "language": "ko-KR",
    },
    "domain": {
        "objects": [
            {"id": "expr.option_0", "type": "vertical_multiplication", "label": "28 × 5 = 100", "actual": 140, "is_correct": False},
            {"id": "expr.option_1", "type": "vertical_multiplication", "label": "72 × 6 = 432", "actual": 432, "is_correct": True},
        ],
        "relations": [
            {
                "id": "relation.correct_calculation",
                "type": "is_valid_calculation",
                "from_id": "expr.option_1",
                "to_id": "concept.true_equation",
            }
        ],
    },
    "answer": ANSWER,
}


def build_problem_template() -> ProblemTemplate:
    stem_slot = TextBoxSlot(
        id="slot.stem.question",
        prompt="",
        text="23. 계산을 바르게 한 것을 선택하세요.",
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

    # 왼쪽 세로셈: 28 × 5 = 100 (오답)
    box_0 = RectSlot(
        id="slot.choice.option_0",
        prompt="",
        x=275,
        y=76,
        width=180,
        height=148,
        fill="#f0f9ff",
        stroke="#bae6fd",
        stroke_width=1.5,
        interaction={"type": "choice", "role": "answer", "choice_index": 0, "value": "28 × 5 = 100", "group_id": "slot.choice.group", "include_in_submission": True},
    )
    top_0 = columnar_number_slots(id_prefix="slot.diagram.top0", value="28", right_x=425, y=106, column_width=32, font_size=24)
    mul_0 = TextSlot(id="slot.diagram.mul0", prompt="", text="×", x=320, y=142, font_size=22, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center")
    bot_0 = columnar_number_slots(id_prefix="slot.diagram.bot0", value="5", right_x=425, y=142, column_width=32, font_size=24)
    line_0 = LineSlot(id="slot.diagram.line0", prompt="", x1=308, y1=162, x2=430, y2=162, stroke="#111827", stroke_width=1.5)
    res_0 = columnar_number_slots(id_prefix="slot.diagram.res0", value="100", right_x=425, y=190, column_width=32, font_size=24)

    # 오른쪽 세로셈: 72 × 6 = 432 (정답)
    box_1 = RectSlot(
        id="slot.choice.option_1",
        prompt="",
        x=675,
        y=76,
        width=180,
        height=148,
        fill="#f0f9ff",
        stroke="#bae6fd",
        stroke_width=1.5,
        interaction={"type": "choice", "role": "answer", "choice_index": 1, "value": "72 × 6 = 432", "group_id": "slot.choice.group", "include_in_submission": True},
    )
    top_1 = columnar_number_slots(id_prefix="slot.diagram.top1", value="72", right_x=825, y=106, column_width=32, font_size=24)
    mul_1 = TextSlot(id="slot.diagram.mul1", prompt="", text="×", x=720, y=142, font_size=22, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center")
    bot_1 = columnar_number_slots(id_prefix="slot.diagram.bot1", value="6", right_x=825, y=142, column_width=32, font_size=24)
    line_1 = LineSlot(id="slot.diagram.line1", prompt="", x1=708, y1=162, x2=830, y2=162, stroke="#111827", stroke_width=1.5)
    res_1 = columnar_number_slots(id_prefix="slot.diagram.res1", value="432", right_x=825, y=190, column_width=32, font_size=24)

    diagram_slots = (*top_0, mul_0, *bot_0, line_0, *res_0, *top_1, mul_1, *bot_1, line_1, *res_1)

    return ProblemTemplate(
        id=PROBLEM_ID,
        title=PROBLEM_TITLE,
        canvas=Canvas(width=886, height=245, coordinate_mode="logical"),
        regions=(
            Region(id="region.stem", role="stem", flow="absolute", slot_ids=("slot.stem.question",)),
            Region(id="region.diagram", role="diagram", flow="absolute", slot_ids=tuple(s.id for s in diagram_slots)),
            Region(id="region.choices", role="choices", flow="absolute", slot_ids=("slot.choice.option_0", "slot.choice.option_1")),
        ),
        slots=(stem_slot, box_0, box_1, *diagram_slots),
    )


PROBLEM_TEMPLATE = build_problem_template()

SOLVABLE = {
    "schema": "modu.solvable.v1.3",
    "problem_id": PROBLEM_ID,
    "given": [
        {"ref": "expr.option_0", "value": "28 × 5 = 100"},
        {"ref": "expr.option_1", "value": "72 × 6 = 432"},
    ],
    "target": {"ref": "slot.choice.option_1", "type": "choice"},
    "method": "verify_vertical_multiplication",
    "steps": [
        {"id": "step.calc_0", "expr": "28 * 5", "value": 140, "explanation": "28 × 5 = 140이므로 왼쪽 식은 틀렸습니다."},
        {"id": "step.calc_1", "expr": "72 * 6", "value": 432, "explanation": "72 × 6 = 432이므로 바르게 계산한 것은 오른쪽 식입니다."},
    ],
    "answer": ANSWER,
    "diagnostics": {
        "skills": ["multiplication.two_by_one_with_carry"],
        "errors": {
            "28 × 5 = 100": "multiplication.carry_omission",
        },
    },
}
