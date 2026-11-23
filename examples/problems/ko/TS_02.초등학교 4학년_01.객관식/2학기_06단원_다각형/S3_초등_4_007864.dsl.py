"""ModuMath Problem DSL: 모양 조각으로 오리 모양 채우기 (S3_초등_4_007864)"""

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


PROBLEM_ID = "S3_초등_4_007864"
PROBLEM_TITLE = "주어진 모양 조각을 모두 사용하여 오리 모양을 채울 수 있는지 선택하기"

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
                    "id": "diag.missed_tiling_possibility",
                    "condition": "answer_equals_x",
                    "concept": "모양 채우기",
                    "reason": "여러 가지 모양 조각을 이용해 주어진 오리 모양을 채울 수 있음을 놓침",
                    "feedback": "주어진 모양 조각을 여러 번 사용하면 오리 모양을 빈틈없이 채울 수 있으므로 ○입니다.",
                },
            ],
        },
    ],
}

SEMANTIC = {
    "problem_id": PROBLEM_ID,
    "problem_type": "multiple_choice_tiling_ox",
    "metadata": {
        "school": "초등학교",
        "grade": 4,
        "semester": "2학기",
        "chapter": "06단원_다각형",
        "difficulty": "중",
    },
    "entities": {
        "target_shape": {"label": "오리 모양", "can_tile": True},
    },
    "relations": [
        {
            "type": "tiling_feasibility",
            "target": "target_shape",
            "result": True,
        }
    ],
}


def build_problem_template() -> ProblemTemplate:
    stem_text_slot = TextBoxSlot(
        id="slot.stem.question",
        prompt="",
        text="79. 주어진 모양 조각을 모두 사용하여 다음 모양을 채울 수 있으면 ○, 채울 수 없으면 ×를 선택하세요.(단, 모양 조각은 여러 번 사용할 수 있습니다.)",
        x=32,
        y=24,
        width=820,
        height=64,
        font_size=21,
        font_family='"Noto Sans KR", sans-serif',
        fill="#202124",
        align="left",
        valign="top",
        line_height=1.5,
    )

    diagram_slots = [
        RectSlot(id="slot.diagram.box", prompt="", x=98, y=98, width=690, height=78, fill="#ffffff", stroke="#8b5cf6", stroke_width=1.6),
        PolygonSlot(id="slot.diagram.p1", prompt="", points=[(156, 118), (134, 156), (178, 156)], fill="#4ade80", stroke="#15803d", stroke_width=1.4),
        PolygonSlot(id="slot.diagram.p2", prompt="", points=[(246, 118), (290, 118), (312, 156), (224, 156)], fill="#fb7185", stroke="#be123c", stroke_width=1.4),
        PolygonSlot(id="slot.diagram.p3", prompt="", points=[(372, 118), (416, 118), (394, 156), (350, 156)], fill="#38bdf8", stroke="#0284c7", stroke_width=1.4),
        PolygonSlot(id="slot.diagram.p4", prompt="", points=[(476, 106), (488, 137), (476, 168), (464, 137)], fill="#cbd5e1", stroke="#64748b", stroke_width=1.4),
        RectSlot(id="slot.diagram.p5", prompt="", x=538, y=118, width=38, height=38, fill="#fbbf24", stroke="#d97706", stroke_width=1.4),
        PolygonSlot(id="slot.diagram.p6", prompt="", points=[(650, 110), (694, 110), (716, 137), (694, 164), (650, 164), (628, 137)], fill="#fde047", stroke="#ca8a04", stroke_width=1.4),

        # 오리 모양 외곽선
        PolygonSlot(
            id="slot.diagram.duck",
            prompt="",
            points=[
                (412, 192), (450, 192), (468, 224), (450, 254), (492, 254),
                (530, 232), (550, 266), (512, 288), (494, 314), (528, 334),
                (482, 334), (450, 314), (418, 334), (372, 334), (404, 314),
                (386, 284), (404, 254), (366, 254),
            ],
            fill="none",
            stroke="#111827",
            stroke_width=1.8,
        ),
    ]

    choice_0 = RectSlot(id="slot.choice.option_0", prompt="", x=286, y=354, width=124, height=52, fill="#f8fafc", stroke="#94a3b8", stroke_width=1.6, rx=10, ry=10, interaction={"type": "choice", "role": "answer", "choice_index": 0, "value": "○", "group_id": "slot.choice.group", "include_in_submission": True})
    diagram_slots.append(TextSlot(id="slot.diagram.c0_t", prompt="", text="○", x=348, y=366, font_size=26, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center"))

    choice_1 = RectSlot(id="slot.choice.option_1", prompt="", x=476, y=354, width=124, height=52, fill="#f8fafc", stroke="#94a3b8", stroke_width=1.6, rx=10, ry=10, interaction={"type": "choice", "role": "answer", "choice_index": 1, "value": "×", "group_id": "slot.choice.group", "include_in_submission": True})
    diagram_slots.append(TextSlot(id="slot.diagram.c1_t", prompt="", text="×", x=538, y=366, font_size=26, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center"))

    return ProblemTemplate(
        id=PROBLEM_ID,
        title=PROBLEM_TITLE,
        canvas=Canvas(width=886, height=430, coordinate_mode="logical"),
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
    "given": [{"ref": "target_shape", "value": "주어진 오리 모양"}],
    "target": {"ref": "slot.choice.option_0", "label": "채우기 가능 여부", "unit": ""},
    "method": "tiling_feasibility",
    "steps": [
        {
            "id": "check_tiling",
            "expr": "정삼각형, 사다리꼴, 정사각형, 평행사변형 조각으로 오리 모양 채우기 가능",
            "explanation": "주어진 모양 조각을 여러 번 사용하여 오리 모양을 채울 수 있으므로 ○입니다.",
            "value": "○",
        },
    ],
    "answer": ANSWER,
}


if __name__ == "__main__":
    print(f"[{PROBLEM_TEMPLATE.id}] 템플릿 컴파일 성공!")
