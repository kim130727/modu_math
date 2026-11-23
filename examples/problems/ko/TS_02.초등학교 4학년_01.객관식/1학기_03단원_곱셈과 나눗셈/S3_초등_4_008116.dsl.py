"""ModuMath Problem DSL: 몫과 나머지의 차가 가장 큰 나눗셈 찾기 (S3_초등_4_008116)"""

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
PROBLEM_ID = "S3_초등_4_008116"
PROBLEM_TITLE = "몫과 나머지의 차가 가장 큰 식 선택하기"


# ==============================================================================
# 2. 정답 및 오답 진단 정의 (Answer & Diagnostic Key)
# ==============================================================================
ANSWER = {
    "value": "ㄷ",
    "answer_index": 2,
    "unit": "",
    "values": ["ㄷ"],
    "choices": [
        "ㄱ",
        "ㄴ",
        "ㄷ",
        "ㄹ",
    ],
    "blanks": [],
    "answer_key": [
        {
            "slot_id": "slot.choice.option_2",
            "value": "ㄷ",
            "diagnostics": [
                {
                    "id": "diag.diff_giyeok",
                    "condition": "answer_equals_giyeok",
                    "concept": "나눗셈의 몫과 나머지",
                    "reason": "ㄱ의 차(27-19=8)가 ㄷ의 차(14-1=13)보다 작음",
                    "feedback": "ㄱ. 806 ÷ 41 = 19···27 (차: 8), ㄷ. 169 ÷ 12 = 14···1 (차: 13)입니다.",
                },
                {
                    "id": "diag.diff_rieul",
                    "condition": "answer_equals_rieul",
                    "concept": "나눗셈의 몫과 나머지",
                    "reason": "ㄹ의 차(18-8=10)가 ㄷ의 차(14-1=13)보다 작음",
                    "feedback": "ㄹ. 594 ÷ 72 = 8···18 (차: 10), ㄷ. 169 ÷ 12 = 14···1 (차: 13)입니다.",
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
    "problem_type": "multiple_choice_division_quotient_remainder_diff",
    "metadata": {
        "school": "초등학교",
        "grade": 4,
        "semester": "1학기",
        "chapter": "03단원_곱셈과 나눗셈",
        "difficulty": "중",
    },
    "entities": {
        "opt_0": {"label": "ㄱ", "expr": "806 ÷ 41", "quotient": 19, "remainder": 27, "diff": 8},
        "opt_1": {"label": "ㄴ", "expr": "319 ÷ 18", "quotient": 17, "remainder": 13, "diff": 4},
        "opt_2": {"label": "ㄷ", "expr": "169 ÷ 12", "quotient": 14, "remainder": 1, "diff": 13},
        "opt_3": {"label": "ㄹ", "expr": "594 ÷ 72", "quotient": 8, "remainder": 18, "diff": 10},
    },
    "relations": [
        {
            "type": "maximum_difference",
            "correct_entity": "opt_2",
            "distractors": ["opt_0", "opt_1", "opt_3"],
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
        text="24. 다음 계산에서 몫과 나머지의 차가 가장 큰 것은 어느 것일까요?",
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

    box_bg = RectSlot(id="slot.diagram.box_bg", prompt="", x=176, y=88, width=534, height=116, fill="#ffffff", stroke="#6b7280", stroke_width=1.5)
    item_0 = TextSlot(id="slot.diagram.item_0", prompt="", text="ㄱ. 806 ÷ 41", x=290, y=108, font_size=22, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center")
    item_1 = TextSlot(id="slot.diagram.item_1", prompt="", text="ㄴ. 319 ÷ 18", x=560, y=108, font_size=22, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center")
    item_2 = TextSlot(id="slot.diagram.item_2", prompt="", text="ㄷ. 169 ÷ 12", x=290, y=154, font_size=22, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center")
    item_3 = TextSlot(id="slot.diagram.item_3", prompt="", text="ㄹ. 594 ÷ 72", x=560, y=154, font_size=22, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center")

    paren_left = TextSlot(id="slot.choice.paren_left", prompt="", text="(", x=516, y=224, font_size=24, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center")
    labels = ["ㄱ", "ㄴ", "ㄷ", "ㄹ"]
    choice_slots = []
    comma_slots = []
    for idx, label in enumerate(labels):
        cx = 546 + idx * 46
        choice_slots.append(
            TextSlot(
                id=f"slot.choice.option_{idx}",
                prompt="",
                text=label,
                x=cx,
                y=224,
                font_size=22,
                font_family='"Noto Sans KR", sans-serif',
                fill="#111827",
                align="center",
                interaction={"type": "choice", "role": "answer", "choice_index": idx, "value": label, "group_id": "slot.choice.group", "include_in_submission": True},
            )
        )
        if idx < 3:
            comma_slots.append(TextSlot(id=f"slot.choice.c_{idx}", prompt="", text=",", x=cx + 23, y=224, font_size=22, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center"))
    paren_right = TextSlot(id="slot.choice.paren_right", prompt="", text=")", x=714, y=224, font_size=24, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center")

    return ProblemTemplate(
        id=PROBLEM_ID,
        title=PROBLEM_TITLE,
        canvas=Canvas(
            width=886,
            height=280,
            coordinate_mode="logical",
        ),
        regions=(
            Region(id="region.stem", role="stem", flow="absolute", slot_ids=("slot.stem.question",)),
            Region(
                id="region.diagram",
                role="diagram",
                flow="absolute",
                slot_ids=("slot.diagram.box_bg", "slot.diagram.item_0", "slot.diagram.item_1", "slot.diagram.item_2", "slot.diagram.item_3"),
            ),
            Region(
                id="region.choices",
                role="choices",
                flow="absolute",
                slot_ids=(
                    "slot.choice.paren_left",
                    *(s.id for s in choice_slots),
                    *(s.id for s in comma_slots),
                    "slot.choice.paren_right",
                ),
            ),
        ),
        slots=(
            stem_text_slot,
            box_bg,
            item_0,
            item_1,
            item_2,
            item_3,
            paren_left,
            *choice_slots,
            *comma_slots,
            paren_right,
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
        {"ref": "opt_0", "value": "806 ÷ 41"},
        {"ref": "opt_1", "value": "319 ÷ 18"},
        {"ref": "opt_2", "value": "169 ÷ 12"},
        {"ref": "opt_3", "value": "594 ÷ 72"},
    ],
    "target": {"ref": "slot.choice.option_2", "label": "몫과 나머지의 차가 가장 큰 것", "unit": ""},
    "method": "compute_quotient_remainder_diff",
    "steps": [
        {
            "id": "compare_diffs",
            "expr": "ㄱ:8, ㄴ:4, ㄷ:13, ㄹ:10",
            "explanation": "169 ÷ 12 = 14···1이므로 차가 14 - 1 = 13으로 가장 큽니다.",
            "value": "ㄷ",
        },
    ],
    "answer": ANSWER,
}


if __name__ == "__main__":
    print(f"[{PROBLEM_TEMPLATE.id}] 템플릿 컴파일 성공!")
    print(f"- 제목: {PROBLEM_TEMPLATE.title}")
    print(f"- 캔버스: {PROBLEM_TEMPLATE.canvas.width} x {PROBLEM_TEMPLATE.canvas.height}")
    print(f"- 구역 수: {len(PROBLEM_TEMPLATE.regions)}")
