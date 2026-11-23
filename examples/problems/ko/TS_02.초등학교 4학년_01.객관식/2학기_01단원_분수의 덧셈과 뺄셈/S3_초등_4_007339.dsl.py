"""ModuMath Problem DSL: 어림한 결과가 2와 3 사이인 뺄셈식 찾기 2 (S3_초등_4_007339)"""

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
PROBLEM_ID = "S3_초등_4_007339"
PROBLEM_TITLE = "어림한 결과가 2와 3 사이인 뺄셈식 선택하기"


# ==============================================================================
# 2. 정답 및 오답 진단 정의 (Answer & Diagnostic Key)
# ==============================================================================
ANSWER = {
    "value": "①",
    "answer_index": 0,
    "unit": "",
    "values": ["①"],
    "choices": [
        "①",
        "②",
    ],
    "blanks": [],
    "answer_key": [
        {
            "slot_id": "slot.choice.option_0",
            "value": "①",
            "diagnostics": [
                {
                    "id": "diag.below_2",
                    "condition": "answer_equals_2",
                    "concept": "대분수 뺄셈의 어림",
                    "reason": "5와 1/3 - 3과 2/3이 2보다 작은 수임에도 2와 3 사이로 오인함",
                    "feedback": "5와 1/3 - 3과 2/3에서 5 - 3 = 2이고 1/3 < 2/3이므로 2보다 작습니다. 3과 1/6 - 3/6은 2와 3 사이입니다.",
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
    "problem_type": "multiple_choice_fraction_estimation",
    "metadata": {
        "school": "초등학교",
        "grade": 4,
        "semester": "2학기",
        "chapter": "01단원_분수의 덧셈과 뺄셈",
        "difficulty": "중",
    },
    "entities": {
        "expr_0": {"label": "① 3과 1/6 - 3/6", "value": "2와 4/6", "in_range_2_3": True},
        "expr_1": {"label": "② 5와 1/3 - 3과 2/3", "value": "1과 2/3", "in_range_2_3": False},
    },
    "relations": [
        {
            "type": "range_check",
            "min": 2,
            "max": 3,
            "correct_entity": "expr_0",
            "distractor": "expr_1",
        }
    ],
}


# ==============================================================================
# 4. 문제 템플릿 빌더 (ProblemTemplate Builder)
# ==============================================================================
def _add_frac(slots: list, prefix: str, cx: int, cy: int, whole: str, num: str, den: str) -> None:
    if whole:
        slots.append(TextSlot(id=f"slot.diagram.{prefix}_w", prompt="", text=whole, x=cx - 20, y=cy - 12, font_size=24, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center"))
    fx = cx + (6 if whole else 0)
    slots.append(TextSlot(id=f"slot.diagram.{prefix}_n", prompt="", text=num, x=fx, y=cy - 26, font_size=20, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center"))
    slots.append(LineSlot(id=f"slot.diagram.{prefix}_bar", prompt="", x1=fx - 12, y1=cy, x2=fx + 12, y2=cy, stroke="#111827", stroke_width=1.6))
    slots.append(TextSlot(id=f"slot.diagram.{prefix}_d", prompt="", text=den, x=fx, y=cy + 4, font_size=20, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center"))


def build_problem_template() -> ProblemTemplate:
    """문제의 캔버스 크기, 슬롯(텍스트/도형/선택지), 리전(구역)을 정의합니다."""

    stem_text_slot = TextBoxSlot(
        id="slot.stem.question",
        prompt="",
        text="10. 어림한 결과가 2와 3 사이인 뺄셈식을 선택하세요.",
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

    diagram_slots = []
    card_0 = RectSlot(id="slot.choice.option_0", prompt="", x=176, y=92, width=267, height=112, fill="#fef3c7", stroke="#d97706", stroke_width=1.5, interaction={"type": "choice", "role": "answer", "choice_index": 0, "value": "①", "group_id": "slot.choice.group", "include_in_submission": True})
    diagram_slots.append(TextSlot(id="slot.diagram.b0", prompt="", text="①", x=196, y=104, font_size=18, font_family='"Noto Sans KR", sans-serif', fill="#4b5563", align="center"))
    _add_frac(diagram_slots, "l1", 268, 148, "3", "1", "6")
    diagram_slots.append(TextSlot(id="slot.diagram.op0", prompt="", text="−", x=312, y=134, font_size=24, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center"))
    _add_frac(diagram_slots, "l2", 350, 148, "", "3", "6")

    card_1 = RectSlot(id="slot.choice.option_1", prompt="", x=443, y=92, width=267, height=112, fill="#fef3c7", stroke="#d97706", stroke_width=1.5, interaction={"type": "choice", "role": "answer", "choice_index": 1, "value": "②", "group_id": "slot.choice.group", "include_in_submission": True})
    diagram_slots.append(TextSlot(id="slot.diagram.b1", prompt="", text="②", x=463, y=104, font_size=18, font_family='"Noto Sans KR", sans-serif', fill="#4b5563", align="center"))
    _add_frac(diagram_slots, "r1", 530, 148, "5", "1", "3")
    diagram_slots.append(TextSlot(id="slot.diagram.op1", prompt="", text="−", x=575, y=134, font_size=24, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center"))
    _add_frac(diagram_slots, "r2", 620, 148, "3", "2", "3")

    return ProblemTemplate(
        id=PROBLEM_ID,
        title=PROBLEM_TITLE,
        canvas=Canvas(
            width=886,
            height=240,
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
        {"ref": "expr_0", "value": "3과 1/6 - 3/6"},
        {"ref": "expr_1", "value": "5와 1/3 - 3과 2/3"},
    ],
    "target": {"ref": "slot.choice.option_0", "label": "2와 3 사이인 뺄셈식", "unit": ""},
    "method": "fraction_estimation",
    "steps": [
        {
            "id": "estimate_difference",
            "expr": "3과 1/6 - 3/6 = 2와 4/6",
            "explanation": "1/6은 3/6보다 작으므로 3과 1/6 - 3/6은 2와 3 사이에 있습니다.",
            "value": "①",
        },
    ],
    "answer": ANSWER,
}


if __name__ == "__main__":
    print(f"[{PROBLEM_TEMPLATE.id}] 템플릿 컴파일 성공!")
    print(f"- 제목: {PROBLEM_TEMPLATE.title}")
    print(f"- 캔버스: {PROBLEM_TEMPLATE.canvas.width} x {PROBLEM_TEMPLATE.canvas.height}")
    print(f"- 구역 수: {len(PROBLEM_TEMPLATE.regions)}")
