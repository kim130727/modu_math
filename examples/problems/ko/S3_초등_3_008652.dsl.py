from __future__ import annotations

from modu_math.dsl import (
    Canvas,
    CircleSlot,
    PathSlot,
    PolygonSlot,
    ProblemTemplate,
    RectSlot,
    Region,
    TextSlot,
    character_body_slots,
)


def _grid_paper_slots(
    prefix: str,
    *,
    x: float,
    y: float,
    size: float,
    divisions: int,
    stroke: str = "#37C7FF",
) -> tuple[PathSlot, ...]:
    step = size / divisions
    slots: list[PathSlot] = [
        PathSlot(
            id=f"{prefix}.frame",
            prompt="",
            d=f"M {x} {y} L {x + size} {y} L {x + size} {y + size} L {x} {y + size} Z",
            fill="#ffffff",
            stroke=stroke,
            stroke_width=1.4,
            stroke_dasharray="4 3",
        )
    ]
    for i in range(1, divisions):
        gx = x + step * i
        gy = y + step * i
        slots.append(
            PathSlot(
                id=f"{prefix}.v{i}",
                prompt="",
                d=f"M {gx:.2f} {y} L {gx:.2f} {y + size}",
                fill="none",
                stroke=stroke,
                stroke_width=1.0,
                stroke_dasharray="4 3",
            )
        )
        slots.append(
            PathSlot(
                id=f"{prefix}.h{i}",
                prompt="",
                d=f"M {x} {gy:.2f} L {x + size} {gy:.2f}",
                fill="none",
                stroke=stroke,
                stroke_width=1.0,
                stroke_dasharray="4 3",
            )
        )
    return tuple(slots)


def _speech_bubble_slots(
    prefix: str,
    *,
    cx: float,
    cy: float,
    width: float,
    height: float,
    tail_x: float,
    tail_y: float,
    lines: tuple[str, ...],
) -> tuple[PathSlot | PolygonSlot | TextSlot, ...]:
    rx = width / 2
    ry = height / 2
    d = (
        f"M {cx - rx} {cy} "
        f"C {cx - rx} {cy - ry * 0.78}, {cx - rx * 0.58} {cy - ry}, {cx} {cy - ry} "
        f"C {cx + rx * 0.58} {cy - ry}, {cx + rx} {cy - ry * 0.78}, {cx + rx} {cy} "
        f"C {cx + rx} {cy + ry * 0.78}, {cx + rx * 0.58} {cy + ry}, {cx} {cy + ry} "
        f"C {cx - rx * 0.58} {cy + ry}, {cx - rx} {cy + ry * 0.78}, {cx - rx} {cy} Z"
    )
    slots: list[PathSlot | PolygonSlot | TextSlot] = [
        PathSlot(
            id=f"{prefix}.bubble",
            prompt="",
            d=d,
            fill="#ffffff",
            stroke="#222222",
            stroke_width=1.6,
        ),
        PolygonSlot(
            id=f"{prefix}.tail",
            prompt="",
            points=((cx - rx + 7, cy + 12), (cx - rx + 26, cy + 18), (tail_x, tail_y)),
            fill="#ffffff",
            stroke="#222222",
            stroke_width=1.4,
        ),
    ]
    start_y = cy - 44
    for idx, line in enumerate(lines, start=1):
        slots.append(
            TextSlot(
                id=f"{prefix}.text{idx}",
                prompt="",
                text=line,
                style_role="speech",
                x=cx,
                y=start_y + (idx - 1) * 35,
                font_size=23,
                anchor="middle",
            )
        )
    return tuple(slots)


def _name_tag_slots(prefix: str, *, x: float, y: float, name: str) -> tuple[RectSlot, TextSlot]:
    return (
        RectSlot(
            id=f"{prefix}.namebox",
            prompt="",
            x=x,
            y=y,
            width=74,
            height=38,
            fill="#FCE6F5",
            stroke="#D77BBE",
            stroke_width=1.4,
            rx=10,
            ry=10,
        ),
        TextSlot(
            id=f"{prefix}.name",
            prompt="",
            text=name,
            style_role="label",
            x=x + 37,
            y=y + 27,
            font_size=23,
            anchor="middle",
            fill="#333333",
        ),
    )


