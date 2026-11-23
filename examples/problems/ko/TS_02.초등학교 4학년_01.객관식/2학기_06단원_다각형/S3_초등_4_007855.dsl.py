"""ModuMath Problem DSL: 모양을 만드는 데 사용한 다각형 찾기 (S3_초등_4_007855)"""

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


PROBLEM_ID = "S3_초등_4_007855"
PROBLEM_TITLE = "모양을 만드는 데 사용한 다각형의 이름 선택하기"

ANSWER = {
    "value": "사각형",
    "answer_index": 1,
    "unit": "",
    "values": ["사각형"],
    "choices": [
        "삼각형",
        "사각형",
        "육각형",
    ],
    "blanks": [],
    "answer_key": [
        {
            "slot_id": "slot.choice.option_1",
            "value": "사각형",
            "diagnostics": [
                {
                    "id": "diag.wrong_polygon_name",
                    "condition": "answer_not_quad",
                    "concept": "다각형의 이름",
                    "reason": "모양을 이루는 각 조각의 변의 수를 잘못 셈",
                    "feedback": "모양을 자세히 보면 변이 4개인 사각형 3개를 이어 붙여 만든 모양입니다.",
                },
            ],
        },
    ],
}

SEMANTIC = {
    "problem_id": PROBLEM_ID,
    "problem_type": "multiple_choice_pattern_block_polygon",
    "metadata": {
        "school": "초등학교",
        "grade": 4,
        "semester": "2학기",
        "chapter": "06단원_다각형",
        "difficulty": "하",
    },
    "entities": {
        "shape": {"label": "만든 모양", "piece_type": "사각형", "piece_count": 3},
    },
    "relations": [
        {
            "type": "composition",
            "whole": "shape",
            "part": "사각형",
            "count": 3,
        }
    ],
}


def build_problem_template() -> ProblemTemplate:
    stem_text_slot = TextBoxSlot(
        id="slot.stem.question",
        prompt="",
        text="69. 모양을 만드는 데 사용한 다각형의 이름을 찾아 선택하세요.",
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
        # 사각형(마름모) 3개로 만든 배/왕관 모양
        PolygonSlot(id="slot.diagram.p_left", prompt="", points=[(366, 126), (416, 126), (443, 174), (393, 174)], fill="#38bdf8", stroke="#0284c7", stroke_width=1.8),
        PolygonSlot(id="slot.diagram.p_mid", prompt="", points=[(443, 78), (470, 126), (443, 174), (416, 126)], fill="#38bdf8", stroke="#0284c7", stroke_width=1.8),
        PolygonSlot(id="slot.diagram.p_right", prompt="", points=[(470, 126), (520, 126), (493, 174), (443, 174)], fill="#38bdf8", stroke="#0284c7", stroke_width=1.8),
        RectSlot(id="slot.diagram.frame", prompt="", x=142, y=206, width=602, height=74, fill="#ffffff", stroke="#a78bfa", stroke_width=1.6),
    ]

    opts = ["삼각형", "사각형", "육각형"]
    choice_slots = []
    for idx, label in enumerate(opts):
        cx = 168 + idx * 196
        choice_slots.append(
            RectSlot(
                id=f"slot.choice.option_{idx}",
                prompt="",
                x=cx,
                y=219,
                width=158,
                height=48,
                fill="#f8fafc",
                stroke="#cbd5e1",
                stroke_width=1.4,
                rx=8,
                ry=8,
                interaction={
                    "type": "choice",
                    "role": "answer",
                    "choice_index": idx,
                    "value": label,
                    "group_id": "slot.choice.group",
                    "include_in_submission": True,
                },
            )
        )
        diagram_slots.append(TextSlot(id=f"slot.diagram.opt_{idx}", prompt="", text=label, x=cx + 79, y=231, font_size=21, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center"))

    return ProblemTemplate(
        id=PROBLEM_ID,
        title=PROBLEM_TITLE,
        canvas=Canvas(width=886, height=308, coordinate_mode="logical"),
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
    "given": [{"ref": "shape", "value": "사각형 3개로 만든 모양"}],
    "target": {"ref": "slot.choice.option_1", "label": "사용한 다각형의 이름", "unit": ""},
    "method": "shape_decomposition",
    "steps": [
        {
            "id": "identify_piece",
            "expr": "변이 4개인 다각형(사각형) 3개 사용",
            "explanation": "사각형 3개로 만든 모양이므로 정답은 사각형입니다.",
            "value": "사각형",
        },
    ],
    "answer": ANSWER,
}


if __name__ == "__main__":
    print(f"[{PROBLEM_TEMPLATE.id}] 템플릿 컴파일 성공!")
