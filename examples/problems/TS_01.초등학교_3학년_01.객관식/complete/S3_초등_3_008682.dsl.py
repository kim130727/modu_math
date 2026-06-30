from __future__ import annotations

from modu_math.dsl import (
    Canvas,
    CircleSlot,
    PathSlot,
    ProblemTemplate,
    Region,
    TextSlot,
    SpeakerSpec,
    speaker_group_slot_ids,
    speaker_group_slots,
)

GRID_COLOR = "#37C7FF"
GRID_SIZE = 192.0
GRID_CELLS = 8
GRID_STEP = GRID_SIZE / GRID_CELLS


ANSWER = {
    "blanks": [],
    "choices": [],
    "answer_key": [],
    "target": {"type": "selected_term", "description": "지름과 반지름 중 알맞은 말"},
    "value": "지름",
    "unit": "",
}


def _grid_slots(prefix: str, *, x: float, y: float) -> tuple[PathSlot, ...]:
    slots: list[PathSlot] = [
        PathSlot(
            id=f"{prefix}.frame",
            prompt="",
            d=f"M {x} {y} L {x + GRID_SIZE} {y} L {x + GRID_SIZE} {y + GRID_SIZE} L {x} {y + GRID_SIZE} Z",
            stroke=GRID_COLOR,
            stroke_width=1.4,
            stroke_dasharray="4 3",
            fill="#ffffff",
        )
    ]
    for i in range(1, GRID_CELLS):
        gx = x + i * GRID_STEP
        gy = y + i * GRID_STEP
        slots.extend(
            (
                PathSlot(
                    id=f"{prefix}.v{i}",
                    prompt="",
                    d=f"M {gx:.1f} {y} L {gx:.1f} {y + GRID_SIZE}",
                    stroke=GRID_COLOR,
                    stroke_width=1.0,
                    stroke_dasharray="4 3",
                    fill="none",
                ),
                PathSlot(
                    id=f"{prefix}.h{i}",
                    prompt="",
                    d=f"M {x} {gy:.1f} L {x + GRID_SIZE} {gy:.1f}",
                    stroke=GRID_COLOR,
                    stroke_width=1.0,
                    stroke_dasharray="4 3",
                    fill="none",
                ),
            )
        )
    return tuple(slots)


def _circle_on_grid(
    slot_id: str,
    *,
    grid_x: float,
    grid_y: float,
    center: tuple[float, float],
    radius_cells: float,
) -> CircleSlot:
    return CircleSlot(
        id=slot_id,
        prompt="",
        cx=grid_x + center[0] * GRID_STEP,
        cy=grid_y + center[1] * GRID_STEP,
        r=radius_cells * GRID_STEP,
        fill="none",
        stroke="#444444",
        stroke_width=1.6,
    )


def build_problem_template() -> ProblemTemplate:
    left_x, grid_y = 239.0, 86.0
    right_x = 562.0

    left_grid = _grid_slots("slot.grid.left", x=left_x, y=grid_y)
    right_grid = _grid_slots("slot.grid.right", x=right_x, y=grid_y)
    speakers = (
        SpeakerSpec(
            key="boy",
            cx=(((154.0) + (200.0)) + (-75.0)) + (30.0),
            head_cy=(((395.0) + (5.0)) + (-10.0)) + (5.0),
            bubble_cy=(((354.0) + (5.0)) + (-10.0)) + (5.0),
            text="큰 원을\n먼저 그려.",
            name="민수",
            hair="#3B2417",
            shirt="#58C7BC",
            bubble_width=170.0,
            bubble_height=88.0,
            tail_y=(((350.0) + (5.0)) + (-10.0)) + (5.0),
            name_y=(((468.0) + (5.0)) + (-10.0)) + (5.0),
            speech_font_size=23,
            speech_text_dy=-10,
        ),
        SpeakerSpec(
            key="girl",
            cx=((790.0) + (-230.0)) + (45.0),
            head_cy=((395.0) + (-5.0)) + (10.0),
            bubble_cy=((354.0) + (-5.0)) + (10.0),
            text="큰 원의 반지름을\n( 지름, 반지름 )으로 하는\n작은 원을 2개 그려.",
            name="지혜",
            hair="#4B260B",
            shirt="#F16078",
            bow="#E85BA6",
            pigtails=True,
            bubble_width=285.0,
            bubble_height=118.0,
            tail_y=((350.0) + (-5.0)) + (10.0),
            name_y=((468.0) + (-5.0)) + (10.0),
            speech_font_size=21,
            speech_text_dy=-26,
        ),
    )
    dialogue_slots = speaker_group_slots(speakers)

    return ProblemTemplate(
        id="S3_초등_3_008682",
        title="알맞은 말 선택하기",
        canvas=Canvas(width=960, height=580, coordinate_mode="logical"),
        regions=(
            Region(id="region.stem", role="stem", flow="absolute", slot_ids=("slot.q1", "slot.q2")),
            Region(
                id="region.diagram",
                role="diagram",
                flow="absolute",
                slot_ids=(
                    *(slot.id for slot in left_grid),
                    "slot.left.outer_circle",
                    "slot.left.inner_circle_1",
                    "slot.left.inner_circle_2",
                    "slot.arrow",
                    *(slot.id for slot in right_grid),
                ),
            ),
            Region(
                id="region.dialogue",
                role="diagram",
                flow="absolute",
                slot_ids=speaker_group_slot_ids(speakers),
            ),
        ),
        slots=(
            TextSlot(
                id="slot.q1",
                prompt="",
                text="    주어진 모양과 똑같은 그림을 그리는 방법을 설명한 것입니다. ",
                style_role="question",
                x=74.0,
                y=34.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.q2",
                prompt="",
                text="알맞은 말을 선택하세요.",
                style_role="question",
                x=74.0,
                y=70.0,
                font_size=28,
            ),
            *left_grid,
            _circle_on_grid(
                "slot.left.outer_circle",
                grid_x=left_x,
                grid_y=grid_y,
                center=(4, 4),
                radius_cells=4,
            ),
            _circle_on_grid(
                "slot.left.inner_circle_1",
                grid_x=left_x,
                grid_y=grid_y,
                center=(2, 4),
                radius_cells=2,
            ),
            _circle_on_grid(
                "slot.left.inner_circle_2",
                grid_x=left_x,
                grid_y=grid_y,
                center=(6, 4),
                radius_cells=2,
            ),
            PathSlot(
                id="slot.arrow",
                prompt="",
                d="M 454 182 L 496 182 M 482 170 L 496 182 L 482 194",
                stroke="#444444",
                stroke_width=2.0,
                fill="none",
            ),
            *right_grid,
            *dialogue_slots,
        ),
        diagrams=(),
        groups=(),
        constraints=(),
        tags=("geometry", "circle", "grid", "term_selection"),
    )


