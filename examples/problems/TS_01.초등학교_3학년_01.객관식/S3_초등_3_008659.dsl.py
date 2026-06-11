from __future__ import annotations

from modu_math.dsl import Canvas, CircleSlot, LineSlot, ProblemTemplate, Region, TextSlot


ANSWER = {
    "blanks": [],
    "choices": [],
    "answer_key": [],
    "target": {"type": "selected_point", "description": "원의 중심"},
    "value": "ㄹ",
    "unit": "",
}


def _grid_slots(prefix: str, *, x: float, y: float, cols: int = 8, rows: int = 8, step: float = 27.0) -> tuple[LineSlot, ...]:
    slots: list[LineSlot] = []
    for i in range(cols + 1):
        gx = x + i * step
        slots.append(
            LineSlot(
                id=f"{prefix}.v{i}",
                prompt="",
                x1=gx,
                y1=y,
                x2=gx,
                y2=y + rows * step,
                stroke="#19BDF2",
                stroke_width=1.1,
                stroke_dasharray="4 3",
            )
        )
    for i in range(rows + 1):
        gy = y + i * step
        slots.append(
            LineSlot(
                id=f"{prefix}.h{i}",
                prompt="",
                x1=x,
                y1=gy,
                x2=x + cols * step,
                y2=gy,
                stroke="#19BDF2",
                stroke_width=1.1,
                stroke_dasharray="4 3",
            )
        )
    return tuple(slots)


def _point(origin_x: float, origin_y: float, step: float, coordinate: tuple[int, int]) -> tuple[float, float]:
    return origin_x + coordinate[0] * step, origin_y + coordinate[1] * step


def _candidate_slots(
    prefix: str,
    *,
    label: str,
    origin_x: float,
    origin_y: float,
    step: float,
    coordinate: tuple[int, int],
    label_dx: float,
    label_dy: float,
) -> tuple[CircleSlot, TextSlot]:
    cx, cy = _point(origin_x, origin_y, step, coordinate)
    return (
        CircleSlot(id=f"{prefix}.point", prompt="", cx=cx, cy=cy, r=4.0, fill="#E91E63", stroke="#E91E63", stroke_width=1.0),
        TextSlot(id=f"{prefix}.label", prompt="", text=label, style_role="label", x=cx + label_dx, y=cy + label_dy, font_size=24),
    )


def build_problem_template() -> ProblemTemplate:
    grid_x, grid_y = 370.0, 56.0
    step = 27.0
    center = (4, 4)
    center_x, center_y = _point(grid_x, grid_y, step, center)

    grid = _grid_slots("slot.grid", x=grid_x, y=grid_y, step=step)
    candidates = (
        *_candidate_slots("slot.pt.giyeok", label="ㄱ", origin_x=grid_x, origin_y=grid_y, step=step, coordinate=(1, 4), label_dx=-18.0, label_dy=18.0),
        *_candidate_slots("slot.pt.nieun", label="ㄴ", origin_x=grid_x, origin_y=grid_y, step=step, coordinate=(2, 3), label_dx=8.0, label_dy=18.0),
        *_candidate_slots("slot.pt.digeut", label="ㄷ", origin_x=grid_x, origin_y=grid_y, step=step, coordinate=(4, 2), label_dx=8.0, label_dy=16.0),
        *_candidate_slots("slot.pt.rieul", label="ㄹ", origin_x=grid_x, origin_y=grid_y, step=step, coordinate=center, label_dx=8.0, label_dy=18.0),
    )

    return ProblemTemplate(
        id="S3_초등_3_008659",
        title="원의 중심 찾기",
        canvas=Canvas(width=640.0, height=420.0, coordinate_mode="logical"),
        regions=(
            Region(id="region.stem", role="stem", flow="absolute", slot_ids=("slot.question",)),
            Region(
                id="region.diagram",
                role="diagram",
                flow="absolute",
                slot_ids=(*(slot.id for slot in grid), "slot.circle", *(slot.id for slot in candidates)),
            ),
            Region(id="region.answer", role="answer", flow="absolute", slot_ids=()),
        ),
        slots=(
            TextSlot(
                id="slot.question",
                prompt="",
                text="그림에서 원의 중심을 선택해 보세요.",
                style_role="question",
                x=72.0,
                y=26.0,
                font_size=26,
            ),
            *grid,
            CircleSlot(
                id="slot.circle",
                prompt="",
                cx=center_x,
                cy=center_y,
                r=3 * step,
                fill="none",
                stroke="#222222",
                stroke_width=1.5,
            ),
            *candidates,
            
        ),
        diagrams=(),
        groups=(),
        constraints=(),
        tags=("geometry", "circle", "center", "grid"),
    )


