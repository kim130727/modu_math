"""ModuMath Problem DSL: 이등변삼각형의 두 각의 크기 (S3_초등_4_007365)"""

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


PROBLEM_ID = "S3_초등_4_007365"
PROBLEM_TITLE = "색종이로 만든 이등변삼각형에서 두 각의 크기 비교하기"

ANSWER = {
    "value": "같아",
    "answer_index": 0,
    "unit": "",
    "values": ["같아"],
    "choices": [
        "같아",
        "달라",
    ],
    "blanks": [],
    "answer_key": [
        {
            "slot_id": "slot.choice.option_0",
            "value": "같아",
            "diagnostics": [
                {
                    "id": "diag.chose_different",
                    "condition": "answer_equals_diff",
                    "concept": "이등변삼각형의 성질",
                    "reason": "겹쳐서 자른 두 각의 크기가 같다는 성질을 놓침",
                    "feedback": "색종이를 반으로 접어 겹쳐서 잘랐기 때문에 양쪽 두 각 ㄱ과 ㄴ의 크기는 같습니다.",
                },
            ],
        },
    ],
}

SEMANTIC = {
    "problem_id": PROBLEM_ID,
    "problem_type": "multiple_choice_isosceles_angles",
    "metadata": {
        "school": "초등학교",
        "grade": 4,
        "semester": "2학기",
        "chapter": "02단원_삼각형",
        "difficulty": "하",
    },
    "entities": {
        "angle_a": {"label": "ㄱ", "equals": "ㄴ"},
        "angle_b": {"label": "ㄴ", "equals": "ㄱ"},
    },
    "relations": [
        {
            "type": "angle_equality",
            "property": "isosceles_base_angles",
            "correct_choice": "같아",
        }
    ],
}


