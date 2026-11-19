"""ModuMath Problem DSL: 표의 빈칸을 구해 순서대로 나열한 것 판별하기 (S3_초등_3_008885)"""

from __future__ import annotations

from modu_math.dsl import (
    Canvas,
    ProblemTemplate,
    Region,
    TextBoxSlot,
    TextSlot,
    table_slots,
)


PROBLEM_ID = "S3_초등_3_008885"
PROBLEM_TITLE = "표를 보고 좋아하는 학생이 많은 민속놀이 순서 판별하기"

ANSWER = {
    "type": "choice",
    "value": "○",
    "unit": "",
    "answer_index": 0,
    "values": ["○"],
    "blanks": [],
    "choices": [
        {"id": "slot.choice.option_0", "slot_id": "slot.choice.option_0", "text": "○", "value": "○"},
        {"id": "slot.choice.option_1", "slot_id": "slot.choice.option_1", "text": "×", "value": "×"},
    ],
    "answer_key": [{"slot_id": "slot.choice.option_0", "value": "○"}],
}

SEMANTIC_OVERRIDE = {
    "problem_id": PROBLEM_ID,
    "problem_type": "multiple_choice_table_ordering_ox",
    "metadata": {
        "grade": 3,
        "semester": 2,
        "subject": "수학",
        "chapter": "06단원_자료의 정리",
        "language": "ko-KR",
    },
    "domain": {
        "objects": [
            {"id": "cat.ssireum", "type": "survey_item", "label": "씨름", "count": 9},
            {"id": "cat.kite", "type": "survey_item", "label": "연날리기", "count": 7},
            {"id": "cat.yut", "type": "survey_item", "label": "윷놀이", "count": 6},
            {"id": "cat.neol", "type": "survey_item", "label": "널뛰기", "count": 8},
            {"id": "cat.total", "type": "survey_total", "count": 30},
        ],
        "relations": [
            {
                "id": "relation.descending_order",
                "type": "is_valid_descending_order",
                "from_id": "cat.ssireum",
                "to_id": "cat.yut",
            }
        ],
    },
    "answer": ANSWER,
}


def build_problem_template() -> ProblemTemplate:
    context_slot = TextBoxSlot(
        id="slot.stem.context",
        prompt="",
        text="영채네 반 학생들이 좋아하는 민속놀이를 조사하여 표로 나타내었습니다. 물음에 답하세요.",
        x=32,
        y=16,
        width=820,
        height=54,
        font_size=20,
        font_family='"Noto Sans KR", sans-serif',
        fill="#202124",
        align="left",
        valign="top",
        line_height=1.4,
    )

    table_title = TextSlot(id="slot.diagram.table_title", prompt="", text="학생들이 좋아하는 민속놀이", x=443, y=82, font_size=20, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center")
    tbl = table_slots(
        "slot.diagram.table",
        x=118,
        y=102,
        col_widths=(170, 96, 96, 96, 96, 96),
        row_heights=(40, 40),
        cells=(
            ("민속놀이", "씨름", "연날리기", "윷놀이", "널뛰기", "합계"),
            ("학생 수(명)", "", "7", "6", "8", "30"),
        ),
        font_size=19,
        stroke="#a8a29e",
    )

    stem_slot = TextBoxSlot(
        id="slot.stem.question",
        prompt="",
        text="49. 좋아하는 학생이 가장 많은 민속놀이부터 순서대로 써보았습니다. 바르게 썼으면 ○표, 그렇지 않으면 ×표를 선택하세요.",
        x=32,
        y=200,
        width=820,
        height=60,
        font_size=21,
        font_family='"Noto Sans KR", sans-serif',
        fill="#202124",
        align="left",
        valign="top",
        line_height=1.5,
    )

    order_text = TextSlot(id="slot.diagram.order_text", prompt="", text="씨름, 널뛰기, 연날리기, 윷놀이 (", x=410, y=282, font_size=22, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center")
    opt_0 = TextSlot(id="slot.choice.option_0", prompt="", text="○", x=595, y=282, font_size=24, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center", interaction={"type": "choice", "role": "answer", "choice_index": 0, "value": "○", "group_id": "slot.choice.group", "include_in_submission": True})
    comma_1 = TextSlot(id="slot.choice.comma_1", prompt="", text=",", x=628, y=282, font_size=22, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center")
    opt_1 = TextSlot(id="slot.choice.option_1", prompt="", text="×", x=660, y=282, font_size=24, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center", interaction={"type": "choice", "role": "answer", "choice_index": 1, "value": "×", "group_id": "slot.choice.group", "include_in_submission": True})
    paren_r = TextSlot(id="slot.choice.paren_r", prompt="", text=")", x=690, y=282, font_size=22, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center")

    diagram_slots = (table_title, *tbl, order_text)

    return ProblemTemplate(
        id=PROBLEM_ID,
        title=PROBLEM_TITLE,
        canvas=Canvas(width=886, height=320, coordinate_mode="logical"),
        regions=(
            Region(id="region.stem", role="stem", flow="absolute", slot_ids=("slot.stem.context", "slot.stem.question")),
            Region(id="region.diagram", role="diagram", flow="absolute", slot_ids=tuple(s.id for s in diagram_slots)),
            Region(id="region.choices", role="choices", flow="absolute", slot_ids=("slot.choice.option_0", "slot.choice.comma_1", "slot.choice.option_1", "slot.choice.paren_r")),
        ),
        slots=(context_slot, *diagram_slots, stem_slot, opt_0, comma_1, opt_1, paren_r),
    )


PROBLEM_TEMPLATE = build_problem_template()

SOLVABLE = {
    "schema": "modu.solvable.v1.3",
    "problem_id": PROBLEM_ID,
    "given": [
        {"ref": "cat.kite", "value": 7},
        {"ref": "cat.yut", "value": 6},
        {"ref": "cat.neol", "value": 8},
        {"ref": "cat.total", "value": 30},
    ],
    "target": {"ref": "slot.choice.option_0", "type": "choice"},
    "method": "complete_table_and_verify_order",
    "steps": [
        {"id": "step.find_missing", "expr": "30 - (7 + 6 + 8)", "value": 9, "explanation": "합계가 30명이므로 씨름을 좋아하는 학생 수는 30 - 21 = 9명입니다."},
        {"id": "step.verify_order", "expr": "9 > 8 > 7 > 6", "value": "○", "explanation": "9 > 8 > 7 > 6이므로 씨름, 널뛰기, 연날리기, 윷놀이 순서는 바릅니다."},
    ],
    "answer": ANSWER,
    "diagnostics": {
        "skills": ["data.table_missing_value", "data.ordering"],
        "errors": {
            "×": "data.forgot_to_compute_missing_cell",
        },
    },
}
