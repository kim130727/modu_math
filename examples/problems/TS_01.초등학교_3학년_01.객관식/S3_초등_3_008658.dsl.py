from __future__ import annotations

from modu_math.dsl import Canvas, CircleSlot, LineSlot, ProblemTemplate, Region, TextSlot


ANSWER = {
    "blanks": [],
    "choices": [],
    "answer_key": [],
    "target": {"type": "selected_points", "description": "컴퍼스의 침을 꽂아야 할 곳"},
    "value": ["ㄱ", "ㄴ", "ㄷ", "ㄹ"],
    "unit": "",
}


def _grid_slots(prefix: str, *, x: float, y: float, cols: int = 10, rows: int = 10, step: float = 34.0) -> tuple[LineSlot, ...]:
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
                stroke_width=1.2,
                stroke_dasharray="5 3",
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
                stroke_width=1.2,
                stroke_dasharray="5 3",
            )
        )
    return tuple(slots)


def _grid_point(origin_x: float, origin_y: float, step: float, point: tuple[int, int]) -> tuple[float, float]:
    return origin_x + point[0] * step, origin_y + point[1] * step


def _candidate_slots(
    prefix: str,
    *,
    label: str,
    origin_x: float,
    origin_y: float,
    step: float,
    point: tuple[int, int],
) -> tuple[CircleSlot, TextSlot]:
    cx, cy = _grid_point(origin_x, origin_y, step, point)
    return (
        CircleSlot(id=f"{prefix}.point", prompt="", cx=cx, cy=cy, r=4.4, fill="#EC1685", stroke="#EC1685", stroke_width=1.0),
        TextSlot(id=f"{prefix}.label", prompt="", text=label, style_role="label", x=cx - 18.0, y=cy - 20.0, font_size=24),
    )


def build_problem_template() -> ProblemTemplate:
    grid_x, grid_y = 304.0, 94.0
    step = 34.0

    grid = _grid_slots("slot.grid", x=grid_x, y=grid_y, step=step)
    circles = (
        CircleSlot(
            id="slot.circle.giyeok",
            prompt="",
            cx=_grid_point(grid_x, grid_y, step, (2, 5))[0],
            cy=_grid_point(grid_x, grid_y, step, (2, 5))[1],
            r=1 * step,
            fill="none",
            stroke="#333333",
            stroke_width=1.5,
        ),
        CircleSlot(
            id="slot.circle.nieun",
            prompt="",
            cx=_grid_point(grid_x, grid_y, step, (3, 5))[0],
            cy=_grid_point(grid_x, grid_y, step, (3, 5))[1],
            r=2 * step,
            fill="none",
            stroke="#333333",
            stroke_width=1.5,
        ),
        CircleSlot(
            id="slot.circle.digeut",
            prompt="",
            cx=_grid_point(grid_x, grid_y, step, (4, 5))[0],
            cy=_grid_point(grid_x, grid_y, step, (4, 5))[1],
            r=3 * step,
            fill="none",
            stroke="#333333",
            stroke_width=1.5,
        ),
        CircleSlot(
            id="slot.circle.rieul",
            prompt="",
            cx=_grid_point(grid_x, grid_y, step, (5, 5))[0],
            cy=_grid_point(grid_x, grid_y, step, (5, 5))[1],
            r=4 * step,
            fill="none",
            stroke="#333333",
            stroke_width=1.5,
        ),
    )
    candidates = (
        *_candidate_slots("slot.pt.giyeok", label="ㄱ", origin_x=grid_x, origin_y=grid_y, step=step, point=(2, 5)),
        *_candidate_slots("slot.pt.nieun", label="ㄴ", origin_x=grid_x, origin_y=grid_y, step=step, point=(3, 5)),
        *_candidate_slots("slot.pt.digeut", label="ㄷ", origin_x=grid_x, origin_y=grid_y, step=step, point=(4, 5)),
        *_candidate_slots("slot.pt.rieul", label="ㄹ", origin_x=grid_x, origin_y=grid_y, step=step, point=(5, 5)),
        *_candidate_slots("slot.pt.mieum", label="ㅁ", origin_x=grid_x, origin_y=grid_y, step=step, point=(6, 5)),
        *_candidate_slots("slot.pt.bieup", label="ㅂ", origin_x=grid_x, origin_y=grid_y, step=step, point=(7, 5)),
    )

    return ProblemTemplate(
        id="S3_초등_3_008658",
        title="컴퍼스의 침을 꽂아야 할 곳",
        canvas=Canvas(width=920, height=560, coordinate_mode="logical"),
        regions=(
            Region(id="region.stem", role="stem", flow="absolute", slot_ids=("slot.q1", )),
            Region(
                id="region.diagram",
                role="diagram",
                flow="absolute",
                slot_ids=(*(slot.id for slot in grid), *(slot.id for slot in circles), *(slot.id for slot in candidates)),
            ),
            Region(id="region.answer", role="answer", flow="absolute", slot_ids=()),
        ),
        slots=(
            TextSlot(
                id="slot.q1",
                prompt="",
                text = '\n    \n    주어진 모양을 그리기 위하여 컴퍼스의 침을 꽂아야 할 곳을 모두\n    선택해보세요  \n  ', style_role="question",
                x = 95, y = 15, font_size = 25),
            *grid,
            *circles,
            *candidates,
            
        ),
        diagrams=(),
        groups=(),
        constraints=(),
        tags=("geometry", "circle", "compass", "grid", "center"),
    )


PROBLEM_TEMPLATE = build_problem_template()

