from __future__ import annotations
from modu_math.dsl import Canvas, ProblemTemplate, Region, TextSlot, RectSlot


def build_problem_template() -> ProblemTemplate:
    return ProblemTemplate(
        id="Hpdf_8QQBoCf63S",
        title="정사각형의 개수",
        canvas=Canvas(width=880, height=518, coordinate_mode="logical"),
        regions=(
            Region(
                id="region.stem",
                role="stem",
                flow="absolute",
                slot_ids=(
                    "slot.q1",
                    "slot.q2",
                    "slot.fig.1",
                    "slot.fig.2",
                    "slot.fig.3",
                    "slot.fig.4",
                    "slot.fig.5",
                    "slot.fig.6",
                    "slot.fig.7",
                    "slot.fig.8",
                    "slot.fig.9",
                    "slot.fig.10",
                    "slot.fig.11",
                ),
            ),
        ),
        slots=(
            TextSlot(
                id="slot.q1",
                prompt="",
                text="도형에서 찾을 수 있는 크고 작은 정사각형은",
                style_role="question",
                x=12.0,
                y=40.0,
                font_size=35,
            ),
            TextSlot(
                id="slot.q2",
                prompt="",
                text="모두 몇 개입니까?",
                style_role="question",
                x=12.0,
                y=100.0,
                font_size=35,
            ),
            RectSlot(
                id="slot.fig.1",
                prompt="",
                x=300.0,
                y=150.0,
                width=100.0,
                height=100.0,
                stroke="#222222",
                stroke_width=1.5,
                fill="none",
            ),
            RectSlot(
                id="slot.fig.2",
                prompt="",
                x=400.0,
                y=150.0,
                width=100.0,
                height=100.0,
                stroke="#222222",
                stroke_width=1.5,
                fill="none",
            ),
            RectSlot(
                id="slot.fig.3",
                prompt="",
                x=500.0,
                y=150.0,
                width=100.0,
                height=100.0,
                stroke="#222222",
                stroke_width=1.5,
                fill="none",
            ),
            RectSlot(
                id="slot.fig.4",
                prompt="",
                x=200.0,
                y=250.0,
                width=100.0,
                height=100.0,
                stroke="#222222",
                stroke_width=1.5,
                fill="none",
            ),
            RectSlot(
                id="slot.fig.5",
                prompt="",
                x=300.0,
                y=250.0,
                width=100.0,
                height=100.0,
                stroke="#222222",
                stroke_width=1.5,
                fill="none",
            ),
            RectSlot(
                id="slot.fig.6",
                prompt="",
                x=400.0,
                y=250.0,
                width=100.0,
                height=100.0,
                stroke="#222222",
                stroke_width=1.5,
                fill="none",
            ),
            RectSlot(
                id="slot.fig.7",
                prompt="",
                x=500.0,
                y=250.0,
                width=100.0,
                height=100.0,
                stroke="#222222",
                stroke_width=1.5,
                fill="none",
            ),
            RectSlot(
                id="slot.fig.8",
                prompt="",
                x=600.0,
                y=250.0,
                width=100.0,
                height=100.0,
                stroke="#222222",
                stroke_width=1.5,
                fill="none",
            ),
            RectSlot(
                id="slot.fig.9",
                prompt="",
                x=300.0,
                y=350.0,
                width=100.0,
                height=100.0,
                stroke="#222222",
                stroke_width=1.5,
                fill="none",
            ),
            RectSlot(
                id="slot.fig.10",
                prompt="",
                x=400.0,
                y=350.0,
                width=100.0,
                height=100.0,
                stroke="#222222",
                stroke_width=1.5,
                fill="none",
            ),
            RectSlot(
                id="slot.fig.11",
                prompt="",
                x=500.0,
                y=350.0,
                width=100.0,
                height=100.0,
                stroke="#222222",
                stroke_width=1.5,
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
    "problem_id": "Hpdf_8QQBoCf63S",
    "problem_type": "counting_squares",
    "metadata": {
        "language": "ko",
        "question": "도형에서 찾을 수 있는 크고 작은 정사각형은 모두 몇 개인가?",
        "instruction": "도형 속 정사각형의 총 개수를 구한다.",
    },
    "domain": {
        "objects": [
            {
                "id": "obj.figure",
                "type": "composite_shape",
                "description": "여러 개의 정사각형이 맞닿아 이루어진 도형",
            },
        ],
        "relations": [],
        "problem_solving": {
            "understand": {
                "given_refs": ["obj.figure"],
                "target_ref": "answer.target",
            },
            "plan": {
                "method": "systematic_counting",
                "description": "정사각형의 크기별(1x1, 2x2, 3x3)로 나누어 개수를 센다.",
            },
            "execute": {
                "expected_operations": [
                    "count_1x1",
                    "count_2x2",
                    "count_3x3",
                    "sum_counts",
                ]
            },
            "review": {
                "check_methods": [
                    "recount",
                ]
            },
        },
    },
    "answer": {
        "target": {
            "type": "count_total_squares",
            "description": "도형에서 찾을 수 있는 크고 작은 정사각형의 총 개수",
        },
        "value": 16,
        "unit": "개",
    },
}
SOLVABLE = {
    "schema": "modu.solvable.v1",
    "problem_id": "Hpdf_8QQBoCf63S",
    "problem_type": "counting_squares",
    "inputs": {
        "total_ticks": 0,
        "target_label": "정사각형의 총 개수",
        "target_ticks": 0,
        "target_count": 0,
        "unit": "개",
    },
    "given": [
        {"ref": "obj.figure", "value": "여러 개의 정사각형이 맞닿아 이루어진 도형"},
    ],
    "target": {"ref": "answer.target", "type": "count_total_squares"},
    "method": "systematic_counting",
    "plan": [
        "크기가 1x1인 정사각형 11개를 찾는다.",
        "크기가 2x2인 정사각형 4개를 찾는다.",
        "크기가 3x3인 정사각형 1개를 찾는다.",
        "모든 개수를 더한다.",
    ],
    "steps": [
        {
            "id": "step.1",
            "operation": "sum_counts",
            "expr": "11 + 4 + 1",
            "value": 16,
        },
    ],
    "checks": [
        {
            "id": "check.1",
            "type": "logic_check",
            "expr": "11+4+1 = 16",
            "expected": 16,
            "actual": 16,
            "pass": True,
        }
    ],
    "answer": {"value": 16, "unit": "개", "derived_from": "step.1"},
}
