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

PROBLEM_ID = "六年级_圆与正六边形周长之差_0002"
PROBLEM_TITLE = "圆与正六边形的周长之差"


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
                text="在右图中，圆与正六边形的周长相差多少厘米？（圆周率：3.14）",
                prompt="求圆与正六边形周长之差的问题",
                semantic_role="question",
                x=15,
                y=18,
                width=656,
                height=36,
                font_size=22,
                line_height=1.25,
                fill="#111111",
                align="left",
            ),
            # 圆：直径30 cm，半径15 cm
            CircleSlot(
                id="slot.circle",
                prompt="直径为30 cm的圆",
                cx=336,
                cy=264,
                r=100,
                fill="#ffffff",
                stroke="#202020",
                stroke_width=2,
            ),
            # 圆内接正六边形
            # 圆心 (565, 225)，半径100 px
            # 顶点：0°、60°、120°、180°、240°、300°
            PolygonSlot(
                id="slot.hexagon",
                prompt="圆内接正六边形",
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
            # 连接正六边形相对顶点的直径
            LineSlot(
                id="slot.diameter_line",
                prompt="圆的直径30 cm",
                x1=236,
                y1=264,
                x2=436,
                y2=264,
                stroke="#202020",
                stroke_width=2,
            ),
            CircleSlot(
                id="slot.center_point",
                prompt="圆心",
                cx=336,
                cy=264,
                r=4.5,
                fill="#ff3f7f",
                stroke="none",
                stroke_width=0,
            ),
            TextSlot(
                id="slot.label_30",
                prompt="直径长度标注",
                text="30 cm",
                x=336,
                y=230,
                font_size=24,
                anchor="middle",
                fill="#222222",
            ),
            BlankSlot(
                id="slot.answer",
                prompt="圆与正六边形的周长之差",
                answer_key="4.2cm",
                placeholder="答案",
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
        "language": "zh-CN",
        "question": ("在右图中，圆与正六边形的周长相差多少厘米？（圆周率：3.14）"),
        "instruction": (
            "先根据圆的直径求出半径，并利用圆内接正六边形的" "边长等于圆的半径这一性质。"
        ),
    },
    "domain": {
        "objects": [
            {
                "id": "obj.circle",
                "type": "circle",
                "label": "圆",
                "center_ref": "point.center",
                "diameter": 30,
                "radius": 15,
                "unit": "cm",
            },
            {
                "id": "obj.hexagon",
                "type": "regular_polygon",
                "label": "正六边形",
                "sides": 6,
                "inscribed_in": "obj.circle",
                "side_length": 15,
                "unit": "cm",
            },
            {
                "id": "point.center",
                "type": "point",
                "label": "圆心",
            },
            {
                "id": "measure.diameter",
                "type": "length",
                "label": "圆的直径",
                "value": 30,
                "unit": "cm",
            },
            {
                "id": "const.pi",
                "type": "constant",
                "label": "圆周率",
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
            "description": "圆的周长减去正六边形周长所得的值",
        },
        "value": 4.2,
        "unit": "cm",
    },
}


# Editor-build compatibility payload. The visual layout above is authored; this
# block keeps generated ids and answer/solvable shapes aligned with schemas.
PROBLEM_ID = "六年级_圆与正六边形周长之差_0002"
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
        "description": "圆的周长减去正六边形周长所得的值",
    },
    "value": 4.2,
    "unit": "cm",
}

SEMANTIC_OVERRIDE["problem_id"] = PROBLEM_ID
SEMANTIC_OVERRIDE["answer"] = ANSWER

SOLVABLE = {
    "schema": "modu.solvable.v1.1",
    "problem_id": PROBLEM_ID,
    "problem_type": "numeric_answer_perimeter_difference",
    "inputs": {
        "diameter": 30,
        "pi": 3.14,
        "polygon_sides": 6,
        "target_label": "圆与正六边形的周长之差",
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
    "method": "compare_circle_and_inscribed_hexagon_perimeters",
    "plan": [
        "将圆的直径30 cm除以2，求出半径15 cm。",
        "圆内接正六边形的边长等于圆的半径，因此边长是15 cm。",
        "分别求出圆的周长和正六边形的周长。",
        "用圆的周长减去正六边形的周长，求出两者的差。",
    ],
    "steps": [
        {
            "id": "step.1",
            "expr": "30 ÷ 2",
            "value": {"result": 15, "meaning": "圆的半径", "unit": "cm"},
            "explanation": "直径30 cm除以2，半径就是15 cm。",
        },
        {
            "id": "step.2",
            "expr": "正六边形的一条边 = 圆的半径",
            "value": {"result": 15, "meaning": "正六边形的一条边", "unit": "cm"},
            "explanation": "圆内接正六边形的边长等于圆的半径。",
        },
        {
            "id": "step.3",
            "expr": "30 × 3.14",
            "value": {"result": 94.2, "meaning": "圆的周长", "unit": "cm"},
            "explanation": "圆的周长等于直径乘以圆周率，因此是94.2 cm。",
        },
        {
            "id": "step.4",
            "expr": "15 × 6",
            "value": {"result": 90, "meaning": "正六边形的周长", "unit": "cm"},
            "explanation": "正六边形有6条边，因此周长是90 cm。",
        },
        {
            "id": "step.5",
            "expr": "94.2 - 90",
            "value": {"result": 4.2, "meaning": "圆与正六边形的周长之差", "unit": "cm"},
            "explanation": "圆的周长94.2 cm减去正六边形的周长90 cm，结果是4.2 cm。",
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
