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
        title="반지름의 개수",
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
                slot_ids=("slot.ans", "slot.exp"),
            ),
        ),
        slots=(
            TextSlot(
                id="slot.q1",
                prompt="",
                text="□ 12. 원에 반지를를 3개 그은 것입니다. 한 원에 반지를를 몇 개 그을 수 있는지",
                style_role="question",
                x=16.0,
                y=34.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.q2",
                prompt="",
                text="알맞은 것을 선택하세요.",
                style_role="question",
                x=16.0,
                y=70.0,
                font_size=28,
            ),
            CircleSlot(
                id="slot.circle.boundary",
                prompt="",
                cx=471.0,
                cy=206.0,
                r=134.0,
                fill="none",
            ),
            CircleSlot(
                id="slot.circle.center",
                prompt="",
                cx=490.0,
                cy=208.0,
                r=3.5,
                fill="#e91e63",
            ),
            CircleSlot(
                id="slot.circle.marker",
                prompt="",
                cx=484.0,
                cy=193.0,
                r=4.5,
                fill="none",
            ),
            LineSlot(
                id="slot.radius.left", prompt="", x1=490.0, y1=208.0, x2=355.0, y2=214.0
            ),
            LineSlot(
                id="slot.radius.up_right",
                prompt="",
                x1=490.0,
                y1=208.0,
                x2=580.0,
                y2=131.0,
            ),
            LineSlot(
                id="slot.radius.down", prompt="", x1=490.0, y1=208.0, x2=474.0, y2=344.0
            ),
            RectSlot(
                id="slot.choice.box",
                prompt="",
                x=95.0,
                y=328.0,
                width=760.0,
                height=78.0,
                fill="none",
            ),
            TextSlot(
                id="slot.choice.text",
                prompt="",
                text="( 무수히 많이 그을 수 있습니다. , 3개 )",
                style_role="choice",
                x=500.0,
                y=373.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.ans",
                prompt="",
                text="(정답)무수히 많이 그을 수 있습니다.",
                style_role="supporting",
                x=16.0,
                y=435.0,
                font_size=22,
            ),
            TextSlot(
                id="slot.exp",
                prompt="",
                text="(해설)반지름은 원의 중심과 원 위의 한 점을 이은 선분이이므로 무수히 많이 그을 수 있습니다.",
                style_role="supporting",
                x=16.0,
                y=478.0,
                font_size=20,
            ),
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
        "value": 0,
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
        "value": 0,
        "unit": "",
    },
}
