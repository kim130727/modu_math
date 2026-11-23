"""ModuMath Problem DSL: 물결선 꺾은선그래프에서 중간 값 예상하기 (S3_초등_4_007720)"""

from __future__ import annotations

from modu_math.dsl import (
    Canvas,
    CircleSlot,
    LineSlot,
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
PROBLEM_ID = "S3_초등_4_007720"
PROBLEM_TITLE = "9월 16일의 지혜의 몸무게 예상하기"


# ==============================================================================
# 2. 정답 및 오답 진단 정의 (Answer & Diagnostic Key)
# ==============================================================================
ANSWER = {
    "value": "33.1 kg",
    "answer_index": 1,
    "unit": "kg",
    "values": ["33.1 kg"],
    "choices": [
        "33 kg",
        "33.1 kg",
        "33.2 kg",
    ],
    "blanks": [],
    "answer_key": [
        {
            "slot_id": "slot.choice.option_1",
            "value": "33.1 kg",
            "diagnostics": [
                {
                    "id": "diag.chose_sep_1",
                    "condition": "answer_equals_33",
                    "concept": "꺾은선그래프의 중간값 예상",
                    "reason": "9월 1일의 몸무게(33 kg)를 그대로 선택함",
                    "feedback": "9월 16일은 9월 1일(33 kg)과 10월 1일(33.2 kg)의 중간이므로, 몸무게도 두 값의 중간인 33.1 kg이었을 것입니다.",
                },
                {
                    "id": "diag.chose_oct_1",
                    "condition": "answer_equals_33_2",
                    "concept": "꺾은선그래프의 중간값 예상",
                    "reason": "10월 1일의 몸무게(33.2 kg)를 그대로 선택함",
                    "feedback": "9월 1일(33 kg)과 10월 1일(33.2 kg) 사이의 가운데 값을 읽으면 33.1 kg입니다.",
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
    "problem_type": "multiple_choice_line_chart_interpolation",
    "metadata": {
        "school": "초등학교",
        "grade": 4,
        "semester": "1학기",
        "chapter": "05단원_막대그래프",
        "difficulty": "중",
    },
    "entities": {
        "sep_1": {"label": "9월 1일", "value": 33.0, "unit": "kg"},
        "oct_1": {"label": "10월 1일", "value": 33.2, "unit": "kg"},
        "sep_16": {"label": "9월 16일", "value": 33.1, "unit": "kg"},
    },
    "relations": [
        {
            "type": "midpoint_interpolation",
            "expression": "(33.0 + 33.2) / 2 = 33.1",
            "target": "sep_16",
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
        text="10. 지혜의 몸무게를 매월 1일에 조사하여 나타낸 꺾은선그래프입니다. 9월 16일의 지혜의 몸무게는 몇 kg이었을까요?",
        x=32,
        y=20,
        width=820,
        height=52,
        font_size=21,
        font_family='"Noto Sans KR", sans-serif',
        fill="#202124",
        align="left",
        valign="top",
        line_height=1.45,
    )

    diagram_slots = [
        TextSlot(id="slot.diagram.title", prompt="", text="지혜의 몸무게", x=443, y=78, font_size=18, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center"),
        RectSlot(id="slot.diagram.frame", prompt="", x=233, y=104, width=420, height=156, fill="#ffffff", stroke="#6b7280", stroke_width=1.2),
        RectSlot(id="slot.diagram.ybox", prompt="", x=233, y=104, width=96, height=124, fill="#ffffff", stroke="#6b7280", stroke_width=1),
        RectSlot(id="slot.diagram.xbox", prompt="", x=329, y=228, width=324, height=32, fill="#ffffff", stroke="#6b7280", stroke_width=1),
        LineSlot(id="slot.diagram.diag", prompt="", x1=233, y1=260, x2=329, y2=228, stroke="#6b7280", stroke_width=1),
        TextSlot(id="slot.diagram.unit", prompt="", text="(kg)", x=258, y=110, font_size=13, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center"),
        PathSlot(id="slot.diagram.wavy", prompt="", d="M 233 212 Q 338 204, 443 212 T 653 212", fill="none", stroke="#6b7280", stroke_width=1.4),
    ]

    for lbl, gy in [("32", 196), ("32.5", 168), ("33", 140), ("33.5", 112)]:
        diagram_slots.append(LineSlot(id=f"slot.diagram.grid_{lbl}", prompt="", x1=329, y1=gy, x2=653, y2=gy, stroke="#9ca3af", stroke_width=0.9))
        diagram_slots.append(TextSlot(id=f"slot.diagram.ylbl_{lbl}", prompt="", text=lbl, x=320, y=gy - 6, font_size=11, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="end"))

    months = ["7", "8", "9", "10", "11"]
    vals = [32.2, 32.4, 33.0, 33.2, 33.3]
    pts = []
    for i, (m, val) in enumerate(zip(months, vals)):
        px = 378 + i * 54
        py = round(196 - (val - 32.0) * 56, 1)
        pts.append((px, py))
        diagram_slots.append(LineSlot(id=f"slot.diagram.vgrid_{i}", prompt="", x1=px, y1=104, x2=px, y2=228, stroke="#9ca3af", stroke_width=0.9))
        diagram_slots.append(TextSlot(id=f"slot.diagram.xlbl_{i}", prompt="", text=m, x=px, y=234, font_size=13, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center"))

    for i in range(len(pts) - 1):
        diagram_slots.append(LineSlot(id=f"slot.diagram.seg_{i}", prompt="", x1=pts[i][0], y1=pts[i][1], x2=pts[i + 1][0], y2=pts[i + 1][1], stroke="#ec4899", stroke_width=2))
    for i, (px, py) in enumerate(pts):
        diagram_slots.append(CircleSlot(id=f"slot.diagram.dot_{i}", prompt="", cx=px, cy=py, r=3, fill="#111827", stroke="#111827", stroke_width=1))

    p_l = TextSlot(id="slot.choice.p_l", prompt="", text="(", x=470, y=280, font_size=22, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center")
    c0 = TextSlot(id="slot.choice.option_0", prompt="", text="33 kg", x=520, y=280, font_size=20, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center", interaction={"type": "choice", "role": "answer", "choice_index": 0, "value": "33 kg", "group_id": "slot.choice.group", "include_in_submission": True})
    cm0 = TextSlot(id="slot.choice.cm0", prompt="", text=",", x=562, y=280, font_size=20, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center")
    c1 = TextSlot(id="slot.choice.option_1", prompt="", text="33.1 kg", x=612, y=280, font_size=20, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center", interaction={"type": "choice", "role": "answer", "choice_index": 1, "value": "33.1 kg", "group_id": "slot.choice.group", "include_in_submission": True})
    cm1 = TextSlot(id="slot.choice.cm1", prompt="", text=",", x=662, y=280, font_size=20, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center")
    c2 = TextSlot(id="slot.choice.option_2", prompt="", text="33.2 kg", x=712, y=280, font_size=20, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center", interaction={"type": "choice", "role": "answer", "choice_index": 2, "value": "33.2 kg", "group_id": "slot.choice.group", "include_in_submission": True})
    p_r = TextSlot(id="slot.choice.p_r", prompt="", text=")", x=764, y=280, font_size=22, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center")

    choice_slots = (p_l, c0, cm0, c1, cm1, c2, p_r)

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
            Region(id="region.diagram", role="diagram", flow="absolute", slot_ids=tuple(s.id for s in diagram_slots)),
            Region(id="region.choices", role="choices", flow="absolute", slot_ids=tuple(s.id for s in choice_slots)),
        ),
        slots=(
            stem_text_slot,
            *diagram_slots,
            *choice_slots,
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
        {"ref": "sep_1", "value": 33.0, "unit": "kg"},
        {"ref": "oct_1", "value": 33.2, "unit": "kg"},
    ],
    "target": {"ref": "slot.choice.option_1", "label": "9월 16일의 몸무게", "unit": "kg"},
    "method": "linear_midpoint_interpolation",
    "steps": [
        {
            "id": "interpolate_midpoint",
            "expr": "(33.0 + 33.2) / 2 = 33.1",
            "explanation": "9월 1일(33 kg)과 10월 1일(33.2 kg)의 중간인 33.1 kg입니다.",
            "value": "33.1 kg",
        },
    ],
    "answer": ANSWER,
}


if __name__ == "__main__":
    print(f"[{PROBLEM_TEMPLATE.id}] 템플릿 컴파일 성공!")
    print(f"- 제목: {PROBLEM_TEMPLATE.title}")
    print(f"- 캔버스: {PROBLEM_TEMPLATE.canvas.width} x {PROBLEM_TEMPLATE.canvas.height}")
    print(f"- 구역 수: {len(PROBLEM_TEMPLATE.regions)}")
