"""ModuMath Problem DSL: 서로 수직인 두 직선 선택하기 (S3_초등_4_007528)"""

from __future__ import annotations

from modu_math.dsl import (
    Canvas,
    LineSlot,
    ProblemTemplate,
    RectSlot,
    Region,
    TextBoxSlot,
    TextSlot,
)


# ==============================================================================
# 1. 문제 식별자 및 제목 (Problem Metadata)
# ==============================================================================
PROBLEM_ID = "S3_초등_4_007528"
PROBLEM_TITLE = "두 직선이 서로 수직인 것 선택하기"


# ==============================================================================
# 2. 정답 및 오답 진단 정의 (Answer & Diagnostic Key)
# ==============================================================================
ANSWER = {
    "value": "②",
    "answer_index": 1,
    "unit": "",
    "values": ["②"],
    "choices": [
        "①",
        "②",
    ],
    "blanks": [],
    "answer_key": [
        {
            "slot_id": "slot.choice.option_1",
            "value": "②",
            "diagnostics": [
                {
                    "id": "diag.chose_non_perpendicular",
                    "condition": "answer_equals_1",
                    "concept": "수직",
                    "reason": "직각을 이루지 않고 비스듬히 만나는 두 직선(①)을 선택함",
                    "feedback": "두 직선이 만나서 이루는 각이 직각(90°)일 때 서로 수직이라고 합니다. ②의 두 직선이 서로 수직입니다.",
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
    "problem_type": "multiple_choice_perpendicular_lines",
    "metadata": {
        "school": "초등학교",
        "grade": 4,
        "semester": "1학기",
        "chapter": "04단원_평면도형의 이동",
        "difficulty": "하",
    },
    "entities": {
        "pair_0": {"label": "①", "is_perpendicular": False},
        "pair_1": {"label": "②", "is_perpendicular": True},
    },
    "relations": [
        {
            "type": "perpendicular",
            "correct_entity": "pair_1",
            "distractor": "pair_0",
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
        text="63. 두 직선이 서로 수직인 것을 선택하세요.",
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

    # ① 비스듬히 만나는 두 직선
    card_0 = RectSlot(
        id="slot.choice.option_0",
        prompt="",
        x=156,
        y=84,
        width=240,
        height=176,
        fill="#ffffff",
        stroke="#e5e7eb",
        stroke_width=1.5,
        rx=10,
        ry=10,
        interaction={"type": "choice", "role": "answer", "choice_index": 0, "value": "①", "group_id": "slot.choice.group", "include_in_submission": True},
    )
    badge_0 = TextSlot(id="slot.diagram.badge_0", prompt="", text="①", x=182, y=100, font_size=20, font_family='"Noto Sans KR", sans-serif', fill="#4b5563", align="center")
    l0_h = LineSlot(id="slot.diagram.l0_h", prompt="", x1=196, y1=168, x2=360, y2=168, stroke="#111827", stroke_width=2)
    l0_s = LineSlot(id="slot.diagram.l0_s", prompt="", x1=236, y1=102, x2=328, y2=238, stroke="#111827", stroke_width=2)

    # ② 서로 수직인 두 직선
    card_1 = RectSlot(
        id="slot.choice.option_1",
        prompt="",
        x=490,
        y=84,
        width=240,
        height=176,
        fill="#ffffff",
        stroke="#e5e7eb",
        stroke_width=1.5,
        rx=10,
        ry=10,
        interaction={"type": "choice", "role": "answer", "choice_index": 1, "value": "②", "group_id": "slot.choice.group", "include_in_submission": True},
    )
    badge_1 = TextSlot(id="slot.diagram.badge_1", prompt="", text="②", x=516, y=100, font_size=20, font_family='"Noto Sans KR", sans-serif', fill="#4b5563", align="center")
    l1_h = LineSlot(id="slot.diagram.l1_h", prompt="", x1=554, y1=114, x2=682, y2=114, stroke="#111827", stroke_width=2)
    l1_v = LineSlot(id="slot.diagram.l1_v", prompt="", x1=682, y1=114, x2=682, y2=238, stroke="#111827", stroke_width=2)

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
                slot_ids=("slot.diagram.badge_0", "slot.diagram.l0_h", "slot.diagram.l0_s", "slot.diagram.badge_1", "slot.diagram.l1_h", "slot.diagram.l1_v"),
            ),
        ),
        slots=(
            stem_text_slot,
            card_0,
            badge_0,
            l0_h,
            l0_s,
            card_1,
            badge_1,
            l1_h,
            l1_v,
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
        {"ref": "pair_0", "value": "비스듬히 만나는 두 직선"},
        {"ref": "pair_1", "value": "직각으로 만나는 두 직선"},
    ],
    "target": {"ref": "slot.choice.option_1", "label": "서로 수직인 두 직선", "unit": ""},
    "method": "right_angle_identification",
    "steps": [
        {
            "id": "identify_perpendicular",
            "expr": "②",
            "explanation": "두 직선이 만나서 이루는 각이 직각(90°)인 것은 ②입니다.",
            "value": "②",
        },
    ],
    "answer": ANSWER,
}


if __name__ == "__main__":
    print(f"[{PROBLEM_TEMPLATE.id}] 템플릿 컴파일 성공!")
    print(f"- 제목: {PROBLEM_TEMPLATE.title}")
    print(f"- 캔버스: {PROBLEM_TEMPLATE.canvas.width} x {PROBLEM_TEMPLATE.canvas.height}")
    print(f"- 구역 수: {len(PROBLEM_TEMPLATE.regions)}")
