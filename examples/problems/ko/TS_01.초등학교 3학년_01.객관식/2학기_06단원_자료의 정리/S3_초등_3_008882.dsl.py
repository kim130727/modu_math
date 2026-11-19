"""ModuMath Problem DSL: 표를 보고 가장 많은 학생이 배우고 싶어 하는 운동 선택하기 (S3_초등_3_008882)"""

from __future__ import annotations

from modu_math.dsl import (
    Canvas,
    ProblemTemplate,
    Region,
    TextBoxSlot,
    TextSlot,
    table_slots,
)


PROBLEM_ID = "S3_초등_3_008882"
PROBLEM_TITLE = "표를 보고 가장 많은 학생이 배우고 싶어 하는 운동 선택하기"

ANSWER = {
    "type": "choice",
    "value": "야구",
    "unit": "",
    "answer_index": 2,
    "values": ["야구"],
    "blanks": [],
    "choices": [
        {"id": "slot.choice.option_0", "slot_id": "slot.choice.option_0", "text": "축구", "value": "축구"},
        {"id": "slot.choice.option_1", "slot_id": "slot.choice.option_1", "text": "골프", "value": "골프"},
        {"id": "slot.choice.option_2", "slot_id": "slot.choice.option_2", "text": "야구", "value": "야구"},
        {"id": "slot.choice.option_3", "slot_id": "slot.choice.option_3", "text": "스쿼시", "value": "스쿼시"},
    ],
    "answer_key": [{"slot_id": "slot.choice.option_2", "value": "야구"}],
}

SEMANTIC_OVERRIDE = {
    "problem_id": PROBLEM_ID,
    "problem_type": "multiple_choice_table_max",
    "metadata": {
        "grade": 3,
        "semester": 2,
        "subject": "수학",
        "chapter": "06단원_자료의 정리",
        "language": "ko-KR",
    },
    "domain": {
        "objects": [
            {"id": "cat.soccer", "type": "survey_item", "label": "축구", "count": 50},
            {"id": "cat.golf", "type": "survey_item", "label": "골프", "count": 30},
            {"id": "cat.baseball", "type": "survey_item", "label": "야구", "count": 55},
            {"id": "cat.squash", "type": "survey_item", "label": "스쿼시", "count": 50},
        ],
        "relations": [
            {
                "id": "relation.maximum",
                "type": "has_max_count",
                "from_id": "cat.baseball",
                "to_id": "value.55",
            }
        ],
    },
    "answer": ANSWER,
}


def build_problem_template() -> ProblemTemplate:
    stem_slot = TextBoxSlot(
        id="slot.stem.question",
        prompt="",
        text="46. 연우네 학교 학생들이 방과 후 수업으로 배우고 싶어 하는 운동을 조사하여 나타낸 표입니다. 표를 보고 알맞은 말을 선택해 보세요.",
        x=32,
        y=18,
        width=820,
        height=64,
        font_size=22,
        font_family='"Noto Sans KR", sans-serif',
        fill="#202124",
        align="left",
        valign="top",
        line_height=1.5,
    )

    table_title = TextSlot(id="slot.diagram.table_title", prompt="", text="배우고 싶어 하는 운동", x=443, y=98, font_size=22, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center")
    tbl = table_slots(
        "slot.diagram.table",
        x=118,
        y=118,
        col_widths=(170, 96, 96, 96, 96, 96),
        row_heights=(42, 42),
        cells=(
            ("운동", "축구", "골프", "야구", "스쿼시", "합계"),
            ("학생 수(명)", "50", "30", "55", "50", "185"),
        ),
        font_size=20,
        stroke="#65a30d",
    )

    sent_1 = TextSlot(id="slot.diagram.sent_1", prompt="", text="가장 많은 학생이 배우고 싶어 하는 운동은", x=443, y=236, font_size=22, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center")
    paren_l = TextSlot(id="slot.choice.paren_l", prompt="", text="(", x=230, y=274, font_size=22, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center")
    opt_0 = TextSlot(id="slot.choice.option_0", prompt="", text="축구", x=275, y=274, font_size=22, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center", interaction={"type": "choice", "role": "answer", "choice_index": 0, "value": "축구", "group_id": "slot.choice.group", "include_in_submission": True})
    comma_1 = TextSlot(id="slot.choice.comma_1", prompt="", text=",", x=315, y=274, font_size=22, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center")
    opt_1 = TextSlot(id="slot.choice.option_1", prompt="", text="골프", x=355, y=274, font_size=22, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center", interaction={"type": "choice", "role": "answer", "choice_index": 1, "value": "골프", "group_id": "slot.choice.group", "include_in_submission": True})
    comma_2 = TextSlot(id="slot.choice.comma_2", prompt="", text=",", x=395, y=274, font_size=22, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center")
    opt_2 = TextSlot(id="slot.choice.option_2", prompt="", text="야구", x=435, y=274, font_size=22, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center", interaction={"type": "choice", "role": "answer", "choice_index": 2, "value": "야구", "group_id": "slot.choice.group", "include_in_submission": True})
    comma_3 = TextSlot(id="slot.choice.comma_3", prompt="", text=",", x=475, y=274, font_size=22, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center")
    opt_3 = TextSlot(id="slot.choice.option_3", prompt="", text="스쿼시", x=525, y=274, font_size=22, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center", interaction={"type": "choice", "role": "answer", "choice_index": 3, "value": "스쿼시", "group_id": "slot.choice.group", "include_in_submission": True})
    paren_r = TextSlot(id="slot.choice.paren_r", prompt="", text=")입니다.", x=612, y=274, font_size=22, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center")

    diagram_slots = (table_title, *tbl, sent_1)

    return ProblemTemplate(
        id=PROBLEM_ID,
        title=PROBLEM_TITLE,
        canvas=Canvas(width=886, height=315, coordinate_mode="logical"),
        regions=(
            Region(id="region.stem", role="stem", flow="absolute", slot_ids=("slot.stem.question",)),
            Region(id="region.diagram", role="diagram", flow="absolute", slot_ids=tuple(s.id for s in diagram_slots)),
            Region(
                id="region.choices",
                role="choices",
                flow="absolute",
                slot_ids=("slot.choice.paren_l", "slot.choice.option_0", "slot.choice.comma_1", "slot.choice.option_1", "slot.choice.comma_2", "slot.choice.option_2", "slot.choice.comma_3", "slot.choice.option_3", "slot.choice.paren_r"),
            ),
        ),
        slots=(stem_slot, *diagram_slots, paren_l, opt_0, comma_1, opt_1, comma_2, opt_2, comma_3, opt_3, paren_r),
    )


PROBLEM_TEMPLATE = build_problem_template()

SOLVABLE = {
    "schema": "modu.solvable.v1.3",
    "problem_id": PROBLEM_ID,
    "given": [
        {"ref": "cat.soccer", "value": 50},
        {"ref": "cat.golf", "value": 30},
        {"ref": "cat.baseball", "value": 55},
        {"ref": "cat.squash", "value": 50},
    ],
    "target": {"ref": "slot.choice.option_2", "type": "choice"},
    "method": "find_maximum_in_table",
    "steps": [
        {
            "id": "step.find_max",
            "expr": "max(50, 30, 55, 50)",
            "value": "야구",
            "explanation": "학생 수에서 55가 가장 큰 수이므로 가장 많은 학생이 배우고 싶어 하는 운동은 야구입니다.",
        }
    ],
    "answer": ANSWER,
    "diagnostics": {
        "skills": ["data.table_interpretation_max"],
        "errors": {
            "골프": "data.chose_min_instead_of_max",
        },
    },
}
