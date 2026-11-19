"""ModuMath Problem DSL: 부등식 □ 안에 들어갈 수 있는 수 모두 선택하기 (S3_초등_3_009159)"""

from __future__ import annotations

from modu_math.dsl import (
    Canvas,
    ProblemTemplate,
    RectSlot,
    Region,
    TextBoxSlot,
    TextSlot,
)


PROBLEM_ID = "S3_초등_3_009159"
PROBLEM_TITLE = "곱셈 부등식 □ 안에 들어갈 수 있는 수 모두 선택하기"

ANSWER = {
    "type": "multi_choice",
    "value": ["1", "2", "3", "4", "5"],
    "unit": "",
    "values": ["1", "2", "3", "4", "5"],
    "blanks": [],
    "choices": [
        {"id": f"slot.choice.option_{i}", "slot_id": f"slot.choice.option_{i}", "text": str(i + 1), "value": str(i + 1)}
        for i in range(9)
    ],
    "answer_key": [
        {"slot_id": f"slot.choice.option_{i}", "value": str(i + 1)}
        for i in range(5)
    ],
}

SEMANTIC_OVERRIDE = {
    "problem_id": PROBLEM_ID,
    "problem_type": "multiple_select_multiplication_inequality",
    "metadata": {
        "grade": 3,
        "semester": 1,
        "subject": "수학",
        "chapter": "04단원_곱셈",
        "language": "ko-KR",
    },
    "domain": {
        "objects": [
            {"id": "expr.lhs", "type": "multiplication", "label": "36 × 3", "value": 108},
            {"id": "expr.rhs", "type": "multiplication_with_unknown", "label": "18 × □", "known_factor": 18, "unknown": "□"},
            {"id": "domain.candidates", "type": "integer_range", "min": 1, "max": 9},
        ],
        "relations": [
            {
                "id": "relation.inequality",
                "type": "greater_than",
                "from_id": "expr.lhs",
                "to_id": "expr.rhs",
            }
        ],
    },
    "answer": ANSWER,
}


def build_problem_template() -> ProblemTemplate:
    stem_slot = TextBoxSlot(
        id="slot.stem.question",
        prompt="",
        text="19. 1부터 9까지의 자연수 중에서 □ 안에 들어갈 수 있는 수를 모두 선택하세요.",
        x=32,
        y=20,
        width=820,
        height=64,
        font_size=22,
        font_family='"Noto Sans KR", sans-serif',
        fill="#202124",
        align="left",
        valign="top",
        line_height=1.5,
    )

    expr_box = RectSlot(
        id="slot.diagram.expr_box",
        prompt="",
        x=265,
        y=92,
        width=360,
        height=68,
        fill="#fff1f0",
        stroke="none",
        stroke_width=0,
    )
    expr_text = TextSlot(
        id="slot.diagram.expr_text",
        prompt="",
        text="36 × 3 > 18 ×",
        x=425,
        y=126,
        font_size=24,
        font_family='"Noto Sans KR", sans-serif',
        fill="#111827",
        align="center",
    )
    blank_box = RectSlot(
        id="slot.diagram.blank_box",
        prompt="",
        x=518,
        y=111,
        width=28,
        height=28,
        fill="#ffffff",
        stroke="#111827",
        stroke_width=1.3,
    )

    paren_l = TextSlot(id="slot.choice.paren_l", prompt="", text="(", x=240, y=195, font_size=24, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center")
    choice_slots = []
    comma_slots = []
    choice_ids = ["slot.choice.paren_l"]
    for i in range(9):
        cx = 272 + i * 44
        opt = TextSlot(
            id=f"slot.choice.option_{i}",
            prompt="",
            text=str(i + 1),
            x=cx,
            y=195,
            font_size=22,
            font_family='"Noto Sans KR", sans-serif',
            fill="#111827",
            align="center",
            interaction={
                "type": "choice",
                "role": "answer",
                "choice_index": i,
                "value": str(i + 1),
                "group_id": "slot.choice.group",
                "multi_select": True,
                "include_in_submission": True,
            },
        )
        choice_slots.append(opt)
        choice_ids.append(opt.id)
        if i < 8:
            comma = TextSlot(
                id=f"slot.choice.comma_{i + 1}",
                prompt="",
                text=",",
                x=cx + 22,
                y=195,
                font_size=22,
                font_family='"Noto Sans KR", sans-serif',
                fill="#111827",
                align="center",
            )
            comma_slots.append(comma)
            choice_ids.append(comma.id)

    paren_r = TextSlot(id="slot.choice.paren_r", prompt="", text=")", x=656, y=195, font_size=24, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center")
    choice_ids.append("slot.choice.paren_r")

    return ProblemTemplate(
        id=PROBLEM_ID,
        title=PROBLEM_TITLE,
        canvas=Canvas(width=886, height=235, coordinate_mode="logical"),
        regions=(
            Region(id="region.stem", role="stem", flow="absolute", slot_ids=("slot.stem.question",)),
            Region(id="region.diagram", role="diagram", flow="absolute", slot_ids=("slot.diagram.expr_box", "slot.diagram.expr_text", "slot.diagram.blank_box")),
            Region(id="region.choices", role="choices", flow="absolute", slot_ids=tuple(choice_ids)),
        ),
        slots=(stem_slot, expr_box, expr_text, blank_box, paren_l, *choice_slots, *comma_slots, paren_r),
    )


PROBLEM_TEMPLATE = build_problem_template()

SOLVABLE = {
    "schema": "modu.solvable.v1.3",
    "problem_id": PROBLEM_ID,
    "given": [
        {"ref": "expr.lhs", "value": "36 × 3"},
        {"ref": "expr.rhs", "value": "18 × □"},
        {"ref": "domain.candidates", "value": [1, 2, 3, 4, 5, 6, 7, 8, 9]},
    ],
    "target": {"ref": "answer.values", "type": "choice_list"},
    "method": "solve_multiplication_inequality",
    "steps": [
        {"id": "step.calc_lhs", "expr": "36 * 3", "value": 108, "explanation": "36 × 3 = 108입니다."},
        {"id": "step.find_boundary", "expr": "18 * 6 = 108", "value": 6, "explanation": "18 × 6 = 108이므로 108 > 18 × □를 만족하려면 □는 6보다 작아야 합니다."},
        {"id": "step.filter_domain", "expr": "1 <= x < 6", "value": [1, 2, 3, 4, 5], "explanation": "1부터 9까지의 자연수 중 6보다 작은 수는 1, 2, 3, 4, 5입니다."},
    ],
    "answer": ANSWER,
    "diagnostics": {
        "skills": ["multiplication.inequality_reasoning"],
        "errors": {
            "6": "inequality.included_boundary",
        },
    },
}
