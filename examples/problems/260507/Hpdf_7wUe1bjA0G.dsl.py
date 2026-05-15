from __future__ import annotations
from modu_math.dsl import Canvas, ProblemTemplate, Region, TextSlot, RectSlot, PathSlot


def build_problem_template() -> ProblemTemplate:
    return ProblemTemplate(
        id="Hpdf_7wUe1bjA0G",
        title="도화지의 모든 변의 길이의 합",
        canvas=Canvas(width=912.0, height=738.0, coordinate_mode="logical"),
        regions=(
            Region(
                id="region.stem",
                role="stem",
                flow="absolute",
                slot_ids=("slot.q1", "slot.q2", "slot.q3", "slot.q4"),
            ),
            Region(
                id="region.diagram",
                role="figure",
                flow="absolute",
                slot_ids=(
                    "slot.shape.paper",
                    "slot.dim.bottom",
                    "slot.dim.right",
                    "slot.lb.bottom",
                    "slot.lb.right",
                ),
            ),
        ),
        slots=(
            TextSlot(
                id="slot.q1",
                prompt="",
                text="다음은 직사각형 모양의 도화지에서 한 변이",
                style_role="question",
                x=20.0,
                y=50.0,
                font_size=35,
            ),
            TextSlot(
                id="slot.q2",
                prompt="",
                text="6 cm인 정사각형 모양 2개를 잘라 낸 것입니다.",
                style_role="question",
                x=20.0,
                y=110.0,
                font_size=35,
            ),
            TextSlot(
                id="slot.q3",
                prompt="",
                text="남은 도화지의 모든 변의 길이의 합은 몇 cm",
                style_role="question",
                x=20.0,
                y=170.0,
                font_size=35,
            ),
            TextSlot(
                id="slot.q4",
                prompt="",
                text="입니까?",
                style_role="question",
                x=20.0,
                y=230.0,
                font_size=35,
            ),
            PathSlot(
                id="slot.shape.paper",
                prompt="",
                d="M 320 320 L 360 320 L 360 440 L 480 440 L 480 320 L 520 320 L 520 680 L 480 680 L 480 560 L 360 560 L 360 680 L 320 680 Z",
                stroke="#2B2424",
                stroke_width=3.0,
                fill="#D9D9DD",
            ),
            PathSlot(
                id="slot.dim.bottom",
                prompt="",
                d="M 320.0 685.0 C 340.0 730.0, 500.0 730.0, 520.0 685.0",
                stroke="#2B2424",
                stroke_width=1.6,
                stroke_dasharray="7 5",
                fill="none",
            ),
            PathSlot(
                id="slot.dim.right",
                prompt="",
                d="M 525.0 320.0 C 560.0 380.0, 560.0 660.0, 525.0 680.0",
                stroke="#2B2424",
                stroke_width=1.6,
                stroke_dasharray="7 5",
                fill="none",
            ),
            TextSlot(
                id="slot.lb.bottom",
                prompt="",
                text="10 cm",
                style_role="label",
                x=380.0,
                y=730.0,
                font_size=35,
            ),
            TextSlot(
                id="slot.lb.right",
                prompt="",
                text="18 cm",
                style_role="label",
                x=550.0,
                y=500.0,
                font_size=35,
            ),
        ),
        diagrams=(),
        groups=(),
        constraints=(),
        tags=(),
    )


PROBLEM_TEMPLATE = build_problem_template()
SEMANTIC_OVERRIDE = {
    "problem_id": "Hpdf_7wUe1bjA0G",
    "problem_type": "perimeter_after_cutting_squares",
    "metadata": {
        "language": "ko",
        "question": "직사각형 모양의 도화지에서 한 변이 6 cm인 정사각형 모양 2개를 잘라 낸 뒤 남은 도화지의 모든 변의 길이의 합을 묻는 문제",
        "instruction": "남은 도화지의 모든 변의 길이의 합은 몇 cm입니까?",
    },
    "domain": {
        "objects": [
            {
                "id": "obj.paper",
                "type": "figure",
                "shape": "rectangular_sheet_with_two_square_cuts",
            },
            {"id": "obj.cut_square", "type": "square", "side_length_cm": 6, "count": 2},
            {
                "id": "obj.dim_bottom",
                "type": "measurement",
                "value_cm": 10,
                "orientation": "horizontal",
            },
            {
                "id": "obj.dim_right",
                "type": "measurement",
                "value_cm": 18,
                "orientation": "vertical",
            },
        ],
        "relations": [
            {
                "id": "rel.cut_from.paper",
                "type": "removed_from",
                "from_id": "obj.cut_square",
                "to_id": "obj.paper",
            }
        ],
        "problem_solving": {
            "understand": {
                "given_refs": [
                    "obj.paper",
                    "obj.cut_square",
                    "obj.dim_bottom",
                    "obj.dim_right",
                ],
                "target_ref": "answer.target",
                "condition_refs": ["rel.cut_from.paper"],
            },
            "plan": {
                "method": "perimeter_calculation",
                "description": "원래 직사각형의 둘레에서 잘라낸 부분에 의해 늘어난 변의 길이를 합산한다.",
            },
            "execute": {
                "expected_operations": [
                    "calculate_original_perimeter",
                    "add_extra_sides_from_cuts",
                ]
            },
            "review": {
                "check_methods": [
                    "measurement_consistency_check",
                    "shape_structure_check",
                ]
            },
        },
    },
    "answer": {
        "target": {
            "type": "perimeter_sum",
            "description": "남은 도화지의 모든 변의 길이의 합",
        },
        "value": 80,
        "unit": "cm",
    },
}
SOLVABLE = {
    "schema": "modu.solvable.v1",
    "problem_id": "Hpdf_7wUe1bjA0G",
    "problem_type": "perimeter_after_cutting_squares",
    "inputs": {
        "total_ticks": 0,
        "target_label": "남은 도화지의 모든 변의 길이의 합",
        "target_ticks": 0,
        "target_count": 1,
        "unit": "cm",
    },
    "given": [
        {"ref": "obj.cut_square", "value": {"side_length_cm": 6, "count": 2}},
        {
            "ref": "obj.dim_bottom",
            "value": {"value_cm": 10, "orientation": "horizontal"},
        },
        {"ref": "obj.dim_right", "value": {"value_cm": 18, "orientation": "vertical"}},
    ],
    "target": {"ref": "answer.target", "type": "perimeter_sum"},
    "method": "perimeter_calculation",
    "plan": [
        "직사각형의 둘레를 구하고, 잘라낸 정사각형에 의해 늘어난 길이를 더한다.",
        "정사각형 하나를 잘라낼 때마다 가로 변은 유지되고 세로 변 2개가 추가되므로, 한 변의 길이의 2배만큼 늘어난다.",
    ],
    "steps": [
        {
            "id": "step.1",
            "operation": "calculate_perimeter",
            "expr": "2 * (10 + 18) + 2 * (2 * 6)",
            "value": 80,
        }
    ],
    "checks": [
        {
            "id": "check.1",
            "type": "logic_check",
            "expr": "56 + 24 = 80",
            "expected": 80,
            "actual": 80,
            "pass": True,
        }
    ],
    "answer": {"value": 80, "unit": "cm", "derived_from": "step.1"},
}
