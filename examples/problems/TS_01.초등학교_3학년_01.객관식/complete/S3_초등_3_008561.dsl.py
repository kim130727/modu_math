from __future__ import annotations
from modu_math.dsl import (
    Canvas,
    ProblemTemplate,
    Region,
    TextSlot,
    RectSlot,
    CircleSlot,
    LineSlot,
)


def build_problem_template() -> ProblemTemplate:
    return ProblemTemplate(
        id="S3_초등_3_008561",
        title="계산 결과가 2000보다 큰 곱셈식을 모두 선택해 보세요.",
        canvas=Canvas(width=760, height=367, coordinate_mode="logical"),
        regions=(
            Region(
                id="region.stem",
                role="stem",
                flow="absolute",
                slot_ids=("slot.q_text"),
            ),
            Region(
                id="region.diagram",
                role="diagram",
                flow="absolute",
                slot_ids=(
                    "slot.road",
                    "slot.road_dash",
                    "slot.car1.body",
                    "slot.car1.roof",
                    "slot.car1.wheel1",
                    "slot.car1.wheel2",
                    "slot.car1.window",
                    "slot.car1.text",
                    "slot.car2.body",
                    "slot.car2.roof",
                    "slot.car2.wheel1",
                    "slot.car2.wheel2",
                    "slot.car2.window",
                    "slot.car2.text",
                    "slot.car3.body",
                    "slot.car3.roof",
                    "slot.car3.wheel1",
                    "slot.car3.wheel2",
                    "slot.car3.window",
                    "slot.car3.text",
                ),
            ),
            Region(
                id="region.answer",
                role="answer",
                flow="absolute",
                slot_ids=("slot.answer_label", "slot.answer_text"),
            ),
            Region(
                id="region.explanation",
                role="explanation",
                flow="absolute",
                slot_ids=(
                    "slot.explain_label",
                    "slot.explain1",
                    "slot.explain2",
                    "slot.explain3",
                ),
            ),
        ),
        slots=(
            TextSlot(
                id="slot.q_text",
                prompt="",
                text = '계산 결과가 2000보다 큰 곱셈식을 모두 선택해 보세요.', style_role="question",
                x = 50, y = 50, font_size = 30),
            RectSlot(
                id="slot.road",
                prompt="",
                x = 130, y = 140, width = 505, height = 80, fill="#D8D8D8",
            ),
            LineSlot(
                id="slot.road_dash",
                prompt="",
                x1 = 130, y1 = 180, x2 = 640, y2 = 180, stroke="#F4F4F4",
                stroke_dasharray="8 5",
            ),
            RectSlot(
                id="slot.car1.body",
                prompt="",
                x = 180, y = 100, width = 125, height = 55, fill="#BFE6E0",
            ),
            RectSlot(
                id="slot.car1.roof",
                prompt="",
                x = 195, y = 90, width = 70, height = 20, fill="#BFE6E0",
            ),
            CircleSlot(
                id="slot.car1.wheel1",
                prompt="",
                cx = 190, cy = 155, r = 10, fill="#7A7A7A",
            ),
            CircleSlot(
                id="slot.car1.wheel2",
                prompt="",
                cx = 275, cy = 155, r = 10, fill="#7A7A7A",
            ),
            RectSlot(
                id="slot.car1.window",
                prompt="",
                x = 200, y = 95, width = 55, height = 25, fill="#DDF3F1",
            ),
            TextSlot(
                id="slot.car1.text",
                prompt="",
                text = '37 × 60', style_role="question",
                x = 195, y = 140, font_size = 25),
            RectSlot(
                id="slot.car2.body",
                prompt="",
                x = 340, y = 100, width = 125, height = 55, fill="#BFE6E0",
            ),
            RectSlot(
                id="slot.car2.roof",
                prompt="",
                x = 355, y = 90, width = 70, height = 20, fill="#BFE6E0",
            ),
            CircleSlot(
                id="slot.car2.wheel1",
                prompt="",
                cx = 350, cy = 155, r = 10, fill="#7A7A7A",
            ),
            CircleSlot(
                id="slot.car2.wheel2",
                prompt="",
                cx = 435, cy = 155, r = 10, fill="#7A7A7A",
            ),
            RectSlot(
                id="slot.car2.window",
                prompt="",
                x = 365, y = 95, width = 55, height = 25, fill="#DDF3F1",
            ),
            TextSlot(
                id="slot.car2.text",
                prompt="",
                text = '80 × 20', style_role="question",
                x = 355, y = 140, font_size = 25),
            RectSlot(
                id="slot.car3.body",
                prompt="",
                x = 500, y = 100, width = 125, height = 55, fill="#BFE6E0",
            ),
            RectSlot(
                id="slot.car3.roof",
                prompt="",
                x = 515, y = 90, width = 70, height = 20, fill="#BFE6E0",
            ),
            CircleSlot(
                id="slot.car3.wheel1",
                prompt="",
                cx = 510, cy = 155, r = 10, fill="#7A7A7A",
            ),
            CircleSlot(
                id="slot.car3.wheel2",
                prompt="",
                cx = 595, cy = 155, r = 10, fill="#7A7A7A",
            ),
            RectSlot(
                id="slot.car3.window",
                prompt="",
                x = 525, y = 95, width = 55, height = 25, fill="#DDF3F1",
            ),
            TextSlot(
                id="slot.car3.text",
                prompt="",
                text = '70 × 40', style_role="question",
                x = 515, y = 140, font_size = 25),
        ),
        diagrams=(),
        groups=(),
        constraints=(),
        tags=("곱셈", "비교", "선택", "2000보다큰수"),
    )


