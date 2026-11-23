"""ModuMath Problem DSL: 점 ㄱ을 지나고 직선 가에 수직인 직선 찾기 (S3_초등_4_007531)"""

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
PROBLEM_ID = "S3_초등_4_007531"
PROBLEM_TITLE = "점 ㄱ을 지나고 직선 가에 수직인 직선 선택하기"


# ==============================================================================
# 2. 정답 및 오답 진단 정의 (Answer & Diagnostic Key)
# ==============================================================================
ANSWER = {
    "value": "①",
    "answer_index": 0,
    "unit": "",
    "values": ["①"],
    "choices": [
        "①",
        "②",
    ],
    "blanks": [],
    "answer_key": [
        {
            "slot_id": "slot.choice.option_0",
            "value": "①",
            "diagnostics": [
                {
                    "id": "diag.chose_oblique_line",
                    "condition": "answer_equals_2",
                    "concept": "점과 수선",
                    "reason": "점 ㄱ을 지나지만 직선 가와 수직이 아닌 비스듬한 직선(②)을 선택함",
                    "feedback": "삼각자에서 직각을 낀 변 중 한 변을 직선 가에 맞춘 후 직각을 낀 다른 한 변을 따라 점 ㄱ을 지나게 그은 ①이 수직입니다.",
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
    "problem_type": "multiple_choice_perpendicular_through_point",
    "metadata": {
        "school": "초등학교",
        "grade": 4,
        "semester": "1학기",
        "chapter": "04단원_평면도형의 이동",
        "difficulty": "하",
    },
    "entities": {
        "option_0": {"label": "①", "passes_through_point": True, "is_perpendicular": True},
        "option_1": {"label": "②", "passes_through_point": True, "is_perpendicular": False},
    },
    "relations": [
        {
            "type": "perpendicular_through_point",
            "correct_entity": "option_0",
            "distractor": "option_1",
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
        text="66. 삼각자를 사용하여 점 ㄱ을 지나고 직선 가에 수직인 직선을 그은 것을 선택하세요.",
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

    # ① 수직인 직선
    card_0 = RectSlot(
        id="slot.choice.option_0",
        prompt="",
        x=116,
        y=92,
        width=290,
        height=168,
        fill="#ffffff",
        stroke="#e5e7eb",
        stroke_width=1.5,
        rx=10,
        ry=10,
        interaction={"type": "choice", "role": "answer", "choice_index": 0, "value": "①", "group_id": "slot.choice.group", "include_in_submission": True},
    )
    badge_0 = TextSlot(id="slot.diagram.badge_0", prompt="", text="①", x=140, y=106, font_size=20, font_family='"Noto Sans KR", sans-serif', fill="#4b5563", align="center")
    l0_ga_label = TextSlot(id="slot.diagram.l0_ga", prompt="", text="가", x=142, y=214, font_size=18, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center")
    l0_ga = LineSlot(id="slot.diagram.l0_base", prompt="", x1=160, y1=226, x2=384, y2=226, stroke="#111827", stroke_width=2)
    l0_perp = LineSlot(id="slot.diagram.l0_perp", prompt="", x1=272, y1=108, x2=272, y2=226, stroke="#111827", stroke_width=2)
    l0_pt = CircleSlot(id="slot.diagram.l0_pt", prompt="", cx=272, cy=136, r=3.5, fill="#111827", stroke="#111827", stroke_width=1)
    l0_pt_label = TextSlot(id="slot.diagram.l0_pt_lbl", prompt="", text="ㄱ", x=254, y=124, font_size=18, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center")

    # ② 비스듬한 직선
    card_1 = RectSlot(
        id="slot.choice.option_1",
        prompt="",
        x=480,
        y=92,
        width=290,
        height=168,
        fill="#ffffff",
        stroke="#e5e7eb",
        stroke_width=1.5,
        rx=10,
        ry=10,
        interaction={"type": "choice", "role": "answer", "choice_index": 1, "value": "②", "group_id": "slot.choice.group", "include_in_submission": True},
    )
    badge_1 = TextSlot(id="slot.diagram.badge_1", prompt="", text="②", x=504, y=106, font_size=20, font_family='"Noto Sans KR", sans-serif', fill="#4b5563", align="center")
    l1_ga_label = TextSlot(id="slot.diagram.l1_ga", prompt="", text="가", x=506, y=214, font_size=18, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center")
    l1_ga = LineSlot(id="slot.diagram.l1_base", prompt="", x1=524, y1=226, x2=748, y2=226, stroke="#111827", stroke_width=2)
    l1_ob = LineSlot(id="slot.diagram.l1_ob", prompt="", x1=566, y1=226, x2=682, y2=110, stroke="#111827", stroke_width=2)
    l1_pt = CircleSlot(id="slot.diagram.l1_pt", prompt="", cx=656, cy=136, r=3.5, fill="#111827", stroke="#111827", stroke_width=1)
    l1_pt_label = TextSlot(id="slot.diagram.l1_pt_lbl", prompt="", text="ㄱ", x=636, y=124, font_size=18, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center")

    return ProblemTemplate(
        id=PROBLEM_ID,
        title=PROBLEM_TITLE,
        canvas=Canvas(
            width=886,
            height=290,
            coordinate_mode="logical",
        ),
        regions=(
            Region(id="region.stem", role="stem", flow="absolute", slot_ids=("slot.stem.question",)),
            Region(id="region.choices", role="choices", flow="absolute", slot_ids=("slot.choice.option_0", "slot.choice.option_1")),
            Region(
                id="region.diagram",
                role="diagram",
                flow="absolute",
                slot_ids=(
                    "slot.diagram.badge_0",
                    "slot.diagram.l0_ga",
                    "slot.diagram.l0_base",
                    "slot.diagram.l0_perp",
                    "slot.diagram.l0_pt",
                    "slot.diagram.l0_pt_lbl",
                    "slot.diagram.badge_1",
                    "slot.diagram.l1_ga",
                    "slot.diagram.l1_base",
                    "slot.diagram.l1_ob",
                    "slot.diagram.l1_pt",
                    "slot.diagram.l1_pt_lbl",
                ),
            ),
        ),
        slots=(
            stem_text_slot,
            card_0,
            badge_0,
            l0_ga_label,
            l0_ga,
            l0_perp,
            l0_pt,
            l0_pt_label,
            card_1,
            badge_1,
            l1_ga_label,
            l1_ga,
            l1_ob,
            l1_pt,
            l1_pt_label,
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
        {"ref": "option_0", "value": "점 ㄱ을 지나고 직선 가에 수직인 직선"},
        {"ref": "option_1", "value": "점 ㄱ을 지나지만 수직이 아닌 직선"},
    ],
    "target": {"ref": "slot.choice.option_0", "label": "수직인 직선", "unit": ""},
    "method": "set_square_perpendicular",
    "steps": [
        {
            "id": "identify_perpendicular",
            "expr": "①",
            "explanation": "점 ㄱ을 지나고 직선 가와 직각으로 만나는 ①이 바릅니다.",
            "value": "①",
        },
    ],
    "answer": ANSWER,
}


if __name__ == "__main__":
    print(f"[{PROBLEM_TEMPLATE.id}] 템플릿 컴파일 성공!")
    print(f"- 제목: {PROBLEM_TEMPLATE.title}")
    print(f"- 캔버스: {PROBLEM_TEMPLATE.canvas.width} x {PROBLEM_TEMPLATE.canvas.height}")
    print(f"- 구역 수: {len(PROBLEM_TEMPLATE.regions)}")
