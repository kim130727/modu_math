"""ModuMath Problem DSL: 삼각자를 사용하여 수선 긋기 (S3_초등_4_007530)"""

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
PROBLEM_ID = "S3_초등_4_007530"
PROBLEM_TITLE = "삼각자를 사용하여 주어진 직선에 대한 수선 고르기"


# ==============================================================================
# 2. 정답 및 오답 진단 정의 (Answer & Diagnostic Key)
# ==============================================================================
ANSWER = {
    "value": "①",
    "answer_index": 0,
    "unit": "",
    "values": ["①"],
    "choices": [
        "①",
        "②",
    ],
    "blanks": [],
    "answer_key": [
        {
            "slot_id": "slot.choice.option_0",
            "value": "①",
            "diagnostics": [
                {
                    "id": "diag.drew_along_hypotenuse",
                    "condition": "answer_equals_2",
                    "concept": "수선 긋기",
                    "reason": "직각을 낀 변이 아니라 빗변을 따라 그은 그림(②)을 선택함",
                    "feedback": "삼각자에서 직각을 낀 다른 한 변을 따라 선을 그어야 주어진 직선과 수직이 됩니다. ①이 바릅니다.",
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
        "difficulty": "하",
    },
    "entities": {
        "option_0": {"label": "①", "drawn_along": "perpendicular_leg", "is_perpendicular": True},
        "option_1": {"label": "②", "drawn_along": "hypotenuse", "is_perpendicular": False},
    },
    "relations": [
        {
            "type": "correct_construction",
            "correct_entity": "option_0",
            "distractor": "option_1",
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
        text="65. 왼쪽 그림과 같이 삼각자를 사용하여 주어진 직선에 대한 수선을 그은 것을 선택하세요.",
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

    # 왼쪽 예시 그림
    ref_tri = PolygonSlot(id="slot.diagram.ref_tri", prompt="", points=[(108, 224), (222, 224), (222, 108)], fill="#e0f2fe", stroke="#0284c7", stroke_width=1.6)
    ref_hole = PolygonSlot(id="slot.diagram.ref_hole", prompt="", points=[(162, 204), (204, 204), (204, 162)], fill="#ffffff", stroke="#0284c7", stroke_width=1.2)
    ref_line = LineSlot(id="slot.diagram.ref_line", prompt="", x1=108, y1=224, x2=254, y2=224, stroke="#111827", stroke_width=2)

    # ① 수선 (직각을 낀 변)
    card_0 = RectSlot(
        id="slot.choice.option_0",
        prompt="",
        x=324,
        y=92,
        width=240,
        height=168,
        fill="#ffffff",
        stroke="#f59e0b",
        stroke_width=1.8,
        rx=12,
        ry=12,
        interaction={"type": "choice", "role": "answer", "choice_index": 0, "value": "①", "group_id": "slot.choice.group", "include_in_submission": True},
    )
    badge_0 = TextSlot(id="slot.diagram.badge_0", prompt="", text="①", x=348, y=106, font_size=20, font_family='"Noto Sans KR", sans-serif', fill="#4b5563", align="center")
    c0_tri = PolygonSlot(id="slot.diagram.c0_tri", prompt="", points=[(376, 226), (484, 226), (484, 118)], fill="#e0f2fe", stroke="#0284c7", stroke_width=1.5)
    c0_hole = PolygonSlot(id="slot.diagram.c0_hole", prompt="", points=[(426, 208), (466, 208), (466, 168)], fill="#ffffff", stroke="#0284c7", stroke_width=1.2)
    c0_base = LineSlot(id="slot.diagram.c0_base", prompt="", x1=346, y1=226, x2=532, y2=226, stroke="#111827", stroke_width=2)
    c0_drawn = LineSlot(id="slot.diagram.c0_drawn", prompt="", x1=484, y1=226, x2=484, y2=106, stroke="#111827", stroke_width=2)

    # ② 빗변 따라 그은 선
    card_1 = RectSlot(
        id="slot.choice.option_1",
        prompt="",
        x=592,
        y=92,
        width=240,
        height=168,
        fill="#ffffff",
        stroke="#f59e0b",
        stroke_width=1.8,
        rx=12,
        ry=12,
        interaction={"type": "choice", "role": "answer", "choice_index": 1, "value": "②", "group_id": "slot.choice.group", "include_in_submission": True},
    )
    badge_1 = TextSlot(id="slot.diagram.badge_1", prompt="", text="②", x=616, y=106, font_size=20, font_family='"Noto Sans KR", sans-serif', fill="#4b5563", align="center")
    c1_tri = PolygonSlot(id="slot.diagram.c1_tri", prompt="", points=[(644, 226), (752, 226), (752, 118)], fill="#e0f2fe", stroke="#0284c7", stroke_width=1.5)
    c1_hole = PolygonSlot(id="slot.diagram.c1_hole", prompt="", points=[(694, 208), (734, 208), (734, 168)], fill="#ffffff", stroke="#0284c7", stroke_width=1.2)
    c1_base = LineSlot(id="slot.diagram.c1_base", prompt="", x1=614, y1=226, x2=800, y2=226, stroke="#111827", stroke_width=2)
    c1_drawn = LineSlot(id="slot.diagram.c1_drawn", prompt="", x1=644, y1=226, x2=764, y2=106, stroke="#111827", stroke_width=2)

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
            Region(id="region.choices", role="choices", flow="absolute", slot_ids=("slot.choice.option_0", "slot.choice.option_1")),
            Region(
                id="region.diagram",
                role="diagram",
                flow="absolute",
                slot_ids=(
                    "slot.diagram.ref_tri",
                    "slot.diagram.ref_hole",
                    "slot.diagram.ref_line",
                    "slot.diagram.badge_0",
                    "slot.diagram.c0_tri",
                    "slot.diagram.c0_hole",
                    "slot.diagram.c0_base",
                    "slot.diagram.c0_drawn",
                    "slot.diagram.badge_1",
                    "slot.diagram.c1_tri",
                    "slot.diagram.c1_hole",
                    "slot.diagram.c1_base",
                    "slot.diagram.c1_drawn",
                ),
            ),
        ),
        slots=(
            stem_text_slot,
            ref_tri,
            ref_hole,
            ref_line,
            card_0,
            badge_0,
            c0_tri,
            c0_hole,
            c0_base,
            c0_drawn,
            card_1,
            badge_1,
            c1_tri,
            c1_hole,
            c1_base,
            c1_drawn,
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
        {"ref": "option_0", "value": "직각을 낀 변을 따라 그은 선"},
        {"ref": "option_1", "value": "빗변을 따라 그은 선"},
    ],
    "target": {"ref": "slot.choice.option_0", "label": "수선을 바르게 그은 것", "unit": ""},
    "method": "set_square_perpendicular",
    "steps": [
        {
            "id": "identify_perpendicular_line",
            "expr": "①",
            "explanation": "삼각자에서 직각을 낀 다른 한 변을 따라 선을 그은 ①이 수선입니다.",
            "value": "①",
        },
    ],
    "answer": ANSWER,
}


if __name__ == "__main__":
    print(f"[{PROBLEM_TEMPLATE.id}] 템플릿 컴파일 성공!")
    print(f"- 제목: {PROBLEM_TEMPLATE.title}")
    print(f"- 캔버스: {PROBLEM_TEMPLATE.canvas.width} x {PROBLEM_TEMPLATE.canvas.height}")
    print(f"- 구역 수: {len(PROBLEM_TEMPLATE.regions)}")
