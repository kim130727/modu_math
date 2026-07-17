from __future__ import annotations

from modu_math.dsl import (
    BlankSlot,
    Canvas,
    CircleSlot,
    Group,
    LineSlot,
    PathSlot,
    ProblemTemplate,
    Region,
    TextBoxSlot,
    TextSlot,
)

PROBLEM_ID = "three_circle_circumference_001"
PROBLEM_TITLE = "세 원의 원주의 합"


def build_problem_template() -> ProblemTemplate:
    return ProblemTemplate(
        id=PROBLEM_ID,
        title=PROBLEM_TITLE,
        canvas=Canvas(
            width=700,
            height=420,
            coordinate_mode="logical",
        ),
        regions=(
            Region(
                id="region.stem",
                role="stem",
                flow="vertical",
                slot_ids=("slot.question",),
            ),
            Region(
                id="region.diagram",
                role="diagram",
                flow="absolute",
                slot_ids=(
                    "slot.circle_left",
                    "slot.circle_middle",
                    "slot.circle_right",
                    # 중심을 잇는 선
                    "slot.center_line",
                    # 반지름 10cm를 나타내는 선
                    "slot.radius_10_line",
                    # 중심 사이 거리를 나타내는 점선 호
                    "slot.distance_14_arc",
                    "slot.distance_18_arc",
                    "slot.center_left",
                    "slot.center_middle",
                    "slot.center_right",
                    # 길이 표시
                    "slot.label_14",
                    "slot.label_18",
                    "slot.label_10",
                    "slot.radius_10_arc",
                ),
            ),
            Region(
                id="region.answer",
                role="answer",
                flow="vertical",
                slot_ids=(),
            ),
        ),
        slots=(
            TextBoxSlot(
                id="slot.question",
                text="세 원의 원주의 합은 몇 cm입니까? (원주율: 3)",
                prompt="세 원의 원주의 합을 묻는 문제",
                semantic_role="question",
                x=40,
                y=30,
                width=579,
                height=86,
                font_size=30,
                line_height=1.3,
                fill="#111111",
                align="left",
            ),
            # =========================================================
            # 원의 배치
            #
            # 축척: 1cm = 8px
            #
            # 왼쪽 원 반지름: 6cm  → 48px
            # 가운데 원 반지름: 8cm → 64px
            # 오른쪽 원 반지름: 10cm → 80px
            #
            # 왼쪽-가운데 중심 거리: 6 + 8 = 14cm → 112px
            # 가운데-오른쪽 중심 거리: 8 + 10 = 18cm → 144px
            # =========================================================
            CircleSlot(
                id="slot.circle_left",
                prompt="반지름이 6cm인 왼쪽 원",
                cx=210,
                cy=244,
                r=48,
                fill="#ffffff",
                stroke="#202020",
                stroke_width=2,
            ),
            CircleSlot(
                id="slot.circle_middle",
                prompt="반지름이 8cm인 가운데 원",
                cx=323,
                cy=244,
                r=64,
                fill="#ffffff",
                stroke="#202020",
                stroke_width=2,
            ),
            CircleSlot(
                id="slot.circle_right",
                prompt="반지름이 10cm인 오른쪽 원",
                cx=466,
                cy=245,
                r=80,
                fill="#ffffff",
                stroke="#202020",
                stroke_width=2,
            ),
            # 세 원의 중심을 잇는 수평선
            LineSlot(
                id="slot.center_line",
                prompt="세 원의 중심을 잇는 선",
                x1=210,
                y1=245,
                x2=466,
                y2=245,
                stroke="#303030",
                stroke_width=2,
            ),
            # 오른쪽 원의 반지름
            LineSlot(
                id="slot.radius_10_line",
                prompt="오른쪽 원의 반지름 10cm",
                x1=466,
                y1=245,
                x2=466,
                y2=325,
                stroke="#303030",
                stroke_width=2,
            ),
            # 왼쪽 원 중심부터 가운데 원 중심까지: 14cm
            PathSlot(
                id="slot.distance_14_arc",
                prompt="왼쪽 원과 가운데 원의 중심 사이 거리 14cm",
                d="M 207 240 Q 266 300 325 240",
                fill="none",
                stroke="#555555",
                stroke_width=1.8,
                stroke_dasharray="6 5",
            ),
            # 가운데 원 중심부터 오른쪽 원 중심까지: 18cm
            PathSlot(
                id="slot.distance_18_arc",
                prompt="가운데 원과 오른쪽 원의 중심 사이 거리 18cm",
                d="M 320 248 Q 396 188 472 248",
                fill="none",
                stroke="#555555",
                stroke_width=1.8,
                stroke_dasharray="6 5",
            ),
            # 오른쪽 원 중심에서 원주 방향으로 향하는 점선 곡선
            CircleSlot(
                id="slot.center_left",
                prompt="왼쪽 원의 중심",
                cx=210,
                cy=245,
                r=4.5,
                fill="#ff3f7f",
                stroke="none",
                stroke_width=2,
            ),
            CircleSlot(
                id="slot.center_middle",
                prompt="가운데 원의 중심",
                cx=322,
                cy=245,
                r=4.5,
                fill="#ff3f7f",
                stroke="none",
                stroke_width=2,
            ),
            CircleSlot(
                id="slot.center_right",
                prompt="오른쪽 원의 중심",
                cx=466,
                cy=245,
                r=4.5,
                fill="#ff3f7f",
                stroke="none",
                stroke_width=2,
            ),
            # 길이 표시 텍스트
            TextSlot(
                id="slot.label_14",
                prompt="두 원의 중심 사이 거리 14cm",
                text="14cm",
                x=256,
                y=308,
                font_size=25,
                anchor="middle",
                fill="#222222",
            ),
            TextSlot(
                id="slot.label_18",
                prompt="두 원의 중심 사이 거리 18cm",
                text="18cm",
                x=428,
                y=213,
                font_size=25,
                anchor="middle",
                fill="#222222",
            ),
            TextSlot(
                id="slot.label_10",
                prompt="오른쪽 원의 반지름 10cm",
                text="10cm",
                x=507,
                y=274,
                font_size=24,
                anchor="middle",
                fill="#222222",
            ),
            BlankSlot(
                id="slot.answer",
                prompt="세 원의 원주의 합",
                answer_key="144cm",
                placeholder="정답",
            ),
            PathSlot(
                id="slot.radius_10_arc",
                prompt="오른쪽 원의 반지름 10cm를 보조 표시하는 점선 곡선",
                d="M 465 251 Q 495 286 465 321",
                fill="none",
                stroke="#555555",
                stroke_width=1.8,
                stroke_dasharray="6 5",
            ),
        ),
        diagrams=(),
        groups=(
            Group(
                id="group.diagram.three_circles",
                role="diagram_block",
                member_ids=(
                    "slot.circle_left",
                    "slot.circle_middle",
                    "slot.circle_right",
                    "slot.center_line",
                    "slot.radius_10_line",
                    "slot.distance_14_arc",
                    "slot.distance_18_arc",
                    "slot.center_left",
                    "slot.center_middle",
                    "slot.center_right",
                    "slot.label_14",
                    "slot.label_18",
                    "slot.label_10",
                    "slot.radius_10_arc",
                    "konva_1783766230573_arrow_592743",
                    "konva_1783766230573_arrow_617127",
                    "konva_1783766230573_paste_678750_0",
                ),
            ),
        ),
        constraints=(),
        tags=(
            "circle",
            "circumference",
            "tangent-circles",
            "elementary-math",
            "schema-compliant",
        ),
    )


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
        "answer_key": [
            {
                "blank_id": "slot.answer",
                "value": 144,
                "unit": "cm",
            }
        ],
        "target": {
            "type": "total_circumference",
            "description": "세 원의 원주의 합",
        },
        "value": 144,
        "unit": "cm",
        "sentence": "세 원의 원주의 합은 144cm입니다.",
    },
}

