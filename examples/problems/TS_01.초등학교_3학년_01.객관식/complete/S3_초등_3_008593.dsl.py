from __future__ import annotations
from modu_math.dsl import Canvas, ProblemTemplate, RectSlot, Region, TextSlot


def build_problem_template() -> ProblemTemplate:
    return ProblemTemplate(
        id="S3_초등_3_008593",
        title="나누어떨어지는 나눗셈을 선택하세요",
        canvas=Canvas(width=736, height=384, coordinate_mode="logical"),
        regions=(
            Region(
                id="region.stem",
                role="stem",
                flow="absolute",
                slot_ids=(
                    "slot.q1",
                    "slot.choice_box",
                    "slot.choice_1",
                    "slot.choice_2",
                    "slot.choice_3",
                ),
            ),
            Region(id="region.answer", role="answer", flow="absolute", slot_ids=()),
        ),
        slots=(
            TextSlot(
                id="slot.q1",
                prompt="",
                text = '나누어떨어지는 나눗셈을 선택하세요.', style_role="question",
                x = 95, y = 50, font_size = 30),
            RectSlot(
                id="slot.choice_box",
                prompt="",
                x = 95, y = 85, width = 500, height = 80, fill="#F8E7CA",
            ),
            TextSlot(
                id="slot.choice_1",
                prompt="",
                text = '35 ÷ 4', style_role="choice",
                x = 145, y = 135, font_size = 30),
            TextSlot(
                id="slot.choice_2",
                prompt="",
                text = '54 ÷ 9', style_role="choice",
                x = 310, y = 135, font_size = 30),
            TextSlot(
                id="slot.choice_3",
                prompt="",
                text = '28 ÷ 3', style_role="choice",
                x = 465, y = 135, font_size = 30),
        ),
        diagrams=(),
        groups=(),
        constraints=(),
        tags=(),
    )


PROBLEM_TEMPLATE = build_problem_template()

SEMANTIC_OVERRIDE = {
    "problem_id": "S3_초등_3_008593",
    "problem_type": "divisibility_selection",
    "metadata": {
        "language": "ko",
        "question": "나누어떨어지는 나눗셈을 선택하는 문제",
        "instruction": "나머지가 0인 나눗셈을 찾는다.",
    },
    "domain": {
        "objects": [
            {
                "id": "obj.choice_1",
                "type": "division_expression",
                "dividend": 35,
                "divisor": 4,
            },
            {
                "id": "obj.choice_2",
                "type": "division_expression",
                "dividend": 54,
                "divisor": 9,
            },
            {
                "id": "obj.choice_3",
                "type": "division_expression",
                "dividend": 28,
                "divisor": 3,
            },
        ],
        "relations": [],
        "problem_solving": {
            "understand": {
                "given_refs": ["obj.choice_1", "obj.choice_2", "obj.choice_3"],
                "target_ref": "answer.target",
                "condition_refs": ["rel.divisible_choice"],
            },
            "plan": {
                "method": "remainder_check",
                "description": "각 나눗셈의 나머지를 확인해 나머지가 0인 식을 찾는다.",
            },
            "execute": {
                "expected_operations": [
                    "compare_remainders",
                    "identify_divisible_expression",
                ]
            },
            "review": {"check_methods": ["remainder_zero_check"]},
        },
    },
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {
            "type": "division_expression",
            "description": "나누어떨어지는 나눗셈",
        },
        "value": "54 ÷ 9",
        "unit": "",
    },
}

SOLVABLE = {
    "schema": "modu.solvable.v1.1",
    "problem_id": "S3_초등_3_008593",
    "problem_type": "divisibility_selection",
    "inputs": {
        "total_ticks": 3,
        "target_label": "나누어떨어지는 나눗셈",
        "target_ticks": 1,
        "target_count": 1,
        "unit": "",
    },
    "given": [
        {"ref": "obj.choice_1", "value": {"dividend": 35, "divisor": 4}},
        {"ref": "obj.choice_2", "value": {"dividend": 54, "divisor": 9}},
        {"ref": "obj.choice_3", "value": {"dividend": 28, "divisor": 3}},
    ],
    "target": {"ref": "answer.target", "type": "division_expression"},
    "method": "remainder_check",
    "plan": ["각 나눗셈의 나머지를 확인한다.", "나머지가 0인 식을 정답으로 고른다."],
    "steps": [
        {"id": "step.1", "expr": "35 ÷ 4", "value": {"quotient": 8, "remainder": 3}},
        {"id": "step.2", "expr": "54 ÷ 9", "value": {"quotient": 6, "remainder": 0}},
        {"id": "step.3", "expr": "28 ÷ 3", "value": {"quotient": 9, "remainder": 1}},
        {"id": "step.4", "expr": "나머지가 0인 나눗셈 선택", "value": "54 ÷ 9"},
    ],
    "checks": [
        {
            "id": "check.1",
            "expr": "54 ÷ 9 의 나머지가 0인지 확인",
            "expected": 0,
            "actual": 0,
            "pass": True,
        }
    ],
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {
            "type": "division_expression",
            "description": "나누어떨어지는 나눗셈",
        },
        "value": "54 ÷ 9",
        "unit": "",
    },
}
