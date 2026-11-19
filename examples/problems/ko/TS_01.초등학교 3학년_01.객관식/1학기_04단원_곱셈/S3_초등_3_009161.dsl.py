"""ModuMath Problem DSL: 세로셈 올림 숫자 자릿값 구하기 (S3_초등_3_009161)"""

from __future__ import annotations

from modu_math.dsl import (
    Canvas,
    LineSlot,
    ProblemTemplate,
    RectSlot,
    Region,
    TextBoxSlot,
    TextSlot,
    columnar_number_slots,
)


PROBLEM_ID = "S3_초등_3_009161"
PROBLEM_TITLE = "곱셈 세로셈에서 올림한 숫자 2가 나타내는 수 구하기"

ANSWER = {
    "type": "choice",
    "value": "②",
    "unit": "",
    "answer_index": 1,
    "values": ["②"],
    "blanks": [],
    "choices": [
        {"id": "slot.choice.option_0", "slot_id": "slot.choice.option_0", "text": "①", "value": "①"},
        {"id": "slot.choice.option_1", "slot_id": "slot.choice.option_1", "text": "②", "value": "②"},
        {"id": "slot.choice.option_2", "slot_id": "slot.choice.option_2", "text": "③", "value": "③"},
        {"id": "slot.choice.option_3", "slot_id": "slot.choice.option_3", "text": "④", "value": "④"},
        {"id": "slot.choice.option_4", "slot_id": "slot.choice.option_4", "text": "⑤", "value": "⑤"},
    ],
    "answer_key": [
        {
            "slot_id": "slot.choice.option_1",
            "value": "②",
        }
    ],
}

SEMANTIC_OVERRIDE = {
    "problem_id": PROBLEM_ID,
    "problem_type": "multiple_choice_multiplication_place_value",
    "metadata": {
        "grade": 3,
        "semester": 1,
        "subject": "수학",
        "chapter": "04단원_곱셈",
        "language": "ko-KR",
    },
    "domain": {
        "objects": [
            {"id": "expr.vertical", "type": "vertical_multiplication", "multiplicand": 18, "multiplier": 3, "product": 54},
            {"id": "digit.carry_2", "type": "carry_digit", "digit": 2, "place": "tens", "actual_value": 20},
        ],
        "relations": [
            {
                "id": "relation.place_value",
                "type": "represents_value",
                "from_id": "digit.carry_2",
                "to_id": "value.20",
            }
        ],
    },
    "answer": ANSWER,
}


