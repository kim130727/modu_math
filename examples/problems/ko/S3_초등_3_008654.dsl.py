from __future__ import annotations

from modu_math.dsl import Canvas, CircleSlot, PathSlot, ProblemTemplate, Region, TextSlot

ANSWER = {
    "blanks": [],
    "choices": [],
    "answer_key": [],
    "target": {
        "type": "rule_description",
        "description": "두 모양을 그린 규칙의 같은 점과 다른 점",
    },
    "value": "가는 원의 중심을 옮겨가며 그렸고, 나는 원의 중심을 모두 같게 그렸습니다.",
    "unit": "",
}


def _grid_slots(
    prefix: str, *, x: float, y: float, cells: int = 6, step: float = 30.0
) -> tuple[PathSlot, ...]:
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


def _circle_at(
    prefix: str, *, grid_x: float, grid_y: float, step: float, center: tuple[int, int], radius: int
) -> CircleSlot:
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
        id="S3_초등_3_008654",
        title="가와 나의 원 그리기 규칙",
        canvas=Canvas(width=940, height=350, coordinate_mode="logical"),
        regions=(
            Region(id="region.stem", role="stem", flow="absolute", slot_ids=("slot.q1", "slot.q2")),
            Region(
                id="region.diagram.ga",
                role="diagram",
                flow="absolute",
                slot_ids=(
                    "slot.label.ga",
                    *(slot.id for slot in ga_grid),
                    *(slot.id for slot in ga_circles),
                ),
            ),
            Region(
                id="region.diagram.na",
                role="diagram",
                flow="absolute",
                slot_ids=(
                    "slot.label.na",
                    *(slot.id for slot in na_grid),
                    *(slot.id for slot in na_circles),
                ),
            ),
            Region(
                id="region.choice",
                role="choices",
                flow="absolute",
                slot_ids=("slot.choice1", "slot.choice1.copy1"),
            ),
        ),
        slots=(
            TextSlot(
                id="slot.q1",
                prompt="",
                text="가와 나는 규칙에 따라 원을 그린 것입니다. 알맞은 것을 선택해 두 모양",
                style_role="question",
                x=10,
                y=30,
                font_size=25,
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
            TextSlot(
                id="slot.label.ga",
                prompt="",
                text="가",
                style_role="label",
                x=220.0,
                y=103.0,
                font_size=24,
            ),
            *ga_grid,
            *ga_circles,
            TextSlot(
                id="slot.label.na",
                prompt="",
                text="나",
                style_role="label",
                x=505.0,
                y=103.0,
                font_size=24,
            ),
            *na_grid,
            *na_circles,
            TextSlot(
                id="slot.choice1",
                prompt="",
                text="    다른 점: (가,나)는 원의 중심을 옮겨가며 그렸고, (가,나)는 원의 중심이 모두",
                style_role="answer_option",
                x=15,
                y=300,
                font_size=25,
            ),
            TextSlot(
                id="slot.choice1.copy1",
                prompt="",
                text="같게 그렸습니다.  ",
                x=15,
                y=335,
                font_size=25,
                fill="#111111",
            ),
        ),
        diagrams=(),
        groups=(),
        constraints=(),
        tags=("geometry", "circle", "grid", "rule_comparison"),
    )


PROBLEM_TEMPLATE = build_problem_template()

SEMANTIC_OVERRIDE = {
    "problem_id": "S3_초등_3_008654",
    "problem_type": "compare_patterns",
    "metadata": {
        "language": "ko",
        "question": "원을 그린 두 규칙의 같은 점과 다른 점을 설명하는 문제",
        "instruction": "알맞은 것을 선택해 두 모양을 그린 규칙의 같은 점과 다른 점을 설명해 보세요.",
    },
    "domain": {
        "objects": [
            {"id": "obj.figure.ga", "type": "figure", "label": "가"},
            {"id": "obj.figure.na", "type": "figure", "label": "나"},
            {"id": "obj.circle_set.ga", "type": "circle_group", "count": 3},
            {"id": "obj.circle_set.na", "type": "circle_group", "count": 3},
        ],
        "relations": [],
        "problem_solving": {
            "understand": {
                "given_refs": ["obj.figure.ga", "obj.figure.na"],
                "target_ref": "answer.target",
                "condition_refs": ["rel.compare.same", "rel.compare.different"],
            },
            "plan": {
                "method": "compare_two_figures",
                "description": "두 그림에서 원의 중심 배치를 비교해 같은 점과 다른 점을 찾는다.",
            },
            "execute": {
                "expected_operations": [
                    "observe_figure_ga",
                    "observe_figure_na",
                    "compare_center_positions",
                ]
            },
            "review": {"check_methods": ["compare_background", "compare_circle_centers"]},
        },
    },
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {
            "type": "explain_same_and_different",
            "description": "두 모양을 그린 규칙의 같은 점과 다른 점",
        },
        "value": ANSWER,
        "unit": "",
    },
}

SOLVABLE = {
    "schema": "modu.solvable.v1.1",
    "problem_id": "S3_초등_3_008654",
    "problem_type": "compare_patterns",
    "inputs": {
        "total_ticks": 0,
        "target_label": "두 모양을 그린 규칙의 같은 점과 다른 점",
        "target_ticks": 0,
        "target_count": 2,
        "unit": "",
    },
    "given": [
        {"ref": "obj.figure.ga", "value": "가"},
        {"ref": "obj.figure.na", "value": "나"},
    ],
    "target": {"ref": "answer.target", "type": "explain_same_and_different"},
    "method": "compare_two_figures",
    "plan": [
        "두 그림의 원 배치와 중심 위치를 비교한다.",
        "같은 점은 공통 배경과 같은 종류의 원이라는 점으로 본다.",
        "다른 점은 원의 중심이 옮겨졌는지, 모두 같은지로 본다.",
    ],
    "steps": [
        {
            "id": "step.1",
            "expr": "가 그림의 원 중심 배치 확인",
            "value": "중심이 서로 다른 위치로 옮겨진 배치",
        },
        {
            "id": "step.2",
            "expr": "나 그림의 원 중심 배치 확인",
            "value": "중심이 모두 같은 배치",
        },
        {
            "id": "step.3",
            "expr": "두 그림의 공통점 비교",
            "value": "같은 격자 위에 원 3개를 겹쳐 그림",
        },
    ],
    "checks": [
        {
            "id": "check.1",
            "expr": "가와 나의 배치가 서로 다른가",
            "expected": True,
            "actual": True,
            "pass": True,
        },
        {
            "id": "check.2",
            "expr": "나의 원들이 같은 중심을 가지는가",
            "expected": True,
            "actual": True,
            "pass": True,
        },
    ],
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {
            "type": "explain_same_and_different",
            "description": "두 모양을 그린 규칙의 같은 점과 다른 점",
        },
        "value": ANSWER,
        "unit": "",
    },
}
