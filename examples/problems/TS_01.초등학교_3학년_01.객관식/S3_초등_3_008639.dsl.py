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
        title="원의 반지름",
        canvas=Canvas(width=900, height=520, coordinate_mode        regions=(
            Region(
                id="region.stem",
                role="stem",
                flow="absolute",
                slot_ids=(
                    "slot.q1",
                    "slot.diagram.circle",
                    "slot.diagram.radius1",
                    "slot.diagram.radius2",
                    "slot.diagram.radius3",
                    "slot.diagram.center_mark.outer",
                    "slot.diagram.center_mark.inner",
                    "slot.diagram.center_label",
                ),
            ),
            Region(
                id="region.choice",
                role="body",
                flow="absolute",
                slot_ids=("slot.choice.box", "slot.choice.text"),
            ),
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
                text="□ 11. 원에 반지름을 3개 그은 것입니다. 반지름을 재어 알맞은 말을 선택하세요.",
                style_role="question",
                x=18.0,
                y=32.0,
                font_size=28,
            ),
            CircleSlot(
                id="slot.diagram.circle",
                prompt="",
                cx=486.0,
                cy=165.0,
                r=119.0,
                fill="none",
            ),
            LineSlot(
                id="slot.diagram.radius1",
                prompt="",
                x1=486.0,
                y1=165.0,
                x2=577.9,
                y2=89.4,
                stroke="#8584b4",
                stroke_width=2.5,
            ),
            LineSlot(
                id="slot.diagram.radius2",
                prompt="",
                x1=486.0,
                y1=165.0,
                x2=367.2,
                y2=171.3,
                stroke="#00aeef",
                stroke_width=2.5,
            ),
            LineSlot(
                id="slot.diagram.radius3",
                prompt="",
                x1=486.0,
                y1=165.0,
                x2=469.2,
                y2=282.8,
                stroke="#3cb878",
                stroke_width=2.5,
            ),
            CircleSlot(
                id="slot.diagram.center_mark.outer",
                prompt="",
                cx=486.0,
                cy=165.0,
                r=5.0,
                fill="none",
            ),
            CircleSlot(
                id="slot.diagram.center_mark.inner",
                prompt="",
                cx=486.0,
                cy=165.0,
                r=2.5,
                fill="#ff2aa6",
            ),
            TextSlot(
                id="slot.diagram.center_label",
                prompt="",
                text="ㅇ",
                style_role="question",
                x=486.0,
                y=148.0,
                font_size=20,
                anchor="middle",
            ),
            RectSlot(
                id="slot.choice.box",
                prompt="",
                x=95.0,
                y=291.0,
                width=731.0,
                height=78.0,
                stroke="#8cc63f",
                stroke_width=2.0,
                fill="none",
            ),
            TextSlot(
                id="slot.choice.text",
                prompt="",
                text="한 원에서 원의 반지름들은 모두 ( 같습니다 , 다릅니다 ).",
                style_role="question",
                x=460.5,
                y=339.0,
                font_size=28,
                anchor="middle",
            ),
            TextSlot(
                id="slot.ans",
                prompt="",
                text="(정답)같습니다",
                style_role="supporting",
                x=18.0,
                y=390.0,
                font_size=22,
            ),
            TextSlot(
                id="slot.exp",
                prompt="",
                text="(해설)반지름은 모두 같습니다.",
                style_role="supporting",
                x=18.0,
                y=430.0,
                font_size=20,
            ),�니다.",
                style_role="supporting",
                x=18.0,
                y=430.0,
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
