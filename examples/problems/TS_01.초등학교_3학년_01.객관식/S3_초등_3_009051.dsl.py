from __future__ import annotations
from modu_math.dsl import Canvas, ProblemTemplate, Region, TextSlot, LineSlot, CircleSlot, PathSlot


def build_problem_template() -> ProblemTemplate:
    return ProblemTemplate(
        id="S3_초등_3_009051",
        title="반직선을 찾아 선택하세요",
        canvas=Canvas(width=720, height=292, coordinate_mode="logical"),
        regions=(
            Region(id="region.stem", role="stem", flow="absolute", slot_ids=("slot.q1",)),
            Region(
                id="region.options",
                role="diagram",
                flow="absolute",
                slot_ids=(
                    "slot.opt1.line1",
                    "slot.opt1.line2",
                    "slot.opt1.pt1",
                    "slot.opt1.pt2",
                    "slot.opt1.pt3",
                    "slot.opt2.line1",
                    "slot.opt2.pt1",
                    "slot.opt2.pt2",
                    "slot.opt3.curve1",
                    "slot.opt3.pt1",
                    "slot.opt3.pt2",
                    "slot.ans.line1",
                    "slot.ans.pt1",
                    "slot.ans.pt2",
                ),
            ),
            Region(id="region.explanation", role="supporting_text", flow="absolute", slot_ids=()),
        ),
        slots=(
            TextSlot(
                id="slot.q1",
                prompt="",
                text="□ 89. 반직선을 찾아 선택하세요.",
                style_role="question",
                x=10.0,
                y=28.0,
                font_size=28,
            ),
            LineSlot(id="slot.opt1.line1", prompt="", x1=120.0, y1=53.0, x2=145.0, y2=108.0),
            LineSlot(id="slot.opt1.line2", prompt="", x1=145.0, y1=108.0, x2=230.0, y2=114.0),
            CircleSlot(id="slot.opt1.pt1", prompt="", cx=123.0, cy=54.0, r=2.8, fill="#222222"),
            CircleSlot(id="slot.opt1.pt2", prompt="", cx=178.0, cy=110.0, r=2.8, fill="#222222"),
            CircleSlot(id="slot.opt1.pt3", prompt="", cx=227.0, cy=113.0, r=2.8, fill="#222222"),
            LineSlot(id="slot.opt2.line1", prompt="", x1=358.0, y1=109.0, x2=499.0, y2=37.0),
            CircleSlot(id="slot.opt2.pt1", prompt="", cx=385.0, cy=95.0, r=2.8, fill="#222222"),
            CircleSlot(id="slot.opt2.pt2", prompt="", cx=490.0, cy=42.0, r=2.8, fill="#222222"),
            PathSlot(
                id="slot.opt3.curve1",
                prompt="",
                d="M 610.0 45.0 C 602.0 58.0, 606.0 86.0, 629.0 101.0 C 645.0 112.0, 664.0 118.0, 687.0 118.0",
            ),
            CircleSlot(id="slot.opt3.pt1", prompt="", cx=608.0, cy=60.0, r=2.8, fill="#222222"),
            CircleSlot(id="slot.opt3.pt2", prompt="", cx=682.0, cy=117.0, r=2.8, fill="#222222"),
            LineSlot(id="slot.ans.line1", prompt="", x1=55.0, y1=180.0, x2=176.0, y2=118.0),
            CircleSlot(id="slot.ans.pt1", prompt="", cx=78.0, cy=168.0, r=2.8, fill="#222222"),
            CircleSlot(id="slot.ans.pt2", prompt="", cx=171.0, cy=121.0, r=2.8, fill="#222222"),
        ),
        diagrams=(),
        groups=(),
        constraints=(),
        tags=(),
    )


PROBLEM_TEMPLATE = build_problem_template()

SEMANTIC_OVERRIDE = {
    "problem_id": "S3_초등_3_009051",
    "problem_type": "도형분류",
    "metadata": {
        "language": "ko",
        "question": "반직선을 찾아 선택하세요.",
        "instruction": "그림들 중 반직선에 해당하는 것을 찾는다.",
    },
    "domain": {
        "objects": [
            {"id": "obj.option1", "type": "line_shape", "classification": "꺾인 선"},
            {"id": "obj.option2", "type": "line_shape", "classification": "반직선 후보"},
            {"id": "obj.option3", "type": "line_shape", "classification": "굽은 선"},
        ],
        "relations": [],
        "problem_solving": {
            "understand": {
                "given_refs": ["obj.option1", "obj.option2", "obj.option3"],
                "target_ref": "answer.target",
                "condition_refs": ["rel.options_compare"],
            },
            "plan": {
                "method": "shape_classification",
                "description": "각 그림이 반직선인지 도형의 종류를 보고 판단한다.",
            },
            "execute": {"expected_operations": ["compare_shape_types", "exclude_non_ray_shapes"]},
            "review": {"check_methods": ["shape_type_consistency_check"]},
        },
    },
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {"type": "selected_shape", "description": "반직선인 그림"},
        "value": None,
        "unit": "",
    },
}

SOLVABLE = {
    "schema": "modu.solvable.v1.1",
    "problem_id": "S3_초등_3_009051",
    "problem_type": "도형분류",
    "inputs": {
        "total_ticks": 3,
        "target_label": "반직선",
        "target_ticks": 1,
        "target_count": 1,
        "unit": "",
    },
    "given": [
        {"ref": "obj.option1", "value": {"classification": "꺾인 선"}},
        {"ref": "obj.option2", "value": {"classification": "반직선 후보"}},
        {"ref": "obj.option3", "value": {"classification": "굽은 선"}},
    ],
    "target": {"ref": "answer.target", "type": "selected_shape"},
    "method": "shape_classification",
    "plan": ["세 그림의 선의 모양을 비교한다.", "반직선이 아닌 꺾인 선과 굽은 선을 제외한다."],
    "steps": [
        {"id": "step.1", "expr": "첫째 그림은 꺾인 선", "value": "꺾인 선"},
        {"id": "step.2", "expr": "셋째 그림은 굽은 선", "value": "굽은 선"},
        {"id": "step.3", "expr": "반직선에 해당하는 그림을 선택", "value": None},
    ],
    "checks": [
        {
            "id": "check.1",
            "expr": "꺾인 선과 굽은 선은 반직선이 아님",
            "expected": True,
            "actual": True,
            "pass": True,
        }
    ],
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {"type": "selected_shape", "description": "반직선인 그림"},
        "value": None,
        "unit": "",
    },
}
