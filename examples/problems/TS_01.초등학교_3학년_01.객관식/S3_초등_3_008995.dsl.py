from __future__ import annotations
from modu_math.dsl import Canvas, ProblemTemplate, Region, TextSlot, RectSlot, CircleSlot


def build_problem_template() -> ProblemTemplate:
    return ProblemTemplate(
        id="S3_초등_3_008995",
        title="정사각형 판별",
        canvas=Canvas(width=850, height=380, coordinate_mode="logical"),
        regions=(
            Region(
                id="region.stem",
                role="stem",
                flow="absolute",
                slot_ids=(
                    "slot.q1",
                    "slot.shape1",
                    "slot.answer.circle",
                    "slot.example.shape",
                    "slot.example.corner1",
                    "slot.example.corner2",
                    "slot.example.corner3",
                    "slot.example.corner4",
                ),
            ),
        ),
        slots=(
            TextSlot(
                id="slot.q1",
                prompt="",
                text="33. 정사각형이면 ○, 정사각형이 아니면 ×를 선택하세요.",
                style_role="question",
                x=10.0,
                y=18.0,
                font_size=28,
            ),
            RectSlot(
                id="slot.shape1",
                prompt="",
                x=378.0,
                y=41.0,
                width=83.0,
                height=84.0,
                fill="none",
                stroke="#888888",
                stroke_width=1.5,
            ),
            CircleSlot(
                id="slot.answer.circle",
                prompt="",
                cx=59.0,
                cy=146.0,
                r=9.0,
                fill="none",
                stroke="#444444",
                stroke_width=1.2,
            ),
            RectSlot(
                id="slot.example.shape",
                prompt="",
                x=32.0,
                y=283.0,
                width=86.0,
                height=86.0,
                fill="none",
                stroke="#888888",
                stroke_width=1.5,
            ),
            CircleSlot(
                id="slot.example.corner1",
                prompt="",
                cx=36.0,
                cy=287.0,
                r=3.5,
                fill="#8fd3ff",
                stroke="none",
            ),
            CircleSlot(
                id="slot.example.corner2",
                prompt="",
                cx=114.0,
                cy=287.0,
                r=3.5,
                fill="#8fd3ff",
                stroke="none",
            ),
            CircleSlot(
                id="slot.example.corner3",
                prompt="",
                cx=36.0,
                cy=365.0,
                r=3.5,
                fill="#8fd3ff",
                stroke="none",
            ),
            CircleSlot(
                id="slot.example.corner4",
                prompt="",
                cx=114.0,
                cy=365.0,
                r=3.5,
                fill="#8fd3ff",
                stroke="none",
            ),
        ),
        diagrams=(),
        groups=(),
        constraints=(),
        tags=(),
    )


PROBLEM_TEMPLATE = build_problem_template()

SEMANTIC_OVERRIDE = {
    "problem_id": "S3_초등_3_008995",
    "problem_type": "도형_판별",
    "metadata": {
        "language": "ko",
        "question": "정사각형이면 ○, 정사각형이 아니면 ×를 선택하는 문제",
        "instruction": "정사각형이면 ○, 정사각형이 아니면 ×를 선택하세요.",
    },
    "domain": {
        "objects": [
            {"id": "obj.target_shape", "type": "quadrilateral"},
            {
                "id": "obj.square_definition",
                "type": "shape_definition",
                "properties": ["네 각이 모두 직각", "네 변의 길이가 모두 같음"],
            },
            {"id": "obj.example_square", "type": "quadrilateral"},
        ],
        "relations": [],
        "problem_solving": {
            "understand": {
                "given_refs": ["obj.target_shape", "obj.square_definition"],
                "target_ref": "answer.target",
                "condition_refs": ["rel.classify_target_shape"],
            },
            "plan": {
                "method": "shape_classification",
                "description": "도형이 정사각형의 정의를 만족하는지 보고 ○ 또는 ×를 고른다.",
            },
            "execute": {
                "expected_operations": ["check_right_angles", "check_equal_sides", "choose_symbol"]
            },
            "review": {"check_methods": ["definition_match_check", "symbol_consistency_check"]},
        },
    },
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {"type": "selection", "description": "정사각형이면 ○, 정사각형이 아니면 ×"},
        "value": 0,
        "unit": "",
    },
}

SOLVABLE = {
    "schema": "modu.solvable.v1.1",
    "problem_id": "S3_초등_3_008995",
    "problem_type": "도형_판별",
    "inputs": {
        "total_ticks": 1,
        "target_label": "정사각형 판별",
        "target_ticks": 1,
        "target_count": 1,
        "unit": "",
    },
    "given": [
        {"ref": "obj.target_shape", "value": {"type": "quadrilateral"}},
        {
            "ref": "obj.square_definition",
            "value": {"properties": ["네 각이 모두 직각", "네 변의 길이가 모두 같음"]},
        },
    ],
    "target": {"ref": "answer.target", "type": "selection"},
    "method": "shape_classification",
    "plan": [
        "도형의 성질을 보고 정사각형인지 판단한다.",
        "정사각형의 정의와 일치하면 ○를, 아니면 ×를 고른다.",
    ],
    "steps": [
        {
            "id": "step.1",
            "expr": "정사각형의 정의 확인",
            "value": "네 각이 모두 직각이고 네 변의 길이가 모두 같은 사각형",
        },
        {"id": "step.2", "expr": "선택 기호 결정", "value": "미정"},
    ],
    "checks": [
        {
            "id": "check.1",
            "expr": "정의와 선택 기호가 일치하는지 확인",
            "expected": "○ 또는 ×",
            "actual": "미정",
            "pass": False,
        }
    ],
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {"type": "selection", "description": "정사각형이면 ○, 정사각형이 아니면 ×"},
        "value": 0,
        "unit": "",
    },
}
