"""ModuMath Problem DSL: 지우개 두께에 알맞은 단위 선택하기 (S3_초등_3_009178)"""

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


PROBLEM_ID = "S3_초등_3_009178"
PROBLEM_TITLE = "지우개의 두께에 알맞은 단위 선택하기"

ANSWER = {
    "type": "choice",
    "value": "mm",
    "unit": "",
    "answer_index": 0,
    "values": ["mm"],
    "blanks": [],
    "choices": [
        {"id": "slot.choice.option_0", "slot_id": "slot.choice.option_0", "text": "mm", "value": "mm"},
        {"id": "slot.choice.option_1", "slot_id": "slot.choice.option_1", "text": "cm", "value": "cm"},
    ],
    "answer_key": [
        {
            "slot_id": "slot.choice.option_0",
            "value": "mm",
        }
    ],
}

SEMANTIC_OVERRIDE = {
    "problem_id": PROBLEM_ID,
    "problem_type": "multiple_choice_unit_estimation",
    "metadata": {
        "grade": 3,
        "semester": 1,
        "subject": "수학",
        "chapter": "05단원_길이와 시간",
        "language": "ko-KR",
    },
    "domain": {
        "objects": [
            {"id": "object.eraser_thickness", "type": "measured_length", "label": "지우개의 두께", "numeric_value": 9},
        ],
        "relations": [
            {
                "id": "relation.appropriate_unit",
                "type": "has_unit",
                "from_id": "object.eraser_thickness",
                "to_id": "unit.mm",
            }
        ],
    },
    "answer": ANSWER,
}


def build_problem_template() -> ProblemTemplate:
    stem_slot = TextBoxSlot(
        id="slot.stem.question",
        prompt="",
        text="40. □ 안에 들어갈 알맞은 단위를 선택해 보세요.",
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

    outer_box = RectSlot(
        id="slot.diagram.outer_box",
        prompt="",
        x=210,
        y=72,
        width=655,
        height=175,
        fill="#ffffff",
        stroke="#7c3aed",
        stroke_width=1.2,
    )
    divider_line = LineSlot(id="slot.diagram.divider", prompt="", x1=210, y1=195, x2=865, y2=195, stroke="#7c3aed", stroke_width=1.0)

    # 지우개 일러스트
    eraser_front = RectSlot(id="slot.diagram.eraser_front", prompt="", x=470, y=94, width=90, height=40, fill="#e0e7ff", stroke="#94a3b8", stroke_width=1.0)
    eraser_band = RectSlot(id="slot.diagram.eraser_band", prompt="", x=518, y=94, width=36, height=40, fill="#f472b6", stroke="#db2777", stroke_width=1.0)
    eraser_label = TextSlot(id="slot.diagram.eraser_label", prompt="", text="지우개", x=536, y=114, font_size=12, font_family='"Noto Sans KR", sans-serif', fill="#ffffff", align="center")
    eraser_top = PolygonSlot(id="slot.diagram.eraser_top", prompt="", points=((470, 94), (495, 80), (585, 80), (560, 94)), fill="#f1f5f9", stroke="#94a3b8", stroke_width=1.0)

    sent_left = TextSlot(id="slot.diagram.sent_left", prompt="", text="지우개의 두께는 약 9", x=450, y=166, font_size=24, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center")
    blank_box = RectSlot(id="slot.diagram.blank", prompt="", x=578, y=148, width=64, height=34, fill="#ffffff", stroke="#111827", stroke_width=1.2)
    sent_right = TextSlot(id="slot.diagram.sent_right", prompt="", text="입니다.", x=695, y=166, font_size=24, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center")

    opt_0 = TextSlot(
        id="slot.choice.option_0",
        prompt="",
        text="mm",
        x=455,
        y=220,
        font_size=24,
        font_family='"Noto Sans KR", sans-serif',
        fill="#111827",
        align="center",
        interaction={"type": "choice", "role": "answer", "choice_index": 0, "value": "mm", "group_id": "slot.choice.group", "include_in_submission": True},
    )
    opt_1 = TextSlot(
        id="slot.choice.option_1",
        prompt="",
        text="cm",
        x=610,
        y=220,
        font_size=24,
        font_family='"Noto Sans KR", sans-serif',
        fill="#111827",
        align="center",
        interaction={"type": "choice", "role": "answer", "choice_index": 1, "value": "cm", "group_id": "slot.choice.group", "include_in_submission": True},
    )

    diagram_slots = (outer_box, divider_line, eraser_front, eraser_band, eraser_label, eraser_top, sent_left, blank_box, sent_right)

    return ProblemTemplate(
        id=PROBLEM_ID,
        title=PROBLEM_TITLE,
        canvas=Canvas(width=886, height=265, coordinate_mode="logical"),
        regions=(
            Region(id="region.stem", role="stem", flow="absolute", slot_ids=("slot.stem.question",)),
            Region(id="region.diagram", role="diagram", flow="absolute", slot_ids=tuple(s.id for s in diagram_slots)),
            Region(id="region.choices", role="choices", flow="absolute", slot_ids=("slot.choice.option_0", "slot.choice.option_1")),
        ),
        slots=(stem_slot, *diagram_slots, opt_0, opt_1),
    )


PROBLEM_TEMPLATE = build_problem_template()

SOLVABLE = {
    "schema": "modu.solvable.v1.3",
    "problem_id": PROBLEM_ID,
    "given": [
        {"ref": "object.eraser_thickness", "value": 9},
    ],
    "target": {"ref": "slot.choice.option_0", "type": "choice"},
    "method": "estimate_appropriate_length_unit",
    "steps": [
        {
            "id": "step.estimate",
            "expr": "thickness(eraser) < 9 cm",
            "value": "mm",
            "explanation": "지우개의 두께는 9 cm보다 얇으므로 알맞은 단위는 mm입니다.",
        }
    ],
    "answer": ANSWER,
    "diagnostics": {
        "skills": ["measurement.unit_estimation_mm_cm"],
        "errors": {
            "cm": "measurement.overestimated_small_object",
        },
    },
}
