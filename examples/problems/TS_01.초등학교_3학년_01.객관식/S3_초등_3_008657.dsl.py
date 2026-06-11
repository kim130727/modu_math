from __future__ import annotations

from modu_math.dsl import Canvas, CircleSlot, ProblemTemplate, RectSlot, Region, TextSlot, compass_slots


ANSWER = {
    "blanks": [],
    "choices": [],
    "answer_key": [],
    "target": {"type": "selected_option", "description": "원을 그릴 때 컴퍼스를 바르게 사용한 보기"},
    "value": "나",
    "unit": "",
}


def _option_slots(
    prefix: str,
    *,
    label: str,
    label_x: float,
    circle_cx: float,
    circle_cy: float,
    radius: float,
    needle_x: float,
    needle_y: float,
    pencil_x: float,
    pencil_y: float,
    hinge_x: float,
    hinge_y: float,
) -> tuple:
    return (
        TextSlot(id=f"{prefix}.label", prompt="", text=label, style_role="label", x=label_x, y=92.0, font_size=28),
        CircleSlot(
            id=f"{prefix}.circle",
            prompt="",
            cx=circle_cx,
            cy=circle_cy,
            r=radius,
            fill="none",
            stroke="#9A9A9A",
            stroke_width=1.4,
        ),
        CircleSlot(id=f"{prefix}.center.dot", prompt="", cx=circle_cx, cy=circle_cy, r=3.0, fill="#E91E63"),
        CircleSlot(
            id=f"{prefix}.center.mark",
            prompt="",
            cx=circle_cx,
            cy=circle_cy + 14.0,
            r=4.0,
            fill="none",
            stroke="#555555",
            stroke_width=1.4,
        ),
        *compass_slots(
            f"{prefix}.compass",
            hinge_x=hinge_x,
            hinge_y=hinge_y,
            needle_x=needle_x,
            needle_y=needle_y,
            pencil_x=pencil_x,
            pencil_y=pencil_y,
            scale=0.86,
        ),
    )


def build_problem_template() -> ProblemTemplate:
    option_a = _option_slots(
        "slot.opt.a",
        label="가",
        label_x=216.0,
        circle_cx=294.0,
        circle_cy=178.0,
        radius=42.0,
        needle_x=252.0,
        needle_y=178.0,
        pencil_x=336.0,
        pencil_y=178.0,
        hinge_x=292.0,
        hinge_y=84.0,
    )
    option_b = _option_slots(
        "slot.opt.b",
        label="나",
        label_x=396.0,
        circle_cx=475.0,
        circle_cy=178.0,
        radius=42.0,
        needle_x=475.0,
        needle_y=178.0,
        pencil_x=517.0,
        pencil_y=178.0,
        hinge_x=496.0,
        hinge_y=84.0,
    )
    option_c = _option_slots(
        "slot.opt.c",
        label="다",
        label_x=577.0,
        circle_cx=656.0,
        circle_cy=178.0,
        radius=42.0,
        needle_x=698.0,
        needle_y=178.0,
        pencil_x=656.0,
        pencil_y=178.0,
        hinge_x=676.0,
        hinge_y=84.0,
    )

    return ProblemTemplate(
        id="S3_초등_3_008657",
        title="원을 그릴 때 컴퍼스를 바르게 사용한 것",
        canvas=Canvas(width=940.0, height=366.0, coordinate_mode="logical"),
        regions=(
            Region(
                id="region.stem",
                role="stem",
                flow="absolute",
                slot_ids=("slot.title.text",),
            ),
            Region(
                id="region.options",
                role="diagram",
                flow="absolute",
                slot_ids=("slot.box", *(slot.id for slot in option_a), *(slot.id for slot in option_b), *(slot.id for slot in option_c)),
            ),
            Region(id="region.solution", role="answer", flow="absolute", slot_ids=( )),
        ),
        slots=(
            TextSlot(
                id="slot.title.text",
                prompt="",
                text = '원을 그릴 때 컴퍼스를 바르게 사용한 것을 찾아 선택해 보세요.', style_role="question",
                x = 80, y = 40, font_size = 30),
            RectSlot(
                id="slot.box",
                prompt="",
                x=194.0,
                y=52.0,
                width=578.0,
                height=190.0,
                fill="none",
                stroke="#18B7AF",
                stroke_width=2.0,
            ),
            *option_a,
            *option_b,
            *option_c,
            
            
        ),
        diagrams=(),
        groups=(),
        constraints=(),
        tags=("geometry", "circle", "compass", "measurement_tool"),
    )


