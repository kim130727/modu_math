"""ModuMath Problem DSL: 모양 채우기 규칙 알기 (S3_초등_4_007856)"""

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


PROBLEM_ID = "S3_초등_4_007856"
PROBLEM_TITLE = "정육각형 모양 채우기를 보고 알맞은 말 선택하기"

ANSWER = {
    "value": "겹치지 않게",
    "answer_index": 1,
    "unit": "",
    "values": ["겹치지 않게"],
    "choices": [
        "겹치게",
        "겹치지 않게",
    ],
    "blanks": [],
    "answer_key": [
        {
            "slot_id": "slot.choice.option_1",
            "value": "겹치지 않게",
            "diagnostics": [
                {
                    "id": "diag.overlap_error",
                    "condition": "answer_equals_0",
                    "concept": "모양 채우기의 규칙",
                    "reason": "모양 조각을 겹쳐서 채웠다고 잘못 이해함",
                    "feedback": "지현, 동민, 수아 모두 모양 조각을 서로 겹치지 않게 빈틈없이 이어 붙여 정육각형 모양을 채웠습니다.",
                },
            ],
        },
    ],
}

SEMANTIC = {
    "problem_id": PROBLEM_ID,
    "problem_type": "multiple_choice_tiling_rule",
    "metadata": {
        "school": "초등학교",
        "grade": 4,
        "semester": "2학기",
        "chapter": "06단원_다각형",
        "difficulty": "하",
    },
    "entities": {
        "jihyun": {"label": "지현", "pieces": "사다리꼴 2개"},
        "dongmin": {"label": "동민", "pieces": "평행사변형 3개"},
        "sua": {"label": "수아", "pieces": "정삼각형 6개"},
    },
    "relations": [
        {
            "type": "tiling_rule",
            "condition": "겹치지 않게 빈틈없이",
        }
    ],
}


