from __future__ import annotations
from modu_math.dsl import (
    Canvas,
    ProblemTemplate,
    Region,
    TextSlot,
    RectSlot,
    CircleSlot,
    LineSlot,
    PolygonSlot,
)


def build_problem_template() -> ProblemTemplate:
    return ProblemTemplate(
        id="S3_초등_3_008541",
        title="계산 결과가 큰 것부터 차례대로 나열한 것을 고르시오",
        canvas=Canvas(width=940, height=394, coordinate_mode="logical"),
        regions=(
            Region(
                id="region.stem",
                role="stem",
                flow="absolute",
                slot_ids=("slot.q0",
                    "slot.q1",
                    "slot.box",
                    "slot.expr1",
                    "slot.expr2",
                    "slot.expr3",
                    "slot.opt1",
                    "slot.opt2",
                    "slot.opt3",
                    "slot.opt4",'konva_1784850887765_rect_10764'),
            ),
        ),
        slots=(TextSlot(
                id="slot.q1",
                prompt="",
                text="계산 결과가 큰 것부터 차례대로 나열한 것을 고르시오.",
                style_role="question",
                x = 50, y = 30, font_size=28,
            ),
            RectSlot(
                id="slot.box",
                prompt="",
                x = 45, y = 50, width=765.0,
                height=78.0,
                fill="#FBE7C4",
                stroke="#FBE7C4",
                stroke_width=1.0,
            ),
            TextSlot(
                id="slot.expr1",
                prompt="",
                text="ㄱ. 397 × 6",
                style_role="body",
                x = 145, y = 100, font_size=28,
            ),
            TextSlot(
                id="slot.expr2",
                prompt="",
                text="ㄴ. 549 × 4",
                style_role="body",
                x = 355, y = 100, font_size=28,
            ),
            TextSlot(
                id="slot.expr3",
                prompt="",
                text="ㄷ. 456 × 5",
                style_role="body",
                x = 585, y = 100, font_size=28,
            ),
            TextSlot(
                id="slot.opt1",
                prompt="",
                text = '① ㄱ ㄴ ㄷ', style_role="body",
                x = 105, y = 190, font_size=28,
            ),
            TextSlot(
                id="slot.opt2",
                prompt="",
                text="② ㄱ ㄷ ㄴ",
                style_role="body",
                x = 475, y = 190, font_size=28,
            ),
            TextSlot(
                id="slot.opt3",
                prompt="",
                text="③ ㄴ ㄷ ㄱ",
                style_role="body",
                x = 105, y = 250, font_size=28,
            ),
            TextSlot(
                id="slot.opt4",
                prompt="",
                text="④ ㄷ ㄴ ㄱ",
                style_role="body",
                x = 475, y = 245, font_size=28,
            ),
            RectSlot(
                id = 'konva_1784850887765_rect_10764',
                prompt = '', x = 222.027, y = 302.089,
                width = 119.5, height = 63.733,
                fill = '#ffffff', stroke = '#111827',
                stroke_width = 1.2,
                interaction = {'type': 'input', 'role': 'answer', 'value_type': 'digit', 'max_length': 1, 'include_in_submission': True, 'order': 0, 'group_id': 'final_answer', 'auto_advance': True, 'keyboard': 'number'},
                input_style = {'font_size_mode': 'auto', 'font_size_adjust': 0, 'min_font_size': 14, 'max_font_size': 52, 'font_weight': 700, 'horizontal_align': 'center', 'vertical_align': 'middle', 'padding': 6, 'text_color': '#222222'})),
        diagrams=(),
        groups=(),
        constraints=(),
        tags=(),
    )


PROBLEM_TEMPLATE = build_problem_template()

SEMANTIC_OVERRIDE = {
    "problem_id": "S3_초등_3_008541",
    "problem_type": "multiple_choice_ordering",
    "metadata": {
        "language": "ko",
        "question": "계산 결과가 큰 것부터 차례대로 나열한 것을 고르시오.",
        "instruction": "보기에서 계산 결과가 큰 것부터 차례대로 나열한 것을 고르시오.",
    },
    "domain": {
        "objects": [
            {
                "id": "obj.a",
                "type": "expression",
                "label": "ㄱ",
                "operation": "397 × 6",
            },
            {
                "id": "obj.b",
                "type": "expression",
                "label": "ㄴ",
                "operation": "549 × 4",
            },
            {
                "id": "obj.c",
                "type": "expression",
                "label": "ㄷ",
                "operation": "456 × 5",
            },
            {
                "id": "obj.option2",
                "type": "choice",
                "label": "②",
                "sequence": ["ㄱ", "ㄷ", "ㄴ"],
            },
        ],
        "relations": [
            {
                "id": "rel.order",
                "type": "descending_order",
                "from_id": "obj.a",
                "to_id": "obj.b",
            }
        ],
    },
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {
            "type": "choice_number",
            "description": "계산 결과가 큰 것부터 차례대로 나열한 보기 번호",
        },
        "value": 2,
        "unit": "",
    },
}

