"""ModuMath Problem DSL: 네 자리 수와 두 자리 수 배열표의 규칙 (S3_초등_4_008502)"""

from __future__ import annotations

from modu_math.dsl import (
    Canvas,
    CircleSlot,
    ProblemTemplate,
    RectSlot,
    Region,
    TextBoxSlot,
    TextSlot,
)


# ==============================================================================
# 1. 문제 식별자 및 제목 (Problem Metadata)
# ==============================================================================
PROBLEM_ID = "S3_초등_4_008502"
PROBLEM_TITLE = "수 배열표에서 덧셈과 일의 자리 규칙 찾기"


# ==============================================================================
# 2. 정답 및 오답 진단 정의 (Answer & Diagnostic Key)
# ==============================================================================
ANSWER = {
    "value": ["덧셈", "일"],
    "unit": "",
    "values": ["덧셈", "일"],
    "choices": [
        "덧셈",
        "뺄셈",
        "십",
        "일",
    ],
    "blanks": [],
    "answer_key": [
        {
            "slot_id": "slot.choice.g1_option_0",
            "value": "덧셈",
            "diagnostics": [
                {
                    "id": "diag.wrong_operation",
                    "condition": "answer_equals_subtraction",
                    "concept": "수 배열의 규칙",
                    "reason": "덧셈을 뺄셈으로 오인함",
                    "feedback": "1001 + 11 = 1012, 1002 + 11 = 1013이므로 덧셈의 결과입니다.",
                },
            ],
        },
        {
            "slot_id": "slot.choice.g2_option_1",
            "value": "일",
            "diagnostics": [
                {
                    "id": "diag.wrong_digit",
                    "condition": "answer_equals_ten",
                    "concept": "수 배열의 규칙",
                    "reason": "일의 자리 숫자를 십의 자리 숫자로 혼동함",
                    "feedback": "1001 + 11 = 1012에서 표에 적힌 수 2는 일의 자리 숫자입니다.",
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
    "problem_type": "multiple_choice_pattern_table",
    "metadata": {
        "school": "초등학교",
        "grade": 4,
        "semester": "1학기",
        "chapter": "06단원_규칙 찾기",
        "difficulty": "하",
    },
    "entities": {
        "operation": {"label": "연산", "value": "덧셈"},
        "place": {"label": "자릿수", "value": "일"},
    },
    "relations": [
        {
            "type": "modular_addition_table",
            "operation": "덧셈",
            "place": "일",
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
        text="28. 덧셈을 이용한 다음 수 배열표를 보고 알맞은 말을 선택하세요.",
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

    diagram_slots = []
    cols = ["", "1001", "1002", "1003", "1004", "1005"]
    rows = ["11", "12", "13", "14"]
    for c_idx, c_lbl in enumerate(cols):
        cx = 173 + c_idx * 90
        diagram_slots.append(RectSlot(id=f"slot.diagram.h_{c_idx}", prompt="", x=cx, y=76, width=90, height=30, fill="#bae6fd", stroke="#0284c7", stroke_width=1))
        if c_lbl:
            diagram_slots.append(TextSlot(id=f"slot.diagram.ht_{c_idx}", prompt="", text=c_lbl, x=cx + 45, y=82, font_size=16, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center"))

    for r_idx, r_lbl in enumerate(rows):
        ry = 106 + r_idx * 30
        diagram_slots.append(RectSlot(id=f"slot.diagram.r_{r_idx}", prompt="", x=173, y=ry, width=90, height=30, fill="#bae6fd", stroke="#0284c7", stroke_width=1))
        diagram_slots.append(TextSlot(id=f"slot.diagram.rt_{r_idx}", prompt="", text=r_lbl, x=218, y=ry + 6, font_size=16, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center"))
        for c_idx in range(1, 6):
            cx = 173 + c_idx * 90
            diagram_slots.append(RectSlot(id=f"slot.diagram.c_{r_idx}_{c_idx}", prompt="", x=cx, y=ry, width=90, height=30, fill="#ffffff", stroke="#0284c7", stroke_width=1))
            if r_idx == 1 and c_idx == 2:
                diagram_slots.append(RectSlot(id="slot.diagram.sq_mark", prompt="", x=cx + 37, y=ry + 7, width=16, height=16, fill="#16a34a", stroke="#16a34a", stroke_width=1))
            elif r_idx == 3 and c_idx == 3:
                diagram_slots.append(CircleSlot(id="slot.diagram.dot_mark", prompt="", cx=cx + 45, cy=ry + 15, r=8, fill="#6d28d9", stroke="#6d28d9", stroke_width=1))
            else:
                val = (int(cols[c_idx]) + int(r_lbl)) % 10
                diagram_slots.append(TextSlot(id=f"slot.diagram.ct_{r_idx}_{c_idx}", prompt="", text=str(val), x=cx + 45, y=ry + 6, font_size=16, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center"))

    diagram_slots.extend([
        RectSlot(id="slot.diagram.rule_badge", prompt="", x=96, y=242, width=54, height=28, fill="#ddd6fe", stroke="#c4b5fd", stroke_width=1),
        TextSlot(id="slot.diagram.rule_lbl", prompt="", text="규칙", x=123, y=246, font_size=17, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center"),
    ])

    g1_pre = TextSlot(id="slot.choice.g1_pre", prompt="", text="가로줄에 있는 네 자리 수와 세로줄에 있는 두 자리 수의 (", x=390, y=246, font_size=19, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center")
    g1_0 = TextSlot(id="slot.choice.g1_option_0", prompt="", text="덧셈", x=654, y=246, font_size=19, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center", interaction={"type": "choice", "role": "answer", "choice_index": 0, "value": "덧셈", "group_id": "slot.choice.group_1", "include_in_submission": True})
    g1_c = TextSlot(id="slot.choice.g1_c", prompt="", text=",", x=686, y=246, font_size=19, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center")
    g1_1 = TextSlot(id="slot.choice.g1_option_1", prompt="", text="뺄셈", x=718, y=246, font_size=19, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center", interaction={"type": "choice", "role": "answer", "choice_index": 1, "value": "뺄셈", "group_id": "slot.choice.group_1", "include_in_submission": True})
    g1_suf = TextSlot(id="slot.choice.g1_suf", prompt="", text=")의 결과에서", x=792, y=246, font_size=19, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center")

    g2_pre = TextSlot(id="slot.choice.g2_pre", prompt="", text="(", x=174, y=288, font_size=19, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center")
    g2_0 = TextSlot(id="slot.choice.g2_option_0", prompt="", text="십", x=204, y=288, font_size=19, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center", interaction={"type": "choice", "role": "answer", "choice_index": 0, "value": "십", "group_id": "slot.choice.group_2", "include_in_submission": True})
    g2_c = TextSlot(id="slot.choice.g2_c", prompt="", text=",", x=228, y=288, font_size=19, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center")
    g2_1 = TextSlot(id="slot.choice.g2_option_1", prompt="", text="일", x=252, y=288, font_size=19, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center", interaction={"type": "choice", "role": "answer", "choice_index": 1, "value": "일", "group_id": "slot.choice.group_2", "include_in_submission": True})
    g2_suf = TextSlot(id="slot.choice.g2_suf", prompt="", text=")의 자리 숫자만 쓴 것입니다.", x=410, y=288, font_size=19, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center")

    choice_slots = (g1_pre, g1_0, g1_c, g1_1, g1_suf, g2_pre, g2_0, g2_c, g2_1, g2_suf)

    return ProblemTemplate(
        id=PROBLEM_ID,
        title=PROBLEM_TITLE,
        canvas=Canvas(
            width=886,
            height=340,
            coordinate_mode="logical",
        ),
        regions=(
            Region(id="region.stem", role="stem", flow="absolute", slot_ids=("slot.stem.question",)),
            Region(id="region.diagram", role="diagram", flow="absolute", slot_ids=tuple(s.id for s in diagram_slots)),
            Region(id="region.choices", role="choices", flow="absolute", slot_ids=tuple(s.id for s in choice_slots)),
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
        {"ref": "operation", "value": "덧셈"},
        {"ref": "place", "value": "일"},
    ],
    "target": {"ref": "slot.choice.g2_option_1", "label": "연산과 자릿수 규칙", "unit": ""},
    "method": "pattern_observation",
    "steps": [
        {
            "id": "find_rule",
            "expr": "1001 + 11 = 1012 -> 2",
            "explanation": "두 수의 덧셈 결과에서 일의 자리 숫자만 쓴 것입니다.",
            "value": ["덧셈", "일"],
        },
    ],
    "answer": ANSWER,
}


if __name__ == "__main__":
    print(f"[{PROBLEM_TEMPLATE.id}] 템플릿 컴파일 성공!")
    print(f"- 제목: {PROBLEM_TEMPLATE.title}")
    print(f"- 캔버스: {PROBLEM_TEMPLATE.canvas.width} x {PROBLEM_TEMPLATE.canvas.height}")
    print(f"- 구역 수: {len(PROBLEM_TEMPLATE.regions)}")
