"""ModuMath Problem DSL: 나눗셈의 몫을 구하는 데 필요한 곱셈식 찾기 (S3_초등_3_009136)"""

from __future__ import annotations

from modu_math.dsl import (
    Canvas,
    ProblemTemplate,
    RectSlot,
    Region,
    TextBoxSlot,
    TextSlot,
)


PROBLEM_ID = "S3_초등_3_009136"
PROBLEM_TITLE = "18 ÷ 3의 몫을 구하는 데 필요한 곱셈식 선택하기"

ANSWER = {
    "type": "choice",
    "value": "㉢",
    "unit": "",
    "answer_index": 2,
    "values": ["㉢"],
    "blanks": [],
    "choices": [
        {"id": "slot.choice.option_0", "slot_id": "slot.choice.option_0", "text": "㉠", "value": "㉠"},
        {"id": "slot.choice.option_1", "slot_id": "slot.choice.option_1", "text": "㉡", "value": "㉡"},
        {"id": "slot.choice.option_2", "slot_id": "slot.choice.option_2", "text": "㉢", "value": "㉢"},
    ],
    "answer_key": [
        {
            "slot_id": "slot.choice.option_2",
            "value": "㉢",
        }
    ],
}

SEMANTIC_OVERRIDE = {
    "problem_id": PROBLEM_ID,
    "problem_type": "multiple_choice_division_via_multiplication",
    "metadata": {
        "grade": 3,
        "semester": 1,
        "subject": "수학",
        "chapter": "03단원_나눗셈",
        "language": "ko-KR",
    },
    "domain": {
        "objects": [
            {"id": "expr.division", "type": "division", "dividend": 18, "divisor": 3},
            {"id": "expr.ga", "type": "multiplication", "label": "㉠", "equation": "3 × 4 = 12"},
            {"id": "expr.na", "type": "multiplication", "label": "㉡", "equation": "3 × 5 = 15"},
            {"id": "expr.da", "type": "multiplication", "label": "㉢", "equation": "3 × 6 = 18"},
        ],
        "relations": [
            {
                "id": "relation.inverse_multiplication",
                "type": "solves_division",
                "from_id": "expr.da",
                "to_id": "expr.division",
            }
        ],
    },
    "answer": ANSWER,
}


