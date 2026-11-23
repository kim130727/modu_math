"""ModuMath Problem DSL: 한글로 된 큰 수를 숫자로 나타냈을 때 0의 개수 비교 (S3_초등_4_007953)"""

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
PROBLEM_ID = "S3_초등_4_007953"
PROBLEM_TITLE = "수로 나타냈을 때 0의 개수가 더 적은 사람 선택하기"


# ==============================================================================
# 2. 정답 및 오답 진단 정의 (Answer & Diagnostic Key)
# ==============================================================================
ANSWER = {
    "value": "현준",
    "answer_index": 0,
    "unit": "",
    "values": ["현준"],
    "choices": [
        "현준",
        "유정",
    ],
    "blanks": [],
    "answer_key": [
        {
            "slot_id": "slot.choice.option_0",
            "value": "현준",
            "diagnostics": [
                {
                    "id": "diag.chose_more_zeros",
                    "condition": "answer_equals_yujeong",
                    "concept": "다섯 자리 수 쓰기",
                    "reason": "유정이의 수(60009)가 0이 더 많음에도 유정을 선택함",
                    "feedback": "현준이의 '사만 십구'는 40019로 0이 2개이고, 유정이의 '육만 구'는 60009로 0이 3개입니다. 따라서 0이 더 적은 사람은 현준입니다.",
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
    "problem_type": "multiple_choice_korean_number_reading_writing",
    "metadata": {
        "school": "초등학교",
        "grade": 4,
        "semester": "1학기",
        "chapter": "01단원_큰 수",
        "difficulty": "중",
    },
    "entities": {
        "hyunjun": {"label": "현준", "korean_text": "사만 십구", "value": 40019, "zero_count": 2},
        "yujeong": {"label": "유정", "korean_text": "육만 구", "value": 60009, "zero_count": 3},
    },
    "relations": [
        {
            "type": "fewer_zeros",
            "correct_entity": "hyunjun",
            "distractor": "yujeong",
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
        text="14. 수로 나타냈을 때 0의 개수가 더 적은 것을 들고 있는 사람을 선택해 보세요.",
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

    # 현준 (왼쪽)
    hj_head = CircleSlot(id="slot.diagram.hj_head", prompt="", cx=310, cy=124, r=24, fill="#fde68a", stroke="#78350f", stroke_width=1.5)
    hj_hair = CircleSlot(id="slot.diagram.hj_hair", prompt="", cx=310, cy=110, r=20, fill="#4b5563", stroke="#374151", stroke_width=1)
    hj_board = RectSlot(id="slot.diagram.hj_board", prompt="", x=230, y=148, width=160, height=58, fill="#e7cfa8", stroke="#a16207", stroke_width=1.5, rx=4, ry=4)
    hj_board_text = TextSlot(id="slot.diagram.hj_board_text", prompt="", text="사만 십구", x=310, y=164, font_size=22, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center")
    hj_badge = RectSlot(id="slot.diagram.hj_badge", prompt="", x=272, y=220, width=76, height=34, fill="#fff1f2", stroke="#f43f5e", stroke_width=1.2, rx=6, ry=6)
    choice_0 = TextSlot(
        id="slot.choice.option_0",
        prompt="",
        text="현준",
        x=310,
        y=225,
        font_size=20,
        font_family='"Noto Sans KR", sans-serif',
        fill="#111827",
        align="center",
        interaction={
            "type": "choice",
            "role": "answer",
            "choice_index": 0,
            "value": "현준",
            "group_id": "slot.choice.group",
            "include_in_submission": True,
        },
    )

    # 유정 (오른쪽)
    yj_head = CircleSlot(id="slot.diagram.yj_head", prompt="", cx=576, cy=124, r=24, fill="#fde68a", stroke="#78350f", stroke_width=1.5)
    yj_hair = CircleSlot(id="slot.diagram.yj_hair", prompt="", cx=576, cy=110, r=21, fill="#92400e", stroke="#78350f", stroke_width=1)
    yj_board = RectSlot(id="slot.diagram.yj_board", prompt="", x=496, y=148, width=160, height=58, fill="#e7cfa8", stroke="#a16207", stroke_width=1.5, rx=4, ry=4)
    yj_board_text = TextSlot(id="slot.diagram.yj_board_text", prompt="", text="육만 구", x=576, y=164, font_size=22, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center")
    yj_badge = RectSlot(id="slot.diagram.yj_badge", prompt="", x=538, y=220, width=76, height=34, fill="#fff1f2", stroke="#f43f5e", stroke_width=1.2, rx=6, ry=6)
    choice_1 = TextSlot(
        id="slot.choice.option_1",
        prompt="",
        text="유정",
        x=576,
        y=225,
        font_size=20,
        font_family='"Noto Sans KR", sans-serif',
        fill="#111827",
        align="center",
        interaction={
            "type": "choice",
            "role": "answer",
            "choice_index": 1,
            "value": "유정",
            "group_id": "slot.choice.group",
            "include_in_submission": True,
        },
    )

    return ProblemTemplate(
        id=PROBLEM_ID,
        title=PROBLEM_TITLE,
        canvas=Canvas(
            width=886,
            height=290,
            coordinate_mode="logical",
        ),
        regions=(
            Region(id="region.stem", role="stem", flow="absolute", slot_ids=("slot.stem.question",)),
            Region(
                id="region.diagram",
                role="diagram",
                flow="absolute",
                slot_ids=(
                    "slot.diagram.hj_hair",
                    "slot.diagram.hj_head",
                    "slot.diagram.hj_board",
                    "slot.diagram.hj_board_text",
                    "slot.diagram.hj_badge",
                    "slot.diagram.yj_hair",
                    "slot.diagram.yj_head",
                    "slot.diagram.yj_board",
                    "slot.diagram.yj_board_text",
                    "slot.diagram.yj_badge",
                ),
            ),
            Region(
                id="region.choices",
                role="choices",
                flow="absolute",
                slot_ids=("slot.choice.option_0", "slot.choice.option_1"),
            ),
        ),
        slots=(
            stem_text_slot,
            hj_hair,
            hj_head,
            hj_board,
            hj_board_text,
            hj_badge,
            choice_0,
            yj_hair,
            yj_head,
            yj_board,
            yj_board_text,
            yj_badge,
            choice_1,
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
        {"ref": "hyunjun", "value": 40019},
        {"ref": "yujeong", "value": 60009},
    ],
    "target": {"ref": "slot.choice.option_0", "label": "0의 개수가 더 적은 사람", "unit": ""},
    "method": "zero_count_comparison",
    "steps": [
        {
            "id": "count_zeros",
            "expr": "40019 (0: 2개) < 60009 (0: 3개)",
            "explanation": "현준이는 40019로 0이 2개, 유정이는 60009로 0이 3개이므로 현준이가 더 적습니다.",
            "value": "현준",
        },
    ],
    "answer": ANSWER,
}


if __name__ == "__main__":
    print(f"[{PROBLEM_TEMPLATE.id}] 템플릿 컴파일 성공!")
    print(f"- 제목: {PROBLEM_TEMPLATE.title}")
    print(f"- 캔버스: {PROBLEM_TEMPLATE.canvas.width} x {PROBLEM_TEMPLATE.canvas.height}")
    print(f"- 구역 수: {len(PROBLEM_TEMPLATE.regions)}")
