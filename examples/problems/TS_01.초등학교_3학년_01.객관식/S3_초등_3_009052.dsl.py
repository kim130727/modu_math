from __future__ import annotations
from modu_math.dsl import Canvas, CircleSlot, LineSlot, ProblemTemplate, Region, TextSlot


def build_problem_template() -> ProblemTemplate:
    return ProblemTemplate(
        id="S3_초등_3_009052",
        title="직선을 찾아 선택하세요.",
        canvas=Canvas(width=735, height=348, coordinate_mode="logical"),
        regions=(
            Region(
                id="region.stem",
                role="stem",
                flow="absolute",
                slot_ids=(
                    "slot.no",
                    "slot.instruction",
                    "slot.figure.left",
                    "slot.figure.middle",
                    "slot.figure.right",
                    "slot.answer.figure",
                ),
            ),
        ),
        slots=(
            TextSlot(
                id="slot.no",
                prompt="",
                text="90.",
                style_role="question",
                x=9.0,
                y=27.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.instruction",
                prompt="",
                text="직선을 찾아 선택하세요.",
                style_role="question",
                x=54.0,
                y=28.0,
                font_size=28,
            ),
            LineSlot(id="slot.figure.left", prompt="", x1=153.0, y1=106.0, x2=251.0, y2=106.0),
            CircleSlot(
                id="slot.figure.left.p1", prompt="", cx=154.0, cy=106.0, r=2.4, fill="#222222"
            ),
            CircleSlot(
                id="slot.figure.left.p2", prompt="", cx=250.0, cy=106.0, r=2.4, fill="#222222"
            ),
            PathSlot(
                id="slot.figure.middle",
                prompt="",
                d="M 394.0 83.0 C 417.0 83.0 439.0 89.0 454.0 102.0 C 460.0 107.0 465.0 115.0 470.0 124.0",
            ),
            CircleSlot(
                id="slot.figure.middle.p1", prompt="", cx=395.0, cy=83.0, r=2.4, fill="#222222"
            ),
            CircleSlot(
                id="slot.figure.middle.p2", prompt="", cx=454.0, cy=102.0, r=2.4, fill="#222222"
            ),
            CircleSlot(
                id="slot.figure.middle.p3", prompt="", cx=469.0, cy=124.0, r=2.4, fill="#222222"
            ),
            LineSlot(id="slot.figure.right", prompt="", x1=617.0, y1=104.0, x2=695.0, y2=27.0),
            CircleSlot(
                id="slot.figure.right.p1", prompt="", cx=617.0, cy=104.0, r=2.4, fill="#222222"
            ),
            CircleSlot(
                id="slot.figure.right.p2", prompt="", cx=695.0, cy=27.0, r=2.4, fill="#222222"
            ),
            LineSlot(id="slot.answer.figure", prompt="", x1=45.0, y1=316.0, x2=143.0, y2=218.0),
            CircleSlot(
                id="slot.answer.figure.p1", prompt="", cx=46.0, cy=315.0, r=2.4, fill="#222222"
            ),
            CircleSlot(
                id="slot.answer.figure.p2", prompt="", cx=142.0, cy=219.0, r=2.4, fill="#222222"
            ),
        ),
        diagrams=(),
        groups=(),
        constraints=(),
        tags=(),
    )


PROBLEM_TEMPLATE = build_problem_template()

SEMANTIC_OVERRIDE = {
    "problem_id": "S3_초등_3_009052",
    "problem_type": "선의 종류 식별",
    "metadata": {
        "language": "ko",
        "question": "직선을 찾아 선택하세요.",
        "instruction": "직선을 찾는 문제",
    },
    "domain": {
        "objects": [
            {"id": "obj.figure.left", "type": "line_shape", "kind": "segment"},
            {"id": "obj.figure.middle", "type": "line_shape", "kind": "curve"},
            {"id": "obj.figure.right", "type": "line_shape", "kind": "line"},
        ],
        "relations": [],
        "problem_solving": {
            "understand": {
                "given_refs": ["obj.figure.left", "obj.figure.middle", "obj.figure.right"],
                "target_ref": "answer.target",
                "condition_refs": ["rel.compare_shapes"],
            },
            "plan": {
                "method": "shape_classification",
                "description": "그림들의 모양을 비교하여 직선인지 선분인지 곡선인지 구분한다.",
            },
            "execute": {"expected_operations": ["compare_straightness", "identify_line"]},
            "review": {"check_methods": ["shape_type_consistency_check"]},
        },
    },
    "answer": {
        "target": {"type": "직선 찾기", "description": "여러 그림 중 직선인 것을 고른다."},
        "value": 0,
        "unit": "",
    },
}

SOLVABLE = {
    "schema": "modu.solvable.v1.1",
    "problem_id": "S3_초등_3_009052",
    "problem_type": "선의 종류 식별",
    "inputs": {
        "total_ticks": 0,
        "target_label": "직선",
        "target_ticks": 0,
        "target_count": 1,
        "unit": "",
    },
    "given": [
        {"ref": "obj.figure.left", "value": {"kind": "segment"}},
        {"ref": "obj.figure.middle", "value": {"kind": "curve"}},
        {"ref": "obj.figure.right", "value": {"kind": "line"}},
    ],
    "target": {"ref": "answer.target", "type": "직선 찾기"},
    "method": "shape_classification",
    "plan": [
        "그림의 모양을 보고 직선인지 선분인지 굽은 선인지 구분한다.",
        "직선에 해당하는 그림을 찾는다.",
    ],
    "steps": [
        {"id": "step.1", "expr": "왼쪽 그림은 선분으로 분류한다.", "value": "segment"},
        {"id": "step.2", "expr": "가운데 그림은 굽은 선으로 분류한다.", "value": "curve"},
        {"id": "step.3", "expr": "직선 후보를 확인한다.", "value": "line"},
    ],
    "checks": [
        {
            "id": "check.1",
            "expr": "직선, 선분, 굽은 선을 서로 구분했는가",
            "expected": True,
            "actual": True,
            "pass": True,
        }
    ],
    "answer": {"value": 0, "unit": "", "derived_from": "step.3"},
}
