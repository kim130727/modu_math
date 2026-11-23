"""ModuMath Problem DSL: 모양 조각으로 물고기 모양 만들기 (S3_초등_4_007866)"""

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


PROBLEM_ID = "S3_초등_4_007866"
PROBLEM_TITLE = "모양 조각을 여러 번 사용하여 물고기 모양을 만들 수 있는지 선택하기"

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
                    "concept": "모양 만들기",
                    "reason": "정육각형, 사다리꼴, 평행사변형, 정삼각형, 정사각형, 마름모를 조합해 만들 수 있음을 놓침",
                    "feedback": "가(정육각형), 나(사다리꼴), 다(평행사변형), 라(정삼각형), 마(정사각형), 바(마름모)를 조합하면 물고기 모양을 만들 수 있으므로 ○입니다.",
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
        "target_shape": {"label": "물고기 모양", "can_make": True},
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
        text="81. 모양 조각을 여러 번 사용하여 다음 모양을 만들 수 있으면 ○, 그렇지 않으면 ×를 선택하세요.",
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
        RectSlot(id="slot.diagram.box", prompt="", x=98, y=98, width=690, height=82, fill="#ffffff", stroke="#fb923c", stroke_width=1.6),
        PolygonSlot(id="slot.diagram.ga", prompt="", points=[(142, 112), (182, 112), (202, 139), (182, 166), (142, 166), (122, 139)], fill="#fde047", stroke="#ca8a04", stroke_width=1.4),
        TextSlot(id="slot.diagram.l_ga", prompt="", text="가", x=162, y=130, font_size=15, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center"),

        PolygonSlot(id="slot.diagram.na", prompt="", points=[(252, 118), (294, 118), (314, 158), (232, 158)], fill="#f97316", stroke="#c2410c", stroke_width=1.4),
        TextSlot(id="slot.diagram.l_na", prompt="", text="나", x=273, y=130, font_size=15, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center"),

        PolygonSlot(id="slot.diagram.da", prompt="", points=[(366, 118), (408, 118), (388, 158), (346, 158)], fill="#38bdf8", stroke="#0284c7", stroke_width=1.4),
        TextSlot(id="slot.diagram.l_da", prompt="", text="다", x=377, y=130, font_size=15, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center"),

        PolygonSlot(id="slot.diagram.ra", prompt="", points=[(468, 118), (446, 158), (490, 158)], fill="#4ade80", stroke="#15803d", stroke_width=1.4),
        TextSlot(id="slot.diagram.l_ra", prompt="", text="라", x=468, y=134, font_size=15, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center"),

        RectSlot(id="slot.diagram.ma", prompt="", x=540, y=118, width=38, height=38, fill="#fbbf24", stroke="#d97706", stroke_width=1.4),
        TextSlot(id="slot.diagram.l_ma", prompt="", text="마", x=559, y=128, font_size=15, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center"),

        PolygonSlot(id="slot.diagram.ba", prompt="", points=[(630, 138), (674, 126), (718, 138), (674, 150)], fill="#cbd5e1", stroke="#64748b", stroke_width=1.4),
        TextSlot(id="slot.diagram.l_ba", prompt="", text="바", x=674, y=130, font_size=15, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center"),

        # 물고기 모양 외곽선
        PolygonSlot(
            id="slot.diagram.fish",
            prompt="",
            points=[
                (356, 264), (434, 218), (452, 192), (492, 192), (474, 224),
                (514, 248), (546, 224), (546, 304), (514, 280), (474, 304),
                (492, 336), (452, 336), (434, 310),
            ],
            fill="none",
            stroke="#111827",
            stroke_width=1.8,
        ),
    ]

    choice_0 = RectSlot(id="slot.choice.option_0", prompt="", x=286, y=356, width=124, height=52, fill="#f8fafc", stroke="#94a3b8", stroke_width=1.6, rx=10, ry=10, interaction={"type": "choice", "role": "answer", "choice_index": 0, "value": "○", "group_id": "slot.choice.group", "include_in_submission": True})
    diagram_slots.append(TextSlot(id="slot.diagram.c0_t", prompt="", text="○", x=348, y=368, font_size=26, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center"))

    choice_1 = RectSlot(id="slot.choice.option_1", prompt="", x=476, y=356, width=124, height=52, fill="#f8fafc", stroke="#94a3b8", stroke_width=1.6, rx=10, ry=10, interaction={"type": "choice", "role": "answer", "choice_index": 1, "value": "×", "group_id": "slot.choice.group", "include_in_submission": True})
    diagram_slots.append(TextSlot(id="slot.diagram.c1_t", prompt="", text="×", x=538, y=368, font_size=26, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center"))

    return ProblemTemplate(
        id=PROBLEM_ID,
        title=PROBLEM_TITLE,
        canvas=Canvas(width=886, height=432, coordinate_mode="logical"),
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
    "given": [{"ref": "target_shape", "value": "주어진 물고기 모양"}],
    "target": {"ref": "slot.choice.option_0", "label": "만들기 가능 여부", "unit": ""},
    "method": "tiling_feasibility",
    "steps": [
        {
            "id": "check_tiling",
            "expr": "가, 나, 다, 라, 마, 바 조각을 조합해 물고기 모양 완성 가능",
            "explanation": "모양 조각을 여러 번 사용하여 물고기 모양을 만들 수 있으므로 ○입니다.",
            "value": "○",
        },
    ],
    "answer": ANSWER,
}


if __name__ == "__main__":
    print(f"[{PROBLEM_TEMPLATE.id}] 템플릿 컴파일 성공!")
