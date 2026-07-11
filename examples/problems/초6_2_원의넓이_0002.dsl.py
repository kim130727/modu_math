from __future__ import annotations

from modu_math.dsl import (
    BlankSlot,
    Canvas,
    CircleSlot,
    Group,
    LineSlot,
    PolygonSlot,
    ProblemTemplate,
    Region,
    TextBoxSlot,
    TextSlot,
    PathSlot,
)

PROBLEM_ID = "circle_hexagon_perimeter_difference_001"
PROBLEM_TITLE = "원과 정육각형의 둘레의 차"


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
                    "slot.circle",
                    "slot.hexagon",
                    "slot.diameter_line",
                    "slot.center_point",
                    "slot.label_30",
                    "konva_1783767050396_paste_321289_0",
                ),
            ),
            Region(
                id="region.answer",
                role="answer",
                flow="absolute",
                slot_ids=(),
            ),
        ),
        slots=(
            TextBoxSlot(
                id="slot.question",
                text="오른쪽 도형에서 원과 정육각형의 둘레의 차는 몇 cm입니까? (원주율: 3.14)",
                prompt="원과 정육각형의 둘레의 차를 묻는 문제",
                semantic_role="question",
                x=17,
                y=20,
                width=430,
                height=126,
                font_size=27,
                line_height=1.45,
                fill="#111111",
                align="left",
            ),
            # 원: 지름 30cm, 반지름 15cm
            CircleSlot(
                id="slot.circle",
                prompt="지름이 30cm인 원",
                cx=336,
                cy=264,
                r=100,
                fill="#ffffff",
                stroke="#202020",
                stroke_width=2,
            ),
            # 원에 내접한 정육각형
            # 중심 (565, 225), 반지름 100px
            # 꼭짓점: 0°, 60°, 120°, 180°, 240°, 300°
            PolygonSlot(
                id="slot.hexagon",
                prompt="원에 내접한 정육각형",
                points=(
                    (436, 264),
                    (386, 177.4),
                    (286, 177.4),
                    (236, 264),
                    (286, 350.6),
                    (386, 350.6),
                ),
                fill="none",
                stroke="#202020",
                stroke_width=2,
            ),
            # 정육각형의 서로 마주 보는 꼭짓점을 잇는 지름
            LineSlot(
                id="slot.diameter_line",
                prompt="원의 지름 30cm",
                x1=236,
                y1=264,
                x2=436,
                y2=264,
                stroke="#202020",
                stroke_width=2,
            ),
            CircleSlot(
                id="slot.center_point",
                prompt="원의 중심",
                cx=336,
                cy=264,
                r=4.5,
                fill="#ff3f7f",
                stroke="none",
                stroke_width=0,
            ),
            TextSlot(
                id="slot.label_30",
                prompt="지름의 길이 표시",
                text="30 cm",
                x=336,
                y=230,
                font_size=24,
                anchor="middle",
                fill="#222222",
            ),
            BlankSlot(
                id="slot.answer",
                prompt="원과 정육각형의 둘레의 차",
                answer_key="4.2cm",
                placeholder="정답",
            ),
            PathSlot(
                id="konva_1783767050396_paste_321289_0",
                prompt="",
                d="M 234 267 Q 336.5 207 439 267",
                fill="none",
                stroke="#555555",
                stroke_width=1.8,
                stroke_dasharray="6 5",
            ),
        ),
        diagrams=(),
        groups=(
            Group(
                id="group.diagram.circle_hexagon",
                role="diagram_block",
                member_ids=(
                    "slot.circle",
                    "slot.hexagon",
                    "slot.diameter_line",
                    "slot.center_point",
                    "slot.label_30",
                    "konva_1783767050396_paste_321289_0",
                ),
            ),
        ),
        constraints=(),
        tags=(
            "circle",
            "regular-hexagon",
            "circumference",
            "perimeter",
            "inscribed-polygon",
            "elementary-math",
            "schema-compliant",
        ),
    )


PROBLEM_TEMPLATE = build_problem_template()


