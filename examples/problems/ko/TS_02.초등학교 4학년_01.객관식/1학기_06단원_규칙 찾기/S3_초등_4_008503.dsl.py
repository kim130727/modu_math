"""ModuMath Problem DSL: 사각형 배열에서 다섯째 도형 찾기 (S3_초등_4_008503)"""

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
PROBLEM_ID = "S3_초등_4_008503"
PROBLEM_TITLE = "도형의 배열에서 다섯째에 알맞은 도형 선택하기"


# ==============================================================================
# 2. 정답 및 오답 진단 정의 (Answer & Diagnostic Key)
# ==============================================================================
ANSWER = {
    "value": "①",
    "answer_index": 0,
    "unit": "",
    "values": ["①"],
    "choices": [
        "①",
        "②",
    ],
    "blanks": [],
    "answer_key": [
        {
            "slot_id": "slot.choice.option_0",
            "value": "①",
            "diagnostics": [
                {
                    "id": "diag.wrong_count_5",
                    "condition": "answer_equals_2",
                    "concept": "도형 배열의 규칙",
                    "reason": "넷째와 같은 5개짜리 도형(②)을 다섯째 도형으로 선택함",
                    "feedback": "사각형의 개수가 2개에서 시작하여 1개씩 늘어나는 규칙이므로 다섯째에는 사각형이 6개(①)입니다.",
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
    "problem_type": "multiple_choice_shape_pattern",
    "metadata": {
        "school": "초등학교",
        "grade": 4,
        "semester": "1학기",
        "chapter": "06단원_규칙 찾기",
        "difficulty": "하",
    },
    "entities": {
        "step_1": {"label": "첫째", "count": 2},
        "step_2": {"label": "둘째", "count": 3},
        "step_3": {"label": "셋째", "count": 4},
        "step_4": {"label": "넷째", "count": 5},
        "option_0": {"label": "①", "count": 6, "is_correct": True},
        "option_1": {"label": "②", "count": 5, "is_correct": False},
    },
    "relations": [
        {
            "type": "arithmetic_shape_growth",
            "start": 2,
            "step": 1,
            "target_index": 5,
            "target_count": 6,
        }
    ],
}


# ==============================================================================
# 4. 문제 템플릿 빌더 (ProblemTemplate Builder)
# ==============================================================================
def _add_strip(slots: list, prefix: str, sx: int, sy: int, count: int, horizontal: bool, green_idx: int, sz: int = 22) -> None:
    for i in range(count):
        bx = sx + (i * sz if horizontal else 0)
        by = sy + (0 if horizontal else i * sz)
        is_green = i == green_idx
        slots.append(
            RectSlot(
                id=f"slot.diagram.{prefix}_s_{i}",
                prompt="",
                x=bx,
                y=by,
                width=sz,
                height=sz,
                fill="#86efac" if is_green else "#fbcfe8",
                stroke="#16a34a" if is_green else "#ec4899",
                stroke_width=1.4,
            )
        )


def build_problem_template() -> ProblemTemplate:
    """문제의 캔버스 크기, 슬롯(텍스트/도형/선택지), 리전(구역)을 정의합니다."""

    stem_text_slot = TextBoxSlot(
        id="slot.stem.question",
        prompt="",
        text="30. 도형의 배열을 보고 다섯째에 알맞은 도형을 아래에서 찾아 선택하세요.",
        x=32,
        y=20,
        width=820,
        height=44,
        font_size=21,
        font_family='"Noto Sans KR", sans-serif',
        fill="#202124",
        align="left",
        valign="top",
        line_height=1.45,
    )

    diagram_slots = [
        TextSlot(id="slot.diagram.t0", prompt="", text="첫째", x=148, y=74, font_size=16, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center"),
        TextSlot(id="slot.diagram.t1", prompt="", text="둘째", x=318, y=74, font_size=16, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center"),
        TextSlot(id="slot.diagram.t2", prompt="", text="셋째", x=508, y=74, font_size=16, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center"),
        TextSlot(id="slot.diagram.t3", prompt="", text="넷째", x=724, y=74, font_size=16, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center"),
    ]
    _add_strip(diagram_slots, "st0", 126, 134, 2, True, 1)
    _add_strip(diagram_slots, "st1", 307, 118, 3, False, 2)
    _add_strip(diagram_slots, "st2", 464, 134, 4, True, 0)
    _add_strip(diagram_slots, "st3", 713, 98, 5, False, 0)

    # 선택지 ① (6개 - 정답)
    card_0 = RectSlot(id="slot.choice.option_0", prompt="", x=176, y=236, width=250, height=58, fill="#ffffff", stroke="#a855f7", stroke_width=1.5, rx=8, ry=8, interaction={"type": "choice", "role": "answer", "choice_index": 0, "value": "①", "group_id": "slot.choice.group", "include_in_submission": True})
    diagram_slots.append(TextSlot(id="slot.diagram.b0", prompt="", text="①", x=196, y=252, font_size=18, font_family='"Noto Sans KR", sans-serif', fill="#4b5563", align="center"))
    _add_strip(diagram_slots, "opt0", 232, 254, 6, True, 5, sz=22)

    # 선택지 ② (5개 - 오답)
    card_1 = RectSlot(id="slot.choice.option_1", prompt="", x=460, y=236, width=250, height=58, fill="#ffffff", stroke="#a855f7", stroke_width=1.5, rx=8, ry=8, interaction={"type": "choice", "role": "answer", "choice_index": 1, "value": "②", "group_id": "slot.choice.group", "include_in_submission": True})
    diagram_slots.append(TextSlot(id="slot.diagram.b1", prompt="", text="②", x=480, y=252, font_size=18, font_family='"Noto Sans KR", sans-serif', fill="#4b5563", align="center"))
    _add_strip(diagram_slots, "opt1", 522, 254, 5, True, 0, sz=22)

    return ProblemTemplate(
        id=PROBLEM_ID,
        title=PROBLEM_TITLE,
        canvas=Canvas(
            width=886,
            height=316,
            coordinate_mode="logical",
        ),
        regions=(
            Region(id="region.stem", role="stem", flow="absolute", slot_ids=("slot.stem.question",)),
            Region(id="region.choices", role="choices", flow="absolute", slot_ids=("slot.choice.option_0", "slot.choice.option_1")),
            Region(id="region.diagram", role="diagram", flow="absolute", slot_ids=tuple(s.id for s in diagram_slots)),
        ),
        slots=(
            stem_text_slot,
            card_0,
            card_1,
            *diagram_slots,
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
        {"ref": "step_1", "value": 2},
        {"ref": "step_4", "value": 5},
    ],
    "target": {"ref": "slot.choice.option_0", "label": "다섯째 도형", "unit": ""},
    "method": "arithmetic_sequence_pattern",
    "steps": [
        {
            "id": "find_fifth_count",
            "expr": "2, 3, 4, 5, 6",
            "explanation": "사각형의 개수가 2개에서 시작하여 1개씩 늘어나므로 다섯째에는 6개(①)입니다.",
            "value": "①",
        },
    ],
    "answer": ANSWER,
}


if __name__ == "__main__":
    print(f"[{PROBLEM_TEMPLATE.id}] 템플릿 컴파일 성공!")
    print(f"- 제목: {PROBLEM_TEMPLATE.title}")
    print(f"- 캔버스: {PROBLEM_TEMPLATE.canvas.width} x {PROBLEM_TEMPLATE.canvas.height}")
    print(f"- 구역 수: {len(PROBLEM_TEMPLATE.regions)}")
