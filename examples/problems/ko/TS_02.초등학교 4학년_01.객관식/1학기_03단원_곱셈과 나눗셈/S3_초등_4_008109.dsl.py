"""ModuMath Problem DSL: 세 자리 수 × 두 자리 수 계산 결과 길 찾기 (S3_초등_4_008109)"""

from __future__ import annotations

from modu_math.dsl import (
    Canvas,
    CircleSlot,
    PathSlot,
    ProblemTemplate,
    RectSlot,
    Region,
    TextBoxSlot,
    TextSlot,
)


# ==============================================================================
# 1. 문제 식별자 및 제목 (Problem Metadata)
# ==============================================================================
PROBLEM_ID = "S3_초등_4_008109"
PROBLEM_TITLE = "229 × 36의 계산 결과에 맞는 길 찾기"


# ==============================================================================
# 2. 정답 및 오답 진단 정의 (Answer & Diagnostic Key)
# ==============================================================================
ANSWER = {
    "value": "도토리",
    "answer_index": 1,
    "unit": "",
    "values": ["도토리"],
    "choices": [
        "밤",
        "도토리",
    ],
    "blanks": [],
    "answer_key": [
        {
            "slot_id": "slot.choice.option_1",
            "value": "도토리",
            "diagnostics": [
                {
                    "id": "diag.forgot_place_shift",
                    "condition": "answer_equals_bam",
                    "concept": "세 자리 수 × 두 자리 수",
                    "reason": "229 × 30의 자리를 밀어 쓰지 않고 229 × 3으로 더해 2061을 얻음",
                    "feedback": "229 × 6 = 1374이고, 229 × 30 = 6870입니다. 두 값을 더하면 8244이므로 도토리를 먹게 됩니다.",
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
    "problem_type": "multiple_choice_multiplication_word_problem",
    "metadata": {
        "school": "초등학교",
        "grade": 4,
        "semester": "1학기",
        "chapter": "03단원_곱셈과 나눗셈",
        "difficulty": "중",
    },
    "entities": {
        "expression": {"label": "곱셈식", "value": "229 × 36"},
        "path_bam": {"label": "밤", "value": 2061},
        "path_dotori": {"label": "도토리", "value": 8244},
    },
    "relations": [
        {
            "type": "multiplication",
            "expression": "229 * 36 = 8244",
            "correct_entity": "path_dotori",
            "distractor": "path_bam",
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
        text="17. 다람쥐는 밤과 도토리 중에서 어느 것을 먹게 될까요?",
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

    bubble = RectSlot(id="slot.diagram.bubble", prompt="", x=40, y=88, width=250, height=106, fill="#ffffff", stroke="#374151", stroke_width=1.5, rx=24, ry=24)
    bubble_text = TextBoxSlot(
        id="slot.diagram.bubble_text",
        prompt="",
        text="곱셈식의 계산 결과가\n쓰여 있는 길을 따라 가면\n무엇을 먹게 될까?",
        x=50,
        y=98,
        width=230,
        height=86,
        font_size=18,
        font_family='"Noto Sans KR", sans-serif',
        fill="#111827",
        align="center",
        valign="middle",
        line_height=1.35,
    )

    sq_head = CircleSlot(id="slot.diagram.sq_head", prompt="", cx=365, cy=114, r=20, fill="#d97706", stroke="#92400e", stroke_width=1.5)
    sign_board = RectSlot(id="slot.diagram.sign_board", prompt="", x=306, y=144, width=156, height=50, fill="#fde68a", stroke="#b45309", stroke_width=1.5, rx=4, ry=4)
    sign_text = TextSlot(id="slot.diagram.sign_text", prompt="", text="229 × 36", x=384, y=157, font_size=22, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center")

    start_label = TextSlot(id="slot.diagram.start_label", prompt="", text="출발 →", x=500, y=118, font_size=18, font_family='"Noto Sans KR", sans-serif', fill="#be185d", align="center")

    path_top = PathSlot(id="slot.diagram.path_top", prompt="", d="M 462 169 L 550 169 Q 640 100 790 106", fill="none", stroke="#ca8a04", stroke_width=24)
    path_bot = PathSlot(id="slot.diagram.path_bot", prompt="", d="M 462 169 L 550 169 Q 640 238 790 232", fill="none", stroke="#ca8a04", stroke_width=24)
    path_top_in = PathSlot(id="slot.diagram.path_top_in", prompt="", d="M 462 169 L 550 169 Q 640 100 790 106", fill="none", stroke="#fef3c7", stroke_width=20)
    path_bot_in = PathSlot(id="slot.diagram.path_bot_in", prompt="", d="M 462 169 L 550 169 Q 640 238 790 232", fill="none", stroke="#fef3c7", stroke_width=20)

    val_top = TextSlot(id="slot.diagram.val_top", prompt="", text="2061", x=710, y=96, font_size=20, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center")
    val_bot = TextSlot(id="slot.diagram.val_bot", prompt="", text="8244", x=710, y=220, font_size=20, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center")
    goal_top = TextSlot(id="slot.diagram.goal_top", prompt="", text="밤", x=812, y=96, font_size=20, font_family='"Noto Sans KR", sans-serif', fill="#78350f", align="center")
    goal_bot = TextSlot(id="slot.diagram.goal_bot", prompt="", text="도토리", x=816, y=220, font_size=20, font_family='"Noto Sans KR", sans-serif', fill="#78350f", align="center")

    # 선택 영역: ( 밤 , 도토리 )
    paren_left = TextSlot(id="slot.choice.paren_left", prompt="", text="(", x=362, y=274, font_size=24, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center")
    choice_0 = TextSlot(
        id="slot.choice.option_0",
        prompt="",
        text="밤",
        x=396,
        y=274,
        font_size=22,
        font_family='"Noto Sans KR", sans-serif',
        fill="#111827",
        align="center",
        interaction={"type": "choice", "role": "answer", "choice_index": 0, "value": "밤", "group_id": "slot.choice.group", "include_in_submission": True},
    )
    comma = TextSlot(id="slot.choice.comma", prompt="", text=",", x=424, y=274, font_size=22, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center")
    choice_1 = TextSlot(
        id="slot.choice.option_1",
        prompt="",
        text="도토리",
        x=472,
        y=274,
        font_size=22,
        font_family='"Noto Sans KR", sans-serif',
        fill="#111827",
        align="center",
        interaction={"type": "choice", "role": "answer", "choice_index": 1, "value": "도토리", "group_id": "slot.choice.group", "include_in_submission": True},
    )
    paren_right = TextSlot(id="slot.choice.paren_right", prompt="", text=")", x=520, y=274, font_size=24, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center")

    return ProblemTemplate(
        id=PROBLEM_ID,
        title=PROBLEM_TITLE,
        canvas=Canvas(
            width=886,
            height=330,
            coordinate_mode="logical",
        ),
        regions=(
            Region(id="region.stem", role="stem", flow="absolute", slot_ids=("slot.stem.question",)),
            Region(
                id="region.diagram",
                role="diagram",
                flow="absolute",
                slot_ids=(
                    "slot.diagram.bubble",
                    "slot.diagram.bubble_text",
                    "slot.diagram.sq_head",
                    "slot.diagram.sign_board",
                    "slot.diagram.sign_text",
                    "slot.diagram.start_label",
                    "slot.diagram.path_top",
                    "slot.diagram.path_bot",
                    "slot.diagram.path_top_in",
                    "slot.diagram.path_bot_in",
                    "slot.diagram.val_top",
                    "slot.diagram.val_bot",
                    "slot.diagram.goal_top",
                    "slot.diagram.goal_bot",
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
            bubble,
            bubble_text,
            sq_head,
            sign_board,
            sign_text,
            start_label,
            path_top,
            path_bot,
            path_top_in,
            path_bot_in,
            val_top,
            val_bot,
            goal_top,
            goal_bot,
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
        {"ref": "expression", "value": "229 × 36"},
    ],
    "target": {"ref": "slot.choice.option_1", "label": "도착지", "unit": ""},
    "method": "three_by_two_digit_multiplication",
    "steps": [
        {
            "id": "compute_product",
            "expr": "229 * 36 = 8244",
            "explanation": "229 × 36 = 8244이므로 8244가 쓰여 있는 길을 따라 도토리를 먹게 됩니다.",
            "value": "도토리",
        },
    ],
    "answer": ANSWER,
}


if __name__ == "__main__":
    print(f"[{PROBLEM_TEMPLATE.id}] 템플릿 컴파일 성공!")
    print(f"- 제목: {PROBLEM_TEMPLATE.title}")
    print(f"- 캔버스: {PROBLEM_TEMPLATE.canvas.width} x {PROBLEM_TEMPLATE.canvas.height}")
    print(f"- 구역 수: {len(PROBLEM_TEMPLATE.regions)}")