SEMANTIC_OVERRIDE = {
    "problem_id": "S3_초등_3_008658",
    "problem_type": "geometry_compass_centers",
    "metadata": {
        "language": "ko",
        "question": "주어진 모양을 그리기 위하여 컴퍼스의 침을 꽂아야 할 곳을 모두 선택하는 문제",
        "instruction": "컴퍼스의 침을 꽂아야 할 곳을 모두 선택한다.",
    },
    "domain": {
        "objects": [
            {"id": "obj.point.giyeok", "type": "point", "label": "ㄱ", "coordinate": [2, 5]},
            {"id": "obj.point.nieun", "type": "point", "label": "ㄴ", "coordinate": [3, 5]},
            {"id": "obj.point.digeut", "type": "point", "label": "ㄷ", "coordinate": [4, 5]},
            {"id": "obj.point.rieul", "type": "point", "label": "ㄹ", "coordinate": [5, 5]},
            {"id": "obj.point.mieum", "type": "point", "label": "ㅁ", "coordinate": [6, 5]},
            {"id": "obj.point.bieup", "type": "point", "label": "ㅂ", "coordinate": [7, 5]},
            {"id": "obj.circle.1", "type": "circle", "center_ref": "obj.point.giyeok", "radius": 1},
            {"id": "obj.circle.2", "type": "circle", "center_ref": "obj.point.nieun", "radius": 2},
            {"id": "obj.circle.3", "type": "circle", "center_ref": "obj.point.digeut", "radius": 3},
            {"id": "obj.circle.4", "type": "circle", "center_ref": "obj.point.rieul", "radius": 4},
        ],
        "relations": [
            {
                "id": "rel.circle1.center",
                "type": "center_of",
                "from_id": "obj.point.giyeok",
                "to_id": "obj.circle.1",
                "description": "ㄱ은 반지름 1칸인 원의 중심이다.",
            },
            {
                "id": "rel.circle2.center",
                "type": "center_of",
                "from_id": "obj.point.nieun",
                "to_id": "obj.circle.2",
                "description": "ㄴ은 반지름 2칸인 원의 중심이다.",
            },
            {
                "id": "rel.circle3.center",
                "type": "center_of",
                "from_id": "obj.point.digeut",
                "to_id": "obj.circle.3",
                "description": "ㄷ은 반지름 3칸인 원의 중심이다.",
            },
            {
                "id": "rel.circle4.center",
                "type": "center_of",
                "from_id": "obj.point.rieul",
                "to_id": "obj.circle.4",
                "description": "ㄹ은 반지름 4칸인 원의 중심이다.",
            },
        ],
        "problem_solving": {
            "understand": {
                "given_refs": [
                    "obj.point.giyeok",
                    "obj.point.nieun",
                    "obj.point.digeut",
                    "obj.point.rieul",
                    "obj.point.mieum",
                    "obj.point.bieup",
                ],
                "target_ref": "answer.target",
                "condition_refs": ["rel.circle1.center", "rel.circle2.center", "rel.circle3.center", "rel.circle4.center"],
            },
            "plan": {"method": "center_matching", "description": "각 원의 중심에 해당하는 후보점을 찾는다."},
            "execute": {"expected_operations": ["identify_circle_centers", "select_all_center_points"]},
            "review": {"check_methods": ["count_selected_points", "verify_point_labels"]},
        },
    },
    "answer": ANSWER,
}

SOLVABLE = {
    "schema": "modu.solvable.v1.1",
    "problem_id": "S3_초등_3_008658",
    "problem_type": "geometry_compass_centers",
    "inputs": {
        "target_label": "컴퍼스의 침을 꽂아야 할 곳",
        "target_count": 4,
        "unit": "",
    },
    "given": [
        {"ref": "obj.point.giyeok", "value": {"label": "ㄱ", "coordinate": [2, 5], "circle_radius": 1}},
        {"ref": "obj.point.nieun", "value": {"label": "ㄴ", "coordinate": [3, 5], "circle_radius": 2}},
        {"ref": "obj.point.digeut", "value": {"label": "ㄷ", "coordinate": [4, 5], "circle_radius": 3}},
        {"ref": "obj.point.rieul", "value": {"label": "ㄹ", "coordinate": [5, 5], "circle_radius": 4}},
        {"ref": "obj.point.mieum", "value": {"label": "ㅁ", "coordinate": [6, 5], "circle_radius": None}},
        {"ref": "obj.point.bieup", "value": {"label": "ㅂ", "coordinate": [7, 5], "circle_radius": None}},
    ],
    "target": {"ref": "answer.target", "type": "selected_points"},
    "method": "center_matching",
    "plan": [
        "각 원의 중심을 확인한다.",
        "원 중심에 해당하는 후보점의 이름을 찾는다.",
        "ㄱ, ㄴ, ㄷ, ㄹ을 모두 선택한다.",
    ],
    "steps": [
        {"id": "step.1", "expr": "반지름 1 원의 중심은 ㄱ (2,5)", "value": "ㄱ"},
        {"id": "step.2", "expr": "반지름 2 원의 중심은 ㄴ (3,5)", "value": "ㄴ"},
        {"id": "step.3", "expr": "반지름 3 원의 중심은 ㄷ (4,5)", "value": "ㄷ"},
        {"id": "step.4", "expr": "반지름 4 원의 중심은 ㄹ (5,5)", "value": "ㄹ"},
    ],
    "checks": [
        {"id": "check.1", "expr": "선택한 점의 수", "expected": 4, "actual": 4, "pass": True},
        {"id": "check.2", "expr": "선택한 점", "expected": ["ㄱ", "ㄴ", "ㄷ", "ㄹ"], "actual": ["ㄱ", "ㄴ", "ㄷ", "ㄹ"], "pass": True},
    ],
    "answer": ANSWER,
}
