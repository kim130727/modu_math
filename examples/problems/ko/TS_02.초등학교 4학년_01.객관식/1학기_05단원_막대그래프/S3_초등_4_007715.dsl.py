"""ModuMath Problem DSL: 꺾은선그래프에서 최댓값 시각 찾기 (S3_초등_4_007715)"""

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
PROBLEM_ID = "S3_초등_4_007715"
PROBLEM_TITLE = "교실의 온도가 가장 높은 시각 찾기"


# ==============================================================================
# 2. 정답 및 오답 진단 정의 (Answer & Diagnostic Key)
# ==============================================================================
ANSWER = {
    "value": "오후 2시",
    "answer_index": 3,
    "unit": "",
    "values": ["오후 2시"],
    "choices": [
        "오전 11시",
        "낮 12시",
        "오후 1시",
        "오후 2시",
        "오후 3시",
    ],
    "blanks": [],
    "answer_key": [
        {
            "slot_id": "slot.choice.option_3",
            "value": "오후 2시",
            "diagnostics": [
                {
                    "id": "diag.chose_1pm",
                    "condition": "answer_equals_1pm",
                    "concept": "꺾은선그래프 읽기",
                    "reason": "15℃ 눈금선 위의 오후 1시를 최댓값으로 오인함",
                    "feedback": "그래프에서 점이 가장 높게 찍힌 시각을 찾으면 오후 2시(16℃)입니다.",
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
    "problem_type": "multiple_choice_line_chart_maximum",
    "metadata": {
        "school": "초등학교",
        "grade": 4,
        "semester": "1학기",
        "chapter": "05단원_막대그래프",
        "difficulty": "하",
    },
    "entities": {
        "t_11": {"label": "오전 11시", "value": 9, "unit": "℃"},
        "t_12": {"label": "낮 12시", "value": 11, "unit": "℃"},
        "t_13": {"label": "오후 1시", "value": 15, "unit": "℃"},
        "t_14": {"label": "오후 2시", "value": 16, "unit": "℃"},
        "t_15": {"label": "오후 3시", "value": 14, "unit": "℃"},
    },
    "relations": [
        {
            "type": "maximum",
            "target": "t_14",
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
        text="4. 교실의 온도를 조사하여 나타낸 꺾은선그래프입니다. 교실의 온도가 가장 높은 때는 몇 시인가요?",
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
        TextSlot(id="slot.diagram.title", prompt="", text="교실의 온도", x=443, y=82, font_size=18, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center"),
        RectSlot(id="slot.diagram.frame", prompt="", x=243, y=108, width=400, height=136, fill="#ffffff", stroke="#6b7280", stroke_width=1.2),
        RectSlot(id="slot.diagram.ybox", prompt="", x=243, y=108, width=96, height=104, fill="#ffffff", stroke="#6b7280", stroke_width=1),
        RectSlot(id="slot.diagram.xbox", prompt="", x=339, y=212, width=304, height=32, fill="#ffffff", stroke="#6b7280", stroke_width=1),
        LineSlot(id="slot.diagram.diag", prompt="", x1=243, y1=244, x2=339, y2=212, stroke="#6b7280", stroke_width=1),
        TextSlot(id="slot.diagram.unit", prompt="", text="(℃)", x=268, y=114, font_size=14, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center"),
    ]

    for v in range(0, 16, 5):
        gy = round(212 - (v / 18) * 96, 1)
        diagram_slots.append(LineSlot(id=f"slot.diagram.grid_{v}", prompt="", x1=339, y1=gy, x2=643, y2=gy, stroke="#9ca3af", stroke_width=0.9))
        diagram_slots.append(TextSlot(id=f"slot.diagram.ylbl_{v}", prompt="", text=str(v), x=328, y=gy - 6, font_size=12, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="end"))

    times = ["11", "12", "1", "2", "3"]
    vals = [9, 11, 15, 16, 14]
    pts = []
    for i, (tm, val) in enumerate(zip(times, vals)):
        px = 382 + i * 54
        py = round(212 - (val / 18) * 96, 1)
        pts.append((px, py))
        diagram_slots.append(LineSlot(id=f"slot.diagram.vgrid_{i}", prompt="", x1=px, y1=108, x2=px, y2=212, stroke="#9ca3af", stroke_width=0.9))
        diagram_slots.append(TextSlot(id=f"slot.diagram.xlbl_{i}", prompt="", text=tm, x=px, y=216, font_size=13, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center"))

    for i in range(len(pts) - 1):
        diagram_slots.append(LineSlot(id=f"slot.diagram.seg_{i}", prompt="", x1=pts[i][0], y1=pts[i][1], x2=pts[i + 1][0], y2=pts[i + 1][1], stroke="#ec4899", stroke_width=2))
    for i, (px, py) in enumerate(pts):
        diagram_slots.append(CircleSlot(id=f"slot.diagram.dot_{i}", prompt="", cx=px, cy=py, r=3, fill="#111827", stroke="#111827", stroke_width=1))

    labels = ["오전 11시", "낮 12시", "오후 1시", "오후 2시", "오후 3시"]
    p_l = TextSlot(id="slot.choice.p_l", prompt="", text="(", x=196, y=268, font_size=22, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center")
    choice_slots = [p_l]
    for i, lbl in enumerate(labels):
        cx = 256 + i * 104
        choice_slots.append(
            TextSlot(
                id=f"slot.choice.option_{i}",
                prompt="",
                text=lbl,
                x=cx,
                y=268,
                font_size=19,
                font_family='"Noto Sans KR", sans-serif',
                fill="#111827",
                align="center",
                interaction={"type": "choice", "role": "answer", "choice_index": i, "value": lbl, "group_id": "slot.choice.group", "include_in_submission": True},
            )
        )
        if i < 4:
            choice_slots.append(TextSlot(id=f"slot.choice.c_{i}", prompt="", text=",", x=cx + 52, y=268, font_size=19, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center"))
    choice_slots.append(TextSlot(id="slot.choice.p_r", prompt="", text=")", x=734, y=268, font_size=22, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center"))

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
        {"ref": "t_14", "value": 16, "unit": "℃"},
    ],
    "target": {"ref": "slot.choice.option_3", "label": "온도가 가장 높은 시각", "unit": ""},
    "method": "maximum_point_reading",
    "steps": [
        {
            "id": "find_peak",
            "expr": "오후 2시 (16℃)",
            "explanation": "그래프에서 점이 가장 높게 찍힌 때는 오후 2시입니다.",
            "value": "오후 2시",
        },
    ],
    "answer": ANSWER,
}


if __name__ == "__main__":
    print(f"[{PROBLEM_TEMPLATE.id}] 템플릿 컴파일 성공!")
    print(f"- 제목: {PROBLEM_TEMPLATE.title}")
    print(f"- 캔버스: {PROBLEM_TEMPLATE.canvas.width} x {PROBLEM_TEMPLATE.canvas.height}")
    print(f"- 구역 수: {len(PROBLEM_TEMPLATE.regions)}")
