"""ModuMath Problem DSL: 꺾은선그래프에서 중간 시각의 값 예상하기 (S3_초등_4_007716)"""

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
PROBLEM_ID = "S3_초등_4_007716"
PROBLEM_TITLE = "오후 2시 30분의 교실 온도 예상하기"


# ==============================================================================
# 2. 정답 및 오답 진단 정의 (Answer & Diagnostic Key)
# ==============================================================================
ANSWER = {
    "value": "15 ℃",
    "answer_index": 1,
    "unit": "℃",
    "values": ["15 ℃"],
    "choices": [
        "14 ℃",
        "15 ℃",
        "16 ℃",
    ],
    "blanks": [],
    "answer_key": [
        {
            "slot_id": "slot.choice.option_1",
            "value": "15 ℃",
            "diagnostics": [
                {
                    "id": "diag.chose_3pm_value",
                    "condition": "answer_equals_14",
                    "concept": "꺾은선그래프의 중간값 예상",
                    "reason": "오후 3시의 온도(14 ℃)를 그대로 선택함",
                    "feedback": "오후 2시의 온도는 16 ℃, 오후 3시의 온도는 14 ℃이므로 오후 2시 30분의 온도는 두 값의 중간인 15 ℃입니다.",
                },
                {
                    "id": "diag.chose_2pm_value",
                    "condition": "answer_equals_16",
                    "concept": "꺾은선그래프의 중간값 예상",
                    "reason": "오후 2시의 온도(16 ℃)를 그대로 선택함",
                    "feedback": "오후 2시와 오후 3시 사이의 가운데 점의 값을 읽으면 15 ℃입니다.",
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
        "t_14": {"label": "오후 2시", "value": 16, "unit": "℃"},
        "t_15": {"label": "오후 3시", "value": 14, "unit": "℃"},
        "t_14_30": {"label": "오후 2시 30분", "value": 15, "unit": "℃"},
    },
    "relations": [
        {
            "type": "midpoint_interpolation",
            "expression": "(16 + 14) / 2 = 15",
            "target": "t_14_30",
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
        text="5. 교실의 온도를 조사하여 나타낸 꺾은선그래프입니다. 오후 2시 30분에는 교실의 온도가 몇 ℃였을까요?",
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
        TextSlot(id="slot.diagram.title", prompt="", text="교실의 온도", x=443, y=78, font_size=17, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center"),
        RectSlot(id="slot.diagram.frame", prompt="", x=243, y=102, width=400, height=130, fill="#ffffff", stroke="#6b7280", stroke_width=1.2),
        RectSlot(id="slot.diagram.ybox", prompt="", x=243, y=102, width=96, height=98, fill="#ffffff", stroke="#6b7280", stroke_width=1),
        RectSlot(id="slot.diagram.xbox", prompt="", x=339, y=200, width=304, height=32, fill="#ffffff", stroke="#6b7280", stroke_width=1),
        LineSlot(id="slot.diagram.diag", prompt="", x1=243, y1=232, x2=339, y2=200, stroke="#6b7280", stroke_width=1),
        TextSlot(id="slot.diagram.unit", prompt="", text="(℃)", x=268, y=108, font_size=13, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center"),
    ]

    for v in range(0, 16, 5):
        gy = round(200 - (v / 18) * 90, 1)
        diagram_slots.append(LineSlot(id=f"slot.diagram.grid_{v}", prompt="", x1=339, y1=gy, x2=643, y2=gy, stroke="#9ca3af", stroke_width=0.9))
        diagram_slots.append(TextSlot(id=f"slot.diagram.ylbl_{v}", prompt="", text=str(v), x=328, y=gy - 6, font_size=12, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="end"))

    times = ["11", "12", "1", "2", "3"]
    vals = [9, 11, 15, 16, 14]
    pts = []
    for i, (tm, val) in enumerate(zip(times, vals)):
        px = 382 + i * 54
        py = round(200 - (val / 18) * 90, 1)
        pts.append((px, py))
        diagram_slots.append(LineSlot(id=f"slot.diagram.vgrid_{i}", prompt="", x1=px, y1=102, x2=px, y2=200, stroke="#9ca3af", stroke_width=0.9))
        diagram_slots.append(TextSlot(id=f"slot.diagram.xlbl_{i}", prompt="", text=tm, x=px, y=206, font_size=13, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center"))

    for i in range(len(pts) - 1):
        diagram_slots.append(LineSlot(id=f"slot.diagram.seg_{i}", prompt="", x1=pts[i][0], y1=pts[i][1], x2=pts[i + 1][0], y2=pts[i + 1][1], stroke="#ec4899", stroke_width=2))
    for i, (px, py) in enumerate(pts):
        diagram_slots.append(CircleSlot(id=f"slot.diagram.dot_{i}", prompt="", cx=px, cy=py, r=3, fill="#111827", stroke="#111827", stroke_width=1))

    # 힌트 말풍선
    diagram_slots.extend([
        CircleSlot(id="slot.diagram.girl_head", prompt="", cx=200, cy=284, r=24, fill="#fde68a", stroke="#78350f", stroke_width=1.5),
        RectSlot(id="slot.diagram.bubble", prompt="", x=250, y=246, width=480, height=76, fill="#ffffff", stroke="#374151", stroke_width=1.4, rx=22, ry=22),
        TextBoxSlot(
            id="slot.diagram.bubble_txt",
            prompt="",
            text="오후 2시와 오후 3시의 온도의 값을 이은 선분의\n가운데에 점을 찍고 그 점의 값을 읽어서 예상해 봐.",
            x=264,
            y=254,
            width=452,
            height=60,
            font_size=17,
            font_family='"Noto Sans KR", sans-serif',
            fill="#111827",
            align="center",
            valign="middle",
            line_height=1.4,
        ),
    ])

    p_l = TextSlot(id="slot.choice.p_l", prompt="", text="(", x=546, y=336, font_size=22, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center")
    c0 = TextSlot(id="slot.choice.option_0", prompt="", text="14 ℃", x=596, y=336, font_size=20, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center", interaction={"type": "choice", "role": "answer", "choice_index": 0, "value": "14 ℃", "group_id": "slot.choice.group", "include_in_submission": True})
    cm0 = TextSlot(id="slot.choice.cm0", prompt="", text=",", x=636, y=336, font_size=20, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center")
    c1 = TextSlot(id="slot.choice.option_1", prompt="", text="15 ℃", x=676, y=336, font_size=20, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center", interaction={"type": "choice", "role": "answer", "choice_index": 1, "value": "15 ℃", "group_id": "slot.choice.group", "include_in_submission": True})
    cm1 = TextSlot(id="slot.choice.cm1", prompt="", text=",", x=716, y=336, font_size=20, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center")
    c2 = TextSlot(id="slot.choice.option_2", prompt="", text="16 ℃", x=756, y=336, font_size=20, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center", interaction={"type": "choice", "role": "answer", "choice_index": 2, "value": "16 ℃", "group_id": "slot.choice.group", "include_in_submission": True})
    p_r = TextSlot(id="slot.choice.p_r", prompt="", text=")", x=802, y=336, font_size=22, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center")

    choice_slots = (p_l, c0, cm0, c1, cm1, c2, p_r)

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
        {"ref": "t_14", "value": 16, "unit": "℃"},
        {"ref": "t_15", "value": 14, "unit": "℃"},
    ],
    "target": {"ref": "slot.choice.option_1", "label": "오후 2시 30분의 온도", "unit": "℃"},
    "method": "linear_midpoint_interpolation",
    "steps": [
        {
            "id": "interpolate_midpoint",
            "expr": "(16 + 14) / 2 = 15",
            "explanation": "오후 2시의 온도는 16 ℃, 오후 3시의 온도는 14 ℃이므로 중간인 15 ℃입니다.",
            "value": "15 ℃",
        },
    ],
    "answer": ANSWER,
}


if __name__ == "__main__":
    print(f"[{PROBLEM_TEMPLATE.id}] 템플릿 컴파일 성공!")
    print(f"- 제목: {PROBLEM_TEMPLATE.title}")
    print(f"- 캔버스: {PROBLEM_TEMPLATE.canvas.width} x {PROBLEM_TEMPLATE.canvas.height}")
    print(f"- 구역 수: {len(PROBLEM_TEMPLATE.regions)}")
