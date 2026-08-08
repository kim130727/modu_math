from __future__ import annotations
from modu_math.dsl import (
    Canvas,
    CircleSlot,
    LineSlot,
    ProblemTemplate,
    RectSlot,
    Region,
    TextSlot,
)

def build_problem_template() -> ProblemTemplate:
    return ProblemTemplate(
        id="S3_초등_3_008639",
        title="한 원의 반지름의 성질을 묻는 보기 선택형 문제",
        canvas=Canvas(width=900, height=650, coordinate_mode="logical"),
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
                    "slot.circle.boundary",
                    "slot.circle.center",
                    "slot.circle.marker",
                    "slot.radius.left",
                    "slot.radius.up_right",
                    "slot.radius.down",
                ),
            ),
            Region(
                id="region.choice",
                role="choice",
                flow="absolute",
                slot_ids=("slot.choice.box", "slot.choice.text"),
            ),
            Region(id="region.answer", role="answer", flow="absolute", slot_ids=()),
            Region(
                id="region.explanation",
                role="explanation",
                flow="absolute",
                slot_ids=( ),
            ),
        ),
        slots=(
            TextSlot(
                id="slot.q1",
                prompt="",
                text = '원에 반지름을 3개 그은 것입니다. 반지름을 재어 알맞은 말을 선택하세요', style_role="question",
                x=16.0,
                y=34.0,
                font_size=28,
            ),
            CircleSlot(
                id="slot.circle.boundary",
                prompt="",
                cx = 395, cy = 215, r = 135, fill="none",
            ),
            CircleSlot(
                id="slot.circle.center",
                prompt="",
                cx = 400, cy = 220, r = 5, fill="#e91e63",
            ),
            CircleSlot(
                id="slot.circle.marker",
                prompt="",
                cx = 398, cy = 200, r = 5, fill="none",
            ),
            LineSlot(
                id="slot.radius.left", prompt="", x1 = 401, y1 = 220, x2 = 261, y2 = 230),
            LineSlot(
                id="slot.radius.up_right",
                prompt="",
                x1 = 401, y1 = 217, x2 = 511, y2 = 147),
            LineSlot(
                id="slot.radius.down", prompt="", x1 = 400, y1 = 220, x2 = 385, y2 = 350),
            RectSlot(
                id="slot.choice.box",
                prompt="",
                x = 110, y = 385, width = 685, height = 80, fill="none",
            ),
            TextSlot(
                id="slot.choice.text",
                prompt="",
                text = '한원의 반지름은 모두 (같습니다, 다릅니다).', style_role="choice",
                x = 190, y = 435, font_size = 30),
            
            
        ),
        diagrams=(),
        groups=(),
        constraints=(),
        tags=(),
    )


PROBLEM_TEMPLATE = build_problem_template()

SEMANTIC_OVERRIDE = {
    "problem_id": "S3_초등_3_008639",
    "problem_type": "multiple_choice_geometry",
    "metadata": {
        "language": "ko",
        "question": "한 원의 반지름의 성질을 묻는 보기 선택형 문제",
        "instruction": "알맞은 말을 선택한다.",
    },
    "domain": {
        "objects": [
            {"id": "obj.circle", "type": "circle"},
            {"id": "obj.radius_set", "type": "radius_set", "count": 3},
        ],
        "relations": [],
        "problem_solving": {
            "understand": {
                "given_refs": ["obj.circle", "obj.radius_set"],
                "target_ref": "answer.target",
                "condition_refs": ["rel.radius_of_circle", "rel.radius_equality"],
            },
            "plan": {
                "method": "geometry_property_recognition",
                "description": "한 원에서 반지름의 성질을 확인한다.",
            },
            "execute": {"expected_operations": ["identify_radius", "compare_lengths"]},
            "review": {"check_methods": ["property_check"]},
        },
    },
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {
            "type": "multiple_choice_selection",
            "description": "한 원에서 원의 반지름들은 모두 ( 같습니다, 다릅니다 ).",
        },
        "value": "같습니다",
        "unit": "",
    },
}

SOLVABLE = {
    "schema": "modu.solvable.v1.1",
    "problem_id": "S3_초등_3_008639",
    "problem_type": "multiple_choice_geometry",
    "inputs": {
        "total_ticks": 0,
        "target_label": "반지름의 성질",
        "target_ticks": 0,
        "target_count": 3,
        "unit": "",
    },
    "given": [
        {"ref": "obj.circle", "value": {"type": "circle"}},
        {"ref": "obj.radius_set", "value": {"count": 3}},
    ],
    "target": {"ref": "answer.target", "type": "multiple_choice_selection"},
    "method": "geometry_property_recognition",
    "plan": [
        "한 원의 반지름이라는 도형 성질을 확인한다.",
        "그림에 그려진 3개의 선분이 모두 반지름인지 본다.",
        "반지름의 길이 관계를 판단한다.",
    ],
    "steps": [
        {
            "id": "step.1",
            "expr": "한 원의 반지름은 모두 같은 길이이다.",
            "value": "같습니다",
        }
    ],
    "checks": [
        {
            "id": "check.1",
            "expr": "반지름의 성질과 일치하는가",
            "expected": "같습니다",
            "actual": "같습니다",
            "pass": True,
        }
    ],
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {
            "type": "multiple_choice_selection",
            "description": "한 원에서 원의 반지름들은 모두 ( 같습니다, 다릅니다 ).",
        },
        "value": "같습니다",
        "unit": "",
    },
}
