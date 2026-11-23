"""ModuMath Problem DSL: 수직선에서 큰 수의 크기 비교 (S3_초등_4_007948)"""

from __future__ import annotations

from modu_math.dsl import (
    Canvas,
    CircleSlot,
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
PROBLEM_ID = "S3_초등_4_007948"
PROBLEM_TITLE = "수직선을 보고 28300과 28600의 크기 비교하기"


# ==============================================================================
# 2. 정답 및 오답 진단 정의 (Answer & Diagnostic Key)
# ==============================================================================
ANSWER = {
    "value": "28600",
    "answer_index": 1,
    "unit": "",
    "values": ["28600"],
    "choices": [
        "28300",
        "28600",
    ],
    "blanks": [],
    "answer_key": [
        {
            "slot_id": "slot.choice.option_1",
            "value": "28600",
            "diagnostics": [
                {
                    "id": "diag.chose_smaller_number",
                    "condition": "answer_equals_28300",
                    "concept": "수의 크기 비교",
                    "reason": "더 큰 수 대신 더 작은 수인 28300을 선택함",
                    "feedback": "수직선에서 오른쪽에 위치한 수가 왼쪽에 위치한 수보다 더 큰 수입니다. 28600이 더 오른쪽에 있습니다.",
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
    "problem_type": "multiple_choice_number_comparison_on_number_line",
    "metadata": {
        "school": "초등학교",
        "grade": 4,
        "semester": "1학기",
        "chapter": "01단원_큰 수",
        "difficulty": "하",
    },
    "entities": {
        "num_left": {"label": "28300", "value": 28300},
        "num_right": {"label": "28600", "value": 28600},
    },
    "relations": [
        {
            "type": "greater_than",
            "expression": "28600 > 28300",
            "larger": "num_right",
            "smaller": "num_left",
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
        text="8. 수직선을 보고 28300과 28600의 크기를 비교하여 알맞은 수를 선택하세요.",
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

    # 왼쪽 '작은 수' / 오른쪽 '큰 수' 배지
    left_badge_bg = RectSlot(
        id="slot.diagram.left_badge_bg",
        prompt="",
        x=36,
        y=114,
        width=88,
        height=38,
        fill="#fef3c7",
        stroke="#f59e0b",
        stroke_width=1.5,
        rx=16,
        ry=16,
    )
    left_badge_text = TextSlot(
        id="slot.diagram.left_badge_text",
        prompt="",
        text="작은 수",
        x=80,
        y=121,
        font_size=18,
        font_family='"Noto Sans KR", sans-serif',
        fill="#1f2937",
        align="center",
    )
    right_badge_bg = RectSlot(
        id="slot.diagram.right_badge_bg",
        prompt="",
        x=762,
        y=114,
        width=88,
        height=38,
        fill="#fef3c7",
        stroke="#f59e0b",
        stroke_width=1.5,
        rx=16,
        ry=16,
    )
    right_badge_text = TextSlot(
        id="slot.diagram.right_badge_text",
        prompt="",
        text="큰 수",
        x=806,
        y=121,
        font_size=18,
        font_family='"Noto Sans KR", sans-serif',
        fill="#1f2937",
        align="center",
    )

    # 수직선 본선 (x=136..750, y=133)
    axis_line = LineSlot(
        id="slot.diagram.axis_line",
        prompt="",
        x1=136,
        y1=133,
        x2=750,
        y2=133,
        stroke="#111827",
        stroke_width=2,
    )

    # 10개 눈금 (28100 ~ 29000, 간격 60px: x=173 + i*60)
    ticks = []
    for i in range(10):
        tx = 173 + i * 60
        ticks.append(
            LineSlot(
                id=f"slot.diagram.tick_{i}",
                prompt="",
                x1=tx,
                y1=125,
                x2=tx,
                y2=141,
                stroke="#111827",
                stroke_width=1.5,
            )
        )

    label_28100 = TextSlot(id="slot.diagram.label_28100", prompt="", text="28100", x=173, y=148, font_size=18, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center")
    label_28500 = TextSlot(id="slot.diagram.label_28500", prompt="", text="28500", x=413, y=148, font_size=18, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center")
    label_29000 = TextSlot(id="slot.diagram.label_29000", prompt="", text="29000", x=713, y=148, font_size=18, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center")

    dot_28300 = CircleSlot(id="slot.diagram.dot_28300", prompt="", cx=293, cy=133, r=5, fill="#ec4899", stroke="#ec4899", stroke_width=1)
    dot_28600 = CircleSlot(id="slot.diagram.dot_28600", prompt="", cx=473, cy=133, r=5, fill="#ec4899", stroke="#ec4899", stroke_width=1)

    top_28300 = TextSlot(id="slot.diagram.top_28300", prompt="", text="28300", x=293, y=96, font_size=18, font_family='"Noto Sans KR", sans-serif', fill="#ec4899", align="center")
    top_28600 = TextSlot(id="slot.diagram.top_28600", prompt="", text="28600", x=473, y=96, font_size=18, font_family='"Noto Sans KR", sans-serif', fill="#ec4899", align="center")

    # 설명 문장 및 선택 영역
    desc_text = TextBoxSlot(
        id="slot.diagram.desc_text",
        prompt="",
        text="수직선에서 오른쪽에 위치한 수가 왼쪽에 위치한 수보다 더 큰 수이므로",
        x=60,
        y=200,
        width=766,
        height=36,
        font_size=21,
        font_family='"Noto Sans KR", sans-serif',
        fill="#111827",
        align="center",
        valign="middle",
    )

    paren_left = TextSlot(id="slot.choice.paren_left", prompt="", text="(", x=265, y=252, font_size=24, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center")
    choice_0 = TextSlot(
        id="slot.choice.option_0",
        prompt="",
        text="28300",
        x=320,
        y=252,
        font_size=22,
        font_family='"Noto Sans KR", sans-serif',
        fill="#111827",
        align="center",
        interaction={
            "type": "choice",
            "role": "answer",
            "choice_index": 0,
            "value": "28300",
            "group_id": "slot.choice.group",
            "include_in_submission": True,
        },
    )
    comma = TextSlot(id="slot.choice.comma", prompt="", text=",", x=375, y=252, font_size=22, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center")
    choice_1 = TextSlot(
        id="slot.choice.option_1",
        prompt="",
        text="28600",
        x=430,
        y=252,
        font_size=22,
        font_family='"Noto Sans KR", sans-serif',
        fill="#111827",
        align="center",
        interaction={
            "type": "choice",
            "role": "answer",
            "choice_index": 1,
            "value": "28600",
            "group_id": "slot.choice.group",
            "include_in_submission": True,
        },
    )
    paren_right = TextSlot(id="slot.choice.paren_right", prompt="", text=")이 더 큰 수입니다.", x=575, y=252, font_size=22, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center")

    diagram_slot_ids = (
        "slot.diagram.left_badge_bg",
        "slot.diagram.left_badge_text",
        "slot.diagram.right_badge_bg",
        "slot.diagram.right_badge_text",
        "slot.diagram.axis_line",
        *(f"slot.diagram.tick_{i}" for i in range(10)),
        "slot.diagram.label_28100",
        "slot.diagram.label_28500",
        "slot.diagram.label_29000",
        "slot.diagram.dot_28300",
        "slot.diagram.dot_28600",
        "slot.diagram.top_28300",
        "slot.diagram.top_28600",
        "slot.diagram.desc_text",
    )

    return ProblemTemplate(
        id=PROBLEM_ID,
        title=PROBLEM_TITLE,
        canvas=Canvas(
            width=886,
            height=320,
            coordinate_mode="logical",
        ),
        regions=(
            Region(id="region.stem", role="stem", flow="absolute", slot_ids=("slot.stem.question",)),
            Region(id="region.diagram", role="diagram", flow="absolute", slot_ids=diagram_slot_ids),
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
            left_badge_bg,
            left_badge_text,
            right_badge_bg,
            right_badge_text,
            axis_line,
            *ticks,
            label_28100,
            label_28500,
            label_29000,
            dot_28300,
            dot_28600,
            top_28300,
            top_28600,
            desc_text,
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
        {"ref": "num_left", "value": 28300},
        {"ref": "num_right", "value": 28600},
    ],
    "target": {"ref": "slot.choice.option_1", "label": "더 큰 수", "unit": ""},
    "method": "number_line_comparison",
    "steps": [
        {
            "id": "compare_on_number_line",
            "expr": "28600 > 28300",
            "explanation": "수직선에서 오른쪽에 위치한 28600이 더 큰 수입니다.",
            "value": "28600",
        },
    ],
    "answer": ANSWER,
}


if __name__ == "__main__":
    print(f"[{PROBLEM_TEMPLATE.id}] 템플릿 컴파일 성공!")
    print(f"- 제목: {PROBLEM_TEMPLATE.title}")
    print(f"- 캔버스: {PROBLEM_TEMPLATE.canvas.width} x {PROBLEM_TEMPLATE.canvas.height}")
    print(f"- 구역 수: {len(PROBLEM_TEMPLATE.regions)}")
