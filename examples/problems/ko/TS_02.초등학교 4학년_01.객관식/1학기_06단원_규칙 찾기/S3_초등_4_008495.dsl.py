"""ModuMath Problem DSL: 극장 좌석표에서 규칙 찾기 (S3_초등_4_008495)"""

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
PROBLEM_ID = "S3_초등_4_008495"
PROBLEM_TITLE = "극장 좌석표의 규칙을 찾아 빈칸 좌석 번호 구하기"


# ==============================================================================
# 2. 정답 및 오답 진단 정의 (Answer & Diagnostic Key)
# ==============================================================================
ANSWER = {
    "value": ["1", "D5"],
    "unit": "",
    "values": ["1", "D5"],
    "choices": [
        "0",
        "1",
        "10",
        "C6",
        "D5",
        "D6",
    ],
    "blanks": [],
    "answer_key": [
        {
            "slot_id": "slot.choice.g1_option_1",
            "value": "1",
            "diagnostics": [
                {
                    "id": "diag.wrong_horizontal_step",
                    "condition": "answer_equals_0_or_10",
                    "concept": "수 배열의 규칙",
                    "reason": "가로 방향 숫자의 증가량(1)을 잘못 파악함",
                    "feedback": "A1, A2, A3, ... 순서이므로 가로(→)로 숫자가 1씩 커집니다.",
                },
            ],
        },
        {
            "slot_id": "slot.choice.g2_option_1",
            "value": "D5",
            "diagnostics": [
                {
                    "id": "diag.wrong_seat_code",
                    "condition": "answer_equals_C6_or_D6",
                    "concept": "좌석표 규칙",
                    "reason": "가로와 세로의 위치에 맞는 알파벳과 숫자를 잘못 조합함",
                    "feedback": "D4의 오른쪽(가로 +1)이고 C5의 아래쪽(세로 다음 알파벳)이므로 민재의 좌석 번호는 D5입니다.",
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
        "horizontal_step": {"label": "가로 증가량", "value": 1},
        "target_seat": {"label": "민재의 좌석 번호", "value": "D5"},
    },
    "relations": [
        {
            "type": "grid_pattern",
            "row_rule": "A, B, C, D, E",
            "col_rule": "+1",
            "target": "D5",
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
        text="21. 극장 좌석표에서 규칙을 찾아 민재의 좌석 번호를 알아보려고 합니다. 알맞은 것을 선택하세요.",
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

    diagram_slots = [
        RectSlot(id="slot.diagram.board_bg", prompt="", x=156, y=82, width=338, height=174, fill="#cbd5e1", stroke="#64748b", stroke_width=1.5, rx=4, ry=4),
        TextSlot(id="slot.diagram.board_title", prompt="", text="○○ 극장 좌석표", x=325, y=88, font_size=16, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center"),
    ]

    rows = ["A", "B", "C", "D", "E"]
    for r_idx, row_lbl in enumerate(rows):
        for c_idx in range(1, 8):
            cx = 166 + (c_idx - 1) * 45
            cy = 114 + r_idx * 27
            diagram_slots.append(RectSlot(id=f"slot.diagram.cell_{r_idx}_{c_idx}", prompt="", x=cx, y=cy, width=45, height=27, fill="#ffffff", stroke="#94a3b8", stroke_width=1))
            if row_lbl == "D" and c_idx == 5:
                diagram_slots.append(RectSlot(id="slot.diagram.target_mark", prompt="", x=cx + 13, y=cy + 4, width=18, height=18, fill="#dc2626", stroke="#dc2626", stroke_width=1))
            else:
                diagram_slots.append(TextSlot(id=f"slot.diagram.ctext_{r_idx}_{c_idx}", prompt="", text=f"{row_lbl}{c_idx}", x=cx + 22.5, y=cy + 5, font_size=14, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center"))

    diagram_slots.extend([
        CircleSlot(id="slot.diagram.boy_head", prompt="", cx=586, cy=148, r=24, fill="#fde68a", stroke="#78350f", stroke_width=1.5),
        RectSlot(id="slot.diagram.bubble", prompt="", x=626, y=84, width=124, height=62, fill="#ffffff", stroke="#374151", stroke_width=1.3, rx=22, ry=22),
        TextBoxSlot(id="slot.diagram.bubble_txt", prompt="", text="내 자리는\n어디일까?", x=634, y=90, width=108, height=50, font_size=15, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center", valign="middle", line_height=1.3),
        RectSlot(id="slot.diagram.badge", prompt="", x=552, y=220, width=68, height=30, fill="#fdf2f8", stroke="#ec4899", stroke_width=1.2, rx=6, ry=6),
        TextSlot(id="slot.diagram.badge_txt", prompt="", text="민재", x=586, y=224, font_size=16, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center"),
    ])

    g1_pre = TextSlot(id="slot.choice.g1_pre", prompt="", text="가로(→)로 숫자가 (", x=142, y=274, font_size=19, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center")
    g1_0 = TextSlot(id="slot.choice.g1_option_0", prompt="", text="0", x=246, y=274, font_size=19, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center", interaction={"type": "choice", "role": "answer", "choice_index": 0, "value": "0", "group_id": "slot.choice.group_1", "include_in_submission": True})
    g1_c0 = TextSlot(id="slot.choice.g1_c0", prompt="", text=",", x=266, y=274, font_size=19, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center")
    g1_1 = TextSlot(id="slot.choice.g1_option_1", prompt="", text="1", x=286, y=274, font_size=19, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center", interaction={"type": "choice", "role": "answer", "choice_index": 1, "value": "1", "group_id": "slot.choice.group_1", "include_in_submission": True})
    g1_c1 = TextSlot(id="slot.choice.g1_c1", prompt="", text=",", x=306, y=274, font_size=19, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center")
    g1_2 = TextSlot(id="slot.choice.g1_option_2", prompt="", text="10", x=330, y=274, font_size=19, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center", interaction={"type": "choice", "role": "answer", "choice_index": 2, "value": "10", "group_id": "slot.choice.group_1", "include_in_submission": True})
    g1_suf = TextSlot(id="slot.choice.g1_suf", prompt="", text=")씩 커지고, 세로(↓)로 알파벳이 순서대로 바뀝니다.", x=586, y=274, font_size=19, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center")

    g2_pre = TextSlot(id="slot.choice.g2_pre", prompt="", text="→ 민재의 좌석 번호는 ■ = (", x=292, y=314, font_size=19, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center")
    g2_0 = TextSlot(id="slot.choice.g2_option_0", prompt="", text="C6", x=446, y=314, font_size=19, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center", interaction={"type": "choice", "role": "answer", "choice_index": 0, "value": "C6", "group_id": "slot.choice.group_2", "include_in_submission": True})
    g2_c0 = TextSlot(id="slot.choice.g2_c0", prompt="", text=",", x=474, y=314, font_size=19, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center")
    g2_1 = TextSlot(id="slot.choice.g2_option_1", prompt="", text="D5", x=502, y=314, font_size=19, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center", interaction={"type": "choice", "role": "answer", "choice_index": 1, "value": "D5", "group_id": "slot.choice.group_2", "include_in_submission": True})
    g2_c1 = TextSlot(id="slot.choice.g2_c1", prompt="", text=",", x=530, y=314, font_size=19, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center")
    g2_2 = TextSlot(id="slot.choice.g2_option_2", prompt="", text="D6", x=558, y=314, font_size=19, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center", interaction={"type": "choice", "role": "answer", "choice_index": 2, "value": "D6", "group_id": "slot.choice.group_2", "include_in_submission": True})
    g2_suf = TextSlot(id="slot.choice.g2_suf", prompt="", text=")입니다.", x=614, y=314, font_size=19, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center")

    choice_slots = (g1_pre, g1_0, g1_c0, g1_1, g1_c1, g1_2, g1_suf, g2_pre, g2_0, g2_c0, g2_1, g2_c1, g2_2, g2_suf)

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
        {"ref": "horizontal_step", "value": 1},
    ],
    "target": {"ref": "slot.choice.g2_option_1", "label": "규칙과 좌석 번호", "unit": ""},
    "method": "grid_pattern_deduction",
    "steps": [
        {
            "id": "deduce_seat",
            "expr": "가로 +1, 세로 A->B->C->D => D5",
            "explanation": "가로로 숫자가 1씩 커지고 세로로 알파벳이 순서대로 바뀌므로 민재의 좌석 번호는 D5입니다.",
            "value": ["1", "D5"],
        },
    ],
    "answer": ANSWER,
}


if __name__ == "__main__":
    print(f"[{PROBLEM_TEMPLATE.id}] 템플릿 컴파일 성공!")
    print(f"- 제목: {PROBLEM_TEMPLATE.title}")
    print(f"- 캔버스: {PROBLEM_TEMPLATE.canvas.width} x {PROBLEM_TEMPLATE.canvas.height}")
    print(f"- 구역 수: {len(PROBLEM_TEMPLATE.regions)}")
