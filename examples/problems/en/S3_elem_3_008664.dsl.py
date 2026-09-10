from __future__ import annotations

from modu_math.dsl import (
    Arrow,
    BlankSlot,
    Canvas,
    ChoiceSlot,
    Circle,
    CircleSlot,
    Constraint,
    Cube,
    DiagramTemplate,
    FractionAreaModel,
    Grid,
    Group,
    ImageSlot,
    LabelSlot,
    LineSlot,
    PathSlot,
    PolygonSlot,
    ProblemTemplate,
    RectSlot,
    Region,
    ShapeObject,
    TextBoxSlot,
    TextSlot,
    Triangle,
)


def build_problem_template() -> ProblemTemplate:
    canvas = Canvas(
        width=800,
        height=360,
        coordinate_mode="logical",
    )
    regions = (
        Region(
            id="region.stem",
            role="stem",
            flow="absolute",
            slot_ids=("slot.question",),
        ),
        Region(
            id="region.diagram",
            role="diagram",
            flow="absolute",
            slot_ids=(
                "slot.bar",
                "slot.hole.1",
                "slot.hole.2",
                "slot.hole.3",
                "slot.hole.4",
                "slot.hole.5",
                "slot.link.1",
                "slot.link.2",
                "slot.link.3",
                "slot.link.4",
                "slot.link.5",
                "slot.choice.lb.1",
                "slot.choice.lb.2",
                "slot.choice.lb.3",
                "slot.choice.lb.4",
                "slot.choice.lb.5",
                "slot.hole.5.copy13",
            ),
        ),
    )
    slots = (
        TextBoxSlot(
            id="slot.question",
            prompt="",
            text=(
                "Use a pushpin and a strip of paper to draw a circle. Choose the label of the hole "
                "where the pencil should be inserted to draw the largest circle."
            ),
            style_role="question",
            x=37.211,
            y=23.106,
            width=717.416,
            height=158,
            font_size=30,
            line_height=1.25,
            fill="#111827",
        ),
        RectSlot(
            id="slot.bar",
            prompt="",
            x=175,
            y=210,
            width=435,
            height=40,
            stroke="#8fcfd0",
            stroke_width=1,
            fill="#bfeaed",
        ),
        CircleSlot(
            id="slot.hole.1",
            prompt="",
            cx=275,
            cy=230,
            r=5,
            stroke="#8a8a8a",
            stroke_width=1.0,
            fill="#ffffff",
        ),
        CircleSlot(
            id="slot.hole.2",
            prompt="",
            cx=340,
            cy=230,
            r=5,
            stroke="#8a8a8a",
            stroke_width=1.0,
            fill="#ffffff",
        ),
        CircleSlot(
            id="slot.hole.3",
            prompt="",
            cx=400,
            cy=230,
            r=5,
            stroke="#8a8a8a",
            stroke_width=1.0,
            fill="#ffffff",
        ),
        CircleSlot(
            id="slot.hole.4",
            prompt="",
            cx=460,
            cy=230,
            r=5,
            stroke="#8a8a8a",
            stroke_width=1.0,
            fill="#ffffff",
        ),
        CircleSlot(
            id="slot.hole.5",
            prompt="",
            cx=525,
            cy=230,
            r=5,
            stroke="#8a8a8a",
            stroke_width=1.0,
            fill="#ffffff",
        ),
        LineSlot(
            id="slot.link.1",
            prompt="",
            x1=275,
            y1=235,
            x2=275,
            y2=270,
            stroke="#ff6bb6",
            stroke_width=2.0,
        ),
        LineSlot(
            id="slot.link.2",
            prompt="",
            x1=340,
            y1=235,
            x2=340,
            y2=270,
            stroke="#ff6bb6",
            stroke_width=2.0,
        ),
        LineSlot(
            id="slot.link.3",
            prompt="",
            x1=400,
            y1=235,
            x2=400,
            y2=270,
            stroke="#ff6bb6",
            stroke_width=2.0,
        ),
        LineSlot(
            id="slot.link.4",
            prompt="",
            x1=460,
            y1=235,
            x2=460,
            y2=270,
            stroke="#ff6bb6",
            stroke_width=2.0,
        ),
        LineSlot(
            id="slot.link.5",
            prompt="",
            x1=525,
            y1=235,
            x2=525,
            y2=270,
            stroke="#ff6bb6",
            stroke_width=2.0,
        ),
        TextSlot(
            id="slot.choice.lb.1",
            prompt="",
            text="A",
            style_role="label",
            x=262,
            y=290,
            font_size=25,
            fill="#111111",
        ),
        TextSlot(
            id="slot.choice.lb.2",
            prompt="",
            text="B",
            style_role="label",
            x=327,
            y=290,
            font_size=25,
            fill="#111111",
        ),
        TextSlot(
            id="slot.choice.lb.3",
            prompt="",
            text="C",
            style_role="label",
            x=387,
            y=290,
            font_size=25,
            fill="#111111",
        ),
        TextSlot(
            id="slot.choice.lb.4",
            prompt="",
            text="D",
            style_role="label",
            x=447,
            y=290,
            font_size=25,
            fill="#111111",
        ),
        TextSlot(
            id="slot.choice.lb.5",
            prompt="",
            text="E",
            style_role="label",
            x=513,
            y=290,
            font_size=25,
            fill="#111111",
        ),
        CircleSlot(
            id="slot.hole.5.copy13",
            prompt="",
            cx=220,
            cy=229.49998474121094,
            r=10,
            stroke="#8a8a8a",
            stroke_width=1,
            fill="#6b7280",
        ),
    )
    diagrams = ()
    groups = ()
    constraints = ()
    return ProblemTemplate(
        id="S3_elem_3_008664",
        title="Choose the hole that makes the largest circle",
        canvas=canvas,
        regions=regions,
        slots=slots,
        diagrams=diagrams,
        groups=groups,
        constraints=constraints,
    )


