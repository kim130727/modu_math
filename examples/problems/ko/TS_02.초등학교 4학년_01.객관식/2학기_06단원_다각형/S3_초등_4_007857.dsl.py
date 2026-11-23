"""ModuMath Problem DSL: 모양 조각으로 오각형 만들기 (S3_초등_4_007857)"""

from __future__ import annotations

from modu_math.dsl import (
    Canvas,
    PolygonSlot,
    ProblemTemplate,
    RectSlot,
    Region,
    TextBoxSlot,
    TextSlot,
)


PROBLEM_ID = "S3_초등_4_007857"
PROBLEM_TITLE = "주어진 모양 조각을 모두 사용하여 오각형을 만들 수 있는지 선택하기"

ANSWER = {
    "value": "○",
    "answer_index": 0,
    "unit": "",
    "values": ["○"],
    "choices": [
        "○",
        "×",
    ],
    "blanks": [],
    "answer_key": [
        {
            "slot_id": "slot.choice.option_0",
            "value": "○",
            "diagnostics": [
                {
                    "id": "diag.missed_pentagon_construction",
                    "condition": "answer_equals_x",
                    "concept": "모양 조각으로 다각형 만들기",
                    "reason": "정삼각형 2개, 마름모 1개, 사다리꼴 1개로 오각형을 만들 수 있음을 놓침",
                    "feedback": "정삼각형 2개, 평행사변형(마름모) 1개, 사다리꼴 1개를 이어 붙이면 오각형을 만들 수 있으므로 ○입니다.",
                },
            ],
        },
    ],
}

SEMANTIC = {
    "problem_id": PROBLEM_ID,
    "problem_type": "multiple_choice_polygon_construction_ox",
    "metadata": {
        "school": "초등학교",
        "grade": 4,
        "semester": "2학기",
        "chapter": "06단원_다각형",
        "difficulty": "중",
    },
    "entities": {
        "pieces": {"label": "모양 조각", "items": ["정삼각형 2개", "사다리꼴 1개", "평행사변형 1개"]},
        "target_shape": {"label": "만들 도형", "value": "오각형", "possible": True},
    },
    "relations": [
        {
            "type": "constructibility",
            "pieces": "pieces",
            "target": "target_shape",
            "result": True,
        }
    ],
}


def build_problem_template() -> ProblemTemplate:
    stem_text_slot = TextBoxSlot(
        id="slot.stem.question",
        prompt="",
        text="71. 다음 모양 조각을 모두 사용하여 오각형을 만들 수 있으면 ○, 만들 수 없으면 ×를 선택하세요.",
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

    diagram_slots = [
        PolygonSlot(id="slot.diagram.tri1", prompt="", points=[(216, 108), (186, 160), (246, 160)], fill="#4ade80", stroke="#15803d", stroke_width=1.6),
        PolygonSlot(id="slot.diagram.tri2", prompt="", points=[(346, 108), (316, 160), (376, 160)], fill="#4ade80", stroke="#15803d", stroke_width=1.6),
        PolygonSlot(id="slot.diagram.trap", prompt="", points=[(466, 108), (526, 108), (556, 160), (436, 160)], fill="#fb7185", stroke="#be123c", stroke_width=1.6),
        PolygonSlot(id="slot.diagram.para", prompt="", points=[(646, 108), (706, 108), (676, 160), (616, 160)], fill="#38bdf8", stroke="#0284c7", stroke_width=1.6),
    ]

    choice_0 = RectSlot(id="slot.choice.option_0", prompt="", x=286, y=200, width=124, height=56, fill="#f8fafc", stroke="#94a3b8", stroke_width=1.6, rx=10, ry=10, interaction={"type": "choice", "role": "answer", "choice_index": 0, "value": "○", "group_id": "slot.choice.group", "include_in_submission": True})
    diagram_slots.append(TextSlot(id="slot.diagram.c0_t", prompt="", text="○", x=348, y=214, font_size=26, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center"))

    choice_1 = RectSlot(id="slot.choice.option_1", prompt="", x=476, y=200, width=124, height=56, fill="#f8fafc", stroke="#94a3b8", stroke_width=1.6, rx=10, ry=10, interaction={"type": "choice", "role": "answer", "choice_index": 1, "value": "×", "group_id": "slot.choice.group", "include_in_submission": True})
    diagram_slots.append(TextSlot(id="slot.diagram.c1_t", prompt="", text="×", x=538, y=214, font_size=26, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center"))

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
    "given": [{"ref": "pieces", "value": "정삼각형 2개, 사다리꼴 1개, 평행사변형 1개"}],
    "target": {"ref": "slot.choice.option_0", "label": "오각형 만들기 가능 여부", "unit": ""},
    "method": "shape_composition",
    "steps": [
        {
            "id": "check_pentagon",
            "expr": "정삼각형 2개 + 평행사변형 1개 + 사다리꼴 1개 -> 오각형 가능",
            "explanation": "주어진 모양 조각을 모두 사용하여 오각형을 만들 수 있으므로 ○입니다.",
            "value": "○",
        },
    ],
    "answer": ANSWER,
}


if __name__ == "__main__":
    print(f"[{PROBLEM_TEMPLATE.id}] 템플릿 컴파일 성공!")
