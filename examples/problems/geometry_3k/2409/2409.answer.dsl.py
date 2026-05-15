from __future__ import annotations
from modu_math.dsl import (
    Canvas,
    CircleSlot,
    LineSlot,
    PathSlot,
    PolygonSlot,
    ProblemTemplate,
    RectSlot,
    Region,
    TextSlot,
)


# Choice text template (easy to tune)
CHOICE_FONT_FAMILY = "Cambria Math"
CHOICE_FONT_SIZE = 30
CHOICE_X = 700.0
CHOICE_Y_1 = 168.0
CHOICE_Y_2 = 224.0

RAD2 = "√2"
RAD3 = "√3"
CHOICE_LINE_1 = f"1. 21 / 2. 21 {RAD2} /"
CHOICE_LINE_2 = f"3. 21 {RAD3} / 4."


def build_problem_template() -> ProblemTemplate:
    return ProblemTemplate(
        id="2409.answer",
        title="y를 구하시오.",
        canvas=Canvas(width=1200, height=760, coordinate_mode="logical"),
        regions=(
            Region(
                id="region.stem",
                role="stem",
                flow="absolute",
                slot_ids=(
                    "slot.q1",
                    "slot.diagram_frame",
                    "slot.triangle",
                    "slot.angles",
                    "slot.labels",
                ),
            ),
            Region(
                id="region.choices",
                role="choices",
                flow="absolute",
                slot_ids=(
                    "slot.choice_1",
                    "slot.choice_2",
                    "slot.choice_3",
                    "slot.choice_4",
                ),
            ),
        ),
        slots=(
            TextSlot(
                id="slot.q1",
                prompt="",
                text="y를 구하시오.",
                style_role="question",
                x=70.0,
                y=72.0,
                font_size=34,
            ),
            RectSlot(
                id="slot.diagram_frame",
                prompt="",
                x=72.0,
                y=126.0,
                width=560.0,
                height=500.0,
                stroke="#A6A6A6",
                stroke_width=2.0,
                fill="none",
            ),
            PolygonSlot(
                id="slot.triangle",
                prompt="",
                points=((170.0, 512.0), (335.0, 198.0), (532.0, 470.0)),
                stroke="#111111",
                stroke_width=2.5,
                fill="none",
            ),
            LineSlot(
                id="slot.side_ab",
                prompt="",
                x1=170.0,
                y1=512.0,
                x2=335.0,
                y2=198.0,
                stroke="#111111",
                stroke_width=2.5,
            ),
            LineSlot(
                id="slot.side_bc",
                prompt="",
                x1=335.0,
                y1=198.0,
                x2=532.0,
                y2=470.0,
                stroke="#111111",
                stroke_width=2.5,
            ),
            LineSlot(
                id="slot.side_ca",
                prompt="",
                x1=532.0,
                y1=470.0,
                x2=170.0,
                y2=512.0,
                stroke="#111111",
                stroke_width=2.5,
            ),
            CircleSlot(
                id="slot.pt.a", prompt="", cx=170.0, cy=512.0, r=4.0, fill="#111111"
            ),
            CircleSlot(
                id="slot.pt.b", prompt="", cx=335.0, cy=198.0, r=4.0, fill="#111111"
            ),
            CircleSlot(
                id="slot.pt.c", prompt="", cx=532.0, cy=470.0, r=4.0, fill="#111111"
            ),
            TextSlot(
                id="slot.label_a",
                prompt="",
                text="A",
                style_role="label",
                x=155.0,
                y=545.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.label_b",
                prompt="",
                text="B",
                style_role="label",
                x=302.0,
                y=182.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.label_c",
                prompt="",
                text="C",
                style_role="label",
                x=543.0,
                y=484.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.len_ac",
                prompt="",
                text="21",
                style_role="label",
                x=332.0,
                y=366.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.len_ba",
                prompt="",
                text="y",
                style_role="label",
                x=246.0,
                y=376.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.len_bc",
                prompt="",
                text="x",
                style_role="label",
                x=438.0,
                y=314.0,
                font_size=28,
            ),
            PathSlot(
                id="slot.arc_b",
                prompt="",
                d="M 343 223 C 362 221, 374 230, 382 245 C 372 241, 362 238, 352 234",
                stroke="#7A4FD6",
                stroke_width=3.0,
                fill="none",
            ),
            PathSlot(
                id="slot.arc_c",
                prompt="",
                d="M 507 458 C 509 437, 522 423, 541 415 C 537 426, 531 437, 525 447",
                stroke="#7A4FD6",
                stroke_width=3.0,
                fill="none",
            ),
            TextSlot(
                id="slot.angle_b",
                prompt="",
                text="30",
                style_role="label",
                x=392.0,
                y=222.0,
                font_size=26,
            ),
            TextSlot(
                id="slot.angle_c",
                prompt="",
                text="60",
                style_role="label",
                x=548.0,
                y=425.0,
                font_size=26,
            ),
            TextSlot(
                id="slot.choice_1",
                prompt="",
                text=CHOICE_LINE_1,
                style_role="choice",
                x=CHOICE_X,
                y=CHOICE_Y_1,
                font_size=CHOICE_FONT_SIZE,
                font_family=CHOICE_FONT_FAMILY,
            ),
            TextSlot(
                id="slot.choice_2",
                prompt="",
                text=CHOICE_LINE_2,
                style_role="choice",
                x=CHOICE_X,
                y=CHOICE_Y_2,
                font_size=CHOICE_FONT_SIZE,
                font_family=CHOICE_FONT_FAMILY,
            ),
        ),
        diagrams=(),
        groups=(),
        constraints=(),
        tags=("삼각형", "각도", "객관식"),
    )


