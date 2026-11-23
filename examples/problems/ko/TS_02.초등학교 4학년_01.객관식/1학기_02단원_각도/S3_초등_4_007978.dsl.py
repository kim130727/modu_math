"""ModuMath Problem DSL: 더 많이 벌어진 컴퍼스 선택하기 (S3_초등_4_007978)"""

from __future__ import annotations

from modu_math.dsl import (
    Canvas,
    CircleSlot,
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
PROBLEM_ID = "S3_초등_4_007978"
PROBLEM_TITLE = "두 컴퍼스 중 더 많이 벌어진 컴퍼스 선택하기"


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
                    "id": "diag.chose_narrower_compass",
                    "condition": "answer_equals_1",
                    "concept": "각의 크기 비교",
                    "reason": "더 좁게 벌어진 왼쪽 컴퍼스를 선택함",
                    "feedback": "컴퍼스의 두 다리가 더 많이 벌어진 쪽이 각의 크기가 더 큽니다. 오른쪽 컴퍼스(②)가 더 많이 벌어져 있습니다.",
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
    "problem_type": "multiple_choice_angle_comparison",
    "metadata": {
        "school": "초등학교",
        "grade": 4,
        "semester": "1학기",
        "chapter": "02단원_각도",
        "difficulty": "하",
    },
    "entities": {
        "compass_0": {"label": "①", "approx_deg": 42},
        "compass_1": {"label": "②", "approx_deg": 66},
    },
    "relations": [
        {
            "type": "greater_than",
            "larger": "compass_1",
            "smaller": "compass_0",
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
        text="86. 더 많이 벌어진 컴퍼스를 선택하세요.",
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

    # 왼쪽 컴퍼스 ① (~42도)
    card_0 = RectSlot(
        id="slot.choice.option_0",
        prompt="",
        x=156,
        y=84,
        width=240,
        height=188,
        fill="#ffffff",
        stroke="#e5e7eb",
        stroke_width=1.5,
        rx=10,
        ry=10,
        interaction={"type": "choice", "role": "answer", "choice_index": 0, "value": "①", "group_id": "slot.choice.group", "include_in_submission": True},
    )
    badge_0 = TextSlot(id="slot.diagram.badge_0", prompt="", text="①", x=182, y=100, font_size=20, font_family='"Noto Sans KR", sans-serif', fill="#4b5563", align="center")
    c0_leg1 = LineSlot(id="slot.diagram.c0_leg1", prompt="", x1=320, y1=114, x2=212, y2=166, stroke="#57534e", stroke_width=6)
    c0_leg2 = LineSlot(id="slot.diagram.c0_leg2", prompt="", x1=320, y1=114, x2=262, y2=238, stroke="#57534e", stroke_width=6)
    c0_hinge = CircleSlot(id="slot.diagram.c0_hinge", prompt="", cx=320, cy=114, r=8, fill="#e7e5e4", stroke="#57534e", stroke_width=2)
    c0_arc = PathSlot(id="slot.diagram.c0_arc", prompt="", d="M 294 126 A 28 28 0 0 0 304 139", fill="none", stroke="#ec4899", stroke_width=1.8)

    # 오른쪽 컴퍼스 ② (~66도)
    card_1 = RectSlot(
        id="slot.choice.option_1",
        prompt="",
        x=490,
        y=84,
        width=240,
        height=188,
        fill="#ffffff",
        stroke="#e5e7eb",
        stroke_width=1.5,
        rx=10,
        ry=10,
        interaction={"type": "choice", "role": "answer", "choice_index": 1, "value": "②", "group_id": "slot.choice.group", "include_in_submission": True},
    )
    badge_1 = TextSlot(id="slot.diagram.badge_1", prompt="", text="②", x=516, y=100, font_size=20, font_family='"Noto Sans KR", sans-serif', fill="#4b5563", align="center")
    c1_leg1 = LineSlot(id="slot.diagram.c1_leg1", prompt="", x1=576, y1=114, x2=576, y2=250, stroke="#57534e", stroke_width=6)
    c1_leg2 = LineSlot(id="slot.diagram.c1_leg2", prompt="", x1=576, y1=114, x2=698, y2=176, stroke="#57534e", stroke_width=6)
    c1_hinge = CircleSlot(id="slot.diagram.c1_hinge", prompt="", cx=576, cy=114, r=8, fill="#e7e5e4", stroke="#57534e", stroke_width=2)
    c1_arc = PathSlot(id="slot.diagram.c1_arc", prompt="", d="M 576 142 A 28 28 0 0 0 601 127", fill="none", stroke="#ec4899", stroke_width=1.8)

    return ProblemTemplate(
        id=PROBLEM_ID,
        title=PROBLEM_TITLE,
        canvas=Canvas(
            width=886,
            height=300,
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
                    "slot.diagram.c0_leg1",
                    "slot.diagram.c0_leg2",
                    "slot.diagram.c0_hinge",
                    "slot.diagram.c0_arc",
                    "slot.diagram.badge_1",
                    "slot.diagram.c1_leg1",
                    "slot.diagram.c1_leg2",
                    "slot.diagram.c1_hinge",
                    "slot.diagram.c1_arc",
                ),
            ),
        ),
        slots=(
            stem_text_slot,
            card_0,
            badge_0,
            c0_leg1,
            c0_leg2,
            c0_hinge,
            c0_arc,
            card_1,
            badge_1,
            c1_leg1,
            c1_leg2,
            c1_hinge,
            c1_arc,
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
        {"ref": "compass_0", "value": 42, "unit": "도"},
        {"ref": "compass_1", "value": 66, "unit": "도"},
    ],
    "target": {"ref": "slot.choice.option_1", "label": "더 많이 벌어진 컴퍼스", "unit": ""},
    "method": "visual_angle_comparison",
    "steps": [
        {
            "id": "compare_compasses",
            "expr": "② > ①",
            "explanation": "오른쪽 컴퍼스(②)가 왼쪽 컴퍼스(①)보다 더 많이 벌어져 있습니다.",
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
