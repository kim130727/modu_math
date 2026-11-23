"""ModuMath Problem DSL: 색종이 접어 정삼각형 만들기 (S3_초등_4_007364)"""

from __future__ import annotations

from modu_math.dsl import (
    Canvas,
    LineSlot,
    PolygonSlot,
    ProblemTemplate,
    RectSlot,
    Region,
    TextBoxSlot,
    TextSlot,
)


PROBLEM_ID = "S3_초등_4_007364"
PROBLEM_TITLE = "색종이로 만든 삼각형의 종류와 이유 고르기"

ANSWER = {
    "value": "①",
    "answer_index": 0,
    "unit": "",
    "values": ["①"],
    "choices": [
        "① 정삼각형, 같으므로, 같기",
        "② 정삼각형, 다르므로, 같기",
        "③ 이등변삼각형, 같으므로, 다르기",
        "④ 이등변삼각형, 다르므로, 다르기",
    ],
    "blanks": [],
    "answer_key": [
        {
            "slot_id": "slot.choice.option_0",
            "value": "①",
            "diagnostics": [
                {
                    "id": "diag.missed_equilateral_folding",
                    "condition": "answer_not_1",
                    "concept": "정삼각형 만들기와 성질",
                    "reason": "색종이의 한 변과 그린 두 변의 길이가 모두 같아 정삼각형이 됨을 놓침",
                    "feedback": "서로 겹치도록 접어서 그린 두 변의 길이는 색종이의 한 변의 길이와 같으므로 세 변의 길이가 모두 같은 정삼각형입니다.",
                },
            ],
        },
    ],
}

SEMANTIC = {
    "problem_id": PROBLEM_ID,
    "problem_type": "multiple_choice_paper_folding_equilateral",
    "metadata": {
        "school": "초등학교",
        "grade": 4,
        "semester": "2학기",
        "chapter": "02단원_삼각형",
        "difficulty": "중",
    },
    "entities": {
        "triangle": {"label": "만든 삼각형", "type": "정삼각형"},
        "reason": {"label": "이유", "value": "세 변의 길이가 모두 같음"},
    },
    "relations": [
        {
            "type": "construction_property",
            "method": "paper_folding",
            "result": "정삼각형",
        }
    ],
}


