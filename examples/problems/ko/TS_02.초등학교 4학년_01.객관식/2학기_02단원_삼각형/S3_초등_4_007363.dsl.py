"""ModuMath Problem DSL: 이등변삼각형의 길이 고르기 (S3_초등_4_007363)"""

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


PROBLEM_ID = "S3_초등_4_007363"
PROBLEM_TITLE = "삼각형의 세 변의 길이를 보고 이등변삼각형을 들고 있는 사람 선택하기"

ANSWER = {
    "value": "미희",
    "answer_index": 0,
    "unit": "",
    "values": ["미희"],
    "choices": [
        "미희",
        "선우",
    ],
    "blanks": [],
    "answer_key": [
        {
            "slot_id": "slot.choice.option_0",
            "value": "미희",
            "diagnostics": [
                {
                    "id": "diag.chose_scalene",
                    "condition": "answer_equals_sunwoo",
                    "concept": "이등변삼각형의 성질",
                    "reason": "세 변의 길이가 모두 다른 선우(9 cm, 8 cm, 4 cm)를 선택함",
                    "feedback": "선우가 든 길이는 9 cm, 8 cm, 4 cm로 세 변의 길이가 모두 다릅니다. 두 변의 길이가 9 cm로 같은 미희를 선택하세요.",
                },
            ],
        },
    ],
}

SEMANTIC = {
    "problem_id": PROBLEM_ID,
    "problem_type": "multiple_choice_isosceles_lengths",
    "metadata": {
        "school": "초등학교",
        "grade": 4,
        "semester": "2학기",
        "chapter": "02단원_삼각형",
        "difficulty": "하",
    },
    "entities": {
        "mihee": {"label": "미희", "sides": [5, 9, 9], "is_isosceles": True},
        "sunwoo": {"label": "선우", "sides": [9, 8, 4], "is_isosceles": False},
    },
    "relations": [
        {
            "type": "classification",
            "property": "two_equal_sides",
            "correct_entity": "mihee",
            "distractor": "sunwoo",
        }
    ],
}


def build_problem_template() -> ProblemTemplate:
    stem_text_slot = TextBoxSlot(
        id="slot.stem.question",
        prompt="",
        text="38. 삼각형의 세 변의 길이가 다음과 같을 때 이등변삼각형의 길이를 들고 있는 사람을 선택해 보세요.",
        x=32,
        y=24,
        width=820,
        height=64,
        font_size=22,
        font_family='"Noto Sans KR", sans-serif',
        fill="#202124",
        align="left",
        valign="top",
        line_height=1.5,
    )

    choice_0 = RectSlot(id="slot.choice.option_0", prompt="", x=244, y=244, width=108, height=44, fill="#ffffff", stroke="#fb923c", stroke_width=2.0, rx=8, ry=8, interaction={"type": "choice", "role": "answer", "choice_index": 0, "value": "미희", "group_id": "slot.choice.group", "include_in_submission": True})
    choice_1 = RectSlot(id="slot.choice.option_1", prompt="", x=534, y=244, width=108, height=44, fill="#ffffff", stroke="#fb923c", stroke_width=2.0, rx=8, ry=8, interaction={"type": "choice", "role": "answer", "choice_index": 1, "value": "선우", "group_id": "slot.choice.group", "include_in_submission": True})

    diagram_slots = [
        # 미희 캐릭터 및 나무판
        CircleSlot(id="slot.diagram.face_0", prompt="", cx=298, cy=136, r=24, fill="#fde68a", stroke="#d97706", stroke_width=1.5),
        RectSlot(id="slot.diagram.board_0", prompt="", x=174, y=172, width=248, height=58, fill="#f3e8d2", stroke="#b45309", stroke_width=1.6, rx=8, ry=8),
        TextSlot(id="slot.diagram.len_0", prompt="", text="5 cm, 9 cm, 9 cm", x=298, y=190, font_size=20, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center"),
        TextSlot(id="slot.diagram.name_0", prompt="", text="미희", x=298, y=254, font_size=20, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center"),

        # 선우 캐릭터 및 나무판
        CircleSlot(id="slot.diagram.face_1", prompt="", cx=588, cy=136, r=24, fill="#fde68a", stroke="#15803d", stroke_width=1.5),
        RectSlot(id="slot.diagram.board_1", prompt="", x=464, y=172, width=248, height=58, fill="#f3e8d2", stroke="#b45309", stroke_width=1.6, rx=8, ry=8),
        TextSlot(id="slot.diagram.len_1", prompt="", text="9 cm, 8 cm, 4 cm", x=588, y=190, font_size=20, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center"),
        TextSlot(id="slot.diagram.name_1", prompt="", text="선우", x=588, y=254, font_size=20, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center"),
    ]

    return ProblemTemplate(
        id=PROBLEM_ID,
        title=PROBLEM_TITLE,
        canvas=Canvas(width=886, height=320, coordinate_mode="logical"),
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
        {"ref": "mihee", "value": "5 cm, 9 cm, 9 cm"},
        {"ref": "sunwoo", "value": "9 cm, 8 cm, 4 cm"},
    ],
    "target": {"ref": "slot.choice.option_0", "label": "이등변삼각형을 들고 있는 사람", "unit": ""},
    "method": "triangle_classification",
    "steps": [
        {
            "id": "compare_sides",
            "expr": "5 cm, 9 cm, 9 cm -> 두 변이 9 cm로 같음",
            "explanation": "두 변의 길이가 같은 삼각형은 이등변삼각형이므로 미희입니다.",
            "value": "미희",
        },
    ],
    "answer": ANSWER,
}


if __name__ == "__main__":
    print(f"[{PROBLEM_TEMPLATE.id}] 템플릿 컴파일 성공!")
