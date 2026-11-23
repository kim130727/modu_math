"""ModuMath Problem DSL: 몫이 더 큰 나눗셈 선택하기 (S3_초등_4_008111)"""

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
PROBLEM_ID = "S3_초등_4_008111"
PROBLEM_TITLE = "두 나눗셈 중 몫이 더 큰 식 선택하기"


# ==============================================================================
# 2. 정답 및 오답 진단 정의 (Answer & Diagnostic Key)
# ==============================================================================
ANSWER = {
    "value": "360 ÷ 40",
    "answer_index": 0,
    "unit": "",
    "values": ["360 ÷ 40"],
    "choices": [
        "360 ÷ 40",
        "420 ÷ 60",
    ],
    "blanks": [],
    "answer_key": [
        {
            "slot_id": "slot.choice.option_0",
            "value": "360 ÷ 40",
            "diagnostics": [
                {
                    "id": "diag.chose_larger_dividend",
                    "condition": "answer_equals_420_60",
                    "concept": "몇백몇십 ÷ 몇십",
                    "reason": "나누어지는 수(420)가 더 큰 식의 몫이 더 클 것이라고 오인함",
                    "feedback": "360 ÷ 40 = 9이고, 420 ÷ 60 = 7입니다. 9 > 7이므로 360 ÷ 40의 몫이 더 큽니다.",
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
    "problem_type": "multiple_choice_quotient_comparison",
    "metadata": {
        "school": "초등학교",
        "grade": 4,
        "semester": "1학기",
        "chapter": "03단원_곱셈과 나눗셈",
        "difficulty": "하",
    },
    "entities": {
        "expr_0": {"label": "360 ÷ 40", "quotient": 9},
        "expr_1": {"label": "420 ÷ 60", "quotient": 7},
    },
    "relations": [
        {
            "type": "greater_quotient",
            "larger": "expr_0",
            "smaller": "expr_1",
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
        text="19. 몫이 더 큰 것을 선택하세요.",
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

    card_0 = RectSlot(id="slot.diagram.card_0", prompt="", x=180, y=96, width=230, height=72, fill="#d8dcf0", stroke="#b8bfe3", stroke_width=1.2, rx=4, ry=4)
    choice_0 = TextSlot(
        id="slot.choice.option_0",
        prompt="",
        text="360 ÷ 40",
        x=295,
        y=118,
        font_size=24,
        font_family='"Noto Sans KR", sans-serif',
        fill="#111827",
        align="center",
        interaction={"type": "choice", "role": "answer", "choice_index": 0, "value": "360 ÷ 40", "group_id": "slot.choice.group", "include_in_submission": True},
    )

    card_1 = RectSlot(id="slot.diagram.card_1", prompt="", x=476, y=96, width=230, height=72, fill="#d8dcf0", stroke="#b8bfe3", stroke_width=1.2, rx=4, ry=4)
    choice_1 = TextSlot(
        id="slot.choice.option_1",
        prompt="",
        text="420 ÷ 60",
        x=591,
        y=118,
        font_size=24,
        font_family='"Noto Sans KR", sans-serif',
        fill="#111827",
        align="center",
        interaction={"type": "choice", "role": "answer", "choice_index": 1, "value": "420 ÷ 60", "group_id": "slot.choice.group", "include_in_submission": True},
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
        {"ref": "expr_0", "value": "360 ÷ 40"},
        {"ref": "expr_1", "value": "420 ÷ 60"},
    ],
    "target": {"ref": "slot.choice.option_0", "label": "몫이 더 큰 나눗셈", "unit": ""},
    "method": "division_and_comparison",
    "steps": [
        {
            "id": "compare_quotients",
            "expr": "360 / 40 = 9 > 420 / 60 = 7",
            "explanation": "360 ÷ 40 = 9이고 420 ÷ 60 = 7이므로 360 ÷ 40의 몫이 더 큽니다.",
            "value": "360 ÷ 40",
        },
    ],
    "answer": ANSWER,
}


if __name__ == "__main__":
    print(f"[{PROBLEM_TEMPLATE.id}] 템플릿 컴파일 성공!")
    print(f"- 제목: {PROBLEM_TEMPLATE.title}")
    print(f"- 캔버스: {PROBLEM_TEMPLATE.canvas.width} x {PROBLEM_TEMPLATE.canvas.height}")
    print(f"- 구역 수: {len(PROBLEM_TEMPLATE.regions)}")
