"""ModuMath Problem DSL: 사다리꼴에 대해 잘못 말한 학생 찾기 (S3_초등_4_007553)"""

from __future__ import annotations

from modu_math.dsl import (
    Canvas,
    CircleSlot,
    ProblemTemplate,
    RectSlot,
    Region,
    TextBoxSlot,
    TextSlot,
)


PROBLEM_ID = "S3_초등_4_007553"
PROBLEM_TITLE = "사다리꼴에 대해 잘못 말한 학생 선택하기"

ANSWER = {
    "value": "희진",
    "answer_index": 1,
    "unit": "",
    "values": ["희진"],
    "choices": [
        "동호",
        "희진",
    ],
    "blanks": [],
    "answer_key": [
        {
            "slot_id": "slot.choice.option_1",
            "value": "희진",
            "diagnostics": [
                {
                    "id": "diag.chose_correct_speaker",
                    "condition": "answer_equals_dongho",
                    "concept": "사다리꼴의 성질",
                    "reason": "사다리꼴은 사각형이므로 변이 4개, 각이 4개인 것은 맞음을 놓침",
                    "feedback": "동호의 말처럼 사다리꼴은 4개의 변과 4개의 각이 있습니다. 평행한 변이 한 쌍이라도 있는 사각형이 사다리꼴이므로 잘못 말한 학생은 희진입니다.",
                },
            ],
        },
    ],
}

SEMANTIC = {
    "problem_id": PROBLEM_ID,
    "problem_type": "multiple_choice_trapezoid_misconception",
    "metadata": {
        "school": "초등학교",
        "grade": 4,
        "semester": "2학기",
        "chapter": "04단원_사각형",
        "difficulty": "하",
    },
    "entities": {
        "dongho": {"label": "동호", "claim": "4개의 변과 4개의 각이 있어.", "is_correct": True},
        "heejin": {"label": "희진", "claim": "서로 평행한 변이 없어.", "is_correct": False},
    },
    "relations": [
        {
            "type": "false_claim_detection",
            "correct_entity": "heejin",
            "distractor": "dongho",
        }
    ],
}


def build_problem_template() -> ProblemTemplate:
    stem_text_slot = TextBoxSlot(
        id="slot.stem.question",
        prompt="",
        text="98. 사다리꼴에 대해 잘못 말한 학생을 선택해 보세요.",
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

    choice_0 = RectSlot(id="slot.choice.option_0", prompt="", x=316, y=206, width=84, height=40, fill="#ffffff", stroke="#d8b4fe", stroke_width=1.8, rx=8, ry=8, interaction={"type": "choice", "role": "answer", "choice_index": 0, "value": "동호", "group_id": "slot.choice.group", "include_in_submission": True})
    choice_1 = RectSlot(id="slot.choice.option_1", prompt="", x=512, y=206, width=84, height=40, fill="#ffffff", stroke="#d8b4fe", stroke_width=1.8, rx=8, ry=8, interaction={"type": "choice", "role": "answer", "choice_index": 1, "value": "희진", "group_id": "slot.choice.group", "include_in_submission": True})

    diagram_slots = [
        RectSlot(id="slot.diagram.bub_0", prompt="", x=112, y=94, width=188, height=96, fill="#ffffff", stroke="#111827", stroke_width=1.5, rx=28, ry=28),
        TextBoxSlot(id="slot.diagram.bub_txt_0", prompt="", text="4개의 변과\n4개의 각이 있어.", x=124, y=112, width=164, height=62, font_size=18, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center", valign="middle", line_height=1.4),
        CircleSlot(id="slot.diagram.face_0", prompt="", cx=358, cy=142, r=26, fill="#fde68a", stroke="#15803d", stroke_width=1.4),
        TextSlot(id="slot.diagram.name_0", prompt="", text="동호", x=358, y=214, font_size=19, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center"),

        CircleSlot(id="slot.diagram.face_1", prompt="", cx=554, cy=142, r=26, fill="#fde68a", stroke="#be185d", stroke_width=1.4),
        TextSlot(id="slot.diagram.name_1", prompt="", text="희진", x=554, y=214, font_size=19, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center"),
        RectSlot(id="slot.diagram.bub_1", prompt="", x=612, y=94, width=188, height=96, fill="#ffffff", stroke="#111827", stroke_width=1.5, rx=28, ry=28),
        TextBoxSlot(id="slot.diagram.bub_txt_1", prompt="", text="서로 평행한\n변이 없어.", x=624, y=112, width=164, height=62, font_size=18, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center", valign="middle", line_height=1.4),
    ]

    return ProblemTemplate(
        id=PROBLEM_ID,
        title=PROBLEM_TITLE,
        canvas=Canvas(width=886, height=274, coordinate_mode="logical"),
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
    "given": [
        {"ref": "dongho", "value": "4개의 변과 4개의 각이 있어."},
        {"ref": "heejin", "value": "서로 평행한 변이 없어."},
    ],
    "target": {"ref": "slot.choice.option_1", "label": "잘못 말한 학생", "unit": ""},
    "method": "definition_check",
    "steps": [
        {
            "id": "find_false_claim",
            "expr": "사다리꼴은 평행한 변이 한 쌍 이상 있음 -> 희진의 말이 틀림",
            "explanation": "평행한 변이 한 쌍이라도 있는 사각형을 사다리꼴이라고 하므로 희진이 잘못 말했습니다.",
            "value": "희진",
        },
    ],
    "answer": ANSWER,
}


if __name__ == "__main__":
    print(f"[{PROBLEM_TEMPLATE.id}] 템플릿 컴파일 성공!")
