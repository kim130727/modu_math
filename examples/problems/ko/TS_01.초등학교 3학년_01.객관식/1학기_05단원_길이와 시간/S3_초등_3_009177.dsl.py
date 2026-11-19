"""ModuMath Problem DSL: 학교 뒷산의 높이에 알맞은 단위 선택하기 (S3_초등_3_009177)"""

from __future__ import annotations

from modu_math.dsl import (
    Canvas,
    PolygonSlot,
    ProblemTemplate,
    RectSlot,
    Region,
    TextBoxSlot,
    TextSlot,
)


PROBLEM_ID = "S3_초등_3_009177"
PROBLEM_TITLE = "학교 뒷산의 높이에 알맞은 단위 선택하기"

ANSWER = {
    "type": "choice",
    "value": "km",
    "unit": "",
    "answer_index": 1,
    "values": ["km"],
    "blanks": [],
    "choices": [
        {"id": "slot.choice.option_0", "slot_id": "slot.choice.option_0", "text": "m", "value": "m"},
        {"id": "slot.choice.option_1", "slot_id": "slot.choice.option_1", "text": "km", "value": "km"},
    ],
    "answer_key": [
        {
            "slot_id": "slot.choice.option_1",
            "value": "km",
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
            {"id": "object.mountain_height", "type": "measured_length", "label": "학교 뒷산의 높이", "numeric_value": 1},
        ],
        "relations": [
            {
                "id": "relation.appropriate_unit",
                "type": "has_unit",
                "from_id": "object.mountain_height",
                "to_id": "unit.km",
            }
        ],
    },
    "answer": ANSWER,
}


def build_problem_template() -> ProblemTemplate:
    stem_slot = TextBoxSlot(
        id="slot.stem.question",
        prompt="",
        text="39. 알맞은 단위를 선택하세요.",
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

    # 산 일러스트
    mtn_back = PolygonSlot(
        id="slot.diagram.mountain_back",
        prompt="",
        points=((60, 175), (125, 118), (185, 175)),
        fill="#4d7c0f",
        stroke="#3f6212",
        stroke_width=1,
    )
    mtn_main = PolygonSlot(
        id="slot.diagram.mountain_main",
        prompt="",
        points=((105, 175), (185, 76), (275, 175)),
        fill="#65a30d",
        stroke="#3f6212",
        stroke_width=1,
    )

    box_frame = RectSlot(
        id="slot.diagram.frame",
        prompt="",
        x=325,
        y=84,
        width=540,
        height=76,
        fill="#ffffff",
        stroke="#7c3aed",
        stroke_width=1.2,
    )
    sent_left = TextSlot(id="slot.diagram.sent_left", prompt="", text="학교 뒷산의 높이는 1 (", x=485, y=122, font_size=24, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center")
    opt_0 = TextSlot(
        id="slot.choice.option_0",
        prompt="",
        text="m",
        x=632,
        y=122,
        font_size=24,
        font_family='"Noto Sans KR", sans-serif',
        fill="#111827",
        align="center",
        interaction={"type": "choice", "role": "answer", "choice_index": 0, "value": "m", "group_id": "slot.choice.group", "include_in_submission": True},
    )
    comma_1 = TextSlot(id="slot.choice.comma_1", prompt="", text=",", x=664, y=122, font_size=24, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center")
    opt_1 = TextSlot(
        id="slot.choice.option_1",
        prompt="",
        text="km",
        x=702,
        y=122,
        font_size=24,
        font_family='"Noto Sans KR", sans-serif',
        fill="#111827",
        align="center",
        interaction={"type": "choice", "role": "answer", "choice_index": 1, "value": "km", "group_id": "slot.choice.group", "include_in_submission": True},
    )
    sent_right = TextSlot(id="slot.diagram.sent_right", prompt="", text=")입니다.", x=780, y=122, font_size=24, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center")

    diagram_slots = (mtn_back, mtn_main, box_frame, sent_left, sent_right)

    return ProblemTemplate(
        id=PROBLEM_ID,
        title=PROBLEM_TITLE,
        canvas=Canvas(width=886, height=195, coordinate_mode="logical"),
        regions=(
            Region(id="region.stem", role="stem", flow="absolute", slot_ids=("slot.stem.question",)),
            Region(id="region.diagram", role="diagram", flow="absolute", slot_ids=tuple(s.id for s in diagram_slots)),
            Region(id="region.choices", role="choices", flow="absolute", slot_ids=("slot.choice.option_0", "slot.choice.comma_1", "slot.choice.option_1")),
        ),
        slots=(stem_slot, *diagram_slots, opt_0, comma_1, opt_1),
    )


PROBLEM_TEMPLATE = build_problem_template()

SOLVABLE = {
    "schema": "modu.solvable.v1.3",
    "problem_id": PROBLEM_ID,
    "given": [
        {"ref": "object.mountain_height", "value": 1},
    ],
    "target": {"ref": "slot.choice.option_1", "type": "choice"},
    "method": "estimate_appropriate_length_unit",
    "steps": [
        {
            "id": "step.estimate",
            "expr": "height(mountain) >> 1 m",
            "value": "km",
            "explanation": "학교 뒷산의 높이는 1 m보다 훨씬 크므로 알맞은 단위는 km입니다.",
        }
    ],
    "answer": ANSWER,
    "diagnostics": {
        "skills": ["measurement.unit_estimation_m_km"],
        "errors": {
            "m": "measurement.underestimated_large_object",
        },
    },
}
