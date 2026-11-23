"""ModuMath Problem DSL: 대칭 덧셈식의 규칙 설명 고르기 (S3_초등_4_008499)"""

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
PROBLEM_ID = "S3_초등_4_008499"
PROBLEM_TITLE = "대칭 덧셈식에서 규칙을 바르게 설명한 것 선택하기"


# ==============================================================================
# 2. 정답 및 오답 진단 정의 (Answer & Diagnostic Key)
# ==============================================================================
ANSWER = {
    "value": "계산 결과는 덧셈식의 가운데 수를 두 번 곱한 것과 같아요.",
    "answer_index": 1,
    "unit": "",
    "values": ["계산 결과는 덧셈식의 가운데 수를 두 번 곱한 것과 같아요."],
    "choices": [
        "덧셈식의 가운데 수가 2씩 커져요.",
        "계산 결과는 덧셈식의 가운데 수를 두 번 곱한 것과 같아요.",
    ],
    "blanks": [],
    "answer_key": [
        {
            "slot_id": "slot.choice.option_1",
            "value": "계산 결과는 덧셈식의 가운데 수를 두 번 곱한 것과 같아요.",
            "diagnostics": [
                {
                    "id": "diag.wrong_center_step",
                    "condition": "answer_equals_0",
                    "concept": "계산식의 규칙",
                    "reason": "가운데 수가 1씩 커지는데 2씩 커진다는 잘못된 설명을 선택함",
                    "feedback": "가운데 수는 2, 3, 4, 5로 1씩 커집니다. 계산 결과(4, 9, 16, 25)는 가운데 수를 두 번 곱한 값(2×2, 3×3, 4×4, 5×5)과 같습니다.",
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
    "problem_type": "multiple_choice_equation_pattern",
    "metadata": {
        "school": "초등학교",
        "grade": 4,
        "semester": "1학기",
        "chapter": "06단원_규칙 찾기",
        "difficulty": "중",
    },
    "entities": {
        "eq_0": {"label": "첫째 식", "center": 2, "result": 4},
        "eq_1": {"label": "둘째 식", "center": 3, "result": 9},
        "eq_2": {"label": "셋째 식", "center": 4, "result": 16},
        "eq_3": {"label": "넷째 식", "center": 5, "result": 25},
    },
    "relations": [
        {
            "type": "square_number_pattern",
            "formula": "result = center * center",
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
        text="25. 덧셈식에서 규칙을 찾아 바르게 설명한 것을 선택하세요.",
        x=32,
        y=20,
        width=820,
        height=44,
        font_size=21,
        font_family='"Noto Sans KR", sans-serif',
        fill="#202124",
        align="left",
        valign="top",
        line_height=1.45,
    )

    eq_box = RectSlot(id="slot.diagram.eq_box", prompt="", x=206, y=76, width=474, height=138, fill="#ffffff", stroke="#f87171", stroke_width=1.6)
    eqs = [
        "1 + 2 + 1 = 4",
        "1 + 2 + 3 + 2 + 1 = 9",
        "1 + 2 + 3 + 4 + 3 + 2 + 1 = 16",
        "1 + 2 + 3 + 4 + 5 + 4 + 3 + 2 + 1 = 25",
    ]
    eq_slots = [
        TextSlot(id=f"slot.diagram.eq_{i}", prompt="", text=eq, x=443, y=88 + i * 30, font_size=21, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center")
        for i, eq in enumerate(eqs)
    ]

    card_0 = RectSlot(id="slot.diagram.card_0", prompt="", x=116, y=228, width=654, height=44, fill="#fce7f3", stroke="#f472b6", stroke_width=1.2)
    c0 = TextSlot(
        id="slot.choice.option_0",
        prompt="",
        text="덧셈식의 가운데 수가 2씩 커져요.",
        x=443,
        y=238,
        font_size=19,
        font_family='"Noto Sans KR", sans-serif',
        fill="#111827",
        align="center",
        interaction={"type": "choice", "role": "answer", "choice_index": 0, "value": "덧셈식의 가운데 수가 2씩 커져요.", "group_id": "slot.choice.group", "include_in_submission": True},
    )

    card_1 = RectSlot(id="slot.diagram.card_1", prompt="", x=116, y=284, width=654, height=44, fill="#fce7f3", stroke="#f472b6", stroke_width=1.2)
    c1 = TextSlot(
        id="slot.choice.option_1",
        prompt="",
        text="계산 결과는 덧셈식의 가운데 수를 두 번 곱한 것과 같아요.",
        x=443,
        y=294,
        font_size=19,
        font_family='"Noto Sans KR", sans-serif',
        fill="#111827",
        align="center",
        interaction={"type": "choice", "role": "answer", "choice_index": 1, "value": "계산 결과는 덧셈식의 가운데 수를 두 번 곱한 것과 같아요.", "group_id": "slot.choice.group", "include_in_submission": True},
    )

    return ProblemTemplate(
        id=PROBLEM_ID,
        title=PROBLEM_TITLE,
        canvas=Canvas(
            width=886,
            height=352,
            coordinate_mode="logical",
        ),
        regions=(
            Region(id="region.stem", role="stem", flow="absolute", slot_ids=("slot.stem.question",)),
            Region(id="region.diagram", role="diagram", flow="absolute", slot_ids=("slot.diagram.eq_box", *(s.id for s in eq_slots), "slot.diagram.card_0", "slot.diagram.card_1")),
            Region(id="region.choices", role="choices", flow="absolute", slot_ids=("slot.choice.option_0", "slot.choice.option_1")),
        ),
        slots=(
            stem_text_slot,
            eq_box,
            *eq_slots,
            card_0,
            c0,
            card_1,
            c1,
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
        {"ref": "eq_0", "value": 4},
        {"ref": "eq_1", "value": 9},
        {"ref": "eq_2", "value": 16},
        {"ref": "eq_3", "value": 25},
    ],
    "target": {"ref": "slot.choice.option_1", "label": "바른 설명", "unit": ""},
    "method": "equation_pattern_analysis",
    "steps": [
        {
            "id": "verify_square_pattern",
            "expr": "4=2*2, 9=3*3, 16=4*4, 25=5*5",
            "explanation": "계산 결과는 덧셈식의 가운데 수를 두 번 곱한 것과 같습니다.",
            "value": "계산 결과는 덧셈식의 가운데 수를 두 번 곱한 것과 같아요.",
        },
    ],
    "answer": ANSWER,
}


if __name__ == "__main__":
    print(f"[{PROBLEM_TEMPLATE.id}] 템플릿 컴파일 성공!")
    print(f"- 제목: {PROBLEM_TEMPLATE.title}")
    print(f"- 캔버스: {PROBLEM_TEMPLATE.canvas.width} x {PROBLEM_TEMPLATE.canvas.height}")
    print(f"- 구역 수: {len(PROBLEM_TEMPLATE.regions)}")
