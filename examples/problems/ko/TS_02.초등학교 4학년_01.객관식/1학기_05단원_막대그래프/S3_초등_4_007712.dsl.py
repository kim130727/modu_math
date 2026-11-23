"""ModuMath Problem DSL: 막대그래프와 꺾은선그래프의 다른 점 (S3_초등_4_007712)"""

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
PROBLEM_ID = "S3_초등_4_007712"
PROBLEM_TITLE = "막대그래프와 꺾은선그래프의 다른 점 알기"


# ==============================================================================
# 2. 정답 및 오답 진단 정의 (Answer & Diagnostic Key)
# ==============================================================================
ANSWER = {
    "value": ["막대로", "선으로"],
    "unit": "",
    "values": ["막대로", "선으로"],
    "choices": [
        "막대로",
        "선으로",
    ],
    "blanks": [],
    "answer_key": [
        {
            "slot_id": "slot.choice.g1_option_0",
            "value": "막대로",
            "diagnostics": [
                {
                    "id": "diag.swapped_chart_representation",
                    "condition": "answer_equals_line_first",
                    "concept": "막대그래프와 꺾은선그래프의 차이",
                    "reason": "막대그래프와 꺾은선그래프의 표현 방식을 반대로 선택함",
                    "feedback": "막대그래프는 수량을 막대로 나타내고, 꺾은선그래프는 점들을 선으로 이어서 나타냅니다.",
                },
            ],
        },
        {
            "slot_id": "slot.choice.g2_option_1",
            "value": "선으로",
        },
    ],
}