def build_problem_template() -> ProblemTemplate:
    stem_text_slot = TextBoxSlot(
        id="slot.stem.question",
        prompt="",
        text="41. 색종이 한 장을 반으로 접고 선을 따라 가위로 잘라 이등변삼각형을 만들었습니다. 그림을 보고 알맞은 말을 선택하세요.",
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

    diagram_slots = [
        # 1단계: 반으로 접기
        RectSlot(id="slot.diagram.s1", prompt="", x=142, y=102, width=100, height=96, fill="#ffffff", stroke="#6b7280", stroke_width=1.2, stroke_dasharray="4,3"),
        RectSlot(id="slot.diagram.s1_f", prompt="", x=142, y=102, width=50, height=96, fill="#fed7aa", stroke="#ea580c", stroke_width=1.4),
        TextSlot(id="slot.diagram.ar1", prompt="", text="→", x=272, y=136, font_size=22, font_family='"Noto Sans KR", sans-serif', fill="#6b7280", align="center"),

        # 2단계: 선 그리기
        RectSlot(id="slot.diagram.s2", prompt="", x=306, y=102, width=60, height=96, fill="#fed7aa", stroke="#ea580c", stroke_width=1.4),
        LineSlot(id="slot.diagram.s2_line", prompt="", x1=306, y1=198, x2=366, y2=102, stroke="#111827", stroke_width=1.8),
        TextSlot(id="slot.diagram.ar2", prompt="", text="→", x=398, y=136, font_size=22, font_family='"Noto Sans KR", sans-serif', fill="#6b7280", align="center"),

        # 3단계: 가위로 자르기
        RectSlot(id="slot.diagram.s3", prompt="", x=432, y=102, width=60, height=96, fill="#fed7aa", stroke="#ea580c", stroke_width=1.4),
        LineSlot(id="slot.diagram.s3_line", prompt="", x1=432, y1=198, x2=492, y2=102, stroke="#111827", stroke_width=1.8),
        TextSlot(id="slot.diagram.ar3", prompt="", text="→", x=524, y=136, font_size=22, font_family='"Noto Sans KR", sans-serif', fill="#6b7280", align="center"),

        # 4단계: 펼친 이등변삼각형
        PolygonSlot(id="slot.diagram.s4_tri", prompt="", points=[(626, 102), (566, 198), (686, 198)], fill="#bbf7d0", stroke="#16a34a", stroke_width=1.8),
        LineSlot(id="slot.diagram.s4_fold", prompt="", x1=626, y1=102, x2=626, y2=198, stroke="#16a34a", stroke_width=1.2, stroke_dasharray="3,3"),
        TextSlot(id="slot.diagram.ang_l", prompt="", text="ㄱ", x=590, y=174, font_size=16, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center"),
        TextSlot(id="slot.diagram.ang_r", prompt="", text="ㄴ", x=662, y=174, font_size=16, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center"),

        # 말풍선 & 캐릭터
        CircleSlot(id="slot.diagram.boy_head", prompt="", cx=222, cy=254, r=26, fill="#fde68a", stroke="#92400e", stroke_width=1.4),
        RectSlot(id="slot.diagram.bubble", prompt="", x=286, y=224, width=480, height=74, fill="#ffffff", stroke="#111827", stroke_width=1.6, rx=28, ry=28),
        TextBoxSlot(
            id="slot.diagram.bubble_txt",
            prompt="",
            text="겹쳐서 잘랐기 때문에 위 이등변삼각형에\n표시된 두 각의 크기는 ( 같아 , 달라 ).",
            x=306,
            y=236,
            width=440,
            height=52,
            font_size=18,
            font_family='"Noto Sans KR", sans-serif',
            fill="#111827",
            align="center",
            valign="middle",
            line_height=1.4,
        ),
    ]

    choice_0 = RectSlot(id="slot.choice.option_0", prompt="", x=280, y=322, width=136, height=48, fill="#f8fafc", stroke="#94a3b8", stroke_width=1.5, rx=8, ry=8, interaction={"type": "choice", "role": "answer", "choice_index": 0, "value": "같아", "group_id": "slot.choice.group", "include_in_submission": True})
    diagram_slots.append(TextSlot(id="slot.diagram.c0_txt", prompt="", text="같아", x=348, y=334, font_size=20, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center"))

    choice_1 = RectSlot(id="slot.choice.option_1", prompt="", x=470, y=322, width=136, height=48, fill="#f8fafc", stroke="#94a3b8", stroke_width=1.5, rx=8, ry=8, interaction={"type": "choice", "role": "answer", "choice_index": 1, "value": "달라", "group_id": "slot.choice.group", "include_in_submission": True})
    diagram_slots.append(TextSlot(id="slot.diagram.c1_txt", prompt="", text="달라", x=538, y=334, font_size=20, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center"))

    return ProblemTemplate(
        id=PROBLEM_ID,
        title=PROBLEM_TITLE,
        canvas=Canvas(width=886, height=396, coordinate_mode="logical"),
        regions=(
            Region(id="region.stem", role="stem", flow="absolute", slot_ids=("slot.stem.question",)),
            Region(id="region.choices", role="choices", flow="absolute", slot_ids=("slot.choice.option_0", "slot.choice.option_1")),
            Region(id="region.diagram", role="diagram", flow="absolute", slot_ids=tuple(s.id for s in diagram_slots)),
        ),
        slots=(stem_text_slot, choice_0, choice_1, *diagram_slots),
    )


PROBLEM_TEMPLATE = build_problem_template()
SEMANTIC_OVERRIDE = SEMANTIC
SEMANTIC_ANSWER = ANSWER
SOLVABLE = {
    "schema": "modu.solvable.v1.3",
    "problem_id": PROBLEM_ID,
    "problem_type": SEMANTIC["problem_type"],
    "given": [{"ref": "angle_a", "value": "겹쳐서 자른 이등변삼각형의 두 밑각 ㄱ, ㄴ"}],
    "target": {"ref": "slot.choice.option_0", "label": "두 각의 크기 비교", "unit": ""},
    "method": "triangle_property",
    "steps": [
        {
            "id": "compare_angles",
            "expr": "각 ㄱ = 각 ㄴ",
            "explanation": "이등변삼각형은 길이가 같은 두 변과 마주 보는 두 각의 크기가 같습니다.",
            "value": "같아",
        },
    ],
    "answer": ANSWER,
}


if __name__ == "__main__":
    print(f"[{PROBLEM_TEMPLATE.id}] 템플릿 컴파일 성공!")
