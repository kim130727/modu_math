"""ModuMath Problem DSL: 어림한 결과가 3과 4 사이인 뺄셈식 찾기 (S3_초등_4_007336)"""

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
PROBLEM_ID = "S3_초등_4_007336"
PROBLEM_TITLE = "어림한 결과가 3과 4 사이인 분수의 뺄셈식 선택하기"


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
                    "id": "diag.exceeds_5",
                    "condition": "answer_equals_1",
                    "concept": "대분수 뺄셈의 어림",
                    "reason": "6과 4/5 - 1과 3/5은 5보다 큰 수임에도 3과 4 사이로 오인함",
                    "feedback": "6과 4/5 - 1과 3/5은 6 - 1 = 5이고 4/5 > 3/5이므로 5보다 큽니다. 3과 3/7 - 1/7은 3과 4 사이입니다.",
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
        "difficulty": "하",
    },
    "entities": {
        "expr_0": {"label": "① 6과 4/5 - 1과 3/5", "value": "5와 1/5", "in_range_3_4": False},
        "expr_1": {"label": "② 3과 3/7 - 1/7", "value": "3과 2/7", "in_range_3_4": True},
    },
    "relations": [
        {
            "type": "range_check",
            "min": 3,
            "max": 4,
            "correct_entity": "expr_1",
            "distractor": "expr_0",
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
        text="7. 어림한 결과가 3과 4 사이인 뺄셈식을 선택하세요.",
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
    _add_frac(diagram_slots, "l1", 264, 148, "6", "4", "5")
    diagram_slots.append(TextSlot(id="slot.diagram.op0", prompt="", text="−", x=309, y=134, font_size=24, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center"))
    _add_frac(diagram_slots, "l2", 354, 148, "1", "3", "5")

    card_1 = RectSlot(id="slot.choice.option_1", prompt="", x=443, y=92, width=267, height=112, fill="#fef3c7", stroke="#d97706", stroke_width=1.5, interaction={"type": "choice", "role": "answer", "choice_index": 1, "value": "②", "group_id": "slot.choice.group", "include_in_submission": True})
    diagram_slots.append(TextSlot(id="slot.diagram.b1", prompt="", text="②", x=463, y=104, font_size=18, font_family='"Noto Sans KR", sans-serif', fill="#4b5563", align="center"))
    _add_frac(diagram_slots, "r1", 534, 148, "3", "3", "7")
    diagram_slots.append(TextSlot(id="slot.diagram.op1", prompt="", text="−", x=578, y=134, font_size=24, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center"))
    _add_frac(diagram_slots, "r2", 616, 148, "", "1", "7")

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
        {"ref": "expr_0", "value": "6과 4/5 - 1과 3/5"},
        {"ref": "expr_1", "value": "3과 3/7 - 1/7"},
    ],
    "target": {"ref": "slot.choice.option_1", "label": "3과 4 사이인 뺄셈식", "unit": ""},
    "method": "fraction_estimation",
    "steps": [
        {
            "id": "estimate_difference",
            "expr": "3과 3/7 - 1/7 = 3과 2/7",
            "explanation": "3과 3/7 - 1/7은 3/7 > 1/7이므로 결과가 3과 4 사이에 있습니다.",
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
