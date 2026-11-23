"""ModuMath Problem DSL: 소수 바르게 설명한 사람 고르기 (S3_초등_4_007483)"""

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


PROBLEM_ID = "S3_초등_4_007483"
PROBLEM_TITLE = "주어진 소수(2.63)를 바르게 설명한 사람 선택하기"

ANSWER = {
    "value": "두준",
    "answer_index": 1,
    "unit": "",
    "values": ["두준"],
    "choices": [
        "민영",
        "두준",
    ],
    "blanks": [],
    "answer_key": [
        {
            "slot_id": "slot.choice.option_1",
            "value": "두준",
            "diagnostics": [
                {
                    "id": "diag.wrong_decimal_reading",
                    "condition": "answer_equals_minyoung",
                    "concept": "소수 두 자리 수 읽기",
                    "reason": "소수점 아래를 '육십삼'처럼 자릿값을 붙여 읽은 민영을 선택함",
                    "feedback": "소수점 아래는 숫자만 차례대로 읽으므로 2.63은 '이 점 육삼'이라고 읽습니다. 2.63의 소수 둘째 자리 숫자는 3이므로 두준이 바르게 설명했습니다.",
                },
            ],
        },
    ],
}

SEMANTIC = {
    "problem_id": PROBLEM_ID,
    "problem_type": "multiple_choice_decimal_concept",
    "metadata": {
        "school": "초등학교",
        "grade": 4,
        "semester": "2학기",
        "chapter": "03단원_소수의 덧셈과 뺄셈",
        "difficulty": "하",
    },
    "entities": {
        "target_decimal": {"label": "주어진 소수", "value": "2.63"},
        "minyoung": {"label": "민영", "claim": "'이 점 육십삼'이라고 읽어.", "is_correct": False},
        "dujun": {"label": "두준", "claim": "소수 둘째 자리 숫자는 3이야.", "is_correct": True},
    },
    "relations": [
        {
            "type": "truth_evaluation",
            "correct_entity": "dujun",
            "distractor": "minyoung",
        }
    ],
}


def build_problem_template() -> ProblemTemplate:
    stem_text_slot = TextBoxSlot(
        id="slot.stem.question",
        prompt="",
        text="4. 주어진 소수를 바르게 설명한 사람을 선택해 보세요.",
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

    choice_0 = RectSlot(id="slot.choice.option_0", prompt="", x=284, y=224, width=84, height=40, fill="#ffffff", stroke="#d8b4fe", stroke_width=1.8, rx=8, ry=8, interaction={"type": "choice", "role": "answer", "choice_index": 0, "value": "민영", "group_id": "slot.choice.group", "include_in_submission": True})
    choice_1 = RectSlot(id="slot.choice.option_1", prompt="", x=520, y=224, width=84, height=40, fill="#ffffff", stroke="#d8b4fe", stroke_width=1.8, rx=8, ry=8, interaction={"type": "choice", "role": "answer", "choice_index": 1, "value": "두준", "group_id": "slot.choice.group", "include_in_submission": True})

    diagram_slots = [
        # 왼쪽 민영 말풍선 + 얼굴
        RectSlot(id="slot.diagram.bub_0", prompt="", x=78, y=96, width=182, height=96, fill="#ffffff", stroke="#111827", stroke_width=1.5, rx=28, ry=28),
        TextBoxSlot(id="slot.diagram.bub_txt_0", prompt="", text="'이 점 육십삼'\n이라고 읽어.", x=90, y=114, width=158, height=62, font_size=18, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center", valign="middle", line_height=1.4),
        CircleSlot(id="slot.diagram.face_0", prompt="", cx=326, cy=144, r=26, fill="#fde68a", stroke="#92400e", stroke_width=1.4),
        TextSlot(id="slot.diagram.name_0", prompt="", text="민영", x=326, y=232, font_size=19, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center"),

        # 가운데 숫자 카드 2.63
        RectSlot(id="slot.diagram.card", prompt="", x=388, y=116, width=110, height=58, fill="#ffedd5", stroke="#fdba74", stroke_width=1.4),
        TextSlot(id="slot.diagram.num", prompt="", text="2.63", x=443, y=132, font_size=24, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center"),

        # 오른쪽 두준 얼굴 + 말풍선
        CircleSlot(id="slot.diagram.face_1", prompt="", cx=562, cy=144, r=26, fill="#fde68a", stroke="#92400e", stroke_width=1.4),
        TextSlot(id="slot.diagram.name_1", prompt="", text="두준", x=562, y=232, font_size=19, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center"),
        RectSlot(id="slot.diagram.bub_1", prompt="", x=626, y=96, width=188, height=96, fill="#ffffff", stroke="#111827", stroke_width=1.5, rx=28, ry=28),
        TextBoxSlot(id="slot.diagram.bub_txt_1", prompt="", text="소수 둘째 자리\n숫자는 3이야.", x=638, y=114, width=164, height=62, font_size=18, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center", valign="middle", line_height=1.4),
    ]

    return ProblemTemplate(
        id=PROBLEM_ID,
        title=PROBLEM_TITLE,
        canvas=Canvas(width=886, height=292, coordinate_mode="logical"),
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
        {"ref": "target_decimal", "value": "2.63"},
        {"ref": "minyoung", "value": "'이 점 육십삼'이라고 읽어."},
        {"ref": "dujun", "value": "소수 둘째 자리 숫자는 3이야."},
    ],
    "target": {"ref": "slot.choice.option_1", "label": "바르게 설명한 사람", "unit": ""},
    "method": "decimal_place_value",
    "steps": [
        {
            "id": "verify_claims",
            "expr": "2.63 -> 소수 첫째 자리 6, 소수 둘째 자리 3",
            "explanation": "소수점 아래는 숫자만 차례대로 '이 점 육삼'으로 읽으며, 소수 둘째 자리 숫자는 3입니다.",
            "value": "두준",
        },
    ],
    "answer": ANSWER,
}


if __name__ == "__main__":
    print(f"[{PROBLEM_TEMPLATE.id}] 템플릿 컴파일 성공!")
