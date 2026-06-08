from __future__ import annotations
from modu_math.dsl import (
    Canvas,
    CircleSlot,
    ProblemTemplate,
    RectSlot,
    Region,
    TextSlot,
)


def build_problem_template() -> ProblemTemplate:
    return ProblemTemplate(
        id="S3_초등_3_008584",
        title="묶이 다른 것을 선택하세요",
        canvas=Canvas(width=822, height=304, coordinate_mode="logical"),
        regions=(
            Region(
                id="region.header",
                role="stem",
                flow="absolute",
                slot_ids=("slot.qtext",),
            ),
            Region(
                id="region.options",
                role="diagram",
                flow="absolute",
                slot_ids=(
                    "slot.opt1.body",
                    "slot.opt1.wheel1",
                    "slot.opt1.wheel2",
                    "slot.opt1.text",
                    "slot.opt2.body",
                    "slot.opt2.wheel1",
                    "slot.opt2.wheel2",
                    "slot.opt2.text",
                    "slot.opt3.body",
                    "slot.opt3.wheel1",
                    "slot.opt3.wheel2",
                    "slot.opt3.text",
                ),
            ),
            Region(
                id="region.answer",
                role="supplement",
                flow="absolute",
                slot_ids=(),
            ),
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
                text = '몫이 다른 것을 선택하세요.', style_role="question",
                x = 105, y = 60, font_size = 30),
            RectSlot(
                id="slot.opt1.body",
                prompt="",
                x = 110, y = 100, width = 135, height = 60),
            CircleSlot(
                id="slot.opt1.wheel1",
                prompt="",
                cx = 135, cy = 160, r = 5, fill="#1aa7a7",
            ),
            CircleSlot(
                id="slot.opt1.wheel2",
                prompt="",
                cx = 230, cy = 160, r = 5, fill="#1aa7a7",
            ),
            TextSlot(
                id="slot.opt1.text",
                prompt="",
                text = '72 ÷ 3', style_role="question",
                x = 130, y = 140, font_size = 30),
            RectSlot(
                id="slot.opt2.body",
                prompt="",
                x = 335, y = 100, width = 135, height = 60),
            CircleSlot(
                id="slot.opt2.wheel1",
                prompt="",
                cx = 355, cy = 160, r = 5, fill="#1aa7a7",
            ),
            CircleSlot(
                id="slot.opt2.wheel2",
                prompt="",
                cx = 455, cy = 160, r = 5, fill="#1aa7a7",
            ),
            TextSlot(
                id="slot.opt2.text",
                prompt="",
                text = '84 ÷ 2', style_role="question",
                x = 360, y = 140, font_size = 30),
            RectSlot(
                id="slot.opt3.body",
                prompt="",
                x = 570, y = 100, width = 135, height = 60),
            CircleSlot(
                id="slot.opt3.wheel1",
                prompt="",
                cx = 590, cy = 160, r = 5, fill="#1aa7a7",
            ),
            CircleSlot(
                id="slot.opt3.wheel2",
                prompt="",
                cx = 685, cy = 160, r = 5, fill="#1aa7a7",
            ),
            TextSlot(
                id="slot.opt3.text",
                prompt="",
                text = '96 ÷ 4', style_role="question",
                x = 595, y = 140, font_size = 30),
            
            
        ),
        diagrams=(),
        groups=(),
        constraints=(),
        tags=(),
    )


PROBLEM_TEMPLATE = build_problem_template()

SEMANTIC_OVERRIDE = {
    "problem_id": "S3_초등_3_008584",
    "problem_type": "classification_division_expression",
    "metadata": {
        "language": "ko",
        "question": "묶이 다른 것을 선택하세요.",
        "instruction": "묶이 다른 것을 선택하세요.",
    },
    "domain": {
        "objects": [
            {"id": "obj.expr1", "type": "division_expression", "expression": "72 ÷ 3"},
            {"id": "obj.expr2", "type": "division_expression", "expression": "84 ÷ 2"},
            {"id": "obj.expr3", "type": "division_expression", "expression": "96 ÷ 4"},
        ],
        "relations": [],
        "problem_solving": {
            "understand": {
                "given_refs": ["obj.expr1", "obj.expr2", "obj.expr3"],
                "target_ref": "answer.target",
                "condition_refs": ["rel.compare"],
            },
            "plan": {
                "method": "compare_by_calculation_result",
                "description": "각 나눗셈 식의 결과를 비교하여 묶이 다른 대상을 찾는다.",
            },
            "execute": {
                "expected_operations": ["evaluate_expression", "compare_groups"]
            },
            "review": {"check_methods": ["result_comparison_check"]},
        },
    },
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {"type": "different_group_expression", "description": "묶이 다른 것"},
        "value": 2,
        "unit": "",
    },
}

SOLVABLE = {
    "schema": "modu.solvable.v1.1",
    "problem_id": "S3_초등_3_008584",
    "problem_type": "classification_division_expression",
    "inputs": {
        "total_ticks": 3,
        "target_label": "묶이 다른 것",
        "target_ticks": 1,
        "target_count": 1,
        "unit": "",
    },
    "given": [
        {"ref": "obj.expr1", "value": {"expression": "72 ÷ 3"}},
        {"ref": "obj.expr2", "value": {"expression": "84 ÷ 2"}},
        {"ref": "obj.expr3", "value": {"expression": "96 ÷ 4"}},
    ],
    "target": {"ref": "answer.target", "type": "different_group_expression"},
    "method": "compare_by_calculation_result",
    "plan": ["각 나눗셈 식의 값을 구해 비교한다.", "같은 묶음이 아닌 식을 찾는다."],
    "steps": [
        {"id": "step.1", "expr": "72 ÷ 3", "value": 24},
        {"id": "step.2", "expr": "84 ÷ 2", "value": 42},
        {"id": "step.3", "expr": "96 ÷ 4", "value": 24},
    ],
    "checks": [
        {
            "id": "check.1",
            "expr": "24 == 24",
            "expected": True,
            "actual": True,
            "pass": True,
        },
        {
            "id": "check.2",
            "expr": "42 != 24",
            "expected": True,
            "actual": True,
            "pass": True,
        },
    ],
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {"type": "different_group_expression", "description": "묶이 다른 것"},
        "value": 2,
        "unit": "",
    },
}
