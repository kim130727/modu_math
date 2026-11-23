"""ModuMath Problem DSL: 예각 찾아 선택하기 (S3_초등_4_007983)"""

from __future__ import annotations

from modu_math.dsl import (
    Canvas,
    LineSlot,
    PathSlot,
    ProblemTemplate,
    RectSlot,
    Region,
    TextBoxSlot,
    TextSlot,
)


# ==============================================================================
# 1. 문제 식별자 및 제목 (Problem Metadata)
# ==============================================================================
PROBLEM_ID = "S3_초등_4_007983"
PROBLEM_TITLE = "두 각 중에서 예각 찾아 선택하기"


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
                    "id": "diag.chose_obtuse_angle",
                    "condition": "answer_equals_2",
                    "concept": "예각과 둔각",
                    "reason": "직각(90°)보다 큰 둔각(②)을 예각으로 선택함",
                    "feedback": "예각은 각도가 0°보다 크고 90°(직각)보다 작은 각입니다. ②는 직각보다 큰 둔각이고, ①이 예각입니다.",
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
    "problem_type": "multiple_choice_angle_classification",
    "metadata": {
        "school": "초등학교",
        "grade": 4,
        "semester": "1학기",
        "chapter": "02단원_각도",
        "difficulty": "하",
    },
    "entities": {
        "angle_0": {"label": "①", "approx_deg": 60, "category": "acute"},
        "angle_1": {"label": "②", "approx_deg": 108, "category": "obtuse"},
    },
    "relations": [
        {
            "type": "classification",
            "target_concept": "예각",
            "correct_entity": "angle_0",
            "distractor": "angle_1",
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
        text="91. 예각을 찾아 선택하세요.",
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

    # 왼쪽 각 ① (예각 ~60도)
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
    a0_h = LineSlot(id="slot.diagram.a0_h", prompt="", x1=206, y1=224, x2=346, y2=224, stroke="#111827", stroke_width=2)
    a0_s = LineSlot(id="slot.diagram.a0_s", prompt="", x1=346, y1=224, x2=276, y2=110, stroke="#111827", stroke_width=2)
    a0_arc = PathSlot(id="slot.diagram.a0_arc", prompt="", d="M 324 224 A 22 22 0 0 1 335 205", fill="none", stroke="#ec4899", stroke_width=1.6)

    # 오른쪽 각 ② (둔각 ~108도)
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
    a1_h = LineSlot(id="slot.diagram.a1_h", prompt="", x1=540, y1=224, x2=666, y2=224, stroke="#111827", stroke_width=2)
    a1_s = LineSlot(id="slot.diagram.a1_s", prompt="", x1=666, y1=224, x2=704, y2=110, stroke="#111827", stroke_width=2)
    a1_arc = PathSlot(id="slot.diagram.a1_arc", prompt="", d="M 644 224 A 22 22 0 0 1 673 203", fill="none", stroke="#ec4899", stroke_width=1.6)

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
            Region(
                id="region.choices",
                role="choices",
                flow="absolute",
                slot_ids=("slot.choice.option_0", "slot.choice.option_1"),
            ),
            Region(
                id="region.diagram",
                role="diagram",
                flow="absolute",
                slot_ids=(
                    "slot.diagram.badge_0",
                    "slot.diagram.a0_h",
                    "slot.diagram.a0_s",
                    "slot.diagram.a0_arc",
                    "slot.diagram.badge_1",
                    "slot.diagram.a1_h",
                    "slot.diagram.a1_s",
                    "slot.diagram.a1_arc",
                ),
            ),
        ),
        slots=(
            stem_text_slot,
            card_0,
            badge_0,
            a0_h,
            a0_s,
            a0_arc,
            card_1,
            badge_1,
            a1_h,
            a1_s,
            a1_arc,
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
        {"ref": "angle_0", "value": 60, "unit": "도"},
        {"ref": "angle_1", "value": 108, "unit": "도"},
    ],
    "target": {"ref": "slot.choice.option_0", "label": "예각", "unit": ""},
    "method": "acute_angle_classification",
    "steps": [
        {
            "id": "classify_acute",
            "expr": "0° < ① < 90°",
            "explanation": "각도가 0°보다 크고 90°보다 작은 각은 ①입니다.",
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
