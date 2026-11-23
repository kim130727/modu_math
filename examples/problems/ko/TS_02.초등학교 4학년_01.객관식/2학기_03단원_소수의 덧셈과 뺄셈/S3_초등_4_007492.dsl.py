"""ModuMath Problem DSL: 소수에서 생략할 수 있는 0 찾기 (S3_초등_4_007492)"""

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


PROBLEM_ID = "S3_초등_4_007492"
PROBLEM_TITLE = "소수에서 생략할 수 있는 0이 있는 수 선택하기"

ANSWER = {
    "value": "7.060",
    "answer_index": 1,
    "unit": "",
    "values": ["7.060"],
    "choices": [
        "10.05",
        "7.060",
    ],
    "blanks": [],
    "answer_key": [
        {
            "slot_id": "slot.choice.option_1",
            "value": "7.060",
            "diagnostics": [
                {
                    "id": "diag.middle_zero_error",
                    "condition": "answer_equals_0",
                    "concept": "소수의 끝자리 0 생략",
                    "reason": "일의 자리나 소수 첫째 자리의 0은 생략할 수 없음을 놓침",
                    "feedback": "10.05의 0은 자릿값을 지키기 위해 생략할 수 없습니다. 소수의 오른쪽 끝자리 0만 생략할 수 있으므로 7.060을 선택하세요.",
                },
            ],
        },
    ],
}

SEMANTIC = {
    "problem_id": PROBLEM_ID,
    "problem_type": "multiple_choice_trailing_zero_decimal",
    "metadata": {
        "school": "초등학교",
        "grade": 4,
        "semester": "2학기",
        "chapter": "03단원_소수의 덧셈과 뺄셈",
        "difficulty": "하",
    },
    "entities": {
        "num_0": {"label": "10.05", "has_trailing_zero": False},
        "num_1": {"label": "7.060", "has_trailing_zero": True},
    },
    "relations": [
        {
            "type": "property_check",
            "property": "omittable_trailing_zero",
            "correct_entity": "num_1",
            "distractor": "num_0",
        }
    ],
}


def build_problem_template() -> ProblemTemplate:
    stem_text_slot = TextBoxSlot(
        id="slot.stem.question",
        prompt="",
        text="14. 소수에서 생략할 수 있는 0이 있는 것을 선택하세요.",
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

    choice_0 = RectSlot(id="slot.choice.option_0", prompt="", x=164, y=148, width=228, height=74, fill="#f3e8d2", stroke="#b45309", stroke_width=1.8, rx=8, ry=8, interaction={"type": "choice", "role": "answer", "choice_index": 0, "value": "10.05", "group_id": "slot.choice.group", "include_in_submission": True})
    choice_1 = RectSlot(id="slot.choice.option_1", prompt="", x=494, y=148, width=228, height=74, fill="#f3e8d2", stroke="#b45309", stroke_width=1.8, rx=8, ry=8, interaction={"type": "choice", "role": "answer", "choice_index": 1, "value": "7.060", "group_id": "slot.choice.group", "include_in_submission": True})

    diagram_slots = [
        CircleSlot(id="slot.diagram.rabbit", prompt="", cx=278, cy=114, r=24, fill="#ddd6fe", stroke="#7c3aed", stroke_width=1.4),
        TextSlot(id="slot.diagram.num_0", prompt="", text="10.05", x=278, y=172, font_size=24, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center"),

        CircleSlot(id="slot.diagram.puppy", prompt="", cx=608, cy=114, r=24, fill="#fed7aa", stroke="#c2410c", stroke_width=1.4),
        TextSlot(id="slot.diagram.num_1", prompt="", text="7.060", x=608, y=172, font_size=24, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center"),
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
        {"ref": "num_0", "value": "10.05"},
        {"ref": "num_1", "value": "7.060"},
    ],
    "target": {"ref": "slot.choice.option_1", "label": "생략할 수 있는 0이 있는 소수", "unit": ""},
    "method": "decimal_property",
    "steps": [
        {
            "id": "find_trailing_zero",
            "expr": "7.060 = 7.06",
            "explanation": "소수의 오른쪽 끝자리 0만 생략할 수 있으므로 7.060입니다.",
            "value": "7.060",
        },
    ],
    "answer": ANSWER,
}


if __name__ == "__main__":
    print(f"[{PROBLEM_TEMPLATE.id}] 템플릿 컴파일 성공!")