def build_problem_template() -> ProblemTemplate:
    stem_text_slot = TextBoxSlot(
        id="slot.stem.question",
        prompt="",
        text="70. 3가지 모양 조각 중 1가지 모양을 사용하여 지현, 동민, 수아가 정육각형 모양을 채웠습니다. 지현, 동민, 수아의 모양 채우기를 보고 알맞은 말을 선택하세요.",
        x=32,
        y=24,
        width=820,
        height=72,
        font_size=21,
        font_family='"Noto Sans KR", sans-serif',
        fill="#202124",
        align="left",
        valign="top",
        line_height=1.5,
    )

    diagram_slots = [
        # 표
        RectSlot(id="slot.diagram.th0", prompt="", x=98, y=106, width=210, height=38, fill="#fdf2f8", stroke="#db2777", stroke_width=1.4),
        RectSlot(id="slot.diagram.th1", prompt="", x=308, y=106, width=160, height=38, fill="#fdf2f8", stroke="#db2777", stroke_width=1.4),
        RectSlot(id="slot.diagram.th2", prompt="", x=468, y=106, width=160, height=38, fill="#fdf2f8", stroke="#db2777", stroke_width=1.4),
        RectSlot(id="slot.diagram.th3", prompt="", x=628, y=106, width=160, height=38, fill="#fdf2f8", stroke="#db2777", stroke_width=1.4),
        TextSlot(id="slot.diagram.th0_t", prompt="", text="이름", x=203, y=115, font_size=18, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center"),
        TextSlot(id="slot.diagram.th1_t", prompt="", text="지현", x=388, y=115, font_size=18, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center"),
        TextSlot(id="slot.diagram.th2_t", prompt="", text="동민", x=548, y=115, font_size=18, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center"),
        TextSlot(id="slot.diagram.th3_t", prompt="", text="수아", x=708, y=115, font_size=18, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center"),

        RectSlot(id="slot.diagram.tb0", prompt="", x=98, y=144, width=210, height=94, fill="#fdf2f8", stroke="#db2777", stroke_width=1.4),
        RectSlot(id="slot.diagram.tb1", prompt="", x=308, y=144, width=160, height=94, fill="#ffffff", stroke="#db2777", stroke_width=1.4),
        RectSlot(id="slot.diagram.tb2", prompt="", x=468, y=144, width=160, height=94, fill="#ffffff", stroke="#db2777", stroke_width=1.4),
        RectSlot(id="slot.diagram.tb3", prompt="", x=628, y=144, width=160, height=94, fill="#ffffff", stroke="#db2777", stroke_width=1.4),
        TextBoxSlot(id="slot.diagram.tb0_t", prompt="", text="정육각형 모양을\n채운 방법", x=108, y=162, width=190, height=58, font_size=18, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center", valign="middle", line_height=1.4),

        # 지현: 사다리꼴 2개
        PolygonSlot(id="slot.diagram.hex1", prompt="", points=[(368, 155), (408, 155), (428, 191), (408, 227), (368, 227), (348, 191)], fill="#fb7185", stroke="#be123c", stroke_width=1.4),
        LineSlot(id="slot.diagram.hex1_l", prompt="", x1=348, y1=191, x2=428, y2=191, stroke="#be123c", stroke_width=1.2),

        # 동민: 평행사변형 3개
        PolygonSlot(id="slot.diagram.hex2", prompt="", points=[(528, 155), (568, 155), (588, 191), (568, 227), (528, 227), (508, 191)], fill="#38bdf8", stroke="#0369a1", stroke_width=1.4),
        LineSlot(id="slot.diagram.hex2_l1", prompt="", x1=548, y1=191, x2=508, y2=191, stroke="#0369a1", stroke_width=1.2),
        LineSlot(id="slot.diagram.hex2_l2", prompt="", x1=548, y1=191, x2=568, y2=155, stroke="#0369a1", stroke_width=1.2),
        LineSlot(id="slot.diagram.hex2_l3", prompt="", x1=548, y1=191, x2=568, y2=227, stroke="#0369a1", stroke_width=1.2),

        # 수아: 정삼각형 6개
        PolygonSlot(id="slot.diagram.hex3", prompt="", points=[(688, 155), (728, 155), (748, 191), (728, 227), (688, 227), (668, 191)], fill="#4ade80", stroke="#15803d", stroke_width=1.4),
        LineSlot(id="slot.diagram.hex3_l1", prompt="", x1=668, y1=191, x2=748, y2=191, stroke="#15803d", stroke_width=1.2),
        LineSlot(id="slot.diagram.hex3_l2", prompt="", x1=688, y1=155, x2=728, y2=227, stroke="#15803d", stroke_width=1.2),
        LineSlot(id="slot.diagram.hex3_l3", prompt="", x1=728, y1=155, x2=688, y2=227, stroke="#15803d", stroke_width=1.2),

        # 말풍선 & 캐릭터
        CircleSlot(id="slot.diagram.boy", prompt="", cx=256, cy=292, r=24, fill="#fde68a", stroke="#92400e", stroke_width=1.4),
        RectSlot(id="slot.diagram.bubble", prompt="", x=316, y=252, width=424, height=82, fill="#ffffff", stroke="#111827", stroke_width=1.5, rx=28, ry=28),
        TextBoxSlot(
            id="slot.diagram.bubble_txt",
            prompt="",
            text="모양 조각을 서로 ( 겹치게 , 겹치지 않게 )\n빈틈없이 이어 붙여서 모양을 채웠어.",
            x=332,
            y=266,
            width=392,
            height=54,
            font_size=18,
            font_family='"Noto Sans KR", sans-serif',
            fill="#111827",
            align="center",
            valign="middle",
            line_height=1.4,
        ),
    ]

    choice_0 = RectSlot(id="slot.choice.option_0", prompt="", x=238, y=354, width=176, height=46, fill="#f8fafc", stroke="#94a3b8", stroke_width=1.5, rx=8, ry=8, interaction={"type": "choice", "role": "answer", "choice_index": 0, "value": "겹치게", "group_id": "slot.choice.group", "include_in_submission": True})
    diagram_slots.append(TextSlot(id="slot.diagram.c0_t", prompt="", text="겹치게", x=326, y=366, font_size=19, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center"))

    choice_1 = RectSlot(id="slot.choice.option_1", prompt="", x=472, y=354, width=176, height=46, fill="#f8fafc", stroke="#94a3b8", stroke_width=1.5, rx=8, ry=8, interaction={"type": "choice", "role": "answer", "choice_index": 1, "value": "겹치지 않게", "group_id": "slot.choice.group", "include_in_submission": True})
    diagram_slots.append(TextSlot(id="slot.diagram.c1_t", prompt="", text="겹치지 않게", x=560, y=366, font_size=19, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center"))

    return ProblemTemplate(
        id=PROBLEM_ID,
        title=PROBLEM_TITLE,
        canvas=Canvas(width=886, height=424, coordinate_mode="logical"),
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
        {"ref": "jihyun", "value": "사다리꼴 2개"},
        {"ref": "dongmin", "value": "평행사변형 3개"},
        {"ref": "sua", "value": "정삼각형 6개"},
    ],
    "target": {"ref": "slot.choice.option_1", "label": "모양 채우기 방법", "unit": ""},
    "method": "tiling_rule",
    "steps": [
        {
            "id": "check_tiling",
            "expr": "모양 조각을 서로 겹치지 않게 빈틈없이 이어 붙임",
            "explanation": "모양 조각을 서로 겹치지 않게 빈틈없이 이어 붙여서 모양을 채웠습니다.",
            "value": "겹치지 않게",
        },
    ],
    "answer": ANSWER,
}


if __name__ == "__main__":
    print(f"[{PROBLEM_TEMPLATE.id}] 템플릿 컴파일 성공!")
