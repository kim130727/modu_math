from __future__ import annotations

from modu_math.dsl import Canvas, CircleSlot, PathSlot, ProblemTemplate, Region, TextSlot


ANSWER = {
    "blanks": [],
    "choices": [],
    "answer_key": [],
    "target": {"type": "rule_description", "description": "두 모양을 그린 규칙의 같은 점과 다른 점"},
    "value": "같은 점은 원의 반지름이 1칸, 2칸, 3칸으로 커지는 것이고, 다른 점은 가는 원의 중심이 모두 다르며 나는 원의 중심이 모두 같다는 점이다.",
    "unit": "",
}


def _grid_slots(prefix: str, *, x: float, y: float, cells: int = 6, step: float = 30.0) -> tuple[PathSlot, ...]:
    size = cells * step
    slots: list[PathSlot] = [
        PathSlot(
            id=f"{prefix}.frame",
            prompt="",
            d=f"M {x} {y} L {x + size} {y} L {x + size} {y + size} L {x} {y + size} Z",
            stroke="#37C7FF",
            stroke_width=1.2,
            stroke_dasharray="4 3",
            fill="#ffffff",
        )
    ]
    for i in range(1, cells):
        gx = x + i * step
        gy = y + i * step
        slots.append(
            PathSlot(
                id=f"{prefix}.v{i}",
                prompt="",
                d=f"M {gx} {y} L {gx} {y + size}",
                stroke="#37C7FF",
                stroke_width=1.0,
                stroke_dasharray="4 3",
                fill="none",
            )
        )
        slots.append(
            PathSlot(
                id=f"{prefix}.h{i}",
                prompt="",
                d=f"M {x} {gy} L {x + size} {gy}",
                stroke="#37C7FF",
                stroke_width=1.0,
                stroke_dasharray="4 3",
                fill="none",
            )
        )
    return tuple(slots)


def _circle_at(prefix: str, *, grid_x: float, grid_y: float, step: float, center: tuple[int, int], radius: int) -> CircleSlot:
    return CircleSlot(
        id=f"{prefix}.r{radius}",
        prompt="",
        cx=grid_x + center[0] * step,
        cy=grid_y + center[1] * step,
        r=radius * step,
        fill="none",
        stroke="#444444",
        stroke_width=1.4,
    )


def build_problem_template() -> ProblemTemplate:
    step = 30.0
    ga_x, ga_y = 250.0, 84.0
    na_x, na_y = 535.0, 84.0

    ga_grid = _grid_slots("slot.ga.grid", x=ga_x, y=ga_y, step=step)
    na_grid = _grid_slots("slot.na.grid", x=na_x, y=na_y, step=step)
    ga_circles = (
        _circle_at("slot.ga.circle1", grid_x=ga_x, grid_y=ga_y, step=step, center=(1, 3), radius=1),
        _circle_at("slot.ga.circle2", grid_x=ga_x, grid_y=ga_y, step=step, center=(2, 3), radius=2),
        _circle_at("slot.ga.circle3", grid_x=ga_x, grid_y=ga_y, step=step, center=(3, 3), radius=3),
    )
    na_circles = (
        _circle_at("slot.na.circle1", grid_x=na_x, grid_y=na_y, step=step, center=(3, 3), radius=1),
        _circle_at("slot.na.circle2", grid_x=na_x, grid_y=na_y, step=step, center=(3, 3), radius=2),
        _circle_at("slot.na.circle3", grid_x=na_x, grid_y=na_y, step=step, center=(3, 3), radius=3),
    )

    return ProblemTemplate(
        id="S3_초등_3_008653",
        title="가와 나의 원 그리기 규칙",
        canvas=Canvas(width=940, height=350, coordinate_mode="logical"),
        regions=(
            Region(id="region.stem", role="stem", flow="absolute", slot_ids=("slot.q1", "slot.q2")),
            Region(
                id="region.diagram.ga",
                role="diagram",
                flow="absolute",
                slot_ids=("slot.label.ga", *(slot.id for slot in ga_grid), *(slot.id for slot in ga_circles)),
            ),
            Region(
                id="region.diagram.na",
                role="diagram",
                flow="absolute",
                slot_ids=("slot.label.na", *(slot.id for slot in na_grid), *(slot.id for slot in na_circles)),
            ),
            Region(id="region.choice", role="choices", flow="absolute", slot_ids=("slot.choice1", )),
        ),
        slots=(
            TextSlot(
                id="slot.q1",
                prompt="",
                text = '가와 나는 규칙에 따라 원을 그린 것입니다. 알맞은 것을 선택해 두 모양', style_role="question",
                x=8.0,
                y=30.0,
                font_size=24,
            ),
            TextSlot(
                id="slot.q2",
                prompt="",
                text="을 그린 규칙의 같은 점과 다른 점을 설명해 보세요.",
                style_role="question",
                x=8.0,
                y=66.0,
                font_size=24,
            ),
            TextSlot(id="slot.label.ga", prompt="", text = '가', style_role="label", x = 220, y = 130, font_size = 25),
            *ga_grid,
            *ga_circles,
            TextSlot(id="slot.label.na", prompt="", text = '나', style_role="label", x = 505, y = 130, font_size = 25),
            *na_grid,
            *na_circles,
            TextSlot(
                id="slot.choice1",
                prompt="",
                text = '같은 점: 원의 ( 중심 , 반지름 )을 모두 다르게 하여 그렸습니다.', style_role="answer_option",
                x = 10, y = 345, font_size = 25),
            
        ),
        diagrams=(),
        groups=(),
        constraints=(),
        tags=("geometry", "circle", "grid", "rule_comparison"),
    )


