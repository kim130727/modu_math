"""ModuMath Problem DSL: 몫이 두 자리 수인 나눗셈 선택하기 (S3_초등_4_008113)"""

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
PROBLEM_ID = "S3_초등_4_008113"
PROBLEM_TITLE = "몫이 두 자리 수인 나눗셈 선택하기"


# ==============================================================================
# 2. 정답 및 오답 진단 정의 (Answer & Diagnostic Key)
# ==============================================================================
ANSWER = {
    "value": "275 ÷ 25",
    "answer_index": 0,
    "unit": "",
    "values": ["275 ÷ 25"],
    "choices": [
        "275 ÷ 25",
        "495 ÷ 54",
    ],
    "blanks": [],
    "answer_key": [
        {
            "slot_id": "slot.choice.option_0",
            "value": "275 ÷ 25",
            "diagnostics": [
                {
                    "id": "diag.chose_one_digit_quotient",
                    "condition": "answer_equals_495_54",
                    "concept": "세 자리 수 ÷ 두 자리 수",
                    "reason": "나누어지는 수의 앞 두 자리(49)가 나누는 수(54)보다 작아 몫이 한 자리 수인 식을 선택함",
                    "feedback": "54 × 10 = 540이고 495 < 540이므로 495 ÷ 54의 몫은 한 자리 수입니다. 275 > 250이므로 275 ÷ 25의 몫이 두 자리 수입니다.",
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
    "problem_type": "multiple_choice_quotient_digit_count",
    "metadata": {
        "school": "초등학교",
        "grade": 4,
        "semester": "1학기",
        "chapter": "03단원_곱셈과 나눗셈",
        "difficulty": "중",
    },
    "entities": {
        "expr_0": {"label": "275 ÷ 25", "quotient": 11, "digits": 2},
        "expr_1": {"label": "495 ÷ 54", "quotient": 9, "digits": 1},
    },
    "relations": [
        {
            "type": "quotient_digit_count_match",
            "target_digits": 2,
            "correct_entity": "expr_0",
            "distractor": "expr_1",
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
        text="21. 몫이 두 자리 수인 나눗셈을 선택하세요.",
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

    card_0 = RectSlot(id="slot.diagram.card_0", prompt="", x=180, y=96, width=230, height=72, fill="#fde8e1", stroke="#f7cfc2", stroke_width=1.2, rx=4, ry=4)
    choice_0 = TextSlot(
        id="slot.choice.option_0",
        prompt="",
        text="275 ÷ 25",
        x=295,
        y=118,
        font_size=24,
        font_family='"Noto Sans KR", sans-serif',
        fill="#111827",
        align="center",
        interaction={"type": "choice", "role": "answer", "choice_index": 0, "value": "275 ÷ 25", "group_id": "slot.choice.group", "include_in_submission": True},
    )

    card_1 = RectSlot(id="slot.diagram.card_1", prompt="", x=476, y=96, width=230, height=72, fill="#fde8e1", stroke="#f7cfc2", stroke_width=1.2, rx=4, ry=4)
    choice_1 = TextSlot(
        id="slot.choice.option_1",
        prompt="",
        text="495 ÷ 54",
        x=591,
        y=118,
        font_size=24,
        font_family='"Noto Sans KR", sans-serif',
        fill="#111827",
        align="center",
        interaction={"type": "choice", "role": "answer", "choice_index": 1, "value": "495 ÷ 54", "group_id": "slot.choice.group", "include_in_submission": True},
    )

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
            Region(id="region.diagram", role="diagram", flow="absolute", slot_ids=("slot.diagram.card_0", "slot.diagram.card_1")),
            Region(id="region.choices", role="choices", flow="absolute", slot_ids=("slot.choice.option_0", "slot.choice.option_1")),
        ),
        slots=(
            stem_text_slot,
            card_0,
            choice_0,
            card_1,
            choice_1,
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
        {"ref": "expr_0", "value": "275 ÷ 25"},
        {"ref": "expr_1", "value": "495 ÷ 54"},
    ],
    "target": {"ref": "slot.choice.option_0", "label": "몫이 두 자리 수인 나눗셈", "unit": ""},
    "method": "leading_digits_comparison",
    "steps": [
        {
            "id": "compare_tens",
            "expr": "27 > 25 (몫: 두 자리 수), 49 < 54 (몫: 한 자리 수)",
            "explanation": "275 ÷ 25는 25 × 10 = 250보다 크므로 몫이 두 자리 수입니다.",
            "value": "275 ÷ 25",
        },
    ],
    "answer": ANSWER,
}


if __name__ == "__main__":
    print(f"[{PROBLEM_TEMPLATE.id}] 템플릿 컴파일 성공!")
    print(f"- 제목: {PROBLEM_TEMPLATE.title}")
    print(f"- 캔버스: {PROBLEM_TEMPLATE.canvas.width} x {PROBLEM_TEMPLATE.canvas.height}")
    print(f"- 구역 수: {len(PROBLEM_TEMPLATE.regions)}")
