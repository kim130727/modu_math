"""ModuMath Problem DSL: 어림한 결과가 3과 4 사이인 덧셈식 찾기 (S3_초등_4_007331)"""

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
PROBLEM_ID = "S3_초등_4_007331"
PROBLEM_TITLE = "어림한 결과가 3과 4 사이인 대분수의 덧셈식 선택하기"


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
                    "id": "diag.exceeds_4",
                    "condition": "answer_equals_2",
                    "concept": "대분수 덧셈의 어림",
                    "reason": "진분수 부분의 합이 1보다 커서 4를 넘는 식(②)을 선택함",
                    "feedback": "1 2/3 + 2 2/3에서 1 + 2 = 3이고 2/3 + 2/3 = 1 1/3으로 1보다 크기 때문에 4보다 큽니다. 2 1/7 + 1 2/7은 3과 4 사이입니다.",
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
        "expr_0": {"label": "① 2와 1/7 + 1과 2/7", "value": "3과 3/7", "in_range_3_4": True},
        "expr_1": {"label": "② 1과 2/3 + 2와 2/3", "value": "4와 1/3", "in_range_3_4": False},
    },
    "relations": [
        {
            "type": "range_check",
            "min": 3,
            "max": 4,
            "correct_entity": "expr_0",
            "distractor": "expr_1",
        }
    ],
}


# ==============================================================================
# 4. 문제 템플릿 빌더 (ProblemTemplate Builder)
# ==============================================================================
def _add_mixed_fraction(slots: list, prefix: str, cx: int, cy: int, whole: str, num: str, den: str) -> None:
    if whole:
        slots.append(TextSlot(id=f"slot.diagram.{prefix}_w", prompt="", text=whole, x=cx - 20, y=cy - 12, font_size=24, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center"))
    fx = cx + (6 if whole else 0)
    slots.append(TextSlot(id=f"slot.diagram.{prefix}_n", prompt="", text=num, x=fx, y=cy - 26, font_size=20, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center"))
    slots.append(LineSlot(id=f"slot.diagram.{prefix}_bar", prompt="", x1=fx - 13, y1=cy, x2=fx + 13, y2=cy, stroke="#111827", stroke_width=1.6))
    slots.append(TextSlot(id=f"slot.diagram.{prefix}_d", prompt="", text=den, x=fx, y=cy + 4, font_size=20, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center"))


def build_problem_template() -> ProblemTemplate:
    """문제의 캔버스 크기, 슬롯(텍스트/도형/선택지), 리전(구역)을 정의합니다."""

    stem_text_slot = TextBoxSlot(
        id="slot.stem.question",
        prompt="",
        text="2. 어림한 결과가 3과 4 사이인 덧셈식을 선택하세요.",
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

    card_0 = RectSlot(id="slot.choice.option_0", prompt="", x=176, y=92, width=230, height=112, fill="#e8e4f3", stroke="#a78bfa", stroke_width=1.5, rx=6, ry=6, interaction={"type": "choice", "role": "answer", "choice_index": 0, "value": "①", "group_id": "slot.choice.group", "include_in_submission": True})
    diagram_slots.append(TextSlot(id="slot.diagram.b0", prompt="", text="①", x=196, y=104, font_size=18, font_family='"Noto Sans KR", sans-serif', fill="#4b5563", align="center"))
    _add_mixed_fraction(diagram_slots, "l1", 246, 148, "2", "1", "7")
    diagram_slots.append(TextSlot(id="slot.diagram.op0", prompt="", text="+", x=291, y=134, font_size=24, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center"))
    _add_mixed_fraction(diagram_slots, "l2", 336, 148, "1", "2", "7")

    card_1 = RectSlot(id="slot.choice.option_1", prompt="", x=480, y=92, width=230, height=112, fill="#e8e4f3", stroke="#a78bfa", stroke_width=1.5, rx=6, ry=6, interaction={"type": "choice", "role": "answer", "choice_index": 1, "value": "②", "group_id": "slot.choice.group", "include_in_submission": True})
    diagram_slots.append(TextSlot(id="slot.diagram.b1", prompt="", text="②", x=500, y=104, font_size=18, font_family='"Noto Sans KR", sans-serif', fill="#4b5563", align="center"))
    _add_mixed_fraction(diagram_slots, "r1", 550, 148, "1", "2", "3")
    diagram_slots.append(TextSlot(id="slot.diagram.op1", prompt="", text="+", x=595, y=134, font_size=24, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center"))
    _add_mixed_fraction(diagram_slots, "r2", 640, 148, "2", "2", "3")

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
        {"ref": "expr_0", "value": "2와 1/7 + 1과 2/7"},
        {"ref": "expr_1", "value": "1과 2/3 + 2와 2/3"},
    ],
    "target": {"ref": "slot.choice.option_0", "label": "3과 4 사이인 덧셈식", "unit": ""},
    "method": "fraction_estimation",
    "steps": [
        {
            "id": "estimate_sum",
            "expr": "2 + 1 = 3, 1/7 + 2/7 = 3/7 < 1",
            "explanation": "2와 1/7 + 1과 2/7은 3과 4 사이에 있습니다.",
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
