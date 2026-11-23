"""ModuMath Problem DSL: 삼각자를 사용하여 수선을 바르게 그은 것 찾기 (S3_초등_4_007532)"""

from __future__ import annotations

from modu_math.dsl import (
    Canvas,
    LineSlot,
    PolygonSlot,
    ProblemTemplate,
    RectSlot,
    Region,
    TextBoxSlot,
    TextSlot,
)


# ==============================================================================
# 1. 문제 식별자 및 제목 (Problem Metadata)
# ==============================================================================
PROBLEM_ID = "S3_초등_4_007532"
PROBLEM_TITLE = "삼각자를 사용하여 직선 가에 수직인 직선을 바르게 그은 것 선택하기"


# ==============================================================================
# 2. 정답 및 오답 진단 정의 (Answer & Diagnostic Key)
# ==============================================================================
ANSWER = {
    "value": "③",
    "answer_index": 2,
    "unit": "",
    "values": ["③"],
    "choices": [
        "①",
        "②",
        "③",
    ],
    "blanks": [],
    "answer_key": [
        {
            "slot_id": "slot.choice.option_2",
            "value": "③",
            "diagnostics": [
                {
                    "id": "diag.aligned_hypotenuse",
                    "condition": "answer_equals_1",
                    "concept": "수선 긋기",
                    "reason": "직각을 낀 변이 아니라 빗변을 직선 가에 맞춘 그림(①)을 선택함",
                    "feedback": "삼각자에서 직각을 낀 변 중 한 변을 직선 가에 맞추어야 합니다. ③이 바릅니다.",
                },
                {
                    "id": "diag.not_aligned_to_line",
                    "condition": "answer_equals_2",
                    "concept": "수선 긋기",
                    "reason": "직각을 낀 변을 직선 가에 맞추지 않은 그림(②)을 선택함",
                    "feedback": "②는 삼각자의 변을 직선 가에 맞추지 않았습니다. 직각을 낀 두 변으로 직각을 만든 ③이 바릅니다.",
                },
            ],
        },
    ],
}


# ==============================================================================
# 3. 시맨틱 모델 정의 (Semantic Model & Metadata)
# ==============================================================================
SEMANTIC = {
    "problem_id": PROBLEM_ID,
    "problem_type": "multiple_choice_perpendicular_construction",
    "metadata": {
        "school": "초등학교",
        "grade": 4,
        "semester": "1학기",
        "chapter": "04단원_평면도형의 이동",
        "difficulty": "중",
    },
    "entities": {
        "option_0": {"label": "①", "is_perpendicular": False},
        "option_1": {"label": "②", "is_perpendicular": False},
        "option_2": {"label": "③", "is_perpendicular": True},
    },
    "relations": [
        {
            "type": "correct_construction",
            "correct_entity": "option_2",
            "distractors": ["option_0", "option_1"],
        }
    ],
}


