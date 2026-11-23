"""ModuMath Problem DSL: 소수의 덧셈과 뺄셈 크기 비교 (S3_초등_4_007491)"""

from __future__ import annotations

from modu_math.dsl import (
    Canvas,
    CircleSlot,
    ProblemTemplate,
    RectSlot,
    Region,
    TextBoxSlot,
    TextSlot,
)


PROBLEM_ID = "S3_초등_4_007491"
PROBLEM_TITLE = "소수의 덧셈과 뺄셈 중 계산 결과가 더 큰 것 선택하기"

ANSWER = {
    "value": "4 - 1.6",
    "answer_index": 1,
    "unit": "",
    "values": ["4 - 1.6"],
    "choices": [
        "0.7 + 1.4",
        "4 - 1.6",
    ],
    "blanks": [],
    "answer_key": [
        {
            "slot_id": "slot.choice.option_1",
            "value": "4 - 1.6",
            "diagnostics": [
                {
                    "id": "diag.calculation_error",
                    "condition": "answer_equals_0",
                    "concept": "소수의 덧셈과 뺄셈",
                    "reason": "0.7 + 1.4 = 2.1과 4 - 1.6 = 2.4의 크기 비교 오류",
                    "feedback": "0.7 + 1.4 = 2.1이고, 4 - 1.6 = 2.4입니다. 2.1 < 2.4이므로 계산 결과가 더 큰 것은 4 - 1.6입니다.",
                },
            ],
        },
    ],
}

SEMANTIC = {
    "problem_id": PROBLEM_ID,
    "problem_type": "multiple_choice_decimal_comparison",
    "metadata": {
        "school": "초등학교",
        "grade": 4,
        "semester": "2학기",
        "chapter": "03단원_소수의 덧셈과 뺄셈",
        "difficulty": "중",
    },
    "entities": {
        "expr_0": {"label": "0.7 + 1.4", "value": 2.1},
        "expr_1": {"label": "4 - 1.6", "value": 2.4},
    },
    "relations": [
        {
            "type": "comparison",
            "operator": ">",
            "larger": "expr_1",
            "smaller": "expr_0",
        }
    ],
}


def build_problem_template() -> ProblemTemplate:
    stem_text_slot = TextBoxSlot(
        id="slot.stem.question",
        prompt="",
        text="13. 계산 결과가 더 큰 것을 선택하세요.",
        x=32,
        y=24,
        width=820,
        height=44,
        font_size=22,
        font_family='"Noto Sans KR", sans-serif',
        fill="#202124",
        align="left",
        valign="top",
        line_height=1.5,
    )

    choice_0 = RectSlot(id="slot.choice.option_0", prompt="", x=164, y=148, width=228, height=74, fill="#f3e8d2", stroke="#b45309", stroke_width=1.8, rx=8, ry=8, interaction={"type": "choice", "role": "answer", "choice_index": 0, "value": "0.7 + 1.4", "group_id": "slot.choice.group", "include_in_submission": True})
    choice_1 = RectSlot(id="slot.choice.option_1", prompt="", x=494, y=148, width=228, height=74, fill="#f3e8d2", stroke="#b45309", stroke_width=1.8, rx=8, ry=8, interaction={"type": "choice", "role": "answer", "choice_index": 1, "value": "4 - 1.6", "group_id": "slot.choice.group", "include_in_submission": True})

    diagram_slots = [
        CircleSlot(id="slot.diagram.bear", prompt="", cx=278, cy=114, r=24, fill="#fde047", stroke="#b45309", stroke_width=1.4),
        TextSlot(id="slot.diagram.expr_0", prompt="", text="0.7 + 1.4", x=278, y=172, font_size=24, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center"),

        CircleSlot(id="slot.diagram.squirrel", prompt="", cx=608, cy=114, r=24, fill="#fdba74", stroke="#c2410c", stroke_width=1.4),
        TextSlot(id="slot.diagram.expr_1", prompt="", text="4 - 1.6", x=608, y=172, font_size=24, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center"),
    ]

    return ProblemTemplate(
        id=PROBLEM_ID,
        title=PROBLEM_TITLE,
        canvas=Canvas(width=886, height=256, coordinate_mode="logical"),
        regions=(
            Region(id="region.stem", role="stem", flow="absolute", slot_ids=("slot.stem.question",)),
            Region(id="region.choices", role="choices", flow="absolute", slot_ids=("slot.choice.option_0", "slot.choice.option_1")),
            Region(id="region.diagram", role="diagram", flow="absolute", slot_ids=tuple(s.id for s in diagram_slots)),
        ),
        slots=(stem_text_slot, choice_0, choice_1, *diagram_slots),
    )


PROBLEM_TEMPLATE = build_problem_template()
SEMANTIC_OVERRIDE = SEMANTIC
SEMANTIC_ANSWER = ANSWER
SOLVABLE = {
    "schema": "modu.solvable.v1.3",
    "problem_id": PROBLEM_ID,
    "problem_type": SEMANTIC["problem_type"],
    "given": [
        {"ref": "expr_0", "value": "0.7 + 1.4"},
        {"ref": "expr_1", "value": "4 - 1.6"},
    ],
    "target": {"ref": "slot.choice.option_1", "label": "계산 결과가 더 큰 것", "unit": ""},
    "method": "decimal_arithmetic",
    "steps": [
        {
            "id": "calc_and_compare",
            "expr": "0.7 + 1.4 = 2.1, 4 - 1.6 = 2.4 -> 2.1 < 2.4",
            "explanation": "계산 결과를 비교하면 2.4가 더 크므로 4 - 1.6입니다.",
            "value": "4 - 1.6",
        },
    ],
    "answer": ANSWER,
}


if __name__ == "__main__":
    print(f"[{PROBLEM_TEMPLATE.id}] 템플릿 컴파일 성공!")
