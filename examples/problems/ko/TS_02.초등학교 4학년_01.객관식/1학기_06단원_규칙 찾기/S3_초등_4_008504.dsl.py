"""ModuMath Problem DSL: 상자 배열의 규칙을 바르게 말한 사람 찾기 (S3_초등_4_008504)"""

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
PROBLEM_ID = "S3_초등_4_008504"
PROBLEM_TITLE = "상자의 배열 규칙을 바르게 설명한 사람 선택하기"


# ==============================================================================
# 2. 정답 및 오답 진단 정의 (Answer & Diagnostic Key)
# ==============================================================================
ANSWER = {
    "value": "주영",
    "answer_index": 0,
    "unit": "",
    "values": ["주영"],
    "choices": [
        "주영",
        "민서",
    ],
    "blanks": [],
    "answer_key": [
        {
            "slot_id": "slot.choice.option_0",
            "value": "주영",
            "diagnostics": [
                {
                    "id": "diag.chose_increasing_step",
                    "condition": "answer_equals_minseo",
                    "concept": "도형 배열의 규칙",
                    "reason": "2개씩 일정하게 늘어나는 규칙을 1개, 2개, 3개씩 늘어나는 규칙으로 오인함",
                    "feedback": "상자의 개수는 1개 → 3개 → 5개 → 7개로 매번 2개씩 늘어납니다. 따라서 바르게 말한 사람은 주영입니다.",
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
    "problem_type": "multiple_choice_shape_pattern",
    "metadata": {
        "school": "초등학교",
        "grade": 4,
        "semester": "1학기",
        "chapter": "06단원_규칙 찾기",
        "difficulty": "하",
    },
    "entities": {
        "juyeong": {"label": "주영", "statement": "1개에서 시작하여 2개씩 늘어나.", "is_correct": True},
        "minseo": {"label": "민서", "statement": "1개에서 시작하여 1개, 2개, 3개……가 늘어나.", "is_correct": False},
    },
    "relations": [
        {
            "type": "sequence_rule_verification",
            "sequence": [1, 3, 5, 7],
            "correct_entity": "juyeong",
            "distractor": "minseo",
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
        text="31. 상자의 배열의 규칙을 바르게 말한 사람의 이름을 선택하세요.",
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
    titles = ["첫째", "둘째", "셋째", "넷째"]
    xs = [196, 356, 536, 736]
    counts = [(1, 0), (2, 1), (3, 2), (4, 3)]  # (아랫줄, 윗줄)
    bw, bh = 28, 22
    for idx, (t, cx, (bot_n, top_n)) in enumerate(zip(titles, xs, counts)):
        diagram_slots.append(TextSlot(id=f"slot.diagram.t_{idx}", prompt="", text=t, x=cx, y=72, font_size=16, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center"))
        bx0 = cx - (bot_n * bw) // 2
        for i in range(bot_n):
            diagram_slots.append(RectSlot(id=f"slot.diagram.b_{idx}_{i}", prompt="", x=bx0 + i * bw, y=126, width=bw, height=bh, fill="#d6c2a8", stroke="#78350f", stroke_width=1.2))
        tx0 = cx - (top_n * bw) // 2
        for i in range(top_n):
            diagram_slots.append(RectSlot(id=f"slot.diagram.u_{idx}_{i}", prompt="", x=tx0 + i * bw, y=104, width=bw, height=bh, fill="#d6c2a8", stroke="#78350f", stroke_width=1.2))

    # 주영 (왼쪽)
    diagram_slots.extend([
        RectSlot(id="slot.diagram.jy_bubble", prompt="", x=176, y=164, width=250, height=76, fill="#ffffff", stroke="#374151", stroke_width=1.3, rx=22, ry=22),
        TextBoxSlot(id="slot.diagram.jy_txt", prompt="", text="상자의 개수가 1개에서\n시작하여 2개씩 늘어나.", x=186, y=172, width=230, height=60, font_size=16, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center", valign="middle", line_height=1.35),
        CircleSlot(id="slot.diagram.jy_head", prompt="", cx=346, cy=274, r=24, fill="#fde68a", stroke="#78350f", stroke_width=1.5),
        RectSlot(id="slot.diagram.jy_badge", prompt="", x=310, y=308, width=72, height=30, fill="#fff1f2", stroke="#f43f5e", stroke_width=1.2, rx=6, ry=6),
        TextSlot(id="slot.diagram.jy_name", prompt="", text="주영", x=346, y=312, font_size=17, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center"),
    ])

    # 민서 (오른쪽)
    diagram_slots.extend([
        RectSlot(id="slot.diagram.ms_bubble", prompt="", x=476, y=164, width=250, height=76, fill="#ffffff", stroke="#374151", stroke_width=1.3, rx=22, ry=22),
        TextBoxSlot(id="slot.diagram.ms_txt", prompt="", text="상자의 개수가 1개에서\n시작하여 1개, 2개, 3개……가 늘어나.", x=486, y=172, width=230, height=60, font_size=15, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center", valign="middle", line_height=1.35),
        CircleSlot(id="slot.diagram.ms_head", prompt="", cx=600, cy=274, r=24, fill="#fde68a", stroke="#78350f", stroke_width=1.5),
        RectSlot(id="slot.diagram.ms_badge", prompt="", x=564, y=308, width=72, height=30, fill="#fff1f2", stroke="#f43f5e", stroke_width=1.2, rx=6, ry=6),
        TextSlot(id="slot.diagram.ms_name", prompt="", text="민서", x=600, y=312, font_size=17, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center"),
    ])

    p_l = TextSlot(id="slot.choice.p_l", prompt="", text="(", x=376, y=354, font_size=22, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center")
    c0 = TextSlot(id="slot.choice.option_0", prompt="", text="주영", x=422, y=354, font_size=20, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center", interaction={"type": "choice", "role": "answer", "choice_index": 0, "value": "주영", "group_id": "slot.choice.group", "include_in_submission": True})
    cm = TextSlot(id="slot.choice.cm", prompt="", text=",", x=456, y=354, font_size=20, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center")
    c1 = TextSlot(id="slot.choice.option_1", prompt="", text="민서", x=490, y=354, font_size=20, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center", interaction={"type": "choice", "role": "answer", "choice_index": 1, "value": "민서", "group_id": "slot.choice.group", "include_in_submission": True})
    p_r = TextSlot(id="slot.choice.p_r", prompt="", text=")", x=536, y=354, font_size=22, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center")

    choice_slots = (p_l, c0, cm, c1, p_r)

    return ProblemTemplate(
        id=PROBLEM_ID,
        title=PROBLEM_TITLE,
        canvas=Canvas(
            width=886,
            height=400,
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
        {"ref": "juyeong", "value": "2개씩 늘어남"},
        {"ref": "minseo", "value": "1개, 2개, 3개씩 늘어남"},
    ],
    "target": {"ref": "slot.choice.option_0", "label": "바르게 말한 사람", "unit": ""},
    "method": "sequence_rule_verification",
    "steps": [
        {
            "id": "verify_sequence",
            "expr": "1 -> 3 -> 5 -> 7 (+2)",
            "explanation": "상자의 개수가 1개에서 시작하여 2개씩 늘어나므로 주영이가 바르게 말했습니다.",
            "value": "주영",
        },
    ],
    "answer": ANSWER,
}


if __name__ == "__main__":
    print(f"[{PROBLEM_TEMPLATE.id}] 템플릿 컴파일 성공!")
    print(f"- 제목: {PROBLEM_TEMPLATE.title}")
    print(f"- 캔버스: {PROBLEM_TEMPLATE.canvas.width} x {PROBLEM_TEMPLATE.canvas.height}")
    print(f"- 구역 수: {len(PROBLEM_TEMPLATE.regions)}")
