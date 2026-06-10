from __future__ import annotations
from modu_math.dsl import Canvas, ProblemTemplate, RectSlot, Region, TextSlot


def build_problem_template() -> ProblemTemplate:
    return ProblemTemplate(
        id="S3_초등_3_008629",
        title="몫이 더 작은 것을 선택하세요",
        canvas=Canvas(width=652, height=260, coordinate_mode="logical"),
        regions=(
            Region(
                id="region.header",
                role="stem",
                flow="absolute",
                slot_ids=("slot.prompt",'slot.prompt.copy1', 'slot.prompt.copy1.copy2'),
            ),
            Region(
                id="region.compare_box",
                role="diagram",
                flow="absolute",
                slot_ids=("slot.compare_box",),
            ),
            Region(id="region.answer", role="answer", flow="absolute", slot_ids=()),
            Region(
                id="region.explanation",
                role="explanation",
                flow="absolute",
                slot_ids=(),
            ),
        ),
        slots=(TextSlot(
                id="slot.prompt",
                prompt="",
                text = '몫이 더 작은 것을 선택하세요.', style_role="question",
                x = 65, y = 50, font_size = 30),
            RectSlot(
                id="slot.compare_box",
                prompt="",
                x = 65, y = 75, width = 460, height = 75, fill="none",
                stroke="#EE9AD3",
                stroke_width=1.5,
            ),TextSlot(id = 'slot.prompt.copy1', prompt = '', text = '96 ÷ 3', x = 150, y = 125, font_size = 30, fill = '#111111'), TextSlot(id = 'slot.prompt.copy1.copy2', prompt = '', text = '84 ÷ 2', x = 355, y = 125, font_size = 30, fill = '#111111')),
        diagrams=(),
        groups=(),
        constraints=(),
        tags=(),
    )


PROBLEM_TEMPLATE = build_problem_template()

SEMANTIC_OVERRIDE = {
    "problem_id": "S3_초등_3_008629",
    "problem_type": "compare_division_expressions",
    "metadata": {
        "language": "ko",
        "question": "몫이 더 작은 것을 선택하세요.",
        "instruction": "두 나눗셈 식을 비교하여 더 작은 것을 고른다.",
    },
    "domain": {
        "objects": [
            {"id": "obj.expr1", "type": "division_expression", "expression": "96 ÷ 3"},
            {"id": "obj.expr2", "type": "division_expression", "expression": "84 ÷ 2"},
        ],
        "relations": [],
        "problem_solving": {
            "understand": {
                "given_refs": ["obj.expr1", "obj.expr2"],
                "target_ref": "answer.target",
                "condition_refs": ["rel.compare_results"],
            },
            "plan": {
                "method": "compute_and_compare",
                "description": "두 나눗셈의 결과를 구한 뒤 더 작은 식을 고른다.",
            },
            "execute": {
                "expected_operations": [
                    "divide_each_expression",
                    "compare_results",
                    "select_smaller_expression",
                ]
            },
            "review": {"check_methods": ["comparison_consistency_check"]},
        },
    },
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {
            "type": "smaller_expression",
            "description": "몫이 더 작은 나눗셈 식",
        },
        "value": 0,
        "unit": "",
    },
}

SOLVABLE = {
    "schema": "modu.solvable.v1.1",
    "problem_id": "S3_초등_3_008629",
    "problem_type": "compare_division_expressions",
    "inputs": {
        "total_ticks": 2,
        "target_label": "smaller_expression",
        "target_ticks": 1,
        "target_count": 1,
        "unit": "",
    },
    "given": [
        {"ref": "obj.expr1", "value": {"expression": "96 ÷ 3"}},
        {"ref": "obj.expr2", "value": {"expression": "84 ÷ 2"}},
    ],
    "target": {"ref": "answer.target", "type": "smaller_expression"},
    "method": "compute_and_compare",
    "plan": [
        "두 식의 계산 결과를 구한 뒤 크기를 비교한다.",
        "더 작은 결과를 가진 식을 선택한다.",
    ],
    "steps": [
        {"id": "step.1", "expr": "96 ÷ 3", "value": 32},
        {"id": "step.2", "expr": "84 ÷ 2", "value": 42},
        {"id": "step.3", "expr": "32 < 42", "value": True},
        {"id": "step.4", "expr": "더 작은 식 선택", "value": "96 ÷ 3"},
    ],
    "checks": [
        {
            "id": "check.1",
            "expr": "32 < 42",
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
            "type": "smaller_expression",
            "description": "몫이 더 작은 나눗셈 식",
        },
        "value": 0,
        "unit": "",
    },
}
