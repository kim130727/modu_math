from __future__ import annotations

from modu_math.dsl import (
    Canvas,
    LineSlot,
    PolygonSlot,
    ProblemTemplate,
    RectSlot,
    Region,
    TextSlot,
)


SEMANTIC_OVERRIDE = {
    "problem_type": "geometry_perimeter_word_problem",
    "metadata": {
        "instruction": "철사의 길이는 변하지 않는다.",
        "question": "세로가 18cm인 가장 큰 직사각형 1개를 만들 때 가로는 몇 cm인가?",
        "tags": ["perimeter", "rectangle", "square", "conservation"],
    },
    "domain": {
        "objects": [
            {
                "id": "shape.square",
                "type": "square",
                "properties": {"side_cm": 13},
                "confidence": 1.0,
            },
            {
                "id": "shape.rectangle",
                "type": "rectangle",
                "properties": {"height_cm": 18},
                "confidence": 1.0,
            },
            {
                "id": "wire",
                "type": "wire",
                "properties": {"length_preserved": True},
                "confidence": 1.0,
            },
            {
                "id": "var.width",
                "type": "variable",
                "properties": {"name": "가로"},
                "confidence": 1.0,
            },
        ],
        "relations": [
            {
                "id": "rel.perimeter.square",
                "type": "equation",
                "from_id": "shape.square",
                "to_id": "wire",
                "properties": {"expr": "wire_length = 4 * 13"},
                "confidence": 1.0,
            },
            {
                "id": "rel.perimeter.rectangle",
                "type": "equation",
                "from_id": "shape.rectangle",
                "to_id": "wire",
                "properties": {"expr": "2 * (18 + 가로) = wire_length"},
                "confidence": 1.0,
            },
            {
                "id": "rel.target",
                "type": "target",
                "from_id": "shape.rectangle",
                "to_id": "var.width",
                "properties": {"ask": "가로"},
                "confidence": 1.0,
            },
        ],
        "confidence": 1.0,
    },
    "answer": {
        "value": 8,
        "unit": "cm",
        "source": "perimeter_conservation",
        "confidence": 1.0,
    },
}


SOLVABLE = {
    "schema": "modu.solvable.v1",
    "problem_id": "Hpdf_8FrirrzBkE",
    "problem_type": "geometry_perimeter_word_problem",
    "inputs": {
        "total_ticks": 52,
        "target_label": "직사각형 가로",
        "target_ticks": 8,
        "target_count": 1,
        "unit": "cm",
    },
    "plan": [
        "정사각형 둘레로 철사 길이를 구한다.",
        "직사각형 둘레식과 철사 길이를 같다고 두고 가로를 구한다.",
    ],
    "steps": [
        {"id": "s1", "expr": "wire_length = 4 * 13", "value": 52},
        {"id": "s2", "expr": "2 * (18 + w) = 52", "value": "18 + w = 26"},
        {"id": "s3", "expr": "w = 26 - 18", "value": 8},
    ],
    "checks": [
        {"id": "c1", "expr": "2 * (18 + 8)", "expected": 52, "actual": 52, "pass": True}
    ],
    "answer": {"value": 8, "unit": "cm"},
}


def build_problem_template() -> ProblemTemplate:
    return ProblemTemplate(
        id="Hpdf_8FrirrzBkE",
        title="철사로 만든 도형의 가로 구하기",
        canvas=Canvas(width=750, height=550, coordinate_mode="logical"),
        regions=(
            Region(
                id="region.stem",
                role="stem",
                flow="absolute",
                slot_ids=(
                    "slot.q1",
                    "slot.q2",
                    "slot.q3",
                    "slot.left.rect",
                    "slot.left.cm",
                    "slot.arrow",
                    "slot.arrow.head",
                    "slot.right.rect",
                    "slot.right.cm",
                ),
            ),
        ),
        slots=(
            TextSlot(
                id="slot.q1",
                prompt="",
                text="철사를 사용하여 한 변이 13cm인 정사각형을 만들었습니다.",
                style_role="body",
                x=12.0,
                y=50.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.q2",
                prompt="",
                text="이 철사를 펴서 세로가 18cm인 가장 큰 직사각형 1개를 만들 때,",
                style_role="body",
                x=12.0,
                y=100.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.q3",
                prompt="",
                text="이 직사각형의 가로는 몇 cm입니까?",
                style_role="question",
                x=12.0,
                y=150.0,
                font_size=28,
            ),
            RectSlot(
                id="slot.left.rect",
                prompt="",
                x=50.0,
                y=280.0,
                width=130.0,
                height=130.0,
                stroke="#888888",
                stroke_width=2.0,
                fill="none",
            ),
            TextSlot(
                id="slot.left.cm",
                prompt="",
                text="13cm",
                style_role="body",
                x=190.0,
                y=350.0,
                font_size=28,
            ),
            LineSlot(
                id="slot.arrow",
                prompt="",
                x1=290.0,
                y1=340.0,
                x2=376.0,
                y2=340.0,
                stroke="#666666",
                stroke_width=2.0,
            ),
            PolygonSlot(
                id="slot.arrow.head",
                prompt="",
                x=376.0,
                y=340.0,
                points=((0.0, 0.0), (-8.0, -6.0), (-8.0, 6.0)),
                stroke="#666666",
                stroke_width=2.0,
                fill="#666666",
            ),
            RectSlot(
                id="slot.right.rect",
                prompt="",
                x=450.0,
                y=255.0,
                width=80.0,
                height=180.0,
                stroke="#888888",
                stroke_width=2.0,
                fill="none",
            ),
            TextSlot(
                id="slot.right.cm",
                prompt="",
                text="18cm",
                style_role="body",
                x=540.0,
                y=350.0,
                font_size=28,
            ),
        ),
        diagrams=(),
        groups=(),
        constraints=(),
        tags=("perimeter", "wire", "rectangle"),
    )


PROBLEM_TEMPLATE = build_problem_template()
