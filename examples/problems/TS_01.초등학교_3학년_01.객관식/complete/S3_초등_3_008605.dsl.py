from __future__ import annotations
from modu_math.dsl import Canvas, ProblemTemplate, Region, TextSlot


def build_problem_template() -> ProblemTemplate:
    return ProblemTemplate(
        id="S3_초등_3_008605",
        title="3으로 나누어떨어지는 수가 아닌 것",
        canvas=Canvas(width=855, height=420, coordinate_mode="logical"),
        regions=(
            Region(
                id="region.stem",
                role="stem",
                flow="absolute",
                slot_ids=(
                    "slot.title",
                    "slot.opt1",
                    "slot.opt2",
                    "slot.opt3",
                    "slot.opt4",
                    "slot.opt5",
                ),
            ),
            Region(id="region.answer", role="answer", flow="absolute", slot_ids=()),
            Region(
                id="region.explanation",
                role="explanation",
                flow="absolute",
                slot_ids=(),
            ),
        ),
        slots=(
            TextSlot(
                id="slot.title",
                prompt="",
                text = '3으로 나누어떨어지는 수가 아닌 것을 모두 고르세요.', style_role="question",
                x = 10, y = 40, font_size = 30),
            TextSlot(
                id="slot.opt1",
                prompt="",
                text = '① 27', style_role="question",
                x = 10, y = 95, font_size = 30),
            TextSlot(
                id="slot.opt2",
                prompt="",
                text = '② 56', style_role="question",
                x = 190, y = 95, font_size = 30),
            TextSlot(
                id="slot.opt3",
                prompt="",
                text = '③ 84', style_role="question",
                x = 370, y = 95, font_size = 30),
            TextSlot(
                id="slot.opt4",
                prompt="",
                text = '④ 63', style_role="question",
                x = 530, y = 95, font_size = 30),
            TextSlot(
                id="slot.opt5",
                prompt="",
                text = '⑤ 70', style_role="question",
                x = 695, y = 95, font_size = 30),
        ),
        diagrams=(),
        groups=(),
        constraints=(),
        tags=(),
    )


PROBLEM_TEMPLATE = build_problem_template()

SEMANTIC_OVERRIDE = {
    "problem_id": "S3_초등_3_008605",
    "problem_type": "multiple_choice_divisibility",
    "metadata": {
        "language": "ko",
        "question": "3으로 나누어떨어지는 수가 아닌 것을 모두 고르는 문제",
        "instruction": "보기 중 조건에 맞지 않는 수를 찾는다.",
    },
    "domain": {
        "objects": [
            {"id": "obj.divisor", "type": "number", "value": 3},
            {"id": "obj.choice.1", "type": "number", "value": 27},
            {"id": "obj.choice.2", "type": "number", "value": 56},
            {"id": "obj.choice.3", "type": "number", "value": 84},
            {"id": "obj.choice.4", "type": "number", "value": 63},
            {"id": "obj.choice.5", "type": "number", "value": 70},
        ],
        "relations": [],
        "problem_solving": {
            "understand": {
                "given_refs": [
                    "obj.divisor",
                    "obj.choice.1",
                    "obj.choice.2",
                    "obj.choice.3",
                    "obj.choice.4",
                    "obj.choice.5",
                ],
                "target_ref": "answer.target",
                "condition_refs": [
                    "rel.divisible.1",
                    "rel.divisible.2",
                    "rel.divisible.3",
                    "rel.divisible.4",
                    "rel.divisible.5",
                ],
            },
            "plan": {
                "method": "divisibility_check",
                "description": "각 보기의 3으로 나눈 결과를 보고 나누어떨어지지 않는 수를 찾는다.",
            },
            "execute": {
                "expected_operations": [
                    "check_remainder_for_each_choice",
                    "select_non_divisible_numbers",
                ]
            },
            "review": {
                "check_methods": [
                    "remainder_is_nonzero",
                    "answer_matches_printed_selection",
                ]
            },
        },
    },
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {
            "type": "selected_choices",
            "description": "3으로 나누어떨어지지 않는 보기",
        },
        "value": [2, 5],
        "unit": "",
    },
}

SOLVABLE = {
    "schema": "modu.solvable.v1.1",
    "problem_id": "S3_초등_3_008605",
    "problem_type": "multiple_choice_divisibility",
    "inputs": {
        "total_ticks": 5,
        "target_label": "3으로 나누어떨어지는 수가 아닌 것",
        "target_ticks": 2,
        "target_count": 2,
        "unit": "",
    },
    "given": [
        {"ref": "obj.divisor", "value": 3},
        {"ref": "obj.choice.1", "value": 27},
        {"ref": "obj.choice.2", "value": 56},
        {"ref": "obj.choice.3", "value": 84},
        {"ref": "obj.choice.4", "value": 63},
        {"ref": "obj.choice.5", "value": 70},
    ],
    "target": {"ref": "answer.target", "type": "selected_choices"},
    "method": "divisibility_check",
    "plan": [
        "각 수를 3으로 나누어 나머지가 0인지 확인한다.",
        "나머지가 0이 아닌 보기를 고른다.",
    ],
    "steps": [
        {"id": "step.1", "expr": "27 ÷ 3", "value": {"quotient": 9, "remainder": 0}},
        {"id": "step.2", "expr": "56 ÷ 3", "value": {"quotient": 18, "remainder": 2}},
        {"id": "step.3", "expr": "84 ÷ 3", "value": {"quotient": 28, "remainder": 0}},
        {"id": "step.4", "expr": "63 ÷ 3", "value": {"quotient": 21, "remainder": 0}},
        {"id": "step.5", "expr": "70 ÷ 3", "value": {"quotient": 23, "remainder": 1}},
        {"id": "step.6", "expr": "나누어떨어지지 않는 보기 선택", "value": [2, 5]},
    ],
    "checks": [
        {
            "id": "check.1",
            "expr": "remainder(27 ÷ 3) == 0",
            "expected": True,
            "actual": True,
            "pass": True,
        },
        {
            "id": "check.2",
            "expr": "remainder(56 ÷ 3) != 0",
            "expected": True,
            "actual": True,
            "pass": True,
        },
        {
            "id": "check.3",
            "expr": "remainder(84 ÷ 3) == 0",
            "expected": True,
            "actual": True,
            "pass": True,
        },
        {
            "id": "check.4",
            "expr": "remainder(63 ÷ 3) == 0",
            "expected": True,
            "actual": True,
            "pass": True,
        },
        {
            "id": "check.5",
            "expr": "remainder(70 ÷ 3) != 0",
            "expected": True,
            "actual": True,
            "pass": True,
        },
    ],
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {
            "type": "selected_choices",
            "description": "3으로 나누어떨어지지 않는 보기",
        },
        "value": [2, 5],
        "unit": "",
    },
}
