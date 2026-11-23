"""ModuMath Problem DSL: 소수의 1/10과 소수점 이동 방향 (S3_초등_4_007503)"""

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


PROBLEM_ID = "S3_초등_4_007503"
PROBLEM_TITLE = "소수의 1/10을 할 때 소수점 이동 방향과 자릿수 선택하기"

ANSWER = {
    "value": "①",
    "answer_index": 0,
    "unit": "",
    "values": ["①"],
    "choices": [
        "① 왼쪽, 한",
        "② 왼쪽, 두",
        "③ 오른쪽, 한",
        "④ 오른쪽, 두",
    ],
    "blanks": [],
    "answer_key": [
        {
            "slot_id": "slot.choice.option_0",
            "value": "①",
            "diagnostics": [
                {
                    "id": "diag.wrong_shift_direction",
                    "condition": "answer_not_1",
                    "concept": "소수의 1/10과 소수점 이동",
                    "reason": "1/10을 할 때 소수점이 왼쪽으로 한 자리 이동한다는 성질을 놓침",
                    "feedback": "1 → 0.1 → 0.01 → 0.001처럼 소수의 1/10을 하면 소수점이 왼쪽으로 한 자리 이동합니다.",
                },
            ],
        },
    ],
}

SEMANTIC = {
    "problem_id": PROBLEM_ID,
    "problem_type": "multiple_choice_decimal_shift_rule",
    "metadata": {
        "school": "초등학교",
        "grade": 4,
        "semester": "2학기",
        "chapter": "03단원_소수의 덧셈과 뺄셈",
        "difficulty": "중",
    },
    "entities": {
        "sequence": {"label": "소수 관계표", "values": ["1", "0.1", "0.01", "0.001"]},
        "rule": {"label": "1/10 규칙", "direction": "왼쪽", "places": "한"},
    },
    "relations": [
        {
            "type": "decimal_shift",
            "factor": "1/10",
            "direction": "왼쪽",
            "digits": 1,
        }
    ],
}


def _add_decimal_table(slots: list, tx: int, ty: int) -> None:
    cw, rh = 44, 34
    slots.append(RectSlot(id="slot.diagram.tbl_outer", prompt="", x=tx, y=ty, width=cw * 4, height=rh * 4, fill="#ffffff", stroke="#fb923c", stroke_width=1.4))
    for r in range(1, 4):
        slots.append(LineSlot(id=f"slot.diagram.tbl_hr_{r}", prompt="", x1=tx, y1=ty + r * rh, x2=tx + cw * 4, y2=ty + r * rh, stroke="#fb923c", stroke_width=1.0))
    for c in range(1, 4):
        slots.append(LineSlot(id=f"slot.diagram.tbl_vc_{c}", prompt="", x1=tx + c * cw, y1=ty, x2=tx + c * cw, y2=ty + rh * 4, stroke="#fb923c", stroke_width=0.9, stroke_dasharray="3,3"))

    rows = [
        ["1", "", "", ""],
        ["0.", "1", "", ""],
        ["0.", "0", "1", ""],
        ["0.", "0", "0", "1"],
    ]
    for r_idx, row in enumerate(rows):
        for c_idx, ch in enumerate(row):
            if ch:
                slots.append(TextSlot(id=f"slot.diagram.cell_{r_idx}_{c_idx}", prompt="", text=ch, x=tx + c_idx * cw + 22, y=ty + r_idx * rh + 8, font_size=19, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center"))
    for r in range(3):
        slots.append(TextSlot(id=f"slot.diagram.ratio_{r}", prompt="", text="↘ 1/10", x=tx + cw * 4 + 34, y=ty + r * rh + 24, font_size=14, font_family='"Noto Sans KR", sans-serif', fill="#ec4899", align="center"))


def build_problem_template() -> ProblemTemplate:
    stem_text_slot = TextBoxSlot(
        id="slot.stem.question",
        prompt="",
        text="28. 1, 0.1, 0.01, 0.001 사이의 관계를 보고 알맞은 것을 선택하세요.",
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

    diagram_slots = []
    _add_decimal_table(diagram_slots, 336, 78)
    diagram_slots.append(TextBoxSlot(
        id="slot.diagram.question_sub",
        prompt="",
        text="(1) 소수의 1/10을 하면 소수점이 ( 왼쪽 , 오른쪽 )으로 ( 한 , 두 ) 자리 이동합니다.",
        x=68,
        y=232,
        width=750,
        height=48,
        font_size=20,
        font_family='"Noto Sans KR", sans-serif',
        fill="#111827",
        align="center",
        valign="middle",
        line_height=1.4,
    ))

    opts = ["① 왼쪽, 한", "② 왼쪽, 두", "③ 오른쪽, 한", "④ 오른쪽, 두"]
    choice_slots = []
    for idx, label in enumerate(opts):
        cx = 76 + idx * 190
        choice_slots.append(
            RectSlot(
                id=f"slot.choice.option_{idx}",
                prompt="",
                x=cx,
                y=294,
                width=168,
                height=46,
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
                y=305,
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
    "given": [{"ref": "sequence", "value": "1, 0.1, 0.01, 0.001"}],
    "target": {"ref": "slot.choice.option_0", "label": "소수점 이동 방향과 자릿수", "unit": ""},
    "method": "decimal_shift_rule",
    "steps": [
        {
            "id": "observe_shift",
            "expr": "소수의 1/10 -> 소수점이 왼쪽으로 한 자리 이동",
            "explanation": "소수의 1/10을 하면 소수점이 왼쪽으로 한 자리 이동합니다.",
            "value": "①",
        },
    ],
    "answer": ANSWER,
}


if __name__ == "__main__":
    print(f"[{PROBLEM_TEMPLATE.id}] 템플릿 컴파일 성공!")
