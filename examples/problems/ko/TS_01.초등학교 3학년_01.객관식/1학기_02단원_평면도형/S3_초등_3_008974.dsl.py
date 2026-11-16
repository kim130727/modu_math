"""ModuMath Problem DSL: 곧은 선과 굽은 선 구분하기 (S3_초등_3_008974)"""

from __future__ import annotations

from modu_math.dsl import (
    BlankSlot,
    Canvas,
    CircleSlot,
    LineSlot,
    PathSlot,
    PolygonSlot,
    ProblemTemplate,
    RectSlot,
    Region,
    TextBoxSlot,
    TextSlot,
)


# ==============================================================================
# 1. 문제 식별자 및 제목 (Problem Metadata)
# ==============================================================================
PROBLEM_ID = "S3_초등_3_008974"
PROBLEM_TITLE = "곧은 선 찾아 기호 선택하기"


# ==============================================================================
# 2. 정답 및 오답 진단 정의 (Answer & Diagnostic Key)
# ==============================================================================
ANSWER = {
    "value": "다",
    "answer_index": 2,
    "unit": "",
    "values": ["다"],
    "choices": [
        "가",
        "나",
        "다",
        "라",
    ],
    "blanks": [],
    "answer_key": [
        {
            "slot_id": "slot.choice.option_2",
            "value": "다",
            "diagnostics": [
                {
                    "id": "diag.curved_line_ga",
                    "condition": "answer_equals_ga",
                    "concept": "곧은 선과 굽은 선",
                    "reason": "구불구불하게 휘어진 굽은 선 '가'를 선택함",
                    "feedback": "'가'는 구불구불하게 휘어져 있으므로 굽은 선입니다. 반듯하게 뻗은 선을 찾아보세요.",
                },
                {
                    "id": "diag.curved_line_na",
                    "condition": "answer_equals_na",
                    "concept": "곧은 선과 굽은 선",
                    "reason": "위로 완만하게 휜 굽은 선 '나'를 선택함",
                    "feedback": "'나'는 위쪽으로 완만하게 휘어져 있는 굽은 선입니다. 자를 대었을 때 반듯한 선을 찾아보세요.",
                },
                {
                    "id": "diag.curved_line_ra",
                    "condition": "answer_equals_ra",
                    "concept": "곧은 선과 굽은 선",
                    "reason": "아래로 휘어진 굽은 선 '라'를 선택함",
                    "feedback": "'라'는 아래쪽으로 휘어져 있는 굽은 선입니다. 구부러지지 않고 곧게 뻗은 선을 찾아보세요.",
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
    "problem_type": "multiple_choice_geometry_line_classification",
    "metadata": {
        "school": "초등학교",
        "grade": 3,
        "semester": "1학기",
        "chapter": "02단원_평면도형",
        "difficulty": "하",
    },
    "entities": {
        "point_left": {"label": "왼쪽 끝점", "x": 360, "y": 155},
        "point_right": {"label": "오른쪽 끝점", "x": 815, "y": 175},
        "line_ga": {"label": "가", "type": "curved_line", "is_straight": False},
        "line_na": {"label": "나", "type": "curved_line", "is_straight": False},
        "line_da": {"label": "다", "type": "straight_line", "is_straight": True},
        "line_ra": {"label": "라", "type": "curved_line", "is_straight": False},
    },
    "relations": [
        {
            "type": "classification",
            "target_concept": "곧은 선",
            "correct_entity": "line_da",
            "distractors": ["line_ga", "line_na", "line_ra"],
        }
    ],
}


# ==============================================================================
# 4. 문제 템플릿 빌더 (ProblemTemplate Builder)
# ==============================================================================
def build_problem_template() -> ProblemTemplate:
    """문제의 캔버스 크기, 슬롯(텍스트/도형/선택지), 리전(구역)을 정의합니다."""

    # --------------------------------------------------------------------------
    # 4-1. 발문(지문) 텍스트 슬롯 (Stem Text Slot)
    # --------------------------------------------------------------------------
    stem_text_slot = TextBoxSlot(
        id="slot.stem.question",
        prompt="",
        text="8. 곧은 선을 찾아 기호를 선택하세요.",
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

    # --------------------------------------------------------------------------
    # 4-2. 도형 영역: 두 끝점과 4개의 선 (Diagram Slots)
    # --------------------------------------------------------------------------
    # 왼쪽 끝점 (360, 155) & 오른쪽 끝점 (815, 175)
    left_dot_slot = CircleSlot(
        id="slot.diagram.point_left",
        prompt="",
        cx=360,
        cy=155,
        r=3.5,
        fill="#111827",
        stroke="#111827",
        stroke_width=1,
    )

    right_dot_slot = CircleSlot(
        id="slot.diagram.point_right",
        prompt="",
        cx=815,
        cy=175,
        r=3.5,
        fill="#111827",
        stroke="#111827",
        stroke_width=1,
    )

    # 선 '가': 위쪽 물결 모양 굽은 선 (PathSlot)
    line_ga_slot = PathSlot(
        id="slot.diagram.line_ga",
        prompt="",
        d=(
            "M 360 155 "
            "C 405 100, 480 65, 535 90 "
            "C 575 110, 595 112, 625 95 "
            "C 665 72, 685 82, 695 110 "
            "C 705 135, 725 120, 750 125 "
            "C 780 132, 795 162, 815 175"
        ),
        fill="none",
        stroke="#111827",
        stroke_width=1.6,
    )

    # 선 '나': 위쪽 완만한 아치형 굽은 선 (PathSlot)
    line_na_slot = PathSlot(
        id="slot.diagram.line_na",
        prompt="",
        d="M 360 155 Q 525 75, 815 175",
        fill="none",
        stroke="#111827",
        stroke_width=1.6,
    )

    # 선 '다': 두 끝점을 잇는 곧은 선 (LineSlot)
    line_da_slot = LineSlot(
        id="slot.diagram.line_da",
        prompt="",
        x1=360,
        y1=155,
        x2=815,
        y2=175,
        stroke="#111827",
        stroke_width=1.6,
    )

    # 선 '라': 아래쪽 완만한 아치형 굽은 선 (PathSlot)
    line_ra_slot = PathSlot(
        id="slot.diagram.line_ra",
        prompt="",
        d="M 360 155 Q 545 245, 815 175",
        fill="none",
        stroke="#111827",
        stroke_width=1.6,
    )

    # 도형 내부 기호 라벨 ('가', '나', '다', '라')
    label_ga_slot = TextSlot(
        id="slot.diagram.label_ga",
        prompt="",
        text="가",
        x=522,
        y=62,
        font_size=21,
        font_family='"Noto Sans KR", sans-serif',
        fill="#111827",
        align="center",
    )

    label_na_slot = TextSlot(
        id="slot.diagram.label_na",
        prompt="",
        text="나",
        x=492,
        y=102,
        font_size=21,
        font_family='"Noto Sans KR", sans-serif',
        fill="#111827",
        align="center",
    )

    label_da_slot = TextSlot(
        id="slot.diagram.label_da",
        prompt="",
        text="다",
        x=538,
        y=148,
        font_size=21,
        font_family='"Noto Sans KR", sans-serif',
        fill="#111827",
        align="center",
    )

    label_ra_slot = TextSlot(
        id="slot.diagram.label_ra",
        prompt="",
        text="라",
        x=552,
        y=194,
        font_size=21,
        font_family='"Noto Sans KR", sans-serif',
        fill="#111827",
        align="center",
    )

    # --------------------------------------------------------------------------
    # 4-3. 선택 영역: ( 가 , 나 , 다 , 라 ) 괄호 선택형 슬롯
    # --------------------------------------------------------------------------
    paren_left_slot = TextSlot(
        id="slot.choice.paren_left",
        prompt="",
        text="(",
        x=475,
        y=252,
        font_size=24,
        font_family='"Noto Sans KR", sans-serif',
        fill="#111827",
        align="center",
    )

    choice_ga_slot = TextSlot(
        id="slot.choice.option_0",
        prompt="",
        text="가",
        x=505,
        y=252,
        font_size=22,
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

    comma_1_slot = TextSlot(
        id="slot.choice.comma_1",
        prompt="",
        text=",",
        x=532,
        y=252,
        font_size=22,
        font_family='"Noto Sans KR", sans-serif',
        fill="#111827",
        align="center",
    )

    choice_na_slot = TextSlot(
        id="slot.choice.option_1",
        prompt="",
        text="나",
        x=560,
        y=252,
        font_size=22,
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

    comma_2_slot = TextSlot(
        id="slot.choice.comma_2",
        prompt="",
        text=",",
        x=587,
        y=252,
        font_size=22,
        font_family='"Noto Sans KR", sans-serif',
        fill="#111827",
        align="center",
    )

    choice_da_slot = TextSlot(
        id="slot.choice.option_2",
        prompt="",
        text="다",
        x=615,
        y=252,
        font_size=22,
        font_family='"Noto Sans KR", sans-serif',
        fill="#111827",
        align="center",
        interaction={
            "type": "choice",
            "role": "answer",
            "choice_index": 2,
            "value": "다",
            "group_id": "slot.choice.group",
            "include_in_submission": True,
        },
    )

    comma_3_slot = TextSlot(
        id="slot.choice.comma_3",
        prompt="",
        text=",",
        x=642,
        y=252,
        font_size=22,
        font_family='"Noto Sans KR", sans-serif',
        fill="#111827",
        align="center",
    )

    choice_ra_slot = TextSlot(
        id="slot.choice.option_3",
        prompt="",
        text="라",
        x=670,
        y=252,
        font_size=22,
        font_family='"Noto Sans KR", sans-serif',
        fill="#111827",
        align="center",
        interaction={
            "type": "choice",
            "role": "answer",
            "choice_index": 3,
            "value": "라",
            "group_id": "slot.choice.group",
            "include_in_submission": True,
        },
    )

    paren_right_slot = TextSlot(
        id="slot.choice.paren_right",
        prompt="",
        text=")",
        x=700,
        y=252,
        font_size=24,
        font_family='"Noto Sans KR", sans-serif',
        fill="#111827",
        align="center",
    )

    # --------------------------------------------------------------------------
    # 4-4. 캔버스 및 리전(Region) 결합
    # --------------------------------------------------------------------------
    return ProblemTemplate(
        id=PROBLEM_ID,
        title=PROBLEM_TITLE,
        canvas=Canvas(
            width=886,
            height=300,
            coordinate_mode="logical",
        ),
        regions=(
            # 발문 구역
            Region(
                id="region.stem",
                role="stem",
                flow="absolute",
                slot_ids=("slot.stem.question",),
            ),
            # 선 도형 구역
            Region(
                id="region.diagram",
                role="diagram",
                flow="absolute",
                slot_ids=(
                    "slot.diagram.line_ga",
                    "slot.diagram.line_na",
                    "slot.diagram.line_da",
                    "slot.diagram.line_ra",
                    "slot.diagram.point_left",
                    "slot.diagram.point_right",
                    "slot.diagram.label_ga",
                    "slot.diagram.label_na",
                    "slot.diagram.label_da",
                    "slot.diagram.label_ra",
                ),
            ),
            # 기호 선택 구역
            Region(
                id="region.choices",
                role="choices",
                flow="absolute",
                slot_ids=(
                    "slot.choice.paren_left",
                    "slot.choice.option_0",
                    "slot.choice.comma_1",
                    "slot.choice.option_1",
                    "slot.choice.comma_2",
                    "slot.choice.option_2",
                    "slot.choice.comma_3",
                    "slot.choice.option_3",
                    "slot.choice.paren_right",
                ),
            ),
        ),
        slots=(
            stem_text_slot,
            line_ga_slot,
            line_na_slot,
            line_da_slot,
            line_ra_slot,
            left_dot_slot,
            right_dot_slot,
            label_ga_slot,
            label_na_slot,
            label_da_slot,
            label_ra_slot,
            paren_left_slot,
            choice_ga_slot,
            comma_1_slot,
            choice_na_slot,
            comma_2_slot,
            choice_da_slot,
            comma_3_slot,
            choice_ra_slot,
            paren_right_slot,
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
        {"ref": "line_ga", "value": "curved_line"},
        {"ref": "line_na", "value": "curved_line"},
        {"ref": "line_da", "value": "straight_line"},
        {"ref": "line_ra", "value": "curved_line"},
    ],
    "target": {"ref": "slot.choice.option_2", "label": "곧은 선의 기호", "unit": ""},
    "method": "line_classification",
    "steps": [
        {
            "id": "identify_straight_line",
            "expr": "line_da",
            "explanation": "구부러지지 않고 반듯하게 뻗은 선은 '다'입니다.",
            "value": "다",
        },
    ],
    "answer": ANSWER,
}


if __name__ == "__main__":
    print(f"[{PROBLEM_TEMPLATE.id}] 템플릿 컴파일 성공!")
    print(f"- 제목: {PROBLEM_TEMPLATE.title}")
    print(f"- 캔버스: {PROBLEM_TEMPLATE.canvas.width} x {PROBLEM_TEMPLATE.canvas.height}")
    print(f"- 구역 수: {len(PROBLEM_TEMPLATE.regions)}")
