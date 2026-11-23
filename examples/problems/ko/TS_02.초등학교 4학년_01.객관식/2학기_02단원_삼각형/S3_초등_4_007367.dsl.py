"""ModuMath Problem DSL: 세 각의 크기로 이등변삼각형 찾기 (S3_초등_4_007367)"""

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


PROBLEM_ID = "S3_초등_4_007367"
PROBLEM_TITLE = "세 각의 크기를 보고 이등변삼각형 선택하기"

ANSWER = {
    "value": "②",
    "answer_index": 1,
    "unit": "",
    "values": ["②"],
    "choices": [
        "①",
        "②",
    ],
    "blanks": [],
    "answer_key": [
        {
            "slot_id": "slot.choice.option_1",
            "value": "②",
            "diagnostics": [
                {
                    "id": "diag.chose_scalene_angles",
                    "condition": "answer_equals_1",
                    "concept": "이등변삼각형의 각의 성질",
                    "reason": "세 각의 크기가 모두 다른 ①(100°, 55°, 25°)을 선택함",
                    "feedback": "①은 세 각의 크기가 모두 다르므로 이등변삼각형이 아닙니다. 두 각의 크기가 55°로 같은 ②를 선택하세요.",
                },
            ],
        },
    ],
}

SEMANTIC = {
    "problem_id": PROBLEM_ID,
    "problem_type": "multiple_choice_isosceles_by_angles",
    "metadata": {
        "school": "초등학교",
        "grade": 4,
        "semester": "2학기",
        "chapter": "02단원_삼각형",
        "difficulty": "하",
    },
    "entities": {
        "card_0": {"label": "① 100°, 55°, 25°", "angles": [100, 55, 25], "is_isosceles": False},
        "card_1": {"label": "② 55°, 70°, 55°", "angles": [55, 70, 55], "is_isosceles": True},
    },
    "relations": [
        {
            "type": "classification",
            "property": "two_equal_angles",
            "correct_entity": "card_1",
            "distractor": "card_0",
        }
    ],
}


def build_problem_template() -> ProblemTemplate:
    stem_text_slot = TextBoxSlot(
        id="slot.stem.question",
        prompt="",
        text="44. 삼각형의 세 각의 크기가 다음과 같을 때 이등변삼각형을 찾아 선택하세요.",
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

    choice_0 = RectSlot(id="slot.choice.option_0", prompt="", x=142, y=100, width=264, height=156, fill="#f8fafc", stroke="#cbd5e1", stroke_width=1.5, rx=10, ry=10, interaction={"type": "choice", "role": "answer", "choice_index": 0, "value": "①", "group_id": "slot.choice.group", "include_in_submission": True})
    choice_1 = RectSlot(id="slot.choice.option_1", prompt="", x=480, y=100, width=264, height=156, fill="#f8fafc", stroke="#cbd5e1", stroke_width=1.5, rx=10, ry=10, interaction={"type": "choice", "role": "answer", "choice_index": 1, "value": "②", "group_id": "slot.choice.group", "include_in_submission": True})

    diagram_slots = [
        TextSlot(id="slot.diagram.b0", prompt="", text="①", x=162, y=112, font_size=18, font_family='"Noto Sans KR", sans-serif', fill="#4b5563", align="center"),
        CircleSlot(id="slot.diagram.bear", prompt="", cx=274, cy=142, r=24, fill="#fde047", stroke="#b45309", stroke_width=1.4),
        RectSlot(id="slot.diagram.board_0", prompt="", x=164, y=174, width=220, height=58, fill="#f3e8d2", stroke="#b45309", stroke_width=1.6, rx=8, ry=8),
        TextSlot(id="slot.diagram.ang_0", prompt="", text="100°,  55°,  25°", x=274, y=192, font_size=20, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center"),

        TextSlot(id="slot.diagram.b1", prompt="", text="②", x=500, y=112, font_size=18, font_family='"Noto Sans KR", sans-serif', fill="#4b5563", align="center"),
        CircleSlot(id="slot.diagram.squirrel", prompt="", cx=612, cy=142, r=24, fill="#fdba74", stroke="#c2410c", stroke_width=1.4),
        RectSlot(id="slot.diagram.board_1", prompt="", x=502, y=174, width=220, height=58, fill="#f3e8d2", stroke="#b45309", stroke_width=1.6, rx=8, ry=8),
        TextSlot(id="slot.diagram.ang_1", prompt="", text="55°,  70°,  55°", x=612, y=192, font_size=20, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center"),
    ]

    return ProblemTemplate(
        id=PROBLEM_ID,
        title=PROBLEM_TITLE,
        canvas=Canvas(width=886, height=286, coordinate_mode="logical"),
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
        {"ref": "card_0", "value": "100°, 55°, 25°"},
        {"ref": "card_1", "value": "55°, 70°, 55°"},
    ],
    "target": {"ref": "slot.choice.option_1", "label": "이등변삼각형", "unit": ""},
    "method": "triangle_classification",
    "steps": [
        {
            "id": "check_angles",
            "expr": "55° = 55° -> 두 각의 크기가 같음",
            "explanation": "두 각의 크기가 같으면 이등변삼각형이므로 ②입니다.",
            "value": "②",
        },
    ],
    "answer": ANSWER,
}


if __name__ == "__main__":
    print(f"[{PROBLEM_TEMPLATE.id}] 템플릿 컴파일 성공!")
