"""ModuMath Problem DSL: 소수 51.94 바르게 읽기 (S3_초등_4_007499)"""

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


PROBLEM_ID = "S3_초등_4_007499"
PROBLEM_TITLE = "소수 51.94의 바른 읽기 선택하기"

ANSWER = {
    "value": "오십일 점 구사",
    "answer_index": 1,
    "unit": "",
    "values": ["오십일 점 구사"],
    "choices": [
        "오십일 점 구십사",
        "오십일 점 구사",
    ],
    "blanks": [],
    "answer_key": [
        {
            "slot_id": "slot.choice.option_1",
            "value": "오십일 점 구사",
            "diagnostics": [
                {
                    "id": "diag.place_value_after_dot",
                    "condition": "answer_equals_0",
                    "concept": "소수 두 자리 수 읽기",
                    "reason": "소수점 아래에 자릿값('구십사')을 붙여 읽음",
                    "feedback": "소수를 읽을 때는 자연수 부분은 자릿값을 붙여 읽고, 소수점 아래부터는 숫자만 차례로 읽으므로 '오십일 점 구사'라고 읽습니다.",
                },
            ],
        },
    ],
}

SEMANTIC = {
    "problem_id": PROBLEM_ID,
    "problem_type": "multiple_choice_decimal_reading",
    "metadata": {
        "school": "초등학교",
        "grade": 4,
        "semester": "2학기",
        "chapter": "03단원_소수의 덧셈과 뺄셈",
        "difficulty": "하",
    },
    "entities": {
        "decimal_value": {"label": "소수", "value": "51.94"},
        "opt_0": {"label": "오십일 점 구십사", "is_correct": False},
        "opt_1": {"label": "오십일 점 구사", "is_correct": True},
    },
    "relations": [
        {
            "type": "reading_match",
            "target": "decimal_value",
            "correct_entity": "opt_1",
        }
    ],
}


def build_problem_template() -> ProblemTemplate:
    stem_text_slot = TextBoxSlot(
        id="slot.stem.question",
        prompt="",
        text="24. 알맞은 것을 선택하세요.",
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

    diagram_slots = [
        RectSlot(id="slot.diagram.green_box", prompt="", x=78, y=80, width=730, height=58, fill="#ffffff", stroke="#84cc16", stroke_width=2.0),
        TextSlot(id="slot.diagram.sentence", prompt="", text="51.94는 ( 오십일 점 구십사 , 오십일 점 구사 )라고 읽습니다.", x=443, y=98, font_size=21, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center"),

        CircleSlot(id="slot.diagram.girl_head", prompt="", cx=316, cy=204, r=26, fill="#fde68a", stroke="#92400e", stroke_width=1.4),
        RectSlot(id="slot.diagram.bubble", prompt="", x=378, y=156, width=282, height=110, fill="#ffffff", stroke="#111827", stroke_width=1.6, rx=30, ry=30),
        TextBoxSlot(
            id="slot.diagram.bubble_txt",
            prompt="",
            text="자연수 부분은\n자릿값을 붙여 읽고,\n소수점 아래부터는\n숫자만 읽어야 해.",
            x=396,
            y=168,
            width=246,
            height=86,
            font_size=16,
            font_family='"Noto Sans KR", sans-serif',
            fill="#111827",
            align="center",
            valign="middle",
            line_height=1.35,
        ),
    ]

    choice_0 = RectSlot(id="slot.choice.option_0", prompt="", x=178, y=288, width=230, height=48, fill="#f8fafc", stroke="#94a3b8", stroke_width=1.5, rx=8, ry=8, interaction={"type": "choice", "role": "answer", "choice_index": 0, "value": "오십일 점 구십사", "group_id": "slot.choice.group", "include_in_submission": True})
    diagram_slots.append(TextSlot(id="slot.diagram.c0_txt", prompt="", text="오십일 점 구십사", x=293, y=300, font_size=19, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center"))

    choice_1 = RectSlot(id="slot.choice.option_1", prompt="", x=478, y=288, width=230, height=48, fill="#f8fafc", stroke="#94a3b8", stroke_width=1.5, rx=8, ry=8, interaction={"type": "choice", "role": "answer", "choice_index": 1, "value": "오십일 점 구사", "group_id": "slot.choice.group", "include_in_submission": True})
    diagram_slots.append(TextSlot(id="slot.diagram.c1_txt", prompt="", text="오십일 점 구사", x=593, y=300, font_size=19, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center"))

    return ProblemTemplate(
        id=PROBLEM_ID,
        title=PROBLEM_TITLE,
        canvas=Canvas(width=886, height=360, coordinate_mode="logical"),
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
    "given": [{"ref": "decimal_value", "value": "51.94"}],
    "target": {"ref": "slot.choice.option_1", "label": "51.94의 바른 읽기", "unit": ""},
    "method": "decimal_reading",
    "steps": [
        {
            "id": "read_decimal",
            "expr": "51.94 -> 오십일 점 구사",
            "explanation": "자연수 부분은 '오십일', 소수점 아래는 숫자만 '구사'라고 읽습니다.",
            "value": "오십일 점 구사",
        },
    ],
    "answer": ANSWER,
}


if __name__ == "__main__":
    print(f"[{PROBLEM_TEMPLATE.id}] 템플릿 컴파일 성공!")
