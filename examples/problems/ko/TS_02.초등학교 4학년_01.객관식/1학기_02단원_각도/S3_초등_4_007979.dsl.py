"""ModuMath Problem DSL: 두 각 중에서 더 작은 각 선택하기 (S3_초등_4_007979)"""

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
PROBLEM_ID = "S3_초등_4_007979"
PROBLEM_TITLE = "두 각 중에서 더 작은 각 선택하기"


# ==============================================================================
# 2. 정답 및 오답 진단 정의 (Answer & Diagnostic Key)
# ==============================================================================
ANSWER = {
    "value": "나",
    "answer_index": 1,
    "unit": "",
    "values": ["나"],
    "choices": [
        "가",
        "나",
    ],
    "blanks": [],
    "answer_key": [
        {
            "slot_id": "slot.choice.option_1",
            "value": "나",
            "diagnostics": [
                {
                    "id": "diag.chose_larger_angle",
                    "condition": "answer_equals_ga",
                    "concept": "각의 크기 비교",
                    "reason": "더 많이 벌어진 각 가를 더 작은 각으로 선택함",
                    "feedback": "두 변이 더 적게 벌어진 각을 찾습니다. 나(약 72°)가 가(약 110°)보다 더 작습니다.",
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
        "angle_ga": {"label": "가", "approx_deg": 110},
        "angle_na": {"label": "나", "approx_deg": 72},
    },
    "relations": [
        {
            "type": "less_than",
            "smaller": "angle_na",
            "larger": "angle_ga",
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
        text="87. 두 각 중에서 더 작은 각을 선택하세요.",
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

    outer_box = RectSlot(id="slot.diagram.outer_box", prompt="", x=156, y=82, width=574, height=180, fill="#ffffff", stroke="#f59e0b", stroke_width=2, rx=4, ry=4)

    # 각 가 (둔각 ~110도)
    choice_ga = TextSlot(
        id="slot.choice.option_0",
        prompt="",
        text="가",
        x=212,
        y=108,
        font_size=24,
        font_family='"Noto Sans KR", sans-serif',
        fill="#111827",
        align="center",
        interaction={"type": "choice", "role": "answer", "choice_index": 0, "value": "가", "group_id": "slot.choice.group", "include_in_submission": True},
    )
    ga_h = LineSlot(id="slot.diagram.ga_h", prompt="", x1=286, y1=224, x2=416, y2=224, stroke="#111827", stroke_width=2)
    ga_s = LineSlot(id="slot.diagram.ga_s", prompt="", x1=286, y1=224, x2=244, y2=114, stroke="#111827", stroke_width=2)
    ga_arc = PathSlot(id="slot.diagram.ga_arc", prompt="", d="M 308 224 A 22 22 0 0 0 278 203", fill="none", stroke="#ec4899", stroke_width=1.6)

    # 각 나 (예각 V자 ~72도)
    choice_na = TextSlot(
        id="slot.choice.option_1",
        prompt="",
        text="나",
        x=486,
        y=108,
        font_size=24,
        font_family='"Noto Sans KR", sans-serif',
        fill="#111827",
        align="center",
        interaction={"type": "choice", "role": "answer", "choice_index": 1, "value": "나", "group_id": "slot.choice.group", "include_in_submission": True},
    )
    na_l = LineSlot(id="slot.diagram.na_l", prompt="", x1=606, y1=218, x2=532, y2=118, stroke="#111827", stroke_width=2)
    na_r = LineSlot(id="slot.diagram.na_r", prompt="", x1=606, y1=218, x2=682, y2=118, stroke="#111827", stroke_width=2)
    na_arc = PathSlot(id="slot.diagram.na_arc", prompt="", d="M 592 200 A 22 22 0 0 1 620 200", fill="none", stroke="#ec4899", stroke_width=1.6)

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
                id="region.diagram",
                role="diagram",
                flow="absolute",
                slot_ids=(
                    "slot.diagram.outer_box",
                    "slot.diagram.ga_h",
                    "slot.diagram.ga_s",
                    "slot.diagram.ga_arc",
                    "slot.diagram.na_l",
                    "slot.diagram.na_r",
                    "slot.diagram.na_arc",
                ),
            ),
            Region(
                id="region.choices",
                role="choices",
                flow="absolute",
                slot_ids=("slot.choice.option_0", "slot.choice.option_1"),
            ),
        ),
        slots=(
            stem_text_slot,
            outer_box,
            choice_ga,
            ga_h,
            ga_s,
            ga_arc,
            choice_na,
            na_l,
            na_r,
            na_arc,
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
        {"ref": "angle_ga", "value": 110, "unit": "도"},
        {"ref": "angle_na", "value": 72, "unit": "도"},
    ],
    "target": {"ref": "slot.choice.option_1", "label": "더 작은 각", "unit": ""},
    "method": "visual_angle_comparison",
    "steps": [
        {
            "id": "compare_angles",
            "expr": "나 < 가",
            "explanation": "두 변이 더 적게 벌어진 각은 나입니다.",
            "value": "나",
        },
    ],
    "answer": ANSWER,
}


if __name__ == "__main__":
    print(f"[{PROBLEM_TEMPLATE.id}] 템플릿 컴파일 성공!")
    print(f"- 제목: {PROBLEM_TEMPLATE.title}")
    print(f"- 캔버스: {PROBLEM_TEMPLATE.canvas.width} x {PROBLEM_TEMPLATE.canvas.height}")
    print(f"- 구역 수: {len(PROBLEM_TEMPLATE.regions)}")