PROBLEM_TEMPLATE = build_problem_template()

SEMANTIC_OVERRIDE = {
    "problem_id": "S3_초등_3_008653",
    "problem_type": "diagram_choice",
    "metadata": {
        "language": "ko",
        "question": "가와 나의 원 그리기 규칙을 비교하여 알맞은 설명을 고르는 문제",
        "instruction": "그림을 보고 같은 점과 다른 점을 설명한다.",
    },
    "domain": {
        "objects": [
            {"id": "obj.figure.ga", "type": "figure", "label": "가"},
            {"id": "obj.figure.na", "type": "figure", "label": "나"},
            {
                "id": "obj.circle_set.ga",
                "type": "circles",
                "centers": [[1, 3], [2, 3], [3, 3]],
                "radii": [1, 2, 3],
            },
            {
                "id": "obj.circle_set.na",
                "type": "circles",
                "centers": [[3, 3], [3, 3], [3, 3]],
                "radii": [1, 2, 3],
            },
        ],
        "relations": [
            {
                "id": "rel.same_radii_rule",
                "type": "same_rule",
                "from_id": "obj.circle_set.ga",
                "to_id": "obj.circle_set.na",
                "description": "가와 나는 모두 반지름이 1칸, 2칸, 3칸으로 커진다.",
            },
            {
                "id": "rel.different_centers_rule",
                "type": "different_rule",
                "from_id": "obj.circle_set.ga",
                "to_id": "obj.circle_set.na",
                "description": "가는 원의 중심이 모두 다르고, 나는 원의 중심이 모두 같다.",
            },
        ],
        "problem_solving": {
            "understand": {
                "given_refs": ["obj.figure.ga", "obj.figure.na"],
                "target_ref": "answer.target",
                "condition_refs": ["rel.same_radii_rule", "rel.different_centers_rule"],
            },
            "plan": {"method": "figure_comparison", "description": "두 그림에서 원의 중심과 반지름 규칙을 비교한다."},
            "execute": {"expected_operations": ["compare_circle_centers", "compare_circle_radii", "match_with_choice"]},
            "review": {"check_methods": ["image_text_consistency_check"]},
        },
    },
    "answer": ANSWER,
}

SOLVABLE = {
    "schema": "modu.solvable.v1.1",
    "problem_id": "S3_초등_3_008653",
    "problem_type": "diagram_choice",
    "inputs": {"target_label": "가와 나의 원 그리기 규칙", "target_count": 1, "unit": ""},
    "given": [
        {"ref": "obj.circle_set.ga", "value": {"centers": [[1, 3], [2, 3], [3, 3]], "radii": [1, 2, 3]}},
        {"ref": "obj.circle_set.na", "value": {"centers": [[3, 3], [3, 3], [3, 3]], "radii": [1, 2, 3]}},
    ],
    "target": {"ref": "answer.target", "type": "rule_description"},
    "method": "figure_comparison",
    "plan": [
        "가의 원들의 중심과 반지름을 확인한다.",
        "나의 원들의 중심과 반지름을 확인한다.",
        "두 그림의 같은 점과 다른 점을 비교한다.",
    ],
    "steps": [
        {"id": "step.1", "expr": "가: 중심 (1,3),(2,3),(3,3), 반지름 1,2,3", "value": "centers_different_radii_increase"},
        {"id": "step.2", "expr": "나: 중심 (3,3)으로 모두 같고, 반지름 1,2,3", "value": "same_center_radii_increase"},
        {"id": "step.3", "expr": "같은 점과 다른 점 정리", "value": "same_radii_different_centers"},
    ],
    "checks": [
        {
            "id": "check.1",
            "expr": "두 그림 모두 반지름이 1,2,3으로 커지는가",
            "expected": True,
            "actual": True,
            "pass": True,
        }
    ],
    "answer": ANSWER,
}
