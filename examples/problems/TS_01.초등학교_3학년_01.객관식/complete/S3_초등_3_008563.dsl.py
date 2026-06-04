from __future__ import annotations

from modu_math.dsl import Canvas, CircleSlot, LineSlot, ProblemTemplate, RectSlot, Region, TextSlot


def person_slot_ids(prefix: str) -> tuple[str, ...]:
    return (
        f"{prefix}.body",
        f"{prefix}.head",
        f"{prefix}.eye1",
        f"{prefix}.eye2",
        f"{prefix}.mouth",
    )


def person_slots(
    prefix: str,
    *,
    cx: float,
    head_cy: float,
    body_fill: str,
) -> tuple[CircleSlot, RectSlot, CircleSlot, CircleSlot, LineSlot]:
    return (
        RectSlot(
            id=f"{prefix}.body",
            prompt="",
            x=cx - 15,
            y=head_cy + 20,
            width=30,
            height=36,
            rx=10,
            ry=10,
            fill=body_fill,
            stroke=body_fill,
        ),
        CircleSlot(
            id=f"{prefix}.head",
            prompt="",
            cx=cx,
            cy=head_cy,
            r=28,
            fill="#F3C0AD",
        ),
        CircleSlot(
            id=f"{prefix}.eye1",
            prompt="",
            cx=cx - 8,
            cy=head_cy - 3,
            r=3.5,
            fill="#222222",
        ),
        CircleSlot(
            id=f"{prefix}.eye2",
            prompt="",
            cx=cx + 8,
            cy=head_cy - 3,
            r=3.5,
            fill="#222222",
        ),
        LineSlot(
            id=f"{prefix}.mouth",
            prompt="",
            x1=cx - 7,
            y1=head_cy + 10,
            x2=cx + 7,
            y2=head_cy + 10,
            stroke="#C36A6A",
            stroke_dasharray="",
        ),
    )


def build_problem_template() -> ProblemTemplate:
    return ProblemTemplate(
        id="S3_초등_3_008563",
        title="계산 결과가 더 큰 사람을 선택해 보세요.",
        canvas=Canvas(width=550, height=300, coordinate_mode="logical"),
        regions=(
            Region(
                id="region.top",
                role="stem",
                flow="absolute",
                slot_ids=("slot.q_text",),
            ),
            Region(
                id="region.middle",
                role="diagram",
                flow="absolute",
                slot_ids=(
                    "slot.left_card",
                    "slot.right_card",
                    "slot.left_name_box",
                    "slot.right_name_box",
                    "slot.left_name",
                    "slot.right_name",
                    *person_slot_ids("slot.figure.left"),
                    *person_slot_ids("slot.figure.right"),
                    "slot.left_expr",
                    "slot.right_expr",
                ),
            ),
            Region(
                id="region.bottom",
                role="supporting",
                flow="absolute",
                slot_ids=(),
            ),
        ),
        slots=(
            TextSlot(
                id="slot.q_text",
                prompt="",
                text = '계산 결과가 더 큰 사람을 선택해 보세요.', style_role="question",
                x = 75, y = 40, font_size = 25),
            RectSlot(id="slot.left_card", prompt="", x = 120, y = 180, width = 120, height = 60),
            RectSlot(id="slot.right_card", prompt="", x = 310, y = 180, width = 120, height = 60),
            RectSlot(id="slot.left_name_box", prompt="", x = 150, y = 70, width = 60, height = 25),
            RectSlot(id="slot.right_name_box", prompt="", x = 345, y = 70, width = 50, height = 25),
            TextSlot(id="slot.left_name", prompt="", text = '은우', style_role="diagram", x = 165, y = 90, font_size = 20),
            TextSlot(id="slot.right_name", prompt="", text = '도윤', style_role="diagram", x = 355, y = 90, font_size = 20),
            *person_slots("slot.figure.left", cx=180, head_cy=128, body_fill="#D7A0D7"),
            *person_slots("slot.figure.right", cx=370, head_cy=128, body_fill="#8ED7E6"),
            TextSlot(id="slot.left_expr", prompt="", text = '24 × 42', style_role="diagram", x = 130, y = 220, font_size = 25),
            TextSlot(id="slot.right_expr", prompt="", text = '19 × 78', style_role="diagram", x = 325, y = 220, font_size = 25),
        ),
        diagrams=(),
        groups=(),
        constraints=(),
        tags=(),
    )


PROBLEM_TEMPLATE = build_problem_template()

SEMANTIC_OVERRIDE = {
    "problem_id": "S3_초등_3_008563",
    "problem_type": "선택형 비교",
    "metadata": {"grade": 3, "subject": "수학", "topic": "곱셈 결과 비교"},
    "domain": {
        "objects": [
            {"id": "expr_1", "type": "multiplication", "text": "24 × 42"},
            {"id": "expr_2", "type": "multiplication", "text": "19 × 78"},
            {"id": "person_1", "type": "person", "text": "은우"},
            {"id": "person_2", "type": "person", "text": "도윤"},
        ],
        "relations": [],
        "problem_solving": {
            "understand": "두 사람의 곱셈식 결과를 비교해 더 큰 사람을 고르는 문제이다.",
            "plan": "각 식의 결과를 확인하고 크기를 비교한다.",
            "execute": "더 큰 결과에 해당하는 사람을 선택한다.",
            "review": "선택 결과가 조건과 일치하는지 확인한다.",
        },
    },
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {"type": "selected_person", "description": "계산 결과가 더 큰 사람"},
        "value": "도윤",
        "unit": "",
    },
}

SOLVABLE = {
    "schema": "modu.solvable.v1.1",
    "problem_id": "S3_초등_3_008563",
    "problem_type": "선택형 비교",
    "inputs": {
        "target_label": "계산 결과가 더 큰 사람",
        "unit": "",
        "quantities": {
            "expr_1": "24 × 42",
            "expr_2": "19 × 78",
            "person_1": "은우",
            "person_2": "도윤",
        },
    },
    "given": [
        {"ref": "expr_1", "value": "24 × 42"},
        {"ref": "expr_2", "value": "19 × 78"},
    ],
    "target": {"ref": "answer.target", "type": "selected_person"},
    "method": "compare_and_select",
    "plan": ["각 식의 값을 계산한다.", "두 값을 비교한다.", "더 큰 값의 사람을 고른다."],
    "steps": [
        {"id": "step.1", "expr": "24 × 42 와 19 × 78 비교", "value": "도윤이 더 큼"},
        {"id": "step.2", "expr": "정답 사람 선택", "value": "도윤"},
    ],
    "checks": [
        {"id": "check.1", "expr": "선택값 존재 여부", "expected": True, "actual": True, "pass": True},
        {"id": "check.2", "expr": "정답 일치", "expected": "도윤", "actual": "도윤", "pass": True},
    ],
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {"type": "selected_person", "description": "계산 결과가 더 큰 사람"},
        "value": "도윤",
        "unit": "",
    },
}
