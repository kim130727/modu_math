"""ModuMath Problem DSL: 가격이 더 낮은 휴대 전화 선택하기 (S3_초등_4_007951)"""

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
PROBLEM_ID = "S3_초등_4_007951"
PROBLEM_TITLE = "큰 수의 크기 비교를 통해 가격이 더 낮은 휴대 전화 찾기"


# ==============================================================================
# 2. 정답 및 오답 진단 정의 (Answer & Diagnostic Key)
# ==============================================================================
ANSWER = {
    "value": "가",
    "answer_index": 0,
    "unit": "",
    "values": ["가"],
    "choices": [
        "가",
        "나",
    ],
    "blanks": [],
    "answer_key": [
        {
            "slot_id": "slot.choice.option_0",
            "value": "가",
            "diagnostics": [
                {
                    "id": "diag.chose_more_expensive",
                    "condition": "answer_equals_na",
                    "concept": "수의 크기 비교",
                    "reason": "자릿수가 더 많은 1020000원을 더 낮은 가격으로 선택함",
                    "feedback": "865000은 6자리 수이고 1020000은 7자리 수이므로, 865000 < 1020000입니다. 가격이 더 낮은 휴대 전화는 가입니다.",
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
    "problem_type": "multiple_choice_number_comparison",
    "metadata": {
        "school": "초등학교",
        "grade": 4,
        "semester": "1학기",
        "chapter": "01단원_큰 수",
        "difficulty": "하",
    },
    "entities": {
        "phone_ga": {"label": "가", "price": 865000, "unit": "원", "digits": 6},
        "phone_na": {"label": "나", "price": 1020000, "unit": "원", "digits": 7},
    },
    "relations": [
        {
            "type": "less_than",
            "expression": "865000 < 1020000",
            "smaller": "phone_ga",
            "larger": "phone_na",
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
        text="9. 가격이 더 낮은 휴대 전화를 선택하세요.",
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

    # 휴대 전화 '가'
    choice_ga = TextSlot(
        id="slot.choice.option_0",
        prompt="",
        text="가",
        x=265,
        y=96,
        font_size=24,
        font_family='"Noto Sans KR", sans-serif',
        fill="#111827",
        align="center",
        interaction={
            "type": "choice",
            "role": "answer",
            "choice_index": 0,
            "value": "가",
            "group_id": "slot.choice.group",
            "include_in_submission": True,
        },
    )
    phone_ga_body = RectSlot(id="slot.diagram.phone_ga_body", prompt="", x=295, y=88, width=88, height=156, fill="#1f2937", stroke="#111827", stroke_width=2, rx=12, ry=12)
    phone_ga_screen = RectSlot(id="slot.diagram.phone_ga_screen", prompt="", x=303, y=108, width=72, height=112, fill="#ecfccb", stroke="#4b5563", stroke_width=1, rx=4, ry=4)
    phone_ga_time = TextSlot(id="slot.diagram.phone_ga_time", prompt="", text="2:45", x=339, y=120, font_size=18, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center")
    phone_ga_btn = CircleSlot(id="slot.diagram.phone_ga_btn", prompt="", cx=339, cy=232, r=7, fill="#374151", stroke="#9ca3af", stroke_width=1)
    price_ga = TextSlot(id="slot.diagram.price_ga", prompt="", text="865000원", x=339, y=262, font_size=22, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center")

    # 휴대 전화 '나'
    choice_na = TextSlot(
        id="slot.choice.option_1",
        prompt="",
        text="나",
        x=565,
        y=96,
        font_size=24,
        font_family='"Noto Sans KR", sans-serif',
        fill="#111827",
        align="center",
        interaction={
            "type": "choice",
            "role": "answer",
            "choice_index": 1,
            "value": "나",
            "group_id": "slot.choice.group",
            "include_in_submission": True,
        },
    )
    phone_na_body = RectSlot(id="slot.diagram.phone_na_body", prompt="", x=595, y=88, width=88, height=156, fill="#1f2937", stroke="#111827", stroke_width=2, rx=12, ry=12)
    phone_na_screen = RectSlot(id="slot.diagram.phone_na_screen", prompt="", x=603, y=108, width=72, height=112, fill="#e0f2fe", stroke="#4b5563", stroke_width=1, rx=4, ry=4)
    phone_na_btn = CircleSlot(id="slot.diagram.phone_na_btn", prompt="", cx=639, cy=232, r=7, fill="#374151", stroke="#9ca3af", stroke_width=1)
    price_na = TextSlot(id="slot.diagram.price_na", prompt="", text="1020000원", x=639, y=262, font_size=22, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center")

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
            Region(
                id="region.diagram",
                role="diagram",
                flow="absolute",
                slot_ids=(
                    "slot.diagram.phone_ga_body",
                    "slot.diagram.phone_ga_screen",
                    "slot.diagram.phone_ga_time",
                    "slot.diagram.phone_ga_btn",
                    "slot.diagram.price_ga",
                    "slot.diagram.phone_na_body",
                    "slot.diagram.phone_na_screen",
                    "slot.diagram.phone_na_btn",
                    "slot.diagram.price_na",
                ),
            ),
            Region(
                id="region.choices",
                role="choices",
                flow="absolute",
                slot_ids=(
                    "slot.choice.option_0",
                    "slot.choice.option_1",
                ),
            ),
        ),
        slots=(
            stem_text_slot,
            choice_ga,
            phone_ga_body,
            phone_ga_screen,
            phone_ga_time,
            phone_ga_btn,
            price_ga,
            choice_na,
            phone_na_body,
            phone_na_screen,
            phone_na_btn,
            price_na,
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
        {"ref": "phone_ga", "value": 865000, "unit": "원"},
        {"ref": "phone_na", "value": 1020000, "unit": "원"},
    ],
    "target": {"ref": "slot.choice.option_0", "label": "가격이 더 낮은 휴대 전화", "unit": ""},
    "method": "digit_count_comparison",
    "steps": [
        {
            "id": "compare_prices",
            "expr": "865000 < 1020000",
            "explanation": "865000은 6자리 수이고 1020000은 7자리 수이므로 가격이 더 낮은 휴대 전화는 가입니다.",
            "value": "가",
        },
    ],
    "answer": ANSWER,
}


if __name__ == "__main__":
    print(f"[{PROBLEM_TEMPLATE.id}] 템플릿 컴파일 성공!")
    print(f"- 제목: {PROBLEM_TEMPLATE.title}")
    print(f"- 캔버스: {PROBLEM_TEMPLATE.canvas.width} x {PROBLEM_TEMPLATE.canvas.height}")
    print(f"- 구역 수: {len(PROBLEM_TEMPLATE.regions)}")
