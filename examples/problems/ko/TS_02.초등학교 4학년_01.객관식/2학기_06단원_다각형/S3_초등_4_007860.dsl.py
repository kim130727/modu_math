"""ModuMath Problem DSL: 가장 많이 사용해야 하는 모양 조각 찾기 (S3_초등_4_007860)"""

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


PROBLEM_ID = "S3_초등_4_007860"
PROBLEM_TITLE = "난초 모양을 채울 때 가장 많이 사용해야 하는 모양 조각 선택하기"

ANSWER = {
    "value": "②",
    "answer_index": 1,
    "unit": "",
    "values": ["②"],
    "choices": [
        "① 정삼각형",
        "② 마름모",
        "③ 정육각형",
    ],
    "blanks": [],
    "answer_key": [
        {
            "slot_id": "slot.choice.option_1",
            "value": "②",
            "diagnostics": [
                {
                    "id": "diag.wrong_piece_count",
                    "condition": "answer_not_2",
                    "concept": "모양 조각으로 모양 채우기",
                    "reason": "난초의 잎 부분을 채우는 마름모(4개)가 가장 많음을 놓침",
                    "feedback": "정삼각형 2개, 마름모 4개, 정육각형 1개로 채울 수 있으므로 가장 많이 사용한 조각은 마름모(②)입니다.",
                },
            ],
        },
    ],
}

SEMANTIC = {
    "problem_id": PROBLEM_ID,
    "problem_type": "multiple_choice_most_used_pattern_block",
    "metadata": {
        "school": "초등학교",
        "grade": 4,
        "semester": "2학기",
        "chapter": "06단원_다각형",
        "difficulty": "중",
    },
    "entities": {
        "piece_0": {"label": "① 정삼각형", "count": 2},
        "piece_1": {"label": "② 마름모", "count": 4},
        "piece_2": {"label": "③ 정육각형", "count": 1},
    },
    "relations": [
        {
            "type": "argmax",
            "property": "count",
            "correct_entity": "piece_1",
        }
    ],
}


def build_problem_template() -> ProblemTemplate:
    stem_text_slot = TextBoxSlot(
        id="slot.stem.question",
        prompt="",
        text="75. 3가지 모양 조각을 모두 사용하여 오른쪽 난초 모양을 채우려고 합니다. 가장 많이 사용해야 하는 모양 조각을 찾아 선택하세요.",
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

    choice_0 = RectSlot(id="slot.choice.option_0", prompt="", x=106, y=108, width=104, height=130, fill="#f8fafc", stroke="#cbd5e1", stroke_width=1.5, rx=10, ry=10, interaction={"type": "choice", "role": "answer", "choice_index": 0, "value": "①", "group_id": "slot.choice.group", "include_in_submission": True})
    choice_1 = RectSlot(id="slot.choice.option_1", prompt="", x=230, y=108, width=104, height=130, fill="#f8fafc", stroke="#cbd5e1", stroke_width=1.5, rx=10, ry=10, interaction={"type": "choice", "role": "answer", "choice_index": 1, "value": "②", "group_id": "slot.choice.group", "include_in_submission": True})
    choice_2 = RectSlot(id="slot.choice.option_2", prompt="", x=354, y=108, width=124, height=130, fill="#f8fafc", stroke="#cbd5e1", stroke_width=1.5, rx=10, ry=10, interaction={"type": "choice", "role": "answer", "choice_index": 2, "value": "③", "group_id": "slot.choice.group", "include_in_submission": True})

    diagram_slots = [
        TextSlot(id="slot.diagram.b0", prompt="", text="①", x=122, y=118, font_size=16, font_family='"Noto Sans KR", sans-serif', fill="#4b5563", align="center"),
        PolygonSlot(id="slot.diagram.tri", prompt="", points=[(158, 148), (132, 196), (184, 196)], fill="#4ade80", stroke="#15803d", stroke_width=1.6),

        TextSlot(id="slot.diagram.b1", prompt="", text="②", x=246, y=118, font_size=16, font_family='"Noto Sans KR", sans-serif', fill="#4b5563", align="center"),
        PolygonSlot(id="slot.diagram.rhom", prompt="", points=[(282, 128), (298, 174), (282, 220), (266, 174)], fill="#cbd5e1", stroke="#64748b", stroke_width=1.6),

        TextSlot(id="slot.diagram.b2", prompt="", text="③", x=370, y=118, font_size=16, font_family='"Noto Sans KR", sans-serif', fill="#4b5563", align="center"),
        PolygonSlot(id="slot.diagram.hex", prompt="", points=[(396, 138), (436, 138), (456, 174), (436, 210), (396, 210), (376, 174)], fill="#fde047", stroke="#ca8a04", stroke_width=1.6),

        TextSlot(id="slot.diagram.arrow", prompt="", text="→", x=514, y=160, font_size=26, font_family='"Noto Sans KR", sans-serif', fill="#6b7280", align="center"),

        # 오른쪽 난초 모양 외곽선
        PolygonSlot(
            id="slot.diagram.orchid",
            prompt="",
            points=[
                (630, 248), (694, 248), (736, 176), (710, 176), (762, 148),
                (700, 148), (740, 100), (662, 176), (584, 100), (624, 148),
                (562, 148), (614, 176), (588, 176),
            ],
            fill="none",
            stroke="#111827",
            stroke_width=1.8,
        ),
    ]

    return ProblemTemplate(
        id=PROBLEM_ID,
        title=PROBLEM_TITLE,
        canvas=Canvas(width=886, height=278, coordinate_mode="logical"),
        regions=(
            Region(id="region.stem", role="stem", flow="absolute", slot_ids=("slot.stem.question",)),
            Region(id="region.choices", role="choices", flow="absolute", slot_ids=("slot.choice.option_0", "slot.choice.option_1", "slot.choice.option_2")),
            Region(id="region.diagram", role="diagram", flow="absolute", slot_ids=tuple(s.id for s in diagram_slots)),
        ),
        slots=(stem_text_slot, choice_0, choice_1, choice_2, *diagram_slots),
    )


PROBLEM_TEMPLATE = build_problem_template()
SEMANTIC_OVERRIDE = SEMANTIC
SEMANTIC_ANSWER = ANSWER
SOLVABLE = {
    "schema": "modu.solvable.v1.3",
    "problem_id": PROBLEM_ID,
    "problem_type": SEMANTIC["problem_type"],
    "given": [
        {"ref": "piece_0", "value": "정삼각형 2개"},
        {"ref": "piece_1", "value": "마름모 4개"},
        {"ref": "piece_2", "value": "정육각형 1개"},
    ],
    "target": {"ref": "slot.choice.option_1", "label": "가장 많이 사용한 모양 조각", "unit": ""},
    "method": "shape_decomposition",
    "steps": [
        {
            "id": "count_pieces",
            "expr": "정삼각형 2개, 마름모 4개, 정육각형 1개",
            "explanation": "가장 많이 사용해야 하는 모양 조각은 4개인 마름모(②)입니다.",
            "value": "②",
        },
    ],
    "answer": ANSWER,
}


if __name__ == "__main__":
    print(f"[{PROBLEM_TEMPLATE.id}] 템플릿 컴파일 성공!")
