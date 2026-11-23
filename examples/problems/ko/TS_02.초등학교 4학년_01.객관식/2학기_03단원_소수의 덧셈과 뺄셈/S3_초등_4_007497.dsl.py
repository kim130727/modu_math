"""ModuMath Problem DSL: 계산 결과가 1.4인 소수의 덧셈 (S3_초등_4_007497)"""

from __future__ import annotations

from modu_math.dsl import (
    Canvas,
    ProblemTemplate,
    RectSlot,
    Region,
    TextBoxSlot,
    TextSlot,
)


PROBLEM_ID = "S3_초등_4_007497"
PROBLEM_TITLE = "소수의 덧셈 중 계산 결과가 1.4인 것 선택하기"

ANSWER = {
    "value": "0.5 + 0.9",
    "answer_index": 1,
    "unit": "",
    "values": ["0.5 + 0.9"],
    "choices": [
        "0.7 + 0.6",
        "0.5 + 0.9",
        "1.3 + 0.4",
    ],
    "blanks": [],
    "answer_key": [
        {
            "slot_id": "slot.choice.option_1",
            "value": "0.5 + 0.9",
            "diagnostics": [
                {
                    "id": "diag.wrong_sum",
                    "condition": "answer_not_1",
                    "concept": "소수 한 자리 수의 덧셈",
                    "reason": "받아올림이 있는 소수의 덧셈 계산 오류",
                    "feedback": "0.7 + 0.6 = 1.3, 0.5 + 0.9 = 1.4, 1.3 + 0.4 = 1.7입니다. 따라서 계산 결과가 1.4인 것은 0.5 + 0.9입니다.",
                },
            ],
        },
    ],
}

SEMANTIC = {
    "problem_id": PROBLEM_ID,
    "problem_type": "multiple_choice_decimal_addition",
    "metadata": {
        "school": "초등학교",
        "grade": 4,
        "semester": "2학기",
        "chapter": "03단원_소수의 덧셈과 뺄셈",
        "difficulty": "하",
    },
    "entities": {
        "expr_0": {"label": "0.7 + 0.6", "value": 1.3},
        "expr_1": {"label": "0.5 + 0.9", "value": 1.4},
        "expr_2": {"label": "1.3 + 0.4", "value": 1.7},
    },
    "relations": [
        {
            "type": "value_match",
            "target_value": 1.4,
            "correct_entity": "expr_1",
        }
    ],
}


def build_problem_template() -> ProblemTemplate:
    stem_text_slot = TextBoxSlot(
        id="slot.stem.question",
        prompt="",
        text="21. 계산 결과가 1.4인 것을 선택하세요.",
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

    exprs = ["0.7 + 0.6", "0.5 + 0.9", "1.3 + 0.4"]
    choice_slots = []
    diagram_slots = []
    for idx, expr in enumerate(exprs):
        cy = 88 + idx * 84
        choice_slots.append(
            RectSlot(
                id=f"slot.choice.option_{idx}",
                prompt="",
                x=318,
                y=cy,
                width=250,
                height=66,
                fill="#ffffff",
                stroke="#f59e0b",
                stroke_width=1.8,
                interaction={
                    "type": "choice",
                    "role": "answer",
                    "choice_index": idx,
                    "value": expr,
                    "group_id": "slot.choice.group",
                    "include_in_submission": True,
                },
            )
        )
        diagram_slots.append(
            TextSlot(
                id=f"slot.diagram.expr_{idx}",
                prompt="",
                text=expr,
                x=443,
                y=cy + 20,
                font_size=24,
                font_family='"Noto Sans KR", sans-serif',
                fill="#111827",
                align="center",
            )
        )

    return ProblemTemplate(
        id=PROBLEM_ID,
        title=PROBLEM_TITLE,
        canvas=Canvas(width=886, height=350, coordinate_mode="logical"),
        regions=(
            Region(id="region.stem", role="stem", flow="absolute", slot_ids=("slot.stem.question",)),
            Region(id="region.choices", role="choices", flow="absolute", slot_ids=tuple(s.id for s in choice_slots)),
            Region(id="region.diagram", role="diagram", flow="absolute", slot_ids=tuple(s.id for s in diagram_slots)),
        ),
        slots=(stem_text_slot, *choice_slots, *diagram_slots),
    )


PROBLEM_TEMPLATE = build_problem_template()
SEMANTIC_OVERRIDE = SEMANTIC
SEMANTIC_ANSWER = ANSWER
SOLVABLE = {
    "schema": "modu.solvable.v1.3",
    "problem_id": PROBLEM_ID,
    "problem_type": SEMANTIC["problem_type"],
    "given": [
        {"ref": "expr_0", "value": "0.7 + 0.6"},
        {"ref": "expr_1", "value": "0.5 + 0.9"},
        {"ref": "expr_2", "value": "1.3 + 0.4"},
    ],
    "target": {"ref": "slot.choice.option_1", "label": "계산 결과가 1.4인 식", "unit": ""},
    "method": "decimal_addition",
    "steps": [
        {
            "id": "compute_sum",
            "expr": "0.5 + 0.9 = 1.4",
            "explanation": "계산 결과가 1.4인 것은 0.5 + 0.9입니다.",
            "value": "0.5 + 0.9",
        },
    ],
    "answer": ANSWER,
}


if __name__ == "__main__":
    print(f"[{PROBLEM_TEMPLATE.id}] 템플릿 컴파일 성공!")
