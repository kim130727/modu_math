"""ModuMath Problem DSL: 꺾은선그래프에서 온도 변화 추이 읽기 (S3_초등_4_007714)"""

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
PROBLEM_ID = "S3_초등_4_007714"
PROBLEM_TITLE = "교실 온도 꺾은선그래프의 변화 추이 선택하기"


# ==============================================================================
# 2. 정답 및 오답 진단 정의 (Answer & Diagnostic Key)
# ==============================================================================
ANSWER = {
    "value": "높아지다가 낮아지고",
    "answer_index": 0,
    "unit": "",
    "values": ["높아지다가 낮아지고"],
    "choices": [
        "높아지다가 낮아지고",
        "낮아지다가 높아지고",
    ],
    "blanks": [],
    "answer_key": [
        {
            "slot_id": "slot.choice.option_0",
            "value": "높아지다가 낮아지고",
            "diagnostics": [
                {
                    "id": "diag.reversed_trend",
                    "condition": "answer_equals_down_then_up",
                    "concept": "꺾은선그래프의 변화 추이",
                    "reason": "오른쪽 위로 올라가는 선과 아래로 내려가는 선의 방향을 반대로 해석함",
                    "feedback": "오전 11시부터 오후 2시까지는 선이 오른쪽 위로 올라가고, 오후 2시부터 3시까지는 내려오므로 높아지다가 낮아지고 있습니다.",
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
    "problem_type": "multiple_choice_line_chart_trend",
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
            "type": "trend",
            "pattern": "높아지다가 낮아지고",
        }
    ],
}


# ==============================================================================
# 4. 문제 템플릿 빌더 (ProblemTemplate Builder)
# ==============================================================================
def _build_temp_chart() -> list:
    slots = [
        TextSlot(id="slot.diagram.title", prompt="", text="교실의 온도", x=443, y=82, font_size=18, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center"),
        RectSlot(id="slot.diagram.frame", prompt="", x=243, y=108, width=400, height=136, fill="#ffffff", stroke="#6b7280", stroke_width=1.2),
        RectSlot(id="slot.diagram.ybox", prompt="", x=243, y=108, width=96, height=104, fill="#ffffff", stroke="#6b7280", stroke_width=1),
        RectSlot(id="slot.diagram.xbox", prompt="", x=339, y=212, width=304, height=32, fill="#ffffff", stroke="#6b7280", stroke_width=1),
        LineSlot(id="slot.diagram.diag", prompt="", x1=243, y1=244, x2=339, y2=212, stroke="#6b7280", stroke_width=1),
        TextSlot(id="slot.diagram.unit", prompt="", text="(℃)", x=268, y=114, font_size=14, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center"),
        TextSlot(id="slot.diagram.wy", prompt="", text="온도", x=264, y=218, font_size=12, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center"),
        TextSlot(id="slot.diagram.wx", prompt="", text="시각", x=318, y=224, font_size=12, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center"),
    ]

    for v in range(0, 16, 5):
        gy = round(212 - (v / 18) * 96, 1)
        slots.append(LineSlot(id=f"slot.diagram.grid_{v}", prompt="", x1=339, y1=gy, x2=643, y2=gy, stroke="#9ca3af", stroke_width=0.9))
        slots.append(TextSlot(id=f"slot.diagram.ylbl_{v}", prompt="", text=str(v), x=328, y=gy - 6, font_size=12, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="end"))

    times = ["11", "12", "1", "2", "3"]
    vals = [9, 11, 15, 16, 14]
    pts = []
    for i, (tm, val) in enumerate(zip(times, vals)):
        px = 382 + i * 54
        py = round(212 - (val / 18) * 96, 1)
        pts.append((px, py))
        slots.append(LineSlot(id=f"slot.diagram.vgrid_{i}", prompt="", x1=px, y1=108, x2=px, y2=212, stroke="#9ca3af", stroke_width=0.9))
        slots.append(TextSlot(id=f"slot.diagram.xlbl_{i}", prompt="", text=tm, x=px, y=216, font_size=13, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center"))

    for i in range(len(pts) - 1):
        slots.append(LineSlot(id=f"slot.diagram.seg_{i}", prompt="", x1=pts[i][0], y1=pts[i][1], x2=pts[i + 1][0], y2=pts[i + 1][1], stroke="#ec4899", stroke_width=2))
    for i, (px, py) in enumerate(pts):
        slots.append(CircleSlot(id=f"slot.diagram.dot_{i}", prompt="", cx=px, cy=py, r=3, fill="#111827", stroke="#111827", stroke_width=1))

    return slots


def build_problem_template() -> ProblemTemplate:
    """문제의 캔버스 크기, 슬롯(텍스트/도형/선택지), 리전(구역)을 정의합니다."""

    stem_text_slot = TextBoxSlot(
        id="slot.stem.question",
        prompt="",
        text="3. 교실의 온도를 조사하여 나타낸 꺾은선그래프입니다. 교실의 온도가 어떻게 변하는지 알맞은 말을 선택하세요.",
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

    diagram_slots = _build_temp_chart()

    c_pre = TextSlot(id="slot.choice.pre", prompt="", text="교실의 온도가 (", x=156, y=268, font_size=21, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center")
    c0 = TextSlot(id="slot.choice.option_0", prompt="", text="높아지다가 낮아지고", x=338, y=268, font_size=21, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center", interaction={"type": "choice", "role": "answer", "choice_index": 0, "value": "높아지다가 낮아지고", "group_id": "slot.choice.group", "include_in_submission": True})
    cm = TextSlot(id="slot.choice.cm", prompt="", text=",", x=448, y=268, font_size=21, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center")
    c1 = TextSlot(id="slot.choice.option_1", prompt="", text="낮아지다가 높아지고", x=558, y=268, font_size=21, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center", interaction={"type": "choice", "role": "answer", "choice_index": 1, "value": "낮아지다가 높아지고", "group_id": "slot.choice.group", "include_in_submission": True})
    c_suf = TextSlot(id="slot.choice.suf", prompt="", text=") 있습니다.", x=720, y=268, font_size=21, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center")

    choice_slots = (c_pre, c0, cm, c1, c_suf)

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
        {"ref": "t_11", "value": 9, "unit": "℃"},
        {"ref": "t_14", "value": 16, "unit": "℃"},
        {"ref": "t_15", "value": 14, "unit": "℃"},
    ],
    "target": {"ref": "slot.choice.option_0", "label": "온도 변화 추이", "unit": ""},
    "method": "line_slope_interpretation",
    "steps": [
        {
            "id": "read_trend",
            "expr": "9 -> 16 -> 14",
            "explanation": "선이 올라가다가 내려오므로 교실의 온도가 높아지다가 낮아지고 있습니다.",
            "value": "높아지다가 낮아지고",
        },
    ],
    "answer": ANSWER,
}


if __name__ == "__main__":
    print(f"[{PROBLEM_TEMPLATE.id}] 템플릿 컴파일 성공!")
    print(f"- 제목: {PROBLEM_TEMPLATE.title}")
    print(f"- 캔버스: {PROBLEM_TEMPLATE.canvas.width} x {PROBLEM_TEMPLATE.canvas.height}")
    print(f"- 구역 수: {len(PROBLEM_TEMPLATE.regions)}")
