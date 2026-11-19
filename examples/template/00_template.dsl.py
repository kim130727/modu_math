"""ModuMath Problem DSL Template (표준 템플릿)

이 파일은 all_dsl_py(377개 파일)의 구조, 슬롯 배치, 정답 및 오답 진단 스펙,
시맨틱 모델, ModuMath DSL 컴파일러 규격을 종합하여 제작된 표준 템플릿입니다.

새로운 수학 문제 DSL을 작성할 때 이 템플릿을 복사하여 수정해 사용하세요.
"""

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
PROBLEM_ID = "P3_1_01_TEMPLATE_001"
PROBLEM_TITLE = "두 가족이 캔 고구마의 수"


# ==============================================================================
# 2. 정답 및 오답 진단 정의 (Answer & Diagnostic Key)
# ==============================================================================
# [유형 1: 주관식 / 빈칸 입력형 (기본 예시)]
ANSWER = {
    "value": 507,
    "unit": "개",
    "values": [507],
    "choices": [],  # 주관식은 빈 리스트
    "blanks": [
        {
            "id": "slot.answer.blank",
            "slot_id": "slot.answer.blank",
            "expected": 507,
        },
    ],
    "answer_key": [
        {
            "slot_id": "slot.answer.blank",
            "value": 507,
            "diagnostics": [
                {
                    "id": "diag.wrong_calculation",
                    "condition": "addition_with_carry_wrong_answer",
                    "concept": "받아올림",
                    "reason": "받아올림이 있는 덧셈에서 계산 오류",
                    "feedback": "일의 자리부터 다시 계산해요. 10이 넘으면 올린 1을 다음 자리에 꼭 더해 보세요.",
                },
                {
                    "id": "diag.single_given_value",
                    "condition": "answer_equals_given_value",
                    "concept": "문제 이해",
                    "reason": "주어진 한쪽 값만 답으로 작성함",
                    "feedback": "한 가족이 캔 수만 쓰면 안 돼요. 두 가족이 캔 수를 모두 더해 보세요.",
                },
            ],
        },
    ],
}

# [유형 2: 객관식인 경우 아래 형식을 사용하세요]
# ANSWER = {
#     "value": "②",
#     "answer_index": 1,
#     "choices": [
#         "① 487",
#         "② 507",
#         "③ 517",
#         "④ 607",
#     ],
#     "blanks": [],
#     "answer_key": [],
# }


# ==============================================================================
# 3. 시맨틱 모델 정의 (Semantic Model & Metadata)
# ==============================================================================
SEMANTIC = {
    "problem_id": PROBLEM_ID,
    "problem_type": "numeric_answer_addition_word_problem",
    "metadata": {
        "school": "초등학교",
        "grade": 3,
        "semester": "1학기",
        "chapter": "01단원_덧셈과 뺄셈",
        "difficulty": "중",
    },
    "entities": {
        "sanghyun": {"label": "상현이네 고구마", "value": 259, "unit": "개"},
        "yongjin": {"label": "용진이네 고구마", "value": 248, "unit": "개"},
        "total": {"label": "전체 고구마", "value": 507, "unit": "개"},
    },
    "relations": [
        {
            "type": "addition",
            "expression": "259 + 248 = 507",
            "inputs": ["sanghyun", "yongjin"],
            "output": "total",
        }
    ],
}


# ==============================================================================
# 4. 문제 템플릿 빌더 (ProblemTemplate Builder)
# ==============================================================================
def build_problem_template() -> ProblemTemplate:
    """문제의 캔버스 크기, 슬롯(텍스트/도형/입력창), 리전(구역)을 정의합니다."""

    # --------------------------------------------------------------------------
    # 4-1. 발문(지문) 텍스트 슬롯 (Stem Text Slot)
    # --------------------------------------------------------------------------
    stem_text_slot = TextBoxSlot(
        id="slot.stem.question",
        prompt="",
        text="지난 일요일 상현이네와 용진이네 가족은 주말 농장에 갔습니다. 고구마를 상현이네는 259개, 용진이네는 248개 캤습니다. 이 두 가족이 캔 고구마는 모두 몇 개입니까?",
        x=32,
        y=24,
        width=820,
        height=60,
        font_size=20,
        font_family='"Noto Sans KR", sans-serif',
        fill="#202124",
        align="left",
        valign="top",
        line_height=1.5,
    )

    # --------------------------------------------------------------------------
    # 4-2. 수식 및 풀이 영역 (Formula / Diagram Slots)
    # --------------------------------------------------------------------------
    # 수식 텍스트 라벨
    formula_slot = TextSlot(
        id="slot.formula.label",
        prompt="",
        text="259 + 248 =",
        x=280,
        y=130,
        font_size=32,
        font_family='"Noto Sans KR", sans-serif',
        fill="#111827",
        align="left",
    )

    # 정답 입력 박스 (RectSlot with interaction & input_style)
    answer_input_slot = RectSlot(
        id="slot.answer.blank",
        prompt="",
        x=460,
        y=118,
        width=110,
        height=54,
        fill="#ffffff",
        stroke="#111827",
        stroke_width=1.5,
        rx=4,
        ry=4,
        interaction={
            "type": "input",
            "role": "answer",
            "value_type": "integer",
            "max_length": 4,
            "include_in_submission": True,
            "order": 0,
            "group_id": "final_answer",
            "auto_advance": False,
            "keyboard": "number",
        },
        input_style={
            "font_size_mode": "auto",
            "font_size_adjust": 0,
            "min_font_size": 16,
            "max_font_size": 32,
            "font_weight": 700,
            "horizontal_align": "center",
            "vertical_align": "middle",
            "padding": 6,
            "text_color": "#222222",
        },
    )

    # 단위 라벨
    unit_slot = TextSlot(
        id="slot.answer.unit",
        prompt="",
        text="개",
        x=585,
        y=130,
        font_size=24,
        font_family='"Noto Sans KR", sans-serif',
        fill="#111827",
        align="left",
    )

    # --------------------------------------------------------------------------
    # 4-3. 캔버스 및 리전(Region) 결합
    # --------------------------------------------------------------------------
    return ProblemTemplate(
        id=PROBLEM_ID,
        title=PROBLEM_TITLE,
        canvas=Canvas(
            width=886,
            height=240,
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
            # 수식 및 입력 구역
            Region(
                id="region.expression",
                role="diagram",
                flow="absolute",
                slot_ids=(
                    "slot.formula.label",
                    "slot.answer.blank",
                    "slot.answer.unit",
                ),
            ),
        ),
        slots=(
            stem_text_slot,
            formula_slot,
            answer_input_slot,
            unit_slot,
        ),
    )


# ==============================================================================
# 5. ModuMath 프레임워크 필수 익스포트
# ==============================================================================
PROBLEM_TEMPLATE = build_problem_template()
SEMANTIC_OVERRIDE = SEMANTIC
SOLVABLE = {
    "problem_id": PROBLEM_ID,
    "solvable": True,
    "answer": ANSWER,
}


if __name__ == "__main__":
    print(f"[{PROBLEM_TEMPLATE.id}] 템플릿 컴파일 성공!")
    print(f"- 제목: {PROBLEM_TEMPLATE.title}")
    print(f"- 캔버스: {PROBLEM_TEMPLATE.canvas.width} x {PROBLEM_TEMPLATE.canvas.height}")
    print(f"- 구역 수: {len(PROBLEM_TEMPLATE.regions)}")