SEMANTIC_OVERRIDE = {
    "problem_id": PROBLEM_ID,
    "problem_type": "numeric_answer_perimeter_difference",
    "metadata": {
        "language": "ko",
        "question": ("오른쪽 도형에서 원과 정육각형의 둘레의 차는 " "몇 cm입니까? (원주율: 3.14)"),
        "instruction": (
            "원의 지름으로 반지름을 구하고, 원에 내접한 정육각형의 "
            "한 변의 길이가 원의 반지름과 같음을 이용합니다."
        ),
    },
    "domain": {
        "objects": [
            {
                "id": "obj.circle",
                "type": "circle",
                "label": "원",
                "center_ref": "point.center",
                "diameter": 30,
                "radius": 15,
                "unit": "cm",
            },
            {
                "id": "obj.hexagon",
                "type": "regular_polygon",
                "label": "정육각형",
                "sides": 6,
                "inscribed_in": "obj.circle",
                "side_length": 15,
                "unit": "cm",
            },
            {
                "id": "point.center",
                "type": "point",
                "label": "원의 중심",
            },
            {
                "id": "measure.diameter",
                "type": "length",
                "label": "원의 지름",
                "value": 30,
                "unit": "cm",
            },
            {
                "id": "const.pi",
                "type": "constant",
                "label": "원주율",
                "value": 3.14,
            },
        ],
        "relations": [
            {
                "id": "rel.hexagon_inscribed",
                "type": "inscribed_in",
                "from_id": "obj.hexagon",
                "to_id": "obj.circle",
            },
            {
                "id": "rel.hexagon_side_equals_radius",
                "type": "side_length_equals_radius",
                "from_id": "obj.hexagon",
                "to_id": "obj.circle",
                "equation": "s = r",
            },
            {
                "id": "rel.diameter_measure",
                "type": "diameter_measure",
                "from_id": "obj.circle",
                "to_id": "measure.diameter",
                "equation": "d = 30",
            },
        ],
    },
    "answer": {
        "blanks": [
            {
                "id": "slot.answer",
                "type": "number",
                "value": 4.2,
                "unit": "cm",
            }
        ],
        "choices": [],
        "answer_key": "4.2cm",
        "target": {
            "type": "perimeter_difference",
            "description": "원의 둘레에서 정육각형의 둘레를 뺀 값",
        },
        "value": 4.2,
        "unit": "cm",
    },
}

