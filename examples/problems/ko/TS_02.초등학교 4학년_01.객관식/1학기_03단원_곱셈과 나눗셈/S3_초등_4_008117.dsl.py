"""ModuMath Problem DSL: 어림셈으로 곱의 크기 비교하기 (S3_초등_4_008117)"""

from __future__ import annotations

from modu_math.dsl import (
    Canvas,
    CircleSlot,
    ProblemTemplate,
    RectSlot,
    Region,
    TextBoxSlot,
    TextSlot,
)


# ==============================================================================
# 1. 문제 식별자 및 제목 (Problem Metadata)
# ==============================================================================
PROBLEM_ID = "S3_초등_4_008117"
PROBLEM_TITLE = "186 × 40의 어림셈 결과 비교하기"


# ==============================================================================
# 2. 정답 및 오답 진단 정의 (Answer & Diagnostic Key)
# ==============================================================================
ANSWER = {
    "value": "작을 거야",
    "answer_index": 1,
    "unit": "",
    "values": ["작을 거야"],
    "choices": [
        "클 거야",
        "작을 거야",
    ],
    "blanks": [],
    "answer_key": [
        {
            "slot_id": "slot.choice.option_1",
            "value": "작을 거야",
            "diagnostics": [
                {
                    "id": "diag.confused_direction",
                    "condition": "answer_equals_larger",
                    "concept": "곱셈의 어림",
                    "reason": "186을 200으로 올려 어림했음에도 원래 곱이 더 클 것이라고 오인함",
                    "feedback": "186은 200보다 작은 수이므로 186 × 40은 200 × 40 = 8000보다 작을 것입니다.",
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
    "problem_type": "multiple_choice_multiplication_estimation",
    "metadata": {
        "school": "초등학교",
        "grade": 4,
        "semester": "1학기",
        "chapter": "03단원_곱셈과 나눗셈",
        "difficulty": "하",
    },
    "entities": {
        "exact_expr": {"label": "원래 식", "value": "186 × 40"},
        "estimated_expr": {"label": "어림한 식", "value": "200 × 40", "result": 8000},
    },
    "relations": [
        {
            "type": "less_than",
            "expression": "186 * 40 < 200 * 40",
            "smaller": "exact_expr",
            "larger": "estimated_expr",
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
        text="25. 186 × 40을 어림하려고 합니다. 알맞은 말을 선택하세요.",
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

    boy_head = CircleSlot(id="slot.diagram.boy_head", prompt="", cx=336, cy=148, r=32, fill="#fde68a", stroke="#78350f", stroke_width=1.5)
    boy_hair = CircleSlot(id="slot.diagram.boy_hair", prompt="", cx=336, cy=128, r=28, fill="#451a03", stroke="#451a03", stroke_width=1)
    bubble = RectSlot(id="slot.diagram.bubble", prompt="", x=402, y=88, width=360, height=136, fill="#ffffff", stroke="#374151", stroke_width=1.5, rx=28, ry=28)

    line1 = TextSlot(id="slot.diagram.line1", prompt="", text="200 × 40 = 8000이므로", x=582, y=106, font_size=21, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center")
    line2 = TextSlot(id="slot.diagram.line2", prompt="", text="186 × 40은 8000보다", x=582, y=140, font_size=21, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center")

    paren_left = TextSlot(id="slot.choice.paren_left", prompt="", text="(", x=446, y=176, font_size=22, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center")
    choice_0 = TextSlot(
        id="slot.choice.option_0",
        prompt="",
        text="클 거야",
        x=502,
        y=176,
        font_size=21,
        font_family='"Noto Sans KR", sans-serif',
        fill="#111827",
        align="center",
        interaction={"type": "choice", "role": "answer", "choice_index": 0, "value": "클 거야", "group_id": "slot.choice.group", "include_in_submission": True},
    )
    comma = TextSlot(id="slot.choice.comma", prompt="", text=",", x=556, y=176, font_size=21, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center")
    choice_1 = TextSlot(
        id="slot.choice.option_1",
        prompt="",
        text="작을 거야",
        x=622,
        y=176,
        font_size=21,
        font_family='"Noto Sans KR", sans-serif',
        fill="#111827",
        align="center",
        interaction={"type": "choice", "role": "answer", "choice_index": 1, "value": "작을 거야", "group_id": "slot.choice.group", "include_in_submission": True},
    )
    paren_right = TextSlot(id="slot.choice.paren_right", prompt="", text=").", x=690, y=176, font_size=22, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center")

    return ProblemTemplate(
        id=PROBLEM_ID,
        title=PROBLEM_TITLE,
        canvas=Canvas(
            width=886,
            height=260,
            coordinate_mode="logical",
        ),
        regions=(
            Region(id="region.stem", role="stem", flow="absolute", slot_ids=("slot.stem.question",)),
            Region(
                id="region.diagram",
                role="diagram",
                flow="absolute",
                slot_ids=(
                    "slot.diagram.boy_hair",
                    "slot.diagram.boy_head",
                    "slot.diagram.bubble",
                    "slot.diagram.line1",
                    "slot.diagram.line2",
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
            boy_hair,
            boy_head,
            bubble,
            line1,
            line2,
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
        {"ref": "exact_expr", "value": "186 × 40"},
        {"ref": "estimated_expr", "value": "200 × 40 = 8000"},
    ],
    "target": {"ref": "slot.choice.option_1", "label": "어림셈 비교 결과", "unit": ""},
    "method": "estimation_bound_comparison",
    "steps": [
        {
            "id": "compare_with_estimate",
            "expr": "186 < 200 => 186 * 40 < 200 * 40 = 8000",
            "explanation": "186은 200보다 작으므로 186 × 40은 8000보다 작습니다.",
            "value": "작을 거야",
        },
    ],
    "answer": ANSWER,
}


if __name__ == "__main__":
    print(f"[{PROBLEM_TEMPLATE.id}] 템플릿 컴파일 성공!")
    print(f"- 제목: {PROBLEM_TEMPLATE.title}")
    print(f"- 캔버스: {PROBLEM_TEMPLATE.canvas.width} x {PROBLEM_TEMPLATE.canvas.height}")
    print(f"- 구역 수: {len(PROBLEM_TEMPLATE.regions)}")
