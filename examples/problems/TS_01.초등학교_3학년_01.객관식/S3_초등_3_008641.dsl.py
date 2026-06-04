from __future__ import annotations
from modu_math.dsl import (
    Canvas,
    ProblemTemplate,
    Region,
    TextSlot,
    RectSlot,
    LineSlot,
    CircleSlot,
    PathSlot,
)


def build_problem_template() -> ProblemTemplate:
    return ProblemTemplate(
        id="S3_초등_3_008641",
        title="원의 지름",
        canvas=Canvas(width=940, height=640, coordinate_mode="logical"),
        regions=(
            Region(
                id="region.stem", role="stem", flow="absolute", slot_ids=("slot.q1",)
            ),
            Region(
                id="region.diagram",
                role="diagram",
                flow="absolute",
                slot_ids=(
                    "slot.circle",
                    "slot.center",
                    "slot.diameter.vertical",
                    "slot.diameter.green",
                    "slot.diameter.purple",
                    "slot.label.eunji",
                    "slot.label.jina",
                    "slot.label.hyeonjun",
                    "slot.note.arrow",
                    "slot.note.text",
                ),
            ),
            Region(
                id="region.choice",
                role="choice",
                flow="absolute",
                slot_ids=("slot.choice.box", "slot.choice.text"),
            ),
            Region(id="region.footer", role="footer", flow="absolute", slot_ids=()),
        ),
        slots=(
            TextSlot(
                id="slot.q1",
                prompt="",
                text="13. 은지, 진아, 현준이가 한 원에 지름을 그은 것입니다. 지름을 재어 알맞은 말을 선택하세요.",
                style_role="question",
                x=18.0,
                y=34.0,
                font_size=28,
            ),
            CircleSlot(
                id="slot.circle", prompt="", cx=455.0, cy=205.0, r=100.0, fill="none"
            ),
            CircleSlot(
                id="slot.center", prompt="", cx=455.0, cy=231.0, r=3.5, fill="#d02aa6"
            ),
            LineSlot(
                id="slot.diameter.vertical",
                prompt="",
                x1=455.0,
                y1=105.0,
                x2=455.0,
                y2=305.0,
            ),
            LineSlot(
                id="slot.diameter.green",
                prompt="",
                x1=366.0,
                y1=151.0,
                x2=544.0,
                y2=259.0,
            ),
            LineSlot(
                id="slot.diameter.purple",
                prompt="",
                x1=363.0,
                y1=261.0,
                x2=547.0,
                y2=199.0,
            ),
            TextSlot(
                id="slot.label.eunji",
                prompt="",
                text="은지",
                style_role="label",
                x=438.0,
                y=92.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.label.jina",
                prompt="",
                text="진아",
                style_role="label",
                x=558.0,
                y=170.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.label.hyeonjun",
                prompt="",
                text="현준",
                style_role="label",
                x=559.0,
                y=288.0,
                font_size=28,
            ),
            PathSlot(
                id="slot.note.arrow",
                prompt="",
                d="M 500.0 303.0 C 488.0 289.0, 484.0 272.0, 473.0 257.0 C 467.0 247.0, 461.0 239.0, 455.0 231.0",
            ),
            TextSlot(
                id="slot.note.text",
                prompt="",
                text="지름은 모두\n원의 중심을\n지나요.",
                style_role="note",
                x=500.0,
                y=315.0,
                font_size=24,
            ),
            RectSlot(
                id="slot.choice.box",
                prompt="",
                x=95.0,
                y=414.0,
                width=760.0,
                height=80.0,
            ),
            TextSlot(
                id="slot.choice.text",
                prompt="",
                text="한 원에서 원의 지름은 모두 ( 같습니다, 다릅니다 ).",
                style_role="choice",
                x=170.0,
                y=469.0,
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
    "problem_id": "S3_초등_3_008641",
    "problem_type": "concept_choice",
    "metadata": {
        "language": "ko",
        "question": "한 원에서 지름의 성질을 보고 알맞은 말을 고르는 문제",
        "instruction": "지름을 재어 알맞은 말을 선택하세요.",
    },
    "domain": {
        "objects": [
            {"id": "obj.circle", "type": "circle"},
            {"id": "obj.diameter.1", "type": "diameter", "owner": "은지"},
            {"id": "obj.diameter.2", "type": "diameter", "owner": "진아"},
            {"id": "obj.diameter.3", "type": "diameter", "owner": "현준"},
            {"id": "obj.center", "type": "center"},
        ],
        "relations": [],
        "problem_solving": {
            "understand": {
                "given_refs": [
                    "obj.circle",
                    "obj.diameter.1",
                    "obj.diameter.2",
                    "obj.diameter.3",
                ],
                "target_ref": "answer.target",
                "condition_refs": ["rel.diameter_equality"],
            },
            "plan": {
                "method": "concept_recognition",
                "description": "한 원에서 지름의 성질을 떠올려 알맞은 선택지를 고른다.",
            },
            "execute": {
                "expected_operations": [
                    "identify_diameter_property",
                    "compare_choice_words",
                ]
            },
            "review": {"check_methods": ["property_consistency_check"]},
        },
    },
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {
            "type": "choice_word",
            "description": "한 원에서 원의 지름은 모두 ( 같습니다, 다릅니다 )에서 알맞은 말",
        },
        "value": "같습니다",
        "unit": "",
    },
}

SOLVABLE = {
    "schema": "modu.solvable.v1.1",
    "problem_id": "S3_초등_3_008641",
    "problem_type": "concept_choice",
    "inputs": {
        "total_ticks": 0,
        "target_label": "같습니다",
        "target_ticks": 0,
        "target_count": 3,
        "unit": "",
    },
    "given": [
        {"ref": "obj.circle", "value": {"type": "circle"}},
        {"ref": "obj.diameter.1", "value": {"owner": "은지", "type": "diameter"}},
        {"ref": "obj.diameter.2", "value": {"owner": "진아", "type": "diameter"}},
        {"ref": "obj.diameter.3", "value": {"owner": "현준", "type": "diameter"}},
    ],
    "target": {"ref": "answer.target", "type": "choice_word"},
    "method": "concept_recognition",
    "plan": [
        "한 원에서 지름의 성질을 확인한다.",
        "보기의 두 말 중 알맞은 말을 고른다.",
    ],
    "steps": [
        {
            "id": "step.1",
            "expr": "한 원의 지름은 모두 같은 성질을 가진다.",
            "value": "같다",
        },
        {
            "id": "step.2",
            "expr": "선택지 ( 같습니다, 다릅니다 ) 중 알맞은 말 선택",
            "value": "같습니다",
        },
    ],
    "checks": [
        {
            "id": "check.1",
            "expr": "지름의 성질과 선택어가 일치하는가",
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
            "type": "choice_word",
            "description": "한 원에서 원의 지름은 모두 ( 같습니다, 다릅니다 )에서 알맞은 말",
        },
        "value": "같습니다",
        "unit": "",
    },
}