def build_problem_template() -> ProblemTemplate:
    stem_text_slot = TextBoxSlot(
        id="slot.stem.question",
        prompt="",
        text="40. 색종이로 그림과 같이 삼각형을 만들었을 때 만든 삼각형이 어떤 삼각형인지 찾고 알맞은 말을 고르세요.",
        x=32,
        y=24,
        width=820,
        height=64,
        font_size=22,
        font_family='"Noto Sans KR", sans-serif',
        fill="#202124",
        align="left",
        valign="top",
        line_height=1.5,
    )

    diagram_slots = []
    # 5단계 종이접기 도식
    step_x = [110, 248, 386, 524, 662]
    for i, sx in enumerate(step_x):
        diagram_slots.append(RectSlot(id=f"slot.diagram.paper_{i}", prompt="", x=sx, y=96, width=84, height=84, fill="#ddd6fe", stroke="#6b7280", stroke_width=1.2))
        diagram_slots.append(LineSlot(id=f"slot.diagram.fold_{i}", prompt="", x1=sx + 42, y1=96, x2=sx + 42, y2=180, stroke="#94a3b8", stroke_width=1.0, stroke_dasharray="3,3"))
        if i < 4:
            diagram_slots.append(TextSlot(id=f"slot.diagram.arrow_{i}", prompt="", text="→", x=sx + 111, y=126, font_size=22, font_family='"Noto Sans KR", sans-serif', fill="#6b7280", align="center"))

    diagram_slots.append(PolygonSlot(id="slot.diagram.step2_tri", prompt="", points=[(386, 180), (428, 96), (470, 146)], fill="#fef08a", stroke="#111827", stroke_width=1.2))
    diagram_slots.append(PolygonSlot(id="slot.diagram.step3_tri", prompt="", points=[(608, 180), (566, 96), (524, 146)], fill="#fef08a", stroke="#111827", stroke_width=1.2))
    diagram_slots.append(PolygonSlot(id="slot.diagram.step4_tri", prompt="", points=[(662, 180), (704, 96), (746, 180)], fill="none", stroke="#111827", stroke_width=2.0))

    # 표
    diagram_slots.append(RectSlot(id="slot.diagram.tbl_r1_l", prompt="", x=56, y=200, width=148, height=54, fill="#ffffff", stroke="#86efac", stroke_width=1.5))
    diagram_slots.append(RectSlot(id="slot.diagram.tbl_r1_r", prompt="", x=204, y=200, width=626, height=54, fill="#ffffff", stroke="#86efac", stroke_width=1.5))
    diagram_slots.append(RectSlot(id="slot.diagram.tbl_r2_l", prompt="", x=56, y=254, width=148, height=100, fill="#ffffff", stroke="#86efac", stroke_width=1.5))
    diagram_slots.append(RectSlot(id="slot.diagram.tbl_r2_r", prompt="", x=204, y=254, width=626, height=100, fill="#ffffff", stroke="#86efac", stroke_width=1.5))

    diagram_slots.append(RectSlot(id="slot.diagram.lbl_bg1", prompt="", x=68, y=212, width=124, height=30, fill="#c084fc", stroke="none"))
    diagram_slots.append(TextSlot(id="slot.diagram.lbl_1", prompt="", text="만든 삼각형", x=130, y=217, font_size=17, font_family='"Noto Sans KR", sans-serif', fill="#ffffff", align="center"))
    diagram_slots.append(TextSlot(id="slot.diagram.val_1", prompt="", text="( 정삼각형, 이등변삼각형 )", x=517, y=217, font_size=19, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center"))

    diagram_slots.append(RectSlot(id="slot.diagram.lbl_bg2", prompt="", x=100, y=289, width=60, height=30, fill="#c084fc", stroke="none"))
    diagram_slots.append(TextSlot(id="slot.diagram.lbl_2", prompt="", text="이유", x=130, y=294, font_size=17, font_family='"Noto Sans KR", sans-serif', fill="#ffffff", align="center"))
    diagram_slots.append(TextBoxSlot(
        id="slot.diagram.val_2",
        prompt="",
        text="색종이에 그린 두 변의 길이는 색종이의 한 변의 길이와 ( 같으므로, 다르므로 ) 세 변의 길이가 모두 ( 같기, 다르기 ) 때문입니다.",
        x=222,
        y=268,
        width=590,
        height=74,
        font_size=18,
        font_family='"Noto Sans KR", sans-serif',
        fill="#111827",
        align="left",
        valign="middle",
        line_height=1.5,
    ))

    opts = [
        "① 정삼각형, 같으므로, 같기",
        "② 정삼각형, 다르므로, 같기",
        "③ 이등변삼각형, 같으므로, 다르기",
        "④ 이등변삼각형, 다르므로, 다르기",
    ]
    choice_slots = []
    for idx, label in enumerate(opts):
        col = idx % 2
        row = idx // 2
        cx = 56 + col * 396
        cy = 374 + row * 56
        choice_slots.append(
            RectSlot(
                id=f"slot.choice.option_{idx}",
                prompt="",
                x=cx,
                y=cy,
                width=378,
                height=44,
                fill="#f8fafc",
                stroke="#94a3b8",
                stroke_width=1.5,
                rx=8,
                ry=8,
                interaction={
                    "type": "choice",
                    "role": "answer",
                    "choice_index": idx,
                    "value": label.split(" ")[0],
                    "group_id": "slot.choice.group",
                    "include_in_submission": True,
                },
            )
        )
        diagram_slots.append(
            TextSlot(
                id=f"slot.diagram.opt_text_{idx}",
                prompt="",
                text=label,
                x=cx + 18,
                y=cy + 12,
                font_size=17,
                font_family='"Noto Sans KR", sans-serif',
                fill="#111827",
                align="left",
            )
        )

    return ProblemTemplate(
        id=PROBLEM_ID,
        title=PROBLEM_TITLE,
        canvas=Canvas(width=886, height=496, coordinate_mode="logical"),
        regions=(
            Region(id="region.stem", role="stem", flow="absolute", slot_ids=("slot.stem.question",)),
            Region(id="region.choices", role="choices", flow="absolute", slot_ids=tuple(s.id for s in choice_slots)),
            Region(id="region.diagram", role="diagram", flow="absolute", slot_ids=tuple(s.id for s in diagram_slots)),
        ),
        slots=(stem_text_slot, *choice_slots, *diagram_slots),
    )


PROBLEM_TEMPLATE = build_problem_template()
SEMANTIC_OVERRIDE = SEMANTIC
SEMANTIC_ANSWER = ANSWER
SOLVABLE = {
    "schema": "modu.solvable.v1.3",
    "problem_id": PROBLEM_ID,
    "problem_type": SEMANTIC["problem_type"],
    "given": [{"ref": "triangle", "value": "색종이를 접어 한 변의 길이와 같게 그린 삼각형"}],
    "target": {"ref": "slot.choice.option_0", "label": "만든 삼각형과 이유", "unit": ""},
    "method": "geometric_reasoning",
    "steps": [
        {
            "id": "reason_equilateral",
            "expr": "그린 두 변 = 색종이의 한 변 -> 세 변의 길이가 모두 같음",
            "explanation": "그린 변의 길이와 색종이의 한 변의 길이가 같으므로 세 변의 길이가 모두 같은 정삼각형입니다.",
            "value": "①",
        },
    ],
    "answer": ANSWER,
}


if __name__ == "__main__":
    print(f"[{PROBLEM_TEMPLATE.id}] 템플릿 컴파일 성공!")
