from __future__ import annotations
from modu_math.dsl import Canvas, ProblemTemplate, Region, TextSlot, RectSlot


def build_problem_template() -> ProblemTemplate:
    return ProblemTemplate(
        id="S3_초등_3_008632",
        title="나눗셈에서 나머지가 다른 것 고르기",
        canvas=Canvas(width=730, height=250, coordinate_mode="logical"),
        regions=(
            Region(
                id="region.stem",
                role="stem",
                flow="absolute",
                slot_ids=("slot.q.text",),
            ),
            Region(
                id="region.choices",
                role="body",
                flow="absolute",
                slot_ids=(
                    "slot.choice.1",
                    "slot.choice.2",
                    "slot.choice.3",
                    "slot.choice.4",
                    "slot.choice.5",
                ),
            ),
            Region(
                id="region.answer_explanation",
                role="explanation",
                flow="absolute",
                slot_ids=(
                    
                ),
            ),
        ),
        slots=(
            TextSlot(
                id="slot.q.text",
                prompt="",
                text = '나눗셈 중에서 나머지가 다른 하나를 고르세요.', style_role="question",
                x = 25, y = 40, font_size = 30),
            TextSlot(
                id="slot.choice.1",
                prompt="",
                text = '① 39 ÷ 3', style_role="question",
                x = 25, y = 105, font_size = 30),
            TextSlot(
                id="slot.choice.2",
                prompt="",
                text = '② 17 ÷ 4', style_role="question",
                x = 205, y = 105, font_size = 30),
            TextSlot(
                id="slot.choice.3",
                prompt="",
                text = '③ 16 ÷ 5', style_role="question",
                x = 390, y = 105, font_size = 30),
            TextSlot(
                id="slot.choice.4",
                prompt="",
                text = '④ 31 ÷ 6', style_role="question",
                x = 25, y = 150, font_size = 30),
            TextSlot(
                id="slot.choice.5",
                prompt="",
                text = '⑤ 27 ÷ 2', style_role="question",
                x = 205, y = 150, font_size = 30),
            
        ),
        diagrams=(),
        groups=(),
        constraints=(),
        tags=(),
    )


PROBLEM_TEMPLATE = build_problem_template()

SEMANTIC_OVERRIDE = {
    "problem_id": "S3_초등_3_008632",
    "problem_type": "multiple_choice_division_remainder_comparison",
    "metadata": {
        "language": "ko",
        "question": "나눗셈 중에서 나머지가 다른 하나를 고르세요.",
        "instruction": "보기의 나눗셈식들에서 나머지를 비교하여 다른 하나를 찾는다.",
    },
    "domain": {
        "objects": [
            {
                "id": "obj.choice.1",
                "type": "division_expression",
                "expression": "39 ÷ 3",
            },
            {
                "id": "obj.choice.2",
                "type": "division_expression",
                "expression": "17 ÷ 4",
            },
            {
                "id": "obj.choice.3",
                "type": "division_expression",
                "expression": "16 ÷ 5",
            },
            {
                "id": "obj.choice.4",
                "type": "division_expression",
                "expression": "31 ÷ 6",
            },
            {
                "id": "obj.choice.5",
                "type": "division_expression",
                "expression": "27 ÷ 2",
            },
        ],
        "relations": [],
        "problem_solving": {
            "understand": {
                "given_refs": [
                    "obj.choice.1",
                    "obj.choice.2",
                    "obj.choice.3",
                    "obj.choice.4",
                    "obj.choice.5",
                ],
                "target_ref": "answer.target",
                "condition_refs": ["rel.compare.remainder"],
            },
            "plan": {
                "method": "remainder_comparison",
                "description": "각 나눗셈식의 나머지를 비교하여 다른 하나를 찾는다.",
            },
            "execute": {
                "expected_operations": [
                    "identify_remainder",
                    "compare_remainders",
                    "select_different_one",
                ]
            },
            "review": {
                "check_methods": [
                    "verify_remainder_pattern",
                    "confirm_selected_choice_matches_statement",
                ]
            },
        },
    },
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {
            "type": "different_remainder_choice",
            "description": "나머지가 다른 하나",
        },
        "value": 1,
        "unit": "",
    },
}

SOLVABLE = {
    "schema": "modu.solvable.v1.1",
    "problem_id": "S3_초등_3_008632",
    "problem_type": "multiple_choice_division_remainder_comparison",
    "inputs": {
        "total_ticks": 5,
        "target_label": "나머지가 다른 하나",
        "target_ticks": 1,
        "target_count": 1,
        "unit": "",
    },
    "given": [
        {"ref": "obj.choice.1", "value": {"expression": "39 ÷ 3"}},
        {"ref": "obj.choice.2", "value": {"expression": "17 ÷ 4"}},
        {"ref": "obj.choice.3", "value": {"expression": "16 ÷ 5"}},
        {"ref": "obj.choice.4", "value": {"expression": "31 ÷ 6"}},
        {"ref": "obj.choice.5", "value": {"expression": "27 ÷ 2"}},
    ],
    "target": {"ref": "answer.target", "type": "different_remainder_choice"},
    "method": "remainder_comparison",
    "plan": ["각 식의 나머지를 확인하고, 다른 나머지를 가진 보기를 찾는다."],
    "steps": [
        {"id": "step.1", "expr": "39 ÷ 3", "value": {"quotient": 13, "remainder": 0}},
        {"id": "step.2", "expr": "17 ÷ 4", "value": {"quotient": 4, "remainder": 1}},
        {"id": "step.3", "expr": "16 ÷ 5", "value": {"quotient": 3, "remainder": 1}},
        {"id": "step.4", "expr": "31 ÷ 6", "value": {"quotient": 5, "remainder": 1}},
        {"id": "step.5", "expr": "27 ÷ 2", "value": {"quotient": 13, "remainder": 1}},
        {"id": "step.6", "expr": "나머지가 다른 보기 선택", "value": 1},
    ],
    "checks": [
        {
            "id": "check.1",
            "expr": "obj.choice.1.remainder != obj.choice.2.remainder",
            "expected": True,
            "actual": True,
            "pass": True,
        },
        {
            "id": "check.2",
            "expr": "선택된 답이 ①인지 확인",
            "expected": 1,
            "actual": 1,
            "pass": True,
        },
    ],
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {
            "type": "different_remainder_choice",
            "description": "나머지가 다른 하나",
        },
        "value": 1,
        "unit": "",
    },
}