def build_problem_template() -> ProblemTemplate:
    grid_slots = _grid_paper_slots("slot.grid", x=118.0, y=150.0, size=282.0, divisions=12)
    sunga_character = character_body_slots(
        "slot.sunga.character", cx=532.0, head_cy=164.0, hair="#3A2116", shirt="#F16078"
    )
    jaewon_character = character_body_slots(
        "slot.jaewon.character", cx=532.0, head_cy=338.0, hair="#4B260B", shirt="#1E8AD6"
    )
    sunga_name = _name_tag_slots("slot.sunga", x=493.0, y=236.0, name="승아")
    jaewon_name = _name_tag_slots("slot.jaewon", x=493.0, y=416.0, name="재원")
    sunga_bubble = _speech_bubble_slots(
        "slot.sunga",
        cx=725.0,
        cy=181.0,
        width=240.0,
        height=174.0,
        tail_x=590.0,
        tail_y=186.0,
        lines=("원의 중심이 모두", "다르고 원의 반지름이", "모눈 1칸씩 늘어나게", "그렸어요."),
    )
    jaewon_bubble = _speech_bubble_slots(
        "slot.jaewon",
        cx=725.0,
        cy=363.0,
        width=240.0,
        height=174.0,
        tail_x=590.0,
        tail_y=370.0,
        lines=("원의 중심이 모두", "같고 원의 반지름이", "모눈 2칸씩 늘어나게", "그렸어요."),
    )

    return ProblemTemplate(
        id="S3_초등_3_008652",
        title="그림의 규칙을 바르게 말한 사람 선택하기",
        canvas=Canvas(width=960, height=620, coordinate_mode="logical"),
        regions=(
            Region(
                id="region.header",
                role="stem",
                flow="absolute",
                slot_ids=("slot.qnum", "slot.qtext1", "slot.qtext2"),
            ),
            Region(
                id="region.diagram",
                role="diagram",
                flow="absolute",
                slot_ids=(
                    *(slot.id for slot in grid_slots),
                    "slot.circle.outer",
                    "slot.circle.middle",
                    "slot.circle.inner",
                    "slot.center",
                ),
            ),
            Region(
                id="region.characters",
                role="diagram",
                flow="absolute",
                slot_ids=(
                    *(slot.id for slot in sunga_character),
                    *(slot.id for slot in sunga_name),
                    *(slot.id for slot in sunga_bubble),
                    *(slot.id for slot in jaewon_character),
                    *(slot.id for slot in jaewon_name),
                    *(slot.id for slot in jaewon_bubble),
                ),
            ),
            Region(
                id="region.footer",
                role="note",
                flow="absolute",
                slot_ids=("slot.answer", "slot.explain1", "slot.explain2"),
            ),
        ),
        slots=(
            TextSlot(
                id="slot.qtext1",
                prompt="",
                text="규칙에 따라 원을 그린 것입니다. 그린 규칙을 바르게 말한 사람을 선택",
                style_role="question",
                x=35,
                y=35,
                font_size=25,
            ),
            TextSlot(
                id="slot.qtext2",
                prompt="",
                text="해 보세요.",
                style_role="question",
                x=36.0,
                y=70.0,
                font_size=24,
            ),
            *grid_slots,
            CircleSlot(
                id="slot.circle.outer",
                prompt="",
                cx=259.0,
                cy=291.0,
                r=118.0,
                fill="none",
                stroke="#444444",
                stroke_width=1.4,
            ),
            CircleSlot(
                id="slot.circle.middle",
                prompt="",
                cx=259.0,
                cy=291.0,
                r=71.0,
                fill="none",
                stroke="#444444",
                stroke_width=1.4,
            ),
            CircleSlot(
                id="slot.circle.inner",
                prompt="",
                cx=259.0,
                cy=291.0,
                r=23.5,
                fill="none",
                stroke="#444444",
                stroke_width=1.4,
            ),
            CircleSlot(
                id="slot.center",
                prompt="",
                cx=259.0,
                cy=291.0,
                r=4.0,
                fill="#E11A86",
                stroke="none",
            ),
            *sunga_character,
            *sunga_name,
            *sunga_bubble,
            *jaewon_character,
            *jaewon_name,
            *jaewon_bubble,
        ),
        diagrams=(),
        groups=(),
        constraints=(),
        tags=("geometry", "circle", "grid", "rule_selection"),
    )