SOLVABLE = {
    "schema": "modu.solvable.v1.1",
    "problem_id": "S3_초등_3_008541",
    "problem_type": "multiple_choice_ordering",
    "inputs": {
        "total_ticks": 3,
        "target_label": "보기 번호",
        "target_ticks": 1,
        "target_count": 1,
        "unit": "",
    },
    "given": [
        {"ref": "obj.a", "value": {"label": "ㄱ", "expr": "397 × 6"}},
        {"ref": "obj.b", "value": {"label": "ㄴ", "expr": "549 × 4"}},
        {"ref": "obj.c", "value": {"label": "ㄷ", "expr": "456 × 5"}},
    ],
    "target": {"ref": "answer.target", "type": "choice_number"},
    "method": "compare_results_descending",
    "plan": [
        "각 곱셈식의 결과를 구한 뒤 큰 값부터 작은 값 순서로 비교합니다.",
        "비교한 순서와 같은 보기 번호를 찾습니다.",
    ],
    "steps": [
        {"id": "step.1", "expr": "397 × 6", "value": 2382},
        {"id": "step.2", "expr": "549 × 4", "value": 2196},
        {"id": "step.3", "expr": "456 × 5", "value": 2280},
        {"id": "step.4", "expr": "2382 > 2280 > 2196", "value": "ㄱ, ㄷ, ㄴ"},
        {"id": "step.5", "expr": "보기 대조", "value": "②"},
    ],
    "checks": [
        {
            "id": "check.1",
            "expr": "2382 > 2280 > 2196",
            "expected": True,
            "actual": True,
            "pass": True,
        },
        {
            "id": "check.2",
            "expr": "보기 ②의 순서",
            "expected": "ㄱ, ㄷ, ㄴ",
            "actual": "ㄱ, ㄷ, ㄴ",
            "pass": True,
        },
    ],
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {
            "type": "choice_number",
            "description": "계산 결과가 큰 것부터 차례대로 나열한 보기 번호",
        },
        "value": 2,
        "unit": "",
    },
}

PROBLEM_TEMPLATE = build_problem_template()


SEMANTIC_OVERRIDE = {
    "problem_id": "three_circle_circumference_001",
    "problem_type": "numeric_answer_circle_circumference",
    "metadata": {
        "language": "ko",
        "question": "세 원의 원주의 합은 몇 cm입니까? (원주율: 3)",
        "instruction": (
            "서로 이웃한 두 원의 중심 사이의 거리와 오른쪽 원의 "
            "반지름을 이용하여 세 원의 반지름을 구한 뒤 원주의 합을 구합니다."
        ),
    },
    "domain": {
        "objects": [
            {
                "id": "obj.circle_left",
                "type": "circle",
                "label": "왼쪽 원",
                "center_ref": "point.center_left",
                "radius": 6,
                "radius_unit": "cm",
            },
            {
                "id": "obj.circle_middle",
                "type": "circle",
                "label": "가운데 원",
                "center_ref": "point.center_middle",
                "radius": 8,
                "radius_unit": "cm",
            },
            {
                "id": "obj.circle_right",
                "type": "circle",
                "label": "오른쪽 원",
                "center_ref": "point.center_right",
                "radius": 10,
                "radius_unit": "cm",
            },
            {
                "id": "point.center_left",
                "type": "point",
                "label": "왼쪽 원의 중심",
            },
            {
                "id": "point.center_middle",
                "type": "point",
                "label": "가운데 원의 중심",
            },
            {
                "id": "point.center_right",
                "type": "point",
                "label": "오른쪽 원의 중심",
            },
            {
                "id": "measure.center_distance_left_middle",
                "type": "length",
                "label": "왼쪽 원과 가운데 원의 중심 사이 거리",
                "value": 14,
                "unit": "cm",
            },
            {
                "id": "measure.center_distance_middle_right",
                "type": "length",
                "label": "가운데 원과 오른쪽 원의 중심 사이 거리",
                "value": 18,
                "unit": "cm",
            },
            {
                "id": "measure.right_radius",
                "type": "length",
                "label": "오른쪽 원의 반지름",
                "value": 10,
                "unit": "cm",
            },
            {
                "id": "const.pi",
                "type": "constant",
                "label": "원주율",
                "value": 3,
            },
        ],
        "relations": [
            {
                "id": "rel.left_middle_tangent",
                "type": "externally_tangent",
                "from_id": "obj.circle_left",
                "to_id": "obj.circle_middle",
            },
            {
                "id": "rel.middle_right_tangent",
                "type": "externally_tangent",
                "from_id": "obj.circle_middle",
                "to_id": "obj.circle_right",
            },
            {
                "id": "rel.left_middle_center_distance",
                "type": "center_distance_equals_radius_sum",
                "from_id": "obj.circle_left",
                "to_id": "obj.circle_middle",
                "measure_ref": "measure.center_distance_left_middle",
                "equation": "r_left + r_middle = 14",
            },
            {
                "id": "rel.middle_right_center_distance",
                "type": "center_distance_equals_radius_sum",
                "from_id": "obj.circle_middle",
                "to_id": "obj.circle_right",
                "measure_ref": "measure.center_distance_middle_right",
                "equation": "r_middle + r_right = 18",
            },
            {
                "id": "rel.right_radius_given",
                "type": "radius_measure",
                "from_id": "obj.circle_right",
                "to_id": "measure.right_radius",
                "equation": "r_right = 10",
            },
        ],
    },
    "answer": {
        "blanks": [
            {
                "id": "slot.answer",
                "type": "number",
                "value": 144,
                "unit": "cm",
            }
        ],
        "choices": [],
        "answer_key": "144cm",
        "target": {
            "type": "total_circumference",
            "description": "세 원의 원주의 합",
        },
        "value": 144,
        "unit": "cm",
    },
}


