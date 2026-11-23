"""ModuMath Problem DSL: 정삼각형의 뜻 완성하기 (S3_초등_4_007360)"""

from __future__ import annotations

from modu_math.dsl import (
    Canvas,
    CircleSlot,
    PolygonSlot,
    ProblemTemplate,
    RectSlot,
    Region,
    TextBoxSlot,
    TextSlot,
)


PROBLEM_ID = "S3_초등_4_007360"
PROBLEM_TITLE = "정삼각형을 설명한 것을 읽고 알맞은 말 선택하기"

ANSWER = {
    "value": "③",
    "answer_index": 2,
    "unit": "",
    "values": ["③"],
    "choices": [
        "① 두, 같은",
        "② 두, 다른",
        "③ 세, 같은",
        "④ 세, 다른",
    ],
    "blanks": [],
    "answer_key": [
        {
            "slot_id": "slot.choice.option_2",
            "value": "③",
            "diagnostics": [
                {
                    "id": "diag.confused_isosceles",
                    "condition": "answer_equals_1",
                    "concept": "정삼각형과 이등변삼각형의 구분",
                    "reason": "두 변의 길이가 같은 이등변삼각형과 혼동함",
                    "feedback": "두 변의 길이가 같은 삼각형은 이등변삼각형입니다. 정삼각형은 세 변의 길이가 모두 같은 삼각형입니다.",
                },
            ],
        },
    ],
}

SEMANTIC = {
    "problem_id": PROBLEM_ID,
    "problem_type": "multiple_choice_equilateral_definition",
    "metadata": {
        "school": "초등학교",
        "grade": 4,
        "semester": "2학기",
        "chapter": "02단원_삼각형",
        "difficulty": "하",
    },
    "entities": {
        "definition": {"label": "정삼각형", "sides": 3, "relation": "같은"},
    },
    "relations": [
        {
            "type": "definition",
            "term": "정삼각형",
            "correct_choice": "③ 세, 같은",
        }
    ],
}


def build_problem_template() -> ProblemTemplate:
    stem_text_slot = TextBoxSlot(
        id="slot.stem.question",
        prompt="",
        text="34. 정삼각형을 설명한 것을 읽고 알맞은 말을 선택하세요.",
        x=32,
        y=24,
        width=820,
        height=44,
        font_size=22,
        font_family='"Noto Sans KR", sans-serif',
        fill="#202124",
        align="left",
        valign="top",
        line_height=1.5,
    )

    diagram_slots = [
        # 초록색 삼각형 캐릭터
        PolygonSlot(id="slot.diagram.char_head", prompt="", points=[(300, 82), (250, 170), (350, 170)], fill="#65a30d", stroke="#3f6212", stroke_width=2.0),
        CircleSlot(id="slot.diagram.char_eye_l", prompt="", cx=288, cy=132, r=7, fill="#ffffff", stroke="#111827", stroke_width=1.2),
        CircleSlot(id="slot.diagram.char_eye_r", prompt="", cx=312, cy=132, r=7, fill="#ffffff", stroke="#111827", stroke_width=1.2),
        CircleSlot(id="slot.diagram.char_pupil_l", prompt="", cx=288, cy=132, r=3.5, fill="#111827", stroke="none"),
        CircleSlot(id="slot.diagram.char_pupil_r", prompt="", cx=312, cy=132, r=3.5, fill="#111827", stroke="none"),
        RectSlot(id="slot.diagram.char_body", prompt="", x=280, y=170, width=40, height=34, fill="#facc15", stroke="#ca8a04", stroke_width=1.5, rx=6, ry=6),
        # 말풍선
        RectSlot(id="slot.diagram.bubble", prompt="", x=388, y=92, width=320, height=84, fill="#ffffff", stroke="#111827", stroke_width=1.6, rx=28, ry=28),
        TextBoxSlot(
            id="slot.diagram.bubble_text",
            prompt="",
            text="내 얼굴처럼 세 변의\n길이가 같은 삼각형이야.",
            x=408,
            y=108,
            width=280,
            height=56,
            font_size=18,
            font_family='"Noto Sans KR", sans-serif',
            fill="#111827",
            align="center",
            valign="middle",
            line_height=1.4,
        ),
        # 빈칸 문장
        TextSlot(
            id="slot.diagram.sentence",
            prompt="",
            text="( 두 , 세 ) 변의 길이가 ( 같은 , 다른 ) 삼각형을 정삼각형이라고 합니다.",
            x=443,
            y=232,
            font_size=21,
            font_family='"Noto Sans KR", sans-serif',
            fill="#111827",
            align="center",
        ),
    ]

    opts = ["① 두, 같은", "② 두, 다른", "③ 세, 같은", "④ 세, 다른"]
    choice_slots = []
    for idx, label in enumerate(opts):
        cx = 76 + idx * 190
        choice_slots.append(
            RectSlot(
                id=f"slot.choice.option_{idx}",
                prompt="",
                x=cx,
                y=288,
                width=168,
                height=48,
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
                x=cx + 84,
                y=300,
                font_size=18,
                font_family='"Noto Sans KR", sans-serif',
                fill="#111827",
                align="center",
            )
        )

    return ProblemTemplate(
        id=PROBLEM_ID,
        title=PROBLEM_TITLE,
        canvas=Canvas(width=886, height=368, coordinate_mode="logical"),
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
    "given": [{"ref": "definition", "value": "세 변의 길이가 같은 삼각형"}],
    "target": {"ref": "slot.choice.option_2", "label": "알맞은 말", "unit": ""},
    "method": "definition_matching",
    "steps": [
        {
            "id": "match_definition",
            "expr": "세 변의 길이가 같은 삼각형 = 정삼각형",
            "explanation": "세 변의 길이가 같은 삼각형을 정삼각형이라고 합니다.",
            "value": "③",
        },
    ],
    "answer": ANSWER,
}


if __name__ == "__main__":
    print(f"[{PROBLEM_TEMPLATE.id}] 템플릿 컴파일 성공!")
