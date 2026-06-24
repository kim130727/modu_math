from __future__ import annotations
from modu_math.dsl import Canvas, ProblemTemplate, Region, TextSlot, LineSlot, CircleSlot, RectSlot


def build_problem_template() -> ProblemTemplate:
    return ProblemTemplate(
        id="S3_초등_3_009047",
        title="반직선 ㄴ ㄱ 판독",
        canvas=Canvas(width=760, height=285, coordinate_mode="logical"),
        regions=(
            Region(
                id="region.header",
                role="stem",
                flow="absolute",
                slot_ids=("slot.box", "slot.no", "slot.q"),
            ),
            Region(
                id="region.figures.top",
                role="diagram",
                flow="absolute",
                slot_ids=(
                    "slot.top.left.line",
                    "slot.top.left.pt1",
                    "slot.top.left.pt2",
                    "slot.top.left.lb1",
                    "slot.top.left.lb2",
                    "slot.top.right.line",
                    "slot.top.right.pt1",
                    "slot.top.right.pt2",
                    "slot.top.right.lb1",
                    "slot.top.right.lb2",
                ),
            ),
            Region(
                id="region.answer",
                role="diagram",
                flow="absolute",
                slot_ids=("slot.answer.line", "slot.answer.pt1", "slot.answer.pt2"),
            ),
            Region(id="region.explanation", role="explanation", flow="absolute", slot_ids=()),
        ),
        slots=(
            RectSlot(id="slot.box", prompt="", x=16.0, y=16.0, width=12.0, height=12.0),
            TextSlot(
                id="slot.no",
                prompt="",
                text="85.",
                style_role="question",
                x=38.0,
                y=27.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.q",
                prompt="",
                text="반직선 ㄴ ㄱ으로 알맞은 것을 고르세요.",
                style_role="question",
                x=90.0,
                y=27.0,
                font_size=28,
            ),
            LineSlot(id="slot.top.left.line", prompt="", x1=116.0, y1=90.0, x2=404.0, y2=90.0),
            CircleSlot(id="slot.top.left.pt1", prompt="", cx=156.0, cy=90.0, r=4.0, fill="#222222"),
            CircleSlot(id="slot.top.left.pt2", prompt="", cx=400.0, cy=90.0, r=4.0, fill="#222222"),
            TextSlot(
                id="slot.top.left.lb1",
                prompt="",
                text="ㄱ",
                style_role="label",
                x=150.0,
                y=74.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.top.left.lb2",
                prompt="",
                text="ㄴ",
                style_role="label",
                x=395.0,
                y=74.0,
                font_size=28,
            ),
            LineSlot(id="slot.top.right.line", prompt="", x1=486.0, y1=90.0, x2=740.0, y2=90.0),
            CircleSlot(
                id="slot.top.right.pt1", prompt="", cx=486.0, cy=90.0, r=4.0, fill="#222222"
            ),
            CircleSlot(
                id="slot.top.right.pt2", prompt="", cx=736.0, cy=90.0, r=4.0, fill="#222222"
            ),
            TextSlot(
                id="slot.top.right.lb1",
                prompt="",
                text="ㄱ",
                style_role="label",
                x=480.0,
                y=74.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.top.right.lb2",
                prompt="",
                text="ㄴ",
                style_role="label",
                x=731.0,
                y=74.0,
                font_size=28,
            ),
            LineSlot(id="slot.answer.line", prompt="", x1=66.0, y1=159.0, x2=264.0, y2=159.0),
            CircleSlot(id="slot.answer.pt1", prompt="", cx=74.0, cy=159.0, r=4.0, fill="#222222"),
            CircleSlot(id="slot.answer.pt2", prompt="", cx=260.0, cy=159.0, r=4.0, fill="#222222"),
        ),
        diagrams=(),
        groups=(),
        constraints=(),
        tags=(),
    )


PROBLEM_TEMPLATE = build_problem_template()

SEMANTIC_OVERRIDE = {
    "problem_id": "S3_초등_3_009047",
    "problem_type": "geometry_ray_reading",
    "metadata": {
        "language": "ko",
        "question": "반직선 ㄴ ㄱ으로 알맞은 것을 고르세요.",
        "instruction": "도형에서 반직선의 시작점과 지나는 점의 관계를 읽는다.",
    },
    "domain": {
        "objects": [
            {"id": "obj.point.giyeok", "type": "point", "label": "ㄱ"},
            {"id": "obj.point.nieun", "type": "point", "label": "ㄴ"},
            {
                "id": "obj.ray",
                "type": "ray",
                "start_ref": "obj.point.nieun",
                "passes_through_ref": "obj.point.giyeok",
            },
        ],
        "relations": [],
        "problem_solving": {
            "understand": {
                "given_refs": ["obj.point.giyeok", "obj.point.nieun", "obj.ray"],
                "target_ref": "answer.target",
                "condition_refs": ["rel.ray_direction"],
            },
            "plan": {
                "method": "ray_reading",
                "description": "반직선의 시작점과 지나가는 점의 순서를 읽는다.",
            },
            "execute": {"expected_operations": ["identify_start_point", "identify_through_point"]},
            "review": {"check_methods": ["direction_order_check"]},
        },
    },
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {"type": "selected_ray", "description": "ㄴ에서 시작하여 ㄱ을 지나는 반직선"},
        "value": 1,
        "unit": "",
    },
}

SOLVABLE = {
    "schema": "modu.solvable.v1.1",
    "problem_id": "S3_초등_3_009047",
    "problem_type": "geometry_ray_reading",
    "inputs": {
        "total_ticks": 0,
        "target_label": "ㄴ ㄱ",
        "target_ticks": 0,
        "target_count": 1,
        "unit": "",
    },
    "given": [
        {"ref": "obj.point.giyeok", "value": {"label": "ㄱ"}},
        {"ref": "obj.point.nieun", "value": {"label": "ㄴ"}},
        {
            "ref": "obj.ray",
            "value": {"start_ref": "obj.point.nieun", "passes_through_ref": "obj.point.giyeok"},
        },
    ],
    "target": {"ref": "answer.target", "type": "selected_ray"},
    "method": "ray_reading",
    "plan": [
        "반직선의 이름 순서를 보고 시작점과 지나가는 점을 확인한다.",
        "ㄴ에서 시작하여 ㄱ을 지나는 그림을 찾는다.",
    ],
    "steps": [
        {"id": "step.1", "expr": "ㄴ을 시작점으로 본다.", "value": "start=ㄴ"},
        {"id": "step.2", "expr": "ㄱ을 지나는지 확인한다.", "value": "through=ㄱ"},
        {"id": "step.3", "expr": "반직선 ㄴ ㄱ을 선택한다.", "value": "selected"},
    ],
    "checks": [
        {
            "id": "check.1",
            "expr": "start=ㄴ and through=ㄱ",
            "expected": True,
            "actual": True,
            "pass": True,
        }
    ],
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {"type": "selected_ray", "description": "ㄴ에서 시작하여 ㄱ을 지나는 반직선"},
        "value": 1,
        "unit": "",
    },
}
