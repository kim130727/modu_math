from __future__ import annotations
from modu_math.dsl import (
    Canvas,
    ProblemTemplate,
    Region,
    TextSlot,
    RectSlot,
    PolygonSlot,
    LineSlot,
)


def build_problem_template() -> ProblemTemplate:
    return ProblemTemplate(
        id="S3_초등_3_008542",
        title="계산 결과가 3000보다 큰 곱셈식",
        canvas=Canvas(width=894, height=343, coordinate_mode="logical"),
        regions=(
            Region(
                id="region.header",
                role="stem",
                flow="absolute",
                slot_ids=("slot.qbox", "slot.qtext"),
            ),
            Region(
                id="region.options",
                role="diagram",
                flow="absolute",
                slot_ids=(
                    "slot.house1",
                    "slot.house1.text",
                    "slot.house2",
                    "slot.house2.text",
                    "slot.house3",
                    "slot.house3.text",
                    "slot.house4",
                    "slot.house4.text",
                ),
            ),
            Region(
                id="region.footer",
                role="explanation",
                flow="absolute",
                slot_ids=(
                    
                    
                ),
            ),
        ),
        slots=(
            TextSlot(
                id="slot.qtext",
                prompt="",
                text="계산 결과가 3000보다 큰 곱셈식을 모두 선택하세요.",
                style_role="question",
                x=36.0,
                y=30.0,
                font_size=28,
            ),
            PolygonSlot(
                id="slot.house1",
                prompt="",
                points=(
                    (96.0, 110.0),   # 106 -> 96 (왼쪽으로)
                    (146.0, 68.0),
                    (166.0, 88.0),
                    (178.0, 76.0),
                    (184.0, 76.0),
                    (184.0, 92.0),
                    (212.0, 110.0),  # 202 -> 212 (오른쪽으로)
                    (212.0, 218.0),  # 202 -> 212
                    (96.0, 218.0),   # 106 -> 96
                ),
            ),
            TextSlot(
                id="slot.house1.text",
                prompt="",
                text="80 × 40",
                style_role="answer_choice",
                x = 105, y = 170, font_size=28,
            ),
            PolygonSlot(
                id="slot.house2",
                prompt="",
                points=(
                    (274.0, 110.0),
                    (324.0, 68.0),
                    (344.0, 88.0),
                    (356.0, 76.0),
                    (362.0, 76.0),
                    (362.0, 92.0),
                    (390.0, 110.0),
                    (390.0, 218.0),
                    (274.0, 218.0),
                ),
            ),
            TextSlot(
                id="slot.house2.text",
                prompt="",
                text="62 × 50",
                style_role="answer_choice",
                x = 280, y = 165, font_size=28,
            ),
            PolygonSlot(
                id="slot.house3",
                prompt="",
                points=(
                    (452.0, 110.0),
                    (502.0, 68.0),
                    (522.0, 88.0),
                    (534.0, 76.0),
                    (540.0, 76.0),
                    (540.0, 92.0),
                    (568.0, 110.0),
                    (568.0, 218.0),
                    (452.0, 218.0),
                ),
            ),
            TextSlot(
                id="slot.house3.text",
                prompt="",
                text="90 × 30",
                style_role="answer_choice",
                x = 460, y = 165, font_size=28,
            ),
            PolygonSlot(
                id="slot.house4",
                prompt="",
                points=(
                    (620.0, 110.0),
                    (680.0, 68.0),
                    (700.0, 88.0),
                    (712.0, 76.0),
                    (718.0, 76.0),
                    (718.0, 92.0),
                    (736.0, 110.0),
                    (736.0, 218.0),
                    (620.0, 218.0),
                ),
            ),
            TextSlot(
                id="slot.house4.text",
                prompt="",
                text="43 × 60",
                style_role="answer_choice",
                x = 630, y = 165, font_size=28,
            ),
            
            
        ),
        diagrams=(),
        groups=(),
        constraints=(),
        tags=(),
    )


PROBLEM_TEMPLATE = build_problem_template()

