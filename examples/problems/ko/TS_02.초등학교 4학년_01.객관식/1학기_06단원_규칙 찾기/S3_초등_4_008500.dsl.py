"""ModuMath Problem DSL: 11을 곱하는 곱셈식의 규칙 찾기 (S3_초등_4_008500)"""

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
PROBLEM_ID = "S3_초등_4_008500"
PROBLEM_TITLE = "11을 곱하는 곱셈식의 자릿수 규칙 찾기"


# ==============================================================================
# 2. 정답 및 오답 진단 정의 (Answer & Diagnostic Key)
# ==============================================================================
ANSWER = {
    "value": "같은",
    "answer_index": 0,
    "unit": "",
    "values": ["같은"],
    "choices": [
        "같은",
        "다른",
    ],
    "blanks": [],
    "answer_key": [
        {
            "slot_id": "slot.choice.option_0",
            "value": "같은",
            "diagnostics": [
                {
                    "id": "diag.misread_digits",
                    "condition": "answer_equals_different",
                    "concept": "곱셈식의 규칙",
                    "reason": "121, 242, 363, 484의 백의 자리와 일의 자리 숫자가 같음을 놓침",
                    "feedback": "121(1, 1), 242(2, 2), 363(3, 3), 484(4, 4)처럼 백의 자리 수와 일의 자리 수가 같은 세 자리 수가 나옵니다.",
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
        "eq_0": {"label": "11 × 11", "result": 121},
        "eq_1": {"label": "22 × 11", "result": 242},
        "eq_2": {"label": "33 × 11", "result": 363},
        "eq_3": {"label": "44 × 11", "result": 484},
    },
    "relations": [
        {
            "type": "digit_symmetry",
            "hundreds_equals_ones": True,
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
        text="26. 곱셈식에서 규칙을 찾아 알맞은 것을 선택하세요.",
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

    eq_box = RectSlot(id="slot.diagram.eq_box", prompt="", x=293, y=76, width=300, height=138, fill="#ffffff", stroke="#8b5cf6", stroke_width=1.6)
    eqs = [
        "11 × 11 = 121",
        "22 × 11 = 242",
        "33 × 11 = 363",
        "44 × 11 = 484",
    ]
    eq_slots = [
        TextSlot(id=f"slot.diagram.eq_{i}", prompt="", text=eq, x=443, y=88 + i * 30, font_size=22, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center")
        for i, eq in enumerate(eqs)
    ]

    desc = TextSlot(id="slot.diagram.desc", prompt="", text="11, 22, 33, 44에 각각 11을 곱하면", x=443, y=228, font_size=20, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center")

    c_pre = TextSlot(id="slot.choice.pre", prompt="", text="백의 자리 수와 일의 자리 수가 (", x=250, y=268, font_size=20, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center")
    c0 = TextSlot(id="slot.choice.option_0", prompt="", text="같은", x=422, y=268, font_size=20, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center", interaction={"type": "choice", "role": "answer", "choice_index": 0, "value": "같은", "group_id": "slot.choice.group", "include_in_submission": True})
    cm = TextSlot(id="slot.choice.cm", prompt="", text=",", x=450, y=268, font_size=20, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center")
    c1 = TextSlot(id="slot.choice.option_1", prompt="", text="다른", x=478, y=268, font_size=20, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center", interaction={"type": "choice", "role": "answer", "choice_index": 1, "value": "다른", "group_id": "slot.choice.group", "include_in_submission": True})
    c_suf = TextSlot(id="slot.choice.suf", prompt="", text=") 세 자리 수가 나옵니다.", x=618, y=268, font_size=20, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center")

    return ProblemTemplate(
        id=PROBLEM_ID,
        title=PROBLEM_TITLE,
        canvas=Canvas(
            width=886,
            height=320,
            coordinate_mode="logical",
        ),
        regions=(
            Region(id="region.stem", role="stem", flow="absolute", slot_ids=("slot.stem.question",)),
            Region(id="region.diagram", role="diagram", flow="absolute", slot_ids=("slot.diagram.eq_box", *(s.id for s in eq_slots), "slot.diagram.desc")),
            Region(id="region.choices", role="choices", flow="absolute", slot_ids=("slot.choice.pre", "slot.choice.option_0", "slot.choice.cm", "slot.choice.option_1", "slot.choice.suf")),
        ),
        slots=(
            stem_text_slot,
            eq_box,
            *eq_slots,
            desc,
            c_pre,
            c0,
            cm,
            c1,
            c_suf,
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
        {"ref": "eq_0", "value": 121},
        {"ref": "eq_1", "value": 242},
        {"ref": "eq_2", "value": 363},
        {"ref": "eq_3", "value": 484},
    ],
    "target": {"ref": "slot.choice.option_0", "label": "백의 자리와 일의 자리의 관계", "unit": ""},
    "method": "digit_pattern_observation",
    "steps": [
        {
            "id": "compare_digits",
            "expr": "121, 242, 363, 484",
            "explanation": "백의 자리 수와 일의 자리 수가 같은 세 자리 수가 나옵니다.",
            "value": "같은",
        },
    ],
    "answer": ANSWER,
}


if __name__ == "__main__":
    print(f"[{PROBLEM_TEMPLATE.id}] 템플릿 컴파일 성공!")
    print(f"- 제목: {PROBLEM_TEMPLATE.title}")
    print(f"- 캔버스: {PROBLEM_TEMPLATE.canvas.width} x {PROBLEM_TEMPLATE.canvas.height}")
    print(f"- 구역 수: {len(PROBLEM_TEMPLATE.regions)}")
