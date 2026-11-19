"""ModuMath Problem DSL: 1 km 바르게 쓰기 (S3_초등_3_009175)"""

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


PROBLEM_ID = "S3_초등_3_009175"
PROBLEM_TITLE = "1 km를 바르게 쓴 것 선택하기"

ANSWER = {
    "type": "choice",
    "value": "오른쪽 표기(1은 2칸)",
    "unit": "",
    "answer_index": 1,
    "values": ["오른쪽 표기(1은 2칸)"],
    "blanks": [],
    "choices": [
        {"id": "slot.choice.option_0", "slot_id": "slot.choice.option_0", "text": "왼쪽 표기(1은 1칸)", "value": "왼쪽 표기(1은 1칸)"},
        {"id": "slot.choice.option_1", "slot_id": "slot.choice.option_1", "text": "오른쪽 표기(1은 2칸)", "value": "오른쪽 표기(1은 2칸)"},
    ],
    "answer_key": [
        {
            "slot_id": "slot.choice.option_1",
            "value": "오른쪽 표기(1은 2칸)",
        }
    ],
}

SEMANTIC_OVERRIDE = {
    "problem_id": PROBLEM_ID,
    "problem_type": "multiple_choice_unit_notation",
    "metadata": {
        "grade": 3,
        "semester": 1,
        "subject": "수학",
        "chapter": "05단원_길이와 시간",
        "language": "ko-KR",
    },
    "domain": {
        "objects": [
            {"id": "notation.option_0", "type": "unit_writing", "label": "왼쪽 표기", "number_height_lines": 1, "is_correct": False},
            {"id": "notation.option_1", "type": "unit_writing", "label": "오른쪽 표기", "number_height_lines": 2, "is_correct": True},
        ],
        "relations": [
            {
                "id": "relation.correct_notation",
                "type": "is_proper_notation",
                "from_id": "notation.option_1",
                "to_id": "unit.1km",
            }
        ],
    },
    "answer": ANSWER,
}


def _guide_lines(prefix: str, x1: float, x2: float, top_y: float, step: float = 16.0) -> list[LineSlot]:
    return [
        LineSlot(
            id=f"{prefix}_line_{i}",
            prompt="",
            x1=x1,
            y1=top_y + i * step,
            x2=x2,
            y2=top_y + i * step,
            stroke="#38bdf8",
            stroke_width=1.0,
            stroke_dasharray="3,3",
        )
        for i in range(4)
    ]


def build_problem_template() -> ProblemTemplate:
    stem_slot = TextBoxSlot(
        id="slot.stem.question",
        prompt="",
        text="37. 1 km를 바르게 쓴 것을 선택하세요.",
        x=32,
        y=22,
        width=820,
        height=44,
        font_size=24,
        font_family='"Noto Sans KR", sans-serif',
        fill="#202124",
        align="left",
        valign="top",
        line_height=1.5,
    )

    lines_0 = _guide_lines("slot.diagram.guide0", 365, 550, 82)
    num_0 = TextSlot(id="slot.diagram.num0", prompt="", text="1", x=402, y=118, font_size=26, font_family='"Noto Serif", serif', fill="#111827", align="center")
    unit_0 = TextSlot(id="slot.diagram.unit0", prompt="", text="km", x=485, y=108, font_size=42, font_family='"Noto Serif", serif', fill="#111827", align="center")
    choice_0 = RectSlot(
        id="slot.choice.option_0",
        prompt="",
        x=355,
        y=74,
        width=205,
        height=72,
        fill="transparent",
        stroke="none",
        stroke_width=0,
        interaction={"type": "choice", "role": "answer", "choice_index": 0, "value": "왼쪽 표기(1은 1칸)", "group_id": "slot.choice.group", "include_in_submission": True},
    )

    lines_1 = _guide_lines("slot.diagram.guide1", 660, 845, 82)
    num_1 = TextSlot(id="slot.diagram.num1", prompt="", text="1", x=697, y=108, font_size=46, font_family='"Noto Serif", serif', fill="#111827", align="center")
    unit_1 = TextSlot(id="slot.diagram.unit1", prompt="", text="km", x=780, y=108, font_size=42, font_family='"Noto Serif", serif', fill="#111827", align="center")
    choice_1 = RectSlot(
        id="slot.choice.option_1",
        prompt="",
        x=650,
        y=74,
        width=205,
        height=72,
        fill="transparent",
        stroke="none",
        stroke_width=0,
        interaction={"type": "choice", "role": "answer", "choice_index": 1, "value": "오른쪽 표기(1은 2칸)", "group_id": "slot.choice.group", "include_in_submission": True},
    )

    diagram_slots = (*lines_0, num_0, unit_0, *lines_1, num_1, unit_1)

    return ProblemTemplate(
        id=PROBLEM_ID,
        title=PROBLEM_TITLE,
        canvas=Canvas(width=886, height=175, coordinate_mode="logical"),
        regions=(
            Region(id="region.stem", role="stem", flow="absolute", slot_ids=("slot.stem.question",)),
            Region(id="region.diagram", role="diagram", flow="absolute", slot_ids=tuple(s.id for s in diagram_slots)),
            Region(id="region.choices", role="choices", flow="absolute", slot_ids=("slot.choice.option_0", "slot.choice.option_1")),
        ),
        slots=(stem_slot, *diagram_slots, choice_0, choice_1),
    )


PROBLEM_TEMPLATE = build_problem_template()

SOLVABLE = {
    "schema": "modu.solvable.v1.3",
    "problem_id": PROBLEM_ID,
    "given": [
        {"ref": "notation.option_0", "value": "1은 1칸"},
        {"ref": "notation.option_1", "value": "1은 2칸"},
    ],
    "target": {"ref": "slot.choice.option_1", "type": "choice"},
    "method": "check_unit_writing_proportion",
    "steps": [
        {
            "id": "step.check_lines",
            "expr": "height(1) == 2_spaces",
            "value": "오른쪽 표기(1은 2칸)",
            "explanation": "숫자 1은 두 칸에 걸쳐 써야 합니다.",
        }
    ],
    "answer": ANSWER,
    "diagnostics": {
        "skills": ["measurement.unit_notation_km"],
        "errors": {
            "왼쪽 표기(1은 1칸)": "notation.number_written_too_small",
        },
    },
}