SOLVABLE = {
    "schema": "modu.solvable.v1.1",
    "problem_id": PROBLEM_ID,
    "problem_type": "numeric_answer_perimeter_difference",

    "inputs": {
        "diameter": 30,
        "pi": 3.14,
        "polygon_sides": 6,
        "target_label": "원과 정육각형의 둘레의 차",
        "unit": "cm",
    },

    "given": [
        {
            "ref": "measure.diameter",
            "value": {
                "length": 30,
                "unit": "cm",
            },
        },
        {
            "ref": "const.pi",
            "value": 3.14,
        },
        {
            "ref": "rel.hexagon_inscribed",
            "value": True,
        },
        {
            "ref": "rel.hexagon_side_equals_radius",
            "value": True,
        },
    ],

    "target": {
        "ref": "answer.target",
        "type": "perimeter_difference",
        "description": "원의 둘레에서 정육각형의 둘레를 뺀 값",
        "unit": "cm",
    },

    "method": "compare_circle_and_inscribed_hexagon_perimeters",

    "prerequisites": [
        {
            "id": "prerequisite.1",
            "concept": "radius_and_diameter",
            "description": "원의 지름은 반지름의 2배입니다.",
        },
        {
            "id": "prerequisite.2",
            "concept": "circle_circumference",
            "description": "원의 둘레는 지름 × 원주율로 구합니다.",
        },
        {
            "id": "prerequisite.3",
            "concept": "regular_polygon_perimeter",
            "description": "정다각형의 둘레는 한 변의 길이 × 변의 수입니다.",
        },
        {
            "id": "prerequisite.4",
            "concept": "inscribed_regular_hexagon",
            "description": (
                "원에 내접한 정육각형의 한 변의 길이는 "
                "원의 반지름과 같습니다."
            ),
        },
    ],

    "concepts": [
        {
            "id": "concept.radius",
            "name": "원의 반지름",
            "formula": "반지름 = 지름 ÷ 2",
        },
        {
            "id": "concept.circle_circumference",
            "name": "원의 둘레",
            "formula": "원의 둘레 = 지름 × 원주율",
        },
        {
            "id": "concept.hexagon_side",
            "name": "내접한 정육각형의 한 변",
            "formula": "정육각형의 한 변 = 원의 반지름",
        },
        {
            "id": "concept.hexagon_perimeter",
            "name": "정육각형의 둘레",
            "formula": "정육각형의 둘레 = 한 변 × 6",
        },
        {
            "id": "concept.perimeter_difference",
            "name": "둘레의 차",
            "formula": "원의 둘레 - 정육각형의 둘레",
        },
    ],

    "plan": [
        {
            "id": "plan.1",
            "goal": "원의 반지름 구하기",
            "description": "지름 30cm를 2로 나누어 반지름을 구합니다.",
        },
        {
            "id": "plan.2",
            "goal": "정육각형의 한 변 구하기",
            "description": (
                "원에 내접한 정육각형의 한 변이 "
                "원의 반지름과 같음을 이용합니다."
            ),
        },
        {
            "id": "plan.3",
            "goal": "원의 둘레 구하기",
            "description": "지름에 원주율 3.14를 곱합니다.",
        },
        {
            "id": "plan.4",
            "goal": "정육각형의 둘레 구하기",
            "description": "한 변의 길이에 6을 곱합니다.",
        },
        {
            "id": "plan.5",
            "goal": "두 둘레의 차 구하기",
            "description": "큰 둘레에서 작은 둘레를 뺍니다.",
        },
    ],

    "steps": [
        {
            "id": "step.1",
            "title": "원의 반지름 구하기",
            "goal": "지름 30cm에서 반지름을 구합니다.",
            "question": (
                "원의 지름은 반지름의 몇 배인가요? "
                "그렇다면 반지름은 몇 cm인가요?"
            ),
            "expected_response": {
                "type": "number",
                "value": 15,
                "unit": "cm",
                "accepted_forms": [
                    "15",
                    "15cm",
                    "15 cm",
                    "30 ÷ 2 = 15",
                ],
            },
            "hint": [
                "지름은 원의 중심을 지나 원의 양 끝을 잇는 선분입니다.",
                "지름은 반지름 2개를 이어 붙인 길이입니다.",
                "30을 2로 나누어 보세요.",
            ],
            "formula": "반지름 = 지름 ÷ 2",
            "expr": "30 ÷ 2",
            "value": {
                "result": 15,
                "meaning": "원의 반지름",
                "unit": "cm",
            },
            "explanation": (
                "지름은 반지름 2개의 길이와 같습니다. "
                "따라서 지름 30cm를 2로 나누면 "
                "반지름은 15cm입니다."
            ),
            "misconceptions": [
                {
                    "pattern": "30",
                    "feedback": (
                        "30cm는 반지름이 아니라 지름입니다. "
                        "반지름은 지름의 절반입니다."
                    ),
                },
                {
                    "pattern": "60",
                    "feedback": (
                        "반지름을 구할 때는 지름에 2를 곱하지 않고 "
                        "2로 나누어야 합니다."
                    ),
                },
            ],
        },

        {
            "id": "step.2",
            "title": "정육각형의 한 변 구하기",
            "goal": "정육각형의 한 변과 원의 반지름의 관계를 이해합니다.",
            "question": (
                "원에 내접한 정육각형의 한 변은 "
                "원의 어떤 길이와 같을까요?"
            ),
            "expected_response": {
                "type": "concept_and_number",
                "concept": "원의 반지름",
                "value": 15,
                "unit": "cm",
                "accepted_forms": [
                    "반지름",
                    "원의 반지름",
                    "15",
                    "15cm",
                    "15 cm",
                ],
            },
            "hint": [
                (
                    "원의 중심에서 정육각형의 이웃한 두 꼭짓점까지 "
                    "선을 그어 보세요."
                ),
                (
                    "중심과 두 꼭짓점을 이으면 세 변의 길이가 같은 "
                    "정삼각형이 만들어집니다."
                ),
                "정삼각형의 세 변은 모두 같습니다.",
            ],
            "formula": "정육각형의 한 변 = 원의 반지름",
            "expr": "정육각형의 한 변 = 15",
            "value": {
                "result": 15,
                "meaning": "정육각형의 한 변",
                "unit": "cm",
            },
            "explanation": (
                "원에 내접한 정육각형에서 원의 중심과 이웃한 두 꼭짓점을 "
                "연결하면 중심각은 60도입니다. 두 선분은 모두 반지름이고, "
                "만들어진 삼각형은 정삼각형이 됩니다. 따라서 정육각형의 "
                "한 변의 길이는 원의 반지름과 같은 15cm입니다."
            ),
            "visual_support": {
                "action": "highlight_triangle",
                "refs": [
                    "point.center",
                    "vertex.hexagon.1",
                    "vertex.hexagon.2",
                ],
                "caption": (
                    "중심과 이웃한 두 꼭짓점을 연결하면 "
                    "정삼각형이 만들어집니다."
                ),
            },
            "misconceptions": [
                {
                    "pattern": "30",
                    "feedback": (
                        "정육각형의 한 변은 원의 지름이 아니라 "
                        "원의 반지름과 같습니다."
                    ),
                },
                {
                    "pattern": "5",
                    "feedback": (
                        "지름 30cm를 정육각형의 변 6개로 바로 나누는 것이 "
                        "아닙니다. 먼저 반지름을 구해야 합니다."
                    ),
                },
            ],
        },

        {
            "id": "step.3",
            "title": "원의 둘레 구하기",
            "goal": "지름과 원주율을 이용해 원의 둘레를 구합니다.",
            "question": (
                "원의 둘레는 지름에 무엇을 곱해서 구하나요? "
                "원의 둘레는 몇 cm인가요?"
            ),
            "expected_response": {
                "type": "number",
                "value": 94.2,
                "unit": "cm",
                "accepted_forms": [
                    "94.2",
                    "94.2cm",
                    "94.2 cm",
                    "30 × 3.14 = 94.2",
                ],
            },
            "hint": [
                "원의 둘레 = 지름 × 원주율입니다.",
                "지름은 30cm이고 원주율은 3.14입니다.",
                "30 × 3.14를 계산해 보세요.",
            ],
            "formula": "원의 둘레 = 지름 × 원주율",
            "expr": "30 × 3.14",
            "calculation": [
                "3.14 × 3 = 9.42",
                "30은 3의 10배이므로 9.42 × 10 = 94.2",
            ],
            "value": {
                "result": 94.2,
                "meaning": "원의 둘레",
                "unit": "cm",
            },
            "explanation": (
                "원의 둘레는 지름에 원주율을 곱하여 구합니다. "
                "따라서 30 × 3.14 = 94.2이므로 "
                "원의 둘레는 94.2cm입니다."
            ),
            "misconceptions": [
                {
                    "pattern": "47.1",
                    "feedback": (
                        "15 × 3.14는 반지름에 원주율만 곱한 값입니다. "
                        "원의 둘레는 지름 × 원주율 또는 "
                        "2 × 반지름 × 원주율로 구합니다."
                    ),
                },
                {
                    "pattern": "942",
                    "feedback": (
                        "소수점 위치를 확인해 보세요. "
                        "30 × 3.14는 94.2입니다."
                    ),
                },
            ],
        },

        {
            "id": "step.4",
            "title": "정육각형의 둘레 구하기",
            "goal": "한 변의 길이와 변의 수를 이용해 둘레를 구합니다.",
            "question": (
                "정육각형은 변이 몇 개이며, 한 변이 15cm일 때 "
                "둘레는 몇 cm인가요?"
            ),
            "expected_response": {
                "type": "number",
                "value": 90,
                "unit": "cm",
                "accepted_forms": [
                    "90",
                    "90cm",
                    "90 cm",
                    "15 × 6 = 90",
                ],
            },
            "hint": [
                "정육각형은 길이가 같은 변이 6개입니다.",
                "둘레는 모든 변의 길이를 더한 값입니다.",
                "15를 6번 더하거나 15 × 6을 계산해 보세요.",
            ],
            "formula": "정육각형의 둘레 = 한 변의 길이 × 6",
            "expr": "15 × 6",
            "value": {
                "result": 90,
                "meaning": "정육각형의 둘레",
                "unit": "cm",
            },
            "explanation": (
                "정육각형은 길이가 같은 변이 6개입니다. "
                "한 변이 15cm이므로 둘레는 "
                "15 × 6 = 90cm입니다."
            ),
            "misconceptions": [
                {
                    "pattern": "21",
                    "feedback": (
                        "한 변의 길이 15에 변의 수 6을 더하는 것이 아니라 "
                        "15cm인 변이 6개이므로 곱해야 합니다."
                    ),
                },
                {
                    "pattern": "180",
                    "feedback": (
                        "정육각형의 한 변은 지름 30cm가 아니라 "
                        "반지름 15cm입니다."
                    ),
                },
            ],
        },

        {
            "id": "step.5",
            "title": "두 둘레의 차 구하기",
            "goal": "원의 둘레와 정육각형의 둘레를 비교합니다.",
            "question": (
                "원의 둘레 94.2cm와 정육각형의 둘레 90cm의 "
                "차는 몇 cm인가요?"
            ),
            "expected_response": {
                "type": "number",
                "value": 4.2,
                "unit": "cm",
                "accepted_forms": [
                    "4.2",
                    "4.2cm",
                    "4.2 cm",
                    "94.2 - 90 = 4.2",
                ],
            },
            "hint": [
                "차를 구할 때는 큰 수에서 작은 수를 뺍니다.",
                "원의 둘레가 정육각형의 둘레보다 큽니다.",
                "94.2 - 90을 계산해 보세요.",
            ],
            "formula": "둘레의 차 = 원의 둘레 - 정육각형의 둘레",
            "expr": "94.2 - 90",
            "value": {
                "result": 4.2,
                "meaning": "원과 정육각형의 둘레의 차",
                "unit": "cm",
            },
            "explanation": (
                "원의 둘레는 94.2cm이고 정육각형의 둘레는 90cm입니다. "
                "따라서 두 둘레의 차는 "
                "94.2 - 90 = 4.2cm입니다."
            ),
            "misconceptions": [
                {
                    "pattern": "-4.2",
                    "feedback": (
                        "둘레의 차는 보통 큰 값에서 작은 값을 빼서 "
                        "양수로 나타냅니다."
                    ),
                },
                {
                    "pattern": "184.2",
                    "feedback": (
                        "문제는 두 둘레의 합이 아니라 차를 묻고 있습니다."
                    ),
                },
            ],
        },
    ],

    "summary": {
        "narration": [
            "원의 지름은 30cm이므로 반지름은 15cm입니다.",
            (
                "원에 내접한 정육각형의 한 변은 원의 반지름과 같으므로 "
                "15cm입니다."
            ),
            "원의 둘레는 30 × 3.14 = 94.2cm입니다.",
            "정육각형의 둘레는 15 × 6 = 90cm입니다.",
            "따라서 두 둘레의 차는 94.2 - 90 = 4.2cm입니다.",
        ],
        "combined_expr": "(30 × 3.14) - ((30 ÷ 2) × 6)",
        "combined_value": 4.2,
        "unit": "cm",
    },

    "checks": [
        {
            "id": "check.1",
            "type": "inverse_check",
            "description": "반지름을 2배 하면 원래 지름이 되는지 확인합니다.",
            "expr": "15 × 2",
            "expected": 30,
            "actual": 30,
            "pass": True,
        },
        {
            "id": "check.2",
            "type": "formula_check",
            "description": "정육각형의 둘레 계산을 확인합니다.",
            "expr": "15 × 6",
            "expected": 90,
            "actual": 90,
            "pass": True,
        },
        {
            "id": "check.3",
            "type": "formula_check",
            "description": "원의 둘레 계산을 확인합니다.",
            "expr": "30 × 3.14",
            "expected": 94.2,
            "actual": 94.2,
            "pass": True,
        },
        {
            "id": "check.4",
            "type": "difference_check",
            "description": "두 둘레의 차를 확인합니다.",
            "expr": "94.2 - 90",
            "expected": 4.2,
            "actual": 4.2,
            "pass": True,
        },
        {
            "id": "check.5",
            "type": "reasonableness_check",
            "description": (
                "원은 내접한 정육각형의 바깥쪽을 지나므로 "
                "원의 둘레가 정육각형의 둘레보다 커야 합니다."
            ),
            "expr": "94.2 > 90",
            "expected": True,
            "actual": True,
            "pass": True,
        },
    ],

    "common_misconceptions": [
        {
            "id": "misconception.1",
            "description": "지름 30cm를 정육각형의 한 변으로 생각함",
            "correction": (
                "정육각형의 한 변은 지름이 아니라 반지름과 같습니다."
            ),
        },
        {
            "id": "misconception.2",
            "description": "원의 둘레를 반지름 × 원주율로 계산함",
            "correction": (
                "원의 둘레는 지름 × 원주율 또는 "
                "2 × 반지름 × 원주율입니다."
            ),
        },
        {
            "id": "misconception.3",
            "description": "두 둘레의 차가 아니라 합을 계산함",
            "correction": (
                "문제에서 '차'를 묻고 있으므로 큰 둘레에서 "
                "작은 둘레를 빼야 합니다."
            ),
        },
    ],

    "answer": {
        "blanks": [
            {
                "id": "slot.answer",
                "type": "number",
                "value": 4.2,
                "unit": "cm",
            }
        ],
        "choices": [],
        "answer_key": "4.2cm",
        "target": {
            "type": "perimeter_difference",
            "description": "원의 둘레에서 정육각형의 둘레를 뺀 값",
        },
        "value": 4.2,
        "unit": "cm",
    },
}
