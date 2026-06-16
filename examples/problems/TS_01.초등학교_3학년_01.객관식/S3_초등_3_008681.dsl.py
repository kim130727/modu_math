from __future__ import annotations
from modu_math.dsl import (
    Canvas,
    CircleSlot,
    LineSlot,
    PathSlot,
    ProblemTemplate,
    Region,
    RectSlot,
    TextSlot,
)


def _make_ruler_slots(
    prefix: str,
    x: float,
    y: float,
    label_y: float,
    right_mark_cm: int,
) -> tuple[tuple[str, ...], tuple[object, ...]]:
    slots: list[object] = []
    ids: list[str] = []

    slots.append(
        RectSlot(
            id=f"{prefix}.base",
            prompt="",
            x=x,
            y=y,
            width=88.0,
            height=30.0,
            fill="#d9f2ff",
            stroke="#66bdf0",
            stroke_width=1.6,
        )
    )
    ids.append(f"{prefix}.base")

    slots.append(
        LineSlot(
            id=f"{prefix}.top",
            prompt="",
            x1=x,
            y1=y + 2.0,
            x2=x + 88.0,
            y2=y + 2.0,
            stroke="#66bdf0",
            stroke_width=1.2,
        )
    )
    ids.append(f"{prefix}.top")
    slots.append(
        LineSlot(
            id=f"{prefix}.bottom",
            prompt="",
            x1=x,
            y1=y + 24.0,
            x2=x + 88.0,
            y2=y + 24.0,
            stroke="#66bdf0",
            stroke_width=1.2,
        )
    )
    ids.append(f"{prefix}.bottom")

    start_x = x + 6.0
    cm_step = 22.0
    for cm in range(4):
        tick_x = start_x + cm * cm_step
        slots.append(
            LineSlot(
                id=f"{prefix}.major.{cm}",
                prompt="",
                x1=tick_x,
                y1=y + 2.0,
                x2=tick_x,
                y2=y + 12.0,
                stroke="#66bdf0",
                stroke_width=1.1,
            )
        )
        ids.append(f"{prefix}.major.{cm}")
        slots.append(
            TextSlot(
                id=f"{prefix}.num.{cm}",
                prompt="",
                text=str(cm),
                style_role="label",
                x=tick_x - 2.5,
                y=label_y,
                font_size=20,
            )
        )
        ids.append(f"{prefix}.num.{cm}")

        if cm < 3:
            for sub in range(1, 5):
                minor_x = tick_x + sub * (cm_step / 5.0)
                minor_h = 5.5 if sub != 2 else 7.0
                slots.append(
                    LineSlot(
                        id=f"{prefix}.minor.{cm}.{sub}",
                        prompt="",
                        x1=minor_x,
                        y1=y + 2.0,
                        x2=minor_x,
                        y2=y + 2.0 + minor_h,
                        stroke="#66bdf0",
                        stroke_width=0.9,
                    )
                )
                ids.append(f"{prefix}.minor.{cm}.{sub}")

    mark_x = start_x + right_mark_cm * cm_step
    return tuple(ids), tuple(slots + [CircleSlot(id=f"{prefix}.mark", prompt="", cx=mark_x, cy=y + 2.0, r=1.2, fill="#444444")])


