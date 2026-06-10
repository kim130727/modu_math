from __future__ import annotations
from modu_math.dsl import (
    Canvas,
    ProblemTemplate,
    Region,
    TextSlot,
    RectSlot,
    CircleSlot,
    LineSlot,
    PolygonSlot,
)


def build_problem_template() -> ProblemTemplate:
    return ProblemTemplate(
        id="S3_초등_3_008636",
        title="누름 못과 띠 종이로 원을 그렸습니다",
        canvas=Canvas(width=940, height=620, coordinate_mode="logical"),
        regions=(
            Region(
                id="region.stem",
                role="stem",
                flow="absolute",
                slot_ids=("slot.q1", "slot.q2"),
            ),
            Region(
                id="region.diagram",
                role="diagram",
                flow="absolute",
                slot_ids=(
                    "slot.left.circle",
                    "slot.left.paper",
                    "slot.left.paper.dot1",
                    "slot.left.paper.dot2",
                    "slot.left.paper.dot3",
                    "slot.left.paper.dot4",
                    "slot.left.pin",
                    "slot.left.pencil.body",
                    "slot.left.pencil.tip",
                    "slot.left.pencil.line1",
                    "slot.left.pencil.line2",
                    "slot.arrow",
                    "slot.right.circle",
                    "slot.right.center",
                    "slot.right.radius1",
                    "slot.right.radius2",
                    "slot.right.pt1",
                    "slot.right.pt2",
                ),
            ),
            Region(
                id="region.choice",
                role="answer_choice",
                flow="absolute",
                slot_ids=("slot.choice",'slot.choice.copy4'),
            ),
            Region(
                id="region.explanation",
                role="explanation",
                flow="absolute",
                slot_ids=( ),
            ),
        ),
        slots=(TextSlot(
                id="slot.q1",
                prompt="",
                text = '누름 못과 띠 종이로 원을 그렸습니다. 누름 못이 꽂힌 점에서 원 위에 찍힌', style_role="question",
                x = 5, y = 65, font_size = 30),
            TextSlot(
                id="slot.q2",
                prompt="",
                text = '2개의 점까지의 길이를 각각 재어 알맞은 말을 선택하세요.', style_role="question",
                x = 8, y = 115, font_size = 30),
            CircleSlot(
                id="slot.left.circle",
                prompt="",
                cx = 330, cy = 230, r = 90, fill="none",
            ),
            RectSlot(
                id="slot.left.paper",
                prompt="",
                x = 310, y = 215, width = 130, height = 25, rx=4.0,
                ry=4.0,
                fill="#d2ecfb",
            ),
            CircleSlot(
                id="slot.left.paper.dot1",
                prompt="",
                cx = 330, cy = 230, r = 5, fill="#7a7a7a",
            ),
            CircleSlot(
                id="slot.left.paper.dot2",
                prompt="",
                cx = 360, cy = 230, r = 5, fill="#7a7a7a",
            ),
            CircleSlot(
                id="slot.left.paper.dot3",
                prompt="",
                cx = 390, cy = 230, r = 5, fill="#7a7a7a",
            ),
            CircleSlot(
                id="slot.left.paper.dot4",
                prompt="",
                cx = 420, cy = 230, r = 5, fill="#7a7a7a",
            ),
            CircleSlot(
                id="slot.left.pin", prompt="", cx = 330, cy = 230, r = 5, fill="#8d8d8d"
            ),
            PolygonSlot(
                id="slot.left.pencil.body",
                prompt="",
                points = [[421.39869689941406, 218.47747116088868], [446.39869689941406, 175.17747116088867], [453.39869689941406, 179.17747116088867], [428.39869689941406, 222.47747116088868]], fill = '#f39c82', stroke = '#111111', stroke_width = 2),
            PolygonSlot(
                id="slot.left.pencil.tip",
                prompt="",
                points = [[419.89869689941406, 229.17747116088867], [421.39869689941406, 218.47747116088868], [428.39869689941406, 222.47747116088868]], fill = '#fce4c8', stroke = '#111111', stroke_width = 2),
            LineSlot(
                id="slot.left.pencil.line1",
                prompt="",
                x1 = 425, y1 = 220, x2 = 450, y2 = 175),
            LineSlot(
                id="slot.left.pencil.line2",
                prompt="",
                x1 = 425, y1 = 220, x2 = 450, y2 = 180),
            TextSlot(
                id="slot.arrow",
                prompt="",
                text = '→', style_role="question",
                x = 500, y = 245, font_size = 45),
            CircleSlot(
                id="slot.right.circle",
                prompt="",
                cx = 650, cy = 230, r = 90, fill="none",
            ),
            CircleSlot(
                id="slot.right.center",
                prompt="",
                cx = 650, cy = 230, r = 5, fill="#8d8d8d",
            ),
            LineSlot(
                id="slot.right.radius1",
                prompt="",
                x1 = 650, y1 = 230, x2 = 710, y2 = 165, stroke="#3fa9f5",
                stroke_width=2.5,
            ),
            LineSlot(
                id="slot.right.radius2",
                prompt="",
                x1 = 650, y1 = 230, x2 = 560, y2 = 255, stroke="#3fa9f5",
                stroke_width=2.5,
            ),
            CircleSlot(
                id="slot.right.pt1", prompt="", cx = 710, cy = 165, r = 5, fill="#ff00aa"
            ),
            CircleSlot(
                id="slot.right.pt2",
                prompt="",
                cx = 560, cy = 255, r = 5, fill="#ff00aa",
            ),
            TextSlot(
                id="slot.choice",
                prompt="",
                text = '    누름 못이 꽂힌 점에서 원 위의 한 점까지의 길이는 모두', style_role="question",
                x = 500, y = 375, font_size = 30, anchor="middle",
            ),TextSlot(id = 'slot.choice.copy4', prompt = '', text = '( 같습니다 ,    다릅니다 ).  ', x = 345, y = 430, font_size = 30, fill = '#111111')),
        diagrams=(),
        groups=(),
        constraints=(),
        tags=(),
    )


