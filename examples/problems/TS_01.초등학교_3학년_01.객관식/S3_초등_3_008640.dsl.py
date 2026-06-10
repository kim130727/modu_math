from __future__ import annotations
from modu_math.dsl import (
    Canvas,
    ProblemTemplate,
    Region,
    TextSlot,
    RectSlot,
    LineSlot,
    CircleSlot,
)


def build_problem_template() -> ProblemTemplate:
    return ProblemTemplate(
        id="S3_초등_3_008640",
        title="한 원의 반지름의 개수를 묻는 객관식 문제",
        canvas=Canvas(width=960, height=650, coordinate_mode="logical"),
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
                text = '원에 반지름을 3개 그은 것입니다. 한 원에 반지름을 몇 개 그을 수 있는지\n알맞은 것을 선택하세요', style_role="question",
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
    "problem_id": "S3_초등_3_008640",
    "problem_type": "multiple_choice_concept",
    "metadata": {
        "language": "ko",
        "question": "원에서 반지름의 개수를 묻는 객관식 문제",
        "instruction": "알맞은 것을 선택하세요.",
    },
    "domain": {
        "objects": [
            {"id": "obj.circle", "type": "circle"},
            {"id": "obj.center", "type": "center", "belongs_to": "obj.circle"},
            {
                "id": "obj.radius",
                "type": "segment",
                "meaning": "원의 중심과 원 위의 한 점을 이은 선분",
                "belongs_to": "obj.circle",
            },
        ],
        "relations": [],
        "problem_solving": {
            "understand": {
                "given_refs": ["obj.circle", "obj.center", "obj.radius"],
                "target_ref": "answer.target",
                "condition_refs": ["rel.radius_definition"],
            },
            "plan": {
                "method": "concept_identification",
                "description": "그림과 해설을 보고 반지름의 뜻을 확인한다.",
            },
            "execute": {
                "expected_operations": [
                    "identify_radius_definition",
                    "match_to_answer_choice",
                ]
            },
            "review": {"check_methods": ["definition_match_check"]},
        },
    },
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {
            "type": "correct_choice",
            "description": "반지름은 무수히 많이 그을 수 있다.",
        },
        "value": "무수히 많이 그을 수 있습니다.",
        "unit": "",
    },
}

SOLVABLE = {
    "schema": "modu.solvable.v1.1",
    "problem_id": "S3_초등_3_008640",
    "problem_type": "multiple_choice_concept",
    "inputs": {
        "total_ticks": 1,
        "target_label": "반지름의 개수",
        "target_ticks": 1,
        "target_count": 1,
        "unit": "",
    },
    "given": [
        {"ref": "obj.circle", "value": {"type": "circle"}},
        {"ref": "obj.center", "value": {"type": "center"}},
        {
            "ref": "obj.radius",
            "value": {
                "type": "segment",
                "meaning": "원의 중심과 원 위의 한 점을 이은 선분",
            },
        },
    ],
    "target": {"ref": "answer.target", "type": "correct_choice"},
    "method": "concept_identification",
    "plan": [
        "그림과 해설에서 반지름의 정의를 확인한다.",
        "반지름은 중심과 원 위의 점을 잇는 선분임을 이용한다.",
        "보기 중 알맞은 설명을 고른다.",
    ],
    "steps": [
        {
            "id": "step.1",
            "expr": "반지름의 정의 확인",
            "value": "원의 중심과 원 위의 한 점을 이은 선분",
        },
        {
            "id": "step.2",
            "expr": "그림에 보이는 반지름의 개념 적용",
            "value": "무수히 많이 그을 수 있음",
        },
    ],
    "checks": [
        {
            "id": "check.1",
            "expr": "정의와 일치하는가",
            "expected": "원의 중심과 원 위의 한 점을 이은 선분",
            "actual": "원의 중심과 원 위의 한 점을 이은 선분",
            "pass": True,
        }
    ],
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {
            "type": "correct_choice",
            "description": "반지름은 무수히 많이 그을 수 있다.",
        },
        "value": "무수히 많이 그을 수 있습니다.",
        "unit": "",
    },
}
