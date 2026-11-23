"""ModuMath Problem DSL: 10000원이 되기 위해 필요한 10원짜리 동전의 수 (S3_초등_4_007946)"""

from __future__ import annotations

from modu_math.dsl import (
    Canvas,
    CircleSlot,
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
PROBLEM_ID = "S3_초등_4_007946"
PROBLEM_TITLE = "10000원이 되기 위해 필요한 10원짜리 동전의 수"


# ==============================================================================
# 2. 정답 및 오답 진단 정의 (Answer & Diagnostic Key)
# ==============================================================================
ANSWER = {
    "value": "1000",
    "answer_index": 1,
    "unit": "개",
    "values": ["1000"],
    "choices": [
        "100",
        "1000",
    ],
    "blanks": [],
    "answer_key": [
        {
            "slot_id": "slot.choice.option_1",
            "value": "1000",
            "diagnostics": [
                {
                    "id": "diag.confused_with_100won",
                    "condition": "answer_equals_100",
                    "concept": "10000의 구성",
                    "reason": "10원이 100개일 때와 1000개일 때의 자릿수를 혼동함",
                    "feedback": "10원이 100개이면 1000원입니다. 10000원이 되려면 10원이 1000개 필요합니다.",
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
    "problem_type": "multiple_choice_large_number_unit_conversion",
    "metadata": {
        "school": "초등학교",
        "grade": 4,
        "semester": "1학기",
        "chapter": "01단원_큰 수",
        "difficulty": "하",
    },
    "entities": {
        "target_amount": {"label": "목표 금액", "value": 10000, "unit": "원"},
        "reference_bill": {"label": "1000원 지폐", "unit_value": 1000, "count": 10},
        "coin": {"label": "10원 동전", "unit_value": 10, "needed_count": 1000},
    },
    "relations": [
        {
            "type": "multiplication_equivalence",
            "expression": "10 * 1000 = 10000",
            "target": "target_amount",
            "unit_entity": "coin",
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
        text="3. 10000원이 되려면 돈이 얼마만큼 필요한지 알맞은 수를 선택하세요.",
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

    # 1000원 지폐 10장 예시 박스
    ref_box = RectSlot(
        id="slot.diagram.ref_box",
        prompt="",
        x=358,
        y=82,
        width=170,
        height=136,
        fill="#ffffff",
        stroke="#f59e0b",
        stroke_width=2,
        rx=12,
        ry=12,
    )
    bill_bg = RectSlot(
        id="slot.diagram.bill_bg",
        prompt="",
        x=384,
        y=98,
        width=118,
        height=54,
        fill="#dbeafe",
        stroke="#60a5fa",
        stroke_width=1.5,
        rx=4,
        ry=4,
    )
    bill_line = LineSlot(
        id="slot.diagram.bill_line",
        prompt="",
        x1=443,
        y1=102,
        x2=443,
        y2=148,
        stroke="#3b82f6",
        stroke_width=1.5,
    )
    bill_label = TextSlot(
        id="slot.diagram.bill_label",
        prompt="",
        text="1000",
        x=413,
        y=116,
        font_size=18,
        font_family='"Noto Sans KR", sans-serif',
        fill="#1e3a8a",
        align="center",
    )
    bill_count_bg = RectSlot(
        id="slot.diagram.bill_count_bg",
        prompt="",
        x=405,
        y=164,
        width=76,
        height=34,
        fill="#fce7f3",
        stroke="#f9a8d4",
        stroke_width=1,
        rx=4,
        ry=4,
    )
    bill_count_text = TextSlot(
        id="slot.diagram.bill_count_text",
        prompt="",
        text="10장",
        x=443,
        y=170,
        font_size=20,
        font_family='"Noto Sans KR", sans-serif',
        fill="#111827",
        align="center",
    )

    # 10원 동전 (구리색)
    coin_outer = CircleSlot(
        id="slot.diagram.coin_outer",
        prompt="",
        cx=443,
        cy=272,
        r=34,
        fill="#e7c697",
        stroke="#b47b44",
        stroke_width=2,
    )
    coin_inner = CircleSlot(
        id="slot.diagram.coin_inner",
        prompt="",
        cx=443,
        cy=272,
        r=27,
        fill="#f0d5ad",
        stroke="#c9935b",
        stroke_width=1,
    )
    coin_value = TextSlot(
        id="slot.diagram.coin_value",
        prompt="",
        text="10",
        x=443,
        y=258,
        font_size=22,
        font_family='"Noto Sans KR", sans-serif',
        fill="#78350f",
        align="center",
    )

    # 선택 영역: ( 100 , 1000 )개
    paren_left = TextSlot(
        id="slot.choice.paren_left",
        prompt="",
        text="(",
        x=362,
        y=336,
        font_size=26,
        font_family='"Noto Sans KR", sans-serif',
        fill="#111827",
        align="center",
    )
    choice_0 = TextSlot(
        id="slot.choice.option_0",
        prompt="",
        text="100",
        x=402,
        y=336,
        font_size=24,
        font_family='"Noto Sans KR", sans-serif',
        fill="#111827",
        align="center",
        interaction={
            "type": "choice",
            "role": "answer",
            "choice_index": 0,
            "value": "100",
            "group_id": "slot.choice.group",
            "include_in_submission": True,
        },
    )
    comma = TextSlot(
        id="slot.choice.comma",
        prompt="",
        text=",",
        x=438,
        y=336,
        font_size=24,
        font_family='"Noto Sans KR", sans-serif',
        fill="#111827",
        align="center",
    )
    choice_1 = TextSlot(
        id="slot.choice.option_1",
        prompt="",
        text="1000",
        x=482,
        y=336,
        font_size=24,
        font_family='"Noto Sans KR", sans-serif',
        fill="#111827",
        align="center",
        interaction={
            "type": "choice",
            "role": "answer",
            "choice_index": 1,
            "value": "1000",
            "group_id": "slot.choice.group",
            "include_in_submission": True,
        },
    )
    paren_right = TextSlot(
        id="slot.choice.paren_right",
        prompt="",
        text=")개",
        x=538,
        y=336,
        font_size=26,
        font_family='"Noto Sans KR", sans-serif',
        fill="#111827",
        align="center",
    )

    return ProblemTemplate(
        id=PROBLEM_ID,
        title=PROBLEM_TITLE,
        canvas=Canvas(
            width=886,
            height=400,
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
                    "slot.diagram.ref_box",
                    "slot.diagram.bill_bg",
                    "slot.diagram.bill_line",
                    "slot.diagram.bill_label",
                    "slot.diagram.bill_count_bg",
                    "slot.diagram.bill_count_text",
                    "slot.diagram.coin_outer",
                    "slot.diagram.coin_inner",
                    "slot.diagram.coin_value",
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
            ref_box,
            bill_bg,
            bill_line,
            bill_label,
            bill_count_bg,
            bill_count_text,
            coin_outer,
            coin_inner,
            coin_value,
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
        {"ref": "target_amount", "value": 10000, "unit": "원"},
        {"ref": "coin", "value": 10, "unit": "원"},
    ],
    "target": {"ref": "slot.choice.option_1", "label": "필요한 10원 동전의 수", "unit": "개"},
    "method": "unit_conversion",
    "steps": [
        {
            "id": "divide_10000_by_10",
            "expr": "10000 / 10 = 1000",
            "explanation": "10원이 1000개이면 10000원입니다.",
            "value": "1000",
        },
    ],
    "answer": ANSWER,
}


if __name__ == "__main__":
    print(f"[{PROBLEM_TEMPLATE.id}] 템플릿 컴파일 성공!")
    print(f"- 제목: {PROBLEM_TEMPLATE.title}")
    print(f"- 캔버스: {PROBLEM_TEMPLATE.canvas.width} x {PROBLEM_TEMPLATE.canvas.height}")
    print(f"- 구역 수: {len(PROBLEM_TEMPLATE.regions)}")