def build_problem_template() -> ProblemTemplate:
    stem_slot = TextBoxSlot(
        id="slot.stem.question",
        prompt="",
        text="22. 계산에서 □ 안의 숫자 2가 실제로 나타내는 수는 얼마일까요?",
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

    frame_box = RectSlot(
        id="slot.diagram.frame",
        prompt="",
        x=355,
        y=72,
        width=175,
        height=178,
        fill="#ffffff",
        stroke="#65a30d",
        stroke_width=1.5,
    )
    carry_box = RectSlot(
        id="slot.diagram.carry_box",
        prompt="",
        x=434,
        y=84,
        width=28,
        height=28,
        fill="#ffffff",
        stroke="#111827",
        stroke_width=1.2,
    )
    carry_digit = TextSlot(
        id="slot.diagram.carry_digit",
        prompt="",
        text="2",
        x=448,
        y=98,
        font_size=20,
        font_family='"Noto Sans KR", sans-serif',
        fill="#db2777",
        align="center",
    )

    top_digits = columnar_number_slots(id_prefix="slot.diagram.top", value="18", right_x=495, y=132, column_width=32, font_size=24)
    mul_sign = TextSlot(id="slot.diagram.mul_sign", prompt="", text="×", x=402, y=166, font_size=22, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="center")
    bot_digits = columnar_number_slots(id_prefix="slot.diagram.bot", value="3", right_x=495, y=166, column_width=32, font_size=24)
    sep_line = LineSlot(id="slot.diagram.sep_line", prompt="", x1=390, y1=186, x2=500, y2=186, stroke="#111827", stroke_width=1.5)
    res_digits = columnar_number_slots(id_prefix="slot.diagram.res", value="54", right_x=495, y=214, column_width=32, font_size=24)

    opt_0 = TextSlot(id="slot.choice.option_0", prompt="", text="① 2", x=32, y=282, font_size=22, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="left", interaction={"type": "choice", "role": "answer", "choice_index": 0, "value": "①", "group_id": "slot.choice.group", "include_in_submission": True})
    opt_1 = TextSlot(id="slot.choice.option_1", prompt="", text="② 20", x=310, y=282, font_size=22, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="left", interaction={"type": "choice", "role": "answer", "choice_index": 1, "value": "②", "group_id": "slot.choice.group", "include_in_submission": True})
    opt_2 = TextSlot(id="slot.choice.option_2", prompt="", text="③ 22", x=590, y=282, font_size=22, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="left", interaction={"type": "choice", "role": "answer", "choice_index": 2, "value": "③", "group_id": "slot.choice.group", "include_in_submission": True})
    opt_3 = TextSlot(id="slot.choice.option_3", prompt="", text="④ 24", x=32, y=322, font_size=22, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="left", interaction={"type": "choice", "role": "answer", "choice_index": 3, "value": "④", "group_id": "slot.choice.group", "include_in_submission": True})
    opt_4 = TextSlot(id="slot.choice.option_4", prompt="", text="⑤ 200", x=310, y=322, font_size=22, font_family='"Noto Sans KR", sans-serif', fill="#111827", align="left", interaction={"type": "choice", "role": "answer", "choice_index": 4, "value": "⑤", "group_id": "slot.choice.group", "include_in_submission": True})

    diagram_slots = (
        frame_box,
        carry_box,
        carry_digit,
        *top_digits,
        mul_sign,
        *bot_digits,
        sep_line,
        *res_digits,
    )

    return ProblemTemplate(
        id=PROBLEM_ID,
        title=PROBLEM_TITLE,
        canvas=Canvas(width=886, height=360, coordinate_mode="logical"),
        regions=(
            Region(id="region.stem", role="stem", flow="absolute", slot_ids=("slot.stem.question",)),
            Region(id="region.diagram", role="diagram", flow="absolute", slot_ids=tuple(s.id for s in diagram_slots)),
            Region(id="region.choices", role="choices", flow="absolute", slot_ids=("slot.choice.option_0", "slot.choice.option_1", "slot.choice.option_2", "slot.choice.option_3", "slot.choice.option_4")),
        ),
        slots=(stem_slot, *diagram_slots, opt_0, opt_1, opt_2, opt_3, opt_4),
    )


PROBLEM_TEMPLATE = build_problem_template()

SOLVABLE = {
    "schema": "modu.solvable.v1.3",
    "problem_id": PROBLEM_ID,
    "given": [
        {"ref": "expr.vertical", "value": "18 × 3 = 54"},
        {"ref": "digit.carry_2", "value": 2},
    ],
    "target": {"ref": "slot.choice.option_1", "type": "choice"},
    "method": "place_value_of_carry",
    "steps": [
        {"id": "step.ones_mul", "expr": "8 * 3", "value": 24, "explanation": "일의 자리 계산 8 × 3 = 24에서 2를 십의 자리로 올림한 것입니다."},
        {"id": "step.place_value", "expr": "2 * 10", "value": 20, "explanation": "십의 자리에 올림한 2가 실제로 나타내는 수는 20(②)입니다."},
    ],
    "answer": ANSWER,
    "diagnostics": {
        "skills": ["multiplication.carry_place_value"],
        "errors": {
            "①": "place_value.ignored_tens_place",
            "⑤": "place_value.confused_tens_with_hundreds",
        },
    },
}
