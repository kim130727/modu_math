"""ModuMath Problem DSL: 도형의 배열에서 여섯째 도형 찾기 (S3_초등_4_008497)"""

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
PROBLEM_ID = "S3_초등_4_008497"
PROBLEM_TITLE = "도형의 회전·증가 규칙을 찾아 여섯째 도형 선택하기"


# ==============================================================================
# 2. 정답 및 오답 진단 정의 (Answer & Diagnostic Key)
# ==============================================================================
ANSWER = {
    "value": "②",
    "answer_index": 1,
    "unit": "",
    "values": ["②"],
    "choices": [
        "①",
        "②",
    ],
    "blanks": [],
    "answer_key": [
        {
            "slot_id": "slot.choice.option_1",
            "value": "②",
            "diagnostics": [
                {
                    "id": "diag.wrong_direction_increase",
                    "condition": "answer_equals_1",
                    "concept": "도형 배열의 규칙",
                    "reason": "다섯째 도형에서 아래쪽이 아닌 위쪽으로 1개 늘어난 도형(①)을 선택함",
                    "feedback": "○ 표시된 사각형을 중심으로 시계 반대 방향(왼쪽 → 아래 → 오른쪽 → 위 → 왼쪽 → 아래)으로 1개씩 늘어납니다. 여섯째에는 아래쪽으로 1개 더 늘어납니다.",
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
        "difficulty": "중",
    },
    "entities": {
        "step_1": {"label": "첫째", "blocks": 2},
        "step_5": {"label": "다섯째", "blocks": 6},
        "option_0": {"label": "①", "is_correct": False},
        "option_1": {"label": "②", "is_correct": True},
    },
    "relations": [
        {
            "type": "counterclockwise_growth",
            "correct_entity": "option_1",
            "distractor": "option_0",
        }
    ],
}


# ==============================================================================
# 4. 문제 템플릿 빌더 (ProblemTemplate Builder)
# ==============================================================================
def _add_block_figure(slots: list, prefix: str, cx: int, cy: int, offsets: list[tuple[int, int]], sz: int = 24) -> None:
    for idx, (ox, oy) in enumerate(offsets):
        bx = cx + ox * sz - sz // 2
        by = cy + oy * sz - sz // 2
        slots.append(RectSlot(id=f"slot.diagram.{prefix}_b_{idx}", prompt="", x=bx, y=by, width=sz, height=sz, fill="#93c5fd", stroke="#2563eb", stroke_width=1.2))
    slots.append(CircleSlot(id=f"slot.diagram.{prefix}_ring", prompt="", cx=cx, cy=cy, r=round(sz * 0.34, 1), fill="none", stroke="#ec4899", stroke_width=1.6))


def build_problem_template() -> ProblemTemplate:
    """문제의 캔버스 크기, 슬롯(텍스트/도형/선택지), 리전(구역)을 정의합니다."""

    stem_text_slot = TextBoxSlot(
        id="slot.stem.question",
        prompt="",
        text="23. 도형의 배열에서 규칙을 찾아 여섯째에 올 도형을 선택하세요.",
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

    diagram_slots = []
    titles = ["첫째", "둘째", "셋째", "넷째", "다섯째"]
    xs = [126, 266, 426, 606, 786]
    patterns = [
        [(0, 0), (-1, 0)],
        [(0, 0), (-1, 0), (0, 1)],
        [(0, 0), (-1, 0), (0, 1), (1, 0)],
        [(0, 0), (-1, 0), (0, 1), (1, 0), (0, -1)],
        [(0, 0), (-1, 0), (0, 1), (1, 0), (0, -1), (-2, 0)],
    ]
    for i, (t, x, pat) in enumerate(zip(titles, xs, patterns)):
        diagram_slots.append(TextSlot(id=f"slot.diagram.t_{i}", prompt="", text=t, x=x, y=72, font_size=16, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center"))
        _add_block_figure(diagram_slots, f"p{i}", x, 134, pat, sz=22)

    # 선택지 ① (위쪽 2칸 - 오답)
    card_0 = RectSlot(id="slot.choice.option_0", prompt="", x=186, y=198, width=220, height=166, fill="#ffffff", stroke="#e5e7eb", stroke_width=1.5, rx=10, ry=10, interaction={"type": "choice", "role": "answer", "choice_index": 0, "value": "①", "group_id": "slot.choice.group", "include_in_submission": True})
    diagram_slots.append(TextSlot(id="slot.diagram.b0", prompt="", text="①", x=208, y=212, font_size=18, font_family='"Noto Sans KR", sans-serif', fill="#4b5563", align="center"))
    _add_block_figure(diagram_slots, "opt0", 306, 294, [(0, 0), (-1, 0), (-2, 0), (0, 1), (1, 0), (0, -1), (0, -2)], sz=22)

    # 선택지 ② (아래쪽 2칸 - 정답)
    card_1 = RectSlot(id="slot.choice.option_1", prompt="", x=480, y=198, width=220, height=166, fill="#ffffff", stroke="#e5e7eb", stroke_width=1.5, rx=10, ry=10, interaction={"type": "choice", "role": "answer", "choice_index": 1, "value": "②", "group_id": "slot.choice.group", "include_in_submission": True})
    diagram_slots.append(TextSlot(id="slot.diagram.b1", prompt="", text="②", x=502, y=212, font_size=18, font_family='"Noto Sans KR", sans-serif', fill="#4b5563", align="center"))
    _add_block_figure(diagram_slots, "opt1", 600, 274, [(0, 0), (-1, 0), (-2, 0), (0, 1), (0, 2), (1, 0), (0, -1)], sz=22)

    return ProblemTemplate(
        id=PROBLEM_ID,
        title=PROBLEM_TITLE,
        canvas=Canvas(
            width=886,
            height=384,
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
        {"ref": "step_5", "value": 6},
    ],
    "target": {"ref": "slot.choice.option_1", "label": "여섯째 도형", "unit": ""},
    "method": "spatial_growth_pattern",
    "steps": [
        {
            "id": "find_sixth_figure",
            "expr": "②",
            "explanation": "○ 표시된 사각형을 중심으로 시계 반대 방향으로 1개씩 늘어나므로 여섯째는 아래쪽으로 1개 더 늘어난 ②입니다.",
            "value": "②",
        },
    ],
    "answer": ANSWER,
}


if __name__ == "__main__":
    print(f"[{PROBLEM_TEMPLATE.id}] 템플릿 컴파일 성공!")
    print(f"- 제목: {PROBLEM_TEMPLATE.title}")
    print(f"- 캔버스: {PROBLEM_TEMPLATE.canvas.width} x {PROBLEM_TEMPLATE.canvas.height}")
    print(f"- 구역 수: {len(PROBLEM_TEMPLATE.regions)}")
