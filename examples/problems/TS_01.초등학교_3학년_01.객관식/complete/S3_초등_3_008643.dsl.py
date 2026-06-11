from __future__ import annotations
from modu_math.dsl import (
    Canvas,
    CircleSlot,
    LineSlot,
    ProblemTemplate,
    RectSlot,
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
            text = '원의 중심을 찾아 선택해 보세요.', style_role="question",
            x = 105, y = 70, font_size = 30, fill = '#111111'),
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
            prefix="slot.top.grid", x0=200.0, y0=100.0, cell=24.0, cols=8, rows=8
        )
    )
    slots.extend(
        [
            CircleSlot(
                id="slot.top.circle",
                prompt="",
                cx = 295, cy = 195, r = 70, fill="none",
                stroke="#333333",
                stroke_width=1.8,
            ),
            CircleSlot(
                id="slot.top.pt.ga",
                prompt="",
                cx = 297, cy = 196, r = 5, fill="#ff3aa8",
            ),
            CircleSlot(
                id="slot.top.pt.na",
                prompt="",
                cx = 345, cy = 197, r = 5, fill="#ff3aa8",
            ),
            CircleSlot(
                id="slot.top.pt.da",
                prompt="",
                cx = 344, cy = 243, r = 5, fill="#ff3aa8",
            ),
            CircleSlot(
                id="slot.top.pt.db",
                prompt="",
                cx = 249, cy = 245, r = 5, fill = '#ff3aa8', stroke = '#111111', stroke_width = 2),
            CircleSlot(
                id="slot.top.pt.dc",
                prompt="",
                cx = 297, cy = 125, r = 5, fill="#ff3aa8",
            ),
            TextSlot(
                id="slot.top.lb.ga",
                prompt="",
                text = 'ㄱ', style_role="label",
                x = 270, y = 125, font_size = 25),
            TextSlot(
                id="slot.top.lb.na",
                prompt="",
                text = 'ㄴ', style_role="label",
                x = 270, y = 190, font_size = 25),
            TextSlot(
                id="slot.top.lb.da",
                prompt="",
                text = 'ㄷ', style_role="label",
                x = 320, y = 190, font_size = 25, fill = '#111111'),
        ]
    )
    
    return ProblemTemplate(
        id="S3_초등_3_008643",
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
                id="region.answer",
                role="answer",
                flow="absolute",
                slot_ids=("slot.answer_blank",),
            ),
            Region(id="region.explain", role="explain", flow="absolute", slot_ids=( )),
            Region(
                id="region.diagram.top",
                role="diagram",
                flow="absolute",
                slot_ids=(
                    *(s.id for s in slots if s.id.startswith("slot.top.")),
                    "slot.top.lb.na.copy1",
                    "slot.top.lb.na.copy2",
                ),
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
        slots=(
            *slots,
            TextSlot(
                id="slot.top.lb.na.copy1",
                prompt="",
                text = 'ㄹ', x = 225, y = 265, font_size = 25, fill="#111111",
            ),
            TextSlot(
                id="slot.top.lb.na.copy2",
                prompt="",
                text = 'ㅁ', x = 345, y = 265, font_size = 25, fill="#111111",
            ),
        ),
        diagrams=(),
        groups=(),
        constraints=(),
        tags=(),
    )


PROBLEM_TEMPLATE = build_problem_template()

SEMANTIC_OVERRIDE = {
    "problem_id": "S3_초등_3_008643",
    "problem_type": "geometry_circle_center",
    "metadata": {
        "language": "ko",
        "question": "원의 중심을 찾아 선택해 보세요.",
        "instruction": "정답을 선택한다.",
        "points": 0,
    },
    "domain": {
        "objects": [
            {"id": "obj.circle", "type": "circle"},
            {"id": "obj.center_candidate", "type": "point", "label": "ㄴ"},
            {
                "id": "obj.points_on_figure",
                "type": "point_set",
                "labels": ["ㄱ", "ㄷ", "ㄹ", "ㅁ"],
            },
        ],
        "relations": [],
        "problem_solving": {
            "understand": {
                "given_refs": ["obj.circle", "obj.points_on_figure"],
                "target_ref": "answer.target",
                "condition_refs": ["rel.center_property"],
            },
            "plan": {
                "method": "circle_center_identification",
                "description": "원 위의 점들과 같은 거리를 가지는 중심 후보를 찾는다.",
            },
            "execute": {
                "expected_operations": [
                    "identify_center_candidate",
                    "match_visual_center",
                ]
            },
            "review": {"check_methods": ["center_property_check"]},
        },
    },
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {"type": "selected_point", "description": "원의 중심"},
        "value": "ㄴ",
        "unit": "",
    },
}

SOLVABLE = {
    "schema": "modu.solvable.v1.1",
    "problem_id": "S3_초등_3_008643",
    "problem_type": "geometry_circle_center",
    "inputs": {
        "total_ticks": 0,
        "target_label": "원의 중심",
        "target_ticks": 0,
        "target_count": 1,
        "unit": "",
    },
    "given": [
        {"ref": "obj.circle", "value": "circle"},
        {"ref": "obj.points_on_figure", "value": ["ㄱ", "ㄷ", "ㄹ", "ㅁ"]},
    ],
    "target": {"ref": "answer.target", "type": "selected_point"},
    "method": "circle_center_identification",
    "plan": [
        "원의 중심과 원 위의 점 사이의 거리가 같다는 성질을 이용한다.",
        "그림에서 중심처럼 보이는 점을 찾는다.",
    ],
    "steps": [{"id": "step.1", "expr": "원의 중심 후보를 찾는다", "value": "ㄴ"}],
    "checks": [
        {
            "id": "check.1",
            "expr": "원의 중심은 원 위의 점들과 같은 거리를 가져야 한다",
            "expected": True,
            "actual": True,
            "pass": True,
        }
    ],
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {"type": "selected_point", "description": "원의 중심"},
        "value": "ㄴ",
        "unit": "",
    },
}
