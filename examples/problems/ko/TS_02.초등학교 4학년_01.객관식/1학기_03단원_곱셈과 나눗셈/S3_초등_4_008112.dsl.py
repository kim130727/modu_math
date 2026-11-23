"""ModuMath Problem DSL: 어림한 나눗셈의 몫 찾기 (S3_초등_4_008112)"""

from __future__ import annotations

from modu_math.dsl import (
    Canvas,
    ProblemTemplate,
    RectSlot,
    Region,
    TextBoxSlot,
    TextSlot,
)


# ==============================================================================
# 1. 문제 식별자 및 제목 (Problem Metadata)
# ==============================================================================
PROBLEM_ID = "S3_초등_4_008112"
PROBLEM_TITLE = "91 ÷ 28의 어림한 몫 선택하기"


# ==============================================================================
# 2. 정답 및 오답 진단 정의 (Answer & Diagnostic Key)
# ==============================================================================
ANSWER = {
    "value": "3",
    "answer_index": 1,
    "unit": "",
    "values": ["3"],
    "choices": [
        "2",
        "3",
        "20",
        "30",
    ],
    "blanks": [],
    "answer_key": [
        {
            "slot_id": "slot.choice.option_1",
            "value": "3",
            "diagnostics": [
                {
                    "id": "diag.underestimate_2",
                    "condition": "answer_equals_2",
                    "concept": "나눗셈의 어림",
                    "reason": "28을 30으로 어림하지 않고 몫을 너무 작게 잡음",
                    "feedback": "28을 30으로 생각하면 30 × 3 = 90이므로 91 ÷ 28의 몫은 3 정도라고 어림할 수 있습니다.",
                },
                {
                    "id": "diag.wrong_place_30",
                    "condition": "answer_equals_30",
                    "concept": "나눗셈의 어림",
                    "reason": "몫의 자릿수를 십의 자리로 잘못 어림함",
                    "feedback": "30 × 30 = 900이므로 91 ÷ 28의 몫은 30이 아니라 한 자리 수인 3입니다.",
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
    "problem_type": "multiple_choice_division_estimation",
    "metadata": {
        "school": "초등학교",
        "grade": 4,
        "semester": "1학기",
        "chapter": "03단원_곱셈과 나눗셈",
        "difficulty": "하",
    },
    "entities": {
        "dividend": {"label": "나누어지는 수", "value": 91},
        "divisor": {"label": "나누는 수", "value": 28},
        "estimated_quotient": {"label": "어림한 몫", "value": 3},
    },
    "relations": [
        {
            "type": "estimation",
            "expression": "91 / 28 ≈ 90 / 30 = 3",
            "target": "estimated_quotient",
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
        text="20. 어림한 나눗셈의 몫으로 가장 적절한 것을 선택하세요.",
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

    expr_card = RectSlot(id="slot.diagram.expr_card", prompt="", x=176, y=96, width=220, height=70, fill="#e8e4f3", stroke="#d8d0ec", stroke_width=1.2, rx=4, ry=4)
    expr_text = TextSlot(id="slot.diagram.expr_text", prompt="", text="91 ÷ 28", x=286, y=118, font_size=24, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center")

    paren_left = TextSlot(id="slot.choice.paren_left", prompt="", text="(", x=470, y=118, font_size=26, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center")
    choice_0 = TextSlot(
        id="slot.choice.option_0",
        prompt="",
        text="2",
        x=502,
        y=118,
        font_size=24,
        font_family='"Noto Sans KR", sans-serif',
        fill="#111827",
        align="center",
        interaction={"type": "choice", "role": "answer", "choice_index": 0, "value": "2", "group_id": "slot.choice.group", "include_in_submission": True},
    )
    c0 = TextSlot(id="slot.choice.c0", prompt="", text=",", x=528, y=118, font_size=24, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center")
    choice_1 = TextSlot(
        id="slot.choice.option_1",
        prompt="",
        text="3",
        x=554,
        y=118,
        font_size=24,
        font_family='"Noto Sans KR", sans-serif',
        fill="#111827",
        align="center",
        interaction={"type": "choice", "role": "answer", "choice_index": 1, "value": "3", "group_id": "slot.choice.group", "include_in_submission": True},
    )
    c1 = TextSlot(id="slot.choice.c1", prompt="", text=",", x=580, y=118, font_size=24, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center")
    choice_2 = TextSlot(
        id="slot.choice.option_2",
        prompt="",
        text="20",
        x=612,
        y=118,
        font_size=24,
        font_family='"Noto Sans KR", sans-serif',
        fill="#111827",
        align="center",
        interaction={"type": "choice", "role": "answer", "choice_index": 2, "value": "20", "group_id": "slot.choice.group", "include_in_submission": True},
    )
    c2 = TextSlot(id="slot.choice.c2", prompt="", text=",", x=644, y=118, font_size=24, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center")
    choice_3 = TextSlot(
        id="slot.choice.option_3",
        prompt="",
        text="30",
        x=676,
        y=118,
        font_size=24,
        font_family='"Noto Sans KR", sans-serif',
        fill="#111827",
        align="center",
        interaction={"type": "choice", "role": "answer", "choice_index": 3, "value": "30", "group_id": "slot.choice.group", "include_in_submission": True},
    )
    paren_right = TextSlot(id="slot.choice.paren_right", prompt="", text=")", x=708, y=118, font_size=26, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center")

    return ProblemTemplate(
        id=PROBLEM_ID,
        title=PROBLEM_TITLE,
        canvas=Canvas(
            width=886,
            height=220,
            coordinate_mode="logical",
        ),
        regions=(
            Region(id="region.stem", role="stem", flow="absolute", slot_ids=("slot.stem.question",)),
            Region(id="region.diagram", role="diagram", flow="absolute", slot_ids=("slot.diagram.expr_card", "slot.diagram.expr_text")),
            Region(
                id="region.choices",
                role="choices",
                flow="absolute",
                slot_ids=(
                    "slot.choice.paren_left",
                    "slot.choice.option_0",
                    "slot.choice.c0",
                    "slot.choice.option_1",
                    "slot.choice.c1",
                    "slot.choice.option_2",
                    "slot.choice.c2",
                    "slot.choice.option_3",
                    "slot.choice.paren_right",
                ),
            ),
        ),
        slots=(
            stem_text_slot,
            expr_card,
            expr_text,
            paren_left,
            choice_0,
            c0,
            choice_1,
            c1,
            choice_2,
            c2,
            choice_3,
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
        {"ref": "dividend", "value": 91},
        {"ref": "divisor", "value": 28},
    ],
    "target": {"ref": "slot.choice.option_1", "label": "어림한 몫", "unit": ""},
    "method": "rounding_estimation",
    "steps": [
        {
            "id": "estimate_quotient",
            "expr": "90 / 30 = 3",
            "explanation": "28을 30으로 생각하면 30 × 3 = 90이므로 91 ÷ 28의 몫은 3 정도입니다.",
            "value": "3",
        },
    ],
    "answer": ANSWER,
}


if __name__ == "__main__":
    print(f"[{PROBLEM_TEMPLATE.id}] 템플릿 컴파일 성공!")
    print(f"- 제목: {PROBLEM_TEMPLATE.title}")
    print(f"- 캔버스: {PROBLEM_TEMPLATE.canvas.width} x {PROBLEM_TEMPLATE.canvas.height}")
    print(f"- 구역 수: {len(PROBLEM_TEMPLATE.regions)}")
