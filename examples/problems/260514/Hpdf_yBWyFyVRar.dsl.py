from __future__ import annotations
from modu_math.dsl import Canvas, ProblemTemplate, Region, RectSlot, TextSlot, PathSlot


def build_problem_template() -> ProblemTemplate:
    return ProblemTemplate(
        id="Hpdf_yBWyFyVRar",
        title="직사각형을 정사각형으로 나누기",
        canvas=Canvas(width=860, height=600, coordinate_mode="logical"),
        regions=(
            Region(
                id="region.stem",
                role="stem",
                flow="absolute",
                slot_ids=(
                    "slot.q1",
                    "slot.q2",
                    "slot.q3",
                    "slot.q4",
                    "slot.q5",
                    "slot.q6",
                    "slot.rect",
                    "slot.len.top",
                    "slot.len.right",
                    "slot.arc.top",
                    "slot.arc.right",
                ),
            ),
        ),
        slots=(
            TextSlot(
                id="slot.q1",
                prompt="",
                text="다음 직사각형을 한 변이 9 cm인 정사각형 모",
                style_role="question",
                x=22.0,
                y=40.0,
                font_size=45,
            ),
            TextSlot(
                id="slot.q2",
                prompt="",
                text="양으로 될 수 있는 대로 많이 나누려고 합니다.",
                style_role="question",
                x=22.0,
                y=100.0,
                font_size=45,
            ),
            TextSlot(
                id="slot.q3",
                prompt="",
                text="정사각형은 몇 개로 나누어집니까?",
                style_role="question",
                x=22.0,
                y=160.0,
                font_size=45,
            ),
            RectSlot(
                id="slot.rect",
                prompt="",
                x=150.0,
                y=300.0,
                width=540.0,
                height=270.0,
                stroke="#333333",
                stroke_width=2.0,
                fill="none",
            ),
            TextSlot(
                id="slot.len.top",
                prompt="",
                text="54 cm",
                style_role="label",
                x=370.0,
                y=260.0,
                font_size=35,
            ),
            TextSlot(
                id="slot.len.right",
                prompt="",
                text="27 cm",
                style_role="label",
                x=705.0,
                y=435.0,
                font_size=35,
            ),
            PathSlot(
                id="slot.arc.top",
                prompt="",
                d="M 150 295 C 240 245, 450 245, 690 295",
                stroke="#666666",
                stroke_width=1.5,
                stroke_dasharray="8 6",
                fill="none",
            ),
            PathSlot(
                id="slot.arc.right",
                prompt="",
                d="M 695 300 C 745 335, 745 535, 695 570",
                stroke="#666666",
                stroke_width=1.5,
                stroke_dasharray="8 6",
                fill="none",
            ),
        ),
        diagrams=(),
        groups=(),
        constraints=(),
        tags=(),
    )


PROBLEM_TEMPLATE = build_problem_template()
SEMANTIC_OVERRIDE = {
    "problem_id": "Hpdf_yBWyFyVRar",
    "problem_type": "rectangle_partition",
    "metadata": {
        "language": "ko",
        "question": "직사각형을 한 변이 9 cm인 정사각형으로 될 수 있는 대로 많이 나누는 문제",
        "instruction": "정사각형은 몇 개로 나누어집니까?",
    },
    "domain": {
        "objects": [
            {
                "id": "obj.rectangle",
                "type": "rectangle",
                "width_cm": 54,
                "height_cm": 27,
            },
            {"id": "obj.square_side", "type": "length", "value_cm": 9},
        ],
        "relations": [
            {
                "id": "rel.partition",
                "type": "tile_by_equal_squares",
                "from_id": "obj.rectangle",
                "to_id": "obj.square_side",
            }
        ],
        "problem_solving": {
            "understand": {
                "given_refs": ["obj.rectangle", "obj.square_side"],
                "target_ref": "answer.target",
                "condition_refs": ["rel.partition"],
            },
            "plan": {
                "method": "area_based_partition",
                "description": "직사각형을 같은 크기의 정사각형으로 최대한 많이 나누는 관계를 이해한다.",
            },
            "execute": {
                "expected_operations": [
                    "compare_side_lengths",
                    "determine_possible_tiling",
                ]
            },
            "review": {
                "check_methods": ["unit_consistency_check", "tiling_feasibility_check"]
            },
        },
    },
    "answer": {
        "target": {
            "type": "count_of_squares",
            "description": "정사각형은 몇 개로 나누어집니까?",
        },
        "value": 18,
        "unit": "개",
    },
}
SOLVABLE = {
    "schema": "modu.solvable.v1",
    "problem_id": "Hpdf_yBWyFyVRar",
    "problem_type": "rectangle_partition",
    "inputs": {
        "total_ticks": 0,
        "target_label": "정사각형은 몇 개로 나누어집니까?",
        "target_ticks": 0,
        "target_count": 0,
        "unit": "개",
    },
    "given": [
        {"ref": "obj.rectangle", "value": {"width_cm": 54, "height_cm": 27}},
        {"ref": "obj.square_side", "value": {"value_cm": 9}},
    ],
    "target": {"ref": "answer.target", "type": "count_of_squares"},
    "method": "area_based_partition",
    "plan": [
        "직사각형과 정사각형의 길이 조건을 확인한다.",
        "나누는 상황의 의미를 해석한다.",
    ],
    "steps": [
        {
            "id": "step.1",
            "operation": "calculate_count",
            "expr": "(54 / 9) * (27 / 9)",
            "value": 18,
        }
    ],
    "checks": [
        {
            "id": "check.1",
            "type": "unit_consistency_check",
            "expr": "cm 단위가 일치하는지 확인",
            "expected": 0,
            "actual": 0,
            "pass": True,
        }
    ],
    "answer": {"value": 18, "unit": "개", "derived_from": "step.1"},
}