PROBLEM_TEMPLATE = build_problem_template()

SEMANTIC_OVERRIDE = {
    "problem_id": "S3_초등_3_008657",
    "problem_type": "diagram_choice",
    "metadata": {
        "language": "ko",
        "question": "원을 그릴 때 컴퍼스를 바르게 사용한 것을 찾아 선택하는 문제",
        "instruction": "보기 가, 나, 다 중에서 고르기",
    },
    "domain": {
        "objects": [
            {"id": "obj.circle", "type": "circle"},
            {"id": "obj.compass", "type": "compass"},
            {"id": "obj.choice.a", "type": "option", "label": "가", "needle_position": "not_center"},
            {"id": "obj.choice.b", "type": "option", "label": "나", "needle_position": "center"},
            {"id": "obj.choice.c", "type": "option", "label": "다", "needle_position": "not_center"},
        ],
        "relations": [
            {
                "id": "rel.correct_usage",
                "type": "rule",
                "from_id": "obj.compass",
                "to_id": "obj.circle",
                "description": "원을 그릴 때 컴퍼스의 침은 원의 중심에 꽂고 연필 끝은 원둘레에 닿게 한다.",
            },
            {
                "id": "rel.choice.b.correct",
                "type": "matches_rule",
                "from_id": "obj.choice.b",
                "to_id": "rel.correct_usage",
                "description": "보기 나는 컴퍼스의 침이 원의 중심에 있으므로 바른 사용이다.",
            },
        ],
        "problem_solving": {
            "understand": {
                "given_refs": ["obj.choice.a", "obj.choice.b", "obj.choice.c"],
                "target_ref": "answer.target",
                "condition_refs": ["rel.correct_usage"],
            },
            "plan": {"method": "visual_choice", "description": "세 보기에서 컴퍼스 침이 원의 중심에 꽂힌 보기를 찾는다."},
            "execute": {"expected_operations": ["compare_options", "check_needle_at_circle_center"]},
            "review": {"check_methods": ["confirm_selected_option"]},
        },
    },
    "answer": ANSWER,
}

SOLVABLE = {
    "schema": "modu.solvable.v1.1",
    "problem_id": "S3_초등_3_008657",
    "problem_type": "diagram_choice",
    "inputs": {
        "target_label": "컴퍼스를 바르게 사용한 보기",
        "target_count": 1,
        "unit": "",
    },
    "given": [
        {"ref": "obj.choice.a", "value": {"label": "가", "needle_position": "not_center"}},
        {"ref": "obj.choice.b", "value": {"label": "나", "needle_position": "center"}},
        {"ref": "obj.choice.c", "value": {"label": "다", "needle_position": "not_center"}},
    ],
    "target": {"ref": "answer.target", "type": "selected_option"},
    "method": "visual_choice",
    "plan": [
        "원의 중심을 확인한다.",
        "각 보기에서 컴퍼스의 침 위치를 확인한다.",
        "침이 원의 중심에 꽂힌 보기를 선택한다.",
    ],
    "steps": [
        {"id": "step.1", "expr": "가: 침이 중심이 아닌 곳에 있음", "value": "incorrect"},
        {"id": "step.2", "expr": "나: 침이 원의 중심에 있음", "value": "correct"},
        {"id": "step.3", "expr": "다: 연필 끝이 중심 쪽에 있고 침이 중심이 아님", "value": "incorrect"},
    ],
    "checks": [
        {"id": "check.1", "expr": "선택한 보기의 침이 원의 중심에 있는가", "expected": "나", "actual": "나", "pass": True}
    ],
    "answer": ANSWER,
}
