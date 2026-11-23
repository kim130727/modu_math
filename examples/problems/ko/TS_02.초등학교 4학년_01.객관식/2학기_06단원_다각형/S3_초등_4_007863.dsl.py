"""ModuMath Problem DSL: 정삼각형 만들기 2 (S3_초등_4_007863)"""

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


PROBLEM_ID = "S3_초등_4_007863"
PROBLEM_TITLE = "정삼각형을 만들 때 평행사변형 1개와 함께 필요한 모양 조각과 개수 선택하기"

ANSWER = {
    "value": "②",
    "answer_index": 1,
    "unit": "",
    "values": ["②"],
    "choices": [
        "① 사다리꼴, 2개",
        "② 정삼각형, 2개",
        "③ 정삼각형, 3개",
        "④ 사다리꼴, 1개",
    ],
    "blanks": [],
    "answer_key": [
        {
            "slot_id": "slot.choice.option_1",
            "value": "②",
            "diagnostics": [
                {
                    "id": "diag.wrong_piece_or_count",
                    "condition": "answer_not_2",
                    "concept": "모양 조각으로 정삼각형 만들기",
                    "reason": "평행사변형 1개(정삼각형 2개 크기)에 정삼각형 2개를 붙이면 큰 정삼각형(정삼각형 4개 크기)이 됨을 놓침",
                    "feedback": "평행사변형 1개에 정삼각형 모양 조각 2개를 붙이면 큰 정삼각형을 만들 수 있습니다. 따라서 ②를 선택하세요.",
                },
            ],
        },
    ],
}

SEMANTIC = {
    "problem_id": PROBLEM_ID,
    "problem_type": "multiple_choice_triangle_composition",
    "metadata": {
        "school": "초등학교",
        "grade": 4,
        "semester": "2학기",
        "chapter": "06단원_다각형",
        "difficulty": "중",
    },
    "entities": {
        "given_piece": {"label": "평행사변형 1개"},
        "needed": {"label": "정삼각형", "count": 2},
    },
    "relations": [
        {
            "type": "composition",
            "base": "given_piece",
            "addition": "정삼각형 2개",
            "result": "큰 정삼각형",
        }
    ],
}


def build_problem_template() -> ProblemTemplate:
    stem_text_slot = TextBoxSlot(
        id="slot.stem.question",
        prompt="",
        text="78. 정삼각형, 사다리꼴, 평행사변형 모양 조각 중에서 2가지를 골라 정삼각형을 만들려고 합니다. 다음 물음에 답하세요.\n(2) 평행사변형 모양 조각 1개를 사용할 때, 필요한 모양 조각과 개수를 선택하세요.",
        x=32,
        y=24,
        width=820,
        height=76,
        font_size=21,
        font_family='"Noto Sans KR", sans-serif',
        fill="#202124",
        align="left",
        valign="top",
        line_height=1.5,
    )

    diagram_slots = [
        RectSlot(id="slot.diagram.pink_box", prompt="", x=78, y=114, width=730, height=94, fill="#ffffff", stroke="#ec4899", stroke_width=1.6),
        TextSlot(id="slot.diagram.box_txt_l", prompt="", text="모양 조각은 (", x=174, y=148, font_size=20, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center"),
        PolygonSlot(id="slot.diagram.trap", prompt="", points=[(276, 134), (324, 134), (348, 178), (252, 178)], fill="#fb7185", stroke="#be123c", stroke_width=1.4),
        TextSlot(id="slot.diagram.comma", prompt="", text=",", x=362, y=148, font_size=20, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center"),
        PolygonSlot(id="slot.diagram.tri", prompt="", points=[(398, 134), (374, 178), (422, 178)], fill="#4ade80", stroke="#15803d", stroke_width=1.4),
        TextSlot(id="slot.diagram.box_txt_r", prompt="", text=")이며 모두 ( 1 , 2 , 3 )개가 필요합니다.", x=604, y=148, font_size=20, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center"),
    ]

    opts = [
        "① 사다리꼴, 2개",
        "② 정삼각형, 2개",
        "③ 정삼각형, 3개",
        "④ 사다리꼴, 1개",
    ]
    choice_slots = []
    for idx, label in enumerate(opts):
        col = idx % 2
        row = idx // 2
        cx = 138 + col * 320
        cy = 232 + row * 54
        choice_slots.append(
            RectSlot(
                id=f"slot.choice.option_{idx}",
                prompt="",
                x=cx,
                y=cy,
                width=290,
                height=42,
                fill="#f8fafc",
                stroke="#94a3b8",
                stroke_width=1.5,
                rx=8,
                ry=8,
                interaction={
                    "type": "choice",
                    "role": "answer",
                    "choice_index": idx,
                    "value": label.split(" ")[0],
                    "group_id": "slot.choice.group",
                    "include_in_submission": True,
                },
            )
        )
        diagram_slots.append(TextSlot(id=f"slot.diagram.opt_text_{idx}", prompt="", text=label, x=cx + 22, y=cy + 11, font_size=18, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="left"))

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
    "given": [{"ref": "given_piece", "value": "평행사변형 1개"}],
    "target": {"ref": "slot.choice.option_1", "label": "필요한 모양 조각과 개수", "unit": ""},
    "method": "shape_composition",
    "steps": [
        {
            "id": "compose_triangle",
            "expr": "평행사변형 1개 + 정삼각형 2개 = 큰 정삼각형",
            "explanation": "필요한 모양 조각은 정삼각형이며 모두 2개가 필요합니다.",
            "value": "②",
        },
    ],
    "answer": ANSWER,
}


if __name__ == "__main__":
    print(f"[{PROBLEM_TEMPLATE.id}] 템플릿 컴파일 성공!")
