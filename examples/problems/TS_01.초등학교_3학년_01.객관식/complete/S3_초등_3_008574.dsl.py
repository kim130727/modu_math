from __future__ import annotations

from modu_math.dsl import (
    Canvas,
    CircleSlot,
    LineSlot,
    ProblemTemplate,
    RectSlot,
    Region,
    TextSlot,
)


def build_problem_template() -> ProblemTemplate:
    return ProblemTemplate(
        id="S3_초등_3_008574",
        title="계산 결과가 더 작은 사람의 이름을 선택해 보세요.",
        canvas=Canvas(width = 800, height = 290, coordinate_mode="logical"),
        regions=(
            Region(
                id="region.stem",
                role="stem",
                flow="absolute",
                slot_ids=("slot.q_text",),
            ),
            Region(
                id="region.scene",
                role="diagram",
                flow="absolute",
                slot_ids=(
                    "slot.lb.left",
                    "slot.lb.right",
                    "slot.lb.left.text",
                    "slot.lb.right.text",
                    "slot.card.left",
                    "slot.card.right",
                    "slot.card.left_text",
                    "slot.card.right_text",
                    "slot.figure.left.head",
                    "slot.figure.left.body",
                    "slot.figure.left.eye1",
                    "slot.figure.left.eye2",
                    "slot.figure.left.mouth",
                    "slot.figure.right.head",
                    "slot.figure.right.body",
                    "slot.figure.right.eye1",
                    "slot.figure.right.eye2",
                    "slot.figure.right.mouth",
                ),
            ),
            Region(
                id="region.explain",
                role="supporting",
                flow="absolute",
                slot_ids=(
                    "slot.colon",
                    "slot.lt",
                    "slot.eq1",
                    "slot.eq2",
                    "slot.comp",
                ),
            ),
        ),
        slots=(
            TextSlot(
                id="slot.q_text",
                prompt="",
                text = '계산 결과가 더 작은 사람의 이름을 선택해 보세요.', style_role="question",
                x = 80, y = 40, font_size = 30),
            RectSlot(
                id="slot.lb.left",
                prompt="",
                x = 170, y = 120, width = 45, height = 30, rx=4.0,
                ry=4.0,
                fill="#FFFFFF",
                stroke="#B9C2D0",
            ),
            RectSlot(
                id="slot.lb.right",
                prompt="",
                x = 480, y = 120, width = 45, height = 30, rx=4.0,
                ry=4.0,
                fill="#FFFFFF",
                stroke="#B9C2D0",
            ),
            TextSlot(
                id="slot.lb.left.text",
                prompt="",
                text = '은우', style_role="label",
                x = 180, y = 140, font_size = 20),
            TextSlot(
                id="slot.lb.right.text",
                prompt="",
                text = '도윤', style_role="label",
                x = 485, y = 140, font_size = 20),
            RectSlot(
                id="slot.card.left",
                prompt="",
                x = 180, y = 190, width = 120, height = 60, rx=2.0,
                ry=2.0,
                fill="#F8C54A",
                stroke="#F8C54A",
            ),
            RectSlot(
                id="slot.card.right",
                prompt="",
                x = 495, y = 190, width = 120, height = 60, rx=2.0,
                ry=2.0,
                fill="#F8C54A",
                stroke="#F8C54A",
            ),
            TextSlot(
                id="slot.card.left_text",
                prompt="",
                text = '51 × 18', style_role="label",
                x = 185, y = 230, font_size = 30),
            TextSlot(
                id="slot.card.right_text",
                prompt="",
                text = '23 × 41', style_role="label",
                x = 505, y = 230, font_size = 30),
            CircleSlot(
                id="slot.figure.left.head",
                prompt="",
                cx = 275, cy = 115, r = 30, fill="#F3C0AD",
            ),
            RectSlot(
                id="slot.figure.left.body",
                prompt="",
                x = 260, y = 135, width = 30, height = 40, rx=10.0,
                ry=10.0,
                fill="#D7A0D7",
                stroke="#D7A0D7",
            ),
            CircleSlot(
                id="slot.figure.left.eye1",
                prompt="",
                cx = 265, cy = 110, r = 5, fill="#222222",
            ),
            CircleSlot(
                id="slot.figure.left.eye2",
                prompt="",
                cx = 280, cy = 110, r = 5, fill="#222222",
            ),
            LineSlot(
                id="slot.figure.left.mouth",
                prompt="",
                x1 = 265, y1 = 120, x2 = 280, y2 = 120, stroke="#C36A6A",
                stroke_dasharray="",
            ),
            CircleSlot(
                id="slot.figure.right.head",
                prompt="",
                cx = 575, cy = 115, r = 30, fill="#F3C0AD",
            ),
            RectSlot(
                id="slot.figure.right.body",
                prompt="",
                x = 560, y = 135, width = 30, height = 40, rx=10.0,
                ry=10.0,
                fill="#8ED7E6",
                stroke="#8ED7E6",
            ),
            CircleSlot(
                id="slot.figure.right.eye1",
                prompt="",
                cx = 565, cy = 115, r = 5, fill="#222222",
            ),
            CircleSlot(
                id="slot.figure.right.eye2",
                prompt="",
                cx = 580, cy = 115, r = 5, fill="#222222",
            ),
            LineSlot(
                id="slot.figure.right.mouth",
                prompt="",
                x1 = 565, y1 = 125, x2 = 580, y2 = 125, stroke="#C36A6A",
                stroke_dasharray="",
            ),
            TextSlot(
                id="slot.colon",
                prompt="",
                text=":",
                style_role="body",
                x=12.0,
                y=360.0,
                font_size=1,
            ),
            TextSlot(
                id="slot.lt",
                prompt="",
                text="<",
                style_role="body",
                x=16.0,
                y=360.0,
                font_size=1,
            ),
            TextSlot(
                id="slot.eq1",
                prompt="",
                text="=",
                style_role="body",
                x=20.0,
                y=360.0,
                font_size=1,
            ),
            TextSlot(
                id="slot.eq2",
                prompt="",
                text="=",
                style_role="body",
                x=24.0,
                y=360.0,
                font_size=1,
            ),
            TextSlot(
                id="slot.comp",
                prompt="",
                text="918<943",
                style_role="body",
                x=28.0,
                y=360.0,
                font_size=1,
            ),
        ),
        diagrams=(),
        groups=(),
        constraints=(),
        tags=(),
    )