# ==============================================================================
# 4. 문제 템플릿 빌더 (ProblemTemplate Builder)
# ==============================================================================
def build_problem_template() -> ProblemTemplate:
    """문제의 캔버스 크기, 슬롯(텍스트/도형/선택지), 리전(구역)을 정의합니다."""

    stem_text_slot = TextBoxSlot(
        id="slot.stem.question",
        prompt="",
        text="68. 삼각자를 사용하여 직선 가에 수직인 직선을 바르게 그은 것을 선택하세요.",
        x=32,
        y=24,
        width=820,
        height=56,
        font_size=22,
        font_family='"Noto Sans KR", sans-serif',
        fill="#202124",
        align="left",
        valign="top",
        line_height=1.5,
    )

    # ① 빗변을 직선 가에 맞춤
    card_0 = RectSlot(id="slot.choice.option_0", prompt="", x=56, y=92, width=238, height=176, fill="#ffffff", stroke="#e5e7eb", stroke_width=1.5, rx=10, ry=10, interaction={"type": "choice", "role": "answer", "choice_index": 0, "value": "①", "group_id": "slot.choice.group", "include_in_submission": True})
    b0 = TextSlot(id="slot.diagram.b0", prompt="", text="①", x=80, y=106, font_size=20, font_family='"Noto Sans KR", sans-serif', fill="#4b5563", align="center")
    c0_ga = LineSlot(id="slot.diagram.c0_ga", prompt="", x1=126, y1=246, x2=246, y2=126, stroke="#111827", stroke_width=2)
    c0_ga_l = TextSlot(id="slot.diagram.c0_ga_l", prompt="", text="가", x=106, y=236, font_size=18, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center")
    c0_tri = PolygonSlot(id="slot.diagram.c0_tri", prompt="", points=[(146, 226), (146, 114), (218, 154)], fill="#e0f2fe", stroke="#0284c7", stroke_width=1.5)
    c0_drawn = LineSlot(id="slot.diagram.c0_drawn", prompt="", x1=146, y1=226, x2=146, y2=102, stroke="#111827", stroke_width=2)

    # ② 꼭짓점만 맞춤
    card_1 = RectSlot(id="slot.choice.option_1", prompt="", x=324, y=92, width=238, height=176, fill="#ffffff", stroke="#e5e7eb", stroke_width=1.5, rx=10, ry=10, interaction={"type": "choice", "role": "answer", "choice_index": 1, "value": "②", "group_id": "slot.choice.group", "include_in_submission": True})
    b1 = TextSlot(id="slot.diagram.b1", prompt="", text="②", x=348, y=106, font_size=20, font_family='"Noto Sans KR", sans-serif', fill="#4b5563", align="center")
    c1_ga = LineSlot(id="slot.diagram.c1_ga", prompt="", x1=376, y1=236, x2=524, y2=236, stroke="#111827", stroke_width=2)
    c1_ga_l = TextSlot(id="slot.diagram.c1_ga_l", prompt="", text="가", x=356, y=224, font_size=18, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center")
    c1_tri = PolygonSlot(id="slot.diagram.c1_tri", prompt="", points=[(424, 236), (504, 124), (534, 186)], fill="#e0f2fe", stroke="#0284c7", stroke_width=1.5)
    c1_drawn = LineSlot(id="slot.diagram.c1_drawn", prompt="", x1=424, y1=236, x2=516, y2=108, stroke="#111827", stroke_width=2)

    # ③ 직각을 낀 두 변을 이용 (정답)
    card_2 = RectSlot(id="slot.choice.option_2", prompt="", x=592, y=92, width=238, height=176, fill="#ffffff", stroke="#e5e7eb", stroke_width=1.5, rx=10, ry=10, interaction={"type": "choice", "role": "answer", "choice_index": 2, "value": "③", "group_id": "slot.choice.group", "include_in_submission": True})
    b2 = TextSlot(id="slot.diagram.b2", prompt="", text="③", x=616, y=106, font_size=20, font_family='"Noto Sans KR", sans-serif', fill="#4b5563", align="center")
    c2_ga = LineSlot(id="slot.diagram.c2_ga", prompt="", x1=644, y1=136, x2=744, y2=236, stroke="#111827", stroke_width=2)
    c2_ga_l = TextSlot(id="slot.diagram.c2_ga_l", prompt="", text="가", x=626, y=122, font_size=18, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center")
    c2_tri = PolygonSlot(id="slot.diagram.c2_tri", prompt="", points=[(724, 216), (656, 148), (792, 148)], fill="#e0f2fe", stroke="#0284c7", stroke_width=1.5)
    c2_drawn = LineSlot(id="slot.diagram.c2_drawn", prompt="", x1=724, y1=216, x2=804, y2=136, stroke="#111827", stroke_width=2)

    return ProblemTemplate(
        id=PROBLEM_ID,
        title=PROBLEM_TITLE,
        canvas=Canvas(
            width=886,
            height=290,
            coordinate_mode="logical",
        ),
        regions=(
            Region(id="region.stem", role="stem", flow="absolute", slot_ids=("slot.stem.question",)),
            Region(id="region.choices", role="choices", flow="absolute", slot_ids=("slot.choice.option_0", "slot.choice.option_1", "slot.choice.option_2")),
            Region(
                id="region.diagram",
                role="diagram",
                flow="absolute",
                slot_ids=(
                    "slot.diagram.b0",
                    "slot.diagram.c0_ga",
                    "slot.diagram.c0_ga_l",
                    "slot.diagram.c0_tri",
                    "slot.diagram.c0_drawn",
                    "slot.diagram.b1",
                    "slot.diagram.c1_ga",
                    "slot.diagram.c1_ga_l",
                    "slot.diagram.c1_tri",
                    "slot.diagram.c1_drawn",
                    "slot.diagram.b2",
                    "slot.diagram.c2_ga",
                    "slot.diagram.c2_ga_l",
                    "slot.diagram.c2_tri",
                    "slot.diagram.c2_drawn",
                ),
            ),
        ),
        slots=(
            stem_text_slot,
            card_0,
            b0,
            c0_ga,
            c0_ga_l,
            c0_tri,
            c0_drawn,
            card_1,
            b1,
            c1_ga,
            c1_ga_l,
            c1_tri,
            c1_drawn,
            card_2,
            b2,
            c2_ga,
            c2_ga_l,
            c2_tri,
            c2_drawn,
        ),
    )


# ==============================================================================
# 5. ModuMath 프레임워크 필수 익스포트
# ==============================================================================
PROBLEM_TEMPLATE = build_problem_template()
SEMANTIC_OVERRIDE = SEMANTIC
SEMANTIC_ANSWER = ANSWER
SOLVABLE = {
    "schema": "modu.solvable.v1.3",
    "problem_id": PROBLEM_ID,
    "problem_type": SEMANTIC["problem_type"],
    "given": [
        {"ref": "option_0", "value": "빗변을 맞춤"},
        {"ref": "option_1", "value": "꼭짓점만 맞춤"},
        {"ref": "option_2", "value": "직각을 낀 변을 맞춤"},
    ],
    "target": {"ref": "slot.choice.option_2", "label": "바르게 그린 것", "unit": ""},
    "method": "set_square_perpendicular",
    "steps": [
        {
            "id": "verify_set_square",
            "expr": "③",
            "explanation": "삼각자의 직각을 낀 한 변을 직선 가에 맞추고 다른 한 변을 따라 그은 ③이 바릅니다.",
            "value": "③",
        },
    ],
    "answer": ANSWER,
}


if __name__ == "__main__":
    print(f"[{PROBLEM_TEMPLATE.id}] 템플릿 컴파일 성공!")
    print(f"- 제목: {PROBLEM_TEMPLATE.title}")
    print(f"- 캔버스: {PROBLEM_TEMPLATE.canvas.width} x {PROBLEM_TEMPLATE.canvas.height}")
    print(f"- 구역 수: {len(PROBLEM_TEMPLATE.regions)}")
