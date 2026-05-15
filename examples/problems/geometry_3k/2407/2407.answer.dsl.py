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
        id="2407.answer",
        title="x의 값을 구하시오",
        canvas=Canvas(width=920, height=640, coordinate_mode="logical"),
        regions=(
            Region(
                id="region.stem", role="stem", flow="absolute", slot_ids=("slot.q1",)
            ),
            Region(
                id="region.diagram",
                role="diagram",
                flow="absolute",
                slot_ids=(
                    "slot.box",
                    "slot.pt.a",
                    "slot.pt.b",
                    "slot.pt.c",
                    "slot.pt.d",
                    "slot.pt.e",
                    "slot.pt.f",
                    "slot.pt.g",
                    "slot.pt.h",
                    "slot.pt.i",
                    "slot.pt.j",
                    "slot.line.1",
                    "slot.line.2",
                    "slot.line.3",
                    "slot.line.4",
                    "slot.line.5",
                    "slot.line.6",
                    "slot.line.7",
                    "slot.line.8",
                    "slot.line.9",
                    "slot.line.10",
                    "slot.lb.x1",
                    "slot.lb.x2",
                    "slot.lb.x3",
                    "slot.lb.x4",
                    "slot.lb.x5",
                    "slot.ans_overlay",
                ),
            ),
            Region(
                id="region.choice",
                role="choice",
                flow="absolute",
                slot_ids=(
                    "slot.choice1",
                    "slot.choice2",
                    "slot.choice3",
                    "slot.choice4",
                ),
            ),
        ),
        slots=(
            TextSlot(
                id="slot.q1",
                prompt="",
                text="x의 값을 구하시오.",
                style_role="question",
                x=48.0,
                y=58.0,
                font_size=30,
                anchor="start",
            ),
            TextSlot(
                id="slot.choice1",
                prompt="",
                text="1. 56 /",
                style_role="choice",
                x=670.0,
                y=70.0,
                font_size=28,
                anchor="start",
            ),
            TextSlot(
                id="slot.choice2",
                prompt="",
                text="2. 68 /",
                style_role="choice",
                x=780.0,
                y=70.0,
                font_size=28,
                anchor="start",
            ),
            TextSlot(
                id="slot.choice3",
                prompt="",
                text="3. 74 /",
                style_role="choice",
                x=670.0,
                y=110.0,
                font_size=28,
                anchor="start",
            ),
            TextSlot(
                id="slot.choice4",
                prompt="",
                text="4. 84",
                style_role="choice",
                x=780.0,
                y=110.0,
                font_size=28,
                anchor="start",
            ),
            RectSlot(
                id="slot.box",
                prompt="",
                x=52.0,
                y=132.0,
                width=816.0,
                height=430.0,
                stroke="#D0D3D6",
                stroke_width=2.0,
                fill="none",
            ),
            CircleSlot(
                id="slot.pt.a", prompt="", cx=142.0, cy=214.0, r=4.2, fill="#111111"
            ),
            CircleSlot(
                id="slot.pt.b", prompt="", cx=226.0, cy=188.0, r=4.2, fill="#111111"
            ),
            CircleSlot(
                id="slot.pt.c", prompt="", cx=316.0, cy=242.0, r=4.2, fill="#111111"
            ),
            CircleSlot(
                id="slot.pt.d", prompt="", cx=414.0, cy=182.0, r=4.2, fill="#111111"
            ),
            CircleSlot(
                id="slot.pt.e", prompt="", cx=520.0, cy=238.0, r=4.2, fill="#111111"
            ),
            CircleSlot(
                id="slot.pt.f", prompt="", cx=610.0, cy=176.0, r=4.2, fill="#111111"
            ),
            CircleSlot(
                id="slot.pt.g", prompt="", cx=694.0, cy=228.0, r=4.2, fill="#111111"
            ),
            CircleSlot(
                id="slot.pt.h", prompt="", cx=276.0, cy=342.0, r=4.2, fill="#111111"
            ),
            CircleSlot(
                id="slot.pt.i", prompt="", cx=458.0, cy=346.0, r=4.2, fill="#111111"
            ),
            CircleSlot(
                id="slot.pt.j", prompt="", cx=640.0, cy=336.0, r=4.2, fill="#111111"
            ),
            LineSlot(
                id="slot.line.1",
                prompt="",
                x1=142.0,
                y1=214.0,
                x2=226.0,
                y2=188.0,
                stroke="#2F6FDB",
                stroke_width=3.2,
            ),
            LineSlot(
                id="slot.line.2",
                prompt="",
                x1=226.0,
                y1=188.0,
                x2=316.0,
                y2=242.0,
                stroke="#2F6FDB",
                stroke_width=3.2,
            ),
            LineSlot(
                id="slot.line.3",
                prompt="",
                x1=316.0,
                y1=242.0,
                x2=414.0,
                y2=182.0,
                stroke="#2F6FDB",
                stroke_width=3.2,
            ),
            LineSlot(
                id="slot.line.4",
                prompt="",
                x1=414.0,
                y1=182.0,
                x2=520.0,
                y2=238.0,
                stroke="#2F6FDB",
                stroke_width=3.2,
            ),
            LineSlot(
                id="slot.line.5",
                prompt="",
                x1=520.0,
                y1=238.0,
                x2=610.0,
                y2=176.0,
                stroke="#2F6FDB",
                stroke_width=3.2,
            ),
            LineSlot(
                id="slot.line.6",
                prompt="",
                x1=610.0,
                y1=176.0,
                x2=694.0,
                y2=228.0,
                stroke="#2F6FDB",
                stroke_width=3.2,
            ),
            LineSlot(
                id="slot.line.7",
                prompt="",
                x1=226.0,
                y1=188.0,
                x2=276.0,
                y2=342.0,
                stroke="#2F6FDB",
                stroke_width=3.2,
            ),
            LineSlot(
                id="slot.line.8",
                prompt="",
                x1=414.0,
                y1=182.0,
                x2=458.0,
                y2=346.0,
                stroke="#2F6FDB",
                stroke_width=3.2,
            ),
            LineSlot(
                id="slot.line.9",
                prompt="",
                x1=610.0,
                y1=176.0,
                x2=640.0,
                y2=336.0,
                stroke="#2F6FDB",
                stroke_width=3.2,
            ),
            LineSlot(
                id="slot.line.10",
                prompt="",
                x1=316.0,
                y1=242.0,
                x2=458.0,
                y2=346.0,
                stroke="#2F6FDB",
                stroke_width=3.2,
            ),
            TextSlot(
                id="slot.lb.x1",
                prompt="",
                text="X°",
                style_role="label",
                x=164.0,
                y=168.0,
                font_size=28,
                anchor="start",
            ),
            TextSlot(
                id="slot.lb.x2",
                prompt="",
                text="(X-6)°",
                style_role="label",
                x=292.0,
                y=166.0,
                font_size=28,
                anchor="start",
            ),
            TextSlot(
                id="slot.lb.x3",
                prompt="",
                text="(X+10)°",
                style_role="label",
                x=468.0,
                y=162.0,
                font_size=28,
                anchor="start",
            ),
            TextSlot(
                id="slot.lb.x4",
                prompt="",
                text="56°",
                style_role="label",
                x=660.0,
                y=162.0,
                font_size=28,
                anchor="start",
            ),
            TextSlot(
                id="slot.lb.x5",
                prompt="",
                text="(X+4)°",
                style_role="label",
                x=348.0,
                y=292.0,
                font_size=28,
                anchor="start",
            ),
        ),
        diagrams=(),
        groups=(),
        constraints=(),
        tags=(),
    )


