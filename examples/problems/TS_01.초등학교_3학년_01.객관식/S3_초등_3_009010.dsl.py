from __future__ import annotations
from modu_math.dsl import Canvas, ProblemTemplate, Region, TextSlot, LineSlot, CircleSlot


def build_problem_template() -> ProblemTemplate:
    return ProblemTemplate(
        id="S3_초등_3_009010",
        title="선분과 반직선",
        canvas=Canvas(width=856.0, height=300.0, coordinate_mode="logical"),
        regions=(
            Region(
                id="region.stem",
                role="stem",
                flow="absolute",
                slot_ids=(
                    "slot.qnum",
                    "slot.q1",
                    "slot.q2",
                    "slot.q3",
                    "slot.q4",
                    "slot.q5",
                    "slot.q6",
                    "slot.q7",
                    "slot.q8",
                    "slot.q9",
                    "slot.q10",
                    "slot.q11",
                    "slot.q12",
                    "slot.q14",
                    "slot.q15",
                    "slot.q16",
                    "slot.q17",
                    "slot.q18",
                    "slot.q21",
                    "slot.q22",
                    "slot.q23",
                    "slot.q24",
                    "slot.q25",
                    "slot.q26",
                    "slot.q27",
                ),
            ),
        ),
        slots=(
            TextSlot(
                id="slot.qnum",
                prompt="",
                text="49.",
                style_role="question",
                x=22.0,
                y=26.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.q1",
                prompt="",
                text="점 ㄴ에서 시작하여 점 ㄱ을 지나 왼쪽으로 길게 늘인 곧은 선을 알맞",
                style_role="question",
                x=76.0,
                y=26.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.q2",
                prompt="",
                text="은 것을 선택하세요.",
                style_role="question",
                x=28.0,
                y=60.0,
                font_size=28,
            ),
            LineSlot(id="slot.q3", prompt="", x1=293.0, y1=95.0, x2=576.0, y2=95.0),
            CircleSlot(id="slot.q4", prompt="", cx=348.0, cy=95.0, r=4.2, fill="#222222"),
            CircleSlot(id="slot.q5", prompt="", cx=571.0, cy=95.0, r=4.2, fill="#222222"),
            TextSlot(
                id="slot.q6",
                prompt="",
                text="ㄱ",
                style_role="label",
                x=341.0,
                y=70.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.q7",
                prompt="",
                text="ㄴ",
                style_role="label",
                x=566.0,
                y=70.0,
                font_size=28,
            ),
            LineSlot(id="slot.q8", prompt="", x1=313.0, y1=148.0, x2=576.0, y2=148.0),
            CircleSlot(id="slot.q9", prompt="", cx=316.0, cy=148.0, r=4.2, fill="#222222"),
            CircleSlot(id="slot.q10", prompt="", cx=571.0, cy=148.0, r=4.2, fill="#222222"),
            TextSlot(
                id="slot.q11",
                prompt="",
                text="ㄱ",
                style_role="label",
                x=308.0,
                y=123.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.q12",
                prompt="",
                text="ㄴ",
                style_role="label",
                x=566.0,
                y=123.0,
                font_size=28,
            ),
            LineSlot(id="slot.q14", prompt="", x1=93.0, y1=190.0, x2=272.0, y2=190.0),
            CircleSlot(id="slot.q15", prompt="", cx=94.0, cy=190.0, r=4.2, fill="#222222"),
            CircleSlot(id="slot.q16", prompt="", cx=273.0, cy=190.0, r=4.2, fill="#222222"),
            TextSlot(
                id="slot.q17",
                prompt="",
                text="ㄱ",
                style_role="label",
                x=87.0,
                y=165.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.q18",
                prompt="",
                text="ㄴ",
                style_role="label",
                x=266.0,
                y=165.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.q21", prompt="", text="", style_role="label", x=0.0, y=0.0, font_size=28
            ),
            TextSlot(
                id="slot.q22", prompt="", text="", style_role="label", x=0.0, y=0.0, font_size=28
            ),
            TextSlot(
                id="slot.q23", prompt="", text="", style_role="label", x=0.0, y=0.0, font_size=28
            ),
            TextSlot(
                id="slot.q24", prompt="", text="", style_role="label", x=0.0, y=0.0, font_size=28
            ),
            TextSlot(
                id="slot.q25", prompt="", text="", style_role="label", x=0.0, y=0.0, font_size=28
            ),
            TextSlot(
                id="slot.q26", prompt="", text="", style_role="label", x=0.0, y=0.0, font_size=28
            ),
            TextSlot(
                id="slot.q27", prompt="", text="", style_role="label", x=0.0, y=0.0, font_size=28
            ),
        ),
        diagrams=(),
        groups=(),
        constraints=(),
        tags=(),
    )


