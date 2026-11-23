"""ModuMath Problem DSL: 계산 결과가 다른 곱셈식 찾기 (S3_초등_4_008110)"""

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
PROBLEM_ID = "S3_초등_4_008110"
PROBLEM_TITLE = "계산 결과가 다른 곱셈식 선택하기"


# ==============================================================================
# 2. 정답 및 오답 진단 정의 (Answer & Diagnostic Key)
# ==============================================================================
ANSWER = {
    "value": "200 × 90",
    "answer_index": 0,
    "unit": "",
    "values": ["200 × 90"],
    "choices": [
        "200 × 90",
        "30 × 800",
        "400 × 60",
    ],
    "blanks": [],
    "answer_key": [
        {
            "slot_id": "slot.choice.option_0",
            "value": "200 × 90",
            "diagnostics": [
                {
                    "id": "diag.chose_24000_a",
                    "condition": "answer_equals_30_800",
                    "concept": "몇백 × 몇십의 계산",
                    "reason": "30 × 800 = 24000으로 400 × 60과 결과가 같음",
                    "feedback": "30 × 800 = 24000이고 400 × 60 = 24000입니다. 200 × 90 = 18000으로 결과가 다릅니다.",
                },
                {
                    "id": "diag.chose_24000_b",
                    "condition": "answer_equals_400_60",
                    "concept": "몇백 × 몇십의 계산",
                    "reason": "400 × 60 = 24000으로 30 × 800과 결과가 같음",
                    "feedback": "400 × 60 = 24000이고 30 × 800 = 24000입니다. 200 × 90 = 18000으로 결과가 다릅니다.",
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
    "problem_type": "multiple_choice_expression_comparison",
    "metadata": {
        "school": "초등학교",
        "grade": 4,
        "semester": "1학기",
        "chapter": "03단원_곱셈과 나눗셈",
        "difficulty": "하",
    },
    "entities": {
        "expr_0": {"label": "200 × 90", "value": 18000},
        "expr_1": {"label": "30 × 800", "value": 24000},
        "expr_2": {"label": "400 × 60", "value": 24000},
    },
    "relations": [
        {
            "type": "odd_one_out",
            "correct_entity": "expr_0",
            "same_value_entities": ["expr_1", "expr_2"],
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
        text="18. 계산 결과가 다른 것을 선택하세요.",
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

    exprs = ["200 × 90", "30 × 800", "400 × 60"]
    cards = []
    choices = []
    for idx, expr in enumerate(exprs):
        bx = 64 + idx * 268
        cards.append(
            RectSlot(
                id=f"slot.diagram.card_{idx}",
                prompt="",
                x=bx,
                y=96,
                width=222,
                height=74,
                fill="#e2ebd6",
                stroke="#9ab778",
                stroke_width=1.5,
                rx=4,
                ry=4,
            )
        )
        choices.append(
            TextSlot(
                id=f"slot.choice.option_{idx}",
                prompt="",
                text=expr,
                x=bx + 111,
                y=120,
                font_size=24,
                font_family='"Noto Sans KR", sans-serif',
                fill="#111827",
                align="center",
                interaction={"type": "choice", "role": "answer", "choice_index": idx, "value": expr, "group_id": "slot.choice.group", "include_in_submission": True},
            )
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
            Region(id="region.diagram", role="diagram", flow="absolute", slot_ids=tuple(c.id for c in cards)),
            Region(id="region.choices", role="choices", flow="absolute", slot_ids=tuple(c.id for c in choices)),
        ),
        slots=(
            stem_text_slot,
            *cards,
            *choices,
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
        {"ref": "expr_0", "value": "200 × 90"},
        {"ref": "expr_1", "value": "30 × 800"},
        {"ref": "expr_2", "value": "400 × 60"},
    ],
    "target": {"ref": "slot.choice.option_0", "label": "계산 결과가 다른 식", "unit": ""},
    "method": "compute_and_compare",
    "steps": [
        {
            "id": "evaluate_all",
            "expr": "200*90=18000, 30*800=24000, 400*60=24000",
            "explanation": "30 × 800과 400 × 60은 모두 24000이지만, 200 × 90은 18000입니다.",
            "value": "200 × 90",
        },
    ],
    "answer": ANSWER,
}


if __name__ == "__main__":
    print(f"[{PROBLEM_TEMPLATE.id}] 템플릿 컴파일 성공!")
    print(f"- 제목: {PROBLEM_TEMPLATE.title}")
    print(f"- 캔버스: {PROBLEM_TEMPLATE.canvas.width} x {PROBLEM_TEMPLATE.canvas.height}")
    print(f"- 구역 수: {len(PROBLEM_TEMPLATE.regions)}")
