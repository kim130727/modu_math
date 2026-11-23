"""ModuMath Problem DSL: 1억을 바르게 설명한 사람 선택하기 (S3_초등_4_007954)"""

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
PROBLEM_ID = "S3_초등_4_007954"
PROBLEM_TITLE = "1억에 대한 바른 설명 찾기"


# ==============================================================================
# 2. 정답 및 오답 진단 정의 (Answer & Diagnostic Key)
# ==============================================================================
ANSWER = {
    "value": "규리",
    "answer_index": 0,
    "unit": "",
    "values": ["규리"],
    "choices": [
        "규리",
        "동준",
    ],
    "blanks": [],
    "answer_key": [
        {
            "slot_id": "slot.choice.option_0",
            "value": "규리",
            "diagnostics": [
                {
                    "id": "diag.chose_9999man_plus_10man",
                    "condition": "answer_equals_dongjun",
                    "concept": "1억의 이해",
                    "reason": "9999만보다 10만 큰 수를 1억으로 착각함",
                    "feedback": "9999만보다 1만 큰 수가 1억이고, 10만 큰 수는 1억 9만입니다. 1000만이 10개인 수가 1억입니다.",
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
    "problem_type": "multiple_choice_concept_verification",
    "metadata": {
        "school": "초등학교",
        "grade": 4,
        "semester": "1학기",
        "chapter": "01단원_큰 수",
        "difficulty": "중",
    },
    "entities": {
        "gyuri": {"label": "규리", "statement": "1000만이 10개인 수야.", "value": "1억", "is_correct": True},
        "dongjun": {"label": "동준", "statement": "9999만보다 10만 큰 수야.", "value": "1억 9만", "is_correct": False},
    },
    "relations": [
        {
            "type": "concept_match",
            "target": "1억",
            "correct_entity": "gyuri",
            "distractor": "dongjun",
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
        text="18. 1억을 바르게 설명한 사람의 이름을 선택하세요.",
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

    # 규리 (왼쪽)
    gr_bubble = RectSlot(id="slot.diagram.gr_bubble", prompt="", x=116, y=88, width=210, height=96, fill="#ffffff", stroke="#374151", stroke_width=1.5, rx=18, ry=18)
    gr_text = TextBoxSlot(
        id="slot.diagram.gr_text",
        prompt="",
        text="1000만이\n10개인 수야.",
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
    gr_head = CircleSlot(id="slot.diagram.gr_head", prompt="", cx=382, cy=136, r=24, fill="#fde68a", stroke="#78350f", stroke_width=1.5)
    gr_badge = RectSlot(id="slot.diagram.gr_badge", prompt="", x=346, y=172, width=72, height=32, fill="#ecfdf5", stroke="#22c55e", stroke_width=1.2, rx=6, ry=6)
    gr_name = TextSlot(id="slot.diagram.gr_name", prompt="", text="규리", x=382, y=177, font_size=18, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center")

    # 동준 (오른쪽)
    dj_head = CircleSlot(id="slot.diagram.dj_head", prompt="", cx=504, cy=136, r=24, fill="#fde68a", stroke="#78350f", stroke_width=1.5)
    dj_badge = RectSlot(id="slot.diagram.dj_badge", prompt="", x=468, y=172, width=72, height=32, fill="#ecfdf5", stroke="#22c55e", stroke_width=1.2, rx=6, ry=6)
    dj_name = TextSlot(id="slot.diagram.dj_name", prompt="", text="동준", x=504, y=177, font_size=18, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center")
    dj_bubble = RectSlot(id="slot.diagram.dj_bubble", prompt="", x=560, y=88, width=220, height=96, fill="#ffffff", stroke="#374151", stroke_width=1.5, rx=18, ry=18)
    dj_text = TextBoxSlot(
        id="slot.diagram.dj_text",
        prompt="",
        text="9999만보다\n10만 큰 수야.",
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

    # 선택 영역: ( 규리 , 동준 )
    paren_left = TextSlot(id="slot.choice.paren_left", prompt="", text="(", x=356, y=236, font_size=24, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center")
    choice_0 = TextSlot(
        id="slot.choice.option_0",
        prompt="",
        text="규리",
        x=402,
        y=236,
        font_size=22,
        font_family='"Noto Sans KR", sans-serif',
        fill="#111827",
        align="center",
        interaction={
            "type": "choice",
            "role": "answer",
            "choice_index": 0,
            "value": "규리",
            "group_id": "slot.choice.group",
            "include_in_submission": True,
        },
    )
    comma = TextSlot(id="slot.choice.comma", prompt="", text=",", x=443, y=236, font_size=22, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center")
    choice_1 = TextSlot(
        id="slot.choice.option_1",
        prompt="",
        text="동준",
        x=484,
        y=236,
        font_size=22,
        font_family='"Noto Sans KR", sans-serif',
        fill="#111827",
        align="center",
        interaction={
            "type": "choice",
            "role": "answer",
            "choice_index": 1,
            "value": "동준",
            "group_id": "slot.choice.group",
            "include_in_submission": True,
        },
    )
    paren_right = TextSlot(id="slot.choice.paren_right", prompt="", text=")", x=530, y=236, font_size=24, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center")

    return ProblemTemplate(
        id=PROBLEM_ID,
        title=PROBLEM_TITLE,
        canvas=Canvas(
            width=886,
            height=300,
            coordinate_mode="logical",
        ),
        regions=(
            Region(id="region.stem", role="stem", flow="absolute", slot_ids=("slot.stem.question",)),
            Region(
                id="region.diagram",
                role="diagram",
                flow="absolute",
                slot_ids=(
                    "slot.diagram.gr_bubble",
                    "slot.diagram.gr_text",
                    "slot.diagram.gr_head",
                    "slot.diagram.gr_badge",
                    "slot.diagram.gr_name",
                    "slot.diagram.dj_head",
                    "slot.diagram.dj_badge",
                    "slot.diagram.dj_name",
                    "slot.diagram.dj_bubble",
                    "slot.diagram.dj_text",
                ),
            ),
            Region(
                id="region.choices",
                role="choices",
                flow="absolute",
                slot_ids=(
                    "slot.choice.paren_left",
                    "slot.choice.option_0",
                    "slot.choice.comma",
                    "slot.choice.option_1",
                    "slot.choice.paren_right",
                ),
            ),
        ),
        slots=(
            stem_text_slot,
            gr_bubble,
            gr_text,
            gr_head,
            gr_badge,
            gr_name,
            dj_head,
            dj_badge,
            dj_name,
            dj_bubble,
            dj_text,
            paren_left,
            choice_0,
            comma,
            choice_1,
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
        {"ref": "gyuri", "value": "1000만이 10개인 수"},
        {"ref": "dongjun", "value": "9999만보다 10만 큰 수"},
    ],
    "target": {"ref": "slot.choice.option_0", "label": "1억을 바르게 설명한 사람", "unit": ""},
    "method": "concept_verification",
    "steps": [
        {
            "id": "verify_1eok",
            "expr": "1000만 * 10 = 1억",
            "explanation": "1000만이 10개인 수는 1억이므로 규리가 바르게 설명했습니다.",
            "value": "규리",
        },
    ],
    "answer": ANSWER,
}


if __name__ == "__main__":
    print(f"[{PROBLEM_TEMPLATE.id}] 템플릿 컴파일 성공!")
    print(f"- 제목: {PROBLEM_TEMPLATE.title}")
    print(f"- 캔버스: {PROBLEM_TEMPLATE.canvas.width} x {PROBLEM_TEMPLATE.canvas.height}")
    print(f"- 구역 수: {len(PROBLEM_TEMPLATE.regions)}")