PROBLEM_TEMPLATE = build_problem_template()

SEMANTIC_OVERRIDE = {
    "problem_id": "S3_초등_3_008659",
    "problem_type": "diagram_choice",
    "metadata": {
        "language": "ko",
        "question": "그림에서 원의 중심을 선택하는 문제",
        "instruction": "그림에서 원의 중심을 고른다.",
    },
    "domain": {
        "objects": [
            {"id": "obj.circle", "type": "circle", "center_ref": "obj.point.rieul", "radius": 3},
            {"id": "obj.point.giyeok", "type": "point", "label": "ㄱ", "coordinate": [1, 4]},
            {"id": "obj.point.nieun", "type": "point", "label": "ㄴ", "coordinate": [2, 3]},
            {"id": "obj.point.digeut", "type": "point", "label": "ㄷ", "coordinate": [4, 2]},
            {"id": "obj.point.rieul", "type": "point", "label": "ㄹ", "coordinate": [4, 4]},
        ],
        "relations": [
            {
                "id": "rel.center_choice",
                "type": "center_of",
                "from_id": "obj.point.rieul",
                "to_id": "obj.circle",
                "description": "ㄹ은 원의 중심이다.",
            }
        ],
        "problem_solving": {
            "understand": {
                "given_refs": ["obj.circle", "obj.point.giyeok", "obj.point.nieun", "obj.point.digeut", "obj.point.rieul"],
                "target_ref": "answer.target",
                "condition_refs": ["rel.center_choice"],
            },
            "plan": {"method": "center_identification", "description": "후보점 중 원의 중심에 놓인 점을 찾는다."},
            "execute": {"expected_operations": ["compare_candidate_points", "select_center_point"]},
            "review": {"check_methods": ["confirm_point_at_circle_center"]},
        },
    },
    "answer": ANSWER,
}

SOLVABLE = {
    "schema": "modu.solvable.v1.1",
    "problem_id": "S3_초등_3_008659",
    "problem_type": "diagram_choice",
    "inputs": {"target_label": "원의 중심", "target_count": 1, "unit": ""},
    "given": [
        {"ref": "obj.circle", "value": {"center": "ㄹ", "radius": 3}},
        {"ref": "obj.point.giyeok", "value": {"label": "ㄱ", "coordinate": [1, 4]}},
        {"ref": "obj.point.nieun", "value": {"label": "ㄴ", "coordinate": [2, 3]}},
        {"ref": "obj.point.digeut", "value": {"label": "ㄷ", "coordinate": [4, 2]}},
        {"ref": "obj.point.rieul", "value": {"label": "ㄹ", "coordinate": [4, 4]}},
    ],
    "target": {"ref": "answer.target", "type": "selected_point"},
    "method": "center_identification",
    "plan": [
        "후보점들의 위치를 비교한다.",
        "원의 가운데에 있는 점을 찾는다.",
        "점 ㄹ을 선택한다.",
    ],
    "steps": [{"id": "step.1", "expr": "원의 중심에 있는 점은 ㄹ", "value": "ㄹ"}],
    "checks": [{"id": "check.1", "expr": "선택한 점이 원의 중심인가", "expected": "ㄹ", "actual": "ㄹ", "pass": True}],
    "answer": ANSWER,
}
