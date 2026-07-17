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
                x=26.997,
                y=9.995,
                width=656,
                height=87,
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


# Editor-build compatibility payload. The visual layout above is authored; this
# block keeps generated ids and answer/solvable shapes aligned with schemas.
PROBLEM_ID = "초6_2_원의넓이_0002"
PROBLEM_TEMPLATE = build_problem_template()

ANSWER = {
    "blanks": [
        {
            "id": "slot.answer",
            "type": "number",
            "value": 4.2,
            "unit": "cm",
        }
    ],
    "choices": [],
    "answer_key": [
        {
            "blank_id": "slot.answer",
            "value": 4.2,
            "unit": "cm",
        }
    ],
    "target": {
        "type": "perimeter_difference",
        "description": "원의 둘레에서 정육각형의 둘레를 뺀 값",
    },
    "value": 4.2,
    "unit": "cm",
}

SEMANTIC_OVERRIDE["problem_id"] = PROBLEM_ID
SEMANTIC_OVERRIDE["answer"] = ANSWER

SOLVABLE = {
    "schema": "modu.solvable.v1.2",
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
        {"ref": "measure.diameter", "value": {"length": 30, "unit": "cm"}},
        {"ref": "const.pi", "value": 3.14},
        {"ref": "rel.hexagon_inscribed", "value": True},
        {"ref": "rel.hexagon_side_equals_radius", "value": True},
    ],
    "target": {
        "ref": "answer.target",
        "type": "perimeter_difference",
    },
    "understanding": {
        "summary": (
            "지름이 30cm인 원과 그 안에 그려진 정육각형을 비교하여 "
            "원의 둘레에서 정육각형의 둘레를 뺀 차를 구하는 문제입니다."
        ),
        "facts": [
            {
                "ref": "measure.diameter",
                "label": "원의 지름",
                "value": 30,
                "unit": "cm",
                "source": "explicit",
                "meaning": "반지름은 지름의 절반입니다.",
            },
            {
                "ref": "const.pi",
                "label": "사용할 원주율",
                "value": 3.14,
                "unit": "",
                "source": "explicit",
            },
            {
                "ref": "rel.hexagon_inscribed",
                "label": "정육각형은 원 안에 그려져 있음",
                "value": True,
                "unit": "",
                "source": "explicit",
                "meaning": "내접 정육각형의 한 변은 원의 반지름과 같습니다.",
            },
        ],
        "unknowns": [
            {
                "ref": "derived.radius",
                "label": "원의 반지름",
                "unit": "cm",
            },
            {
                "ref": "derived.circle_perimeter",
                "label": "원의 둘레",
                "unit": "cm",
            },
            {
                "ref": "derived.hexagon_perimeter",
                "label": "정육각형의 둘레",
                "unit": "cm",
            },
            {
                "ref": "answer.target",
                "label": "원과 정육각형의 둘레의 차",
                "unit": "cm",
            },
        ],
        "relation": {
            "type": "circle_inscribed_regular_hexagon",
            "statement": "원에 내접한 정육각형의 한 변은 원의 반지름과 같습니다.",
            "symbolic": (
                "radius = diameter / 2; hexagon_side = radius; "
                "difference = circle_perimeter - hexagon_perimeter"
            ),
            "uses": [
                "measure.diameter",
                "const.pi",
                "rel.hexagon_inscribed",
                "rel.hexagon_side_equals_radius",
            ],
            "result": "answer.target",
        },
        "diagnostic_questions": [
            {
                "id": "understand.target",
                "type": "multiple_choice",
                "prompt": "이 문제에서 구해야 하는 것은 무엇인가요?",
                "choices": [
                    "원의 반지름",
                    "정육각형 한 변의 길이",
                    "원과 정육각형의 둘레의 차",
                ],
                "answer_index": 2,
            },
            {
                "id": "understand.relation",
                "type": "multiple_choice",
                "prompt": "원에 내접한 정육각형의 한 변은 무엇과 같나요?",
                "choices": [
                    "원의 반지름",
                    "원의 지름",
                    "원의 둘레",
                ],
                "answer_index": 0,
            },
        ],
    },
    "method": "compare_circle_and_inscribed_hexagon_perimeters",
    "plan": [
        "원의 지름 30cm를 2로 나누어 반지름 15cm를 구합니다.",
        "원에 내접한 정육각형의 한 변은 원의 반지름과 같으므로 15cm입니다.",
        "원의 둘레와 정육각형의 둘레를 각각 구합니다.",
        "원의 둘레에서 정육각형의 둘레를 빼서 차를 구합니다.",
    ],
    "steps": [
        {
            "id": "step.1",
            "goal": "원의 반지름을 구합니다.",
            "expr": "30 ÷ 2",
            "value": {"result": 15, "meaning": "원의 반지름", "unit": "cm"},
            "explanation": "지름 30cm를 2로 나누면 반지름은 15cm입니다.",
        },
        {
            "id": "step.2",
            "goal": "정육각형의 한 변의 길이를 확인합니다.",
            "expr": "정육각형의 한 변 = 원의 반지름",
            "value": {"result": 15, "meaning": "정육각형의 한 변", "unit": "cm"},
            "explanation": "원에 내접한 정육각형의 한 변은 원의 반지름과 같습니다.",
        },
        {
            "id": "step.3",
            "goal": "원의 둘레를 구합니다.",
            "expr": "30 × 3.14",
            "value": {"result": 94.2, "meaning": "원의 둘레", "unit": "cm"},
            "explanation": "원의 둘레는 지름에 원주율을 곱해 94.2cm입니다.",
        },
        {
            "id": "step.4",
            "goal": "정육각형의 둘레를 구합니다.",
            "expr": "15 × 6",
            "value": {"result": 90, "meaning": "정육각형의 둘레", "unit": "cm"},
            "explanation": "정육각형은 변이 6개이므로 둘레는 90cm입니다.",
        },
        {
            "id": "step.5",
            "goal": "두 둘레의 차를 구합니다.",
            "expr": "94.2 - 90",
            "value": {"result": 4.2, "meaning": "원과 정육각형의 둘레의 차", "unit": "cm"},
            "explanation": "원의 둘레 94.2cm에서 정육각형의 둘레 90cm를 빼면 4.2cm입니다.",
        },
    ],
    "checks": [
        {"id": "check.1", "expr": "15 × 2", "expected": 30, "actual": 30, "pass": True},
        {"id": "check.2", "expr": "15 × 6", "expected": 90, "actual": 90, "pass": True},
        {"id": "check.3", "expr": "30 × 3.14", "expected": 94.2, "actual": 94.2, "pass": True},
        {"id": "check.4", "expr": "94.2 - 90", "expected": 4.2, "actual": 4.2, "pass": True},
    ],
    "answer": ANSWER,
}
