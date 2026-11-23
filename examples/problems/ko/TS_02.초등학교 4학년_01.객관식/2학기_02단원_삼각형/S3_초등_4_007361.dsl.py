"""ModuMath Problem DSL: 정삼각형 찾기 (S3_초등_4_007361)"""

from __future__ import annotations

from modu_math.dsl import (
    Canvas,
    PathSlot,
    PolygonSlot,
    ProblemTemplate,
    RectSlot,
    Region,
    TextBoxSlot,
    TextSlot,
)


PROBLEM_ID = "S3_초등_4_007361"
PROBLEM_TITLE = "변의 길이를 보고 정삼각형 찾아 선택하기"

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
                    "id": "diag.chose_isosceles",
                    "condition": "answer_equals_1",
                    "concept": "정삼각형의 성질",
                    "reason": "두 변의 길이만 같은 이등변삼각형(①: 8 cm, 7 cm, 7 cm)을 선택함",
                    "feedback": "①은 두 변의 길이만 7 cm로 같으므로 이등변삼각형입니다. 정삼각형은 세 변의 길이가 모두 9 cm로 같은 ②입니다.",
                },
            ],
        },
    ],
}

SEMANTIC = {
    "problem_id": PROBLEM_ID,
    "problem_type": "multiple_choice_equilateral_triangle",
    "metadata": {
        "school": "초등학교",
        "grade": 4,
        "semester": "2학기",
        "chapter": "02단원_삼각형",
        "difficulty": "하",
    },
    "entities": {
        "tri_0": {"label": "① 8 cm, 7 cm, 7 cm", "sides": [8, 7, 7], "is_equilateral": False},
        "tri_1": {"label": "② 9 cm, 9 cm, 9 cm", "sides": [9, 9, 9], "is_equilateral": True},
    },
    "relations": [
        {
            "type": "classification",
            "property": "three_equal_sides",
            "correct_entity": "tri_1",
            "distractor": "tri_0",
        }
    ],
}


def build_problem_template() -> ProblemTemplate:
    stem_text_slot = TextBoxSlot(
        id="slot.stem.question",
        prompt="",
        text="35. 정삼각형을 찾아 선택하세요.",
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

    choice_0 = RectSlot(id="slot.choice.option_0", prompt="", x=154, y=82, width=250, height=224, fill="#f8fafc", stroke="#cbd5e1", stroke_width=1.5, rx=10, ry=10, interaction={"type": "choice", "role": "answer", "choice_index": 0, "value": "①", "group_id": "slot.choice.group", "include_in_submission": True})
    choice_1 = RectSlot(id="slot.choice.option_1", prompt="", x=482, y=82, width=250, height=224, fill="#f8fafc", stroke="#cbd5e1", stroke_width=1.5, rx=10, ry=10, interaction={"type": "choice", "role": "answer", "choice_index": 1, "value": "②", "group_id": "slot.choice.group", "include_in_submission": True})

    diagram_slots = [
        TextSlot(id="slot.diagram.b0", prompt="", text="①", x=174, y=94, font_size=18, font_family='"Noto Sans KR", sans-serif', fill="#4b5563", align="center"),
        PolygonSlot(id="slot.diagram.tri0", prompt="", points=[(236, 112), (236, 272), (344, 192)], fill="none", stroke="#111827", stroke_width=1.8),
        PathSlot(id="slot.diagram.arc0_l", prompt="", d="M 236 112 Q 204 192 236 272", fill="none", stroke="#38bdf8", stroke_width=1.2, stroke_dasharray="4,4"),
        PathSlot(id="slot.diagram.arc0_t", prompt="", d="M 236 112 Q 305 128 344 192", fill="none", stroke="#38bdf8", stroke_width=1.2, stroke_dasharray="4,4"),
        PathSlot(id="slot.diagram.arc0_b", prompt="", d="M 236 272 Q 305 256 344 192", fill="none", stroke="#38bdf8", stroke_width=1.2, stroke_dasharray="4,4"),
        TextSlot(id="slot.diagram.l0_a", prompt="", text="8 cm", x=196, y=182, font_size=17, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center"),
        TextSlot(id="slot.diagram.l0_b", prompt="", text="7 cm", x=316, y=126, font_size=17, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center"),
        TextSlot(id="slot.diagram.l0_c", prompt="", text="7 cm", x=316, y=242, font_size=17, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center"),

        TextSlot(id="slot.diagram.b1", prompt="", text="②", x=502, y=94, font_size=18, font_family='"Noto Sans KR", sans-serif', fill="#4b5563", align="center"),
        PolygonSlot(id="slot.diagram.tri1", prompt="", points=[(526, 134), (688, 134), (607, 274)], fill="none", stroke="#111827", stroke_width=1.8),
        PathSlot(id="slot.diagram.arc1_t", prompt="", d="M 526 134 Q 607 96 688 134", fill="none", stroke="#38bdf8", stroke_width=1.2, stroke_dasharray="4,4"),
        PathSlot(id="slot.diagram.arc1_l", prompt="", d="M 526 134 Q 536 218 607 274", fill="none", stroke="#38bdf8", stroke_width=1.2, stroke_dasharray="4,4"),
        PathSlot(id="slot.diagram.arc1_r", prompt="", d="M 688 134 Q 678 218 607 274", fill="none", stroke="#38bdf8", stroke_width=1.2, stroke_dasharray="4,4"),
        TextSlot(id="slot.diagram.l1_t", prompt="", text="9 cm", x=607, y=98, font_size=17, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center"),
        TextSlot(id="slot.diagram.l1_l", prompt="", text="9 cm", x=524, y=214, font_size=17, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center"),
        TextSlot(id="slot.diagram.l1_r", prompt="", text="9 cm", x=690, y=214, font_size=17, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center"),
    ]

    return ProblemTemplate(
        id=PROBLEM_ID,
        title=PROBLEM_TITLE,
        canvas=Canvas(width=886, height=330, coordinate_mode="logical"),
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
        {"ref": "tri_0", "value": "8 cm, 7 cm, 7 cm"},
        {"ref": "tri_1", "value": "9 cm, 9 cm, 9 cm"},
    ],
    "target": {"ref": "slot.choice.option_1", "label": "정삼각형", "unit": ""},
    "method": "triangle_classification",
    "steps": [
        {
            "id": "check_sides",
            "expr": "9 cm = 9 cm = 9 cm",
            "explanation": "정삼각형은 세 변의 길이가 모두 같으므로 ②입니다.",
            "value": "②",
        },
    ],
    "answer": ANSWER,
}


if __name__ == "__main__":
    print(f"[{PROBLEM_TEMPLATE.id}] 템플릿 컴파일 성공!")
