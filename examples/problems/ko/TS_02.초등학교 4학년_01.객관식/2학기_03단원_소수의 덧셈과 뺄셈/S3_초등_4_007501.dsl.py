"""ModuMath Problem DSL: 1/1000을 소수로 쓰고 읽기 (S3_초등_4_007501)"""

from __future__ import annotations

from modu_math.dsl import (
    Canvas,
    LineSlot,
    ProblemTemplate,
    RectSlot,
    Region,
    TextBoxSlot,
    TextSlot,
)


PROBLEM_ID = "S3_초등_4_007501"
PROBLEM_TITLE = "분수 1/1000을 소수로 쓰고 읽는 방법 선택하기"

ANSWER = {
    "value": "②",
    "answer_index": 1,
    "unit": "",
    "values": ["②"],
    "choices": [
        "① 0.01, 영 점 영일",
        "② 0.001, 영 점 영영일",
        "③ 0.01, 영 점 영영일",
        "④ 0.001, 영 점 영일",
    ],
    "blanks": [],
    "answer_key": [
        {
            "slot_id": "slot.choice.option_1",
            "value": "②",
            "diagnostics": [
                {
                    "id": "diag.confused_hundredth_thousandth",
                    "condition": "answer_not_2",
                    "concept": "소수 세 자리 수의 쓰기와 읽기",
                    "reason": "1/1000을 0.01(1/100)과 혼동함",
                    "feedback": "1/1000은 소수 세 자리 수이므로 0.001이라 쓰고 '영 점 영영일'이라고 읽습니다.",
                },
            ],
        },
    ],
}

SEMANTIC = {
    "problem_id": PROBLEM_ID,
    "problem_type": "multiple_choice_fraction_to_decimal",
    "metadata": {
        "school": "초등학교",
        "grade": 4,
        "semester": "2학기",
        "chapter": "03단원_소수의 덧셈과 뺄셈",
        "difficulty": "하",
    },
    "entities": {
        "fraction": {"label": "주어진 분수", "value": "1/1000"},
        "decimal": {"label": "소수 표현", "value": "0.001", "reading": "영 점 영영일"},
    },
    "relations": [
        {
            "type": "conversion",
            "from": "fraction",
            "to": "decimal",
            "correct_choice": "②",
        }
    ],
}


def build_problem_template() -> ProblemTemplate:
    stem_text_slot = TextBoxSlot(
        id="slot.stem.question",
        prompt="",
        text="26. 알맞은 것을 선택하세요.",
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
        RectSlot(id="slot.diagram.gold_box", prompt="", x=98, y=82, width=690, height=130, fill="#ffffff", stroke="#eab308", stroke_width=1.8),
        TextSlot(id="slot.diagram.r1_l", prompt="", text="분수", x=188, y=114, font_size=21, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center"),
        TextSlot(id="slot.diagram.frac_n", prompt="", text="1", x=244, y=96, font_size=19, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center"),
        LineSlot(id="slot.diagram.frac_bar", prompt="", x1=220, y1=120, x2=268, y2=120, stroke="#111827", stroke_width=1.5),
        TextSlot(id="slot.diagram.frac_d", prompt="", text="1000", x=244, y=126, font_size=19, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center"),
        TextSlot(id="slot.diagram.r1_r", prompt="", text="은 소수로 ( 0.01 , 0.001 )이라 쓰고,", x=480, y=114, font_size=21, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center"),
        TextSlot(id="slot.diagram.r2", prompt="", text="( 영 점 영일 , 영 점 영영일 )이라고 읽습니다.", x=443, y=166, font_size=21, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center"),
    ]

    opts = [
        "① 0.01, 영 점 영일",
        "② 0.001, 영 점 영영일",
        "③ 0.01, 영 점 영영일",
        "④ 0.001, 영 점 영일",
    ]
    choice_slots = []
    for idx, label in enumerate(opts):
        col = idx % 2
        row = idx // 2
        cx = 118 + col * 340
        cy = 236 + row * 56
        choice_slots.append(
            RectSlot(
                id=f"slot.choice.option_{idx}",
                prompt="",
                x=cx,
                y=cy,
                width=310,
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
                x=cx + 22,
                y=cy + 12,
                font_size=18,
                font_family='"Noto Sans KR", sans-serif',
                fill="#111827",
                align="left",
            )
        )

    return ProblemTemplate(
        id=PROBLEM_ID,
        title=PROBLEM_TITLE,
        canvas=Canvas(width=886, height=362, coordinate_mode="logical"),
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
    "given": [{"ref": "fraction", "value": "1/1000"}],
    "target": {"ref": "slot.choice.option_1", "label": "소수 표기와 읽기", "unit": ""},
    "method": "fraction_to_decimal",
    "steps": [
        {
            "id": "convert",
            "expr": "1/1000 = 0.001 (영 점 영영일)",
            "explanation": "분수 1/1000은 소수로 0.001이라 쓰고, 영 점 영영일이라고 읽습니다.",
            "value": "②",
        },
    ],
    "answer": ANSWER,
}


if __name__ == "__main__":
    print(f"[{PROBLEM_TEMPLATE.id}] 템플릿 컴파일 성공!")