# ==============================================================================
# 3. 시맨틱 모델 정의 (Semantic Model & Metadata)
# ==============================================================================
SEMANTIC = {
    "problem_id": PROBLEM_ID,
    "problem_type": "multiple_choice_chart_comparison",
    "metadata": {
        "school": "초등학교",
        "grade": 4,
        "semester": "1학기",
        "chapter": "05단원_막대그래프",
        "difficulty": "하",
    },
    "entities": {
        "bar_chart": {"label": "막대그래프", "representation": "막대로"},
        "line_chart": {"label": "꺾은선그래프", "representation": "선으로"},
    },
    "relations": [
        {
            "type": "chart_difference",
            "bar_chart": "막대로",
            "line_chart": "선으로",
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
        text="1. 염소의 무게를 매월 1일에 조사하여 나타낸 막대그래프와 꺾은선그래프입니다. 두 그래프의 다른 점을 알아보고 알맞은 말을 선택하세요.",
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
        TextSlot(id="slot.diagram.t_left", prompt="", text="염소의 무게", x=236, y=80, font_size=15, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center"),
        RectSlot(id="slot.diagram.bg_l", prompt="", x=96, y=102, width=280, height=130, fill="#ffffff", stroke="#6b7280", stroke_width=1),
        TextSlot(id="slot.diagram.t_right", prompt="", text="염소의 무게", x=650, y=80, font_size=15, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center"),
        RectSlot(id="slot.diagram.bg_r", prompt="", x=510, y=102, width=280, height=130, fill="#ffffff", stroke="#6b7280", stroke_width=1),
    ]

    months = ["8", "9", "10", "11"]
    vals = [8, 10, 14, 20]
    for i, (m, val) in enumerate(zip(months, vals)):
        bx = 136 + i * 56
        bh = round((val / 20) * 90, 1)
        diagram_slots.append(RectSlot(id=f"slot.diagram.l_bar_{i}", prompt="", x=bx - 10, y=round(206 - bh, 1), width=20, height=bh, fill="#fed7aa", stroke="#f97316", stroke_width=1.2))
        diagram_slots.append(TextSlot(id=f"slot.diagram.l_m_{i}", prompt="", text=m, x=bx, y=212, font_size=12, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center"))

    pts = []
    for i, (m, val) in enumerate(zip(months, vals)):
        px = 550 + i * 56
        py = round(206 - (val / 20) * 90, 1)
        pts.append((px, py))
        diagram_slots.append(TextSlot(id=f"slot.diagram.r_m_{i}", prompt="", text=m, x=px, y=212, font_size=12, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center"))
    for i in range(len(pts) - 1):
        diagram_slots.append(LineSlot(id=f"slot.diagram.r_seg_{i}", prompt="", x1=pts[i][0], y1=pts[i][1], x2=pts[i + 1][0], y2=pts[i + 1][1], stroke="#ec4899", stroke_width=2))
    for i, (px, py) in enumerate(pts):
        diagram_slots.append(CircleSlot(id=f"slot.diagram.r_dot_{i}", prompt="", cx=px, cy=py, r=3, fill="#111827", stroke="#111827", stroke_width=1))

    # 왼쪽 말풍선 (남학생)
    diagram_slots.extend([
        RectSlot(id="slot.diagram.b1", prompt="", x=86, y=252, width=250, height=94, fill="#ffffff", stroke="#374151", stroke_width=1.4, rx=22, ry=22),
        TextSlot(id="slot.diagram.b1_t1", prompt="", text="막대그래프는", x=211, y=266, font_size=17, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center"),
        TextSlot(id="slot.diagram.b1_t3", prompt="", text="나타냈어.", x=211, y=318, font_size=17, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center"),
        CircleSlot(id="slot.diagram.boy_head", prompt="", cx=378, cy=298, r=24, fill="#fde68a", stroke="#78350f", stroke_width=1.5),
    ])

    # 오른쪽 말풍선 (여학생)
    diagram_slots.extend([
        CircleSlot(id="slot.diagram.girl_head", prompt="", cx=508, cy=298, r=24, fill="#fde68a", stroke="#78350f", stroke_width=1.5),
        RectSlot(id="slot.diagram.b2", prompt="", x=550, y=252, width=260, height=94, fill="#ffffff", stroke="#374151", stroke_width=1.4, rx=22, ry=22),
        TextSlot(id="slot.diagram.b2_t1", prompt="", text="꺾은선그래프는 점들을", x=680, y=266, font_size=17, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center"),
        TextSlot(id="slot.diagram.b2_t3", prompt="", text="이어서 나타냈어.", x=680, y=318, font_size=17, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center"),
    ])

    g1_l = TextSlot(id="slot.choice.g1_l", prompt="", text="(", x=136, y=292, font_size=18, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center")
    g1_0 = TextSlot(id="slot.choice.g1_option_0", prompt="", text="막대로", x=174, y=292, font_size=17, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center", interaction={"type": "choice", "role": "answer", "choice_index": 0, "value": "막대로", "group_id": "slot.choice.group_1", "include_in_submission": True})
    g1_c = TextSlot(id="slot.choice.g1_c", prompt="", text=",", x=210, y=292, font_size=17, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center")
    g1_1 = TextSlot(id="slot.choice.g1_option_1", prompt="", text="선으로", x=246, y=292, font_size=17, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center", interaction={"type": "choice", "role": "answer", "choice_index": 1, "value": "선으로", "group_id": "slot.choice.group_1", "include_in_submission": True})
    g1_r = TextSlot(id="slot.choice.g1_r", prompt="", text=")", x=284, y=292, font_size=18, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center")

    g2_l = TextSlot(id="slot.choice.g2_l", prompt="", text="(", x=604, y=292, font_size=18, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center")
    g2_0 = TextSlot(id="slot.choice.g2_option_0", prompt="", text="막대로", x=642, y=292, font_size=17, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center", interaction={"type": "choice", "role": "answer", "choice_index": 0, "value": "막대로", "group_id": "slot.choice.group_2", "include_in_submission": True})
    g2_c = TextSlot(id="slot.choice.g2_c", prompt="", text=",", x=678, y=292, font_size=17, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center")
    g2_1 = TextSlot(id="slot.choice.g2_option_1", prompt="", text="선으로", x=714, y=292, font_size=17, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center", interaction={"type": "choice", "role": "answer", "choice_index": 1, "value": "선으로", "group_id": "slot.choice.group_2", "include_in_submission": True})
    g2_r = TextSlot(id="slot.choice.g2_r", prompt="", text=")", x=752, y=292, font_size=18, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center")

    choice_slots = (g1_l, g1_0, g1_c, g1_1, g1_r, g2_l, g2_0, g2_c, g2_1, g2_r)

    return ProblemTemplate(
        id=PROBLEM_ID,
        title=PROBLEM_TITLE,
        canvas=Canvas(
            width=886,
            height=376,
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
        {"ref": "bar_chart", "value": "막대그래프"},
        {"ref": "line_chart", "value": "꺾은선그래프"},
    ],
    "target": {"ref": "slot.choice.g2_option_1", "label": "두 그래프의 표현 방식", "unit": ""},
    "method": "chart_representation_comparison",
    "steps": [
        {
            "id": "compare_representations",
            "expr": "막대로, 선으로",
            "explanation": "막대그래프는 막대로 나타내고, 꺾은선그래프는 점들을 선으로 이어서 나타냅니다.",
            "value": ["막대로", "선으로"],
        },
    ],
    "answer": ANSWER,
}


if __name__ == "__main__":
    print(f"[{PROBLEM_TEMPLATE.id}] 템플릿 컴파일 성공!")
    print(f"- 제목: {PROBLEM_TEMPLATE.title}")
    print(f"- 캔버스: {PROBLEM_TEMPLATE.canvas.width} x {PROBLEM_TEMPLATE.canvas.height}")
    print(f"- 구역 수: {len(PROBLEM_TEMPLATE.regions)}")
