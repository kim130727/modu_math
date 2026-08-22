from __future__ import annotations
from modu_math.dsl import Canvas, ProblemTemplate, Region, RectSlot, TextSlot


def build_problem_template() -> ProblemTemplate:
    return ProblemTemplate(
        id="S3_초등_3_008633",
        title="카드를 한 번씩만 사용하여 가장 큰 세 자리 수를 만들고 나머지 구하기",
        canvas=Canvas(width=944, height=352, coordinate_mode="logical"),
        regions=(
            Region(
                id="region.stem",
                role="stem",
                flow="absolute",
                slot_ids=("slot.qtext1", "slot.qtext2", ),
            ),
            Region(
                id="region.cards",
                role="diagram",
                flow="absolute",
                slot_ids=(
                    "slot.card.6",
                    "slot.card.6.text",
                    "slot.card.8",
                    "slot.card.8.text",
                    "slot.card.9",
                    "slot.card.9.text",
                    "slot.card.7",
                    "slot.card.7.text",
                ),
            ),
            Region(
                id="region.options",
                role="choices",
                flow="absolute",
                slot_ids=(
                    "slot.opt1",
                    "slot.opt2",
                    "slot.opt3",
                    "slot.opt4",
                    "slot.opt5",
                ),
            ),
            Region(
                id="region.bottom",
                role="explanation",
                flow="absolute",
                slot_ids=( ),
            ),
        ),
        slots=(TextSlot(
                id="slot.qtext1",
                prompt="",
                text = '수를 카드를 한 번씩만 사용하여 만들 수 있는 가장 큰 세 자리 수를 남은', style_role="question",
                x = 25, y = 35, font_size = 30),
            TextSlot(
                id="slot.qtext2",
                prompt="",
                text = '카드의 수로 나누면 나머지는 얼마일까요?', style_role="question",
                x = 25, y = 85, font_size = 30),
            RectSlot(
                id="slot.card.6", prompt="", x = 320, y = 120, width = 40, height = 50),
            TextSlot(
                id="slot.card.6.text",
                prompt="",
                text = '6', style_role="label",
                x = 333, y = 155, font_size = 30),
            RectSlot(
                id="slot.card.8", prompt="", x = 390, y = 120, width = 40, height = 50),
            TextSlot(
                id="slot.card.8.text",
                prompt="",
                text = '8', style_role="label",
                x = 403, y = 155, font_size = 30),
            RectSlot(
                id="slot.card.9", prompt="", x = 460, y = 120, width = 40, height = 50),
            TextSlot(
                id="slot.card.9.text",
                prompt="",
                text = '9', style_role="label",
                x = 474, y = 155, font_size = 30),
            RectSlot(
                id="slot.card.7", prompt="", x = 530, y = 120, width = 40, height = 50),
            TextSlot(
                id="slot.card.7.text",
                prompt="",
                text = '7', style_role="label",
                x = 543, y = 155, font_size = 30),
            TextSlot(
                id="slot.opt1",
                prompt="",
                text = '① 1', style_role="choice",
                x = 30, y = 240, font_size = 30),
            TextSlot(
                id="slot.opt2",
                prompt="",
                text = '② 2', style_role="choice",
                x = 335, y = 240, font_size = 30),
            TextSlot(
                id="slot.opt3",
                prompt="",
                text = '③ 3', style_role="choice",
                x = 640, y = 240, font_size = 30),
            TextSlot(
                id="slot.opt4",
                prompt="",
                text = '④ 4', style_role="choice",
                x = 30, y = 275, font_size = 30),
            TextSlot(
                id="slot.opt5",
                prompt="",
                text = '⑤ 5', style_role="choice",
                x = 335, y = 275, font_size = 30),),
        diagrams=(),
        groups=(),
        constraints=(),
        tags=(),
    )


PROBLEM_TEMPLATE = build_problem_template()

SEMANTIC_OVERRIDE = {
    "problem_id": "S3_초등_3_008633",
    "problem_type": "나눗셈_나머지",
    "metadata": {
        "language": "ko",
        "question": "카드의 숫자를 이용해 가장 큰 세 자리 수를 만들고 남은 카드의 수로 나눌 때의 나머지를 묻는 문제",
        "instruction": "보이는 카드와 해설 문장을 기준으로 의미를 정리한다.",
    },
    "domain": {
        "objects": [
            {"id": "obj.cards", "type": "digit_cards", "digits": [6, 8, 9, 7]},
            {"id": "obj.dividend", "type": "number", "value": 987},
            {"id": "obj.divisor", "type": "number", "value": 6},
        ],
        "relations": [],
        "problem_solving": {
            "understand": {
                "given_refs": ["obj.cards", "obj.dividend", "obj.divisor"],
                "target_ref": "answer.target",
                "condition_refs": [
                    "rel.make_largest_number",
                    "rel.divide_by_remaining_digit",
                ],
            },
            "plan": {
                "method": "largest_number_then_division",
                "description": "카드로 만들 수 있는 가장 큰 세 자리 수와 남은 숫자를 확인한 뒤 나머지를 읽는다.",
            },
            "execute": {
                "expected_operations": [
                    "identify_largest_three_digit_number",
                    "identify_remaining_digit",
                    "read_remainder_from_division_result",
                ]
            },
            "review": {
                "check_methods": [
                    "division_result_consistency",
                    "remainder_range_check",
                ]
            },
        },
    },
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {"type": "remainder", "description": "나머지"},
        "value": 3,
        "unit": "",
    },
}

SOLVABLE = {
    "schema": "modu.solvable.v1.1",
    "problem_id": "S3_초등_3_008633",
    "problem_type": "나눗셈_나머지",
    "inputs": {
        "total_ticks": 4,
        "target_label": "나머지",
        "target_ticks": 1,
        "target_count": 1,
        "unit": "",
    },
    "given": [
        {"ref": "obj.cards", "value": {"digits": [6, 8, 9, 7]}},
        {"ref": "obj.dividend", "value": 987},
        {"ref": "obj.divisor", "value": 6},
    ],
    "target": {"ref": "answer.target", "type": "remainder"},
    "method": "largest_number_then_division",
    "plan": [
        "카드로 만들 수 있는 가장 큰 세 자리 수와 남은 숫자를 확인한다.",
        "나눗셈 결과의 나머지를 읽는다.",
    ],
    "steps": [
        {
            "id": "step.1",
            "expr": "카드 6, 8, 9, 7 중 가장 큰 세 자리 수 확인",
            "value": 987,
        },
        {"id": "step.2", "expr": "987 ÷ 6", "value": {"quotient": 164, "remainder": 3}},
        {"id": "step.3", "expr": "나머지", "value": 3},
    ],
    "checks": [
        {
            "id": "check.1",
            "expr": "6 × 164 + 3 = 987",
            "expected": 987,
            "actual": 987,
            "pass": True,
        },
        {
            "id": "check.2",
            "expr": "0 ≤ 3 < 6",
            "expected": True,
            "actual": True,
            "pass": True,
        },
    ],
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {"type": "remainder", "description": "나머지"},
        "value": 3,
        "unit": "",
    },
}