PROBLEM_TEMPLATE = build_problem_template()

SEMANTIC_OVERRIDE = {
    "problem_id": "S3_초등_3_009010",
    "problem_type": "geometry_choice",
    "metadata": {
        "language": "ko",
        "question": "점 ㄴ에서 시작하여 점 ㄱ을 지나 왼쪽으로 길게 늘인 곧은 선을 고르는 문제",
        "instruction": "알맞은 것을 선택하세요.",
    },
    "domain": {
        "objects": [
            {"id": "obj.point.giyeok", "type": "point", "label": "ㄱ"},
            {"id": "obj.point.nieun", "type": "point", "label": "ㄴ"},
            {"id": "obj.line_candidate", "type": "line_shape"},
        ],
        "relations": [],
        "problem_solving": {
            "understand": {
                "given_refs": ["obj.point.giyeok", "obj.point.nieun", "obj.line_candidate"],
                "target_ref": "answer.target",
                "condition_refs": ["rel.starts_at", "rel.passes_through", "rel.extends_left"],
            },
            "plan": {
                "method": "shape_matching",
                "description": "시작점, 통과점, 방향 조건이 맞는 선 모양을 찾는다.",
            },
            "execute": {
                "expected_operations": ["compare_shapes", "match_direction", "match_points"]
            },
            "review": {"check_methods": ["condition_consistency_check"]},
        },
    },
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {
            "type": "ray_shape",
            "description": "점 ㄴ에서 시작하여 점 ㄱ을 지나 왼쪽으로 길게 늘인 곧은 선",
        },
        "value": 0,
        "unit": "",
    },
}

SOLVABLE = {
    "schema": "modu.solvable.v1.1",
    "problem_id": "S3_초등_3_009010",
    "problem_type": "geometry_choice",
    "inputs": {
        "total_ticks": 1,
        "target_label": "점 ㄴ에서 시작하여 점 ㄱ을 지나 왼쪽으로 길게 늘인 곧은 선",
        "target_ticks": 1,
        "target_count": 1,
        "unit": "",
    },
    "given": [
        {"ref": "obj.point.giyeok", "value": {"label": "ㄱ"}},
        {"ref": "obj.point.nieun", "value": {"label": "ㄴ"}},
    ],
    "target": {"ref": "answer.target", "type": "ray_shape"},
    "method": "shape_matching",
    "plan": [
        "시작점이 ㄴ인지 확인한다.",
        "ㄱ을 지나가는지 확인한다.",
        "왼쪽으로 길게 늘어진 모양인지 확인한다.",
    ],
    "steps": [
        {"id": "step.1", "expr": "점 ㄴ에서 시작하는지 확인", "value": True},
        {"id": "step.2", "expr": "점 ㄱ을 지나는지 확인", "value": True},
        {"id": "step.3", "expr": "왼쪽 방향으로 연장되는지 확인", "value": True},
    ],
    "checks": [
        {
            "id": "check.1",
            "expr": "시작점, 통과점, 방향 조건이 모두 일치하는가",
            "expected": True,
            "actual": True,
            "pass": True,
        }
    ],
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {
            "type": "ray_shape",
            "description": "점 ㄴ에서 시작하여 점 ㄱ을 지나 왼쪽으로 길게 늘인 곧은 선",
        },
        "value": 0,
        "unit": "",
    },
}
