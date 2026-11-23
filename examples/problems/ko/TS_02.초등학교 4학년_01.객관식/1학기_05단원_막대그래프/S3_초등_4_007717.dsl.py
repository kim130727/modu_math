"""ModuMath Problem DSL: 물결선을 사용한 꺾은선그래프의 특징 (S3_초등_4_007717)"""

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
PROBLEM_ID = "S3_초등_4_007717"
PROBLEM_TITLE = "물결선을 사용한 꺾은선그래프의 장점 알기"


# ==============================================================================
# 2. 정답 및 오답 진단 정의 (Answer & Diagnostic Key)
# ==============================================================================
ANSWER = {
    "value": "나타납니다",
    "answer_index": 0,
    "unit": "",
    "values": ["나타납니다"],
    "choices": [
        "나타납니다",
        "나타나지 않습니다",
    ],
    "blanks": [],
    "answer_key": [
        {
            "slot_id": "slot.choice.option_0",
            "value": "나타납니다",
            "diagnostics": [
                {
                    "id": "diag.misunderstood_wavy_break",
                    "condition": "answer_equals_not_clear",
                    "concept": "물결선의 쓰임",
                    "reason": "물결선으로 줄여 그리면 변화가 더 잘 보인다는 점을 반대로 이해함",
                    "feedback": "물결선을 사용한 꺾은선그래프는 세로 눈금 한 칸의 크기를 작게 하여 자료의 변화하는 모습을 더 뚜렷하게 볼 수 있습니다.",
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
        "difficulty": "하",
    },
    "entities": {
        "chart_ga": {"label": "(가) 강의 수온", "has_wavy_break": False},
        "chart_na": {"label": "(나) 강의 수온", "has_wavy_break": True},
    },
    "relations": [
        {
            "type": "wavy_break_clarity",
            "clearer_chart": "chart_na",
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
        text="6. 어느 강의 수온을 매월 1일에 조사하여 두 꺾은선그래프로 나타냈습니다. 알맞은 말을 선택하세요.",
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
        TextSlot(id="slot.diagram.t_l", prompt="", text="(가) 강의 수온", x=246, y=78, font_size=16, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center"),
        RectSlot(id="slot.diagram.bg_l", prompt="", x=96, y=102, width=300, height=130, fill="#ffffff", stroke="#6b7280", stroke_width=1),
        TextSlot(id="slot.diagram.u_l", prompt="", text="(℃)", x=122, y=110, font_size=13, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center"),
        TextSlot(id="slot.diagram.t_r", prompt="", text="(나) 강의 수온", x=640, y=78, font_size=16, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center"),
        RectSlot(id="slot.diagram.bg_r", prompt="", x=490, y=102, width=300, height=130, fill="#ffffff", stroke="#6b7280", stroke_width=1),
        TextSlot(id="slot.diagram.u_r", prompt="", text="(℃)", x=516, y=110, font_size=13, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center"),
    ]

    # (가) 0~18℃
    for v in range(0, 16, 5):
        gy = round(204 - (v / 18) * 92, 1)
        diagram_slots.append(LineSlot(id=f"slot.diagram.lg_{v}", prompt="", x1=156, y1=gy, x2=396, y2=gy, stroke="#cbd5e1", stroke_width=0.9))
        diagram_slots.append(TextSlot(id=f"slot.diagram.lyl_{v}", prompt="", text=str(v), x=146, y=gy - 6, font_size=11, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="end"))

    months = ["3", "4", "5", "6"]
    vals = [14.4, 14.8, 15.2, 16.4]
    pts_l = []
    for i, (m, val) in enumerate(zip(months, vals)):
        px = 196 + i * 54
        py = round(204 - (val / 18) * 92, 1)
        pts_l.append((px, py))
        diagram_slots.append(TextSlot(id=f"slot.diagram.lxl_{i}", prompt="", text=m, x=px, y=210, font_size=12, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center"))
    for i in range(len(pts_l) - 1):
        diagram_slots.append(LineSlot(id=f"slot.diagram.ls_{i}", prompt="", x1=pts_l[i][0], y1=pts_l[i][1], x2=pts_l[i + 1][0], y2=pts_l[i + 1][1], stroke="#ec4899", stroke_width=1.8))
    for i, (px, py) in enumerate(pts_l):
        diagram_slots.append(CircleSlot(id=f"slot.diagram.ld_{i}", prompt="", cx=px, cy=py, r=2.5, fill="#111827", stroke="#111827", stroke_width=1))

    # (나) 물결선 + 14~16℃
    diagram_slots.append(PathSlot(id="slot.diagram.wavy", prompt="", d="M 490 190 Q 565 182, 640 190 T 790 190", fill="none", stroke="#6b7280", stroke_width=1.4))
    for v, gy in [(14, 178), (15, 148), (16, 118)]:
        diagram_slots.append(LineSlot(id=f"slot.diagram.rg_{v}", prompt="", x1=550, y1=gy, x2=790, y2=gy, stroke="#cbd5e1", stroke_width=0.9))
        diagram_slots.append(TextSlot(id=f"slot.diagram.ryl_{v}", prompt="", text=str(v), x=540, y=gy - 6, font_size=11, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="end"))

    pts_r = []
    for i, (m, val) in enumerate(zip(months, vals)):
        px = 590 + i * 54
        py = round(178 - (val - 14) * 30, 1)
        pts_r.append((px, py))
        diagram_slots.append(TextSlot(id=f"slot.diagram.rxl_{i}", prompt="", text=m, x=px, y=210, font_size=12, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center"))
    for i in range(len(pts_r) - 1):
        diagram_slots.append(LineSlot(id=f"slot.diagram.rs_{i}", prompt="", x1=pts_r[i][0], y1=pts_r[i][1], x2=pts_r[i + 1][0], y2=pts_r[i + 1][1], stroke="#ec4899", stroke_width=1.8))
    for i, (px, py) in enumerate(pts_r):
        diagram_slots.append(CircleSlot(id=f"slot.diagram.rd_{i}", prompt="", cx=px, cy=py, r=2.5, fill="#111827", stroke="#111827", stroke_width=1))

    # 요약 박스 및 선택지
    diagram_slots.extend([
        RectSlot(id="slot.diagram.summary_box", prompt="", x=76, y=246, width=734, height=82, fill="#ffffff", stroke="#84cc16", stroke_width=1.6),
        TextSlot(id="slot.diagram.sum_1", prompt="", text="(나) 그래프와 같이 필요 없는 부분을 물결선으로 줄여서 나타내면", x=443, y=260, font_size=18, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center"),
    ])

    c_pre = TextSlot(id="slot.choice.pre", prompt="", text="변화하는 모습이 (가) 그래프보다 잘 (", x=250, y=296, font_size=18, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center")
    c0 = TextSlot(id="slot.choice.option_0", prompt="", text="나타납니다", x=456, y=296, font_size=18, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center", interaction={"type": "choice", "role": "answer", "choice_index": 0, "value": "나타납니다", "group_id": "slot.choice.group", "include_in_submission": True})
    cm = TextSlot(id="slot.choice.cm", prompt="", text=",", x=514, y=296, font_size=18, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center")
    c1 = TextSlot(id="slot.choice.option_1", prompt="", text="나타나지 않습니다", x=604, y=296, font_size=18, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center", interaction={"type": "choice", "role": "answer", "choice_index": 1, "value": "나타나지 않습니다", "group_id": "slot.choice.group", "include_in_submission": True})
    c_suf = TextSlot(id="slot.choice.suf", prompt="", text=").", x=692, y=296, font_size=18, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center")

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
        {"ref": "chart_ga", "value": "물결선 없음"},
        {"ref": "chart_na", "value": "물결선 사용"},
    ],
    "target": {"ref": "slot.choice.option_0", "label": "변화하는 모습의 가독성", "unit": ""},
    "method": "wavy_break_interpretation",
    "steps": [
        {
            "id": "compare_clarity",
            "expr": "나타납니다",
            "explanation": "물결선을 사용하면 세로 눈금 한 칸의 크기를 작게 하여 변화하는 모습을 뚜렷하게 볼 수 있습니다.",
            "value": "나타납니다",
        },
    ],
    "answer": ANSWER,
}


if __name__ == "__main__":
    print(f"[{PROBLEM_TEMPLATE.id}] 템플릿 컴파일 성공!")
    print(f"- 제목: {PROBLEM_TEMPLATE.title}")
    print(f"- 캔버스: {PROBLEM_TEMPLATE.canvas.width} x {PROBLEM_TEMPLATE.canvas.height}")
    print(f"- 구역 수: {len(PROBLEM_TEMPLATE.regions)}")
