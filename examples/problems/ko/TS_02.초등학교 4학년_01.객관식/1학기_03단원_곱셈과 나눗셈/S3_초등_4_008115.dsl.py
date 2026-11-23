"""ModuMath Problem DSL: 몫과 나머지의 합이 가장 작은 나눗셈 찾기 (S3_초등_4_008115)"""

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
PROBLEM_ID = "S3_초등_4_008115"
PROBLEM_TITLE = "몫과 나머지의 합이 가장 작은 식의 기호 선택하기"


# ==============================================================================
# 2. 정답 및 오답 진단 정의 (Answer & Diagnostic Key)
# ==============================================================================
ANSWER = {
    "value": "ㄹ",
    "answer_index": 3,
    "unit": "",
    "values": ["ㄹ"],
    "choices": [
        "ㄱ",
        "ㄴ",
        "ㄷ",
        "ㄹ",
    ],
    "blanks": [],
    "answer_key": [
        {
            "slot_id": "slot.choice.option_3",
            "value": "ㄹ",
            "diagnostics": [
                {
                    "id": "diag.sum_giyeok",
                    "condition": "answer_equals_giyeok",
                    "concept": "나눗셈의 몫과 나머지",
                    "reason": "ㄱ의 몫과 나머지의 합(21+6=27)이 ㄹ(12+3=15)보다 큼",
                    "feedback": "ㄱ. 846 ÷ 40 = 21···6 → 21 + 6 = 27, ㄹ. 123 ÷ 10 = 12···3 → 12 + 3 = 15입니다.",
                },
                {
                    "id": "diag.chose_smallest_quotient",
                    "condition": "answer_equals_nieun",
                    "concept": "나눗셈의 몫과 나머지",
                    "reason": "몫이 가장 작은 ㄴ(6)을 선택했으나 나머지가 37로 합이 43임",
                    "feedback": "ㄴ은 몫은 6으로 작지만 나머지가 37이어서 합이 43입니다. 몫과 나머지의 합이 가장 작은 것은 ㄹ(15)입니다.",
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
    "problem_type": "multiple_choice_division_quotient_remainder_sum",
    "metadata": {
        "school": "초등학교",
        "grade": 4,
        "semester": "1학기",
        "chapter": "03단원_곱셈과 나눗셈",
        "difficulty": "중",
    },
    "entities": {
        "opt_0": {"label": "ㄱ", "expr": "846 ÷ 40", "quotient": 21, "remainder": 6, "sum": 27},
        "opt_1": {"label": "ㄴ", "expr": "397 ÷ 60", "quotient": 6, "remainder": 37, "sum": 43},
        "opt_2": {"label": "ㄷ", "expr": "524 ÷ 70", "quotient": 7, "remainder": 34, "sum": 41},
        "opt_3": {"label": "ㄹ", "expr": "123 ÷ 10", "quotient": 12, "remainder": 3, "sum": 15},
    },
    "relations": [
        {
            "type": "minimum_sum",
            "correct_entity": "opt_3",
            "distractors": ["opt_0", "opt_1", "opt_2"],
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
        text="23. 다음 계산에서 몫과 나머지의 합이 가장 작은 것의 기호를 선택하세요.",
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
    item_0 = TextSlot(id="slot.diagram.item_0", prompt="", text="ㄱ. 846 ÷ 40", x=290, y=108, font_size=22, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center")
    item_1 = TextSlot(id="slot.diagram.item_1", prompt="", text="ㄴ. 397 ÷ 60", x=560, y=108, font_size=22, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center")
    item_2 = TextSlot(id="slot.diagram.item_2", prompt="", text="ㄷ. 524 ÷ 70", x=290, y=154, font_size=22, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center")
    item_3 = TextSlot(id="slot.diagram.item_3", prompt="", text="ㄹ. 123 ÷ 10", x=560, y=154, font_size=22, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center")

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
        {"ref": "opt_0", "value": "846 ÷ 40"},
        {"ref": "opt_1", "value": "397 ÷ 60"},
        {"ref": "opt_2", "value": "524 ÷ 70"},
        {"ref": "opt_3", "value": "123 ÷ 10"},
    ],
    "target": {"ref": "slot.choice.option_3", "label": "몫과 나머지의 합이 가장 작은 것", "unit": ""},
    "method": "compute_quotient_remainder_sum",
    "steps": [
        {
            "id": "compare_sums",
            "expr": "ㄱ:27, ㄴ:43, ㄷ:41, ㄹ:15",
            "explanation": "123 ÷ 10 = 12···3이므로 합이 12 + 3 = 15로 가장 작습니다.",
            "value": "ㄹ",
        },
    ],
    "answer": ANSWER,
}


if __name__ == "__main__":
    print(f"[{PROBLEM_TEMPLATE.id}] 템플릿 컴파일 성공!")
    print(f"- 제목: {PROBLEM_TEMPLATE.title}")
    print(f"- 캔버스: {PROBLEM_TEMPLATE.canvas.width} x {PROBLEM_TEMPLATE.canvas.height}")
    print(f"- 구역 수: {len(PROBLEM_TEMPLATE.regions)}")