SEMANTIC_OVERRIDE = {
    "problem_id": "S3_초등_3_008542",
    "problem_type": "comparison_selection",
    "metadata": {
        "language": "ko",
        "question": "계산 결과가 3000보다 큰 곱셈식을 모두 선택하는 문제",
        "instruction": "계산 결과가 3000보다 큰 곱셈식을 모두 선택하세요.",
    },
    "domain": {
        "objects": [
            {
                "id": "obj.expr1",
                "type": "multiplication_expression",
                "expression": "80 × 40",
            },
            {
                "id": "obj.expr2",
                "type": "multiplication_expression",
                "expression": "62 × 50",
            },
            {
                "id": "obj.expr3",
                "type": "multiplication_expression",
                "expression": "90 × 30",
            },
            {
                "id": "obj.expr4",
                "type": "multiplication_expression",
                "expression": "43 × 60",
            },
            {"id": "obj.threshold", "type": "number", "value": 3000},
        ],
        "relations": [],
        "problem_solving": {
            "understand": {
                "given_refs": [
                    "obj.expr1",
                    "obj.expr2",
                    "obj.expr3",
                    "obj.expr4",
                    "obj.threshold",
                ],
                "target_ref": "answer.target",
                "condition_refs": [
                    "rel.compare1",
                    "rel.compare2",
                    "rel.compare3",
                    "rel.compare4",
                ],
            },
            "plan": {
                "method": "compute_and_compare",
                "description": "각 곱셈식의 결과를 구한 뒤 3000보다 큰지 비교한다.",
            },
            "execute": {
                "expected_operations": [
                    "multiply_each_expression",
                    "compare_with_threshold",
                    "select_all_true_cases",
                ]
            },
            "review": {
                "check_methods": [
                    "compare_results_with_3000",
                    "verify_selected_expressions",
                ]
            },
        },
    },
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {
            "type": "selected_multiplication_expressions",
            "description": "계산 결과가 3000보다 큰 곱셈식",
        },
        "value": 2,
        "unit": "",
    },
}

SOLVABLE = {
    "schema": "modu.solvable.v1.1",
    "problem_id": "S3_초등_3_008542",
    "problem_type": "comparison_selection",
    "inputs": {
        "total_ticks": 4,
        "target_label": "3000보다 큰 곱셈식",
        "target_ticks": 2,
        "target_count": 2,
        "unit": "",
    },
    "given": [
        {"ref": "obj.expr1", "value": {"expression": "80 × 40"}},
        {"ref": "obj.expr2", "value": {"expression": "62 × 50"}},
        {"ref": "obj.expr3", "value": {"expression": "90 × 30"}},
        {"ref": "obj.expr4", "value": {"expression": "43 × 60"}},
        {"ref": "obj.threshold", "value": 3000},
    ],
    "target": {"ref": "answer.target", "type": "selected_multiplication_expressions"},
    "method": "compute_and_compare",
    "plan": [
        "각 곱셈식을 계산한다.",
        "각 결과를 3000과 비교한다.",
        "3000보다 큰 식만 고른다.",
    ],
    "steps": [
        {"id": "step.1", "expr": "80 × 40", "value": 3200},
        {"id": "step.2", "expr": "62 × 50", "value": 3100},
        {"id": "step.3", "expr": "90 × 30", "value": 2700},
        {"id": "step.4", "expr": "43 × 60", "value": 2580},
        {"id": "step.5", "expr": "3200 > 3000", "value": True},
        {"id": "step.6", "expr": "3100 > 3000", "value": True},
        {"id": "step.7", "expr": "2700 > 3000", "value": False},
        {"id": "step.8", "expr": "2580 > 3000", "value": False},
    ],
    "checks": [
        {
            "id": "check.1",
            "expr": "80 × 40 = 3200",
            "expected": 3200,
            "actual": 3200,
            "pass": True,
        },
        {
            "id": "check.2",
            "expr": "62 × 50 = 3100",
            "expected": 3100,
            "actual": 3100,
            "pass": True,
        },
        {
            "id": "check.3",
            "expr": "90 × 30 = 2700",
            "expected": 2700,
            "actual": 2700,
            "pass": True,
        },
        {
            "id": "check.4",
            "expr": "43 × 60 = 2580",
            "expected": 2580,
            "actual": 2580,
            "pass": True,
        },
        {
            "id": "check.5",
            "expr": "선택 결과가 3000보다 큰 식만 포함하는지 확인",
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
            "type": "selected_multiplication_expressions",
            "description": "계산 결과가 3000보다 큰 곱셈식",
        },
        "value": 2,
        "unit": "",
    },
}
