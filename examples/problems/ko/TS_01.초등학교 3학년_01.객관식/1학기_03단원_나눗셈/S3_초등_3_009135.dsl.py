"""ModuMath Problem DSL: 나눗셈의 몫이 8인 식 선택하기 (S3_초등_3_009135)"""

from __future__ import annotations

from modu_math.dsl import (
    Canvas,
    ProblemTemplate,
    RectSlot,
    Region,
    TextBoxSlot,
    TextSlot,
)


PROBLEM_ID = "S3_초등_3_009135"
PROBLEM_TITLE = "나눗셈의 몫이 8인 식 선택하기"

ANSWER = {
    "type": "choice",
    "value": "24 ÷ 3 = 8",
    "unit": "",
    "answer_index": 1,
    "values": ["24 ÷ 3 = 8"],
    "blanks": [],
    "choices": [
        {
            "id": "slot.choice.option_0",
            "slot_id": "slot.choice.option_0",
            "text": "16 ÷ 8 = 2",
            "value": "16 ÷ 8 = 2",
        },
        {
            "id": "slot.choice.option_1",
            "slot_id": "slot.choice.option_1",
            "text": "24 ÷ 3 = 8",
            "value": "24 ÷ 3 = 8",
        },
    ],
    "answer_key": [
        {
            "slot_id": "slot.choice.option_1",
            "value": "24 ÷ 3 = 8",
        }
    ],
}

SEMANTIC_OVERRIDE = {
    "problem_id": PROBLEM_ID,
    "problem_type": "multiple_choice_division_quotient",
    "metadata": {
        "grade": 3,
        "semester": 1,
        "subject": "수학",
        "chapter": "03단원_나눗셈",
        "language": "ko-KR",
    },
    "domain": {
        "objects": [
            {
                "id": "expr.option_0",
                "type": "division_equation",
                "label": "16 ÷ 8 = 2",
                "dividend": 16,
                "divisor": 8,
                "quotient": 2,
            },
            {
                "id": "expr.option_1",
                "type": "division_equation",
                "label": "24 ÷ 3 = 8",
                "dividend": 24,
                "divisor": 3,
                "quotient": 8,
            },
        ],
        "relations": [
            {
                "id": "relation.target_quotient",
                "type": "has_quotient",
                "from_id": "expr.option_1",
                "to_id": "value.8",
            }
        ],
    },
    "answer": ANSWER,
}


def build_problem_template() -> ProblemTemplate:
    stem_slot = TextBoxSlot(
        id="slot.stem.question",
        prompt="",
        text="90. 나눗셈의 몫이 8인 것을 선택하세요.",
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
        x=250,
        y=82,
        width=240,
        height=64,
        fill="#fff1f0",
        stroke="#f8b4a6",
        stroke_width=1.5,
        interaction={
            "type": "choice",
            "role": "answer",
            "choice_index": 0,
            "value": "16 ÷ 8 = 2",
            "group_id": "slot.choice.group",
            "include_in_submission": True,
        },
    )
    text_0 = TextSlot(
        id="slot.choice.label_0",
        prompt="",
        text="16 ÷ 8 = 2",
        x=370,
        y=114,
        font_size=24,
        font_family='"Noto Sans KR", sans-serif',
        fill="#111827",
        align="center",
    )

    box_1 = RectSlot(
        id="slot.choice.option_1",
        prompt="",
        x=580,
        y=82,
        width=240,
        height=64,
        fill="#e0e7ff",
        stroke="#6366f1",
        stroke_width=1.5,
        interaction={
            "type": "choice",
            "role": "answer",
            "choice_index": 1,
            "value": "24 ÷ 3 = 8",
            "group_id": "slot.choice.group",
            "include_in_submission": True,
        },
    )
    text_1 = TextSlot(
        id="slot.choice.label_1",
        prompt="",
        text="24 ÷ 3 = 8",
        x=700,
        y=114,
        font_size=24,
        font_family='"Noto Sans KR", sans-serif',
        fill="#111827",
        align="center",
    )

    return ProblemTemplate(
        id=PROBLEM_ID,
        title=PROBLEM_TITLE,
        canvas=Canvas(width=886, height=180, coordinate_mode="logical"),
        regions=(
            Region(id="region.stem", role="stem", flow="absolute", slot_ids=("slot.stem.question",)),
            Region(
                id="region.choices",
                role="choices",
                flow="absolute",
                slot_ids=(
                    "slot.choice.option_0",
                    "slot.choice.label_0",
                    "slot.choice.option_1",
                    "slot.choice.label_1",
                ),
            ),
        ),
        slots=(stem_slot, box_0, text_0, box_1, text_1),
    )


PROBLEM_TEMPLATE = build_problem_template()

SOLVABLE = {
    "schema": "modu.solvable.v1.3",
    "problem_id": PROBLEM_ID,
    "given": [
        {"ref": "expr.option_0", "value": "16 ÷ 8 = 2"},
        {"ref": "expr.option_1", "value": "24 ÷ 3 = 8"},
    ],
    "target": {"ref": "slot.choice.option_1", "type": "choice"},
    "method": "division_quotient_identification",
    "steps": [
        {
            "id": "step.check_quotient",
            "expr": "24 / 3",
            "value": 8,
            "explanation": "나눗셈식에서 등호 오른쪽에 있는 수가 몫입니다. 16 ÷ 8 = 2의 몫은 2이고, 24 ÷ 3 = 8의 몫은 8입니다.",
        }
    ],
    "answer": ANSWER,
    "diagnostics": {
        "skills": ["division.quotient_meaning"],
        "errors": {
            "16 ÷ 8 = 2": "division.confused_divisor_with_quotient",
        },
    },
}
EDITOR_ANSWER_REVIEW = {'mode': 'canvas_select',
 'show_canvas': True,
 'status': 'pending',
 'note': '',
 'answers': [{'value': '24 ÷ 3 = 8', 'ref': 'slot.choice.option_1'}],
 'choices': [{'id': 'slot.choice.option_0',
              'text': '16 ÷ 8 = 2',
              'correct': False,
              'label': '1',
              'sourceRefs': ['slot.choice.option_0']},
             {'id': 'slot.choice.option_1',
              'text': '24 ÷ 3 = 8',
              'correct': True,
              'label': '2',
              'sourceRefs': ['slot.choice.option_1']}]}
