"""ModuMath Problem DSL: 덧셈식의 규칙 찾기 (S3_초등_4_008498)"""

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
PROBLEM_ID = "S3_초등_4_008498"
PROBLEM_TITLE = "덧셈식 배열에서 자릿수 변화 규칙 찾기"


# ==============================================================================
# 2. 정답 및 오답 진단 정의 (Answer & Diagnostic Key)
# ==============================================================================
ANSWER = {
    "value": "②",
    "answer_index": 1,
    "unit": "",
    "values": ["②"],
    "choices": [
        "① 일, 20",
        "② 십, 20",
        "③ 백, 100",
    ],
    "blanks": [],
    "answer_key": [
        {
            "slot_id": "slot.choice.option_1",
            "value": "②",
            "diagnostics": [
                {
                    "id": "diag.wrong_place_ones",
                    "condition": "answer_equals_1",
                    "concept": "계산식의 규칙",
                    "reason": "변하는 자리를 일의 자리로 오인함",
                    "feedback": "200 → 210 → 220 → 230, 108 → 118 → 128 → 138에서 변하는 자리는 십의 자리입니다.",
                },
                {
                    "id": "diag.wrong_place_hundreds",
                    "condition": "answer_equals_3",
                    "concept": "계산식의 규칙",
                    "reason": "변하는 자리와 합의 증가량을 백, 100으로 오인함",
                    "feedback": "십의 자리 수가 각각 1씩 커지므로 두 수의 합은 20씩 커집니다. 따라서 ②입니다.",
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
        "difficulty": "하",
    },
    "entities": {
        "eq_0": {"label": "첫째 식", "expr": "200 + 108 = 308"},
        "eq_1": {"label": "둘째 식", "expr": "210 + 118 = 328"},
        "eq_2": {"label": "셋째 식", "expr": "220 + 128 = 348"},
        "eq_3": {"label": "넷째 식", "expr": "230 + 138 = 368"},
    },
    "relations": [
        {
            "type": "equation_pattern",
            "changing_place": "십",
            "sum_step": 20,
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
        text="24. 덧셈식에서 규칙을 찾아 ㉠, ㉡에 알맞은 것을 차례로 쓴 것은 어느 것인지 고르세요.",
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

    eq_box = RectSlot(id="slot.diagram.eq_box", prompt="", x=293, y=82, width=300, height=138, fill="#ffffff", stroke="#84cc16", stroke_width=1.6)
    eqs = [
        "200 + 108 = 308",
        "210 + 118 = 328",
        "220 + 128 = 348",
        "230 + 138 = 368",
    ]
    eq_slots = [
        TextSlot(id=f"slot.diagram.eq_{i}", prompt="", text=eq, x=443, y=94 + i * 30, font_size=22, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center")
        for i, eq in enumerate(eqs)
    ]

    desc = TextBoxSlot(
        id="slot.diagram.desc",
        prompt="",
        text="㉠의 자리 수가 각각 1씩 커지면 두 수의 합은 ㉡씩 커집니다.",
        x=80,
        y=234,
        width=726,
        height=34,
        font_size=20,
        font_family='"Noto Sans KR", sans-serif',
        fill="#111827",
        align="center",
        valign="middle",
    )

    c0 = TextSlot(id="slot.choice.option_0", prompt="", text="① 일, 20", x=186, y=282, font_size=21, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center", interaction={"type": "choice", "role": "answer", "choice_index": 0, "value": "①", "group_id": "slot.choice.group", "include_in_submission": True})
    c1 = TextSlot(id="slot.choice.option_1", prompt="", text="② 십, 20", x=443, y=282, font_size=21, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center", interaction={"type": "choice", "role": "answer", "choice_index": 1, "value": "②", "group_id": "slot.choice.group", "include_in_submission": True})
    c2 = TextSlot(id="slot.choice.option_2", prompt="", text="③ 백, 100", x=700, y=282, font_size=21, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center", interaction={"type": "choice", "role": "answer", "choice_index": 2, "value": "③", "group_id": "slot.choice.group", "include_in_submission": True})

    return ProblemTemplate(
        id=PROBLEM_ID,
        title=PROBLEM_TITLE,
        canvas=Canvas(
            width=886,
            height=336,
            coordinate_mode="logical",
        ),
        regions=(
            Region(id="region.stem", role="stem", flow="absolute", slot_ids=("slot.stem.question",)),
            Region(id="region.diagram", role="diagram", flow="absolute", slot_ids=("slot.diagram.eq_box", *(s.id for s in eq_slots), "slot.diagram.desc")),
            Region(id="region.choices", role="choices", flow="absolute", slot_ids=("slot.choice.option_0", "slot.choice.option_1", "slot.choice.option_2")),
        ),
        slots=(
            stem_text_slot,
            eq_box,
            *eq_slots,
            desc,
            c0,
            c1,
            c2,
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
        {"ref": "eq_0", "value": "200 + 108 = 308"},
        {"ref": "eq_1", "value": "210 + 118 = 328"},
    ],
    "target": {"ref": "slot.choice.option_1", "label": "㉠, ㉡에 알맞은 것", "unit": ""},
    "method": "equation_pattern_analysis",
    "steps": [
        {
            "id": "find_pattern",
            "expr": "십의 자리 +1 => 합 +20",
            "explanation": "십의 자리 수가 각각 1씩 커지면 두 수의 합은 20씩 커집니다.",
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
