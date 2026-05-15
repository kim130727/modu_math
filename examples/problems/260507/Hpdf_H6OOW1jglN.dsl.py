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
        id="Hpdf_H6OOW1jglN",
        title="직사각형 이어 붙이기",
        canvas=Canvas(width=900, height=675, coordinate_mode="logical"),
        regions=(
            Region(
                id="region.stem",
                role="stem",
                flow="absolute",
                slot_ids=(
                    "slot.q1",
                    "slot.q2",
                    "slot.q3",
                    "slot.q4",
                    "slot.q5",
                    "slot.fig.outer",
                    "slot.fig.v1",
                    "slot.fig.v2",
                    "slot.fig.v3",
                    "slot.fig.h1",
                ),
            ),
        ),
        slots=(
            TextSlot(
                id="slot.q1",
                prompt="",
                text="네 변의 길이의 합이 20 cm인 작은 직사각형",
                style_role="question",
                x=12.0,
                y=40.0,
                font_size=35,
            ),
            TextSlot(
                id="slot.q2",
                prompt="",
                text="8개를 그림과 같이 겹치지 않게 이어 붙였더니",
                style_role="question",
                x=12.0,
                y=100.0,
                font_size=35,
            ),
            TextSlot(
                id="slot.q3",
                prompt="",
                text="네 변의 길이의 합이 64 cm인 큰 직사각형이",
                style_role="question",
                x=12.0,
                y=160.0,
                font_size=35,
            ),
            TextSlot(
                id="slot.q4",
                prompt="",
                text="되었습니다. 가장 작은 직사각형 한 개의 짧은",
                style_role="question",
                x=12.0,
                y=220.0,
                font_size=35,
            ),
            TextSlot(
                id="slot.q5",
                prompt="",
                text="변은 몇 cm입니까?",
                style_role="question",
                x=12.0,
                y=280.0,
                font_size=35,
            ),
            RectSlot(
                id="slot.fig.outer",
                prompt="",
                x=150.0,
                y=400.0,
                width=600.0,
                height=200.0,
                stroke="#333333",
                stroke_width=2.5,
                fill="none",
            ),
            LineSlot(
                id="slot.fig.v1",
                prompt="",
                x1=300.0,
                y1=400.0,
                x2=300.0,
                y2=600.0,
                stroke="#333333",
                stroke_width=2.0,
            ),
            LineSlot(
                id="slot.fig.v2",
                prompt="",
                x1=450.0,
                y1=400.0,
                x2=450.0,
                y2=600.0,
                stroke="#333333",
                stroke_width=2.0,
            ),
            LineSlot(
                id="slot.fig.v3",
                prompt="",
                x1=600.0,
                y1=400.0,
                x2=600.0,
                y2=600.0,
                stroke="#333333",
                stroke_width=2.0,
            ),
            LineSlot(
                id="slot.fig.h1",
                prompt="",
                x1=150.0,
                y1=500.0,
                x2=750.0,
                y2=500.0,
                stroke="#333333",
                stroke_width=2.0,
            ),
        ),
        diagrams=(),
        groups=(),
        constraints=(),
        tags=(),
    )


PROBLEM_TEMPLATE = build_problem_template()
SEMANTIC_OVERRIDE = {
    "problem_id": "Hpdf_H6OOW1jglN",
    "problem_type": "geometry_rectangle_composite",
    "metadata": {
        "language": "ko",
        "question": "네 변의 길이의 합이 20 cm인 작은 직사각형 8개를 그림과 같이 겹치지 않게 이어 붙였더니 네 변의 길이의 합이 64 cm인 큰 직사각형이 되었습니다. 가장 작은 직사각형 한 개의 짧은 변은 몇 cm입니까?",
        "instruction": "작은 직사각형의 변의 길이를 미지수로 두고 연립방정식을 세워 푼다.",
    },
    "domain": {
        "objects": [
            {
                "id": "obj.small_rectangle",
                "type": "rectangle",
                "description": "둘레가 20 cm인 작은 직사각형",
            },
            {
                "id": "obj.large_rectangle",
                "type": "rectangle",
                "description": "8개를 이어 붙여 만든 둘레 64 cm인 큰 직사각형",
            },
        ],
        "relations": [],
        "problem_solving": {
            "understand": {
                "given_refs": ["obj.small_rectangle", "obj.large_rectangle"],
                "target_ref": "answer.target",
            },
            "plan": {
                "method": "algebraic_modeling",
                "description": "작은 직사각형의 긴 변을 a, 짧은 변을 b라 하고 둘레 관계식을 세운다.",
            },
            "execute": {
                "expected_operations": [
                    "set_small_perimeter_equation",
                    "set_large_perimeter_equation",
                    "solve_system",
                ]
            },
            "review": {"check_methods": ["consistency_check"]},
        },
    },
    "answer": {
        "target": {
            "type": "length",
            "description": "가장 작은 직사각형 한 개의 짧은 변",
        },
        "value": 4,
        "unit": "cm",
    },
}
SOLVABLE = {
    "schema": "modu.solvable.v1",
    "problem_id": "Hpdf_H6OOW1jglN",
    "problem_type": "geometry_rectangle_composite",
    "inputs": {
        "total_ticks": 0,
        "target_label": "가장 작은 직사각형 한 개의 짧은 변",
        "target_ticks": 0,
        "target_count": 1,
        "unit": "cm",
    },
    "given": [
        {"ref": "obj.small_rectangle", "value": "둘레 20 cm"},
        {"ref": "obj.large_rectangle", "value": "둘레 64 cm"},
    ],
    "target": {"ref": "answer.target", "type": "length"},
    "method": "algebraic_modeling",
    "plan": [
        "작은 직사각형의 긴 변을 a, 짧은 변을 b라 하면 a+b=10이다.",
        "그림과 같이 2행 4열로 배치하면 큰 직사각형의 가로는 4a, 세로는 2b이다.",
        "큰 직사각형의 둘레는 2*(4a + 2b) = 8a + 4b = 64이다.",
        "두 식을 연립하여 a와 b를 구한다.",
    ],
    "steps": [
        {"id": "step.1", "operation": "sum_sides", "expr": "a + b = 10", "value": 10},
        {"id": "step.2", "operation": "large_perimeter", "expr": "8a + 4b = 64", "value": 64},
        {"id": "step.3", "operation": "solve", "expr": "a=6, b=4", "value": 4},
    ],
    "checks": [
        {
            "id": "check.1",
            "type": "logic_check",
            "expr": "2 * (4*6 + 2*4) = 2 * (24 + 8) = 64",
            "expected": 64,
            "actual": 64,
            "pass": True,
        }
    ],
    "answer": {"value": 4, "unit": "cm", "derived_from": "step.3"},
}
