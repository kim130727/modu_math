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
    slots = []
    slots.extend(
        [
            TextSlot(
                id="slot.q1",
                prompt="",
                text="가로, 세로로 이웃한 두 점 사이의 거리가 모두 같은 점 종이에서",
                style_role="question",
                x=18.0,
                y=50.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.q2_label",
                prompt="",
                text="보기의 선분과 길이가 같은 선분은 모두 몇 개 그릴 수 있습니까?",
                style_role="label",
                x=18.0,
                y=96.0,
                font_size=28,
            ),
        ]
    )
    slots.append(
        RectSlot(
            id="slot.panel.left",
            prompt="",
            x=90.0,
            y=272.0,
            width=320.0,
            height=244.0,
            rx=12.0,
            ry=12.0,
            stroke="#7E7E7E",
            stroke_width=2.0,
            fill="none",
        )
    )
    slots.append(
        RectSlot(
            id="slot.panel.left.labelbg",
            prompt="",
            x=116.0,
            y=260.0,
            width=80.0,
            height=40.0,
            rx=14.0,
            ry=14.0,
            stroke="#7E7E7E",
            stroke_width=0.0,
            fill="#9A9A9A",
        )
    )
    slots.append(
        TextSlot(
            id="slot.panel.left.label",
            prompt="",
            text="보기",
            style_role="label",
            x=130.0,
            y=289.0,
            font_size=28,
        )
    )
    left_points = [
        (140.0, 405.0),
        (214.0, 405.0),
        (286.0, 405.0),
        (356.0, 405.0),
        (140.0, 475.0),
        (214.0, 475.0),
        (286.0, 475.0),
        (356.0, 475.0),
    ]
    for i, (cx, cy) in enumerate(left_points, start=1):
        slots.append(
            CircleSlot(
                id=f"slot.left.pt{i}", prompt="", cx=cx, cy=cy, r=6.0, fill="#222222"
            )
        )
    slots.append(
        LineSlot(
            id="slot.left.line1",
            prompt="",
            x1=140.0,
            y1=475.0,
            x2=356.0,
            y2=405.0,
            stroke="#222222",
            stroke_width=3.0,
        )
    )
    slots.append(
        RectSlot(
            id="slot.panel.right",
            prompt="",
            x=500.0,
            y=260.0,
            width=300.0,
            height=310.0,
            rx=12.0,
            ry=12.0,
            stroke="#7E7E7E",
            stroke_width=2.0,
            fill="none",
        )
    )
    right_points = [
        (550.0, 317.0),
        (620.0, 317.0),
        (690.0, 317.0),
        (760.0, 317.0),
        (550.0, 389.0),
        (620.0, 389.0),
        (690.0, 389.0),
        (760.0, 389.0),
        (550.0, 459.0),
        (620.0, 459.0),
        (690.0, 459.0),
        (760.0, 459.0),
        (550.0, 530.0),
        (620.0, 530.0),
        (690.0, 530.0),
        (760.0, 530.0),
    ]
    for i, (cx, cy) in enumerate(right_points, start=1):
        slots.append(
            CircleSlot(
                id=f"slot.right.pt{i}", prompt="", cx=cx, cy=cy, r=6.0, fill="#222222"
            )
        )
    return ProblemTemplate(
        id="Hpdf_rYhg5LRe8h",
        title="보기의 선분과 같은 길이의 선분",
        canvas=Canvas(width=887, height=598, coordinate_mode="logical"),
        regions=(
            Region(
                id="region.stem",
                role="stem",
                flow="absolute",
                slot_ids=(
                    "slot.q1",
                    "slot.q2",
                    "slot.q2_label",
                    "slot.q2_tail",
                    "slot.q3",
                ),
            ),
            Region(
                id="region.diagram.left",
                role="diagram",
                flow="absolute",
                slot_ids=(
                    "slot.panel.left",
                    "slot.panel.left.labelbg",
                    "slot.panel.left.label",
                    "slot.left.pt1",
                    "slot.left.pt2",
                    "slot.left.pt3",
                    "slot.left.pt4",
                    "slot.left.pt5",
                    "slot.left.pt6",
                    "slot.left.pt7",
                    "slot.left.pt8",
                    "slot.left.line1",
                ),
            ),
            Region(
                id="region.diagram.right",
                role="diagram",
                flow="absolute",
                slot_ids=(
                    "slot.panel.right",
                    "slot.right.pt1",
                    "slot.right.pt2",
                    "slot.right.pt3",
                    "slot.right.pt4",
                    "slot.right.pt5",
                    "slot.right.pt6",
                    "slot.right.pt7",
                    "slot.right.pt8",
                    "slot.right.pt9",
                    "slot.right.pt10",
                    "slot.right.pt11",
                    "slot.right.pt12",
                    "slot.right.pt13",
                    "slot.right.pt14",
                    "slot.right.pt15",
                    "slot.right.pt16",
                ),
            ),
        ),
        slots=tuple(slots),
        diagrams=(),
        groups=(),
        constraints=(),
        tags=("점종이", "보기", "선분길이"),
    )