SOLVABLE = {
    "schema": "modu.solvable.v1.1",
    "problem_id": "three_circle_circumference_001",
    "problem_type": "numeric_answer_circle_circumference",
    "inputs": {
        "left_middle_center_distance": 14,
        "middle_right_center_distance": 18,
        "right_radius": 10,
        "pi": 3,
        "circle_count": 3,
        "target_label": "세 원의 원주의 합",
        "unit": "cm",
    },
    "given": [
        {
            "ref": "measure.center_distance_left_middle",
            "value": {
                "distance": 14,
                "unit": "cm",
                "between": [
                    "point.center_left",
                    "point.center_middle",
                ],
            },
        },
        {
            "ref": "measure.center_distance_middle_right",
            "value": {
                "distance": 18,
                "unit": "cm",
                "between": [
                    "point.center_middle",
                    "point.center_right",
                ],
            },
        },
        {
            "ref": "measure.right_radius",
            "value": {
                "radius": 10,
                "unit": "cm",
            },
        },
        {
            "ref": "const.pi",
            "value": 3,
        },
        {
            "ref": "rel.left_middle_tangent",
            "value": True,
        },
        {
            "ref": "rel.middle_right_tangent",
            "value": True,
        },
    ],
    "target": {
        "ref": "answer.target",
        "type": "total_circumference",
        "unit": "cm",
    },
    "method": "derive_radii_and_sum_circumferences",
    "plan": [
        "서로 접하는 두 원의 중심 사이 거리는 두 원의 반지름의 합과 같습니다.",
        "가운데 원의 반지름은 18cm에서 오른쪽 원의 반지름 10cm를 뺍니다.",
        "왼쪽 원의 반지름은 14cm에서 가운데 원의 반지름을 뺍니다.",
        "세 원의 반지름의 합을 구합니다.",
        "원주율 3을 사용하여 세 원의 원주의 합을 계산합니다.",
    ],
    "steps": [
        {
            "id": "step.1",
            "expr": "r_middle + 10 = 18",
            "value": {
                "r_middle": 8,
                "unit": "cm",
            },
        },
        {
            "id": "step.2",
            "expr": "r_middle = 18 - 10",
            "value": 8,
        },
        {
            "id": "step.3",
            "expr": "r_left + 8 = 14",
            "value": {
                "r_left": 6,
                "unit": "cm",
            },
        },
        {
            "id": "step.4",
            "expr": "r_left = 14 - 8",
            "value": 6,
        },
        {
            "id": "step.5",
            "expr": "r_left + r_middle + r_right",
            "substitution": "6 + 8 + 10",
            "value": 24,
            "unit": "cm",
        },
        {
            "id": "step.6",
            "expr": "2 × π × (r_left + r_middle + r_right)",
            "substitution": "2 × 3 × 24",
            "value": 144,
            "unit": "cm",
        },
    ],
    "checks": [
        {
            "id": "check.1",
            "expr": "6 + 8 = 14",
            "expected": 14,
            "actual": 14,
            "pass": True,
        },
        {
            "id": "check.2",
            "expr": "8 + 10 = 18",
            "expected": 18,
            "actual": 18,
            "pass": True,
        },
        {
            "id": "check.3",
            "expr": "2 × 3 × 6 + 2 × 3 × 8 + 2 × 3 × 10",
            "expected": 144,
            "actual": 144,
            "pass": True,
        },
        {
            "id": "check.4",
            "expr": "2 × 3 × (6 + 8 + 10)",
            "expected": 144,
            "actual": 144,
            "pass": True,
        },
    ],
    "answer": {
        "blanks": [
            {
                "id": "slot.answer",
                "type": "number",
                "value": 144,
                "unit": "cm",
            }
        ],
        "choices": [],
        "answer_key": "144cm",
        "target": {
            "type": "total_circumference",
            "description": "세 원의 원주의 합",
        },
        "value": 144,
        "unit": "cm",
    },
}