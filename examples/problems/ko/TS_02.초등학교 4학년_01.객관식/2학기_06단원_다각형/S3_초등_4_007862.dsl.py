"""ModuMath Problem DSL: 정삼각형 만들기 1 (S3_초등_4_007862)"""

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


PROBLEM_ID = "S3_초등_4_007862"
PROBLEM_TITLE = "정삼각형을 만들 때 정삼각형 1개와 함께 필요한 모양 조각 선택하기"

ANSWER = {
    "value": "①",
    "answer_index": 0,
    "unit": "",
    "values": ["①"],
    "choices": [
        "① 사다리꼴",
        "② 평행사변형",
    ],
    "blanks": [],
    "answer_key": [
        {
            "slot_id": "slot.choice.option_0",
            "value": "①",
            "diagnostics": [
                {
                    "id": "diag.chose_parallelogram",
                    "condition": "answer_equals_2",
                    "concept": "모양 조각으로 정삼각형 만들기",
                    "reason": "정삼각형 1개와 평행사변형 1개로는 정삼각형을 만들 수 없음을 놓침",
                    "feedback": "정삼각형 모양 조각 1개의 아래에 사다리꼴 모양 조각 1개를 붙이면 큰 정삼각형이 됩니다. 따라서 ①을 선택하세요.",
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
        "given_piece": {"label": "정삼각형 1개"},
        "opt_0": {"label": "① 사다리꼴", "forms_equilateral": True},
        "opt_1": {"label": "② 평행사변형", "forms_equilateral": False},
    },
    "relations": [
        {
            "type": "composition",
            "base": "given_piece",
            "addition": "opt_0",
            "result": "큰 정삼각형",
        }
    ],
}


def build_problem_template() -> ProblemTemplate:
    stem_text_slot = TextBoxSlot(
        id="slot.stem.question",
        prompt="",
        text="78. 정삼각형, 사다리꼴, 평행사변형 모양 조각 중에서 2가지를 골라 정삼각형을 만들려고 합니다. 다음 물음에 답하세요.\n(1) 정삼각형 모양 조각 1개를 사용할 때, 필요한 모양 조각을 선택하세요.",
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

    choice_0 = RectSlot(id="slot.choice.option_0", prompt="", x=230, y=126, width=184, height=112, fill="#f8fafc", stroke="#cbd5e1", stroke_width=1.5, rx=10, ry=10, interaction={"type": "choice", "role": "answer", "choice_index": 0, "value": "①", "group_id": "slot.choice.group", "include_in_submission": True})
    choice_1 = RectSlot(id="slot.choice.option_1", prompt="", x=472, y=126, width=184, height=112, fill="#f8fafc", stroke="#cbd5e1", stroke_width=1.5, rx=10, ry=10, interaction={"type": "choice", "role": "answer", "choice_index": 1, "value": "②", "group_id": "slot.choice.group", "include_in_submission": True})

    diagram_slots = [
        TextSlot(id="slot.diagram.b0", prompt="", text="①", x=250, y=138, font_size=18, font_family='"Noto Sans KR", sans-serif', fill="#4b5563", align="center"),
        PolygonSlot(id="slot.diagram.trap", prompt="", points=[(292, 152), (352, 152), (382, 206), (262, 206)], fill="#fb7185", stroke="#be123c", stroke_width=1.6),

        TextSlot(id="slot.diagram.b1", prompt="", text="②", x=492, y=138, font_size=18, font_family='"Noto Sans KR", sans-serif', fill="#4b5563", align="center"),
        PolygonSlot(id="slot.diagram.para", prompt="", points=[(544, 152), (604, 152), (574, 206), (514, 206)], fill="#38bdf8", stroke="#0284c7", stroke_width=1.6),
    ]

    return ProblemTemplate(
        id=PROBLEM_ID,
        title=PROBLEM_TITLE,
        canvas=Canvas(width=886, height=268, coordinate_mode="logical"),
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
    "given": [{"ref": "given_piece", "value": "정삼각형 1개"}],
    "target": {"ref": "slot.choice.option_0", "label": "필요한 모양 조각", "unit": ""},
    "method": "shape_composition",
    "steps": [
        {
            "id": "compose_triangle",
            "expr": "정삼각형 1개 + 사다리꼴 1개 = 큰 정삼각형",
            "explanation": "사다리꼴 모양 조각 1개를 아래에 붙이면 정삼각형이 됩니다.",
            "value": "①",
        },
    ],
    "answer": ANSWER,
}


if __name__ == "__main__":
    print(f"[{PROBLEM_TEMPLATE.id}] 템플릿 컴파일 성공!")