PROBLEM_TEMPLATE = build_problem_template()

SEMANTIC_OVERRIDE = {
    "problem_id": "S3_초등_3_008682",
    "problem_type": "geometry_construction_term_selection",
    "metadata": {
        "language": "ko",
        "question": "주어진 모양과 똑같은 그림을 그리는 방법에서 알맞은 말을 선택한다.",
        "instruction": "큰 원의 반지름을 무엇으로 하는 작은 원을 그리는지 고른다.",
    },
    "domain": {
        "objects": [
            {"id": "obj.large_circle", "type": "circle", "radius_cells": 4},
            {"id": "obj.small_circle.left", "type": "circle", "radius_cells": 2},
            {"id": "obj.small_circle.right", "type": "circle", "radius_cells": 2},
        ],
        "relations": [
            {
                "id": "rel.small_diameter_equals_large_radius",
                "type": "equals",
                "from_id": "obj.small_circle.left",
                "to_id": "obj.large_circle",
                "left": "small circle diameter",
                "right": "large circle radius",
            }
        ],
        "problem_solving": {
            "understand": {
                "given_refs": [
                    "obj.large_circle",
                    "obj.small_circle.left",
                    "obj.small_circle.right",
                ],
                "target_ref": "answer.target",
                "condition_refs": ["rel.small_diameter_equals_large_radius"],
            },
            "plan": {
                "method": "term_matching",
                "description": "큰 원의 반지름은 4칸이고 작은 원의 지름도 4칸이므로, 작은 원은 큰 원의 반지름을 지름으로 하여 그린 것이다.",
            },
            "execute": {"expected_operations": ["compare_grid_radius", "select_matching_term"]},
            "review": {"check_methods": ["grid_cell_count_check"]},
        },
    },
    "answer": ANSWER,
}

SOLVABLE = {
    "schema": "modu.solvable.v1.1",
    "problem_id": "S3_초등_3_008682",
    "problem_type": "geometry_construction_term_selection",
    "inputs": {"target_label": "알맞은 말", "unit": ""},
    "given": [
        {"ref": "obj.large_circle", "value": {"radius_cells": 4}},
        {"ref": "obj.small_circle.left", "value": {"radius_cells": 2}},
        {"ref": "obj.small_circle.right", "value": {"radius_cells": 2}},
    ],
    "target": {"ref": "answer.target", "type": "selected_term"},
    "method": "term_matching",
    "plan": [
        "큰 원의 반지름과 작은 원의 지름을 모눈 칸 수로 확인한다.",
        "작은 원에서 큰 원의 반지름과 같은 값을 고른다.",
    ],
    "steps": [
        {"id": "step.1", "expr": "큰 원의 반지름", "value": "4칸"},
        {"id": "step.2", "expr": "작은 원의 지름", "value": "4칸"},
    ],
    "checks": [
        {
            "id": "check.1",
            "expr": "작은 원의 지름이 큰 원의 반지름과 같은가",
            "expected": True,
            "actual": True,
            "pass": True,
        }
    ],
    "answer": ANSWER,
}
