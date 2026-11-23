"""ModuMath Problem DSL: 분수의 뺄셈 결과 크기 비교 (S3_초등_4_007332)"""

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
PROBLEM_ID = "S3_초등_4_007332"
PROBLEM_TITLE = "분수의 뺄셈 중 계산 결과가 더 큰 것 선택하기"


# ==============================================================================
# 2. 정답 및 오답 진단 정의 (Answer & Diagnostic Key)
# ==============================================================================
ANSWER = {
    "value": "②",
    "answer_index": 1,
    "unit": "",
    "values": ["②"],
    "choices": [
        "①",
        "②",
    ],
    "blanks": [],
    "answer_key": [
        {
            "slot_id": "slot.choice.option_1",
            "value": "②",
            "diagnostics": [
                {
                    "id": "diag.chose_smaller_diff",
                    "condition": "answer_equals_1",
                    "concept": "분수의 뺄셈과 크기 비교",
                    "reason": "8 - 3과 3/4 = 4와 1/4이 6과 1/4 - 7/4 = 4와 2/4보다 작음에도 ①을 선택함",
                    "feedback": "8 - 3과 3/4 = 4와 1/4이고, 6과 1/4 - 7/4 = 4와 2/4입니다. 따라서 계산 결과가 더 큰 것은 ②입니다.",
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
    "problem_type": "multiple_choice_fraction_comparison",
    "metadata": {
        "school": "초등학교",
        "grade": 4,
        "semester": "2학기",
        "chapter": "01단원_분수의 덧셈과 뺄셈",
        "difficulty": "중",
    },
    "entities": {
        "expr_0": {"label": "① 8 - 3과 3/4", "value": "4와 1/4"},
        "expr_1": {"label": "② 6과 1/4 - 7/4", "value": "4와 2/4"},
    },
    "relations": [
        {
            "type": "greater_than",
            "larger": "expr_1",
            "smaller": "expr_0",
        }
    ],
}


# ==============================================================================
# 4. 문제 템플릿 빌더 (ProblemTemplate Builder)
# ==============================================================================
def _add_frac(slots: list, prefix: str, cx: int, cy: int, whole: str, num: str, den: str) -> None:
    if whole:
        slots.append(TextSlot(id=f"slot.diagram.{prefix}_w", prompt="", text=whole, x=cx - 20, y=cy - 12, font_size=24, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center"))
    if num and den:
        fx = cx + (6 if whole else 0)
        slots.append(TextSlot(id=f"slot.diagram.{prefix}_n", prompt="", text=num, x=fx, y=cy - 26, font_size=20, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center"))
        slots.append(LineSlot(id=f"slot.diagram.{prefix}_bar", prompt="", x1=fx - 12, y1=cy, x2=fx + 12, y2=cy, stroke="#111827", stroke_width=1.6))
        slots.append(TextSlot(id=f"slot.diagram.{prefix}_d", prompt="", text=den, x=fx, y=cy + 4, font_size=20, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center"))


def build_problem_template() -> ProblemTemplate:
    """문제의 캔버스 크기, 슬롯(텍스트/도형/선택지), 리전(구역)을 정의합니다."""

    stem_text_slot = TextBoxSlot(
        id="slot.stem.question",
        prompt="",
        text="3. 계산 결과가 더 큰 것을 선택하세요.",
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

    diagram_slots = [
        CircleSlot(id="slot.diagram.lion", prompt="", cx=291, cy=114, r=24, fill="#fde68a", stroke="#b45309", stroke_width=2),
        CircleSlot(id="slot.diagram.rabbit", prompt="", cx=595, cy=114, r=24, fill="#f3f4f6", stroke="#6b7280", stroke_width=1.5),
    ]

    card_0 = RectSlot(id="slot.choice.option_0", prompt="", x=176, y=138, width=230, height=96, fill="#f3e0c2", stroke="#b48a5a", stroke_width=1.5, rx=6, ry=6, interaction={"type": "choice", "role": "answer", "choice_index": 0, "value": "①", "group_id": "slot.choice.group", "include_in_submission": True})
    diagram_slots.append(TextSlot(id="slot.diagram.b0", prompt="", text="①", x=196, y=148, font_size=18, font_family='"Noto Sans KR", sans-serif', fill="#4b5563", align="center"))
    _add_frac(diagram_slots, "l1", 268, 186, "8", "", "")
    diagram_slots.append(TextSlot(id="slot.diagram.op0", prompt="", text="−", x=290, y=172, font_size=24, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center"))
    _add_frac(diagram_slots, "l2", 336, 186, "3", "3", "4")

    card_1 = RectSlot(id="slot.choice.option_1", prompt="", x=480, y=138, width=230, height=96, fill="#f3e0c2", stroke="#b48a5a", stroke_width=1.5, rx=6, ry=6, interaction={"type": "choice", "role": "answer", "choice_index": 1, "value": "②", "group_id": "slot.choice.group", "include_in_submission": True})
    diagram_slots.append(TextSlot(id="slot.diagram.b1", prompt="", text="②", x=500, y=148, font_size=18, font_family='"Noto Sans KR", sans-serif', fill="#4b5563", align="center"))
    _add_frac(diagram_slots, "r1", 554, 186, "6", "1", "4")
    diagram_slots.append(TextSlot(id="slot.diagram.op1", prompt="", text="−", x=598, y=172, font_size=24, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center"))
    _add_frac(diagram_slots, "r2", 636, 186, "", "7", "4")

    return ProblemTemplate(
        id=PROBLEM_ID,
        title=PROBLEM_TITLE,
        canvas=Canvas(
            width=886,
            height=265,
            coordinate_mode="logical",
        ),
        regions=(
            Region(id="region.stem", role="stem", flow="absolute", slot_ids=("slot.stem.question",)),
            Region(id="region.choices", role="choices", flow="absolute", slot_ids=("slot.choice.option_0", "slot.choice.option_1")),
            Region(id="region.diagram", role="diagram", flow="absolute", slot_ids=tuple(s.id for s in diagram_slots)),
        ),
        slots=(
            stem_text_slot,
            card_0,
            card_1,
            *diagram_slots,
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
        {"ref": "expr_0", "value": "4와 1/4"},
        {"ref": "expr_1", "value": "4와 2/4"},
    ],
    "target": {"ref": "slot.choice.option_1", "label": "계산 결과가 더 큰 식", "unit": ""},
    "method": "fraction_subtraction_comparison",
    "steps": [
        {
            "id": "compare_differences",
            "expr": "4와 1/4 < 4와 2/4",
            "explanation": "8 - 3과 3/4 = 4와 1/4, 6과 1/4 - 7/4 = 4와 2/4이므로 ②가 더 큽니다.",
            "value": "②",
        },
    ],
    "answer": ANSWER,
}


if __name__ == "__main__":
    print(f"[{PROBLEM_TEMPLATE.id}] 템플릿 컴파일 성공!")
    print(f"- 제목: {PROBLEM_TEMPLATE.title}")
    print(f"- 캔버스: {PROBLEM_TEMPLATE.canvas.width} x {PROBLEM_TEMPLATE.canvas.height}")
    print(f"- 구역 수: {len(PROBLEM_TEMPLATE.regions)}")
