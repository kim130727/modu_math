"""ModuMath Problem DSL: 그림그래프에 필요한 그림의 가지 수 선택하기 (S3_초등_3_008889)"""

from __future__ import annotations

from modu_math.dsl import (
    Canvas,
    ProblemTemplate,
    Region,
    TextBoxSlot,
    TextSlot,
    table_slots,
)


PROBLEM_ID = "S3_초등_3_008889"
PROBLEM_TITLE = "표를 보고 그림그래프에 필요한 그림의 가지 수 선택하기"

ANSWER = {
    "type": "choice",
    "value": "2",
    "unit": "",
    "answer_index": 1,
    "values": ["2"],
    "blanks": [],
    "choices": [
        {"id": "slot.choice.option_0", "slot_id": "slot.choice.option_0", "text": "1", "value": "1"},
        {"id": "slot.choice.option_1", "slot_id": "slot.choice.option_1", "text": "2", "value": "2"},
    ],
    "answer_key": [{"slot_id": "slot.choice.option_1", "value": "2"}],
}

SEMANTIC_OVERRIDE = {
    "problem_id": PROBLEM_ID,
    "problem_type": "multiple_choice_picture_graph_design",
    "metadata": {
        "grade": 3,
        "semester": 2,
        "subject": "수학",
        "chapter": "06단원_자료의 정리",
        "language": "ko-KR",
    },
    "domain": {
        "objects": [
            {"id": "farm.ga", "type": "survey_item", "label": "가", "production_kg": 36},
            {"id": "farm.na", "type": "survey_item", "label": "나", "production_kg": 31},
            {"id": "farm.da", "type": "survey_item", "label": "다", "production_kg": 25},
            {"id": "farm.ra", "type": "survey_item", "label": "라", "production_kg": 43},
        ],
        "relations": [
            {
                "id": "relation.icon_kinds",
                "type": "requires_icon_types",
                "from_id": "farm.ga",
                "to_id": "value.2",
            }
        ],
    },
    "answer": ANSWER,
}


def build_problem_template() -> ProblemTemplate:
    stem_slot = TextBoxSlot(
        id="slot.stem.question",
        prompt="",
        text="53. 호정이네 마을의 목장에서 생산한 우유의 양을 조사하여 표로 나타내었습니다. 알맞은 것을 선택하세요.",
        x=32,
        y=18,
        width=820,
        height=60,
        font_size=21,
        font_family='"Noto Sans KR", sans-serif',
        fill="#202124",
        align="left",
        valign="top",
        line_height=1.45,
    )

    table_title = TextSlot(id="slot.diagram.table_title", prompt="", text="목장별 우유 생산량", x=443, y=94, font_size=20, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center")
    tbl = table_slots(
        "slot.diagram.table",
        x=185,
        y=114,
        col_widths=(160, 72, 72, 72, 72, 80),
        row_heights=(40, 40),
        cells=(
            ("목장", "가", "나", "다", "라", "합계"),
            ("생산량(kg)", "36", "31", "25", "43", "135"),
        ),
        font_size=19,
        stroke="#f59e0b",
    )

    sent_left = TextSlot(id="slot.diagram.sent_left", prompt="", text="우유 생산량이 두 자리 수이므로 그림을 (", x=318, y=236, font_size=22, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center")
    opt_0 = TextSlot(id="slot.choice.option_0", prompt="", text="1", x=538, y=236, font_size=22, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center", interaction={"type": "choice", "role": "answer", "choice_index": 0, "value": "1", "group_id": "slot.choice.group", "include_in_submission": True})
    comma_1 = TextSlot(id="slot.choice.comma_1", prompt="", text=",", x=562, y=236, font_size=22, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center")
    opt_1 = TextSlot(id="slot.choice.option_1", prompt="", text="2", x=586, y=236, font_size=22, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center", interaction={"type": "choice", "role": "answer", "choice_index": 1, "value": "2", "group_id": "slot.choice.group", "include_in_submission": True})
    sent_right = TextSlot(id="slot.diagram.sent_right", prompt="", text=")가지로 나타냅니다.", x=702, y=236, font_size=22, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center")

    diagram_slots = (table_title, *tbl, sent_left, sent_right)

    return ProblemTemplate(
        id=PROBLEM_ID,
        title=PROBLEM_TITLE,
        canvas=Canvas(width=886, height=275, coordinate_mode="logical"),
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
        {"ref": "farm.ga", "value": 36},
        {"ref": "farm.na", "value": 31},
        {"ref": "farm.da", "value": 25},
        {"ref": "farm.ra", "value": 43},
    ],
    "target": {"ref": "slot.choice.option_1", "type": "choice"},
    "method": "determine_picture_graph_icon_count",
    "steps": [
        {
            "id": "step.count_digits",
            "expr": "digits(two_digit_number) == 2",
            "value": "2",
            "explanation": "우유 생산량이 십의 자리와 일의 자리로 이루어진 두 자리 수이므로 십의 자리(10 kg)와 일의 자리(1 kg)를 나타내는 그림 2가지로 나타냅니다.",
        }
    ],
    "answer": ANSWER,
    "diagnostics": {
        "skills": ["data.picture_graph_design"],
        "errors": {
            "1": "data.forgot_place_value_icons",
        },
    },
}
