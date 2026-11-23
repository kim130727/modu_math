"""ModuMath Problem DSL: 덧셈 수 배열표의 규칙 찾기 (S3_초등_4_008496)"""

from __future__ import annotations

from modu_math.dsl import (
    Canvas,
    CircleSlot,
    PolygonSlot,
    ProblemTemplate,
    RectSlot,
    Region,
    TextBoxSlot,
    TextSlot,
)


# ==============================================================================
# 1. 문제 식별자 및 제목 (Problem Metadata)
# ==============================================================================
PROBLEM_ID = "S3_초등_4_008496"
PROBLEM_TITLE = "수의 배열에서 일의 자리 숫자 규칙 찾기"


# ==============================================================================
# 2. 정답 및 오답 진단 정의 (Answer & Diagnostic Key)
# ==============================================================================
ANSWER = {
    "value": "일",
    "answer_index": 1,
    "unit": "",
    "values": ["일"],
    "choices": [
        "십",
        "일",
    ],
    "blanks": [],
    "answer_key": [
        {
            "slot_id": "slot.choice.option_1",
            "value": "일",
            "diagnostics": [
                {
                    "id": "diag.wrong_digit_place",
                    "condition": "answer_equals_ten",
                    "concept": "수 배열의 규칙",
                    "reason": "101 + 11 = 112에서 2가 일의 자리 숫자임을 십의 자리와 혼동함",
                    "feedback": "101 + 11 = 112에서 2는 일의 자리 숫자입니다. 덧셈의 결과에서 일의 자리 수만 쓰는 규칙입니다.",
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
        "example": {"label": "예시", "expr": "101 + 11 = 112", "written_digit": 2},
        "rule_place": {"label": "쓰는 자릿수", "value": "일"},
    },
    "relations": [
        {
            "type": "modular_addition_table",
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
        text="22. 수의 배열에서 규칙을 찾아 알맞은 말을 선택하세요.",
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
    cols = ["+", "101", "102", "103", "104", "105"]
    rows = ["11", "12", "13", "14", "15"]
    for c_idx, c_lbl in enumerate(cols):
        cx = 76 + c_idx * 72
        diagram_slots.append(RectSlot(id=f"slot.diagram.h_{c_idx}", prompt="", x=cx, y=76, width=72, height=30, fill="#ffedd5", stroke="#f59e0b", stroke_width=1))
        diagram_slots.append(TextSlot(id=f"slot.diagram.ht_{c_idx}", prompt="", text=c_lbl, x=cx + 36, y=82, font_size=16, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center"))

    for r_idx, r_lbl in enumerate(rows):
        ry = 106 + r_idx * 28
        diagram_slots.append(RectSlot(id=f"slot.diagram.r_{r_idx}", prompt="", x=76, y=ry, width=72, height=28, fill="#ffedd5", stroke="#f59e0b", stroke_width=1))
        diagram_slots.append(TextSlot(id=f"slot.diagram.rt_{r_idx}", prompt="", text=r_lbl, x=112, y=ry + 5, font_size=16, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center"))
        for c_idx in range(1, 6):
            cx = 76 + c_idx * 72
            diagram_slots.append(RectSlot(id=f"slot.diagram.c_{r_idx}_{c_idx}", prompt="", x=cx, y=ry, width=72, height=28, fill="#ffffff", stroke="#f59e0b", stroke_width=1))
            if r_idx == 3 and c_idx == 4:
                diagram_slots.append(PolygonSlot(id="slot.diagram.tri_mark", prompt="", points=[(cx + 36, ry + 6), (cx + 44, ry + 22), (cx + 28, ry + 22)], fill="#a855f7", stroke="#a855f7", stroke_width=1))
            else:
                val = (int(cols[c_idx]) + int(r_lbl)) % 10
                diagram_slots.append(TextSlot(id=f"slot.diagram.ct_{r_idx}_{c_idx}", prompt="", text=str(val), x=cx + 36, y=ry + 5, font_size=16, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center"))

    diagram_slots.extend([
        CircleSlot(id="slot.diagram.girl_head", prompt="", cx=586, cy=148, r=24, fill="#fde68a", stroke="#78350f", stroke_width=1.5),
        RectSlot(id="slot.diagram.bubble", prompt="", x=636, y=104, width=200, height=76, fill="#ffffff", stroke="#374151", stroke_width=1.3, rx=22, ry=22),
        TextBoxSlot(id="slot.diagram.bubble_txt", prompt="", text="101+11=112이면\n2를 쓰는 거야.", x=646, y=114, width=180, height=56, font_size=16, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center", valign="middle", line_height=1.35),
        RectSlot(id="slot.diagram.rule_box", prompt="", x=116, y=260, width=654, height=78, fill="#ffffff", stroke="#65a30d", stroke_width=1.6),
        TextSlot(id="slot.diagram.rule_1", prompt="", text="가로줄에 있는 세 자리 수와 세로줄에 있는 두 자리 수의", x=443, y=272, font_size=19, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center"),
    ])

    c_pre = TextSlot(id="slot.choice.pre", prompt="", text="덧셈의 결과에서 (", x=250, y=306, font_size=19, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center")
    c0 = TextSlot(id="slot.choice.option_0", prompt="", text="십", x=352, y=306, font_size=19, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center", interaction={"type": "choice", "role": "answer", "choice_index": 0, "value": "십", "group_id": "slot.choice.group", "include_in_submission": True})
    cm = TextSlot(id="slot.choice.cm", prompt="", text=",", x=376, y=306, font_size=19, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center")
    c1 = TextSlot(id="slot.choice.option_1", prompt="", text="일", x=400, y=306, font_size=19, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center", interaction={"type": "choice", "role": "answer", "choice_index": 1, "value": "일", "group_id": "slot.choice.group", "include_in_submission": True})
    c_suf = TextSlot(id="slot.choice.suf", prompt="", text=")의 자리 수만 쓰는 규칙입니다.", x=562, y=306, font_size=19, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center")

    choice_slots = (c_pre, c0, cm, c1, c_suf)

    return ProblemTemplate(
        id=PROBLEM_ID,
        title=PROBLEM_TITLE,
        canvas=Canvas(
            width=886,
            height=364,
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
        {"ref": "example", "value": "101 + 11 = 112 -> 2"},
    ],
    "target": {"ref": "slot.choice.option_1", "label": "규칙에 해당하는 자릿수", "unit": ""},
    "method": "pattern_observation",
    "steps": [
        {
            "id": "identify_ones_digit",
            "expr": "112 -> 2 (일의 자리)",
            "explanation": "덧셈 결과의 일의 자리 수만 쓰는 규칙입니다.",
            "value": "일",
        },
    ],
    "answer": ANSWER,
}


if __name__ == "__main__":
    print(f"[{PROBLEM_TEMPLATE.id}] 템플릿 컴파일 성공!")
    print(f"- 제목: {PROBLEM_TEMPLATE.title}")
    print(f"- 캔버스: {PROBLEM_TEMPLATE.canvas.width} x {PROBLEM_TEMPLATE.canvas.height}")
    print(f"- 구역 수: {len(PROBLEM_TEMPLATE.regions)}")
