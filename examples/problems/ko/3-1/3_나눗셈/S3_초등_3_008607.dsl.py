from __future__ import annotations
from modu_math.dsl import Canvas, ProblemTemplate, RectSlot, Region, TextSlot


def build_problem_template() -> ProblemTemplate:
    return ProblemTemplate(
        id="S3_초등_3_008607",
        title="나누어떨어지는 나눗셈식을 찾아 선택하세요.",
        canvas=Canvas(width=740, height=270, coordinate_mode="logical"),
        regions=(
            Region(
                id="region.stem",
                role="stem",
                flow="absolute",
                slot_ids=("slot.q.text",),
            ),
            Region(
                id="region.choices",
                role="choices",
                flow="absolute",
                slot_ids=(
                    "slot.choice.1.box",
                    "slot.choice.1.text",
                    "slot.choice.2.box",
                    "slot.choice.2.text",
                ),
            ),
            Region(id="region.answer", role="answer", flow="absolute", slot_ids=()),
        ),
        slots=(
            TextSlot(
                id="slot.q.text",
                prompt="",
                text = '나누어떨어지는 나눗셈식을 찾아 선택하세요.', style_role="question",
                x = 70, y = 55, font_size = 30),
            RectSlot(
                id="slot.choice.1.box",
                prompt="",
                x = 115, y = 95, width = 180, height = 80),
            TextSlot(
                id="slot.choice.1.text",
                prompt="",
                text = '87 ÷ 4', style_role="choice",
                x = 155, y = 145, font_size = 30),
            RectSlot(
                id="slot.choice.2.box",
                prompt="",
                x = 340, y = 95, width = 180, height = 80),
            TextSlot(
                id="slot.choice.2.text",
                prompt="",
                text = '48 ÷ 4', style_role="choice",
                x = 385, y = 145, font_size = 30),
        ),
        diagrams=(),
        groups=(),
        constraints=(),
        tags=("초등", "수학", "나눗셈", "나누어떨어짐", "선택형"),
    )


PROBLEM_TEMPLATE = build_problem_template()

SEMANTIC_OVERRIDE = {
    "problem_id": "S3_초등_3_008607",
    "problem_type": "divisibility_selection",
    "metadata": {
        "language": "ko",
        "question": "나누어떨어지는 나눗셈식을 찾아 선택하는 문제",
        "instruction": "나누어떨어지는 나눗셈식을 찾아 선택하세요.",
    },
    "domain": {
        "objects": [
            {"id": "obj.choice.1", "type": "division_expression", "expression": "87 ÷ 4"},
            {"id": "obj.choice.2", "type": "division_expression", "expression": "48 ÷ 4"},
        ],
        "relations": [],
        "problem_solving": {
            "understand": {
                "given_refs": ["obj.choice.1", "obj.choice.2"],
                "target_ref": "answer.target",
                "condition_refs": ["rel.divisibility_check"],
            },
            "plan": {
                "method": "division_remainder_check",
                "description": "각 나눗셈식의 결과를 보고 나누어떨어지는 식을 고른다.",
            },
            "execute": {
                "expected_operations": ["evaluate_each_expression", "compare_remainders", "select_divisible_expression"]
            },
            "review": {"check_methods": ["remainder_zero_check", "selection_consistency_check"]},
        },
    },
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {
            "type": "divisible_division_expression",
            "description": "나누어떨어지는 나눗셈식",
        },
        "value": "48 ÷ 4",
        "unit": "",
    },
}

SOLVABLE = {
    "schema": "modu.solvable.v1.1",
    "problem_id": "S3_초등_3_008607",
    "problem_type": "divisibility_selection",
    "inputs": {
        "total_ticks": 2,
        "target_label": "나누어떨어지는 나눗셈식",
        "target_ticks": 1,
        "target_count": 1,
        "unit": "",
    },
    "given": [
        {"ref": "obj.choice.1", "value": {"expression": "87 ÷ 4"}},
        {"ref": "obj.choice.2", "value": {"expression": "48 ÷ 4"}},
    ],
    "target": {"ref": "answer.target", "type": "divisible_division_expression"},
    "method": "division_remainder_check",
    "plan": ["각 나눗셈식의 결과를 보고 나누어떨어지는 식을 고른다."],
    "steps": [
        {"id": "step.1", "expr": "87 ÷ 4", "value": {"quotient": 21, "remainder": 3}},
        {"id": "step.2", "expr": "48 ÷ 4", "value": {"quotient": 12, "remainder": 0}},
        {"id": "step.3", "expr": "나누어떨어지는 식 선택", "value": "48 ÷ 4"},
    ],
    "checks": [
        {
            "id": "check.1",
            "expr": "48 ÷ 4 remainder == 0",
            "expected": True,
            "actual": True,
            "pass": True,
        }
    ],
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {
            "type": "divisible_division_expression",
            "description": "나누어떨어지는 나눗셈식",
        },
        "value": "48 ÷ 4",
        "unit": "",
    },
}
