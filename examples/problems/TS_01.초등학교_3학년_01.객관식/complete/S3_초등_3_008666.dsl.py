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
        id="S3_초등_3_008666",
        title="원의 반지름과 중심 이동",
        canvas=Canvas(width=900, height=400, coordinate_mode="logical"),
        regions=(
            Region(
                id="region.stem",
                role="stem",
                flow="absolute",
                slot_ids=(
                    "slot.qtext1",
                    "slot.qtext1.copy5",
                    "slot.qtext1.copy5.copy6",
                    "slot.qtext1.copy5.copy7",
                ),
            ),
            Region(
                id="region.options",
                role="diagram",
                flow="absolute",
                slot_ids=(
                    "slot.box",
                    "slot.opt1.c1",
                    "slot.opt1.c2",
                    "slot.opt1.c3",
                    "slot.opt2.c1",
                    "slot.opt2.c2",
                    "slot.opt3.c1",
                    "slot.opt3.c2",
                    "slot.opt3.c3",
                    "slot.opt3.c2.copy4",
                ),
            ),
            Region(
                id="region.answer",
                role="annotation",
                flow="absolute",
                slot_ids=(),
            ),
            Region(
                id="region.explanation",
                role="explanation",
                flow="absolute",
                slot_ids=(),
            ),
            Region(
                id="region.bottom_diagrams",
                role="diagram",
                flow="absolute",
                slot_ids=(),
            ),
        ),
        slots=(
            TextSlot(
                id="slot.qtext1",
                prompt="",
                text="\n    \n    원의 반지름은 모두 같고 원의 중심을 옮겨 가며 그린 그림을\n    찾아 선택하세요.    \n  ",
                style_role="question",
                x=65,
                y=20,
                font_size=30,
            ),
            RectSlot(
                id="slot.box",
                prompt="",
                x=75,
                y=150,
                width=640,
                height=130,
                fill="none",
                stroke="#9ACD32",
                stroke_width=2.0,
            ),
            CircleSlot(
                id="slot.opt1.c1",
                prompt="",
                cx=200,
                cy=215,
                r=20,
                fill="none",
                stroke="#222222",
                stroke_width=1.5,
            ),
            CircleSlot(
                id="slot.opt1.c2",
                prompt="",
                cx=215,
                cy=195,
                r=20,
                fill="none",
                stroke="#222222",
                stroke_width=1.5,
            ),
            CircleSlot(
                id="slot.opt1.c3",
                prompt="",
                cx=180,
                cy=235,
                r=20,
                fill="none",
                stroke="#222222",
                stroke_width=1.5,
            ),
            CircleSlot(
                id="slot.opt2.c1",
                prompt="",
                cx=395,
                cy=215,
                r=40,
                fill="none",
                stroke="#222222",
                stroke_width=1.5,
            ),
            CircleSlot(
                id="slot.opt2.c2",
                prompt="",
                cx=370,
                cy=215,
                r=15,
                fill="none",
                stroke="#222222",
                stroke_width=1.5,
            ),
            CircleSlot(
                id="slot.opt3.c1",
                prompt="",
                cx=595,
                cy=210,
                r=35,
                fill="none",
                stroke="#222222",
                stroke_width=1.5,
            ),
            CircleSlot(
                id="slot.opt3.c2",
                prompt="",
                cx=595,
                cy=210,
                r=25,
                fill="none",
                stroke="#222222",
                stroke_width=1.5,
            ),
            CircleSlot(
                id="slot.opt3.c3",
                prompt="",
                cx=595,
                cy=210,
                r=10,
                fill="none",
                stroke="#222222",
                stroke_width=1.5,
            ),
            CircleSlot(
                id="slot.opt3.c2.copy4",
                prompt="",
                cx=380,
                cy=215,
                r=25,
                stroke="#222222",
                stroke_width=1.5,
            ),
            TextSlot(
                id="slot.qtext1.copy5",
                prompt="",
                text="㉠",
                x=135,
                y=195,
                font_size=30,
                fill="#111111",
            ),
            TextSlot(
                id="slot.qtext1.copy5.copy6",
                prompt="",
                text="㉡",
                x=310,
                y=200,
                font_size=30,
                fill="#111111",
            ),
            TextSlot(
                id="slot.qtext1.copy5.copy7",
                prompt="",
                text="㉢",
                x=510,
                y=200,
                font_size=30,
                fill="#111111",
            ),
        ),
        diagrams=(),
        groups=(),
        constraints=(),
        tags=(),
    )


