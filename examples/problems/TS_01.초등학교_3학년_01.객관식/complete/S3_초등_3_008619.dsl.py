from __future__ import annotations
from modu_math.dsl import Canvas, ProblemTemplate, Region, RectSlot, TextSlot


def build_problem_template() -> ProblemTemplate:
    return ProblemTemplate(
        id="S3_초등_3_008619",
        title="나머지가 더 큰 것을 찾아 선택하세요.",
        canvas=Canvas(width=856, height=317, coordinate_mode="logical"),
        regions=(
            Region(
                id="region.stem",
                role="stem",
                flow="absolute",
                slot_ids=("slot.instruction",),
            ),
            Region(
                id="region.choices",
                role="body",
                flow="absolute",
                slot_ids=(
                    "slot.choice.left",
                    "slot.choice.right",
                    "slot.choice.left.text",
                    "slot.choice.right.text",
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
                id="slot.instruction",
                prompt="",
                text = '나머지가 더 큰 것을 찾아 선택하세요.', style_role="question",
                x = 75, y = 35, font_size = 30, fill = '#111111'),
            RectSlot(
                id="slot.choice.left",
                prompt="",
                x = 75, y = 73, width = 180, height = 75, fill="#FFF6F6",
                stroke="#F4B7B7",
            ),
            RectSlot(
                id="slot.choice.right",
                prompt="",
                x = 335, y = 73, width = 180, height = 75, fill="#FFF6F6",
                stroke="#F4B7B7",
            ),
            TextSlot(
                id="slot.choice.left.text",
                prompt="",
                text = '517 ÷ 4', style_role="question",
                x = 110, y = 120, font_size = 30),
            TextSlot(
                id="slot.choice.right.text",
                prompt="",
                text = '519 ÷ 6', style_role="question",
                x = 370, y = 120, font_size = 30),
        ),
        diagrams=(),
        groups=(),
        constraints=(),
        tags=(),
    )


PROBLEM_TEMPLATE = build_problem_template()

SEMANTIC_OVERRIDE = {
    "problem_id": "S3_초등_3_008619",
    "problem_type": "comparison_remainder",
    "metadata": {
        "language": "ko",
        "question": "나머지가 더 큰 것을 찾아 선택하는 문제",
        "instruction": "나머지가 더 큰 것을 찾아 선택하세요.",
    },
    "domain": {
        "objects": [
            {
                "id": "obj.left_division",
                "type": "division_expression",
                "expression": "517 ÷ 4",
            },
            {
                "id": "obj.right_division",
                "type": "division_expression",
                "expression": "519 ÷ 6",
            },
        ],
        "relations": [],
        "problem_solving": {
            "understand": {
                "given_refs": ["obj.left_division", "obj.right_division"],
                "target_ref": "answer.target",
                "condition_refs": ["rel.compare_remainder"],
            },
            "plan": {
                "method": "compare_remainders",
                "description": "두 나눗셈의 나머지를 비교한다.",
            },
            "execute": {"expected_operations": ["read_remainder", "compare_values"]},
            "review": {"check_methods": ["compare_remainder_consistency"]},
        },
    },
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {
            "type": "selected_division_expression",
            "description": "나머지가 더 큰 나눗셈 식",
        },
        "value": 519,
        "unit": "",
    },
}

SOLVABLE = {
    "schema": "modu.solvable.v1.1",
    "problem_id": "S3_초등_3_008619",
    "problem_type": "comparison_remainder",
    "inputs": {
        "total_ticks": 2,
        "target_label": "나머지가 더 큰 식",
        "target_ticks": 1,
        "target_count": 1,
        "unit": "",
    },
    "given": [
        {
            "ref": "obj.left_division",
            "value": {"expression": "517 ÷ 4", "remainder": 1},
        },
        {
            "ref": "obj.right_division",
            "value": {"expression": "519 ÷ 6", "remainder": 3},
        },
    ],
    "target": {"ref": "answer.target", "type": "selected_division_expression"},
    "method": "compare_remainders",
    "plan": ["두 식의 나머지를 확인하여 더 큰 값을 고른다."],
    "steps": [
        {"id": "step.1", "expr": "517 ÷ 4의 나머지", "value": 1},
        {"id": "step.2", "expr": "519 ÷ 6의 나머지", "value": 3},
        {"id": "step.3", "expr": "1 < 3", "value": True},
    ],
    "checks": [
        {
            "id": "check.1",
            "expr": "더 큰 나머지를 가진 식을 선택했는가",
            "expected": "519 ÷ 6",
            "actual": "519 ÷ 6",
            "pass": True,
        }
    ],
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {
            "type": "selected_division_expression",
            "description": "나머지가 더 큰 나눗셈 식",
        },
        "value": 519,
        "unit": "",
    },
}