def _make_compass_slots(
    prefix: str,
    hinge_x: float,
    hinge_y: float,
    left_tip_x: float,
    left_tip_y: float,
    right_tip_x: float,
    right_tip_y: float,
) -> tuple[tuple[str, ...], tuple[object, ...]]:
    ids = (
        f"{prefix}.joint",
        f"{prefix}.head",
        f"{prefix}.left_outer",
        f"{prefix}.left_inner",
        f"{prefix}.right_outer",
        f"{prefix}.right_inner",
        f"{prefix}.left_tip",
        f"{prefix}.right_tip",
    )
    slots: tuple[object, ...] = (
        CircleSlot(id=f"{prefix}.joint", prompt="", cx=hinge_x, cy=hinge_y, r=3.2, fill="#8a8f98"),
        RectSlot(
            id=f"{prefix}.head",
            prompt="",
            x=hinge_x - 3.2,
            y=hinge_y - 20.0,
            width=6.4,
            height=16.0,
            fill="#a7acb3",
            stroke="#626871",
            stroke_width=1.0,
            rx=2.0,
            ry=2.0,
        ),
        PathSlot(
            id=f"{prefix}.left_outer",
            prompt="",
            d=f"M {hinge_x-1.8} {hinge_y+3.0} L {left_tip_x-1.6} {left_tip_y-3.0}",
            stroke="#7e8b97",
            stroke_width=3.2,
            fill="none",
        ),
        PathSlot(
            id=f"{prefix}.left_inner",
            prompt="",
            d=f"M {hinge_x-0.6} {hinge_y+3.0} L {left_tip_x-0.4} {left_tip_y-3.0}",
            stroke="#c8cfd6",
            stroke_width=1.2,
            fill="none",
        ),
        PathSlot(
            id=f"{prefix}.right_outer",
            prompt="",
            d=f"M {hinge_x+1.8} {hinge_y+3.0} L {right_tip_x+1.6} {right_tip_y-3.0}",
            stroke="#7e8b97",
            stroke_width=3.2,
            fill="none",
        ),
        PathSlot(
            id=f"{prefix}.right_inner",
            prompt="",
            d=f"M {hinge_x+0.6} {hinge_y+3.0} L {right_tip_x+0.4} {right_tip_y-3.0}",
            stroke="#c8cfd6",
            stroke_width=1.2,
            fill="none",
        ),
        CircleSlot(id=f"{prefix}.left_tip", prompt="", cx=left_tip_x, cy=left_tip_y, r=1.6, fill="#666666"),
        CircleSlot(id=f"{prefix}.right_tip", prompt="", cx=right_tip_x, cy=right_tip_y, r=1.6, fill="#666666"),
    )
    return ids, slots


def _make_option_block(
    prefix: str,
    ruler_x: float,
    ruler_y: float,
    right_mark_cm: int,
    label_y: float,
) -> tuple[tuple[str, ...], tuple[object, ...]]:
    ruler_ids, ruler_slots = _make_ruler_slots(
        prefix=f"{prefix}.rule",
        x=ruler_x,
        y=ruler_y,
        label_y=label_y,
        right_mark_cm=right_mark_cm,
    )
    hinge_x = ruler_x + 28.0
    hinge_y = ruler_y - 82.0
    left_tip_x = ruler_x + 6.0
    left_tip_y = ruler_y + 2.0
    right_tip_x = ruler_x + 6.0 + (22.0 * right_mark_cm)
    right_tip_y = ruler_y + 2.0
    compass_ids, compass_slots = _make_compass_slots(
        prefix=f"{prefix}.compass",
        hinge_x=hinge_x,
        hinge_y=hinge_y,
        left_tip_x=left_tip_x,
        left_tip_y=left_tip_y,
        right_tip_x=right_tip_x,
        right_tip_y=right_tip_y,
    )
    return ruler_ids + compass_ids, ruler_slots + compass_slots


def build_problem_template() -> ProblemTemplate:
    choice1_ids, choice1_slots = _make_option_block(
        prefix="slot.choice.1",
        ruler_x=196.0,
        ruler_y=204.0,
        right_mark_cm=2,
        label_y=227.0,
    )
    choice2_ids, choice2_slots = _make_option_block(
        prefix="slot.choice.2",
        ruler_x=436.0,
        ruler_y=204.0,
        right_mark_cm=1,
        label_y=227.0,
    )
    choice3_ids, choice3_slots = _make_option_block(
        prefix="slot.choice.3",
        ruler_x=676.0,
        ruler_y=204.0,
        right_mark_cm=3,
        label_y=227.0,
    )

    return ProblemTemplate(
        id="S3_초등_3_008681",
        title="반지름이 3 cm인 원을 그리도록 컴퍼스를 벌린 것 찾기",
        canvas=Canvas(width=940, height=470, coordinate_mode="logical"),
        regions=(
            Region(
                id="region.stem",
                role="stem",
                flow="absolute",
                slot_ids=("slot.q_text",'slot.q_text.copy1', 'slot.q_text.copy1.copy2', 'slot.q_text.copy1.copy3'),
            ),
            Region(
                id="region.choices",
                role="diagram",
                flow="absolute",
                slot_ids=choice1_ids + choice2_ids + choice3_ids,
            ),
            Region(
                id="region.explain",
                role="explanation",
                flow="absolute",
                slot_ids=(),
            ),
        ),
        slots=(TextSlot(
                id="slot.q_text",
                prompt="",
                text = '반지름이 3 cm인 원을 그리도록 컴퍼스를 벌린 것을 찾아 선택해 보세요.', style_role="question",
                x = 10, y = 47, font_size = 30),
            *choice1_slots,
            *choice2_slots,
            *choice3_slots,
            TextSlot(id = 'slot.q_text.copy1', prompt = '', text = '1.', x = 125, y = 170, font_size = 30, fill = '#111111'), TextSlot(id = 'slot.q_text.copy1.copy2', prompt = '', text = '2.', x = 360, y = 165, font_size = 30, fill = '#111111'), TextSlot(id = 'slot.q_text.copy1.copy3', prompt = '', text = '3.', x = 625, y = 175, font_size = 30, fill = '#111111')),
        diagrams=(),
        groups=(),
        constraints=(),
        tags=(),
    )


