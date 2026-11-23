"""ModuMath Problem DSL: 꺾은선그래프의 가로와 세로 축 알기 (S3_초등_4_007718)"""

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
PROBLEM_ID = "S3_초등_4_007718"
PROBLEM_TITLE = "월별 강수량 꺾은선그래프의 가로와 세로 찾기"


# ==============================================================================
# 2. 정답 및 오답 진단 정의 (Answer & Diagnostic Key)
# ==============================================================================
ANSWER = {
    "value": ["월", "강수량"],
    "unit": "",
    "values": ["월", "강수량"],
    "choices": [
        "월",
        "강수량",
    ],
    "blanks": [],
    "answer_key": [
        {
            "slot_id": "slot.choice.g1_option_0",
            "value": "월",
            "diagnostics": [
                {
                    "id": "diag.swapped_axes",
                    "condition": "answer_equals_rainfall_first",
                    "concept": "꺾은선그래프의 가로와 세로",
                    "reason": "가로축(월)과 세로축(강수량)을 반대로 선택함",
                    "feedback": "꺾은선그래프의 가로는 '월', 세로는 '강수량'(mm)을 나타냅니다.",
                },
            ],
        },
        {
            "slot_id": "slot.choice.g2_option_1",
            "value": "강수량",
        },
    ],
}