PROBLEM_TEMPLATE = build_problem_template()

SEMANTIC_OVERRIDE = {
    "problem_id": "S3_초등_3_008666",
    "problem_type": "도형_관계_선택",
    "metadata": {
        "language": "ko",
        "question": "원의 반지름은 모두 같고 원의 중심을 옮겨 가며 그린 그림을 찾아 선택하세요.",
        "instruction": "그림의 반지름과 중심 관계를 비교하여 보기와 해설을 읽는다.",
    },
    "domain": {
        "objects": [
            {
                "id": "obj.option1",
                "type": "circle_group",
                "property": "same_radius_overlapping_centers",
            },
            {
                "id": "obj.option2",
                "type": "circle_group",
                "property": "different_radii_moved_centers",
            },
            {
                "id": "obj.option3",
                "type": "circle_group",
                "property": "concentric_circles",
            },
        ],
        "relations": [],
        "problem_solving": {
            "understand": {
                "given_refs": ["obj.option1", "obj.option2", "obj.option3"],
                "target_ref": "answer.target",
                "condition_refs": ["rel.compare_radius", "rel.compare_center"],
            },
            "plan": {
                "method": "도형 성질 비교",
                "description": "각 보기의 반지름이 같은지와 중심이 옮겨졌는지를 비교한다.",
            },
            "execute": {
                "expected_operations": [
                    "compare_radius",
                    "compare_center",
                    "match_description_to_view",
                ]
            },
            "review": {
                "check_methods": [
                    "description_consistency_check",
                    "circle_relation_check",
                ]
            },
        },
    },
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {
            "type": "선택",
            "description": "원의 반지름이 모두 같고 원의 중심을 옮겨 가며 그린 그림",
        },
        "value": "㉠",
        "unit": "",
    },
}

SOLVABLE = {
    "schema": "modu.solvable.v1.1",
    "problem_id": "S3_초등_3_008666",
    "problem_type": "도형_관계_선택",
    "inputs": {
        "total_ticks": 3,
        "target_label": "반지름이 모두 같고 원의 중심을 옮겨 가며 그린 그림",
        "target_ticks": 1,
        "target_count": 3,
        "unit": "",
    },
    "given": [
        {
            "ref": "obj.option1",
            "value": {"property": "same_radius_overlapping_centers"},
        },
        {"ref": "obj.option2", "value": {"property": "different_radii_moved_centers"}},
        {"ref": "obj.option3", "value": {"property": "concentric_circles"}},
    ],
    "target": {"ref": "answer.target", "type": "선택"},
    "method": "도형 성질 비교",
    "plan": [
        "각 보기의 원들에서 반지름이 같은지 확인한다.",
        "원의 중심이 옮겨졌는지, 같은 중심인지 확인한다.",
        "문장과 가장 잘 맞는 그림을 고른다.",
    ],
    "steps": [
        {"id": "step.1", "expr": "보기 1의 원 관계 확인", "value": "겹쳐진 원들"},
        {
            "id": "step.2",
            "expr": "보기 2의 원 관계 확인",
            "value": "반지름이 다른 원들",
        },
        {"id": "step.3", "expr": "보기 3의 원 관계 확인", "value": "동심원"},
    ],
    "checks": [
        {
            "id": "check.1",
            "expr": "문장 조건과 일치하는 보기인지 확인",
            "expected": "반지름이 모두 같고 중심이 이동한 그림",
            "actual": "미확정",
            "pass": False,
        }
    ],
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {
            "type": "선택",
            "description": "원의 반지름이 모두 같고 원의 중심을 옮겨 가며 그린 그림",
        },
        "value": "㉠",
        "unit": "",
    },
}
