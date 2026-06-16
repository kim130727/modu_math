from __future__ import annotations
from modu_math.dsl import (
    Canvas,
    ProblemTemplate,
    Region,
    TextSlot,
    RectSlot,
    CircleSlot,
    LineSlot,
)


def build_problem_template() -> ProblemTemplate:
    return ProblemTemplate(
        id="S3_초등_3_008677",
        title="원의 반지름",
        canvas=Canvas(width=800.0, height=390.0, coordinate_mode="logical"),
        regions=(
            Region(
                id="region.stem",
                role="stem",
                flow="absolute",
                slot_ids=("slot.qtext",),
            ),
            Region(
                id="region.diagram",
                role="diagram",
                flow="absolute",
                slot_ids=(
                    "slot.circle",
                    "slot.seg1",
                    "slot.seg2",
                    "slot.seg3",
                    "slot.pt.center",
                    "slot.lb.g1",
                    "slot.lb.g2",
                    "slot.lb.g3",
                    "slot.lb.g4",
                    "slot.lb.o",
                ),
            ),
            Region(
                id="region.choices",
                role="choices",
                flow="absolute",
                slot_ids=(
                    "slot.choice_box",
                    "slot.choice1",
                    "slot.choice2",
                    "slot.choice3",
                ),
            ),
            Region(id="region.answer", role="answer", flow="absolute", slot_ids=()),
        ),
        slots=(
            TextSlot(
                id="slot.qtext",
                prompt="",
                text="원의 반지름을 나타내는 선분을 찾아 선택하세요.",
                style_role="question",
                x=90.0,
                y=24.0,
                font_size=28,
            ),
            CircleSlot(
                id="slot.circle", prompt="", cx = 405, cy = 165, r = 120, fill="none"
            ),
            LineSlot(id="slot.seg1", prompt="", x1 = 292, y1 = 205, x2 = 517, y2 = 125),
            LineSlot(id="slot.seg2", prompt="", x1 = 515, y1 = 125, x2 = 515, y2 = 210),
            LineSlot(id="slot.seg3", prompt="", x1 = 405, y1 = 165, x2 = 405, y2 = 285),
            CircleSlot(
                id="slot.pt.center",
                prompt="",
                cx = 405, cy = 165, r = 5, fill="#ff4aa5",
            ),
            TextSlot(
                id="slot.lb.g1",
                prompt="",
                text = 'ㄱ', style_role="label",
                x = 255, y = 225, font_size = 30),
            TextSlot(
                id="slot.lb.g2",
                prompt="",
                text = 'ㄴ', style_role="label",
                x = 415, y = 260, font_size = 30),
            TextSlot(
                id="slot.lb.g3",
                prompt="",
                text = 'ㄷ', style_role="label",
                x = 480, y = 215, font_size = 30),
            TextSlot(
                id="slot.lb.g4",
                prompt="",
                text = 'ㄹ', style_role="label",
                x = 525, y = 120, font_size = 30),
            TextSlot(
                id="slot.lb.o",
                prompt="",
                text = 'ㅇ', style_role="label",
                x = 380, y = 150, font_size = 30),
            RectSlot(
                id="slot.choice_box",
                prompt="",
                x = 95, y = 305, width = 580, height = 65, fill="none",
            ),
            TextSlot(
                id="slot.choice1",
                prompt="",
                text = '1. 선분 ㄱㄹ', style_role="choice",
                x = 135, y = 345, font_size = 30),
            TextSlot(
                id="slot.choice2",
                prompt="",
                text = '2. 선분 ㅇㄴ', style_role="choice",
                x = 310, y = 345, font_size = 30),
            TextSlot(
                id="slot.choice3",
                prompt="",
                text = '3. 선분 ㄷㄹ', style_role="choice",
                x = 490, y = 345, font_size = 30),
        ),
        diagrams=(),
        groups=(),
        constraints=(),
        tags=(),
    )


PROBLEM_TEMPLATE = build_problem_template()

SEMANTIC_OVERRIDE = {
    "problem_id": "S3_초등_3_008677",
    "problem_type": "geometry_circle_radius_selection",
    "metadata": {
        "language": "ko",
        "question": "원의 반지름을 나타내는 선분을 찾는 선택형 문제",
        "instruction": "원의 반지름을 나타내는 선분을 찾아 선택하세요.",
    },
    "domain": {
        "objects": [
            {"id": "obj.circle", "type": "circle"},
            {"id": "obj.center", "type": "point", "label": "O", "role": "center_like"},
            {"id": "obj.segment.on", "type": "segment", "label": "Oㄴ"},
        ],
        "relations": [],
        "problem_solving": {
            "understand": {
                "given_refs": ["obj.circle", "obj.center"],
                "target_ref": "answer.target",
                "condition_refs": ["rel.radius_definition"],
            },
            "plan": {
                "method": "definition_matching",
                "description": "원의 중심과 원 위의 한 점을 이은 선분을 찾는다.",
            },
            "execute": {
                "expected_operations": [
                    "identify_center",
                    "identify_point_on_circle",
                    "match_segment_to_radius_definition",
                ]
            },
            "review": {"check_methods": ["definition_check"]},
        },
    },
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {"type": "segment", "description": "원의 반지름을 나타내는 선분"},
        "value": 2,
        "unit": "",
    },
}

SOLVABLE = {
    "schema": "modu.solvable.v1.1",
    "problem_id": "S3_초등_3_008677",
    "problem_type": "geometry_circle_radius_selection",
    "inputs": {
        "total_ticks": 1,
        "target_label": "반지름",
        "target_ticks": 1,
        "target_count": 1,
        "unit": "",
    },
    "given": [
        {"ref": "obj.circle", "value": {"type": "circle"}},
        {"ref": "obj.center", "value": {"label": "O"}},
        {"ref": "obj.segment.on", "value": {"label": "Oㄴ"}},
    ],
    "target": {"ref": "answer.target", "type": "segment"},
    "method": "definition_matching",
    "plan": [
        "원의 중심과 원 위의 한 점을 이은 선분이 반지름인지 확인한다.",
        "보기 중 해당하는 선분을 고른다.",
    ],
    "steps": [
        {
            "id": "step.1",
            "expr": "원의 중심 O와 원 위의 한 점 ㄴ을 이은 선분 확인",
            "value": "Oㄴ",
        },
        {
            "id": "step.2",
            "expr": "반지름의 정의와 일치하는 보기 선택",
            "value": "선분 Oㄴ",
        },
    ],
    "checks": [
        {
            "id": "check.1",
            "expr": "중심 O에서 원 위의 점 ㄴ으로 이어지는가",
            "expected": True,
            "actual": True,
            "pass": True,
        }
    ],
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {"type": "segment", "description": "원의 반지름을 나타내는 선분"},
        "value": 2,
        "unit": "",
    },
}
