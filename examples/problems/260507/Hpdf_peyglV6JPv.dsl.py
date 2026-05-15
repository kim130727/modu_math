from __future__ import annotations
from modu_math.dsl import (
    Canvas,
    ProblemTemplate,
    Region,
    TextSlot,
    RectSlot,
    LineSlot,
    PathSlot,
)


def build_problem_template() -> ProblemTemplate:
    return ProblemTemplate(
        id="Hpdf_peyglV6JPv",
        title="직사각형의 네 변의 길이의 합",
        canvas=Canvas(width=700, height=750, coordinate_mode="logical"),
        regions=(
            Region(
                id="region.stem",
                role="stem",
                flow="absolute",
                slot_ids=("slot.q1", "slot.q2", "slot.q3"),
            ),
            Region(
                id="region.diagram",
                role="diagram",
                flow="absolute",
                slot_ids=(
                    "slot.outer",
                    "slot.inner.v1",
                    "slot.inner.v2",
                    "slot.inner.h1",
                    "slot.inner.h2",
                    "slot.inner.h3",
                    "slot.inner.h4",
                    "slot.ann.text",
                    "slot.ann.arrow",
                ),
            ),
        ),
        slots=(
            TextSlot(
                id="slot.q1",
                prompt="",
                text="다음 도형은 크기가 서로 다른 4가지 정사각형",
                style_role="question",
                x=22.0,
                y=40.0,
                font_size=35,
            ),
            TextSlot(
                id="slot.q2",
                prompt="",
                text="으로 만든 직사각형입니다. 가장 큰 직사각형의",
                style_role="question",
                x=22.0,
                y=90.0,
                font_size=35,
            ),
            TextSlot(
                id="slot.q3",
                prompt="",
                text="네 변의 길이의 합은 몇 cm입니까?",
                style_role="question",
                x=22.0,
                y=140.0,
                font_size=35,
            ),
            RectSlot(
                id="slot.outer",
                prompt="",
                x=186.0,
                y=220.0,
                width=300.0,
                height=480.0,
                stroke="#222222",
                stroke_width=2.0,
                fill="none",
            ),
            LineSlot(
                id="slot.inner.v1",
                prompt="",
                x1=306.0,
                y1=220.0,
                x2=306.0,
                y2=400.0,
                stroke="#222222",
                stroke_width=2.0,
            ),
            LineSlot(
                id="slot.inner.v2",
                prompt="",
                x1=246.0,
                y1=220.0,
                x2=246.0,
                y2=280.0,
                stroke="#222222",
                stroke_width=2.0,
            ),
            LineSlot(
                id="slot.inner.h1",
                prompt="",
                x1=186.0,
                y1=280.0,
                x2=306.0,
                y2=280.0,
                stroke="#222222",
                stroke_width=2.0,
            ),
            LineSlot(
                id="slot.inner.h2",
                prompt="",
                x1=186.0,
                y1=400.0,
                x2=486.0,
                y2=400.0,
                stroke="#222222",
                stroke_width=2.0,
            ),
            TextSlot(
                id="slot.ann.text",
                prompt="",
                text="3 cm",
                style_role="label",
                x=200.0,
                y=180.0,
                font_size=35,
            ),
            PathSlot(
                id="slot.ann.arrow",
                prompt="",
                d="M 216 190 C 216 200, 216 210, 216 218",
                stroke="#222222",
                stroke_width=1.2,
                stroke_dasharray="4 3",
                fill="none",
            ),
        ),
        diagrams=(),
        groups=(),
        constraints=(),
        tags=(),
    )


PROBLEM_TEMPLATE = build_problem_template()
SEMANTIC_OVERRIDE = {
    "problem_id": "Hpdf_peyglV6JPv",
    "problem_type": "geometry_rectangle_perimeter",
    "metadata": {
        "language": "ko",
        "question": "다음 도형은 크기가 서로 다른 4가지 정사각형으로 만든 직사각형입니다. 가장 큰 직사각형의 네 변의 길이의 합은 몇 cm입니까?",
        "instruction": "도형의 길이 관계를 보고 가장 큰 직사각형의 둘레를 구한다.",
    },
    "domain": {
        "objects": [
            {
                "id": "obj.outer_rectangle",
                "type": "rectangle",
                "description": "가장 큰 바깥 직사각형",
            },
            {
                "id": "obj.length_marker",
                "type": "length_label",
                "description": "3 cm 표기",
            },
        ],
        "relations": [],
        "problem_solving": {
            "understand": {
                "given_refs": ["obj.length_marker"],
                "target_ref": "answer.target",
                "condition_refs": [],
            },
            "plan": {
                "method": "length_relation",
                "description": "도형 안의 정사각형 배치에서 길이 관계를 읽어 전체 둘레를 구한다.",
            },
            "execute": {
                "expected_operations": [
                    "read_length_label",
                    "analyze_square_partition",
                    "determine_outer_rectangle_perimeter",
                ]
            },
            "review": {"check_methods": ["geometry_consistency_check", "unit_check"]},
        },
    },
    "answer": {
        "target": {
            "type": "perimeter",
            "description": "가장 큰 직사각형의 네 변의 길이의 합",
        },
        "value": 78,
        "unit": "cm",
    },
}
SOLVABLE = {
    "schema": "modu.solvable.v1",
    "problem_id": "Hpdf_peyglV6JPv",
    "problem_type": "geometry_rectangle_perimeter",
    "inputs": {
        "total_ticks": 0,
        "target_label": "가장 큰 직사각형의 네 변의 길이의 합",
        "target_ticks": 0,
        "target_count": 1,
        "unit": "cm",
    },
    "given": [{"ref": "obj.length_marker", "value": "3 cm"}],
    "target": {"ref": "answer.target", "type": "perimeter"},
    "method": "length_relation_inference",
    "plan": [
        "가장 작은 두 정사각형의 한 변이 3cm임을 확인한다.",
        "그 아래의 정사각형은 3+3=6cm, 그 옆의 정사각형은 3+6=9cm임을 구한다.",
        "맨 아래의 큰 정사각형은 6+9=15cm임을 구한다.",
        "전체 직사각형의 가로는 15cm, 세로는 9+15=24cm이므로 둘레를 계산한다.",
    ],
    "steps": [
        {"id": "step.1", "operation": "identify_small_square", "expr": "3", "value": 3},
        {"id": "step.2", "operation": "calculate_sides", "expr": "6, 9, 15", "value": 15},
        {
            "id": "step.3",
            "operation": "calculate_perimeter",
            "expr": "2 * (15 + (9 + 15))",
            "value": 78,
        },
    ],
    "checks": [
        {
            "id": "check.1",
            "type": "logic_check",
            "expr": "2 * (15 + 24) = 78",
            "expected": 78,
            "actual": 78,
            "pass": True,
        }
    ],
    "answer": {"value": 78, "unit": "cm", "derived_from": "step.3"},
}
