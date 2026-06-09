from __future__ import annotations
from modu_math.dsl import Canvas, ProblemTemplate, Region, RectSlot, TextSlot


def build_problem_template() -> ProblemTemplate:
    return ProblemTemplate(
        id="S3_초등_3_008587",
        title="나누어떨어지는 나눗셈을 찾아 선택하세요",
        canvas=Canvas(width=720, height=300, coordinate_mode="logical"),
        regions=(
            Region(
                id="region.stem",
                role="stem",
                flow="absolute",
                slot_ids=(
                    "slot.qtext",
                    "slot.choice_box",
                    "slot.choice.1",
                    "slot.choice.2",
                ),
            ),
        ),
        slots=(
            TextSlot(
                id="slot.qtext",
                prompt="",
                text="나누어떨어지는 나눗셈을 찾아 선택하세요.",
                style_role="question",
                x=62.0,
                y=28.0,
                font_size=28,
            ),
            RectSlot(
                id="slot.choice_box",
                prompt="",
                x = 120, y = 65, width = 390, height = 80, fill="#DCD9EE",
            ),
            TextSlot(
                id="slot.choice.1",
                prompt="",
                text = '① 72 ÷ 4', style_role="body",
                x = 165, y = 115, font_size = 30),
            TextSlot(
                id="slot.choice.2",
                prompt="",
                text = '② 52 ÷ 8', style_role="body",
                x = 340, y = 115, font_size = 30),
        ),
        diagrams=(),
        groups=(),
        constraints=(),
        tags=(),
    )


PROBLEM_TEMPLATE = build_problem_template()

SEMANTIC_OVERRIDE = {
    "problem_id": "S3_초등_3_008587",
    "problem_type": "division_choice",
    "metadata": {
        "language": "ko",
        "question": "나누어떨어지는 나눗셈을 찾아 선택하세요.",
        "instruction": "보기 중 나누어떨어지는 나눗셈을 고르는 선택형 문제",
    },
    "domain": {
        "objects": [
            {
                "id": "obj.choice1",
                "type": "division_expression",
                "dividend": 72,
                "divisor": 4,
            },
            {
                "id": "obj.choice2",
                "type": "division_expression",
                "dividend": 52,
                "divisor": 8,
            },
        ],
        "relations": [],
        "problem_solving": {
            "understand": {
                "given_refs": ["obj.choice1", "obj.choice2"],
                "target_ref": "answer.target",
                "condition_refs": ["rel.choice1.divides", "rel.choice2.remainder"],
            },
            "plan": {
                "method": "compare_remainders",
                "description": "각 나눗셈의 나머지를 확인하여 나머지가 0인 보기를 찾는다.",
            },
            "execute": {
                "expected_operations": [
                    "evaluate_division_expressions",
                    "compare_remainders",
                    "select_valid_choice",
                ]
            },
            "review": {
                "check_methods": ["remainder_zero_check", "choice_consistency_check"]
            },
        },
    },
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {"type": "selected_choice", "description": "나누어떨어지는 나눗셈"},
        "value": 1,
        "unit": "",
    },
}

SOLVABLE = {
    "schema": "modu.solvable.v1.1",
    "problem_id": "S3_초등_3_008587",
    "problem_type": "division_choice",
    "inputs": {
        "total_ticks": 2,
        "target_label": "나누어떨어지는 나눗셈",
        "target_ticks": 1,
        "target_count": 1,
        "unit": "",
    },
    "given": [
        {"ref": "obj.choice1", "value": {"dividend": 72, "divisor": 4}},
        {"ref": "obj.choice2", "value": {"dividend": 52, "divisor": 8}},
    ],
    "target": {"ref": "answer.target", "type": "selected_choice"},
    "method": "compare_remainders",
    "plan": ["각 보기의 나눗셈 결과를 확인한다.", "나머지가 0인 보기를 고른다."],
    "steps": [
        {"id": "step.1", "expr": "72 ÷ 4", "value": 18},
        {"id": "step.2", "expr": "52 ÷ 8", "value": {"quotient": 6, "remainder": 4}},
        {"id": "step.3", "expr": "나머지가 0인 보기", "value": 1},
    ],
    "checks": [
        {
            "id": "check.1",
            "expr": "72 ÷ 4 의 나머지 = 0",
            "expected": 0,
            "actual": 0,
            "pass": True,
        },
        {
            "id": "check.2",
            "expr": "52 ÷ 8 의 나머지 = 4",
            "expected": 4,
            "actual": 4,
            "pass": True,
        },
    ],
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {"type": "selected_choice", "description": "나누어떨어지는 나눗셈"},
        "value": 1,
        "unit": "",
    },
}