PROBLEM_TEMPLATE = build_problem_template()

SEMANTIC_OVERRIDE = {
    "problem_id": "S3_초등_3_008652",
    "problem_type": "rule_selection",
    "metadata": {
        "language": "ko",
        "question": "규칙에 따라 원을 그린 것입니다. 그린 규칙을 바르게 말한 사람을 선택해 보세요.",
        "instruction": "그린 규칙을 바르게 말한 사람을 선택한다.",
    },
    "domain": {
        "objects": [
            {"id": "obj.circles", "type": "circle_set", "count": 3},
            {"id": "obj.center", "type": "center_point"},
            {"id": "obj.grid", "type": "dotted_grid"},
            {"id": "obj.student.sunga", "type": "student", "name": "승아"},
            {"id": "obj.student.jaewon", "type": "student", "name": "재원"},
        ],
        "relations": [
            {
                "id": "rel.same_center",
                "type": "same_center",
                "from_id": "obj.circles",
                "to_id": "obj.center",
                "description": "세 원의 중심이 모두 같다.",
            },
            {
                "id": "rel.radius_increase",
                "type": "arithmetic_pattern",
                "from_id": "obj.circles",
                "to_id": "obj.grid",
                "description": "반지름이 1칸, 3칸, 5칸으로 2칸씩 늘어난다.",
            },
        ],
        "problem_solving": {
            "understand": {
                "given_refs": [
                    "obj.circles",
                    "obj.center",
                    "obj.student.sunga",
                    "obj.student.jaewon",
                ],
                "target_ref": "answer.target",
                "condition_refs": ["rel.same_center", "rel.radius_increase"],
            },
            "plan": {
                "method": "rule_matching",
                "description": "그림의 중심과 반지름 변화 규칙을 보고 두 사람의 말과 비교한다.",
            },
            "execute": {
                "expected_operations": [
                    "identify_same_center",
                    "recognize_increasing_radius_pattern",
                    "match_student_statement",
                ]
            },
            "review": {"check_methods": ["confirm_rule_consistency"]},
        },
    },
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {"type": "correct_student", "description": "그린 규칙을 바르게 말한 사람"},
        "value": "재원",
        "unit": "",
    },
}

SOLVABLE = {
    "schema": "modu.solvable.v1.1",
    "problem_id": "S3_초등_3_008652",
    "problem_type": "rule_selection",
    "inputs": {
        "total_ticks": 0,
        "target_label": "그린 규칙을 바르게 말한 사람",
        "target_ticks": 0,
        "target_count": 1,
        "unit": "",
    },
    "given": [
        {"ref": "obj.circles", "value": {"count": 3}},
        {"ref": "obj.center", "value": {"type": "center_point", "same_for_all": True}},
        {
            "ref": "rel.radius_increase",
            "value": {"radii_in_grid_cells": [1, 3, 5], "difference": 2},
        },
    ],
    "target": {"ref": "answer.target", "type": "correct_student"},
    "method": "rule_matching",
    "plan": [
        "세 원의 중심이 같은지 확인한다.",
        "반지름이 1칸, 3칸, 5칸으로 2칸씩 늘어나는지 확인한다.",
        "두 설명 중 그림과 맞는 사람을 고른다.",
    ],
    "steps": [
        {"id": "step.1", "expr": "세 원의 중심 확인", "value": "모두 같음"},
        {"id": "step.2", "expr": "반지름 변화 확인", "value": [1, 3, 5]},
        {"id": "step.3", "expr": "설명과 규칙 비교", "value": "재원"},
    ],
    "checks": [
        {
            "id": "check.1",
            "expr": "재원의 설명이 중심과 반지름 규칙을 모두 만족하는가",
            "expected": True,
            "actual": True,
            "pass": True,
        }
    ],
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {"type": "correct_student", "description": "그린 규칙을 바르게 말한 사람"},
        "value": "재원",
        "unit": "",
    },
}
