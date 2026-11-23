"""ModuMath Problem DSL: 뛰어 센 규칙 찾기 (S3_초등_4_007949)"""

from __future__ import annotations

from modu_math.dsl import (
    Canvas,
    CircleSlot,
    LineSlot,
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
PROBLEM_ID = "S3_초등_4_007949"
PROBLEM_TITLE = "조 단위 뛰어 세기 규칙 찾기"


# ==============================================================================
# 2. 정답 및 오답 진단 정의 (Answer & Diagnostic Key)
# ==============================================================================
ANSWER = {
    "value": "100조",
    "answer_index": 1,
    "unit": "",
    "values": ["100조"],
    "choices": [
        "10조",
        "100조",
        "1000조",
    ],
    "blanks": [],
    "answer_key": [
        {
            "slot_id": "slot.choice.option_1",
            "value": "100조",
            "diagnostics": [
                {
                    "id": "diag.wrong_step_10jo",
                    "condition": "answer_equals_10jo",
                    "concept": "뛰어 세기",
                    "reason": "백조의 자리가 아닌 십조의 자리가 커진 것으로 오인함",
                    "feedback": "6390조 → 6490조 → 6590조에서 변하는 자리 숫자는 3, 4, 5(백조의 자리)입니다.",
                },
                {
                    "id": "diag.wrong_step_1000jo",
                    "condition": "answer_equals_1000jo",
                    "concept": "뛰어 세기",
                    "reason": "백조의 자리가 아닌 천조의 자리가 커진 것으로 오인함",
                    "feedback": "천조의 자리(6)는 그대로이고 백조의 자리 숫자가 1씩 커지므로 100조씩 뛰어 세었습니다.",
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
        "seq_0": {"label": "첫째 칸", "value": "6390조"},
        "seq_1": {"label": "둘째 칸", "value": "6490조"},
        "seq_2": {"label": "셋째 칸", "value": "6590조"},
        "step": {"label": "뛰어 센 값", "value": "100조"},
    },
    "relations": [
        {
            "type": "skip_counting",
            "sequence": ["seq_0", "seq_1", "seq_2"],
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
        text="7. 뛰어 센 것을 보고 알맞은 것을 선택하세요.",
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

    # 기관차 (x=70..200, y=100..220)
    diagram_slots.extend([
        RectSlot(id="slot.diagram.loco_chimney", prompt="", x=165, y=82, width=22, height=30, fill="#d9f99d", stroke="#4d7c0f", stroke_width=1.5, rx=3, ry=3),
        PolygonSlot(id="slot.diagram.loco_body", prompt="", points=[(85, 200), (105, 130), (155, 112), (200, 112), (200, 200)], fill="#bef264", stroke="#4d7c0f", stroke_width=1.5),
        RectSlot(id="slot.diagram.loco_window", prompt="", x=162, y=126, width=28, height=34, fill="#e0f2fe", stroke="#4d7c0f", stroke_width=1.5, rx=4, ry=4),
        RectSlot(id="slot.diagram.loco_base", prompt="", x=74, y=200, width=130, height=16, fill="#fdba74", stroke="#c2410c", stroke_width=1.5, rx=6, ry=6),
        CircleSlot(id="slot.diagram.loco_w1", prompt="", cx=100, cy=224, r=14, fill="#9ca3af", stroke="#374151", stroke_width=1.5),
        CircleSlot(id="slot.diagram.loco_w2", prompt="", cx=140, cy=224, r=14, fill="#9ca3af", stroke="#374151", stroke_width=1.5),
        CircleSlot(id="slot.diagram.loco_w3", prompt="", cx=182, cy=224, r=14, fill="#9ca3af", stroke="#374151", stroke_width=1.5),
    ])

    car_texts = ["6390조", "6490조", "6590조", "", ""]
    for idx, label in enumerate(car_texts):
        cx = 222 + idx * 126
        # 연결선
        diagram_slots.append(
            LineSlot(
                id=f"slot.diagram.link_{idx}",
                prompt="",
                x1=cx - 18,
                y1=168,
                x2=cx,
                y2=168,
                stroke="#374151",
                stroke_width=3,
            )
        )
        diagram_slots.append(
            RectSlot(
                id=f"slot.diagram.car_body_{idx}",
                prompt="",
                x=cx,
                y=114,
                width=108,
                height=86,
                fill="#bef264",
                stroke="#4d7c0f",
                stroke_width=1.5,
                rx=6,
                ry=6,
            )
        )
        diagram_slots.append(
            RectSlot(
                id=f"slot.diagram.car_panel_{idx}",
                prompt="",
                x=cx + 10,
                y=130,
                width=88,
                height=52,
                fill="#ffffff" if not label else "#d9f99d",
                stroke="#4d7c0f",
                stroke_width=1.2,
                rx=4,
                ry=4,
            )
        )
        if label:
            diagram_slots.append(
                TextSlot(
                    id=f"slot.diagram.car_text_{idx}",
                    prompt="",
                    text=label,
                    x=cx + 54,
                    y=144,
                    font_size=20,
                    font_family='"Noto Sans KR", sans-serif',
                    fill="#111827",
                    align="center",
                )
            )
        diagram_slots.append(
            RectSlot(
                id=f"slot.diagram.car_base_{idx}",
                prompt="",
                x=cx - 2,
                y=200,
                width=112,
                height=16,
                fill="#fdba74",
                stroke="#c2410c",
                stroke_width=1.5,
                rx=6,
                ry=6,
            )
        )
        diagram_slots.append(
            CircleSlot(
                id=f"slot.diagram.car_w1_{idx}",
                prompt="",
                cx=cx + 26,
                cy=224,
                r=13,
                fill="#9ca3af",
                stroke="#374151",
                stroke_width=1.5,
            )
        )
        diagram_slots.append(
            CircleSlot(
                id=f"slot.diagram.car_w2_{idx}",
                prompt="",
                cx=cx + 82,
                cy=224,
                r=13,
                fill="#9ca3af",
                stroke="#374151",
                stroke_width=1.5,
            )
        )

    # 선택 영역: ( 10조 , 100조 , 1000조 )씩 뛰어 세었습니다.
    paren_left = TextSlot(id="slot.choice.paren_left", prompt="", text="(", x=200, y=268, font_size=24, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center")
    choice_0 = TextSlot(
        id="slot.choice.option_0",
        prompt="",
        text="10조",
        x=248,
        y=268,
        font_size=22,
        font_family='"Noto Sans KR", sans-serif',
        fill="#111827",
        align="center",
        interaction={
            "type": "choice",
            "role": "answer",
            "choice_index": 0,
            "value": "10조",
            "group_id": "slot.choice.group",
            "include_in_submission": True,
        },
    )
    comma_0 = TextSlot(id="slot.choice.comma_0", prompt="", text=",", x=290, y=268, font_size=22, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center")
    choice_1 = TextSlot(
        id="slot.choice.option_1",
        prompt="",
        text="100조",
        x=340,
        y=268,
        font_size=22,
        font_family='"Noto Sans KR", sans-serif',
        fill="#111827",
        align="center",
        interaction={
            "type": "choice",
            "role": "answer",
            "choice_index": 1,
            "value": "100조",
            "group_id": "slot.choice.group",
            "include_in_submission": True,
        },
    )
    comma_1 = TextSlot(id="slot.choice.comma_1", prompt="", text=",", x=390, y=268, font_size=22, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center")
    choice_2 = TextSlot(
        id="slot.choice.option_2",
        prompt="",
        text="1000조",
        x=445,
        y=268,
        font_size=22,
        font_family='"Noto Sans KR", sans-serif',
        fill="#111827",
        align="center",
        interaction={
            "type": "choice",
            "role": "answer",
            "choice_index": 2,
            "value": "1000조",
            "group_id": "slot.choice.group",
            "include_in_submission": True,
        },
    )
    paren_right = TextSlot(id="slot.choice.paren_right", prompt="", text=")씩 뛰어 세었습니다.", x=600, y=268, font_size=22, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center")

    diagram_slot_ids = tuple(s.id for s in diagram_slots)

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
            Region(id="region.diagram", role="diagram", flow="absolute", slot_ids=diagram_slot_ids),
            Region(
                id="region.choices",
                role="choices",
                flow="absolute",
                slot_ids=(
                    "slot.choice.paren_left",
                    "slot.choice.option_0",
                    "slot.choice.comma_0",
                    "slot.choice.option_1",
                    "slot.choice.comma_1",
                    "slot.choice.option_2",
                    "slot.choice.paren_right",
                ),
            ),
        ),
        slots=(
            stem_text_slot,
            *diagram_slots,
            paren_left,
            choice_0,
            comma_0,
            choice_1,
            comma_1,
            choice_2,
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
        {"ref": "seq_0", "value": "6390조"},
        {"ref": "seq_1", "value": "6490조"},
        {"ref": "seq_2", "value": "6590조"},
    ],
    "target": {"ref": "slot.choice.option_1", "label": "뛰어 센 값", "unit": ""},
    "method": "skip_counting_difference",
    "steps": [
        {
            "id": "find_step_value",
            "expr": "6490조 - 6390조 = 100조",
            "explanation": "100조의 자리 숫자가 1씩 커지므로 100조씩 뛰어 세었습니다.",
            "value": "100조",
        },
    ],
    "answer": ANSWER,
}


if __name__ == "__main__":
    print(f"[{PROBLEM_TEMPLATE.id}] 템플릿 컴파일 성공!")
    print(f"- 제목: {PROBLEM_TEMPLATE.title}")
    print(f"- 캔버스: {PROBLEM_TEMPLATE.canvas.width} x {PROBLEM_TEMPLATE.canvas.height}")
    print(f"- 구역 수: {len(PROBLEM_TEMPLATE.regions)}")
