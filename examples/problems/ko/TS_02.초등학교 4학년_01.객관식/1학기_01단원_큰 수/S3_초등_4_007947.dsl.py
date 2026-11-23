"""ModuMath Problem DSL: 큰 수에서 각 자리 숫자가 나타내는 값 (S3_초등_4_007947)"""

from __future__ import annotations

from modu_math.dsl import (
    Canvas,
    LineSlot,
    ProblemTemplate,
    RectSlot,
    Region,
    TextBoxSlot,
    TextSlot,
)


# ==============================================================================
# 1. 문제 식별자 및 제목 (Problem Metadata)
# ==============================================================================
PROBLEM_ID = "S3_초등_4_007947"
PROBLEM_TITLE = "숫자 5가 500조를 나타내는 자리 찾기"


# ==============================================================================
# 2. 정답 및 오답 진단 정의 (Answer & Diagnostic Key)
# ==============================================================================
ANSWER = {
    "value": "㉡",
    "answer_index": 1,
    "unit": "",
    "values": ["㉡"],
    "choices": [
        "㉠",
        "㉡",
        "㉢",
        "㉣",
    ],
    "blanks": [],
    "answer_key": [
        {
            "slot_id": "slot.choice.option_1",
            "value": "㉡",
            "diagnostics": [
                {
                    "id": "diag.wrong_place_5000jo",
                    "condition": "answer_equals_giyeok",
                    "concept": "조 단위의 자릿값",
                    "reason": "천조의 자리 숫자를 백조의 자리로 혼동함",
                    "feedback": "오른쪽부터 네 자리씩 나누면 5555 | 0000 | 0000 | 0000입니다. ㉠은 5000조를 나타냅니다.",
                },
                {
                    "id": "diag.wrong_place_50jo",
                    "condition": "answer_equals_digeut",
                    "concept": "조 단위의 자릿값",
                    "reason": "십조의 자리 숫자를 백조의 자리로 혼동함",
                    "feedback": "㉢은 십조의 자리이므로 50조를 나타냅니다. 백조의 자리를 찾아보세요.",
                },
                {
                    "id": "diag.wrong_place_5jo",
                    "condition": "answer_equals_rieul",
                    "concept": "조 단위의 자릿값",
                    "reason": "일조의 자리 숫자를 백조의 자리로 혼동함",
                    "feedback": "㉣은 일조의 자리이므로 5조를 나타냅니다. 백조의 자리를 찾아보세요.",
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
    "problem_type": "multiple_choice_place_value",
    "metadata": {
        "school": "초등학교",
        "grade": 4,
        "semester": "1학기",
        "chapter": "01단원_큰 수",
        "difficulty": "중",
    },
    "entities": {
        "number": {"label": "큰 수", "value": "5555000000000000"},
        "digit_0": {"label": "㉠", "place": "천조", "value": "5000조"},
        "digit_1": {"label": "㉡", "place": "백조", "value": "500조"},
        "digit_2": {"label": "㉢", "place": "십조", "value": "50조"},
        "digit_3": {"label": "㉣", "place": "일조", "value": "5조"},
    },
    "relations": [
        {
            "type": "place_value_match",
            "target_value": "500조",
            "correct_entity": "digit_1",
            "distractors": ["digit_0", "digit_2", "digit_3"],
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
        text="5. 숫자 5가 500조를 나타내는 것을 찾아 기호를 선택하세요.",
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

    bg_box = RectSlot(
        id="slot.diagram.bg_box",
        prompt="",
        x=260,
        y=92,
        width=366,
        height=136,
        fill="#e8e4f3",
        stroke="#d8d0ec",
        stroke_width=1,
        rx=6,
        ry=6,
    )

    # 5 5 5 5 000000000000
    d_5_0 = TextSlot(
        id="slot.diagram.d_5_0",
        prompt="",
        text="5",
        x=305,
        y=118,
        font_size=28,
        font_family='"Noto Sans KR", sans-serif',
        fill="#db2777",
        align="center",
    )
    d_5_1 = TextSlot(
        id="slot.diagram.d_5_1",
        prompt="",
        text="5",
        x=335,
        y=118,
        font_size=28,
        font_family='"Noto Sans KR", sans-serif',
        fill="#db2777",
        align="center",
    )
    d_5_2 = TextSlot(
        id="slot.diagram.d_5_2",
        prompt="",
        text="5",
        x=365,
        y=118,
        font_size=28,
        font_family='"Noto Sans KR", sans-serif',
        fill="#db2777",
        align="center",
    )
    d_5_3 = TextSlot(
        id="slot.diagram.d_5_3",
        prompt="",
        text="5",
        x=395,
        y=118,
        font_size=28,
        font_family='"Noto Sans KR", sans-serif',
        fill="#db2777",
        align="center",
    )
    d_zeros = TextSlot(
        id="slot.diagram.d_zeros",
        prompt="",
        text="000000000000",
        x=505,
        y=118,
        font_size=28,
        font_family='"Noto Sans KR", sans-serif',
        fill="#111827",
        align="center",
    )

    u_0 = LineSlot(id="slot.diagram.u_0", prompt="", x1=295, y1=158, x2=315, y2=158, stroke="#111827", stroke_width=1.5)
    u_1 = LineSlot(id="slot.diagram.u_1", prompt="", x1=325, y1=158, x2=345, y2=158, stroke="#111827", stroke_width=1.5)
    u_2 = LineSlot(id="slot.diagram.u_2", prompt="", x1=355, y1=158, x2=375, y2=158, stroke="#111827", stroke_width=1.5)
    u_3 = LineSlot(id="slot.diagram.u_3", prompt="", x1=385, y1=158, x2=405, y2=158, stroke="#111827", stroke_width=1.5)

    choice_0 = TextSlot(
        id="slot.choice.option_0",
        prompt="",
        text="㉠",
        x=305,
        y=172,
        font_size=24,
        font_family='"Noto Sans KR", sans-serif',
        fill="#111827",
        align="center",
        interaction={
            "type": "choice",
            "role": "answer",
            "choice_index": 0,
            "value": "㉠",
            "group_id": "slot.choice.group",
            "include_in_submission": True,
        },
    )
    choice_1 = TextSlot(
        id="slot.choice.option_1",
        prompt="",
        text="㉡",
        x=335,
        y=172,
        font_size=24,
        font_family='"Noto Sans KR", sans-serif',
        fill="#111827",
        align="center",
        interaction={
            "type": "choice",
            "role": "answer",
            "choice_index": 1,
            "value": "㉡",
            "group_id": "slot.choice.group",
            "include_in_submission": True,
        },
    )
    choice_2 = TextSlot(
        id="slot.choice.option_2",
        prompt="",
        text="㉢",
        x=365,
        y=172,
        font_size=24,
        font_family='"Noto Sans KR", sans-serif',
        fill="#111827",
        align="center",
        interaction={
            "type": "choice",
            "role": "answer",
            "choice_index": 2,
            "value": "㉢",
            "group_id": "slot.choice.group",
            "include_in_submission": True,
        },
    )
    choice_3 = TextSlot(
        id="slot.choice.option_3",
        prompt="",
        text="㉣",
        x=395,
        y=172,
        font_size=24,
        font_family='"Noto Sans KR", sans-serif',
        fill="#111827",
        align="center",
        interaction={
            "type": "choice",
            "role": "answer",
            "choice_index": 3,
            "value": "㉣",
            "group_id": "slot.choice.group",
            "include_in_submission": True,
        },
    )

    return ProblemTemplate(
        id=PROBLEM_ID,
        title=PROBLEM_TITLE,
        canvas=Canvas(
            width=886,
            height=280,
            coordinate_mode="logical",
        ),
        regions=(
            Region(
                id="region.stem",
                role="stem",
                flow="absolute",
                slot_ids=("slot.stem.question",),
            ),
            Region(
                id="region.diagram",
                role="diagram",
                flow="absolute",
                slot_ids=(
                    "slot.diagram.bg_box",
                    "slot.diagram.d_5_0",
                    "slot.diagram.d_5_1",
                    "slot.diagram.d_5_2",
                    "slot.diagram.d_5_3",
                    "slot.diagram.d_zeros",
                    "slot.diagram.u_0",
                    "slot.diagram.u_1",
                    "slot.diagram.u_2",
                    "slot.diagram.u_3",
                ),
            ),
            Region(
                id="region.choices",
                role="choices",
                flow="absolute",
                slot_ids=(
                    "slot.choice.option_0",
                    "slot.choice.option_1",
                    "slot.choice.option_2",
                    "slot.choice.option_3",
                ),
            ),
        ),
        slots=(
            stem_text_slot,
            bg_box,
            d_5_0,
            d_5_1,
            d_5_2,
            d_5_3,
            d_zeros,
            u_0,
            u_1,
            u_2,
            u_3,
            choice_0,
            choice_1,
            choice_2,
            choice_3,
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
        {"ref": "number", "value": "5555000000000000"},
    ],
    "target": {"ref": "slot.choice.option_1", "label": "500조를 나타내는 기호", "unit": ""},
    "method": "place_value_identification",
    "steps": [
        {
            "id": "find_500jo_place",
            "expr": "digit_1",
            "explanation": "오른쪽부터 네 자리씩 나누어 조 단위를 확인하면 백조의 자리는 ㉡입니다.",
            "value": "㉡",
        },
    ],
    "answer": ANSWER,
}


if __name__ == "__main__":
    print(f"[{PROBLEM_TEMPLATE.id}] 템플릿 컴파일 성공!")
    print(f"- 제목: {PROBLEM_TEMPLATE.title}")
    print(f"- 캔버스: {PROBLEM_TEMPLATE.canvas.width} x {PROBLEM_TEMPLATE.canvas.height}")
    print(f"- 구역 수: {len(PROBLEM_TEMPLATE.regions)}")
