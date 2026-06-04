from __future__ import annotations
from modu_math.dsl import (
    Canvas,
    ProblemTemplate,
    Region,
    TextSlot,
    RectSlot,
    LineSlot,
    CircleSlot,
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
            id="slot.qnum",
            prompt="",
            text="10.",
            style_role="question",
            x=26.0,
            y=18.0,
            font_size=28,
        ),
        TextSlot(
            id="slot.qtext",
            prompt="",
            text="원의 중심을 찾아 선택해 보세요.",
            style_role="question",
            x=74.0,
            y=18.0,
            font_size=28,
        ),
        RectSlot(
            id="slot.answer_blank",
            prompt="",
            x=72.0,
            y=269.0,
            width=22.0,
            height=22.0,
            fill="none",
            stroke="none",
        ),
    ]
    slots.extend(
        _grid_slots(
            prefix="slot.top.grid", x0=370.0, y0=40.0, cell=24.0, cols=8, rows=8
        )
    )
    slots.extend(
        [
            CircleSlot(
                id="slot.top.circle",
                prompt="",
                cx=466.0,
                cy=136.0,
                r=78.0,
                fill="none",
                stroke="#333333",
                stroke_width=1.8,
            ),
            CircleSlot(
                id="slot.top.pt.ga",
                prompt="",
                cx=430.0,
                cy=138.0,
                r=3.5,
                fill="#ff3aa8",
            ),
            CircleSlot(
                id="slot.top.pt.na",
                prompt="",
                cx=490.0,
                cy=138.0,
                r=3.5,
                fill="#ff3aa8",
            ),
            CircleSlot(
                id="slot.top.pt.da",
                prompt="",
                cx=430.0,
                cy=196.0,
                r=3.5,
                fill="#ff3aa8",
            ),
            TextSlot(
                id="slot.top.lb.ga",
                prompt="",
                text="가",
                style_role="label",
                x=414.0,
                y=127.0,
                font_size=24,
            ),
            TextSlot(
                id="slot.top.lb.na",
                prompt="",
                text="나",
                style_role="label",
                x=474.0,
                y=127.0,
                font_size=24,
            ),
            TextSlot(
                id="slot.top.lb.da",
                prompt="",
                text="다",
                style_role="label",
                x=414.0,
                y=189.0,
                font_size=24,
            ),
        ]
    )
    slots.extend(
        _grid_slots(
            prefix="slot.bottom.grid", x0=36.0, y0=382.0, cell=24.0, cols=8, rows=8
        )
    )
    slots.extend(
        [
            CircleSlot(
                id="slot.bottom.circle",
                prompt="",
                cx=132.0,
                cy=478.0,
                r=78.0,
                fill="none",
                stroke="#333333",
                stroke_width=1.8,
            ),
            CircleSlot(
                id="slot.bottom.pt.ga",
                prompt="",
                cx=96.0,
                cy=480.0,
                r=3.5,
                fill="#ff3aa8",
            ),
            CircleSlot(
                id="slot.bottom.pt.na",
                prompt="",
                cx=156.0,
                cy=480.0,
                r=3.5,
                fill="#ff3aa8",
            ),
            CircleSlot(
                id="slot.bottom.pt.da",
                prompt="",
                cx=96.0,
                cy=538.0,
                r=3.5,
                fill="#ff3aa8",
            ),
            CircleSlot(
                id="slot.bottom.center_hint",
                prompt="",
                cx=132.0,
                cy=480.0,
                r=16.0,
                fill="none",
                stroke="#b9b9b9",
                stroke_width=1.2,
            ),
            TextSlot(
                id="slot.bottom.lb.ga",
                prompt="",
                text="가",
                style_role="label",
                x=80.0,
                y=469.0,
                font_size=24,
            ),
            TextSlot(
                id="slot.bottom.lb.na",
                prompt="",
                text="나",
                style_role="label",
                x=140.0,
                y=469.0,
                font_size=24,
            ),
            TextSlot(
                id="slot.bottom.lb.da",
                prompt="",
                text="다",
                style_role="label",
                x=80.0,
                y=531.0,
                font_size=24,
            ),
        ]
    )
    slots.extend([
        TextSlot(
            id="slot.ans_label",
            prompt="",
            text="(정답)",
            style_role="supporting",
            x=26.0,
            y=620.0,
            font_size=22,
        ),
        TextSlot(
            id="slot.exp",
            prompt="",
            text="(해설) 원의 중심은 원을 그릴 때 누름 못이 꽂혔던 점으로 한 원에는 원의 중심이 1개 있습니다.",
            style_role="supporting",
            x=26.0,
            y=660.0,
            font_size=20,
        ),
    ])
    return ProblemTemplate(
        id="S3_초등_3_008638",
        title="원의 중심 찾기",
        canvas=Canvas(width=939.0, height=700.0, coordinate_mode="logical"),
        regions=(
            Region(
                id="region.stem",
                role="stem",
                flow="absolute",
                slot_ids=("slot.qnum", "slot.qtext"),
            ),
            Region(
                id="region.answer",
                role="answer",
                flow="absolute",
                slot_ids=("slot.answer_blank",),
            ),
            Region(id="region.explain", role="explain", flow="absolute", slot_ids=("slot.ans_label", "slot.exp")),
            Region(
                id="region.diagram.top",
                role="diagram",
                flow="absolute",
                slot_ids=tuple((s.id for s in slots if s.id.startswith("slot.top."))),
            ),
            Region(
                id="region.diagram.bottom",
                role="diagram",
                flow="absolute",
                slot_ids=tuple(
                    (s.id for s in slots if s.id.startswith("slot.bottom."))
                ),
            ),
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
        "instruction": "(정답)",
    },
    "domain": {
        "objects": [
            {"id": "obj.circle", "type": "circle"},
            {"id": "obj.point.ga", "type": "point", "label": "가"},
            {"id": "obj.point.na", "type": "point", "label": "나"},
            {"id": "obj.point.da", "type": "point", "label": "다"},
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
        "choices": [],
        "answer_key": [],
        "target": {
            "type": "selected_point_label",
            "description": "원의 중심으로 선택할 점의 라벨",
        },
        "value": 0,
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
        {"ref": "obj.circle", "value": {"type": "circle"}},
        {"ref": "obj.point.ga", "value": {"label": "가"}},
        {"ref": "obj.point.na", "value": {"label": "나"}},
        {"ref": "obj.point.da", "value": {"label": "다"}},
    ],
    "target": {"ref": "answer.target", "type": "selected_point_label"},
    "method": "도형식별",
    "plan": [
        "원의 중심의 성질을 확인한다.",
        "세 점 중 원의 중심에 해당하는 점을 찾는다.",
    ],
    "steps": [
        {
            "id": "step.1",
            "expr": "원의 내부 점들 중 중심 후보를 확인한다.",
            "value": "가/나/다 중 하나",
        },
        {"id": "step.2", "expr": "중심의 위치 성질과 비교한다.", "value": "TODO"},
    ],
    "checks": [
        {
            "id": "check.1",
            "expr": "중심은 원의 내부에 있고 원의 가운데에 위치한다.",
            "expected": True,
            "actual": True,
            "pass": True,
        }
    ],
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {
            "type": "selected_point_label",
            "description": "원의 중심으로 선택할 점의 라벨",
        },
        "value": 0,
        "unit": "",
    },
}
