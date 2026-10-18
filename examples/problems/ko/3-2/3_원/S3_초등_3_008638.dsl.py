from __future__ import annotations
from modu_math.dsl import (
    Canvas,
    CircleSlot,
    LineSlot,
    ProblemTemplate,
    Region,
    TextSlot,
)


def _grid_slots(prefix: str, x0: float, y0: float, cell: float, cols: int, rows: int):
    slots = []
    width = cell * cols
    height = cell * rows
    for i in range(cols + 1):
        x = x0 + cell * i
        slots.append(
            LineSlot(
                id=f"{prefix}.v{i}",
                prompt="",
                x1=x,
                y1=y0,
                x2=x,
                y2=y0 + height,
                stroke="#5FCBFF",
                stroke_width=1.2,
                stroke_dasharray="5 3",
            )
        )
    for j in range(rows + 1):
        y = y0 + cell * j
        slots.append(
            LineSlot(
                id=f"{prefix}.h{j}",
                prompt="",
                x1=x0,
                y1=y,
                x2=x0 + width,
                y2=y,
                stroke="#5FCBFF",
                stroke_width=1.2,
                stroke_dasharray="5 3",
            )
        )
    return slots


def build_problem_template() -> ProblemTemplate:
    slots = [
        TextSlot(
            id="slot.qtext",
            prompt="",
            text='원의 중심을 찾아 선택해 보세요.',
            style_role="question",
            x=105,
            y=70,
            font_size=30,
            fill='#111111',
        ),
    ]
    slots.extend(
        _grid_slots(
            prefix="slot.top.grid", x0=200.0, y0=100.0, cell=24.0, cols=8, rows=8
        )
    )
    slots.extend(
        [
            CircleSlot(
                id="slot.top.circle",
                prompt="",
                cx=295,
                cy=195,
                r=70,
                fill="none",
                stroke="#333333",
                stroke_width=1.8,
            ),
            CircleSlot(
                id="slot.top.pt.ga",
                prompt="",
                cx=297,
                cy=196,
                r=5,
                fill="#ff3aa8",
                stroke="#111111",
                stroke_width=2,
            ),
            CircleSlot(
                id="slot.top.pt.na",
                prompt="",
                cx=345,
                cy=197,
                r=5,
                fill="#ff3aa8",
                stroke="#111111",
                stroke_width=2,
            ),
            CircleSlot(
                id="slot.top.pt.da",
                prompt="",
                cx=297,
                cy=244,
                r=5,
                fill="#ff3aa8",
                stroke="#111111",
                stroke_width=2,
            ),
            TextSlot(
                id="slot.top.lb.ga",
                prompt="",
                text='ㄱ',
                style_role="label",
                x=265,
                y=190,
                font_size=25,
            ),
            TextSlot(
                id="slot.top.lb.na",
                prompt="",
                text='ㄴ',
                style_role="label",
                x=320,
                y=190,
                font_size=25,
            ),
            TextSlot(
                id="slot.top.lb.da",
                prompt="",
                text='ㄷ',
                style_role="label",
                x=300,
                y=240,
                font_size=25,
            ),
        ]
    )
    
    return ProblemTemplate(
        id="S3_초등_3_008638",
        title="원의 중심 찾기",
        canvas=Canvas(width=600.0, height=400.0, coordinate_mode="logical"),
        regions=(
            Region(
                id="region.stem",
                role="stem",
                flow="absolute",
                slot_ids=("slot.qtext",),
            ),
            Region(
                id="region.diagram.top",
                role="diagram",
                flow="absolute",
                slot_ids=tuple((s.id for s in slots if s.id.startswith("slot.top."))),
            ),
            Region(id="region.answer", role="answer", flow="absolute", slot_ids=()),
            Region(id="region.explain", role="explain", flow="absolute", slot_ids=()),
        ),
        slots=tuple(slots),
        diagrams=(),
        groups=(),
        constraints=(),
        tags=(),
    )


PROBLEM_TEMPLATE = build_problem_template()

SEMANTIC_OVERRIDE = {
    "problem_id": "S3_초등_3_008638",
    "problem_type": "도형_원의중심_선택",
    "metadata": {
        "language": "ko",
        "question": "원의 중심을 찾아 선택해 보세요.",
        "instruction": "정답을 선택한다.",
    },
    "domain": {
        "objects": [
            {"id": "obj.circle", "type": "circle"},
            {"id": "obj.point.ga", "type": "point", "label": "ㄱ"},
            {"id": "obj.point.na", "type": "point", "label": "ㄴ"},
            {"id": "obj.point.da", "type": "point", "label": "ㄷ"},
        ],
        "relations": [],
        "problem_solving": {
            "understand": {
                "given_refs": [
                    "obj.circle",
                    "obj.point.ga",
                    "obj.point.na",
                    "obj.point.da",
                ],
                "target_ref": "answer.target",
                "condition_refs": ["rel.center_candidate"],
            },
            "plan": {
                "method": "도형식별",
                "description": "원의 안쪽 점들 중 중심의 성질에 맞는 점을 찾는다.",
            },
            "execute": {"expected_operations": ["center_candidate_selection"]},
            "review": {"check_methods": ["center_is_inside_circle"]},
        },
    },
    "answer": {
        "blanks": [],
        "choices": ["ㄱ", "ㄴ", "ㄷ"],
        "answer_key": ["ㄱ"],
        "target": {
            "type": "selected_point_label",
            "description": "원의 중심으로 선택할 점의 라벨",
        },
        "value": "ㄱ",
        "unit": "",
    },
}

SOLVABLE = {
    "schema": "modu.solvable.v1.1",
    "problem_id": "S3_초등_3_008638",
    "problem_type": "도형_원의중심_선택",
    "inputs": {
        "total_ticks": 0,
        "target_label": "원의 중심",
        "target_ticks": 0,
        "target_count": 1,
        "unit": "",
    },
    "given": [
        {"ref": "obj.circle", "value": "circle"},
        {"ref": "obj.point.ga", "value": {"label": "ㄱ", "type": "point"}},
        {"ref": "obj.point.na", "value": {"label": "ㄴ", "type": "point"}},
        {"ref": "obj.point.da", "value": {"label": "ㄷ", "type": "point"}},
    ],
    "target": {"ref": "answer.target", "type": "selected_point_label"},
    "method": "도형식별",
    "plan": ["주어진 점들 중 원의 중심 위치에 해당하는 점을 고른다."],
    "steps": [{"id": "step.1", "expr": "중심 후보 점 선택", "value": "ㄱ"}],
    "checks": [
        {
            "id": "check.1",
            "expr": "점 ㄱ이 원의 중심인가",
            "expected": True,
            "actual": True,
            "pass": True,
        }
    ],
    "answer": {
        "blanks": [],
        "choices": ["ㄱ", "ㄴ", "ㄷ"],
        "answer_key": ["ㄱ"],
        "target": {
            "type": "selected_point_label",
            "description": "원의 중심으로 선택할 점의 라벨",
        },
        "value": "ㄱ",
        "unit": "",
    },
}