PROBLEM_TEMPLATE = build_problem_template()

SEMANTIC_OVERRIDE = {
    "problem_id": "S3_초등_3_008574",
    "problem_type": "compare_multiplication_values",
    "metadata": {
        "language": "ko",
        "question": "계산 결과가 더 작은 사람의 이름을 선택해 보세요.",
        "instruction": "두 곱셈식의 결과를 비교하여 더 작은 쪽의 이름을 고른다.",
    },
    "domain": {
        "objects": [
            {"id": "obj.person.left", "type": "person", "name": "은우"},
            {"id": "obj.person.right", "type": "person", "name": "도윤"},
            {
                "id": "obj.expr.left",
                "type": "multiplication_expression",
                "expression": "51 × 18",
            },
            {
                "id": "obj.expr.right",
                "type": "multiplication_expression",
                "expression": "23 × 41",
            },
        ],
        "relations": [],
        "problem_solving": {
            "understand": {
                "given_refs": [
                    "obj.person.left",
                    "obj.person.right",
                    "obj.expr.left",
                    "obj.expr.right",
                ],
                "target_ref": "answer.target",
                "condition_refs": ["rel.compare_results"],
            },
            "plan": {
                "method": "compare_two_products",
                "description": "두 계산 결과를 비교해 더 작은 값을 찾는다.",
            },
            "execute": {
                "expected_operations": [
                    "compute_product_left",
                    "compute_product_right",
                    "compare_two_results",
                ]
            },
            "review": {
                "check_methods": [
                    "result_order_check",
                    "name_to_expression_match_check",
                ]
            },
        },
    },
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {
            "type": "person_name",
            "description": "계산 결과가 더 작은 사람의 이름",
        },
        "value": "은우",
        "unit": "",
    },
}

SOLVABLE = {
    "schema": "modu.solvable.v1.1",
    "problem_id": "S3_초등_3_008574",
    "problem_type": "compare_multiplication_values",
    "inputs": {
        "total_ticks": 2,
        "target_label": "결과가 더 작은 사람 이름",
        "target_ticks": 1,
        "target_count": 1,
        "unit": "",
    },
    "given": [
        {"ref": "obj.person.left", "value": {"name": "은우"}},
        {"ref": "obj.person.right", "value": {"name": "도윤"}},
        {"ref": "obj.expr.left", "value": {"expression": "51 × 18"}},
        {"ref": "obj.expr.right", "value": {"expression": "23 × 41"}},
    ],
    "target": {"ref": "answer.target", "type": "person_name"},
    "method": "compare_two_products",
    "plan": [
        "왼쪽과 오른쪽의 곱셈 결과를 각각 구한다.",
        "두 값을 비교해 더 작은 값의 이름을 찾는다.",
    ],
    "steps": [
        {"id": "step.1", "expr": "51 × 18", "value": 918},
        {"id": "step.2", "expr": "23 × 41", "value": 943},
        {"id": "step.3", "expr": "918 < 943", "value": True},
    ],
    "checks": [
        {
            "id": "check.1",
            "expr": "51 × 18 = 918",
            "expected": 918,
            "actual": 918,
            "pass": True,
        },
        {
            "id": "check.2",
            "expr": "23 × 41 = 943",
            "expected": 943,
            "actual": 943,
            "pass": True,
        },
        {
            "id": "check.3",
            "expr": "918 < 943",
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
            "type": "person_name",
            "description": "계산 결과가 더 작은 사람의 이름",
        },
        "value": "은우",
        "unit": "",
    },
}
