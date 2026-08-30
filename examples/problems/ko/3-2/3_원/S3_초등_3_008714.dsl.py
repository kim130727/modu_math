from __future__ import annotations
from modu_math.dsl import (
    Canvas,
    CircleSlot,
    PolygonSlot,
    ProblemTemplate,
    RectSlot,
    Region,
    TextSlot,
)


def build_problem_template() -> ProblemTemplate:
    return ProblemTemplate(
        id="S3_초등_3_008714",
        title="원의 중심",
        canvas=Canvas(width=720, height=420, coordinate_mode="logical"),
        regions=(
            Region(
                id="region.stem",
                role="stem",
                flow="absolute",
                slot_ids=("slot.header.text",),
            ),
            Region(
                id="region.diagram",
                role="diagram",
                flow="absolute",
                slot_ids=(
                    "slot.circle.outer",
                    "slot.tool.strip",
                    "slot.hole.1",
                    "slot.hole.2",
                    "slot.hole.3",
                    "slot.hole.4",
                    "slot.pin.base",
                    "slot.pin.dot",
                    "slot.pencil.body",
                    "slot.pencil.tip",
                    "slot.pencil.lead",
                    "slot.pencil.eraser",
                ),
            ),
            Region(
                id="region.choice",
                role="choice",
                flow="absolute",
                slot_ids=("slot.choice",),
            ),
            Region(id="region.answer", role="answer", flow="absolute", slot_ids=()),
        ),
        slots=(
            TextSlot(
                id="slot.header.text",
                prompt="",
                text="그림과 같이 띠 종이를 이용하여 원을 그릴 때, 누름 못이 꽂혔던 점을 무엇이라고 할까요?",
                style_role="question",
                x=35,
                y=35,
                font_size=26,
            ),
            # Circle: Center at (320, 210), radius = 90
            CircleSlot(
                id="slot.circle.outer",
                prompt="",
                cx=320,
                cy=210,
                r=90,
                fill="none",
                stroke="#111111",
                stroke_width=2,
            ),
            # Strip of paper (띠 종이)
            RectSlot(
                id="slot.tool.strip",
                prompt="",
                x=305,
                y=198,
                width=135,
                height=24,
                rx=4,
                ry=4,
                fill="#f0f9ff",
                stroke="#0284c7",
                stroke_width=1.5,
            ),
            # Thumbtack / Pin (누름 못) at center (320, 210)
            CircleSlot(
                id="slot.pin.base",
                prompt="",
                cx=320,
                cy=210,
                r=6,
                fill="#64748b",
                stroke="#334155",
                stroke_width=1.5,
            ),
            CircleSlot(
                id="slot.pin.dot",
                prompt="",
                cx=320,
                cy=210,
                r=2.5,
                fill="#0f172a",
            ),
            # Strip hole dots
            CircleSlot(
                id="slot.hole.1",
                prompt="",
                cx=345,
                cy=210,
                r=2.5,
                fill="#334155",
            ),
            CircleSlot(
                id="slot.hole.2",
                prompt="",
                cx=370,
                cy=210,
                r=2.5,
                fill="#334155",
            ),
            CircleSlot(
                id="slot.hole.3",
                prompt="",
                cx=395,
                cy=210,
                r=2.5,
                fill="#334155",
            ),
            CircleSlot(
                id="slot.hole.4",
                prompt="",
                cx=410,
                cy=210,
                r=3,
                fill="#334155",
            ),
            # Pencil (연필): inserted at (410, 210), pointing up-right to (435, 140)
            PolygonSlot(
                id="slot.pencil.body",
                prompt="",
                points=[[411, 195], [419, 198], [435, 151], [428, 148]],
                fill="#fb7185",
                stroke="#e11d48",
                stroke_width=1,
            ),
            PolygonSlot(
                id="slot.pencil.tip",
                prompt="",
                points=[[410, 210], [411, 195], [419, 198]],
                fill="#fed7aa",
                stroke="#ea580c",
                stroke_width=1,
            ),
            PolygonSlot(
                id="slot.pencil.lead",
                prompt="",
                points=[[410, 210], [410.5, 204], [413, 205]],
                fill="#1e293b",
                stroke="#0f172a",
                stroke_width=1,
            ),
            PolygonSlot(
                id="slot.pencil.eraser",
                prompt="",
                points=[[428, 148], [435, 151], [439, 142], [431, 139]],
                fill="#d97706",
                stroke="#92400e",
                stroke_width=1,
            ),
            TextSlot(
                id="slot.choice",
                prompt="",
                text="원의 ( 중심 , 반지름 , 지름 )",
                style_role="question",
                x=180,
                y=365,
                font_size=28,
            ),
        ),
        diagrams=(),
        groups=(),
        constraints=(),
        tags=(),
    )


