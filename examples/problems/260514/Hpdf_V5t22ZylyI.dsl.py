from __future__ import annotations
from modu_math.dsl import Canvas, ProblemTemplate, PolygonSlot, Region, TextSlot


def build_problem_template() -> ProblemTemplate:
    return ProblemTemplate(
        id="Hpdf_V5t22ZylyI",
        title="남은 색종이의 모든 변의 길이의 합",
        canvas=Canvas(width=800, height=651, coordinate_mode="logical"),
        regions=(
            Region(
                id="region.stem",
                role="stem",
                flow="absolute",
                slot_ids=("slot.q1", "slot.q2", "slot.q3", "slot.q4", "slot.shape"),
            ),
        ),
        slots=(
            TextSlot(
                id="slot.q1",
                prompt="",
                text="다음은 한 변이 15 cm인 정사각형 모양의 색종",
                style_role="question",
                x=18.0,
                y=40.0,
                font_size=35,
            ),
            TextSlot(
                id="slot.q2",
                prompt="",
                text="이에서 작은 직사각형 2개를 잘라 낸 것입니다.",
                style_role="question",
                x=18.0,
                y=95.0,
                font_size=35,
            ),
            TextSlot(
                id="slot.q3",
                prompt="",
                text="남은 색종이의 모든 변의 길이의 합은 몇 cm입",
                style_role="question",
                x=18.0,
                y=150.0,
                font_size=35,
            ),
            TextSlot(
                id="slot.q4",
                prompt="",
                text="니까?",
                style_role="question",
                x=18.0,
                y=205.0,
                font_size=35,
            ),
            PolygonSlot(
                id="slot.shape",
                prompt="",
                points=(
                    (348.0, 242.5),
                    (543.0, 242.5),
                    (543.0, 437.5),
                    (452.0, 437.5),
                    (452.0, 528.5),
                    (257.0, 528.5),
                    (257.0, 333.5),
                    (348.0, 333.5),
                ),
    stroke="#333333",
    stroke_width=3.0,
    fill="#d9d9d9",
),
        ),
        diagrams=(),
        groups=(),
        constraints=(),
        tags=(),
    )


PROBLEM_TEMPLATE = build_problem_template()
SEMANTIC_OVERRIDE = {
    "problem_id": "Hpdf_V5t22ZylyI",
    "problem_type": "geometry_perimeter",
    "metadata": {
        "language": "ko",
        "question": "한 변이 15 cm인 정사각형 모양의 색종이에서 작은 직사각형 2개를 잘라 낸 뒤 남은 색종이의 모든 변의 길이의 합을 구하시오.",
        "instruction": "도형의 모서리를 잘라냈을 때 둘레가 변하지 않는 원리를 이용한다.",
    },
    "domain": {
        "objects": [
            {
                "id": "obj.square",
                "type": "square",
                "side_length": 15,
            },
        ],
        "relations": [],
        "problem_solving": {
            "understand": {
                "given_refs": ["obj.square"],
                "target_ref": "answer.target",
            },
            "plan": {
                "method": "perimeter_invariant_principle",
                "description": "정사각형의 모서리에서 직사각형을 잘라내도 전체 둘레는 원래 정사각형의 둘레와 같음을 이용한다.",
            },
            "execute": {
                "expected_operations": [
                    "calculate_original_perimeter",
                ]
            },
            "review": {"check_methods": ["visual_verification"]},
        },
    },
    "answer": {
        "target": {
            "type": "length",
            "description": "남은 색종이의 모든 변의 길이의 합",
        },
        "value": 60,
        "unit": "cm",
    },
}
SOLVABLE = {
    "schema": "modu.solvable.v1",
    "problem_id": "Hpdf_V5t22ZylyI",
    "problem_type": "geometry_perimeter",
    "inputs": {
        "total_ticks": 0,
        "target_label": "남은 색종이의 둘레",
        "target_ticks": 0,
        "target_count": 0,
        "unit": "cm",
    },
    "given": [{"ref": "obj.square", "value": "한 변 15 cm"}],
    "target": {"ref": "answer.target", "type": "length"},
    "method": "perimeter_invariant_principle",
    "plan": [
        "1. 한 변이 15 cm인 정사각형의 둘레를 구한다.",
        "2. 모서리에서 직사각형을 잘라내도 둘레는 변하지 않음을 확인한다.",
        "3. 따라서 남은 색종이의 둘레도 원래 정사각형의 둘레와 같다.",
    ],
    "steps": [
        {
            "id": "step.1",
            "operation": "multiply",
            "expr": "15 * 4",
            "value": 60,
        }
    ],
    "checks": [
        {
            "id": "check.1",
            "type": "logic_check",
            "expr": "15 * 4 = 60",
            "expected": 60,
            "actual": 60,
            "pass": True,
        }
    ],
    "answer": {"value": 60, "unit": "cm", "derived_from": "step.1"},
}