# ==============================================================================
# 3. 시맨틱 모델 정의 (Semantic Model & Metadata)
# ==============================================================================
SEMANTIC = {
    "problem_id": PROBLEM_ID,
    "problem_type": "multiple_choice_chart_axes",
    "metadata": {
        "school": "초등학교",
        "grade": 4,
        "semester": "1학기",
        "chapter": "05단원_막대그래프",
        "difficulty": "하",
    },
    "entities": {
        "horizontal_axis": {"label": "가로", "value": "월"},
        "vertical_axis": {"label": "세로", "value": "강수량", "unit": "mm"},
    },
    "relations": [
        {
            "type": "chart_axis_mapping",
            "horizontal": "월",
            "vertical": "강수량",
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
        text="7. 어느 지역의 월별 강수량을 조사하여 나타낸 꺾은선그래프입니다. 꺾은선그래프의 가로와 세로는 각각 무엇을 나타내나요?",
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
        TextSlot(id="slot.diagram.title", prompt="", text="월별 강수량", x=443, y=80, font_size=18, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center"),
        RectSlot(id="slot.diagram.frame", prompt="", x=243, y=106, width=400, height=138, fill="#ffffff", stroke="#6b7280", stroke_width=1.2),
        RectSlot(id="slot.diagram.ybox", prompt="", x=243, y=106, width=96, height=106, fill="#ffffff", stroke="#6b7280", stroke_width=1),
        RectSlot(id="slot.diagram.xbox", prompt="", x=339, y=212, width=304, height=32, fill="#ffffff", stroke="#6b7280", stroke_width=1),
        LineSlot(id="slot.diagram.diag", prompt="", x1=243, y1=244, x2=339, y2=212, stroke="#6b7280", stroke_width=1),
        TextSlot(id="slot.diagram.unit", prompt="", text="(mm)", x=270, y=112, font_size=13, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center"),
        TextSlot(id="slot.diagram.wy", prompt="", text="강수량", x=268, y=218, font_size=12, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center"),
        TextSlot(id="slot.diagram.wx", prompt="", text="월", x=318, y=224, font_size=12, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center"),
    ]

    for v in range(0, 51, 10):
        gy = round(212 - (v / 55) * 96, 1)
        diagram_slots.append(LineSlot(id=f"slot.diagram.grid_{v}", prompt="", x1=339, y1=gy, x2=643, y2=gy, stroke="#9ca3af", stroke_width=0.9))
        diagram_slots.append(TextSlot(id=f"slot.diagram.ylbl_{v}", prompt="", text=str(v), x=328, y=gy - 6, font_size=12, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="end"))

    months = ["2", "3", "4", "5", "6"]
    vals = [28, 20, 48, 18, 40]
    pts = []
    for i, (m, val) in enumerate(zip(months, vals)):
        px = 382 + i * 54
        py = round(212 - (val / 55) * 96, 1)
        pts.append((px, py))
        diagram_slots.append(LineSlot(id=f"slot.diagram.vgrid_{i}", prompt="", x1=px, y1=106, x2=px, y2=212, stroke="#9ca3af", stroke_width=0.9))
        diagram_slots.append(TextSlot(id=f"slot.diagram.xlbl_{i}", prompt="", text=m, x=px, y=218, font_size=13, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center"))

    for i in range(len(pts) - 1):
        diagram_slots.append(LineSlot(id=f"slot.diagram.seg_{i}", prompt="", x1=pts[i][0], y1=pts[i][1], x2=pts[i + 1][0], y2=pts[i + 1][1], stroke="#ec4899", stroke_width=2))
    for i, (px, py) in enumerate(pts):
        diagram_slots.append(CircleSlot(id=f"slot.diagram.dot_{i}", prompt="", cx=px, cy=py, r=3, fill="#111827", stroke="#111827", stroke_width=1))

    g1_pre = TextSlot(id="slot.choice.g1_pre", prompt="", text="가로 (", x=240, y=268, font_size=21, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center")
    g1_0 = TextSlot(id="slot.choice.g1_option_0", prompt="", text="월", x=292, y=268, font_size=21, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center", interaction={"type": "choice", "role": "answer", "choice_index": 0, "value": "월", "group_id": "slot.choice.group_1", "include_in_submission": True})
    g1_c = TextSlot(id="slot.choice.g1_c", prompt="", text=",", x=316, y=268, font_size=21, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center")
    g1_1 = TextSlot(id="slot.choice.g1_option_1", prompt="", text="강수량", x=356, y=268, font_size=21, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center", interaction={"type": "choice", "role": "answer", "choice_index": 1, "value": "강수량", "group_id": "slot.choice.group_1", "include_in_submission": True})
    g2_pre = TextSlot(id="slot.choice.g2_pre", prompt="", text="), 세로 (", x=446, y=268, font_size=21, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center")
    g2_0 = TextSlot(id="slot.choice.g2_option_0", prompt="", text="월", x=512, y=268, font_size=21, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center", interaction={"type": "choice", "role": "answer", "choice_index": 0, "value": "월", "group_id": "slot.choice.group_2", "include_in_submission": True})
    g2_c = TextSlot(id="slot.choice.g2_c", prompt="", text=",", x=536, y=268, font_size=21, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center")
    g2_1 = TextSlot(id="slot.choice.g2_option_1", prompt="", text="강수량", x=576, y=268, font_size=21, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center", interaction={"type": "choice", "role": "answer", "choice_index": 1, "value": "강수량", "group_id": "slot.choice.group_2", "include_in_submission": True})
    g2_suf = TextSlot(id="slot.choice.g2_suf", prompt="", text=")", x=622, y=268, font_size=21, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center")

    choice_slots = (g1_pre, g1_0, g1_c, g1_1, g2_pre, g2_0, g2_c, g2_1, g2_suf)

    return ProblemTemplate(
        id=PROBLEM_ID,
        title=PROBLEM_TITLE,
        canvas=Canvas(
            width=886,
            height=320,
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
        {"ref": "horizontal_axis", "value": "월"},
        {"ref": "vertical_axis", "value": "강수량"},
    ],
    "target": {"ref": "slot.choice.g2_option_1", "label": "가로와 세로 축", "unit": ""},
    "method": "chart_axis_reading",
    "steps": [
        {
            "id": "read_axes",
            "expr": "가로: 월, 세로: 강수량",
            "explanation": "꺾은선그래프의 가로는 월, 세로는 강수량을 나타냅니다.",
            "value": ["월", "강수량"],
        },
    ],
    "answer": ANSWER,
}


if __name__ == "__main__":
    print(f"[{PROBLEM_TEMPLATE.id}] 템플릿 컴파일 성공!")
    print(f"- 제목: {PROBLEM_TEMPLATE.title}")
    print(f"- 캔버스: {PROBLEM_TEMPLATE.canvas.width} x {PROBLEM_TEMPLATE.canvas.height}")
    print(f"- 구역 수: {len(PROBLEM_TEMPLATE.regions)}")