PROBLEM_TEMPLATE = build_problem_template()

PROBLEM_ID = "S3_elem_3_008664"

SEMANTIC_OVERRIDE = {
    "problem_id": "S3_elem_3_008664",
    "problem_type": "choice_selection",
    "metadata": {
        "language": "ko",
        "question": "Use a pushpin and a strip of paper to draw a circle. Choose the label "
        "of the hole where the pencil should be inserted to draw the largest "
        "circle.",
        "instruction": "Choose the label of the hole.",
        "points": 5,
    },
    "domain": {
        "objects": [
            {"id": "obj.tool", "type": "center_tool"},
            {"id": "obj.hole_positions", "type": "ordered_holes", "count": 5},
            {"id": "obj.choice_labels", "type": "labels", "labels": ["A", "B", "C", "D", "E"]},
        ],
        "relations": [],
        "problem_solving": {
            "understand": {
                "given_refs": ["obj.tool", "obj.hole_positions"],
                "target_ref": "answer.target",
                "condition_refs": ["rel.radius_vs_distance"],
            },
            "plan": {
                "method": "compare_hole_distances",
                "description": "연필심과 중심점 사이의 거리가 가장 큰 구멍을 고른다.",
            },
            "execute": {"expected_operations": ["compare_positions", "select_farthest_hole"]},
            "review": {"check_methods": ["distance_order_check"]},
        },
    },
    "answer": {
        "blanks": [],
        "choices": ["A", "B", "C", "D", "E"],
        "answer_key": ["E"],
        "target": {
            "type": "choice_label",
            "description": "원을 가장 크게 그릴 수 있는 구멍의 기호",
        },
        "value": "E",
        "unit": "",
    },
}

SEMANTIC = SEMANTIC_OVERRIDE

SOLVABLE = {
    "schema": "modu.solvable.v1.1",
    "problem_id": "S3_elem_3_008664",
    "problem_type": "choice_selection",
    "inputs": {
        "total_ticks": 5,
        "target_label": "E",
        "target_ticks": 5,
        "target_count": 1,
        "unit": "",
    },
    "given": [
        {"ref": "obj.hole_positions", "value": {"count": 5, "labels": ["A", "B", "C", "D", "E"]}},
        {"ref": "obj.tool", "value": {"type": "center_tool"}},
    ],
    "target": {"ref": "answer.target", "type": "choice_label"},
    "method": "compare_hole_distances",
    "plan": [
        "Compare the positions of the holes.",
        "Find the hole that is farthest from the pushpin to the pencil lead.",
        "Use the symbol corresponding to that hole as the answer.",
    ],
    "steps": [
        {
            "id": "step.1",
            "expr": "구멍 위치를 왼쪽에서 오른쪽으로 비교한다.",
            "value": "A, B, C, D, E",
        },
        {"id": "step.2", "expr": "가장 멀리 있는 구멍을 고른다.", "value": "E"},
    ],
    "checks": [
        {
            "id": "check.1",
            "expr": "가장 먼 위치가 마지막 구멍인지 확인한다.",
            "expected": "E",
            "actual": "E",
            "pass": True,
        }
    ],
    "answer": {
        "blanks": [],
        "choices": ["A", "B", "C", "D", "E"],
        "answer_key": ["E"],
        "target": {
            "type": "choice_label",
            "description": "원을 가장 크게 그릴 수 있는 구멍의 기호",
        },
        "value": "E",
        "unit": "",
    },
}

SEMANTIC_ANSWER = SOLVABLE.get("answer")
EDITOR_ANSWER_REVIEW = {'mode': 'choice',
 'status': 'verified',
 'note': '',
 'answers': [],
 'choices': [{'id': 'choice.1', 'text': 'A', 'correct': False, 'label': '1', 'sourceRefs': []},
             {'id': 'choice.2', 'text': 'B', 'correct': False, 'label': '2', 'sourceRefs': []},
             {'id': 'choice.3', 'text': 'C', 'correct': False, 'label': '3', 'sourceRefs': []},
             {'id': 'choice.4', 'text': 'D', 'correct': False, 'label': '4', 'sourceRefs': []},
             {'id': 'choice.5', 'text': 'E', 'correct': True, 'label': '5', 'sourceRefs': []}]}
