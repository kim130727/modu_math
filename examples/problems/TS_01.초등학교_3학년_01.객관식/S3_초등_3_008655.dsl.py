from __future__ import annotations
from modu_math.dsl import (
    Canvas,
    ProblemTemplate,
    Region,
    TextSlot,
    CircleSlot,
    LineSlot,
)


def build_problem_template() -> ProblemTemplate:
    return ProblemTemplate(
        id="S3_초등_3_008655",
        title="원의 반지름",
        canvas=Canvas(width=960, height=520, coordinate_mode="logical"),
        regions=(
            Region(
                id="region.stem",
                role="stem",
                flow="absolute",
                slot_ids=(
                    "slot.q1",
                    "slot.diagram.circle",
                    "slot.diagram.r1",
                    "slot.diagram.r2",
                    "slot.diagram.r3",
                    "slot.diagram.center",
                    "slot.diagram.lb.g",
                    "slot.diagram.lb.n",
                    "slot.diagram.lb.d",
                    "slot.choice",
                ),
            ),
        ),
        slots=(
            TextSlot(
                id="slot.q1",
                prompt="",
                text="□ 30. 선분 ㅇㄱ, 선분 ㅇㄴ, 선분 ㅇㄷ은 모두 원의 반지름입니다. 각 선분의 길이를 재어 알맞은 말을 선택하세요.",
                style_role="question",
                x=18.0,
                y=34.0,
                font_size=28,
            ),
            CircleSlot(
                id="slot.diagram.circle",
                prompt="",
                cx=475.0,
                cy=215.0,
                r=112.0,
                fill="none",
            ),
            LineSlot(
                id="slot.diagram.r1", prompt="", x1=475.0, y1=215.0, x2=375.0, y2=300.0
            ),
            LineSlot(
                id="slot.diagram.r2", prompt="", x1=475.0, y1=215.0, x2=547.0, y2=293.0
            ),
            LineSlot(
                id="slot.diagram.r3", prompt="", x1=475.0, y1=215.0, x2=577.0, y2=193.0
            ),
            CircleSlot(
                id="slot.diagram.center",
                prompt="",
                cx=475.0,
                cy=215.0,
                r=3.5,
                fill="#d81b60",
            ),
            TextSlot(
                id="slot.diagram.lb.g",
                prompt="",
                text="ㄱ",
                style_role="label",
                x=365.0,
                y=312.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.diagram.lb.n",
                prompt="",
                text="ㄴ",
                style_role="label",
                x=555.0,
                y=310.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.diagram.lb.d",
                prompt="",
                text="ㄷ",
                style_role="label",
                x=586.0,
                y=190.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.choice",
                prompt="",
                text="한 원에서 원의 반지름은 모두 ( 같습니다, 다릅니다 ).",
                style_role="question",
                x=175.0,
                y=355.0,
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
    "problem_id": "S3_초등_3_008655",
    "problem_type": "geometry_circle_radius_comparison",
    "metadata": {
        "language": "ko",
        "question": "한 원에서 반지름의 길이가 같은지 묻는 문제",
        "instruction": "알맞은 말을 선택한다.",
    },
    "domain": {
        "objects": [
            {"id": "obj.circle", "type": "circle"},
            {
                "id": "obj.radius_1",
                "type": "segment",
                "name": "ㅇㄱ",
                "property": "radius",
            },
            {
                "id": "obj.radius_2",
                "type": "segment",
                "name": "ㅇㄴ",
                "property": "radius",
            },
            {
                "id": "obj.radius_3",
                "type": "segment",
                "name": "ㅇㄷ",
                "property": "radius",
            },
        ],
        "relations": [],
        "problem_solving": {
            "understand": {
                "given_refs": ["obj.radius_1", "obj.radius_2", "obj.radius_3"],
                "target_ref": "answer.target",
                "condition_refs": ["rel.same_radius"],
            },
            "plan": {
                "method": "compare_equal_radii",
                "description": "한 원에서 반지름들의 길이 관계를 확인한다.",
            },
            "execute": {
                "expected_operations": [
                    "compare_segment_lengths",
                    "select_correct_choice",
                ]
            },
            "review": {"check_methods": ["radius_property_check"]},
        },
    },
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {
            "type": "choice",
            "description": "한 원에서 원의 반지름은 모두 ( 같습니다, 다릅니다 ).",
        },
        "value": 1,
        "unit": "",
    },
}

SOLVABLE = {
    "schema": "modu.solvable.v1.1",
    "problem_id": "S3_초등_3_008655",
    "problem_type": "geometry_circle_radius_comparison",
    "inputs": {
        "total_ticks": 3,
        "target_label": "한 원에서 원의 반지름은 모두 ( 같습니다, 다릅니다 ).",
        "target_ticks": 2,
        "target_count": 3,
        "unit": "",
    },
    "given": [
        {"ref": "obj.radius_1", "value": "ㅇㄱ"},
        {"ref": "obj.radius_2", "value": "ㅇㄴ"},
        {"ref": "obj.radius_3", "value": "ㅇㄷ"},
    ],
    "target": {"ref": "answer.target", "type": "choice"},
    "method": "compare_equal_radii",
    "plan": [
        "한 원의 반지름들은 길이가 같은지 확인한다.",
        "보기에서 알맞은 말을 고른다.",
    ],
    "steps": [
        {
            "id": "step.1",
            "expr": "선분 ㅇㄱ, 선분 ㅇㄴ, 선분 ㅇㄷ은 모두 같은 원의 반지름이다.",
            "value": "same_radius",
        },
        {"id": "step.2", "expr": "한 원의 반지름은 모두 같다.", "value": "같습니다"},
    ],
    "checks": [
        {
            "id": "check.1",
            "expr": "원의 반지름 성질 확인",
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
            "type": "choice",
            "description": "한 원에서 원의 반지름은 모두 ( 같습니다, 다릅니다 ).",
        },
        "value": 1,
        "unit": "",
    },
}
