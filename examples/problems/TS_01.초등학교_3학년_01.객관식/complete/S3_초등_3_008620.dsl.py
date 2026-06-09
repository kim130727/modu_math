from __future__ import annotations
from modu_math.dsl import Canvas, ProblemTemplate, Region, RectSlot, TextSlot


def build_problem_template() -> ProblemTemplate:
    return ProblemTemplate(
        id="S3_초등_3_008620",
        title="70보다 큰 것을 고르기",
        canvas=Canvas(width=808, height=436, coordinate_mode="logical"),
        regions=(
            Region(
                id="region.stem",
                role="stem",
                flow="absolute",
                slot_ids=(
                    "slot.qtext",
                    "slot.choice_box",
                    "slot.c1",
                    "slot.c2",
                    "slot.c3",
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
                id="slot.qtext",
                prompt="",
                text = '몫이 70보다 큰 것을 선택해 보세요.', style_role="question",
                x = 75, y = 40, font_size = 30),
            RectSlot(
                id="slot.choice_box",
                prompt="",
                x = 75, y = 70, width = 610, height = 75, fill="#CFEAF0",
            ),
            TextSlot(
                id="slot.c1",
                prompt="",
                text = '268 ÷ 5', style_role="question",
                x = 150, y = 120, font_size = 30),
            TextSlot(
                id="slot.c2",
                prompt="",
                text = '402 ÷ 4', style_role="question",
                x = 335, y = 120, font_size = 30),
            TextSlot(
                id="slot.c3",
                prompt="",
                text = '397 ÷ 6', style_role="question",
                x = 525, y = 115, font_size = 30),
        ),
        diagrams=(),
        groups=(),
        constraints=(),
        tags=(),
    )


PROBLEM_TEMPLATE = build_problem_template()

SEMANTIC_OVERRIDE = {
    "problem_id": "S3_초등_3_008620",
    "problem_type": "selection_comparison",
    "metadata": {
        "language": "ko",
        "question": "70보다 큰 것을 선택하는 문제",
        "instruction": "70보다 큰 것을 선택해 보세요.",
    },
    "domain": {
        "objects": [
            {"id": "obj.choice1", "type": "division_expression", "expr": "268 ÷ 5"},
            {"id": "obj.choice2", "type": "division_expression", "expr": "402 ÷ 4"},
            {"id": "obj.choice3", "type": "division_expression", "expr": "397 ÷ 6"},
        ],
        "relations": [],
        "problem_solving": {
            "understand": {
                "given_refs": ["obj.choice1", "obj.choice2", "obj.choice3"],
                "target_ref": "answer.target",
                "condition_refs": [],
            },
            "plan": {
                "method": "compare_results",
                "description": "각 나눗셈의 값을 비교해 70보다 큰 것을 고른다.",
            },
            "execute": {
                "expected_operations": [
                    "evaluate_each_expression",
                    "compare_with_threshold",
                ]
            },
            "review": {
                "check_methods": ["threshold_check", "choice_consistency_check"]
            },
        },
    },
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {"type": "selected_expression", "description": "70보다 큰 것"},
        "value": None,
        "unit": "",
    },
}

SOLVABLE = {
    "schema": "modu.solvable.v1.1",
    "problem_id": "S3_초등_3_008620",
    "problem_type": "selection_comparison",
    "inputs": {
        "total_ticks": 3,
        "target_label": "70보다 큰 것",
        "target_ticks": 1,
        "target_count": 1,
        "unit": "",
    },
    "given": [
        {"ref": "obj.choice1", "value": {"expr": "268 ÷ 5"}},
        {"ref": "obj.choice2", "value": {"expr": "402 ÷ 4"}},
        {"ref": "obj.choice3", "value": {"expr": "397 ÷ 6"}},
    ],
    "target": {"ref": "answer.target", "type": "selected_expression"},
    "method": "compare_results",
    "plan": ["각 나눗셈의 결과를 비교하여 70보다 큰 식을 찾는다."],
    "steps": [
        {"id": "step.1", "expr": "268 ÷ 5", "value": None},
        {"id": "step.2", "expr": "402 ÷ 4", "value": None},
        {"id": "step.3", "expr": "397 ÷ 6", "value": None},
    ],
    "checks": [
        {
            "id": "check.1",
            "expr": "선택한 식이 70보다 큰지 확인",
            "expected": True,
            "actual": True,
            "pass": True,
        }
    ],
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {"type": "selected_expression", "description": "70보다 큰 것"},
        "value": None,
        "unit": "",
    },
}
