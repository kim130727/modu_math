"""ModuMath Problem DSL: 모양 조각 설명 바른 사람 고르기 (S3_초등_4_007859)"""

from __future__ import annotations

from modu_math.dsl import (
    Canvas,
    CircleSlot,
    LineSlot,
    PolygonSlot,
    ProblemTemplate,
    RectSlot,
    Region,
    TextBoxSlot,
    TextSlot,
)


PROBLEM_ID = "S3_초등_4_007859"
PROBLEM_TITLE = "모양 조각으로 만든 거북 모양을 바르게 설명한 사람 선택하기"

ANSWER = {
    "value": "민지",
    "answer_index": 0,
    "unit": "",
    "values": ["민지"],
    "choices": [
        "민지",
        "도영",
    ],
    "blanks": [],
    "answer_key": [
        {
            "slot_id": "slot.choice.option_0",
            "value": "민지",
            "diagnostics": [
                {
                    "id": "diag.chose_hexagon_claim",
                    "condition": "answer_equals_doyoung",
                    "concept": "모양 조각 분류",
                    "reason": "육각형 모양 조각을 사용하지 않았는데 육각형을 사용했다고 말한 도영을 선택함",
                    "feedback": "거북 모양을 만드는 데 사용한 조각은 삼각형과 사각형뿐입니다. 육각형 모양 조각은 사용하지 않았으므로 바르게 설명한 사람은 민지입니다.",
                },
            ],
        },
    ],
}

SEMANTIC = {
    "problem_id": PROBLEM_ID,
    "problem_type": "multiple_choice_pattern_block_explanation",
    "metadata": {
        "school": "초등학교",
        "grade": 4,
        "semester": "2학기",
        "chapter": "06단원_다각형",
        "difficulty": "중",
    },
    "entities": {
        "minji": {"label": "민지", "claim": "거북 모양을 만들었어.", "is_correct": True},
        "doyoung": {"label": "도영", "claim": "삼각형, 사각형, 육각형 모양 조각을 사용하여 만들었어.", "is_correct": False},
    },
    "relations": [
        {
            "type": "truth_evaluation",
            "correct_entity": "minji",
            "distractor": "doyoung",
        }
    ],
}


def build_problem_template() -> ProblemTemplate:
    stem_text_slot = TextBoxSlot(
        id="slot.stem.question",
        prompt="",
        text="74. 모양 조각으로 다음과 같은 모양을 만들었습니다. 바르게 설명한 사람을 선택하세요.",
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

    choice_0 = RectSlot(id="slot.choice.option_0", prompt="", x=84, y=244, width=90, height=40, fill="#ffffff", stroke="#d8b4fe", stroke_width=1.8, rx=8, ry=8, interaction={"type": "choice", "role": "answer", "choice_index": 0, "value": "민지", "group_id": "slot.choice.group", "include_in_submission": True})
    choice_1 = RectSlot(id="slot.choice.option_1", prompt="", x=708, y=244, width=90, height=40, fill="#ffffff", stroke="#d8b4fe", stroke_width=1.8, rx=8, ry=8, interaction={"type": "choice", "role": "answer", "choice_index": 1, "value": "도영", "group_id": "slot.choice.group", "include_in_submission": True})

    diagram_slots = [
        # 민지 말풍선 & 얼굴
        RectSlot(id="slot.diagram.bub_0", prompt="", x=72, y=104, width=164, height=78, fill="#ffffff", stroke="#111827", stroke_width=1.5, rx=28, ry=28),
        TextBoxSlot(id="slot.diagram.bub_txt_0", prompt="", text="거북 모양을\n만들었어.", x=84, y=116, width=140, height=54, font_size=17, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center", valign="middle", line_height=1.4),
        CircleSlot(id="slot.diagram.face_0", prompt="", cx=198, cy=210, r=24, fill="#fde68a", stroke="#92400e", stroke_width=1.4),
        TextSlot(id="slot.diagram.name_0", prompt="", text="민지", x=129, y=253, font_size=19, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center"),

        # 거북 모양
        PolygonSlot(id="slot.diagram.head", prompt="", points=[(302, 160), (344, 160), (364, 198), (322, 198)], fill="#38bdf8", stroke="#0284c7", stroke_width=1.4),
        PolygonSlot(id="slot.diagram.shell", prompt="", points=[(406, 122), (468, 122), (510, 198), (364, 198)], fill="#4ade80", stroke="#15803d", stroke_width=1.4),
        LineSlot(id="slot.diagram.sh_l1", prompt="", x1=385, y1=160, x2=489, y2=160, stroke="#15803d", stroke_width=1.2),
        LineSlot(id="slot.diagram.sh_l2", prompt="", x1=406, y1=122, x2=448, y2=198, stroke="#15803d", stroke_width=1.2),
        LineSlot(id="slot.diagram.sh_l3", prompt="", x1=468, y1=122, x2=426, y2=198, stroke="#15803d", stroke_width=1.2),
        PolygonSlot(id="slot.diagram.leg_l", prompt="", points=[(364, 198), (406, 198), (364, 218), (322, 218)], fill="#cbd5e1", stroke="#64748b", stroke_width=1.4),
        PolygonSlot(id="slot.diagram.leg_r", prompt="", points=[(468, 198), (510, 198), (552, 218), (510, 218)], fill="#cbd5e1", stroke="#64748b", stroke_width=1.4),

        # 도영 말풍선 & 얼굴
        RectSlot(id="slot.diagram.bub_1", prompt="", x=604, y=94, width=224, height=96, fill="#ffffff", stroke="#111827", stroke_width=1.5, rx=30, ry=30),
        TextBoxSlot(id="slot.diagram.bub_txt_1", prompt="", text="삼각형, 사각형, 육각형\n모양 조각을 사용하여\n만들었어.", x=614, y=104, width=204, height=76, font_size=16, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center", valign="middle", line_height=1.35),
        CircleSlot(id="slot.diagram.face_1", prompt="", cx=666, cy=210, r=24, fill="#fde68a", stroke="#0284c7", stroke_width=1.4),
        TextSlot(id="slot.diagram.name_1", prompt="", text="도영", x=753, y=253, font_size=19, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center"),
    ]

    return ProblemTemplate(
        id=PROBLEM_ID,
        title=PROBLEM_TITLE,
        canvas=Canvas(width=886, height=304, coordinate_mode="logical"),
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
        {"ref": "minji", "value": "거북 모양을 만들었어."},
        {"ref": "doyoung", "value": "삼각형, 사각형, 육각형 모양 조각을 사용하여 만들었어."},
    ],
    "target": {"ref": "slot.choice.option_0", "label": "바르게 설명한 사람", "unit": ""},
    "method": "truth_evaluation",
    "steps": [
        {
            "id": "verify_pieces",
            "expr": "사용한 조각 = 삼각형, 사각형 (육각형 미사용)",
            "explanation": "육각형 모양 조각은 사용하지 않았으므로 바르게 설명한 사람은 민지입니다.",
            "value": "민지",
        },
    ],
    "answer": ANSWER,
}


if __name__ == "__main__":
    print(f"[{PROBLEM_TEMPLATE.id}] 템플릿 컴파일 성공!")