PROBLEM_TEMPLATE = build_problem_template()

SEMANTIC_OVERRIDE = {
    "problem_id": "S3_초등_3_008636",
    "problem_type": "도형_성질_판단",
    "metadata": {
        "language": "ko",
        "question": "누름 못과 띠 종이로 원을 그렸을 때, 누름 못이 꽂힌 점에서 원 위의 점까지의 길이가 같은지 판단하는 문제",
        "instruction": "알맞은 말을 선택하세요.",
    },
    "domain": {
        "objects": [
            {"id": "obj.center", "type": "point", "role": "중심"},
            {"id": "obj.circle", "type": "circle", "role": "도형"},
            {"id": "obj.point_on_circle_1", "type": "point", "role": "원 위의 점"},
            {"id": "obj.point_on_circle_2", "type": "point", "role": "원 위의 점"},
        ],
        "relations": [],
        "problem_solving": {
            "understand": {
                "given_refs": [
                    "obj.center",
                    "obj.point_on_circle_1",
                    "obj.point_on_circle_2",
                    "obj.circle",
                ],
                "target_ref": "answer.target",
                "condition_refs": ["rel.equal_radius"],
            },
            "plan": {
                "method": "원의 성질 확인",
                "description": "중심에서 원 위의 점까지의 거리가 일정한지 원의 성질을 이용해 판단한다.",
            },
            "execute": {
                "expected_operations": [
                    "원의 중심과 원 위의 점 관계 확인",
                    "같은 반지름인지 판단",
                ]
            },
            "review": {"check_methods": ["원의 반지름 정의와 일치하는지 확인"]},
        },
    },
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {"type": "choice", "description": "같습니다 / 다릅니다 중 알맞은 말"},
        "value": "같습니다",
        "unit": "",
    },
}

SOLVABLE = {
    "schema": "modu.solvable.v1.1",
    "problem_id": "S3_초등_3_008636",
    "problem_type": "도형_성질_판단",
    "inputs": {
        "total_ticks": 0,
        "target_label": "같습니다 / 다릅니다",
        "target_ticks": 0,
        "target_count": 2,
        "unit": "",
    },
    "given": [
        {"ref": "obj.circle", "value": "원"},
        {"ref": "obj.center", "value": "중심"},
        {"ref": "obj.point_on_circle_1", "value": "원 위의 점"},
        {"ref": "obj.point_on_circle_2", "value": "원 위의 점"},
    ],
    "target": {"ref": "answer.target", "type": "choice"},
    "method": "원의 성질 확인",
    "plan": [
        "원의 중심에서 원 위의 점까지의 거리는 반지름이다.",
        "같은 원에서는 반지름의 길이가 모두 같은지 확인한다.",
        "보기에서 알맞은 말을 고른다.",
    ],
    "steps": [
        {"id": "step.1", "expr": "원 위의 두 점은 같은 원에 있다", "value": "같은 원"},
        {
            "id": "step.2",
            "expr": "중심에서 원 위의 점까지의 길이 = 반지름",
            "value": "반지름",
        },
        {"id": "step.3", "expr": "같은 원의 반지름은 서로 같다", "value": "같습니다"},
    ],
    "checks": [
        {
            "id": "check.1",
            "expr": "원의 성질에 따라 중심에서 원 위의 점까지의 거리가 같은가",
            "expected": True,
            "actual": True,
            "pass": True,
        }
    ],
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {"type": "choice", "description": "같습니다 / 다릅니다 중 알맞은 말"},
        "value": "같습니다",
        "unit": "",
    },
}
