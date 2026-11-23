"""ModuMath Problem DSL: 나눗셈의 몫과 나머지를 바르게 말한 사람 찾기 (S3_초등_4_008114)"""

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
PROBLEM_ID = "S3_초등_4_008114"
PROBLEM_TITLE = "482 ÷ 18의 몫과 나머지를 바르게 말한 사람 선택하기"


# ==============================================================================
# 2. 정답 및 오답 진단 정의 (Answer & Diagnostic Key)
# ==============================================================================
ANSWER = {
    "value": "민기",
    "answer_index": 1,
    "unit": "",
    "values": ["민기"],
    "choices": [
        "채아",
        "민기",
    ],
    "blanks": [],
    "answer_key": [
        {
            "slot_id": "slot.choice.option_1",
            "value": "민기",
            "diagnostics": [
                {
                    "id": "diag.wrong_quotient_chae",
                    "condition": "answer_equals_chaea",
                    "concept": "나눗셈의 몫과 나머지",
                    "reason": "18 × 25 + 12 = 462로 482가 되지 않음에도 채아를 선택함",
                    "feedback": "482 ÷ 18을 계산하면 몫은 26이고 나머지는 14입니다(18 × 26 + 14 = 482). 바르게 말한 사람은 민기입니다.",
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
    "problem_type": "multiple_choice_division_verification",
    "metadata": {
        "school": "초등학교",
        "grade": 4,
        "semester": "1학기",
        "chapter": "03단원_곱셈과 나눗셈",
        "difficulty": "중",
    },
    "entities": {
        "dividend": {"label": "나누어지는 수", "value": 482},
        "divisor": {"label": "나누는 수", "value": 18},
        "chaea": {"label": "채아", "quotient": 25, "remainder": 12, "is_correct": False},
        "mingi": {"label": "민기", "quotient": 26, "remainder": 14, "is_correct": True},
    },
    "relations": [
        {
            "type": "division_with_remainder",
            "expression": "482 / 18 = 26 ... 14",
            "correct_entity": "mingi",
            "distractor": "chaea",
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
        text="22. 482 ÷ 18의 몫과 나머지를 바르게 말한 사람을 선택해 보세요.",
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

    # 채아 (왼쪽)
    ca_bubble = RectSlot(id="slot.diagram.ca_bubble", prompt="", x=116, y=88, width=210, height=96, fill="#ffffff", stroke="#374151", stroke_width=1.5, rx=18, ry=18)
    ca_text = TextBoxSlot(
        id="slot.diagram.ca_text",
        prompt="",
        text="몫은 25이고\n나머지는 12야.",
        x=126,
        y=102,
        width=190,
        height=68,
        font_size=20,
        font_family='"Noto Sans KR", sans-serif',
        fill="#111827",
        align="center",
        valign="middle",
        line_height=1.4,
    )
    ca_head = CircleSlot(id="slot.diagram.ca_head", prompt="", cx=382, cy=132, r=24, fill="#fde68a", stroke="#78350f", stroke_width=1.5)
    ca_badge = RectSlot(id="slot.diagram.ca_badge", prompt="", x=344, y=172, width=76, height=34, fill="#fff1f2", stroke="#f43f5e", stroke_width=1.2, rx=6, ry=6)
    choice_0 = TextSlot(
        id="slot.choice.option_0",
        prompt="",
        text="채아",
        x=382,
        y=177,
        font_size=20,
        font_family='"Noto Sans KR", sans-serif',
        fill="#111827",
        align="center",
        interaction={"type": "choice", "role": "answer", "choice_index": 0, "value": "채아", "group_id": "slot.choice.group", "include_in_submission": True},
    )

    # 민기 (오른쪽)
    mg_head = CircleSlot(id="slot.diagram.mg_head", prompt="", cx=504, cy=132, r=24, fill="#fde68a", stroke="#78350f", stroke_width=1.5)
    mg_badge = RectSlot(id="slot.diagram.mg_badge", prompt="", x=466, y=172, width=76, height=34, fill="#fff1f2", stroke="#f43f5e", stroke_width=1.2, rx=6, ry=6)
    choice_1 = TextSlot(
        id="slot.choice.option_1",
        prompt="",
        text="민기",
        x=504,
        y=177,
        font_size=20,
        font_family='"Noto Sans KR", sans-serif',
        fill="#111827",
        align="center",
        interaction={"type": "choice", "role": "answer", "choice_index": 1, "value": "민기", "group_id": "slot.choice.group", "include_in_submission": True},
    )
    mg_bubble = RectSlot(id="slot.diagram.mg_bubble", prompt="", x=560, y=88, width=220, height=96, fill="#ffffff", stroke="#374151", stroke_width=1.5, rx=18, ry=18)
    mg_text = TextBoxSlot(
        id="slot.diagram.mg_text",
        prompt="",
        text="몫은 26이고\n나머지는 14야.",
        x=570,
        y=102,
        width=200,
        height=68,
        font_size=20,
        font_family='"Noto Sans KR", sans-serif',
        fill="#111827",
        align="center",
        valign="middle",
        line_height=1.4,
    )

    return ProblemTemplate(
        id=PROBLEM_ID,
        title=PROBLEM_TITLE,
        canvas=Canvas(
            width=886,
            height=240,
            coordinate_mode="logical",
        ),
        regions=(
            Region(id="region.stem", role="stem", flow="absolute", slot_ids=("slot.stem.question",)),
            Region(
                id="region.diagram",
                role="diagram",
                flow="absolute",
                slot_ids=(
                    "slot.diagram.ca_bubble",
                    "slot.diagram.ca_text",
                    "slot.diagram.ca_head",
                    "slot.diagram.ca_badge",
                    "slot.diagram.mg_head",
                    "slot.diagram.mg_badge",
                    "slot.diagram.mg_bubble",
                    "slot.diagram.mg_text",
                ),
            ),
            Region(id="region.choices", role="choices", flow="absolute", slot_ids=("slot.choice.option_0", "slot.choice.option_1")),
        ),
        slots=(
            stem_text_slot,
            ca_bubble,
            ca_text,
            ca_head,
            ca_badge,
            choice_0,
            mg_head,
            mg_badge,
            choice_1,
            mg_bubble,
            mg_text,
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
        {"ref": "dividend", "value": 482},
        {"ref": "divisor", "value": 18},
    ],
    "target": {"ref": "slot.choice.option_1", "label": "바르게 말한 사람", "unit": ""},
    "method": "long_division",
    "steps": [
        {
            "id": "divide_482_by_18",
            "expr": "482 / 18 = 26 ... 14",
            "explanation": "482 ÷ 18의 몫은 26이고 나머지는 14이므로 민기가 바르게 말했습니다.",
            "value": "민기",
        },
    ],
    "answer": ANSWER,
}


if __name__ == "__main__":
    print(f"[{PROBLEM_TEMPLATE.id}] 템플릿 컴파일 성공!")
    print(f"- 제목: {PROBLEM_TEMPLATE.title}")
    print(f"- 캔버스: {PROBLEM_TEMPLATE.canvas.width} x {PROBLEM_TEMPLATE.canvas.height}")
    print(f"- 구역 수: {len(PROBLEM_TEMPLATE.regions)}")