PROBLEM_TEMPLATE = build_problem_template()
SEMANTIC_OVERRIDE = {
    "problem_id": "Hpdf_rYhg5LRe8h",
    "problem_type": "geometry_segment_counting",
    "metadata": {
        "language": "ko",
        "question": "가로, 세로로 이웃한 두 점 사이의 거리가 모두 같은 점 종이에서 <보기>의 선분과 길이가 같은 선분은 모두 몇 개 그릴 수 있습니까?",
        "instruction": "보기의 선분(가로 3칸, 세로 1칸 대각선)과 같은 길이의 선분을 4x4 점 종이에서 모두 찾는다.",
    },
    "domain": {
        "objects": [
            {
                "id": "obj.grid",
                "type": "dot_grid",
                "size": "4x4",
            },
        ],
        "relations": [],
        "problem_solving": {
            "understand": {
                "given_refs": ["obj.grid"],
                "target_ref": "answer.target",
            },
            "plan": {
                "method": "case_analysis",
                "description": "길이가 sqrt(3^2 + 1^2)인 선분을 (3,1) 또는 (1,3) 벡터 방향으로 센다.",
            },
            "execute": {
                "expected_operations": [
                    "count_horizontal_cases",
                    "count_vertical_cases",
                ]
            },
            "review": {"check_methods": ["symmetry_check"]},
        },
    },
    "answer": {
        "target": {
            "type": "count",
            "description": "길이가 같은 선분의 개수",
        },
        "value": 12,
        "unit": "개",
    },
}
SOLVABLE = {
    "schema": "modu.solvable.v1",
    "problem_id": "Hpdf_rYhg5LRe8h",
    "problem_type": "geometry_segment_counting",
    "inputs": {
        "total_ticks": 0,
        "target_label": "선분의 개수",
        "target_ticks": 0,
        "target_count": 0,
        "unit": "개",
    },
    "given": [{"ref": "obj.grid", "value": "4x4 점 종이, 기준 선분(3x1)"}],
    "target": {"ref": "answer.target", "type": "count"},
    "method": "case_analysis",
    "plan": [
        "1. 보기의 선분은 가로 3칸, 세로 1칸(또는 그 반대)의 대각선 길이이다.",
        "2. 4x4 점 종이에서 가로 3칸, 세로 1칸인 경우를 센다.",
        "   - 가로 3칸인 쌍은 (1,4) 1가지, 세로 1칸인 쌍은 (1,2), (2,3), (3,4) 3가지.",
        "   - 각 조합마다 대각선 방향 2가지(우상향, 우하향)가 있으므로 1 * 3 * 2 = 6개.",
        "3. 세로 3칸, 가로 1칸인 경우도 대칭으로 6개.",
        "4. 총 개수는 6 + 6 = 12개이다.",
    ],
    "steps": [
        {
            "id": "step.1",
            "operation": "multiply",
            "expr": "1 * 3 * 2",
            "value": 6,
        },
        {
            "id": "step.2",
            "operation": "add",
            "expr": "6 + 6",
            "value": 12,
        },
    ],
    "checks": [
        {
            "id": "check.1",
            "type": "logic_check",
            "expr": "6 + 6 = 12",
            "expected": 12,
            "actual": 12,
            "pass": True,
        }
    ],
    "answer": {"value": 12, "unit": "개", "derived_from": "step.2"},
}
