"""ModuMath Problem DSL: 나무 막대로 만든 각의 크기 비교 (S3_초등_4_007974)"""

from __future__ import annotations

from modu_math.dsl import (
    Canvas,
    LineSlot,
    PathSlot,
    ProblemTemplate,
    Region,
    TextBoxSlot,
    TextSlot,
)


# ==============================================================================
# 1. 문제 식별자 및 제목 (Problem Metadata)
# ==============================================================================
PROBLEM_ID = "S3_초등_4_007974"
PROBLEM_TITLE = "두 각을 겹쳐서 각의 크기 비교하기"


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
                    "id": "diag.chose_smaller_angle",
                    "condition": "answer_equals_ga",
                    "concept": "각의 크기 비교",
                    "reason": "더 적게 벌어진 각 가를 더 큰 각으로 선택함",
                    "feedback": "각의 크기는 변의 길이와 관계없이 두 변이 많이 벌어질수록 큰 각입니다. 나가 가보다 더 많이 벌어져 있으므로 나의 각의 크기가 더 큽니다.",
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
        "angle_ga": {"label": "가", "approx_deg": 34},
        "angle_na": {"label": "나", "approx_deg": 78},
    },
    "relations": [
        {
            "type": "greater_than",
            "larger": "angle_na",
            "smaller": "angle_ga",
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
        text="82. 나무 막대로 각을 만든 후 가를 나에 겹쳐 보았습니다. 알맞은 것을 선택하세요.",
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

    # 각 가 (왼쪽)
    label_ga = TextSlot(id="slot.diagram.label_ga", prompt="", text="가", x=120, y=94, font_size=22, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center")
    ga_h = LineSlot(id="slot.diagram.ga_h", prompt="", x1=136, y1=200, x2=256, y2=200, stroke="#d97706", stroke_width=6)
    ga_s = LineSlot(id="slot.diagram.ga_s", prompt="", x1=136, y1=200, x2=236, y2=134, stroke="#d97706", stroke_width=6)
    ga_arc = PathSlot(id="slot.diagram.ga_arc", prompt="", d="M 164 200 A 28 28 0 0 0 159 185", fill="none", stroke="#ec4899", stroke_width=1.8)

    # 각 나 (가운데)
    label_na = TextSlot(id="slot.diagram.label_na", prompt="", text="나", x=330, y=94, font_size=22, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center")
    na_h = LineSlot(id="slot.diagram.na_h", prompt="", x1=346, y1=200, x2=466, y2=200, stroke="#d97706", stroke_width=6)
    na_s = LineSlot(id="slot.diagram.na_s", prompt="", x1=346, y1=200, x2=370, y2=100, stroke="#d97706", stroke_width=6)
    na_arc = PathSlot(id="slot.diagram.na_arc", prompt="", d="M 374 200 A 28 28 0 0 0 353 173", fill="none", stroke="#ec4899", stroke_width=1.8)

    # 화살표
    arrow = TextSlot(id="slot.diagram.arrow", prompt="", text="➡", x=546, y=144, font_size=26, font_family='"Noto Sans KR", sans-serif', fill="#6b7280", align="center")

    # 겹친 그림 (오른쪽)
    ov_na_label = TextSlot(id="slot.diagram.ov_na_label", prompt="", text="나", x=664, y=82, font_size=20, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center")
    ov_ga_label = TextSlot(id="slot.diagram.ov_ga_label", prompt="", text="가", x=760, y=126, font_size=20, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center")
    ov_h = LineSlot(id="slot.diagram.ov_h", prompt="", x1=640, y1=200, x2=760, y2=200, stroke="#d97706", stroke_width=6)
    ov_ga_s = LineSlot(id="slot.diagram.ov_ga_s", prompt="", x1=640, y1=200, x2=740, y2=134, stroke="#d97706", stroke_width=6)
    ov_na_s = LineSlot(id="slot.diagram.ov_na_s", prompt="", x1=640, y1=200, x2=664, y2=100, stroke="#d97706", stroke_width=6)
    ov_arc_1 = PathSlot(id="slot.diagram.ov_arc_1", prompt="", d="M 672 200 A 32 32 0 0 0 667 182", fill="none", stroke="#ec4899", stroke_width=1.6)
    ov_arc_2 = PathSlot(id="slot.diagram.ov_arc_2", prompt="", d="M 664 200 A 24 24 0 0 0 646 177", fill="none", stroke="#ec4899", stroke_width=1.6)

    # 선택 영역: ( 가 , 나 )의 각의 크기가 더 큽니다.
    paren_left = TextSlot(id="slot.choice.paren_left", prompt="", text="(", x=255, y=242, font_size=24, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center")
    choice_0 = TextSlot(
        id="slot.choice.option_0",
        prompt="",
        text="가",
        x=288,
        y=242,
        font_size=22,
        font_family='"Noto Sans KR", sans-serif',
        fill="#111827",
        align="center",
        interaction={"type": "choice", "role": "answer", "choice_index": 0, "value": "가", "group_id": "slot.choice.group", "include_in_submission": True},
    )
    comma = TextSlot(id="slot.choice.comma", prompt="", text=",", x=318, y=242, font_size=22, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center")
    choice_1 = TextSlot(
        id="slot.choice.option_1",
        prompt="",
        text="나",
        x=348,
        y=242,
        font_size=22,
        font_family='"Noto Sans KR", sans-serif',
        fill="#111827",
        align="center",
        interaction={"type": "choice", "role": "answer", "choice_index": 1, "value": "나", "group_id": "slot.choice.group", "include_in_submission": True},
    )
    paren_right = TextSlot(id="slot.choice.paren_right", prompt="", text=")의 각의 크기가 더 큽니다.", x=508, y=242, font_size=22, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center")

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
                id="region.diagram",
                role="diagram",
                flow="absolute",
                slot_ids=(
                    "slot.diagram.label_ga",
                    "slot.diagram.ga_h",
                    "slot.diagram.ga_s",
                    "slot.diagram.ga_arc",
                    "slot.diagram.label_na",
                    "slot.diagram.na_h",
                    "slot.diagram.na_s",
                    "slot.diagram.na_arc",
                    "slot.diagram.arrow",
                    "slot.diagram.ov_na_label",
                    "slot.diagram.ov_ga_label",
                    "slot.diagram.ov_h",
                    "slot.diagram.ov_ga_s",
                    "slot.diagram.ov_na_s",
                    "slot.diagram.ov_arc_1",
                    "slot.diagram.ov_arc_2",
                ),
            ),
            Region(
                id="region.choices",
                role="choices",
                flow="absolute",
                slot_ids=(
                    "slot.choice.paren_left",
                    "slot.choice.option_0",
                    "slot.choice.comma",
                    "slot.choice.option_1",
                    "slot.choice.paren_right",
                ),
            ),
        ),
        slots=(
            stem_text_slot,
            label_ga,
            ga_h,
            ga_s,
            ga_arc,
            label_na,
            na_h,
            na_s,
            na_arc,
            arrow,
            ov_na_label,
            ov_ga_label,
            ov_h,
            ov_ga_s,
            ov_na_s,
            ov_arc_1,
            ov_arc_2,
            paren_left,
            choice_0,
            comma,
            choice_1,
            paren_right,
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
        {"ref": "angle_ga", "value": 34, "unit": "도"},
        {"ref": "angle_na", "value": 78, "unit": "도"},
    ],
    "target": {"ref": "slot.choice.option_1", "label": "더 큰 각", "unit": ""},
    "method": "direct_overlap_comparison",
    "steps": [
        {
            "id": "compare_angles",
            "expr": "나 > 가",
            "explanation": "두 변이 더 많이 벌어진 나가 가보다 큰 각입니다.",
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
