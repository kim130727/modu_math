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
) -> tuple[RectSlot, CircleSlot, CircleSlot, CircleSlot, LineSlot]:
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
        id="S3_초등_3_008564",
        title="계산 결과가 더 작은 사람을 선택해 보세요.",
        canvas=Canvas(width=600, height=300, coordinate_mode="logical"),
        regions=(
            Region(id="region.top", role="stem", flow="absolute", slot_ids=("slot.qnum", "slot.qtext")),
            Region(
                id="region.main",
                role="diagram",
                flow="absolute",
                slot_ids=(
                    "slot.box",
                    *person_slot_ids("slot.figure.left"),
                    *person_slot_ids("slot.figure.right"),
                    "slot.choice1",
                    "slot.choice2",
                ),
            ),
            Region(id="region.note", role="supporting", flow="absolute", slot_ids=("slot.note1", "slot.note2")),
        ),
        slots=(
            TextSlot(id="slot.qtext", prompt="", text="계산 결과가 더 작은 사람을 선택해 보세요.", style_role="question", x=84.0, y=24.0, font_size=24),
            RectSlot(id="slot.box", prompt="", x = 85, y = 150, width = 425, height = 65),
            *person_slots("slot.figure.left", cx = 202.5, head_cy = 85.0, body_fill="#D7A0D7"),
            *person_slots("slot.figure.right", cx = 400.0, head_cy = 85.0, body_fill="#8ED7E6"),
            TextSlot(id="slot.choice1", prompt="", text = '민재 73 × 28', style_role="diagram", x = 130, y = 190, font_size = 25),
            TextSlot(id="slot.choice2", prompt="", text = '서윤 31 × 65', style_role="diagram", x = 335, y = 190, font_size = 25),
        ),
        diagrams=(),
        groups=(),
        constraints=(),
        tags=(),
    )


PROBLEM_TEMPLATE = build_problem_template()

SEMANTIC_OVERRIDE = {
    "problem_id": "S3_초등_3_008564",
    "problem_type": "선택형 비교",
    "metadata": {"grade": 3, "subject": "수학", "topic": "곱셈 결과 비교"},
    "domain": {
        "objects": [
            {"id": "expr_1", "type": "expression", "text": "민재 73 × 28"},
            {"id": "expr_2", "type": "expression", "text": "서윤 31 × 65"},
        ],
        "relations": [],
        "problem_solving": {
            "understand": "비교 대상을 읽고 조건에 맞는 항목을 고르는 문제이다.",
            "plan": "각 대상을 비교 가능한 값으로 확인한 뒤 크기를 판단한다.",
            "execute": "조건에 맞는 항목을 선택한다.",
            "review": "선택한 답이 조건과 일치하는지 확인한다.",
        },
    },
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {"type": "selected_option", "description": "조건에 맞는 항목"},
        "value": "서윤",
        "unit": "",
    },
}

SOLVABLE = {
    "schema": "modu.solvable.v1.1",
    "problem_id": "S3_초등_3_008564",
    "problem_type": "선택형 비교",
    "inputs": {
        "target_label": "조건에 맞는 항목",
        "unit": "",
        "quantities": {
            "expr_1": "민재 73 × 28",
            "expr_2": "서윤 31 × 65",
        },
    },
    "given": [
        {"ref": "expr_1", "value": "민재 73 × 28"},
        {"ref": "expr_2", "value": "서윤 31 × 65"},
    ],
    "target": {"ref": "answer.target", "type": "selected_option"},
    "method": "compare_and_select",
    "plan": ["조건을 확인한다.", "대상을 비교한다.", "알맞은 답을 선택한다."],
    "steps": [
        {"id": "step.1", "expr": "비교 조건 확인", "value": "완료"},
        {"id": "step.2", "expr": "정답 선택", "value": "서윤"},
    ],
    "checks": [
        {"id": "check.1", "expr": "선택값 존재 여부", "expected": True, "actual": True, "pass": True},
        {"id": "check.2", "expr": "정답 일치", "expected": "서윤", "actual": "서윤", "pass": True},
    ],
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {"type": "selected_option", "description": "조건에 맞는 항목"},
        "value": "서윤",
        "unit": "",
    },
}