PROBLEM_TEMPLATE = build_problem_template()

SEMANTIC_OVERRIDE = {
    "problem_id": "S3_초등_3_008561",
    "problem_type": "multiplication_comparison_selection",
    "metadata": {
        "language": "ko",
        "question": "계산 결과가 2000보다 큰 곱셈식을 모두 선택해 보세요.",
        "instruction": "보이는 곱셈식들 중에서 계산 결과가 2000보다 큰 것을 고르는 문제이다.",
    },
    "domain": {
        "objects": [
            {
                "id": "obj.expr1",
                "type": "multiplication_expression",
                "expression": "37×60",
            },
            {
                "id": "obj.expr2",
                "type": "multiplication_expression",
                "expression": "80×20",
            },
            {
                "id": "obj.expr3",
                "type": "multiplication_expression",
                "expression": "70×40",
            },
            {"id": "obj.threshold", "type": "number", "value": 2000},
        ],
        "relations": [],
        "problem_solving": {
            "understand": {
                "given_refs": ["obj.expr1", "obj.expr2", "obj.expr3", "obj.threshold"],
                "target_ref": "answer.target",
                "condition_refs": ["rel.compare1", "rel.compare2", "rel.compare3"],
            },
            "plan": {
                "method": "compute_and_compare",
                "description": "각 곱셈식의 계산 결과를 구한 뒤 2000과 비교한다.",
            },
            "execute": {
                "expected_operations": [
                    "multiply",
                    "compare_to_threshold",
                    "select_valid_expressions",
                ]
            },
            "review": {
                "check_methods": [
                    "compare_result_with_2000",
                    "confirm_selected_expressions_match_condition",
                ]
            },
        },
    },
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {
            "type": "selected_expressions",
            "description": "계산 결과가 2000보다 큰 곱셈식",
        },
        "value": 2,
        "unit": "",
    },
}

SOLVABLE = {
    "schema": "modu.solvable.v1.1",
    "problem_id": "S3_초등_3_008561",
    "problem_type": "multiplication_comparison_selection",
    "inputs": {
        "total_ticks": 3,
        "target_label": "2000보다 큰 곱셈식",
        "target_ticks": 2,
        "target_count": 2,
        "unit": "",
    },
    "given": [
        {"ref": "obj.expr1", "value": {"expression": "37×60"}},
        {"ref": "obj.expr2", "value": {"expression": "80×20"}},
        {"ref": "obj.expr3", "value": {"expression": "70×40"}},
        {"ref": "obj.threshold", "value": 2000},
    ],
    "target": {"ref": "answer.target", "type": "selected_expressions"},
    "method": "compute_and_compare",
    "plan": [
        "각 곱셈식을 계산한 뒤 결과가 2000보다 큰지 비교한다.",
        "조건을 만족하는 식만 선택한다.",
    ],
    "steps": [
        {"id": "step.1", "expr": "37 × 60", "value": 2220},
        {"id": "step.2", "expr": "80 × 20", "value": 1600},
        {"id": "step.3", "expr": "70 × 40", "value": 2800},
        {"id": "step.4", "expr": "2220 > 2000", "value": True},
        {"id": "step.5", "expr": "1600 > 2000", "value": False},
        {"id": "step.6", "expr": "2800 > 2000", "value": True},
    ],
    "checks": [
        {
            "id": "check.1",
            "expr": "step.4 and not step.5 and step.6",
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
            "type": "selected_expressions",
            "description": "계산 결과가 2000보다 큰 곱셈식",
        },
        "value": 2,
        "unit": "",
    },
}