PROBLEM_TEMPLATE = build_problem_template()

SEMANTIC_OVERRIDE = {
    "problem_id": "S3_초등_3_008714",
    "problem_type": "term_selection",
    "metadata": {
        "language": "ko",
        "question": "그림과 같이 띠 종이를 이용하여 원을 그릴 때, 누름 못이 꽂혔던 점을 무엇이라고 할까요?",
        "instruction": "그림을 보고 알맞은 용어를 고르기",
    },
    "domain": {
        "objects": [
            {"id": "obj.circle", "type": "circle"},
            {"id": "obj.point", "type": "point", "role": "pinpoint"},
            {"id": "obj.terms", "type": "term_set", "items": ["중심", "반지름", "지름"]},
        ],
        "relations": [],
        "problem_solving": {
            "understand": {
                "given_refs": ["obj.circle", "obj.point", "obj.terms"],
                "target_ref": "answer.target",
                "condition_refs": ["rel.point_of_circle"],
            },
            "plan": {
                "method": "term_identification",
                "description": "그림 속 누름 못이 꽂힌 점과 원의 용어를 대응시킨다.",
            },
            "execute": {"expected_operations": ["identify_center_point"]},
            "review": {"check_methods": ["definition_check"]},
        },
    },
    "answer": {
        "blanks": [],
        "choices": ["중심", "반지름", "지름"],
        "answer_key": ["중심"],
        "target": {"type": "term", "description": "누름 못이 꽂혔던 점의 이름"},
        "value": "중심",
        "unit": "",
    },
}

SOLVABLE = {
    "schema": "modu.solvable.v1.1",
    "problem_id": "S3_초등_3_008714",
    "problem_type": "term_selection",
    "inputs": {
        "total_ticks": 3,
        "target_label": "누름 못이 꽂혔던 점의 이름",
        "target_ticks": 1,
        "target_count": 1,
        "unit": "",
    },
    "given": [
        {"ref": "obj.circle", "value": {"type": "circle"}},
        {"ref": "obj.point", "value": {"role": "pinpoint"}},
        {"ref": "obj.terms", "value": {"items": ["중심", "반지름", "지름"]}},
    ],
    "target": {"ref": "answer.target", "type": "term"},
    "plan": ["그림 속 누름 못이 꽂힌 점의 용어를 해설과 대응시켜 찾는다."],
    "method": "term_identification",
    "steps": [
        {
            "id": "step.1",
            "expr": "그림의 누름 못이 꽂힌 점은 원의 중심이다.",
            "value": "중심",
        }
    ],
    "checks": [
        {
            "id": "check.1",
            "expr": "누름 못이 꽂힌 점이 중심인가",
            "expected": "중심",
            "actual": "중심",
            "pass": True,
        }
    ],
    "answer": {
        "blanks": [],
        "choices": ["중심", "반지름", "지름"],
        "answer_key": ["중심"],
        "target": {"type": "term", "description": "누름 못이 꽂혔던 점의 이름"},
        "value": "중심",
        "unit": "",
    },
}
