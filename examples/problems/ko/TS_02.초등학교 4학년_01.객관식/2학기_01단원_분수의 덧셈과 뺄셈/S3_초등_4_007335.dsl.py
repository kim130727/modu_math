"""ModuMath Problem DSL: 자연수와 분수의 뺄셈 바르게 계산한 것 찾기 (S3_초등_4_007335)"""

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
PROBLEM_ID = "S3_초등_4_007335"
PROBLEM_TITLE = "자연수와 분수의 뺄셈 중 바르게 계산한 것 선택하기"


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
    ],
    "blanks": [],
    "answer_key": [
        {
            "slot_id": "slot.choice.option_1",
            "value": "㉡",
            "diagnostics": [
                {
                    "id": "diag.forgot_fraction_subtraction",
                    "condition": "answer_equals_giyeok",
                    "concept": "자연수에서 분수 빼기",
                    "reason": "2에서 1을 받아내림만 하고 분수 부분을 빼지 않은 식(㉠)을 선택함",
                    "feedback": "2 - 3/4 = 1과 4/4 - 3/4 = 1과 1/4입니다. 바르게 계산한 것은 ㉡입니다.",
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
    "problem_type": "multiple_choice_fraction_verification",
    "metadata": {
        "school": "초등학교",
        "grade": 4,
        "semester": "2학기",
        "chapter": "01단원_분수의 덧셈과 뺄셈",
        "difficulty": "하",
    },
    "entities": {
        "eq_0": {"label": "㉠", "expr": "2 - 3/4 = 1과 3/4", "is_correct": False},
        "eq_1": {"label": "㉡", "expr": "5 - 1과 4/7 = 3과 3/7", "is_correct": True},
    },
    "relations": [
        {
            "type": "correct_calculation",
            "correct_entity": "eq_1",
            "distractor": "eq_0",
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
        text="6. 바르게 계산한 것을 찾아 선택해 보세요.",
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

    outer_box = RectSlot(id="slot.diagram.outer_box", prompt="", x=116, y=88, width=654, height=118, fill="#ffffff", stroke="#f59e0b", stroke_width=1.8)
    diagram_slots = [outer_box]

    c0 = TextSlot(id="slot.choice.option_0", prompt="", text="㉠", x=166, y=134, font_size=24, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center", interaction={"type": "choice", "role": "answer", "choice_index": 0, "value": "㉠", "group_id": "slot.choice.group", "include_in_submission": True})
    _add_frac(diagram_slots, "g1", 230, 148, "2", "", "")
    diagram_slots.append(TextSlot(id="slot.diagram.g_op", prompt="", text="−", x=250, y=134, font_size=24, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center"))
    _add_frac(diagram_slots, "g2", 282, 148, "", "3", "4")
    diagram_slots.append(TextSlot(id="slot.diagram.g_eq", prompt="", text="=", x=316, y=134, font_size=24, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center"))
    _add_frac(diagram_slots, "g3", 364, 148, "1", "3", "4")

    c1 = TextSlot(id="slot.choice.option_1", prompt="", text="㉡", x=470, y=134, font_size=24, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center", interaction={"type": "choice", "role": "answer", "choice_index": 1, "value": "㉡", "group_id": "slot.choice.group", "include_in_submission": True})
    _add_frac(diagram_slots, "n1", 530, 148, "5", "", "")
    diagram_slots.append(TextSlot(id="slot.diagram.n_op", prompt="", text="−", x=550, y=134, font_size=24, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center"))
    _add_frac(diagram_slots, "n2", 596, 148, "1", "4", "7")
    diagram_slots.append(TextSlot(id="slot.diagram.n_eq", prompt="", text="=", x=642, y=134, font_size=24, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center"))
    _add_frac(diagram_slots, "n3", 690, 148, "3", "3", "7")

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
            c0,
            c1,
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
        {"ref": "eq_0", "value": "2 - 3/4 = 1과 3/4"},
        {"ref": "eq_1", "value": "5 - 1과 4/7 = 3과 3/7"},
    ],
    "target": {"ref": "slot.choice.option_1", "label": "바르게 계산한 것", "unit": ""},
    "method": "fraction_subtraction_verification",
    "steps": [
        {
            "id": "verify_subtraction",
            "expr": "5 - 1과 4/7 = 4와 7/7 - 1과 4/7 = 3과 3/7",
            "explanation": "5에서 1을 받아내림하여 4와 7/7로 바꾼 뒤 빼면 3과 3/7이므로 ㉡이 바릅니다.",
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
