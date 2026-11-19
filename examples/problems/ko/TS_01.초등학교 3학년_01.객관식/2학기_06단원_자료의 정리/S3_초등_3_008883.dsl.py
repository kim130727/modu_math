"""ModuMath Problem DSL: 이원 표에서 여학생이 가장 많이 배우고 싶어 하는 운동 선택하기 (S3_초등_3_008883)"""

from __future__ import annotations

from modu_math.dsl import (
    Canvas,
    ProblemTemplate,
    Region,
    TextBoxSlot,
    TextSlot,
    table_slots,
)


PROBLEM_ID = "S3_초등_3_008883"
PROBLEM_TITLE = "표를 보고 여학생이 가장 많이 배우고 싶어 하는 운동 선택하기"

ANSWER = {
    "type": "choice",
    "value": "스쿼시",
    "unit": "",
    "answer_index": 3,
    "values": ["스쿼시"],
    "blanks": [],
    "choices": [
        {"id": "slot.choice.option_0", "slot_id": "slot.choice.option_0", "text": "축구", "value": "축구"},
        {"id": "slot.choice.option_1", "slot_id": "slot.choice.option_1", "text": "골프", "value": "골프"},
        {"id": "slot.choice.option_2", "slot_id": "slot.choice.option_2", "text": "야구", "value": "야구"},
        {"id": "slot.choice.option_3", "slot_id": "slot.choice.option_3", "text": "스쿼시", "value": "스쿼시"},
    ],
    "answer_key": [{"slot_id": "slot.choice.option_3", "value": "스쿼시"}],
}

SEMANTIC_OVERRIDE = {
    "problem_id": PROBLEM_ID,
    "problem_type": "multiple_choice_table_row_max",
    "metadata": {
        "grade": 3,
        "semester": 2,
        "subject": "수학",
        "chapter": "06단원_자료의 정리",
        "language": "ko-KR",
    },
    "domain": {
        "objects": [
            {"id": "cat.soccer_girls", "type": "survey_item", "label": "축구(여학생)", "count": 18},
            {"id": "cat.golf_girls", "type": "survey_item", "label": "골프(여학생)", "count": 10},
            {"id": "cat.baseball_girls", "type": "survey_item", "label": "야구(여학생)", "count": 27},
            {"id": "cat.squash_girls", "type": "survey_item", "label": "스쿼시(여학생)", "count": 35},
        ],
        "relations": [
            {
                "id": "relation.maximum_girls",
                "type": "has_max_count",
                "from_id": "cat.squash_girls",
                "to_id": "value.35",
            }
        ],
    },
    "answer": ANSWER,
}


def build_problem_template() -> ProblemTemplate:
    stem_slot = TextBoxSlot(
        id="slot.stem.question",
        prompt="",
        text="47. 연우네 학교 학생들이 방과 후 수업으로 배우고 싶어 하는 운동을 조사하여 나타낸 표입니다. 표를 보고 알맞은 말을 선택해 보세요.",
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

    table_title = TextSlot(id="slot.diagram.table_title", prompt="", text="여학생과 남학생이 배우고 싶어 하는 운동", x=443, y=98, font_size=22, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center")
    tbl = table_slots(
        "slot.diagram.table",
        x=118,
        y=118,
        col_widths=(170, 96, 96, 96, 96, 96),
        row_heights=(42, 42, 42),
        cells=(
            ("운동", "축구", "골프", "야구", "스쿼시", "합계"),
            ("여학생 수(명)", "18", "10", "27", "35", "90"),
            ("남학생 수(명)", "32", "20", "28", "15", "95"),
        ),
        font_size=20,
        stroke="#ec4899",
    )

    sent_1 = TextSlot(id="slot.diagram.sent_1", prompt="", text="여학생이 가장 많이 배우고 싶어 하는 운동은", x=443, y=276, font_size=22, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center")
    paren_l = TextSlot(id="slot.choice.paren_l", prompt="", text="(", x=230, y=314, font_size=22, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center")
    opt_0 = TextSlot(id="slot.choice.option_0", prompt="", text="축구", x=275, y=314, font_size=22, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center", interaction={"type": "choice", "role": "answer", "choice_index": 0, "value": "축구", "group_id": "slot.choice.group", "include_in_submission": True})
    comma_1 = TextSlot(id="slot.choice.comma_1", prompt="", text=",", x=315, y=314, font_size=22, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center")
    opt_1 = TextSlot(id="slot.choice.option_1", prompt="", text="골프", x=355, y=314, font_size=22, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center", interaction={"type": "choice", "role": "answer", "choice_index": 1, "value": "골프", "group_id": "slot.choice.group", "include_in_submission": True})
    comma_2 = TextSlot(id="slot.choice.comma_2", prompt="", text=",", x=395, y=314, font_size=22, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center")
    opt_2 = TextSlot(id="slot.choice.option_2", prompt="", text="야구", x=435, y=314, font_size=22, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center", interaction={"type": "choice", "role": "answer", "choice_index": 2, "value": "야구", "group_id": "slot.choice.group", "include_in_submission": True})
    comma_3 = TextSlot(id="slot.choice.comma_3", prompt="", text=",", x=475, y=314, font_size=22, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center")
    opt_3 = TextSlot(id="slot.choice.option_3", prompt="", text="스쿼시", x=525, y=314, font_size=22, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center", interaction={"type": "choice", "role": "answer", "choice_index": 3, "value": "스쿼시", "group_id": "slot.choice.group", "include_in_submission": True})
    paren_r = TextSlot(id="slot.choice.paren_r", prompt="", text=")입니다.", x=612, y=314, font_size=22, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center")

    diagram_slots = (table_title, *tbl, sent_1)

    return ProblemTemplate(
        id=PROBLEM_ID,
        title=PROBLEM_TITLE,
        canvas=Canvas(width=886, height=355, coordinate_mode="logical"),
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
        {"ref": "cat.soccer_girls", "value": 18},
        {"ref": "cat.golf_girls", "value": 10},
        {"ref": "cat.baseball_girls", "value": 27},
        {"ref": "cat.squash_girls", "value": 35},
    ],
    "target": {"ref": "slot.choice.option_3", "type": "choice"},
    "method": "find_row_maximum_in_table",
    "steps": [
        {
            "id": "step.find_max",
            "expr": "max(18, 10, 27, 35)",
            "value": "스쿼시",
            "explanation": "여학생 수를 살펴보면 가장 큰 수가 35이므로 여학생이 가장 많이 배우고 싶어 하는 운동은 스쿼시입니다.",
        }
    ],
    "answer": ANSWER,
    "diagnostics": {
        "skills": ["data.two_way_table_interpretation"],
        "errors": {
            "축구": "data.read_wrong_row_boys",
        },
    },
}