PROBLEM_TEMPLATE = build_problem_template()
SEMANTIC_OVERRIDE = {
    "problem_id": "2407.answer",
    "problem_type": "geometry_angle_choice",
    "metadata": {
        "language": "ko",
        "question": "x의 값을 구하시오.",
        "instruction": "도형 위의 각도 관계를 이용하여 x의 값을 찾는다.",
    },
    "domain": {
        "objects": [
            {"id": "obj.diagram", "type": "geometry_diagram"},
            {"id": "obj.angle.x1", "type": "angle", "label": "X"},
            {"id": "obj.angle.x2", "type": "angle", "label": "X-6"},
            {"id": "obj.angle.x3", "type": "angle", "label": "X+10"},
            {"id": "obj.angle.x4", "type": "angle", "label": "X+4"},
            {"id": "obj.angle.56", "type": "angle", "label": "56"},
            {"id": "obj.choice.1", "type": "choice", "value": 56},
            {"id": "obj.choice.2", "type": "choice", "value": 68},
            {"id": "obj.choice.3", "type": "choice", "value": 74},
            {"id": "obj.choice.4", "type": "choice", "value": 84},
        ],
        "relations": [
            {
                "id": "rel.angle.labels_present",
                "type": "label_presence",
                "from_id": "obj.diagram",
                "to_id": "obj.angle.x1",
            }
        ],
        "problem_solving": {
            "understand": {
                "given_refs": [
                    "obj.angle.x1",
                    "obj.angle.x2",
                    "obj.angle.x3",
                    "obj.angle.x4",
                    "obj.angle.56",
                ],
                "target_ref": "answer.target",
                "condition_refs": ["rel.angle.labels_present"],
            },
            "plan": {
                "method": "angle_relation_analysis",
                "description": "도형에 표시된 각도들의 위치 관계를 확인하고, 보각·맞꼭지각·삼각형 내각 관계 중 가능한 것을 검토한다.",
            },
            "execute": {
                "expected_operations": [
                    "identify_labeled_angles",
                    "inspect_incidence_relations",
                    "test_angle_equations",
                ]
            },
            "review": {
                "check_methods": ["choice_consistency_check", "geometry_relation_check"]
            },
        },
    },
    "answer": {
        "target": {"type": "angle_value", "description": "x의 값"},
        "value": None,
        "unit": "도",
    },
}
SOLVABLE = {
    "schema": "modu.solvable.v1",
    "problem_id": "2407.answer",
    "problem_type": "geometry_angle_choice",
    "inputs": {
        "total_ticks": 0,
        "target_label": "x",
        "target_ticks": 0,
        "target_count": 1,
        "unit": "도",
    },
    "given": [
        {"ref": "obj.angle.x1", "value": {"label": "X"}},
        {"ref": "obj.angle.x2", "value": {"label": "X-6"}},
        {"ref": "obj.angle.x3", "value": {"label": "X+10"}},
        {"ref": "obj.angle.x4", "value": {"label": "X+4"}},
        {"ref": "obj.angle.56", "value": {"label": "56"}},
        {"ref": "obj.choice.1", "value": 56},
        {"ref": "obj.choice.2", "value": 68},
        {"ref": "obj.choice.3", "value": 74},
        {"ref": "obj.choice.4", "value": 84},
    ],
    "target": {"ref": "answer.target", "type": "angle_value"},
    "method": "angle_relation_analysis",
    "plan": [
        "도형에 표시된 각도 라벨을 확인한다.",
        "각 관계식이 확정되지 않으므로, 정답 후보만 비교 가능한 형태로 유지한다.",
    ],
    "steps": [
        {
            "id": "step.1",
            "operation": "collect_labels",
            "expr": "X, X-6, X+10, 56, X+4",
            "value": 0,
        },
        {
            "id": "step.2",
            "operation": "compare_choices",
            "expr": "56, 68, 74, 84",
            "value": 0,
        },
    ],
    "checks": [
        {
            "id": "check.1",
            "type": "choice_presence_check",
            "expr": "보기 4개가 모두 존재하는지 확인",
            "expected": 4,
            "actual": 4,
            "pass": True,
        }
    ],
    "answer": {"value": 0, "unit": "도", "derived_from": "step.2"},
}
