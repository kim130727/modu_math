"""ModuMath Problem DSL: 세 각 중에서 가장 큰 각 선택하기 (S3_초등_4_007981)"""

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
PROBLEM_ID = "S3_초등_4_007981"
PROBLEM_TITLE = "세 각 중에서 가장 큰 각 선택하기"


# ==============================================================================
# 2. 정답 및 오답 진단 정의 (Answer & Diagnostic Key)
# ==============================================================================
ANSWER = {
    "value": "다",
    "answer_index": 2,
    "unit": "",
    "values": ["다"],
    "choices": [
        "가",
        "나",
        "다",
    ],
    "blanks": [],
    "answer_key": [
        {
            "slot_id": "slot.choice.option_2",
            "value": "다",
            "diagnostics": [
                {
                    "id": "diag.chose_ga",
                    "condition": "answer_equals_ga",
                    "concept": "각의 크기 비교",
                    "reason": "예각에 가까운 가를 가장 큰 각으로 선택함",
                    "feedback": "두 변이 가장 많이 벌어진 각을 찾습니다. 다는 둔각으로 가장 크게 벌어져 있습니다.",
                },
                {
                    "id": "diag.chose_na",
                    "condition": "answer_equals_na",
                    "concept": "각의 크기 비교",
                    "reason": "가장 작은 예각인 나를 가장 큰 각으로 선택함",
                    "feedback": "나는 세 각 중에서 가장 작습니다. 두 변이 가장 많이 벌어진 다를 선택하세요.",
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
        "angle_ga": {"label": "가", "approx_deg": 84},
        "angle_na": {"label": "나", "approx_deg": 42},
        "angle_da": {"label": "다", "approx_deg": 124},
    },
    "relations": [
        {
            "type": "maximum",
            "largest": "angle_da",
            "others": ["angle_ga", "angle_na"],
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
        text="89. 세 각 중에서 가장 큰 각을 선택하세요.",
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

    outer_box = RectSlot(id="slot.diagram.outer_box", prompt="", x=46, y=82, width=794, height=180, fill="#ffffff", stroke="#8b5cf6", stroke_width=1.8, rx=4, ry=4)

    # 각 가
    choice_ga = TextSlot(
        id="slot.choice.option_0",
        prompt="",
        text="가",
        x=88,
        y=102,
        font_size=24,
        font_family='"Noto Sans KR", sans-serif',
        fill="#111827",
        align="center",
        interaction={"type": "choice", "role": "answer", "choice_index": 0, "value": "가", "group_id": "slot.choice.group", "include_in_submission": True},
    )
    ga_l = LineSlot(id="slot.diagram.ga_l", prompt="", x1=196, y1=224, x2=114, y2=124, stroke="#111827", stroke_width=2)
    ga_r = LineSlot(id="slot.diagram.ga_r", prompt="", x1=196, y1=224, x2=282, y2=124, stroke="#111827", stroke_width=2)
    ga_arc = PathSlot(id="slot.diagram.ga_arc", prompt="", d="M 182 207 A 22 22 0 0 1 210 207", fill="none", stroke="#ec4899", stroke_width=1.6)

    # 각 나
    choice_na = TextSlot(
        id="slot.choice.option_1",
        prompt="",
        text="나",
        x=356,
        y=102,
        font_size=24,
        font_family='"Noto Sans KR", sans-serif',
        fill="#111827",
        align="center",
        interaction={"type": "choice", "role": "answer", "choice_index": 1, "value": "나", "group_id": "slot.choice.group", "include_in_submission": True},
    )
    na_h = LineSlot(id="slot.diagram.na_h", prompt="", x1=390, y1=224, x2=532, y2=224, stroke="#111827", stroke_width=2)
    na_s = LineSlot(id="slot.diagram.na_s", prompt="", x1=532, y1=224, x2=426, y2=128, stroke="#111827", stroke_width=2)
    na_arc = PathSlot(id="slot.diagram.na_arc", prompt="", d="M 508 224 A 24 24 0 0 1 514 208", fill="none", stroke="#ec4899", stroke_width=1.6)

    # 각 다 (둔각 ~124도)
    choice_da = TextSlot(
        id="slot.choice.option_2",
        prompt="",
        text="다",
        x=612,
        y=102,
        font_size=24,
        font_family='"Noto Sans KR", sans-serif',
        fill="#111827",
        align="center",
        interaction={"type": "choice", "role": "answer", "choice_index": 2, "value": "다", "group_id": "slot.choice.group", "include_in_submission": True},
    )
    da_l = LineSlot(id="slot.diagram.da_l", prompt="", x1=718, y1=142, x2=620, y2=202, stroke="#111827", stroke_width=2)
    da_r = LineSlot(id="slot.diagram.da_r", prompt="", x1=718, y1=142, x2=818, y2=202, stroke="#111827", stroke_width=2)
    da_arc = PathSlot(id="slot.diagram.da_arc", prompt="", d="M 699 154 A 22 22 0 0 0 737 154", fill="none", stroke="#ec4899", stroke_width=1.6)

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
                    "slot.diagram.ga_l",
                    "slot.diagram.ga_r",
                    "slot.diagram.ga_arc",
                    "slot.diagram.na_h",
                    "slot.diagram.na_s",
                    "slot.diagram.na_arc",
                    "slot.diagram.da_l",
                    "slot.diagram.da_r",
                    "slot.diagram.da_arc",
                ),
            ),
            Region(
                id="region.choices",
                role="choices",
                flow="absolute",
                slot_ids=("slot.choice.option_0", "slot.choice.option_1", "slot.choice.option_2"),
            ),
        ),
        slots=(
            stem_text_slot,
            outer_box,
            choice_ga,
            ga_l,
            ga_r,
            ga_arc,
            choice_na,
            na_h,
            na_s,
            na_arc,
            choice_da,
            da_l,
            da_r,
            da_arc,
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
        {"ref": "angle_ga", "value": 84, "unit": "도"},
        {"ref": "angle_na", "value": 42, "unit": "도"},
        {"ref": "angle_da", "value": 124, "unit": "도"},
    ],
    "target": {"ref": "slot.choice.option_2", "label": "가장 큰 각", "unit": ""},
    "method": "visual_angle_comparison",
    "steps": [
        {
            "id": "find_largest_angle",
            "expr": "다 > 가 > 나",
            "explanation": "두 변이 가장 많이 벌어진 각은 다입니다.",
            "value": "다",
        },
    ],
    "answer": ANSWER,
}


if __name__ == "__main__":
    print(f"[{PROBLEM_TEMPLATE.id}] 템플릿 컴파일 성공!")
    print(f"- 제목: {PROBLEM_TEMPLATE.title}")
    print(f"- 캔버스: {PROBLEM_TEMPLATE.canvas.width} x {PROBLEM_TEMPLATE.canvas.height}")
    print(f"- 구역 수: {len(PROBLEM_TEMPLATE.regions)}")
