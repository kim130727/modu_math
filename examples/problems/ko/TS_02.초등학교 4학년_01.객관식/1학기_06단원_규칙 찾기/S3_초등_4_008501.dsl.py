"""ModuMath Problem DSL: 규칙에 맞는 계산식 묶음 선택하기 (S3_초등_4_008501)"""

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
PROBLEM_ID = "S3_초등_4_008501"
PROBLEM_TITLE = "백의 자리 수가 1씩 커질 때 결과가 200씩 커지는 계산식 찾기"


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
                    "id": "diag.chose_constant_difference",
                    "condition": "answer_equals_2",
                    "concept": "덧셈식과 뺄셈식의 규칙",
                    "reason": "결과가 일정한 뺄셈식(②)을 결과가 200씩 커지는 식으로 선택함",
                    "feedback": "오른쪽 뺄셈식(②)은 백의 자리 수가 각각 1씩 커지면 두 수의 차가 340으로 일정합니다. 왼쪽 덧셈식(①)이 200씩 커집니다.",
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
        "option_0": {"label": "①", "operation": "addition", "result_step": 200},
        "option_1": {"label": "②", "operation": "subtraction", "result_step": 0},
    },
    "relations": [
        {
            "type": "pattern_match",
            "target_step": 200,
            "correct_entity": "option_0",
            "distractor": "option_1",
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
        text="27. 백의 자리 수가 각각 1씩 커지면 두 수의 계산 결과가 200씩 커지는 계산식을 선택하세요.",
        x=32,
        y=20,
        width=820,
        height=52,
        font_size=21,
        font_family='"Noto Sans KR", sans-serif',
        fill="#202124",
        align="left",
        valign="top",
        line_height=1.45,
    )

    card_0 = RectSlot(id="slot.choice.option_0", prompt="", x=116, y=92, width=290, height=166, fill="#ffffff", stroke="#8b5cf6", stroke_width=1.6, rx=8, ry=8, interaction={"type": "choice", "role": "answer", "choice_index": 0, "value": "①", "group_id": "slot.choice.group", "include_in_submission": True})
    b0 = TextSlot(id="slot.diagram.b0", prompt="", text="①", x=138, y=104, font_size=18, font_family='"Noto Sans KR", sans-serif', fill="#4b5563", align="center")
    eqs_0 = ["160 + 210 = 370", "260 + 310 = 570", "360 + 410 = 770", "460 + 510 = 970"]
    s0 = [TextSlot(id=f"slot.diagram.l_{i}", prompt="", text=eq, x=266, y=114 + i * 32, font_size=21, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center") for i, eq in enumerate(eqs_0)]

    card_1 = RectSlot(id="slot.choice.option_1", prompt="", x=480, y=92, width=290, height=166, fill="#ffffff", stroke="#8b5cf6", stroke_width=1.6, rx=8, ry=8, interaction={"type": "choice", "role": "answer", "choice_index": 1, "value": "②", "group_id": "slot.choice.group", "include_in_submission": True})
    b1 = TextSlot(id="slot.diagram.b1", prompt="", text="②", x=502, y=104, font_size=18, font_family='"Noto Sans KR", sans-serif', fill="#4b5563", align="center")
    eqs_1 = ["650 - 310 = 340", "750 - 410 = 340", "850 - 510 = 340", "950 - 610 = 340"]
    s1 = [TextSlot(id=f"slot.diagram.r_{i}", prompt="", text=eq, x=630, y=114 + i * 32, font_size=21, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center") for i, eq in enumerate(eqs_1)]

    return ProblemTemplate(
        id=PROBLEM_ID,
        title=PROBLEM_TITLE,
        canvas=Canvas(
            width=886,
            height=290,
            coordinate_mode="logical",
        ),
        regions=(
            Region(id="region.stem", role="stem", flow="absolute", slot_ids=("slot.stem.question",)),
            Region(id="region.choices", role="choices", flow="absolute", slot_ids=("slot.choice.option_0", "slot.choice.option_1")),
            Region(id="region.diagram", role="diagram", flow="absolute", slot_ids=("slot.diagram.b0", *(s.id for s in s0), "slot.diagram.b1", *(s.id for s in s1))),
        ),
        slots=(
            stem_text_slot,
            card_0,
            b0,
            *s0,
            card_1,
            b1,
            *s1,
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
        {"ref": "option_0", "value": "370 -> 570 -> 770 -> 970"},
        {"ref": "option_1", "value": "340 -> 340 -> 340 -> 340"},
    ],
    "target": {"ref": "slot.choice.option_0", "label": "200씩 커지는 계산식", "unit": ""},
    "method": "equation_pattern_analysis",
    "steps": [
        {
            "id": "compare_results",
            "expr": "370, 570, 770, 970 (+200)",
            "explanation": "두 수의 백의 자리 수가 각각 1씩 커질 때 계산 결과가 200씩 커지는 식은 ①입니다.",
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