PROBLEM_TEMPLATE = build_problem_template()
SEMANTIC_OVERRIDE = {
    "problem_id": "2409.answer",
    "problem_type": "geometry_triangle",
    "metadata": {
        "language": "ko",
        "question": "y를 구하시오.",
        "instruction": "그림에서 y의 값을 구하는 문제",
    },
    "domain": {
        "objects": [
            {
                "id": "obj.triangle",
                "type": "triangle",
                "vertices": ["obj.A", "obj.B", "obj.C"],
            },
            {"id": "obj.A", "type": "vertex", "label": "A"},
            {"id": "obj.B", "type": "vertex", "label": "B"},
            {"id": "obj.C", "type": "vertex", "label": "C"},
            {"id": "obj.side_AC", "type": "segment", "label": "21"},
            {"id": "obj.side_BA", "type": "segment", "label": "y"},
            {"id": "obj.side_BC", "type": "segment", "label": "x"},
            {"id": "obj.angle_B", "type": "angle", "measure": 30},
            {"id": "obj.angle_C", "type": "angle", "measure": 60},
        ],
        "relations": [
            {
                "id": "rel.side_assignment",
                "type": "side_labeled_by",
                "from_id": "obj.side_BA",
                "to_id": "obj.B",
            },
            {
                "id": "rel.angle_assignment",
                "type": "angle_labeled_by",
                "from_id": "obj.angle_B",
                "to_id": "obj.B",
            },
            {
                "id": "rel.angle_assignment_2",
                "type": "angle_labeled_by",
                "from_id": "obj.angle_C",
                "to_id": "obj.C",
            },
        ],
        "problem_solving": {
            "understand": {
                "given_refs": ["obj.side_AC", "obj.angle_B", "obj.angle_C"],
                "target_ref": "answer.target",
                "condition_refs": [
                    "rel.side_assignment",
                    "rel.angle_assignment",
                    "rel.angle_assignment_2",
                ],
            },
            "plan": {
                "method": "triangle_geometry_reading",
                "description": "삼각형의 변과 각도 표기를 읽어 y가 표시된 변을 찾는다.",
            },
            "execute": {
                "expected_operations": [
                    "identify_labeled_side",
                    "match_angles_to_vertices",
                ]
            },
            "review": {
                "check_methods": ["label_consistency_check", "diagram_reading_check"]
            },
        },
    },
    "answer": {
        "target": {"type": "side_length", "description": "y의 값"},
        "value": None,
        "unit": "",
    },
}
SOLVABLE = {
    "schema": "modu.solvable.v1",
    "problem_id": "2409.answer",
    "problem_type": "geometry_triangle",
    "inputs": {
        "total_ticks": 1,
        "target_label": "y",
        "target_ticks": 1,
        "target_count": 1,
        "unit": "",
    },
    "given": [
        {"ref": "obj.side_AC", "value": 21},
        {"ref": "obj.angle_B", "value": 30},
        {"ref": "obj.angle_C", "value": 60},
    ],
    "target": {"ref": "answer.target", "type": "side_length"},
    "method": "triangle_geometry_reading",
    "plan": ["그림에서 y가 붙은 변을 확인한다.", "각도 표기와 변 표기를 대응시킨다."],
    "steps": [
        {
            "id": "step.1",
            "operation": "identify_target_side",
            "expr": "y가 표시된 변을 확인",
            "value": "obj.side_BA",
        },
        {
            "id": "step.2",
            "operation": "read_known_labels",
            "expr": "삼각형의 다른 표기 읽기",
            "value": {"side_AC": 21, "angle_B": 30, "angle_C": 60},
        },
    ],
    "checks": [
        {
            "id": "check.1",
            "type": "label_consistency_check",
            "expr": "y는 변 BA에 표기되어 있는가",
            "expected": True,
            "actual": True,
            "pass": True,
        }
    ],
    "answer": {"value": 0, "unit": "", "derived_from": "step.2"},
}
