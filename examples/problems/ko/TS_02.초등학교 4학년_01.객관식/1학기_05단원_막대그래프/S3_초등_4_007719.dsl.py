"""ModuMath Problem DSL: 물결선을 사용한 그래프의 눈금 크기 비교 (S3_초등_4_007719)"""

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
PROBLEM_ID = "S3_초등_4_007719"
PROBLEM_TITLE = "물결선 그래프에서 세로 눈금 한 칸의 값 비교하기"


# ==============================================================================
# 2. 정답 및 오답 진단 정의 (Answer & Diagnostic Key)
# ==============================================================================
ANSWER = {
    "value": "작아서",
    "answer_index": 1,
    "unit": "",
    "values": ["작아서"],
    "choices": [
        "커서",
        "작아서",
    ],
    "blanks": [],
    "answer_key": [
        {
            "slot_id": "slot.choice.option_1",
            "value": "작아서",
            "diagnostics": [
                {
                    "id": "diag.confused_unit_scale",
                    "condition": "answer_equals_larger",
                    "concept": "물결선과 눈금 한 칸의 값",
                    "reason": "세로 눈금 한 칸의 값이 클수록 변화가 잘 보인다고 오인함",
                    "feedback": "(가)의 눈금 한 칸은 2 ℃이고 (나)의 눈금 한 칸은 0.1 ℃입니다. (나)는 세로 눈금 한 칸이 나타내는 값이 작아서 변화하는 모습이 더 잘 나타납니다.",
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
    "problem_type": "multiple_choice_wavy_break_chart",
    "metadata": {
        "school": "초등학교",
        "grade": 4,
        "semester": "1학기",
        "chapter": "05단원_막대그래프",
        "difficulty": "중",
    },
    "entities": {
        "chart_ga": {"label": "(가) 민수의 체온", "unit_tick": 2.0, "unit": "℃"},
        "chart_na": {"label": "(나) 민수의 체온", "unit_tick": 0.1, "unit": "℃"},
    },
    "relations": [
        {
            "type": "smaller_tick_gives_clarity",
            "correct_reason": "작아서",
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
        text="9. 민수의 체온을 조사하여 두 꺾은선그래프로 나타냈습니다. 알맞은 말을 선택하세요.",
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
        TextSlot(id="slot.diagram.t_l", prompt="", text="(가) 민수의 체온", x=246, y=78, font_size=16, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center"),
        RectSlot(id="slot.diagram.bg_l", prompt="", x=96, y=102, width=300, height=130, fill="#ffffff", stroke="#6b7280", stroke_width=1),
        TextSlot(id="slot.diagram.u_l", prompt="", text="(℃)", x=122, y=110, font_size=13, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center"),
        TextSlot(id="slot.diagram.t_r", prompt="", text="(나) 민수의 체온", x=640, y=78, font_size=16, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center"),
        RectSlot(id="slot.diagram.bg_r", prompt="", x=490, y=102, width=300, height=130, fill="#ffffff", stroke="#6b7280", stroke_width=1),
        TextSlot(id="slot.diagram.u_r", prompt="", text="(℃)", x=516, y=110, font_size=13, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center"),
    ]

    for v in range(0, 41, 10):
        gy = round(204 - (v / 42) * 92, 1)
        diagram_slots.append(LineSlot(id=f"slot.diagram.lg_{v}", prompt="", x1=156, y1=gy, x2=396, y2=gy, stroke="#cbd5e1", stroke_width=0.9))
        diagram_slots.append(TextSlot(id=f"slot.diagram.lyl_{v}", prompt="", text=str(v), x=146, y=gy - 6, font_size=11, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="end"))

    times = ["11", "12", "1", "2"]
    vals = [37.1, 37.4, 38.0, 37.9]
    pts_l = []
    for i, (tm, val) in enumerate(zip(times, vals)):
        px = 196 + i * 54
        py = round(204 - (val / 42) * 92, 1)
        pts_l.append((px, py))
        diagram_slots.append(TextSlot(id=f"slot.diagram.lxl_{i}", prompt="", text=tm, x=px, y=210, font_size=12, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center"))
    for i in range(len(pts_l) - 1):
        diagram_slots.append(LineSlot(id=f"slot.diagram.ls_{i}", prompt="", x1=pts_l[i][0], y1=pts_l[i][1], x2=pts_l[i + 1][0], y2=pts_l[i + 1][1], stroke="#ec4899", stroke_width=1.8))
    for i, (px, py) in enumerate(pts_l):
        diagram_slots.append(CircleSlot(id=f"slot.diagram.ld_{i}", prompt="", cx=px, cy=py, r=2.5, fill="#111827", stroke="#111827", stroke_width=1))

    diagram_slots.append(PathSlot(id="slot.diagram.wavy", prompt="", d="M 490 190 Q 565 182, 640 190 T 790 190", fill="none", stroke="#6b7280", stroke_width=1.4))
    for lbl, gy in [("37", 178), ("37.5", 150), ("38", 124), ("38.5", 104)]:
        diagram_slots.append(LineSlot(id=f"slot.diagram.rg_{lbl}", prompt="", x1=550, y1=gy, x2=790, y2=gy, stroke="#cbd5e1", stroke_width=0.9))
        diagram_slots.append(TextSlot(id=f"slot.diagram.ryl_{lbl}", prompt="", text=lbl, x=542, y=gy - 6, font_size=10, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="end"))

    pts_r = []
    for i, (tm, val) in enumerate(zip(times, vals)):
        px = 590 + i * 54
        py = round(178 - (val - 37.0) * 52, 1)
        pts_r.append((px, py))
        diagram_slots.append(TextSlot(id=f"slot.diagram.rxl_{i}", prompt="", text=tm, x=px, y=210, font_size=12, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center"))
    for i in range(len(pts_r) - 1):
        diagram_slots.append(LineSlot(id=f"slot.diagram.rs_{i}", prompt="", x1=pts_r[i][0], y1=pts_r[i][1], x2=pts_r[i + 1][0], y2=pts_r[i + 1][1], stroke="#ec4899", stroke_width=1.8))
    for i, (px, py) in enumerate(pts_r):
        diagram_slots.append(CircleSlot(id=f"slot.diagram.rd_{i}", prompt="", cx=px, cy=py, r=2.5, fill="#111827", stroke="#111827", stroke_width=1))

    diagram_slots.extend([
        CircleSlot(id="slot.diagram.boy_head", prompt="", cx=220, cy=292, r=24, fill="#fde68a", stroke="#78350f", stroke_width=1.5),
        RectSlot(id="slot.diagram.bubble", prompt="", x=272, y=252, width=480, height=82, fill="#ffffff", stroke="#374151", stroke_width=1.4, rx=22, ry=22),
        TextSlot(id="slot.diagram.b_line1", prompt="", text="(나) 그래프는 (가) 그래프보다 세로 눈금 한 칸이 나타내는", x=512, y=268, font_size=17, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center"),
    ])

    c_pre = TextSlot(id="slot.choice.pre", prompt="", text="값이 (", x=316, y=300, font_size=17, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center")
    c0 = TextSlot(id="slot.choice.option_0", prompt="", text="커서", x=374, y=300, font_size=17, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center", interaction={"type": "choice", "role": "answer", "choice_index": 0, "value": "커서", "group_id": "slot.choice.group", "include_in_submission": True})
    cm = TextSlot(id="slot.choice.cm", prompt="", text=",", x=404, y=300, font_size=17, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center")
    c1 = TextSlot(id="slot.choice.option_1", prompt="", text="작아서", x=440, y=300, font_size=17, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center", interaction={"type": "choice", "role": "answer", "choice_index": 1, "value": "작아서", "group_id": "slot.choice.group", "include_in_submission": True})
    c_suf = TextSlot(id="slot.choice.suf", prompt="", text=") 변화하는 모습이 더 잘 나타나.", x=596, y=300, font_size=17, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center")

    choice_slots = (c_pre, c0, cm, c1, c_suf)

    return ProblemTemplate(
        id=PROBLEM_ID,
        title=PROBLEM_TITLE,
        canvas=Canvas(
            width=886,
            height=356,
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
        {"ref": "chart_ga", "value": 2.0, "unit": "℃"},
        {"ref": "chart_na", "value": 0.1, "unit": "℃"},
    ],
    "target": {"ref": "slot.choice.option_1", "label": "세로 눈금 한 칸의 크기 비교", "unit": ""},
    "method": "scale_comparison",
    "steps": [
        {
            "id": "compare_unit_ticks",
            "expr": "0.1 < 2",
            "explanation": "(나) 그래프는 세로 눈금 한 칸이 나타내는 값이 작아서 변화하는 모습이 더 잘 나타납니다.",
            "value": "작아서",
        },
    ],
    "answer": ANSWER,
}


if __name__ == "__main__":
    print(f"[{PROBLEM_TEMPLATE.id}] 템플릿 컴파일 성공!")
    print(f"- 제목: {PROBLEM_TEMPLATE.title}")
    print(f"- 캔버스: {PROBLEM_TEMPLATE.canvas.width} x {PROBLEM_TEMPLATE.canvas.height}")
    print(f"- 구역 수: {len(PROBLEM_TEMPLATE.regions)}")
