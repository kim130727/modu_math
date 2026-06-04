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
        id="S3_초등_3_008650",
        title="지름과 반지름의 관계",
        canvas=Canvas(width=960, height=514, coordinate_mode="logical"),
        regions=(
            Region(
                id="region.header",
                role="stem",
                flow="absolute",
                slot_ids=("slot.qnum", "slot.q1", "slot.q2"),
            ),
            Region(
                id="region.diagram",
                role="diagram",
                flow="absolute",
                slot_ids=(
                    "slot.circle",
                    "slot.center",
                    "slot.radius.right",
                    "slot.diameter",
                    "slot.arc.left",
                    "slot.arc.right",
                    "slot.len4",
                    "slot.len2",
                    "slot.smallmark",
                ),
            ),
            Region(
                id="region.choice",
                role="stem",
                flow="absolute",
                slot_ids=("slot.choice.box", "slot.choice.text"),
            ),
            Region(id="region.footer", role="answer", flow="absolute", slot_ids=()),
        ),
        slots=(
            TextSlot(
                id="slot.qnum",
                prompt="",
                text="□ 21.",
                style_role="question",
                x=12.0,
                y=28.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.q1",
                prompt="",
                text="그림을 보고 지름과 반지름 사이의 관계를 알아보려고 합니다. 알맞은",
                style_role="question",
                x=72.0,
                y=28.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.q2",
                prompt="",
                text="것을 선택하세요.",
                style_role="question",
                x=12.0,
                y=64.0,
                font_size=28,
            ),
            CircleSlot(
                id="slot.circle", prompt="", cx=496.0, cy=204.0, r=119.0, fill="none"
            ),
            CircleSlot(
                id="slot.center", prompt="", cx=512.0, cy=205.0, r=3.8, fill="#d81b60"
            ),
            LineSlot(
                id="slot.radius.right",
                prompt="",
                x1=512.0,
                y1=205.0,
                x2=607.0,
                y2=205.0,
            ),
            LineSlot(
                id="slot.diameter", prompt="", x1=432.0, y1=308.0, x2=571.0, y2=85.0
            ),
            LineSlot(
                id="slot.arc.left", prompt="", x1=474.0, y1=100.0, x2=429.0, y2=287.0
            ),
            LineSlot(
                id="slot.arc.right", prompt="", x1=512.0, y1=205.0, x2=607.0, y2=205.0
            ),
            TextSlot(
                id="slot.len4",
                prompt="",
                text="4 cm",
                style_role="label",
                x=437.0,
                y=197.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.len2",
                prompt="",
                text="2 cm",
                style_role="label",
                x=547.0,
                y=246.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.smallmark",
                prompt="",
                text="○",
                style_role="label",
                x=519.0,
                y=206.0,
                font_size=18,
            ),
            RectSlot(
                id="slot.choice.box",
                prompt="",
                x=64.0,
                y=327.0,
                width=840.0,
                height=79.0,
                fill="none",
            ),
            TextSlot(
                id="slot.choice.text",
                prompt="",
                text="한 원에서 ( 지름 , 반지름 )은 ( 지름 , 반지름 )의 2배입니다.",
                style_role="question",
                x=101.0,
                y=376.0,
                font_size=28,
            ),
        ),
        diagrams=(),
        groups=(),
        constraints=(),
        tags=(),
    )


PROBLEM_TEMPLATE = build_problem_template()

SEMANTIC_OVERRIDE = {
    "problem_id": "S3_초등_3_008650",
    "problem_type": "circle_relationship_choice",
    "metadata": {
        "language": "ko",
        "question": "그림을 보고 지름과 반지름 사이의 관계를 알아보려고 합니다. 알맞은 것을 선택하세요.",
        "instruction": "알맞은 것을 선택하세요.",
    },
    "domain": {
        "objects": [
            {"id": "obj.circle", "type": "circle"},
            {"id": "obj.diameter", "type": "segment", "role": "지름"},
            {"id": "obj.radius", "type": "segment", "role": "반지름"},
        ],
        "relations": [],
        "problem_solving": {
            "understand": {
                "given_refs": ["obj.circle", "obj.diameter", "obj.radius"],
                "target_ref": "answer.target",
                "condition_refs": ["rel.diameter_radius"],
            },
            "plan": {
                "method": "개념_판별",
                "description": "그림과 설명을 보고 지름과 반지름의 관계를 선택한다.",
            },
            "execute": {"expected_operations": ["관계_확인", "보기_선택"]},
            "review": {"check_methods": ["설명문_일치확인"]},
        },
    },
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {
            "type": "choice",
            "description": "지름과 반지름의 관계를 나타내는 알맞은 것을 선택",
        },
        "value": 0,
        "unit": "",
    },
}

SOLVABLE = {
    "schema": "modu.solvable.v1.1",
    "problem_id": "S3_초등_3_008650",
    "problem_type": "circle_relationship_choice",
    "inputs": {
        "total_ticks": 0,
        "target_label": "지름과 반지름의 관계",
        "target_ticks": 0,
        "target_count": 0,
        "unit": "",
    },
    "given": [
        {"ref": "obj.circle", "value": {"type": "circle"}},
        {"ref": "obj.diameter", "value": {"role": "지름"}},
        {"ref": "obj.radius", "value": {"role": "반지름"}},
    ],
    "target": {"ref": "answer.target", "type": "choice"},
    "method": "개념_판별",
    "plan": [
        "그림과 해설 문장을 보고 지름과 반지름의 관계를 확인한다.",
        "보기에서 알맞은 말을 고른다.",
    ],
    "steps": [
        {
            "id": "step.1",
            "expr": "한 원에서 지름은 반지름의 2배이다.",
            "value": "지름, 반지름",
        }
    ],
    "checks": [
        {
            "id": "check.1",
            "expr": "해설 문장과 선택 결과가 일치하는가",
            "expected": "지름, 반지름",
            "actual": "지름, 반지름",
            "pass": True,
        }
    ],
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {
            "type": "choice",
            "description": "지름과 반지름의 관계를 나타내는 알맞은 것을 선택",
        },
        "value": 0,
        "unit": "",
    },
}