def build_problem_template() -> ProblemTemplate:
    stem_slot = TextBoxSlot(
        id="slot.stem.question",
        prompt="",
        text="91. 18 ÷ 3의 몫을 구하려고 합니다. 필요한 곱셈식을 찾아 기호를 선택하세요.",
        x=32,
        y=20,
        width=820,
        height=64,
        font_size=22,
        font_family='"Noto Sans KR", sans-serif',
        fill="#202124",
        align="left",
        valign="top",
        line_height=1.5,
    )

    box_bg = RectSlot(
        id="slot.diagram.box",
        prompt="",
        x=95,
        y=95,
        width=730,
        height=62,
        fill="#fbcfe8",
        stroke="none",
        stroke_width=0,
    )
    item_ga = TextSlot(
        id="slot.diagram.item_ga",
        prompt="",
        text="㉠ 3 × 4 = 12",
        x=250,
        y=126,
        font_size=22,
        font_family='"Noto Sans KR", sans-serif',
        fill="#111827",
        align="center",
    )
    item_na = TextSlot(
        id="slot.diagram.item_na",
        prompt="",
        text="㉡ 3 × 5 = 15",
        x=455,
        y=126,
        font_size=22,
        font_family='"Noto Sans KR", sans-serif',
        fill="#111827",
        align="center",
    )
    item_da = TextSlot(
        id="slot.diagram.item_da",
        prompt="",
        text="㉢ 3 × 6 = 18",
        x=660,
        y=126,
        font_size=22,
        font_family='"Noto Sans KR", sans-serif',
        fill="#111827",
        align="center",
    )

    paren_l = TextSlot(id="slot.choice.paren_l", prompt="", text="(", x=370, y=188, font_size=24, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center")
    opt_0 = TextSlot(
        id="slot.choice.option_0",
        prompt="",
        text="㉠",
        x=405,
        y=188,
        font_size=22,
        font_family='"Noto Sans KR", sans-serif',
        fill="#111827",
        align="center",
        interaction={"type": "choice", "role": "answer", "choice_index": 0, "value": "㉠", "group_id": "slot.choice.group", "include_in_submission": True},
    )
    comma_1 = TextSlot(id="slot.choice.comma_1", prompt="", text=",", x=435, y=188, font_size=22, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center")
    opt_1 = TextSlot(
        id="slot.choice.option_1",
        prompt="",
        text="㉡",
        x=465,
        y=188,
        font_size=22,
        font_family='"Noto Sans KR", sans-serif',
        fill="#111827",
        align="center",
        interaction={"type": "choice", "role": "answer", "choice_index": 1, "value": "㉡", "group_id": "slot.choice.group", "include_in_submission": True},
    )
    comma_2 = TextSlot(id="slot.choice.comma_2", prompt="", text=",", x=495, y=188, font_size=22, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center")
    opt_2 = TextSlot(
        id="slot.choice.option_2",
        prompt="",
        text="㉢",
        x=525,
        y=188,
        font_size=22,
        font_family='"Noto Sans KR", sans-serif',
        fill="#111827",
        align="center",
        interaction={"type": "choice", "role": "answer", "choice_index": 2, "value": "㉢", "group_id": "slot.choice.group", "include_in_submission": True},
    )
    paren_r = TextSlot(id="slot.choice.paren_r", prompt="", text=")", x=560, y=188, font_size=24, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center")

    return ProblemTemplate(
        id=PROBLEM_ID,
        title=PROBLEM_TITLE,
        canvas=Canvas(width=886, height=230, coordinate_mode="logical"),
        regions=(
            Region(id="region.stem", role="stem", flow="absolute", slot_ids=("slot.stem.question",)),
            Region(
                id="region.diagram",
                role="diagram",
                flow="absolute",
                slot_ids=("slot.diagram.box", "slot.diagram.item_ga", "slot.diagram.item_na", "slot.diagram.item_da"),
            ),
            Region(
                id="region.choices",
                role="choices",
                flow="absolute",
                slot_ids=(
                    "slot.choice.paren_l",
                    "slot.choice.option_0",
                    "slot.choice.comma_1",
                    "slot.choice.option_1",
                    "slot.choice.comma_2",
                    "slot.choice.option_2",
                    "slot.choice.paren_r",
                ),
            ),
        ),
        slots=(stem_slot, box_bg, item_ga, item_na, item_da, paren_l, opt_0, comma_1, opt_1, comma_2, opt_2, paren_r),
    )


PROBLEM_TEMPLATE = build_problem_template()

SOLVABLE = {
    "schema": "modu.solvable.v1.3",
    "problem_id": PROBLEM_ID,
    "given": [
        {"ref": "expr.division", "value": "18 ÷ 3"},
        {"ref": "expr.ga", "value": "3 × 4 = 12"},
        {"ref": "expr.na", "value": "3 × 5 = 15"},
        {"ref": "expr.da", "value": "3 × 6 = 18"},
    ],
    "target": {"ref": "slot.choice.option_2", "type": "choice"},
    "method": "division_via_multiplication_table",
    "steps": [
        {
            "id": "step.find_multiplication",
            "expr": "3 * 6 = 18",
            "value": "㉢",
            "explanation": "나누는 수가 3이므로 3의 단 곱셈구구에서 곱이 18인 식 3 × 6 = 18(㉢)을 이용하면 18 ÷ 3 = 6임을 알 수 있습니다.",
        }
    ],
    "answer": ANSWER,
    "diagnostics": {
        "skills": ["division.multiplication_relation"],
        "errors": {
            "㉠": "multiplication.wrong_product",
            "㉡": "multiplication.wrong_product",
        },
    },
}
EDITOR_ANSWER_REVIEW = {'mode': 'canvas_select',
 'show_canvas': True,
 'status': 'pending',
 'note': '',
 'answers': [{'value': '㉢', 'ref': 'slot.choice.option_2'}],
 'choices': [{'id': 'choice.canvas.konva_1795337996416_select_246331',
              'text': '㉠ 3 × 4 = 12',
              'correct': False,
              'label': '1',
              'sourceRefs': ['slot.diagram.item_ga']},
             {'id': 'choice.canvas.konva_1795337996416_select_247842',
              'text': '㉡ 3 × 5 = 15',
              'correct': False,
              'label': '2',
              'sourceRefs': ['slot.diagram.item_na']},
             {'id': 'choice.canvas.konva_1795337996416_select_249162',
              'text': '㉢ 3 × 6 = 18',
              'correct': True,
              'label': '3',
              'sourceRefs': ['slot.diagram.item_da']}]}
