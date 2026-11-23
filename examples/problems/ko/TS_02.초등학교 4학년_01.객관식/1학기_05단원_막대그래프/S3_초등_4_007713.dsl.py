"""ModuMath Problem DSL: 변화 알아보기 쉬운 그래프 선택하기 (S3_초등_4_007713)"""

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
PROBLEM_ID = "S3_초등_4_007713"
PROBLEM_TITLE = "변화를 한눈에 알아보기 쉬운 그래프 선택하기"


# ==============================================================================
# 2. 정답 및 오답 진단 정의 (Answer & Diagnostic Key)
# ==============================================================================
ANSWER = {
    "value": "꺾은선그래프",
    "answer_index": 1,
    "unit": "",
    "values": ["꺾은선그래프"],
    "choices": [
        "막대그래프",
        "꺾은선그래프",
    ],
    "blanks": [],
    "answer_key": [
        {
            "slot_id": "slot.choice.option_1",
            "value": "꺾은선그래프",
            "diagnostics": [
                {
                    "id": "diag.chose_bar_chart",
                    "condition": "answer_equals_bar_chart",
                    "concept": "꺾은선그래프의 특징",
                    "reason": "변화를 알아보기 쉬운 그래프로 막대그래프를 선택함",
                    "feedback": "막대그래프는 수량의 크기를 비교하기 쉽고, 꺾은선그래프는 선의 기울어진 정도를 통해 시간에 따른 변화 모습을 한눈에 알아보기 쉽습니다.",
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
    "problem_type": "multiple_choice_chart_purpose",
    "metadata": {
        "school": "초등학교",
        "grade": 4,
        "semester": "1학기",
        "chapter": "05단원_막대그래프",
        "difficulty": "하",
    },
    "entities": {
        "bar_chart": {"label": "막대그래프", "purpose": "수량 비교"},
        "line_chart": {"label": "꺾은선그래프", "purpose": "변화 추이"},
    },
    "relations": [
        {
            "type": "best_for_change_over_time",
            "correct_entity": "line_chart",
            "distractor": "bar_chart",
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
        text="2. 염소의 무게를 매월 1일에 조사하여 나타낸 막대그래프와 꺾은선그래프입니다. 알맞은 그래프를 선택하세요.",
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

    desc = TextBoxSlot(
        id="slot.diagram.desc",
        prompt="",
        text="염소의 무게의 변화를 한눈에 알아보기 쉬운 그래프는",
        x=120,
        y=252,
        width=646,
        height=32,
        font_size=21,
        font_family='"Noto Sans KR", sans-serif',
        fill="#111827",
        align="center",
        valign="middle",
    )
    diagram_slots.append(desc)

    p_l = TextSlot(id="slot.choice.p_l", prompt="", text="(", x=246, y=296, font_size=22, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center")
    c0 = TextSlot(id="slot.choice.option_0", prompt="", text="막대그래프", x=316, y=296, font_size=21, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center", interaction={"type": "choice", "role": "answer", "choice_index": 0, "value": "막대그래프", "group_id": "slot.choice.group", "include_in_submission": True})
    cm = TextSlot(id="slot.choice.cm", prompt="", text=",", x=382, y=296, font_size=21, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center")
    c1 = TextSlot(id="slot.choice.option_1", prompt="", text="꺾은선그래프", x=456, y=296, font_size=21, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center", interaction={"type": "choice", "role": "answer", "choice_index": 1, "value": "꺾은선그래프", "group_id": "slot.choice.group", "include_in_submission": True})
    p_r = TextSlot(id="slot.choice.p_r", prompt="", text=")입니다.", x=562, y=296, font_size=21, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center")

    choice_slots = (p_l, c0, cm, c1, p_r)

    return ProblemTemplate(
        id=PROBLEM_ID,
        title=PROBLEM_TITLE,
        canvas=Canvas(
            width=886,
            height=350,
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
    "target": {"ref": "slot.choice.option_1", "label": "변화를 알아보기 쉬운 그래프", "unit": ""},
    "method": "chart_purpose_selection",
    "steps": [
        {
            "id": "select_line_chart",
            "expr": "꺾은선그래프",
            "explanation": "꺾은선그래프는 선의 기울어진 정도를 보고 무게의 변화를 한눈에 알아보기 쉽습니다.",
            "value": "꺾은선그래프",
        },
    ],
    "answer": ANSWER,
}


if __name__ == "__main__":
    print(f"[{PROBLEM_TEMPLATE.id}] 템플릿 컴파일 성공!")
    print(f"- 제목: {PROBLEM_TEMPLATE.title}")
    print(f"- 캔버스: {PROBLEM_TEMPLATE.canvas.width} x {PROBLEM_TEMPLATE.canvas.height}")
    print(f"- 구역 수: {len(PROBLEM_TEMPLATE.regions)}")
