"""ModuMath Problem DSL: 4 km 300 m 바르게 읽기 (S3_초등_3_009176)"""

from __future__ import annotations

from modu_math.dsl import (
    Canvas,
    ProblemTemplate,
    RectSlot,
    Region,
    TextBoxSlot,
    TextSlot,
)


PROBLEM_ID = "S3_초등_3_009176"
PROBLEM_TITLE = "4 km 300 m를 바르게 읽은 것 선택하기"

ANSWER = {
    "type": "choice",
    "value": "4 킬로미터 300 미터",
    "unit": "",
    "answer_index": 1,
    "values": ["4 킬로미터 300 미터"],
    "blanks": [],
    "choices": [
        {"id": "slot.choice.option_0", "slot_id": "slot.choice.option_0", "text": "4 킬로 300 미터", "value": "4 킬로 300 미터"},
        {"id": "slot.choice.option_1", "slot_id": "slot.choice.option_1", "text": "4 킬로미터 300 미터", "value": "4 킬로미터 300 미터"},
    ],
    "answer_key": [
        {
            "slot_id": "slot.choice.option_1",
            "value": "4 킬로미터 300 미터",
        }
    ],
}

SEMANTIC_OVERRIDE = {
    "problem_id": PROBLEM_ID,
    "problem_type": "multiple_choice_unit_reading",
    "metadata": {
        "grade": 3,
        "semester": 1,
        "subject": "수학",
        "chapter": "05단원_길이와 시간",
        "language": "ko-KR",
    },
    "domain": {
        "objects": [
            {"id": "qty.given", "type": "length", "label": "4 km 300 m"},
            {"id": "reading.option_0", "type": "unit_reading", "text": "4 킬로 300 미터"},
            {"id": "reading.option_1", "type": "unit_reading", "text": "4 킬로미터 300 미터"},
        ],
        "relations": [
            {
                "id": "relation.reading",
                "type": "correct_reading_of",
                "from_id": "reading.option_1",
                "to_id": "qty.given",
            }
        ],
    },
    "answer": ANSWER,
}


def build_problem_template() -> ProblemTemplate:
    stem_slot = TextBoxSlot(
        id="slot.stem.question",
        prompt="",
        text="38. 4 km 300 m를 바르게 읽은 것을 선택하세요.",
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

    box_0 = RectSlot(
        id="slot.choice.option_0",
        prompt="",
        x=95,
        y=80,
        width=330,
        height=64,
        fill="#fce7f3",
        stroke="#ec4899",
        stroke_width=1.2,
        interaction={"type": "choice", "role": "answer", "choice_index": 0, "value": "4 킬로 300 미터", "group_id": "slot.choice.group", "include_in_submission": True},
    )
    text_0 = TextSlot(id="slot.choice.label_0", prompt="", text="4 킬로 300 미터", x=260, y=112, font_size=22, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center")

    box_1 = RectSlot(
        id="slot.choice.option_1",
        prompt="",
        x=515,
        y=80,
        width=330,
        height=64,
        fill="#fce7f3",
        stroke="#ec4899",
        stroke_width=1.2,
        interaction={"type": "choice", "role": "answer", "choice_index": 1, "value": "4 킬로미터 300 미터", "group_id": "slot.choice.group", "include_in_submission": True},
    )
    text_1 = TextSlot(id="slot.choice.label_1", prompt="", text="4 킬로미터 300 미터", x=680, y=112, font_size=22, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center")

    return ProblemTemplate(
        id=PROBLEM_ID,
        title=PROBLEM_TITLE,
        canvas=Canvas(width=886, height=175, coordinate_mode="logical"),
        regions=(
            Region(id="region.stem", role="stem", flow="absolute", slot_ids=("slot.stem.question",)),
            Region(id="region.choices", role="choices", flow="absolute", slot_ids=("slot.choice.option_0", "slot.choice.label_0", "slot.choice.option_1", "slot.choice.label_1")),
        ),
        slots=(stem_slot, box_0, text_0, box_1, text_1),
    )


PROBLEM_TEMPLATE = build_problem_template()

SOLVABLE = {
    "schema": "modu.solvable.v1.3",
    "problem_id": PROBLEM_ID,
    "given": [
        {"ref": "qty.given", "value": "4 km 300 m"},
    ],
    "target": {"ref": "slot.choice.option_1", "type": "choice"},
    "method": "read_length_units",
    "steps": [
        {
            "id": "step.read_units",
            "expr": "km -> 킬로미터, m -> 미터",
            "value": "4 킬로미터 300 미터",
            "explanation": "km는 킬로미터, m는 미터라고 읽으므로 4 km 300 m는 '4 킬로미터 300 미터'라고 읽습니다.",
        }
    ],
    "answer": ANSWER,
    "diagnostics": {
        "skills": ["measurement.unit_reading_km_m"],
        "errors": {
            "4 킬로 300 미터": "measurement.abbreviated_unit_reading",
        },
    },
}
