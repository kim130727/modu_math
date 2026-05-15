from __future__ import annotations
from modu_math.dsl import (
    Canvas,
    ProblemTemplate,
    Region,
    RectSlot,
    CircleSlot,
    TextSlot,
)


def build_problem_template() -> ProblemTemplate:
    return ProblemTemplate(
        id="Hpdf_NncIZAqRcg",
        title="직각삼각형의 개수",
        canvas=Canvas(width=893, height=658, coordinate_mode="logical"),
        regions=(
            Region(
                id="region.stem", role="stem", flow="absolute", slot_ids=("slot.q1",)
            ),
            Region(
                id="region.diagram",
                role="diagram",
                flow="absolute",
                slot_ids=(
                    "slot.frame",
                    "slot.pt.1",
                    "slot.pt.2",
                    "slot.pt.3",
                    "slot.pt.4",
                    "slot.pt.5",
                    "slot.pt.6",
                    "slot.pt.7",
                    "slot.pt.8",
                ),
            ),
        ),
        slots=(
            TextSlot(
                id="slot.q1",
                prompt="",
                text="일정한 간격으로 점이 찍힌 종이 위에 3개의",
                style_role="question",
                x=15.0,
                y=30.0,
                font_size=35,
            ),
            TextSlot(
                id="slot.q2",
                prompt="",
                text="점을 꼭짓점으로 하는 직각삼각형을 그리려고",
                style_role="question",
                x=15.0,
                y=80.0,
                font_size=35,
            ),
            TextSlot(
                id="slot.q3",
                prompt="",
                text="합니다. 그릴 수 있는 직각삼각형은 모두 몇 개",
                style_role="question",
                x=15.0,
                y=130.0,
                font_size=35,
            ),
            TextSlot(
                id="slot.q4",
                prompt="",
                text="입니까? (단, 모양과 크기가 같아도 위치가 다",
                style_role="question",
                x=15.0,
                y=180.0,
                font_size=35,
            ),
            TextSlot(
                id="slot.q5",
                prompt="",
                text="르면 다른 것으로 봅니다.)",
                style_role="question",
                x=15.0,
                y=230.0,
                font_size=35,
            ),
            RectSlot(
                id="slot.frame",
                prompt="",
                x=159.0,
                y=350.0,
                width=577.0,
                height=227.0,
                stroke="#7F7F7F",
                stroke_width=2.0,
                rx=22.0,
                ry=22.0,
                fill="none",
            ),
            CircleSlot(
                id="slot.pt.1", prompt="", cx=256.0, cy=400.0, r=5.5, fill="#2B2524"
            ),
            CircleSlot(
                id="slot.pt.2", prompt="", cx=383.0, cy=400.0, r=5.5, fill="#2B2524"
            ),
            CircleSlot(
                id="slot.pt.3", prompt="", cx=511.0, cy=400.0, r=5.5, fill="#2B2524"
            ),
            CircleSlot(
                id="slot.pt.4", prompt="", cx=638.0, cy=400.0, r=5.5, fill="#2B2524"
            ),
            CircleSlot(
                id="slot.pt.5", prompt="", cx=256.0, cy=520.0, r=5.5, fill="#2B2524"
            ),
            CircleSlot(
                id="slot.pt.6", prompt="", cx=383.0, cy=520.0, r=5.5, fill="#2B2524"
            ),
            CircleSlot(
                id="slot.pt.7", prompt="", cx=511.0, cy=520.0, r=5.5, fill="#2B2524"
            ),
            CircleSlot(
                id="slot.pt.8", prompt="", cx=638.0, cy=520.0, r=5.5, fill="#2B2524"
            ),
        ),
        diagrams=(),
        groups=(),
        constraints=(),
        tags=(),
    )


PROBLEM_TEMPLATE = build_problem_template()
SEMANTIC_OVERRIDE = {
    "problem_id": "Hpdf_NncIZAqRcg",
    "problem_type": "counting_right_triangles",
    "metadata": {
        "language": "ko",
        "question": "일정한 간격으로 점이 찍힌 종이 위에 3개의 점을 꼭짓점으로 하는 직각삼각형을 그리려고 합니다. 그릴 수 있는 직각삼각형은 모두 몇 개입니까? (단, 모양과 크기가 같아도 위치가 다르면 다른 것으로 봅니다.)",
        "instruction": "점의 배치를 보고 직각이 생기는 경우를 모두 찾는다.",
    },
    "domain": {
        "objects": [
            {
                "id": "obj.point_set",
                "type": "point_grid",
                "structure": "2x4",
            },
        ],
        "relations": [],
        "problem_solving": {
            "understand": {
                "given_refs": ["obj.point_set"],
                "target_ref": "answer.target",
            },
            "plan": {
                "method": "systematic_counting",
                "description": "한 꼭짓점에 직각이 생기는 경우를 분류하여 센다. 가로/세로 변을 가진 경우와 대각선 변을 가진 경우로 나눈다.",
            },
            "execute": {
                "expected_operations": [
                    "count_perpendicular_axial",
                    "count_perpendicular_diagonal",
                ]
            },
            "review": {"check_methods": ["symmetry_check"]},
        },
    },
    "answer": {
        "target": {"type": "count", "description": "그릴 수 있는 직각삼각형의 개수"},
        "value": 28,
        "unit": "개",
    },
}
SOLVABLE = {
    "schema": "modu.solvable.v1",
    "problem_id": "Hpdf_NncIZAqRcg",
    "problem_type": "counting_right_triangles",
    "inputs": {
        "total_ticks": 0,
        "target_label": "직각삼각형의 개수",
        "target_ticks": 0,
        "target_count": 0,
        "unit": "개",
    },
    "given": [{"ref": "obj.point_set", "value": "2x4 점 격자"}],
    "target": {"ref": "answer.target", "type": "count"},
    "method": "systematic_counting",
    "plan": [
        "1. 직각을 낀 두 변이 격자선과 나란한 경우: 각 점에서 가로/세로로 직각을 만들 수 있는 경우는 3가지씩 총 8*3=24개이다.",
        "2. 직각을 낀 두 변이 대각선인 경우: 'ㅅ'자나 'v'자 모양으로 4개가 더 생긴다.",
        "3. 모든 경우를 합하여 총 개수를 구한다.",
    ],
    "steps": [
        {
            "id": "step.1",
            "operation": "count_axial",
            "expr": "8 * 3",
            "value": 24,
        },
        {
            "id": "step.2",
            "operation": "count_diagonal",
            "expr": "4",
            "value": 4,
        },
        {
            "id": "step.3",
            "operation": "sum",
            "expr": "24 + 4",
            "value": 28,
        },
    ],
    "checks": [
        {
            "id": "check.1",
            "type": "logic_check",
            "expr": "24 + 4 = 28",
            "expected": 28,
            "actual": 28,
            "pass": True,
        }
    ],
    "answer": {"value": 28, "unit": "개", "derived_from": "step.3"},
}
