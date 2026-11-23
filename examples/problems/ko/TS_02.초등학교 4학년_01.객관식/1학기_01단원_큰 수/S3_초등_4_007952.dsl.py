"""ModuMath Problem DSL: 조와 억 단위 큰 수의 크기 비교 (S3_초등_4_007952)"""

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
PROBLEM_ID = "S3_초등_4_007952"
PROBLEM_TITLE = "조와 억 단위의 큰 수에서 더 작은 수 선택하기"


# ==============================================================================
# 2. 정답 및 오답 진단 정의 (Answer & Diagnostic Key)
# ==============================================================================
ANSWER = {
    "value": "41조 6985억",
    "answer_index": 1,
    "unit": "",
    "values": ["41조 6985억"],
    "choices": [
        "41조 7320억",
        "41조 6985억",
    ],
    "blanks": [],
    "answer_key": [
        {
            "slot_id": "slot.choice.option_1",
            "value": "41조 6985억",
            "diagnostics": [
                {
                    "id": "diag.chose_larger_number",
                    "condition": "answer_equals_41jo_7320eok",
                    "concept": "큰 수의 크기 비교",
                    "reason": "더 작은 수 대신 더 큰 수인 41조 7320억을 선택함",
                    "feedback": "조 단위가 41조로 같으므로 억 단위의 천억 자리 숫자를 비교합니다. 7 > 6이므로 41조 6985억이 더 작은 수입니다.",
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
        "num_0": {"label": "41조 7320억", "value": 41732000000000},
        "num_1": {"label": "41조 6985억", "value": 41698500000000},
    },
    "relations": [
        {
            "type": "less_than",
            "expression": "41조 6985억 < 41조 7320억",
            "smaller": "num_1",
            "larger": "num_0",
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
        text="11. 더 작은 수를 선택하세요.",
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

    card_0_bg = RectSlot(
        id="slot.diagram.card_0_bg",
        prompt="",
        x=180,
        y=96,
        width=230,
        height=72,
        fill="#e8e4f3",
        stroke="#d8d0ec",
        stroke_width=1.2,
        rx=4,
        ry=4,
    )
    choice_0 = TextSlot(
        id="slot.choice.option_0",
        prompt="",
        text="41조 7320억",
        x=295,
        y=118,
        font_size=24,
        font_family='"Noto Sans KR", sans-serif',
        fill="#111827",
        align="center",
        interaction={
            "type": "choice",
            "role": "answer",
            "choice_index": 0,
            "value": "41조 7320억",
            "group_id": "slot.choice.group",
            "include_in_submission": True,
        },
    )

    card_1_bg = RectSlot(
        id="slot.diagram.card_1_bg",
        prompt="",
        x=476,
        y=96,
        width=230,
        height=72,
        fill="#e8e4f3",
        stroke="#d8d0ec",
        stroke_width=1.2,
        rx=4,
        ry=4,
    )
    choice_1 = TextSlot(
        id="slot.choice.option_1",
        prompt="",
        text="41조 6985억",
        x=591,
        y=118,
        font_size=24,
        font_family='"Noto Sans KR", sans-serif',
        fill="#111827",
        align="center",
        interaction={
            "type": "choice",
            "role": "answer",
            "choice_index": 1,
            "value": "41조 6985억",
            "group_id": "slot.choice.group",
            "include_in_submission": True,
        },
    )

    return ProblemTemplate(
        id=PROBLEM_ID,
        title=PROBLEM_TITLE,
        canvas=Canvas(
            width=886,
            height=220,
            coordinate_mode="logical",
        ),
        regions=(
            Region(id="region.stem", role="stem", flow="absolute", slot_ids=("slot.stem.question",)),
            Region(
                id="region.diagram",
                role="diagram",
                flow="absolute",
                slot_ids=("slot.diagram.card_0_bg", "slot.diagram.card_1_bg"),
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
            card_0_bg,
            choice_0,
            card_1_bg,
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
        {"ref": "num_0", "value": 41732000000000},
        {"ref": "num_1", "value": 41698500000000},
    ],
    "target": {"ref": "slot.choice.option_1", "label": "더 작은 수", "unit": ""},
    "method": "place_by_place_comparison",
    "steps": [
        {
            "id": "compare_jo_eok",
            "expr": "41조 6985억 < 41조 7320억",
            "explanation": "천억의 자리 숫자를 비교하면 7 > 6이므로 41조 6985억이 더 작습니다.",
            "value": "41조 6985억",
        },
    ],
    "answer": ANSWER,
}


if __name__ == "__main__":
    print(f"[{PROBLEM_TEMPLATE.id}] 템플릿 컴파일 성공!")
    print(f"- 제목: {PROBLEM_TEMPLATE.title}")
    print(f"- 캔버스: {PROBLEM_TEMPLATE.canvas.width} x {PROBLEM_TEMPLATE.canvas.height}")
    print(f"- 구역 수: {len(PROBLEM_TEMPLATE.regions)}")
