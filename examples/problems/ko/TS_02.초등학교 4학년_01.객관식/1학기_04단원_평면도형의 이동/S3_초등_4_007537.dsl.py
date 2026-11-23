"""ModuMath Problem DSL: 점 ㄱ을 지나고 주어진 직선과 평행한 직선 긋기 원리 (S3_초등_4_007537)"""

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
PROBLEM_ID = "S3_초등_4_007537"
PROBLEM_TITLE = "점 ㄱ을 지나고 평행한 직선을 긋는 이유 알기"


# ==============================================================================
# 2. 정답 및 오답 진단 정의 (Answer & Diagnostic Key)
# ==============================================================================
ANSWER = {
    "value": "수직",
    "answer_index": 0,
    "unit": "",
    "values": ["수직"],
    "choices": [
        "수직",
        "평행",
    ],
    "blanks": [],
    "answer_key": [
        {
            "slot_id": "slot.choice.option_0",
            "value": "수직",
            "diagnostics": [
                {
                    "id": "diag.confused_perpendicular_parallel",
                    "condition": "answer_equals_parallel",
                    "concept": "평행선 긋기",
                    "reason": "먼저 놓은 삼각자의 변에 대해 두 직선이 각각 수직이라는 점을 평행으로 혼동함",
                    "feedback": "먼저 놓은 삼각자의 한 변에 대해 주어진 직선과 그은 직선이 각각 서로 수직이므로 두 직선은 서로 평행합니다.",
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
    "problem_type": "multiple_choice_parallel_construction_reason",
    "metadata": {
        "school": "초등학교",
        "grade": 4,
        "semester": "1학기",
        "chapter": "04단원_평면도형의 이동",
        "difficulty": "중",
    },
    "entities": {
        "first_edge": {"label": "먼저 놓은 삼각자의 한 변"},
        "given_line": {"label": "주어진 직선"},
        "drawn_line": {"label": "그은 직선"},
    },
    "relations": [
        {
            "type": "perpendicular_implies_parallel",
            "reason": "수직",
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
        text="73. 삼각자를 사용하여 점 ㄱ을 지나고 주어진 직선과 평행한 직선을 긋는 방법입니다. 주어진 직선과 그은 직선이 서로 평행한 이유에 맞게 알맞은 말을 선택하세요.",
        x=32,
        y=24,
        width=820,
        height=56,
        font_size=22,
        font_family='"Noto Sans KR", sans-serif',
        fill="#202124",
        align="left",
        valign="top",
        line_height=1.5,
    )

    # 왼쪽 단계
    s1_base = LineSlot(id="slot.diagram.s1_base", prompt="", x1=156, y1=174, x2=386, y2=174, stroke="#111827", stroke_width=1.8)
    s1_t1 = PolygonSlot(id="slot.diagram.s1_t1", prompt="", points=[(196, 174), (254, 174), (254, 92)], fill="#e0f2fe", stroke="#0284c7", stroke_width=1.4)
    s1_pt = CircleSlot(id="slot.diagram.s1_pt", prompt="", cx=254, cy=118, r=3, fill="#111827", stroke="#111827", stroke_width=1)
    s1_pt_l = TextSlot(id="slot.diagram.s1_pt_l", prompt="", text="ㄱ", x=268, y=110, font_size=16, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center")
    s1_box = RectSlot(id="slot.diagram.s1_box", prompt="", x=144, y=194, width=250, height=78, fill="#fce7f3", stroke="#f9a8d4", stroke_width=1, rx=8, ry=8)
    s1_txt = TextBoxSlot(id="slot.diagram.s1_txt", prompt="", text="삼각자에서 직각을 낀 변 중\n한 변을 주어진 직선에 맞추고\n다른 한 변이 점 ㄱ을 지나도록\n놓습니다.", x=150, y=198, width=238, height=70, font_size=14, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center", valign="middle", line_height=1.25)

    arrow = TextSlot(id="slot.diagram.arrow", prompt="", text="➡", x=443, y=126, font_size=24, font_family='"Noto Sans KR", sans-serif', fill="#6b7280", align="center")

    # 오른쪽 단계
    s2_base = LineSlot(id="slot.diagram.s2_base", prompt="", x1=496, y1=174, x2=746, y2=174, stroke="#111827", stroke_width=1.8)
    s2_t1 = PolygonSlot(id="slot.diagram.s2_t1", prompt="", points=[(536, 174), (594, 174), (594, 92)], fill="#e0f2fe", stroke="#0284c7", stroke_width=1.4)
    s2_t2 = PolygonSlot(id="slot.diagram.s2_t2", prompt="", points=[(594, 118), (710, 118), (594, 174)], fill="#e0f2fe", stroke="#0284c7", stroke_width=1.4)
    s2_l2 = LineSlot(id="slot.diagram.s2_l2", prompt="", x1=594, y1=118, x2=736, y2=118, stroke="#111827", stroke_width=1.8)
    s2_pt = CircleSlot(id="slot.diagram.s2_pt", prompt="", cx=594, cy=118, r=3, fill="#111827", stroke="#111827", stroke_width=1)
    s2_box = RectSlot(id="slot.diagram.s2_box", prompt="", x=486, y=194, width=264, height=78, fill="#fce7f3", stroke="#f9a8d4", stroke_width=1, rx=8, ry=8)
    s2_txt = TextBoxSlot(id="slot.diagram.s2_txt", prompt="", text="다른 삼각자를 사용하여\n점 ㄱ을 지나고 주어진 직선과\n평행한 직선을 긋습니다.", x=496, y=200, width=244, height=66, font_size=15, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center", valign="middle", line_height=1.3)

    # 말풍선 및 선택지
    bubble = RectSlot(id="slot.diagram.bubble", prompt="", x=156, y=290, width=510, height=84, fill="#ffffff", stroke="#374151", stroke_width=1.4, rx=24, ry=24)
    b_line1 = TextSlot(id="slot.diagram.b_line1", prompt="", text="먼저 놓은 삼각자의 한 변에 대해 주어진 직선과", x=411, y=306, font_size=18, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center")
    girl_head = CircleSlot(id="slot.diagram.girl_head", prompt="", cx=726, cy=332, r=28, fill="#fde68a", stroke="#78350f", stroke_width=1.5)

    c_pre = TextSlot(id="slot.choice.prefix", prompt="", text="그은 직선이 각각 서로 (", x=292, y=338, font_size=18, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center")
    choice_0 = TextSlot(
        id="slot.choice.option_0",
        prompt="",
        text="수직",
        x=414,
        y=338,
        font_size=18,
        font_family='"Noto Sans KR", sans-serif',
        fill="#111827",
        align="center",
        interaction={"type": "choice", "role": "answer", "choice_index": 0, "value": "수직", "group_id": "slot.choice.group", "include_in_submission": True},
    )
    comma = TextSlot(id="slot.choice.comma", prompt="", text=",", x=444, y=338, font_size=18, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center")
    choice_1 = TextSlot(
        id="slot.choice.option_1",
        prompt="",
        text="평행",
        x=474,
        y=338,
        font_size=18,
        font_family='"Noto Sans KR", sans-serif',
        fill="#111827",
        align="center",
        interaction={"type": "choice", "role": "answer", "choice_index": 1, "value": "평행", "group_id": "slot.choice.group", "include_in_submission": True},
    )
    c_suf = TextSlot(id="slot.choice.suffix", prompt="", text=")이 되기 때문이야.", x=568, y=338, font_size=18, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center")

    return ProblemTemplate(
        id=PROBLEM_ID,
        title=PROBLEM_TITLE,
        canvas=Canvas(
            width=886,
            height=392,
            coordinate_mode="logical",
        ),
        regions=(
            Region(id="region.stem", role="stem", flow="absolute", slot_ids=("slot.stem.question",)),
            Region(
                id="region.diagram",
                role="diagram",
                flow="absolute",
                slot_ids=(
                    "slot.diagram.s1_base",
                    "slot.diagram.s1_t1",
                    "slot.diagram.s1_pt",
                    "slot.diagram.s1_pt_l",
                    "slot.diagram.s1_box",
                    "slot.diagram.s1_txt",
                    "slot.diagram.arrow",
                    "slot.diagram.s2_base",
                    "slot.diagram.s2_t1",
                    "slot.diagram.s2_t2",
                    "slot.diagram.s2_l2",
                    "slot.diagram.s2_pt",
                    "slot.diagram.s2_box",
                    "slot.diagram.s2_txt",
                    "slot.diagram.bubble",
                    "slot.diagram.b_line1",
                    "slot.diagram.girl_head",
                ),
            ),
            Region(
                id="region.choices",
                role="choices",
                flow="absolute",
                slot_ids=("slot.choice.prefix", "slot.choice.option_0", "slot.choice.comma", "slot.choice.option_1", "slot.choice.suffix"),
            ),
        ),
        slots=(
            stem_text_slot,
            s1_base,
            s1_t1,
            s1_pt,
            s1_pt_l,
            s1_box,
            s1_txt,
            arrow,
            s2_base,
            s2_t1,
            s2_t2,
            s2_l2,
            s2_pt,
            s2_box,
            s2_txt,
            bubble,
            b_line1,
            girl_head,
            c_pre,
            choice_0,
            comma,
            choice_1,
            c_suf,
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
        {"ref": "first_edge", "value": "먼저 놓은 삼각자의 한 변"},
    ],
    "target": {"ref": "slot.choice.option_0", "label": "두 직선과 기준 변의 관계", "unit": ""},
    "method": "parallel_lines_theorem",
    "steps": [
        {
            "id": "explain_parallel",
            "expr": "수직",
            "explanation": "먼저 놓은 삼각자의 한 변에 대해 주어진 직선과 그은 직선이 각각 서로 수직이므로 두 직선은 서로 평행합니다.",
            "value": "수직",
        },
    ],
    "answer": ANSWER,
}


if __name__ == "__main__":
    print(f"[{PROBLEM_TEMPLATE.id}] 템플릿 컴파일 성공!")
    print(f"- 제목: {PROBLEM_TEMPLATE.title}")
    print(f"- 캔버스: {PROBLEM_TEMPLATE.canvas.width} x {PROBLEM_TEMPLATE.canvas.height}")
    print(f"- 구역 수: {len(PROBLEM_TEMPLATE.regions)}")
