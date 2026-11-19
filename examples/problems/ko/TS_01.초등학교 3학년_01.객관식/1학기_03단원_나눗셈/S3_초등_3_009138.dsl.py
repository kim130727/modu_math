"""ModuMath Problem DSL: 몫이 같은 나눗셈식 찾기 (S3_초등_3_009138)"""

from __future__ import annotations

from modu_math.dsl import (
    Canvas,
    ProblemTemplate,
    RectSlot,
    Region,
    TextBoxSlot,
    TextSlot,
)


PROBLEM_ID = "S3_초등_3_009138"
PROBLEM_TITLE = "보기와 몫이 같은 나눗셈식 선택하기"

ANSWER = {
    "type": "choice",
    "value": "18 ÷ 2",
    "unit": "",
    "answer_index": 0,
    "values": ["18 ÷ 2"],
    "blanks": [],
    "choices": [
        {"id": "slot.choice.option_0", "slot_id": "slot.choice.option_0", "text": "18 ÷ 2", "value": "18 ÷ 2"},
        {"id": "slot.choice.option_1", "slot_id": "slot.choice.option_1", "text": "27 ÷ 9", "value": "27 ÷ 9"},
    ],
    "answer_key": [
        {
            "slot_id": "slot.choice.option_0",
            "value": "18 ÷ 2",
        }
    ],
}

SEMANTIC_OVERRIDE = {
    "problem_id": PROBLEM_ID,
    "problem_type": "multiple_choice_division_same_quotient",
    "metadata": {
        "grade": 3,
        "semester": 1,
        "subject": "수학",
        "chapter": "03단원_나눗셈",
        "language": "ko-KR",
    },
    "domain": {
        "objects": [
            {"id": "expr.example", "type": "division", "label": "45 ÷ 5", "dividend": 45, "divisor": 5, "quotient": 9},
            {"id": "expr.option_0", "type": "division", "label": "18 ÷ 2", "dividend": 18, "divisor": 2, "quotient": 9},
            {"id": "expr.option_1", "type": "division", "label": "27 ÷ 9", "dividend": 27, "divisor": 9, "quotient": 3},
        ],
        "relations": [
            {
                "id": "relation.same_quotient",
                "type": "equal_quotient",
                "from_id": "expr.option_0",
                "to_id": "expr.example",
            }
        ],
    },
    "answer": ANSWER,
}


def build_problem_template() -> ProblemTemplate:
    stem_slot = TextBoxSlot(
        id="slot.stem.question",
        prompt="",
        text="93. <보기>와 나눗셈의 몫이 같은 식을 선택하세요.",
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

    example_box = RectSlot(
        id="slot.diagram.example_box",
        prompt="",
        x=110,
        y=76,
        width=210,
        height=115,
        fill="#ffffff",
        stroke="#6b7280",
        stroke_width=1.5,
    )
    example_title = TextSlot(
        id="slot.diagram.example_title",
        prompt="",
        text="<보기>",
        x=162,
        y=108,
        font_size=22,
        font_family='"Noto Sans KR", sans-serif',
        fill="#111827",
        align="center",
    )
    example_expr = TextSlot(
        id="slot.diagram.example_expr",
        prompt="",
        text="45 ÷ 5",
        x=215,
        y=154,
        font_size=24,
        font_family='"Noto Sans KR", sans-serif',
        fill="#111827",
        align="center",
    )

    choice_frame = RectSlot(
        id="slot.diagram.choice_frame",
        prompt="",
        x=500,
        y=92,
        width=320,
        height=76,
        fill="#ffedd5",
        stroke="#f59e0b",
        stroke_width=1.5,
    )
    opt_0 = TextSlot(
        id="slot.choice.option_0",
        prompt="",
        text="18 ÷ 2",
        x=598,
        y=130,
        font_size=24,
        font_family='"Noto Sans KR", sans-serif',
        fill="#111827",
        align="center",
        interaction={"type": "choice", "role": "answer", "choice_index": 0, "value": "18 ÷ 2", "group_id": "slot.choice.group", "include_in_submission": True},
    )
    opt_1 = TextSlot(
        id="slot.choice.option_1",
        prompt="",
        text="27 ÷ 9",
        x=722,
        y=130,
        font_size=24,
        font_family='"Noto Sans KR", sans-serif',
        fill="#111827",
        align="center",
        interaction={"type": "choice", "role": "answer", "choice_index": 1, "value": "27 ÷ 9", "group_id": "slot.choice.group", "include_in_submission": True},
    )

    return ProblemTemplate(
        id=PROBLEM_ID,
        title=PROBLEM_TITLE,
        canvas=Canvas(width=886, height=210, coordinate_mode="logical"),
        regions=(
            Region(id="region.stem", role="stem", flow="absolute", slot_ids=("slot.stem.question",)),
            Region(
                id="region.diagram",
                role="diagram",
                flow="absolute",
                slot_ids=("slot.diagram.example_box", "slot.diagram.example_title", "slot.diagram.example_expr", "slot.diagram.choice_frame"),
            ),
            Region(id="region.choices", role="choices", flow="absolute", slot_ids=("slot.choice.option_0", "slot.choice.option_1")),
        ),
        slots=(stem_slot, example_box, example_title, example_expr, choice_frame, opt_0, opt_1),
    )


PROBLEM_TEMPLATE = build_problem_template()

SOLVABLE = {
    "schema": "modu.solvable.v1.3",
    "problem_id": PROBLEM_ID,
    "given": [
        {"ref": "expr.example", "value": "45 ÷ 5"},
        {"ref": "expr.option_0", "value": "18 ÷ 2"},
        {"ref": "expr.option_1", "value": "27 ÷ 9"},
    ],
    "target": {"ref": "slot.choice.option_0", "type": "choice"},
    "method": "compare_division_quotients",
    "steps": [
        {"id": "step.calc_example", "expr": "45 / 5", "value": 9, "explanation": "45 ÷ 5의 몫은 9입니다."},
        {"id": "step.calc_option_0", "expr": "18 / 2", "value": 9, "explanation": "18 ÷ 2의 몫은 9입니다."},
        {"id": "step.calc_option_1", "expr": "27 / 9", "value": 3, "explanation": "27 ÷ 9의 몫은 3이므로 45 ÷ 5와 몫이 같은 식은 18 ÷ 2입니다."},
    ],
    "answer": ANSWER,
    "diagnostics": {
        "skills": ["division.basic_facts"],
        "errors": {
            "27 ÷ 9": "division.quotient_calculation_error",
        },
    },
}
