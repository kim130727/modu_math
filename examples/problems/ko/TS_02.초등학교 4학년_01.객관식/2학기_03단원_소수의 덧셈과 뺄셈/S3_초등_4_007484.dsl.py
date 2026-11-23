"""ModuMath Problem DSL: 7이 나타내는 수가 0.07인 수 찾기 (S3_초등_4_007484)"""

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


PROBLEM_ID = "S3_초등_4_007484"
PROBLEM_TITLE = "7이 나타내는 수가 0.07인 소수 선택하기"

ANSWER = {
    "value": "3.47",
    "answer_index": 1,
    "unit": "",
    "values": ["3.47"],
    "choices": [
        "0.715",
        "3.47",
        "11.607",
    ],
    "blanks": [],
    "answer_key": [
        {
            "slot_id": "slot.choice.option_1",
            "value": "3.47",
            "diagnostics": [
                {
                    "id": "diag.wrong_place_value",
                    "condition": "answer_not_3.47",
                    "concept": "소수의 자릿값",
                    "reason": "0.07이 나타내는 소수 둘째 자리를 찾지 못함",
                    "feedback": "0.715에서 7은 0.7, 3.47에서 7은 0.07, 11.607에서 7은 0.007을 나타냅니다.",
                },
            ],
        },
    ],
}

SEMANTIC = {
    "problem_id": PROBLEM_ID,
    "problem_type": "multiple_choice_decimal_place_value",
    "metadata": {
        "school": "초등학교",
        "grade": 4,
        "semester": "2학기",
        "chapter": "03단원_소수의 덧셈과 뺄셈",
        "difficulty": "하",
    },
    "entities": {
        "num_0": {"label": "0.715", "digit_7_value": 0.7},
        "num_1": {"label": "3.47", "digit_7_value": 0.07},
        "num_2": {"label": "11.607", "digit_7_value": 0.007},
    },
    "relations": [
        {
            "type": "place_value_match",
            "target_value": 0.07,
            "correct_entity": "num_1",
        }
    ],
}


def build_problem_template() -> ProblemTemplate:
    stem_text_slot = TextBoxSlot(
        id="slot.stem.question",
        prompt="",
        text="5. 7이 나타내는 수가 0.07인 수를 선택해 보세요.",
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

    items = [
        ("0.715", "#ddd6fe", "#7c3aed"),
        ("3.47", "#fef08a", "#a16207"),
        ("11.607", "#fed7aa", "#c2410c"),
    ]
    choice_slots = []
    diagram_slots = []
    for idx, (val, head_fill, head_stroke) in enumerate(items):
        cx = 176 + idx * 267
        diagram_slots.append(CircleSlot(id=f"slot.diagram.animal_{idx}", prompt="", cx=cx, cy=124, r=26, fill=head_fill, stroke=head_stroke, stroke_width=1.4))
        choice_slots.append(
            RectSlot(
                id=f"slot.choice.option_{idx}",
                prompt="",
                x=cx - 104,
                y=158,
                width=208,
                height=68,
                fill="#f3e8d2",
                stroke="#b45309",
                stroke_width=1.8,
                rx=8,
                ry=8,
                interaction={
                    "type": "choice",
                    "role": "answer",
                    "choice_index": idx,
                    "value": val,
                    "group_id": "slot.choice.group",
                    "include_in_submission": True,
                },
            )
        )
        diagram_slots.append(TextSlot(id=f"slot.diagram.val_{idx}", prompt="", text=val, x=cx, y=180, font_size=24, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center"))

    return ProblemTemplate(
        id=PROBLEM_ID,
        title=PROBLEM_TITLE,
        canvas=Canvas(width=886, height=260, coordinate_mode="logical"),
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
        {"ref": "num_0", "value": "0.715"},
        {"ref": "num_1", "value": "3.47"},
        {"ref": "num_2", "value": "11.607"},
    ],
    "target": {"ref": "slot.choice.option_1", "label": "7이 0.07을 나타내는 수", "unit": ""},
    "method": "decimal_place_value",
    "steps": [
        {
            "id": "check_place",
            "expr": "3.47에서 7은 소수 둘째 자리 숫자 -> 0.07",
            "explanation": "7이 소수 둘째 자리에 있는 수는 3.47입니다.",
            "value": "3.47",
        },
    ],
    "answer": ANSWER,
}


if __name__ == "__main__":
    print(f"[{PROBLEM_TEMPLATE.id}] 템플릿 컴파일 성공!")
