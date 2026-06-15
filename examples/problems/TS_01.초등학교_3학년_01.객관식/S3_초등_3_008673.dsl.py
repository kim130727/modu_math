from __future__ import annotations
from modu_math.dsl import (
    Canvas,
    ProblemTemplate,
    Region,
    TextSlot,
    RectSlot,
    CircleSlot,
)


def build_problem_template() -> ProblemTemplate:
    return ProblemTemplate(
        id="S3_초등_3_008673",
        title="원의 중심과 반지름",
        canvas=Canvas(width=926.0, height=487.0, coordinate_mode="logical"),
        regions=(
            Region(
                id="region.header",
                role="stem",
                flow="absolute",
                slot_ids=("slot.stem",),
            ),
            Region(
                id="region.example_box",
                role="diagram",
                flow="absolute",
                slot_ids=(
                    "slot.box",
                    "slot.top.left.c1",
                    "slot.top.left.c2",
                    "slot.top.left.c3",
                    "slot.top.mid.big",
                    "slot.top.mid.small1",
                    "slot.top.mid.small2",
                    "slot.top.right.o1",
                    "slot.top.right.o2",
                    "slot.top.right.o3",
                ),
            ),
            Region(
                id="region.answer_explain",
                role="supporting",
                flow="absolute",
                slot_ids=(),
            ),
            Region(
                id="region.bottom_examples",
                role="supporting",
                flow="absolute",
                slot_ids=(
                    
                ),
            ),
        ),
        slots=(
            TextSlot(
                id="slot.stem",
                prompt="",
                text = '\n    \n    원의 중심을 옮기지 않고 반지름만 다르게 하여 그린 것을\n    선택하세요.\n  ', style_role="question",
                x = 55, y = 45, font_size = 30),
            RectSlot(
                id="slot.box",
                prompt="",
                x = 75, y = 80, width = 780, height = 165, fill="none",
                stroke="#8BC34A",
                stroke_width=2.0,
            ),
            CircleSlot(
                id="slot.top.left.c1",
                prompt="",
                cx = 270, cy = 140, r = 20, fill="none",
                stroke="#333333",
                stroke_width=1.5,
            ),
            CircleSlot(
                id="slot.top.left.c2",
                prompt="",
                cx = 295, cy = 115, r = 20, fill="none",
                stroke="#333333",
                stroke_width=1.5,
            ),
            CircleSlot(
                id="slot.top.left.c3",
                prompt="",
                cx = 325, cy = 85, r = 20, fill="none",
                stroke="#333333",
                stroke_width=1.5,
            ),
            CircleSlot(
                id="slot.top.mid.big",
                prompt="",
                cx = 500, cy = 125, r = 45, fill="none",
                stroke="#333333",
                stroke_width=1.5,
            ),
            CircleSlot(
                id="slot.top.mid.small1",
                prompt="",
                cx = 500, cy = 90, r = 15, fill="none",
                stroke="#333333",
                stroke_width=1.5,
            ),
            CircleSlot(
                id="slot.top.mid.small2",
                prompt="",
                cx = 500, cy = 75, r = 10, fill="none",
                stroke="#333333",
                stroke_width=1.5,
            ),
            CircleSlot(
                id="slot.top.right.o1",
                prompt="",
                cx = 670, cy = 125, r = 35, fill="none",
                stroke="#333333",
                stroke_width=1.5,
            ),
            CircleSlot(
                id="slot.top.right.o2",
                prompt="",
                cx = 670, cy = 125, r = 25, fill="none",
                stroke="#333333",
                stroke_width=1.5,
            ),
            CircleSlot(
                id="slot.top.right.o3",
                prompt="",
                cx = 670, cy = 125, r = 15, fill="none",
                stroke="#333333",
                stroke_width=1.5,
            ),
            
            
        ),
        diagrams=(),
        groups=(),
        constraints=(),
        tags=(),
    )


PROBLEM_TEMPLATE = build_problem_template()

SEMANTIC_OVERRIDE = {
    "problem_id": "S3_초등_3_008673",
    "problem_type": "도형_비교",
    "metadata": {
        "language": "ko",
        "question": "원의 중심을 옮기지 않고 반지름만 다르게 하여 그린 것을 선택하는 문제",
        "instruction": "원의 중심을 옮기지 않고 반지름만 다르게 하여 그린 것을 선택하세요.",
    },
    "domain": {
        "objects": [
            {"id": "obj.circle_group", "type": "circle_set"},
            {"id": "obj.center", "type": "center"},
            {"id": "obj.radius", "type": "radius"},
        ],
        "relations": [],
        "problem_solving": {
            "understand": {
                "given_refs": ["obj.circle_group"],
                "target_ref": "answer.target",
                "condition_refs": ["rel.center_fixed", "rel.radius_varies"],
            },
            "plan": {
                "method": "도형의 중심과 반지름 비교",
                "description": "중심이 같은지, 반지름이 달라지는지를 비교한다.",
            },
            "execute": {
                "expected_operations": [
                    "중심 비교",
                    "반지름 비교",
                    "조건에 맞는 그림 선택",
                ]
            },
            "review": {
                "check_methods": ["중심 동일 여부 확인", "반지름 변화 여부 확인"]
            },
        },
    },
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {
            "type": "circle_diagram_selection",
            "description": "원의 중심을 옮기지 않고 반지름만 다르게 하여 그린 것",
        },
        "value": 1,
        "unit": "",
    },
}

SOLVABLE = {
    "schema": "modu.solvable.v1.1",
    "problem_id": "S3_초등_3_008673",
    "problem_type": "도형_비교",
    "inputs": {
        "total_ticks": 3,
        "target_label": "원의 중심을 옮기지 않고 반지름만 다르게 하여 그린 것",
        "target_ticks": 1,
        "target_count": 1,
        "unit": "",
    },
    "given": [{"ref": "obj.circle_group", "value": "원 그림 묶음"}],
    "target": {"ref": "answer.target", "type": "circle_diagram_selection"},
    "method": "도형의 중심과 반지름 비교",
    "plan": [
        "그림마다 원의 중심이 같은지 확인한다.",
        "반지름이 달라지는지 확인한다.",
        "조건에 맞는 그림을 선택한다.",
    ],
    "steps": [
        {
            "id": "step.1",
            "expr": "중심이 같고 반지름이 다른 원 묶음 찾기",
            "value": "조건 확인",
        },
        {
            "id": "step.2",
            "expr": "중심이 같지 않거나 반지름 변화가 없는 그림 제외",
            "value": "후보 제외",
        },
        {"id": "step.3", "expr": "조건에 맞는 그림 선택", "value": "정답 도형 선택"},
    ],
    "checks": [
        {
            "id": "check.1",
            "expr": "중심이 옮겨지지 않았는가",
            "expected": True,
            "actual": True,
            "pass": True,
        },
        {
            "id": "check.2",
            "expr": "반지름만 달라졌는가",
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
            "type": "circle_diagram_selection",
            "description": "원의 중심을 옮기지 않고 반지름만 다르게 하여 그린 것",
        },
        "value": 1,
        "unit": "",
    },
}
