"""ModuMath Problem DSL: 세 자리 수와 두 자리 수의 곱셈 자릿값 (S3_초등_4_008108)"""

from __future__ import annotations

from modu_math.dsl import (
    Canvas,
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
PROBLEM_ID = "S3_초등_4_008108"
PROBLEM_TITLE = "700 × 40의 세로셈에서 숫자 8의 자리 찾기"


# ==============================================================================
# 2. 정답 및 오답 진단 정의 (Answer & Diagnostic Key)
# ==============================================================================
ANSWER = {
    "value": "㉡",
    "answer_index": 1,
    "unit": "",
    "values": ["㉡"],
    "choices": [
        "㉠",
        "㉡",
        "㉢",
        "㉣",
        "㉤",
    ],
    "blanks": [],
    "answer_key": [
        {
            "slot_id": "slot.choice.option_1",
            "value": "㉡",
            "diagnostics": [
                {
                    "id": "diag.wrong_place_20000",
                    "condition": "answer_equals_giyeok",
                    "concept": "몇백 × 몇십의 계산",
                    "reason": "만의 자리(2)를 천의 자리(8)와 혼동함",
                    "feedback": "700 × 40 = 28000이므로 ㉠ 자리에는 2, ㉡ 자리에는 8이 들어갑니다.",
                },
                {
                    "id": "diag.wrong_place_hundreds",
                    "condition": "answer_equals_digeut",
                    "concept": "몇백 × 몇십의 계산",
                    "reason": "7 × 40을 계산한 자리로 오인하여 0의 개수를 하나 적게 셈",
                    "feedback": "700 × 40은 7 × 4 = 28에 0이 3개 붙어 28000이 됩니다. 따라서 8은 천의 자리인 ㉡에 써야 합니다.",
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
    "problem_type": "multiple_choice_multiplication_place_value",
    "metadata": {
        "school": "초등학교",
        "grade": 4,
        "semester": "1학기",
        "chapter": "03단원_곱셈과 나눗셈",
        "difficulty": "중",
    },
    "entities": {
        "multiplicand": {"label": "피승수", "value": 700},
        "multiplier": {"label": "승수", "value": 40},
        "product": {"label": "곱", "value": 28000},
    },
    "relations": [
        {
            "type": "multiplication",
            "expression": "700 * 40 = 28000",
            "target_digit": 8,
            "target_place": "천의 자리",
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
        text="16. 700 × 40을 계산하려고 합니다. 7 × 4 = 28에서 숫자 8은 어느 자리에 써야 하는지 알맞은 기호를 찾아 선택하세요.",
        x=32,
        y=24,
        width=820,
        height=56,
        font_size=22,
        font_family='"Noto Sans KR", sans-serif',
        fill="#202124",
        align="left",
        valign="top",
        line_height=1.5,
    )

    diagram_slots = [
        RectSlot(id="slot.diagram.outer_box", prompt="", x=283, y=94, width=320, height=176, fill="#ffffff", stroke="#8b5cf6", stroke_width=1.8, rx=4, ry=4),
        LineSlot(id="slot.diagram.h_line", prompt="", x1=308, y1=196, x2=578, y2=196, stroke="#111827", stroke_width=1.8),
        TextSlot(id="slot.diagram.n7", prompt="", text="7", x=443, y=114, font_size=24, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center"),
        TextSlot(id="slot.diagram.n0_1", prompt="", text="0", x=497, y=114, font_size=24, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center"),
        TextSlot(id="slot.diagram.n0_2", prompt="", text="0", x=551, y=114, font_size=24, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center"),
        TextSlot(id="slot.diagram.mul_sign", prompt="", text="×", x=389, y=156, font_size=24, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center"),
        TextSlot(id="slot.diagram.n4", prompt="", text="4", x=497, y=156, font_size=24, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center"),
        TextSlot(id="slot.diagram.n0_3", prompt="", text="0", x=551, y=156, font_size=24, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center"),
    ]

    for idx in range(6):
        vx = 308 + idx * 54
        diagram_slots.append(
            LineSlot(
                id=f"slot.diagram.v_line_{idx}",
                prompt="",
                x1=vx,
                y1=108,
                x2=vx,
                y2=254,
                stroke="#9ca3af",
                stroke_width=1,
            )
        )

    labels = ["㉠", "㉡", "㉢", "㉣", "㉤"]
    choice_slots = []
    for idx, label in enumerate(labels):
        bx = 315 + idx * 54
        diagram_slots.append(
            RectSlot(
                id=f"slot.diagram.cbox_{idx}",
                prompt="",
                x=bx,
                y=208,
                width=40,
                height=38,
                fill="#ffffff",
                stroke="#111827",
                stroke_width=1.2,
            )
        )
        choice_slots.append(
            TextSlot(
                id=f"slot.choice.option_{idx}",
                prompt="",
                text=label,
                x=bx + 20,
                y=214,
                font_size=22,
                font_family='"Noto Sans KR", sans-serif',
                fill="#111827",
                align="center",
                interaction={
                    "type": "choice",
                    "role": "answer",
                    "choice_index": idx,
                    "value": label,
                    "group_id": "slot.choice.group",
                    "include_in_submission": True,
                },
            )
        )

    diagram_slot_ids = tuple(s.id for s in diagram_slots)
    choice_slot_ids = tuple(s.id for s in choice_slots)

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
            Region(id="region.diagram", role="diagram", flow="absolute", slot_ids=diagram_slot_ids),
            Region(id="region.choices", role="choices", flow="absolute", slot_ids=choice_slot_ids),
        ),
        slots=(
            stem_text_slot,
            *diagram_slots,
            *choice_slots,
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
        {"ref": "multiplicand", "value": 700},
        {"ref": "multiplier", "value": 40},
    ],
    "target": {"ref": "slot.choice.option_1", "label": "숫자 8의 자리", "unit": ""},
    "method": "vertical_multiplication_place_value",
    "steps": [
        {
            "id": "compute_product",
            "expr": "700 * 40 = 28000",
            "explanation": "700 × 40 = 28000이므로 8은 천의 자리인 ㉡에 씁니다.",
            "value": "㉡",
        },
    ],
    "answer": ANSWER,
}


if __name__ == "__main__":
    print(f"[{PROBLEM_TEMPLATE.id}] 템플릿 컴파일 성공!")
    print(f"- 제목: {PROBLEM_TEMPLATE.title}")
    print(f"- 캔버스: {PROBLEM_TEMPLATE.canvas.width} x {PROBLEM_TEMPLATE.canvas.height}")
    print(f"- 구역 수: {len(PROBLEM_TEMPLATE.regions)}")