PROBLEM_TEMPLATE = build_problem_template()

SEMANTIC_OVERRIDE = {
    "problem_id": "S3_초등_3_008681",
    "problem_type": "선택형_도형_비교",
    "metadata": {
        "language": "ko",
        "question": "반지름이 3 cm인 원을 그리도록 컴퍼스를 벌린 것을 찾아 선택하는 문제",
        "instruction": "그림을 보고 컴퍼스 벌림이 3 cm에 해당하는 것을 고르기",
    },
    "domain": {
        "objects": [
            {"id": "obj.radius", "type": "length", "value": 3, "unit": "cm"},
            {"id": "obj.compass", "type": "compass"},
            {"id": "obj.ruler", "type": "ruler"},
            {"id": "obj.options", "type": "choice_set", "count": 3},
        ],
        "relations": [],
        "problem_solving": {
            "understand": {
                "given_refs": ["obj.radius", "obj.compass", "obj.ruler"],
                "target_ref": "answer.target",
                "condition_refs": ["rel.match_radius"],
            },
            "plan": {
                "method": "visual_comparison",
                "description": "자의 눈금과 컴퍼스 벌림을 비교하여 3 cm에 해당하는 그림을 찾는다.",
            },
            "execute": {
                "expected_operations": [
                    "compare_each_option",
                    "match_to_3cm",
                    "select_corresponding_figure",
                ]
            },
            "review": {
                "check_methods": ["length_label_check", "option_consistency_check"]
            },
        },
    },
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {
            "type": "selected_figure",
            "description": "반지름이 3 cm인 원을 그리도록 컴퍼스를 벌린 그림",
        },
        "value": 3,
        "unit": "",
    },
}

SOLVABLE = {
    "schema": "modu.solvable.v1.1",
    "problem_id": "S3_초등_3_008681",
    "problem_type": "선택형_도형_비교",
    "inputs": {
        "total_ticks": 3,
        "target_label": "3 cm",
        "target_ticks": 3,
        "target_count": 1,
        "unit": "cm",
    },
    "given": [
        {"ref": "obj.radius", "value": {"value": 3, "unit": "cm"}},
        {"ref": "obj.options", "value": {"count": 3}},
    ],
    "target": {"ref": "answer.target", "type": "selected_figure"},
    "method": "visual_comparison",
    "plan": [
        "각 보기의 컴퍼스 벌림을 자의 눈금과 비교한다.",
        "3 cm와 같은 벌림을 가진 그림을 찾는다.",
    ],
    "steps": [
        {
            "id": "step.1",
            "expr": "보기 1, 2, 3의 벌림 정도를 자 눈금과 비교한다.",
            "value": "비교 수행",
        },
        {"id": "step.2", "expr": "3 cm에 해당하는 보기 선택", "value": "미정"},
    ],
    "checks": [
        {
            "id": "check.1",
            "expr": "선택된 그림의 벌림이 3 cm와 일치하는가",
            "expected": True,
            "actual": False,
            "pass": False,
        }
    ],
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {
            "type": "selected_figure",
            "description": "반지름이 3 cm인 원을 그리도록 컴퍼스를 벌린 그림",
        },
        "value": 3,
        "unit": "",
    },
}