SOLVABLE = {
    "schema": "modu.solvable.v1.1",
    "problem_id": "three_circle_circumference_001",
    "problem_type": "numeric_answer_circle_circumference",

    # =========================================================
    # 1. 문제 이해: inputs + given + target
    # =========================================================
    "inputs": {
        "target_label": "세 원의 원주의 합",
        "unit": "cm",
        "quantities": {
            "left_middle_center_distance": 14,
            "middle_right_center_distance": 18,
            "right_radius": 10,
            "pi": 3,
            "circle_count": 3,
        },
        "conditions": [
            "왼쪽 원과 가운데 원은 서로 접합니다.",
            "가운데 원과 오른쪽 원은 서로 접합니다.",
        ],
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
                "circle_ref": "obj.circle_right",
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
    },

    # =========================================================
    # 2. 계획 세우기: method + plan
    # =========================================================
    "method": "derive_radii_then_sum_circumferences",
    "plan": [
        "서로 접한 두 원의 중심 사이 거리는 두 원의 반지름의 합과 같음을 이용합니다.",
        "18cm와 오른쪽 원의 반지름 10cm를 이용하여 가운데 원의 반지름을 구합니다.",
        "14cm와 가운데 원의 반지름을 이용하여 왼쪽 원의 반지름을 구합니다.",
        "세 원의 반지름을 모두 더합니다.",
        "반지름의 합에 2와 원주율 3을 곱하여 세 원의 원주의 합을 구합니다.",
    ],

    # =========================================================
    # 3. 계획 실행: steps
    # =========================================================
    "steps": [
        {
            "id": "step.1",
            "goal": "가운데 원의 반지름을 구합니다.",
            "uses": [
                "measure.center_distance_middle_right",
                "measure.right_radius",
                "rel.middle_right_tangent",
            ],
            "relation_expr": "r_middle + 10 = 18",
            "expr": "r_middle = 18 - 10",
            "value": {
                "radius": 8,
                "unit": "cm",
                "ref": "derived.radius_middle",
            },
            "explanation": (
                "가운데 원과 오른쪽 원이 서로 접하므로 "
                "두 원의 중심 사이 거리 18cm는 두 반지름의 합입니다. "
                "따라서 18cm에서 오른쪽 원의 반지름 10cm를 뺍니다."
            ),
        },
        {
            "id": "step.2",
            "goal": "왼쪽 원의 반지름을 구합니다.",
            "uses": [
                "measure.center_distance_left_middle",
                "derived.radius_middle",
                "rel.left_middle_tangent",
            ],
            "relation_expr": "r_left + 8 = 14",
            "expr": "r_left = 14 - 8",
            "value": {
                "radius": 6,
                "unit": "cm",
                "ref": "derived.radius_left",
            },
            "explanation": (
                "왼쪽 원과 가운데 원이 서로 접하므로 "
                "두 원의 중심 사이 거리 14cm는 두 반지름의 합입니다. "
                "따라서 14cm에서 가운데 원의 반지름 8cm를 뺍니다."
            ),
        },
        {
            "id": "step.3",
            "goal": "세 원의 반지름의 합을 구합니다.",
            "uses": [
                "derived.radius_left",
                "derived.radius_middle",
                "measure.right_radius",
            ],
            "expr": "r_left + r_middle + r_right = 6 + 8 + 10",
            "value": {
                "radius_sum": 24,
                "unit": "cm",
                "ref": "derived.radius_sum",
            },
            "explanation": (
                "왼쪽 원, 가운데 원, 오른쪽 원의 반지름을 모두 더하면 "
                "6 + 8 + 10 = 24cm입니다."
            ),
        },
        {
            "id": "step.4",
            "goal": "세 원의 원주의 합을 구합니다.",
            "uses": [
                "derived.radius_sum",
                "const.pi",
            ],
            "relation_expr": (
                "2 × π × r_left + 2 × π × r_middle + 2 × π × r_right "
                "= 2 × π × (r_left + r_middle + r_right)"
            ),
            "expr": "2 × 3 × 24 = 144",
            "value": {
                "total_circumference": 144,
                "unit": "cm",
                "ref": "answer.target",
            },
            "explanation": (
                "세 원의 원주의 합은 "
                "2 × 원주율 × 세 원의 반지름의 합으로 계산할 수 있습니다. "
                "따라서 2 × 3 × 24 = 144cm입니다."
            ),
        },
    ],

    # =========================================================
    # 4. 되돌아보기: checks + answer
    # =========================================================
    "checks": [
        {
            "id": "check.1",
            "description": (
                "가운데 원과 오른쪽 원의 반지름의 합이 "
                "두 중심 사이 거리와 같은지 확인합니다."
            ),
            "expr": "8 + 10",
            "expected": 18,
            "actual": 18,
            "pass": True,
        },
        {
            "id": "check.2",
            "description": (
                "왼쪽 원과 가운데 원의 반지름의 합이 "
                "두 중심 사이 거리와 같은지 확인합니다."
            ),
            "expr": "6 + 8",
            "expected": 14,
            "actual": 14,
            "pass": True,
        },
        {
            "id": "check.3",
            "description": (
                "각 원의 원주를 따로 구하여 더한 결과가 "
                "최종 답과 같은지 확인합니다."
            ),
            "expr": "2 × 3 × 6 + 2 × 3 × 8 + 2 × 3 × 10",
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
        "answer_key": [
            {
                "blank_id": "slot.answer",
                "value": 144,
                "unit": "cm",
            }
        ],
        "target": {
            "type": "total_circumference",
            "description": "세 원의 원주의 합",
        },
        "value": 144,
        "unit": "cm",
        "sentence": "세 원의 원주의 합은 144cm입니다.",
    },
}


TUTOR_RENDERER_FLOW = [
    # =========================================================
    # 1. 문제 이해
    # inputs + given + target
    # =========================================================
    {
        "phase": "understand",
        "title": "문제 이해",
        "source_refs": [
            "inputs",
            "given",
            "target",
        ],
        "frames": [
            {
                "id": "understand.given_distances",
                "overlays": [
                    {
                        "type": "dim",
                        "target_ref": "slot.circle_left",
                    },
                    {
                        "type": "dim",
                        "target_ref": "slot.circle_middle",
                    },
                    {
                        "type": "dim",
                        "target_ref": "slot.circle_right",
                    },
                    {
                        "type": "highlight",
                        "target_ref": "slot.distance_14_arc",
                        "variant": "given",
                    },
                    {
                        "type": "highlight",
                        "target_ref": "slot.label_14",
                        "variant": "given",
                    },
                    {
                        "type": "highlight",
                        "target_ref": "slot.distance_18_arc",
                        "variant": "given",
                    },
                    {
                        "type": "highlight",
                        "target_ref": "slot.label_18",
                        "variant": "given",
                    },
                    {
                        "type": "label",
                        "text": "주어진 중심 사이 거리: 14cm, 18cm",
                        "x": 350,
                        "y": 120,
                        "style": {
                            "fill": "#1d4ed8",
                            "font_size": 22,
                            "font_weight": 700,
                        },
                    },
                ],
            },
            {
                "id": "understand.given_radius",
                "overlays": [
                    {
                        "type": "highlight",
                        "target_ref": "slot.radius_10_line",
                        "variant": "given",
                    },
                    {
                        "type": "highlight",
                        "target_ref": "slot.radius_10_arc",
                        "variant": "given",
                    },
                    {
                        "type": "highlight",
                        "target_ref": "slot.label_10",
                        "variant": "given",
                    },
                    {
                        "type": "label",
                        "text": "오른쪽 원의 반지름은 10cm입니다.",
                        "x": 350,
                        "y": 120,
                        "style": {
                            "fill": "#1d4ed8",
                            "font_size": 22,
                            "font_weight": 700,
                        },
                    },
                ],
            },
            {
                "id": "understand.target",
                "overlays": [
                    {
                        "type": "highlight",
                        "target_ref": "slot.circle_left",
                        "variant": "target",
                    },
                    {
                        "type": "highlight",
                        "target_ref": "slot.circle_middle",
                        "variant": "target",
                    },
                    {
                        "type": "highlight",
                        "target_ref": "slot.circle_right",
                        "variant": "target",
                    },
                    {
                        "type": "label",
                        "text": "구할 것: 세 원의 원주의 합",
                        "x": 350,
                        "y": 120,
                        "style": {
                            "fill": "#b45309",
                            "font_size": 24,
                            "font_weight": 700,
                        },
                    },
                ],
            },
        ],
    },

    # =========================================================
    # 2. 계획 세우기
    # method + plan
    # =========================================================
    {
        "phase": "plan",
        "title": "계획 세우기",
        "source_refs": [
            "method",
            "plan",
        ],
        "frames": [
            {
                "id": "plan.principle",
                "overlays": [
                    {
                        "type": "highlight",
                        "target_ref": "slot.center_line",
                        "variant": "method",
                    },
                    {
                        "type": "label",
                        "text": (
                            "서로 접한 두 원의 중심 사이 거리\n"
                            "= 두 원의 반지름의 합"
                        ),
                        "x": 350,
                        "y": 115,
                        "style": {
                            "fill": "#7c3aed",
                            "font_size": 22,
                            "font_weight": 700,
                            "align": "center",
                        },
                    },
                ],
            },
            {
                "id": "plan.sequence",
                "overlays": [
                    {
                        "type": "label",
                        "text": (
                            "① 가운데 반지름 구하기\n"
                            "② 왼쪽 반지름 구하기\n"
                            "③ 세 반지름 더하기\n"
                            "④ 원주의 합 구하기"
                        ),
                        "x": 350,
                        "y": 135,
                        "style": {
                            "fill": "#374151",
                            "font_size": 21,
                            "line_height": 1.5,
                            "align": "center",
                        },
                    },
                ],
            },
        ],
    },

    # =========================================================
    # 3. 계획 실행
    # steps
    # =========================================================
    {
        "phase": "execute",
        "title": "계획 실행",
        "source_refs": [
            "steps",
        ],
        "step_id": "step.1",
        "frames": [
            {
                "id": "step.1.relation",
                "overlays": [
                    {
                        "type": "highlight",
                        "target_ref": "slot.distance_18_arc",
                        "variant": "given",
                    },
                    {
                        "type": "highlight",
                        "target_ref": "slot.label_18",
                        "variant": "given",
                    },
                    {
                        "type": "highlight",
                        "target_ref": "slot.radius_10_line",
                        "variant": "given",
                    },
                    {
                        "type": "highlight",
                        "target_ref": "slot.label_10",
                        "variant": "given",
                    },
                    {
                        "type": "label",
                        "text": "가운데 반지름 + 10 = 18",
                        "x": 350,
                        "y": 120,
                        "style": {
                            "fill": "#374151",
                            "font_size": 24,
                            "font_weight": 700,
                        },
                    },
                ],
            },
            {
                "id": "step.1.question",
                "overlays": [
                    {
                        "type": "label",
                        "text": "□ + 10 = 18",
                        "x": 350,
                        "y": 120,
                        "style": {
                            "fill": "#b45309",
                            "font_size": 28,
                            "font_weight": 700,
                        },
                    },
                ],
            },
            {
                "id": "step.1.result",
                "overlays": [
                    {
                        "type": "label",
                        "text": "18 - 10 = 8cm",
                        "x": 350,
                        "y": 120,
                        "style": {
                            "fill": "#0f766e",
                            "font_size": 26,
                            "font_weight": 700,
                        },
                    },
                    {
                        "type": "label",
                        "text": "8cm",
                        "x": 353,
                        "y": 265,
                        "style": {
                            "fill": "#0f766e",
                            "font_size": 22,
                            "font_weight": 700,
                        },
                    },
                ],
            },
        ],
    },
    {
        "phase": "execute",
        "title": "계획 실행",
        "source_refs": [
            "steps",
        ],
        "step_id": "step.2",
        "frames": [
            {
                "id": "step.2.relation",
                "overlays": [
                    {
                        "type": "highlight",
                        "target_ref": "slot.distance_14_arc",
                        "variant": "given",
                    },
                    {
                        "type": "highlight",
                        "target_ref": "slot.label_14",
                        "variant": "given",
                    },
                    {
                        "type": "highlight",
                        "target_ref": "slot.circle_middle",
                        "variant": "derived",
                    },
                    {
                        "type": "label",
                        "text": "왼쪽 반지름 + 8 = 14",
                        "x": 350,
                        "y": 120,
                        "style": {
                            "fill": "#374151",
                            "font_size": 24,
                            "font_weight": 700,
                        },
                    },
                    {
                        "type": "label",
                        "text": "8cm",
                        "x": 353,
                        "y": 265,
                        "style": {
                            "fill": "#0f766e",
                            "font_size": 22,
                            "font_weight": 700,
                        },
                    },
                ],
            },
            {
                "id": "step.2.question",
                "overlays": [
                    {
                        "type": "label",
                        "text": "□ + 8 = 14",
                        "x": 350,
                        "y": 120,
                        "style": {
                            "fill": "#b45309",
                            "font_size": 28,
                            "font_weight": 700,
                        },
                    },
                ],
            },
            {
                "id": "step.2.result",
                "overlays": [
                    {
                        "type": "label",
                        "text": "14 - 8 = 6cm",
                        "x": 350,
                        "y": 120,
                        "style": {
                            "fill": "#0f766e",
                            "font_size": 26,
                            "font_weight": 700,
                        },
                    },
                    {
                        "type": "label",
                        "text": "6cm",
                        "x": 210,
                        "y": 265,
                        "style": {
                            "fill": "#0f766e",
                            "font_size": 22,
                            "font_weight": 700,
                        },
                    },
                    {
                        "type": "label",
                        "text": "8cm",
                        "x": 353,
                        "y": 265,
                        "style": {
                            "fill": "#0f766e",
                            "font_size": 22,
                            "font_weight": 700,
                        },
                    },
                ],
            },
        ],
    },
    {
        "phase": "execute",
        "title": "계획 실행",
        "source_refs": [
            "steps",
        ],
        "step_id": "step.3",
        "frames": [
            {
                "id": "step.3.radii",
                "overlays": [
                    {
                        "type": "highlight",
                        "target_ref": "slot.circle_left",
                        "variant": "derived",
                    },
                    {
                        "type": "highlight",
                        "target_ref": "slot.circle_middle",
                        "variant": "derived",
                    },
                    {
                        "type": "highlight",
                        "target_ref": "slot.circle_right",
                        "variant": "given",
                    },
                    {
                        "type": "label",
                        "text": "6cm",
                        "x": 210,
                        "y": 265,
                        "style": {
                            "fill": "#0f766e",
                            "font_size": 22,
                            "font_weight": 700,
                        },
                    },
                    {
                        "type": "label",
                        "text": "8cm",
                        "x": 353,
                        "y": 265,
                        "style": {
                            "fill": "#0f766e",
                            "font_size": 22,
                            "font_weight": 700,
                        },
                    },
                    {
                        "type": "label",
                        "text": "10cm",
                        "x": 500,
                        "y": 265,
                        "style": {
                            "fill": "#1d4ed8",
                            "font_size": 22,
                            "font_weight": 700,
                        },
                    },
                ],
            },
            {
                "id": "step.3.sum",
                "overlays": [
                    {
                        "type": "label",
                        "text": "6 + 8 + 10 = 24cm",
                        "x": 350,
                        "y": 120,
                        "style": {
                            "fill": "#0f766e",
                            "font_size": 26,
                            "font_weight": 700,
                        },
                    },
                ],
            },
        ],
    },
    {
        "phase": "execute",
        "title": "계획 실행",
        "source_refs": [
            "steps",
        ],
        "step_id": "step.4",
        "frames": [
            {
                "id": "step.4.formula",
                "overlays": [
                    {
                        "type": "label",
                        "text": "원주의 합 = 2 × 원주율 × 반지름의 합",
                        "x": 350,
                        "y": 110,
                        "style": {
                            "fill": "#374151",
                            "font_size": 22,
                            "font_weight": 700,
                        },
                    },
                ],
            },
            {
                "id": "step.4.substitute",
                "overlays": [
                    {
                        "type": "label",
                        "text": "2 × 3 × 24",
                        "x": 350,
                        "y": 120,
                        "style": {
                            "fill": "#374151",
                            "font_size": 28,
                            "font_weight": 700,
                        },
                    },
                ],
            },
            {
                "id": "step.4.result",
                "overlays": [
                    {
                        "type": "label",
                        "text": "2 × 3 × 24 = 144cm",
                        "x": 350,
                        "y": 120,
                        "style": {
                            "fill": "#0f766e",
                            "font_size": 28,
                            "font_weight": 700,
                        },
                    },
                ],
            },
        ],
    },

    # =========================================================
    # 4. 되돌아보기
    # checks + answer
    # =========================================================
    {
        "phase": "review",
        "title": "되돌아보기",
        "source_refs": [
            "checks",
            "answer",
        ],
        "frames": [
            {
                "id": "review.check_middle_right",
                "overlays": [
                    {
                        "type": "highlight",
                        "target_ref": "slot.distance_18_arc",
                        "variant": "check",
                    },
                    {
                        "type": "label",
                        "text": "8 + 10 = 18  ✓",
                        "x": 350,
                        "y": 120,
                        "style": {
                            "fill": "#15803d",
                            "font_size": 25,
                            "font_weight": 700,
                        },
                    },
                ],
            },
            {
                "id": "review.check_left_middle",
                "overlays": [
                    {
                        "type": "highlight",
                        "target_ref": "slot.distance_14_arc",
                        "variant": "check",
                    },
                    {
                        "type": "label",
                        "text": "6 + 8 = 14  ✓",
                        "x": 350,
                        "y": 120,
                        "style": {
                            "fill": "#15803d",
                            "font_size": 25,
                            "font_weight": 700,
                        },
                    },
                ],
            },
            {
                "id": "review.check_circumference",
                "overlays": [
                    {
                        "type": "label",
                        "text": "36 + 48 + 60 = 144  ✓",
                        "x": 350,
                        "y": 120,
                        "style": {
                            "fill": "#15803d",
                            "font_size": 25,
                            "font_weight": 700,
                        },
                    },
                ],
            },
            {
                "id": "review.answer",
                "overlays": [
                    {
                        "type": "highlight",
                        "target_ref": "slot.circle_left",
                        "variant": "answer",
                    },
                    {
                        "type": "highlight",
                        "target_ref": "slot.circle_middle",
                        "variant": "answer",
                    },
                    {
                        "type": "highlight",
                        "target_ref": "slot.circle_right",
                        "variant": "answer",
                    },
                    {
                        "type": "label",
                        "text": "답: 144cm",
                        "x": 350,
                        "y": 120,
                        "style": {
                            "fill": "#111827",
                            "font_size": 32,
                            "font_weight": 800,
                        },
                    },
                ],
            },
        ],
    },
]
