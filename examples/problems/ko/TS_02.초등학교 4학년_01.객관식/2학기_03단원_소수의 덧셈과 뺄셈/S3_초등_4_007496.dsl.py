"""ModuMath Problem DSL: 0.94와 같은 수 찾기 (S3_초등_4_007496)"""

from __future__ import annotations

from modu_math.dsl import (
    Canvas,
    LineSlot,
    ProblemTemplate,
    RectSlot,
    Region,
    TextBoxSlot,
    TextSlot,
)


PROBLEM_ID = "S3_초등_4_007496"
PROBLEM_TITLE = "0.94와 같은 수 선택하기"

ANSWER = {
    "value": "①",
    "answer_index": 0,
    "unit": "",
    "values": ["①"],
    "choices": [
        "①",
        "②",
    ],
    "blanks": [],
    "answer_key": [
        {
            "slot_id": "slot.choice.option_0",
            "value": "①",
            "diagnostics": [
                {
                    "id": "diag.decimal_shift_error",
                    "condition": "answer_equals_2",
                    "concept": "소수의 10배, 100배, 1/10",
                    "reason": "0.094의 100배를 0.94로 잘못 계산함",
                    "feedback": "0.094의 100배는 소수점이 오른쪽으로 두 자리 이동하므로 9.4입니다. 9.4의 1/10은 소수점이 왼쪽으로 한 자리 이동하므로 0.94입니다.",
                },
            ],
        },
    ],
}

SEMANTIC = {
    "problem_id": PROBLEM_ID,
    "problem_type": "multiple_choice_decimal_scaling",
    "metadata": {
        "school": "초등학교",
        "grade": 4,
        "semester": "2학기",
        "chapter": "03단원_소수의 덧셈과 뺄셈",
        "difficulty": "중",
    },
    "entities": {
        "target": {"label": "기준 수", "value": 0.94},
        "expr_0": {"label": "① 9.4의 1/10", "value": 0.94},
        "expr_1": {"label": "② 0.094의 100배", "value": 9.4},
    },
    "relations": [
        {
            "type": "equality",
            "target": "target",
            "correct_entity": "expr_0",
        }
    ],
}


def build_problem_template() -> ProblemTemplate:
    stem_text_slot = TextBoxSlot(
        id="slot.stem.question",
        prompt="",
        text="20. 0.94와 같은 수를 찾아 선택하세요.",
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

    choice_0 = RectSlot(id="slot.choice.option_0", prompt="", x=126, y=94, width=284, height=118, fill="#ffffff", stroke="#a78bfa", stroke_width=1.8, interaction={"type": "choice", "role": "answer", "choice_index": 0, "value": "①", "group_id": "slot.choice.group", "include_in_submission": True})
    choice_1 = RectSlot(id="slot.choice.option_1", prompt="", x=476, y=94, width=284, height=118, fill="#ffffff", stroke="#a78bfa", stroke_width=1.8, interaction={"type": "choice", "role": "answer", "choice_index": 1, "value": "②", "group_id": "slot.choice.group", "include_in_submission": True})

    diagram_slots = [
        TextSlot(id="slot.diagram.b0", prompt="", text="①", x=146, y=106, font_size=18, font_family='"Noto Sans KR", sans-serif', fill="#4b5563", align="center"),
        TextSlot(id="slot.diagram.l0_a", prompt="", text="9.4의", x=244, y=140, font_size=22, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center"),
        TextSlot(id="slot.diagram.l0_n", prompt="", text="1", x=298, y=120, font_size=19, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center"),
        LineSlot(id="slot.diagram.l0_bar", prompt="", x1=280, y1=146, x2=316, y2=146, stroke="#111827", stroke_width=1.5),
        TextSlot(id="slot.diagram.l0_d", prompt="", text="10", x=298, y=152, font_size=19, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center"),

        TextSlot(id="slot.diagram.b1", prompt="", text="②", x=496, y=106, font_size=18, font_family='"Noto Sans KR", sans-serif', fill="#4b5563", align="center"),
        TextSlot(id="slot.diagram.r0", prompt="", text="0.094의 100배", x=618, y=140, font_size=22, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center"),
    ]

    return ProblemTemplate(
        id=PROBLEM_ID,
        title=PROBLEM_TITLE,
        canvas=Canvas(width=886, height=240, coordinate_mode="logical"),
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
        {"ref": "expr_0", "value": "9.4의 1/10"},
        {"ref": "expr_1", "value": "0.094의 100배"},
    ],
    "target": {"ref": "slot.choice.option_0", "label": "0.94와 같은 수", "unit": ""},
    "method": "decimal_scaling",
    "steps": [
        {
            "id": "shift_decimal",
            "expr": "9.4 × 1/10 = 0.94, 0.094 × 100 = 9.4",
            "explanation": "9.4의 1/10은 0.94이므로 ①입니다.",
            "value": "①",
        },
    ],
    "answer": ANSWER,
}


if __name__ == "__main__":
    print(f"[{PROBLEM_TEMPLATE.id}] 템플릿 컴파일 성공!")
