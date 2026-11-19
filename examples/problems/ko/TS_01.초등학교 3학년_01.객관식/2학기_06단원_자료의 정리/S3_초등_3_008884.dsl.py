"""ModuMath Problem DSL: 표를 보고 가장 적은 색종이 색깔 선택하기 (S3_초등_3_008884)"""

from __future__ import annotations

from modu_math.dsl import (
    Canvas,
    ProblemTemplate,
    Region,
    TextBoxSlot,
    TextSlot,
    table_slots,
)


PROBLEM_ID = "S3_초등_3_008884"
PROBLEM_TITLE = "표를 보고 가장 적은 색종이 색깔 선택하기"

ANSWER = {
    "type": "choice",
    "value": "보라색",
    "unit": "",
    "answer_index": 3,
    "values": ["보라색"],
    "blanks": [],
    "choices": [
        {"id": "slot.choice.option_0", "slot_id": "slot.choice.option_0", "text": "빨간색", "value": "빨간색"},
        {"id": "slot.choice.option_1", "slot_id": "slot.choice.option_1", "text": "노란색", "value": "노란색"},
        {"id": "slot.choice.option_2", "slot_id": "slot.choice.option_2", "text": "초록색", "value": "초록색"},
        {"id": "slot.choice.option_3", "slot_id": "slot.choice.option_3", "text": "보라색", "value": "보라색"},
    ],
    "answer_key": [{"slot_id": "slot.choice.option_3", "value": "보라색"}],
}

SEMANTIC_OVERRIDE = {
    "problem_id": PROBLEM_ID,
    "problem_type": "multiple_choice_table_min",
    "metadata": {
        "grade": 3,
        "semester": 2,
        "subject": "수학",
        "chapter": "06단원_자료의 정리",
        "language": "ko-KR",
    },
    "domain": {
        "objects": [
            {"id": "cat.red", "type": "survey_item", "label": "빨간색", "count": 24},
            {"id": "cat.yellow", "type": "survey_item", "label": "노란색", "count": 30},
            {"id": "cat.green", "type": "survey_item", "label": "초록색", "count": 16},
            {"id": "cat.purple", "type": "survey_item", "label": "보라색", "count": 14},
        ],
        "relations": [
            {
                "id": "relation.minimum",
                "type": "has_min_count",
                "from_id": "cat.purple",
                "to_id": "value.14",
            }
        ],
    },
    "answer": ANSWER,
}


def build_problem_template() -> ProblemTemplate:
    stem_slot = TextBoxSlot(
        id="slot.stem.question",
        prompt="",
        text="48. 서영이는 교실에 색종이가 색깔별로 몇 장 있는지 조사하였습니다. 표를 보고 알맞은 말을 선택해 보세요.",
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

    table_title = TextSlot(id="slot.diagram.table_title", prompt="", text="색깔별 색종이 수", x=120, y=98, font_size=20, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center")
    tbl = table_slots(
        "slot.diagram.table",
        x=42,
        y=118,
        col_widths=(175, 115, 115, 115, 115, 115),
        row_heights=(42, 42),
        cells=(
            ("색깔", "빨간색", "노란색", "초록색", "보라색", "합계"),
            ("색종이 수(장)", "24", "30", "16", "14", "84"),
        ),
        font_size=20,
        stroke="#f59e0b",
    )

    sent_left = TextSlot(id="slot.diagram.sent_left", prompt="", text="가장 적은 색종이는 (", x=142, y=246, font_size=22, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center")
    opt_0 = TextSlot(id="slot.choice.option_0", prompt="", text="빨간색", x=280, y=246, font_size=22, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center", interaction={"type": "choice", "role": "answer", "choice_index": 0, "value": "빨간색", "group_id": "slot.choice.group", "include_in_submission": True})
    comma_1 = TextSlot(id="slot.choice.comma_1", prompt="", text=",", x=326, y=246, font_size=22, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center")
    opt_1 = TextSlot(id="slot.choice.option_1", prompt="", text="노란색", x=372, y=246, font_size=22, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center", interaction={"type": "choice", "role": "answer", "choice_index": 1, "value": "노란색", "group_id": "slot.choice.group", "include_in_submission": True})
    comma_2 = TextSlot(id="slot.choice.comma_2", prompt="", text=",", x=418, y=246, font_size=22, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center")
    opt_2 = TextSlot(id="slot.choice.option_2", prompt="", text="초록색", x=464, y=246, font_size=22, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center", interaction={"type": "choice", "role": "answer", "choice_index": 2, "value": "초록색", "group_id": "slot.choice.group", "include_in_submission": True})
    comma_3 = TextSlot(id="slot.choice.comma_3", prompt="", text=",", x=510, y=246, font_size=22, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center")
    opt_3 = TextSlot(id="slot.choice.option_3", prompt="", text="보라색", x=556, y=246, font_size=22, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center", interaction={"type": "choice", "role": "answer", "choice_index": 3, "value": "보라색", "group_id": "slot.choice.group", "include_in_submission": True})
    sent_right = TextSlot(id="slot.diagram.sent_right", prompt="", text=") 색종이입니다.", x=692, y=246, font_size=22, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center")

    diagram_slots = (table_title, *tbl, sent_left, sent_right)

    return ProblemTemplate(
        id=PROBLEM_ID,
        title=PROBLEM_TITLE,
        canvas=Canvas(width=886, height=285, coordinate_mode="logical"),
        regions=(
            Region(id="region.stem", role="stem", flow="absolute", slot_ids=("slot.stem.question",)),
            Region(id="region.diagram", role="diagram", flow="absolute", slot_ids=tuple(s.id for s in diagram_slots)),
            Region(
                id="region.choices",
                role="choices",
                flow="absolute",
                slot_ids=("slot.choice.option_0", "slot.choice.comma_1", "slot.choice.option_1", "slot.choice.comma_2", "slot.choice.option_2", "slot.choice.comma_3", "slot.choice.option_3"),
            ),
        ),
        slots=(stem_slot, *diagram_slots, opt_0, comma_1, opt_1, comma_2, opt_2, comma_3, opt_3),
    )


PROBLEM_TEMPLATE = build_problem_template()

SOLVABLE = {
    "schema": "modu.solvable.v1.3",
    "problem_id": PROBLEM_ID,
    "given": [
        {"ref": "cat.red", "value": 24},
        {"ref": "cat.yellow", "value": 30},
        {"ref": "cat.green", "value": 16},
        {"ref": "cat.purple", "value": 14},
    ],
    "target": {"ref": "slot.choice.option_3", "type": "choice"},
    "method": "find_minimum_in_table",
    "steps": [
        {
            "id": "step.find_min",
            "expr": "min(24, 30, 16, 14)",
            "value": "보라색",
            "explanation": "색종이 수에서 가장 작은 수는 14이므로 가장 적은 색종이는 보라색 색종이입니다.",
        }
    ],
    "answer": ANSWER,
    "diagnostics": {
        "skills": ["data.table_interpretation_min"],
        "errors": {
            "노란색": "data.chose_max_instead_of_min",
        },
    },
}
