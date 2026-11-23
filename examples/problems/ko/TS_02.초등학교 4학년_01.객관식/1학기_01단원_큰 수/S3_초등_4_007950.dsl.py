"""ModuMath Problem DSL: 얼마만큼씩 뛰어 세었는지 알아보기 (S3_초등_4_007950)"""

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
PROBLEM_ID = "S3_초등_4_007950"
PROBLEM_TITLE = "만 단위의 뛰어 세기 규칙과 자릿값 찾기"


# ==============================================================================
# 2. 정답 및 오답 진단 정의 (Answer & Diagnostic Key)
# ==============================================================================
ANSWER = {
    "value": ["십만", "100000"],
    "unit": "",
    "values": ["십만", "100000"],
    "choices": [
        "만",
        "십만",
        "백만",
        "10000",
        "100000",
        "1000000",
    ],
    "blanks": [],
    "answer_key": [
        {
            "slot_id": "slot.choice.g1_option_1",
            "value": "십만",
            "diagnostics": [
                {
                    "id": "diag.wrong_place_man",
                    "condition": "answer_equals_man",
                    "concept": "자릿값과 뛰어 세기",
                    "reason": "십만의 자리를 만의 자리로 혼동함",
                    "feedback": "206000에서 306000으로 바뀔 때 커진 숫자 2→3은 오른쪽에서 여섯째 자리인 십만의 자리입니다.",
                },
                {
                    "id": "diag.wrong_place_baekman",
                    "condition": "answer_equals_baekman",
                    "concept": "자릿값과 뛰어 세기",
                    "reason": "십만의 자리를 백만의 자리로 혼동함",
                    "feedback": "206000은 여섯 자리 수이므로 가장 높은 자리는 십만의 자리입니다.",
                },
            ],
        },
        {
            "slot_id": "slot.choice.g2_option_1",
            "value": "100000",
            "diagnostics": [
                {
                    "id": "diag.wrong_step_10000",
                    "condition": "answer_equals_10000",
                    "concept": "뛰어 세기",
                    "reason": "100000씩 뛰어 센 것을 10000씩으로 오인함",
                    "feedback": "십만의 자리 숫자가 1씩 커졌으므로 100000씩 뛰어 세었습니다.",
                },
                {
                    "id": "diag.wrong_step_1000000",
                    "condition": "answer_equals_1000000",
                    "concept": "뛰어 세기",
                    "reason": "100000씩 뛰어 센 것을 1000000씩으로 오인함",
                    "feedback": "1000000은 백만입니다. 십만의 자리 숫자가 1씩 커졌으므로 100000씩 뛰어 세었습니다.",
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
    "problem_type": "multiple_choice_skip_counting_pattern",
    "metadata": {
        "school": "초등학교",
        "grade": 4,
        "semester": "1학기",
        "chapter": "01단원_큰 수",
        "difficulty": "하",
    },
    "entities": {
        "seq_0": {"label": "첫째 수", "value": 206000},
        "seq_1": {"label": "둘째 수", "value": 306000},
        "seq_2": {"label": "셋째 수", "value": 406000},
        "seq_3": {"label": "넷째 수", "value": 506000},
        "seq_4": {"label": "다섯째 수", "value": 606000},
        "place": {"label": "변하는 자리", "value": "십만"},
        "step": {"label": "뛰어 센 값", "value": 100000},
    },
    "relations": [
        {
            "type": "skip_counting",
            "sequence": ["seq_0", "seq_1", "seq_2", "seq_3", "seq_4"],
            "place": "place",
            "step": "step",
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
        text="6. 얼마만큼씩 뛰어 세었는지 알아보려고 합니다. 알맞은 것을 선택하세요.",
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

    diagram_slots = []
    nums = ["206000", "306000", "406000", "506000", "606000"]
    for i, num in enumerate(nums):
        bx = 96 + i * 144
        if i > 0:
            diagram_slots.append(
                LineSlot(
                    id=f"slot.diagram.conn_{i}",
                    prompt="",
                    x1=bx - 28,
                    y1=114,
                    x2=bx,
                    y2=114,
                    stroke="#16a34a",
                    stroke_width=2,
                )
            )
        diagram_slots.append(
            RectSlot(
                id=f"slot.diagram.box_{i}",
                prompt="",
                x=bx,
                y=88,
                width=116,
                height=52,
                fill="#bbf7d0",
                stroke="#16a34a",
                stroke_width=1.8,
                rx=3,
                ry=3,
            )
        )
        diagram_slots.append(
            TextSlot(
                id=f"slot.diagram.num_{i}",
                prompt="",
                text=num,
                x=bx + 58,
                y=102,
                font_size=22,
                font_family='"Noto Sans KR", sans-serif',
                fill="#111827",
                align="center",
            )
        )

    # 첫 번째 선택 줄: ( 만 , 십만 , 백만 )의 자리 숫자가 1씩 커졌습니다.
    g1_left = TextSlot(id="slot.choice.g1_left", prompt="", text="(", x=188, y=184, font_size=24, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center")
    g1_0 = TextSlot(
        id="slot.choice.g1_option_0",
        prompt="",
        text="만",
        x=218,
        y=184,
        font_size=22,
        font_family='"Noto Sans KR", sans-serif',
        fill="#111827",
        align="center",
        interaction={"type": "choice", "role": "answer", "choice_index": 0, "value": "만", "group_id": "slot.choice.group_1", "include_in_submission": True},
    )
    g1_c0 = TextSlot(id="slot.choice.g1_c0", prompt="", text=",", x=244, y=184, font_size=22, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center")
    g1_1 = TextSlot(
        id="slot.choice.g1_option_1",
        prompt="",
        text="십만",
        x=278,
        y=184,
        font_size=22,
        font_family='"Noto Sans KR", sans-serif',
        fill="#111827",
        align="center",
        interaction={"type": "choice", "role": "answer", "choice_index": 1, "value": "십만", "group_id": "slot.choice.group_1", "include_in_submission": True},
    )
    g1_c1 = TextSlot(id="slot.choice.g1_c1", prompt="", text=",", x=312, y=184, font_size=22, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center")
    g1_2 = TextSlot(
        id="slot.choice.g1_option_2",
        prompt="",
        text="백만",
        x=348,
        y=184,
        font_size=22,
        font_family='"Noto Sans KR", sans-serif',
        fill="#111827",
        align="center",
        interaction={"type": "choice", "role": "answer", "choice_index": 2, "value": "백만", "group_id": "slot.choice.group_1", "include_in_submission": True},
    )
    g1_right = TextSlot(id="slot.choice.g1_right", prompt="", text=")의 자리 숫자가 1씩 커졌습니다.", x=548, y=184, font_size=22, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center")

    # 두 번째 선택 줄: ➡ ( 10000 , 100000 , 1000000 )씩 뛰어 세었습니다.
    g2_left = TextSlot(id="slot.choice.g2_left", prompt="", text="→ (", x=186, y=236, font_size=24, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center")
    g2_0 = TextSlot(
        id="slot.choice.g2_option_0",
        prompt="",
        text="10000",
        x=250,
        y=236,
        font_size=22,
        font_family='"Noto Sans KR", sans-serif',
        fill="#111827",
        align="center",
        interaction={"type": "choice", "role": "answer", "choice_index": 0, "value": "10000", "group_id": "slot.choice.group_2", "include_in_submission": True},
    )
    g2_c0 = TextSlot(id="slot.choice.g2_c0", prompt="", text=",", x=298, y=236, font_size=22, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center")
    g2_1 = TextSlot(
        id="slot.choice.g2_option_1",
        prompt="",
        text="100000",
        x=352,
        y=236,
        font_size=22,
        font_family='"Noto Sans KR", sans-serif',
        fill="#111827",
        align="center",
        interaction={"type": "choice", "role": "answer", "choice_index": 1, "value": "100000", "group_id": "slot.choice.group_2", "include_in_submission": True},
    )
    g2_c1 = TextSlot(id="slot.choice.g2_c1", prompt="", text=",", x=406, y=236, font_size=22, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center")
    g2_2 = TextSlot(
        id="slot.choice.g2_option_2",
        prompt="",
        text="1000000",
        x=466,
        y=236,
        font_size=22,
        font_family='"Noto Sans KR", sans-serif',
        fill="#111827",
        align="center",
        interaction={"type": "choice", "role": "answer", "choice_index": 2, "value": "1000000", "group_id": "slot.choice.group_2", "include_in_submission": True},
    )
    g2_right = TextSlot(id="slot.choice.g2_right", prompt="", text=")씩 뛰어 세었습니다.", x=626, y=236, font_size=22, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center")

    diagram_slot_ids = tuple(s.id for s in diagram_slots)

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
            Region(id="region.diagram", role="diagram", flow="absolute", slot_ids=diagram_slot_ids),
            Region(
                id="region.choices",
                role="choices",
                flow="absolute",
                slot_ids=(
                    "slot.choice.g1_left",
                    "slot.choice.g1_option_0",
                    "slot.choice.g1_c0",
                    "slot.choice.g1_option_1",
                    "slot.choice.g1_c1",
                    "slot.choice.g1_option_2",
                    "slot.choice.g1_right",
                    "slot.choice.g2_left",
                    "slot.choice.g2_option_0",
                    "slot.choice.g2_c0",
                    "slot.choice.g2_option_1",
                    "slot.choice.g2_c1",
                    "slot.choice.g2_option_2",
                    "slot.choice.g2_right",
                ),
            ),
        ),
        slots=(
            stem_text_slot,
            *diagram_slots,
            g1_left,
            g1_0,
            g1_c0,
            g1_1,
            g1_c1,
            g1_2,
            g1_right,
            g2_left,
            g2_0,
            g2_c0,
            g2_1,
            g2_c1,
            g2_2,
            g2_right,
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
        {"ref": "seq_0", "value": 206000},
        {"ref": "seq_1", "value": 306000},
        {"ref": "seq_2", "value": 406000},
    ],
    "target": {"ref": "slot.choice.g2_option_1", "label": "변하는 자리와 뛰어 센 값", "unit": ""},
    "method": "skip_counting_pattern",
    "steps": [
        {
            "id": "find_place_and_step",
            "expr": "306000 - 206000 = 100000",
            "explanation": "십만의 자리 숫자가 1씩 커지므로 100000씩 뛰어 세었습니다.",
            "value": ["십만", "100000"],
        },
    ],
    "answer": ANSWER,
}


if __name__ == "__main__":
    print(f"[{PROBLEM_TEMPLATE.id}] 템플릿 컴파일 성공!")
    print(f"- 제목: {PROBLEM_TEMPLATE.title}")
    print(f"- 캔버스: {PROBLEM_TEMPLATE.canvas.width} x {PROBLEM_TEMPLATE.canvas.height}")
    print(f"- 구역 수: {len(PROBLEM_TEMPLATE.regions)}")
