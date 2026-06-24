from __future__ import annotations
from modu_math.dsl import Canvas, ProblemTemplate, Region, TextSlot, LineSlot, CircleSlot


def build_problem_template() -> ProblemTemplate:
    return ProblemTemplate(
        id="S3_초등_3_008982",
        title="각의 꼭짓점",
        canvas=Canvas(width=560, height=380, coordinate_mode="logical"),
        regions=(
            Region(
                id="region.top",
                role="stem",
                flow="absolute",
                slot_ids=("slot.q.symbol", "slot.q.text"),
            ),
            Region(
                id="region.diagram",
                role="figure",
                flow="absolute",
                slot_ids=(
                    "slot.line.base",
                    "slot.line.slant",
                    "slot.pt.vertex",
                    "slot.pt.left",
                    "slot.pt.top",
                    "slot.lb.left",
                    "slot.lb.vertex",
                    "slot.lb.top",
                    "slot.choice",
                ),
            ),
            Region(id="region.bottom", role="answer_explanation", flow="absolute", slot_ids=()),
        ),
        slots=(
            TextSlot(
                id="slot.q.symbol",
                prompt="",
                text="□ 17.",
                style_role="question",
                x=10.0,
                y=26.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.q.text",
                prompt="",
                text="각을 보고 꼭짓점을 선택하세요.",
                style_role="question",
                x=72.0,
                y=26.0,
                font_size=28,
            ),
            LineSlot(id="slot.line.base", prompt="", x1=301.0, y1=129.0, x2=445.0, y2=129.0),
            LineSlot(id="slot.line.slant", prompt="", x1=445.0, y1=129.0, x2=504.0, y2=49.0),
            CircleSlot(id="slot.pt.vertex", prompt="", cx=445.0, cy=129.0, r=3.8, fill="#222222"),
            CircleSlot(id="slot.pt.left", prompt="", cx=302.0, cy=129.0, r=3.8, fill="#222222"),
            CircleSlot(id="slot.pt.top", prompt="", cx=482.0, cy=68.0, r=3.8, fill="#222222"),
            TextSlot(
                id="slot.lb.left",
                prompt="",
                text="ㄷ",
                style_role="label",
                x=295.0,
                y=150.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.lb.vertex",
                prompt="",
                text="ㄹ",
                style_role="label",
                x=445.0,
                y=152.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.lb.top",
                prompt="",
                text="ㅁ",
                style_role="label",
                x=490.0,
                y=69.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.choice",
                prompt="",
                text="점 ( ㄷ , ㄹ , □ )",
                style_role="question",
                x=302.0,
                y=194.0,
                font_size=28,
            ),
        ),
        diagrams=(),
        groups=(),
        constraints=(),
        tags=("각", "꼭짓점", "도형"),
    )


PROBLEM_TEMPLATE = build_problem_template()

SEMANTIC_OVERRIDE = {
    "problem_id": "S3_초등_3_008982",
    "problem_type": "geometry_vertex_selection",
    "metadata": {
        "language": "ko",
        "question": "각을 보고 꼭짓점을 선택하세요.",
        "instruction": "보기에서 각의 꼭짓점에 해당하는 점을 고르기",
    },
    "domain": {
        "objects": [
            {"id": "obj.angle", "type": "angle"},
            {"id": "obj.point.d", "type": "point", "name": "ㄷ"},
            {"id": "obj.point.r", "type": "point", "name": "ㄹ"},
            {"id": "obj.point.m", "type": "point", "name": "ㅁ"},
        ],
        "relations": [],
        "problem_solving": {
            "understand": {
                "given_refs": ["obj.angle", "obj.point.d", "obj.point.r", "obj.point.m"],
                "target_ref": "answer.target",
                "condition_refs": ["rel.vertex"],
            },
            "plan": {
                "method": "vertex_identification",
                "description": "두 반직선이 만나는 점을 찾는다.",
            },
            "execute": {
                "expected_operations": [
                    "identify_intersection_point",
                    "match_point_label_to_vertex",
                ]
            },
            "review": {"check_methods": ["intersection_consistency_check"]},
        },
    },
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {"type": "vertex_label", "description": "각의 꼭짓점에 해당하는 점"},
        "value": "ㄹ",
        "unit": "",
    },
}

SOLVABLE = {
    "schema": "modu.solvable.v1.1",
    "problem_id": "S3_초등_3_008982",
    "problem_type": "geometry_vertex_selection",
    "inputs": {
        "total_ticks": 1,
        "target_label": "꼭짓점",
        "target_ticks": 1,
        "target_count": 1,
        "unit": "",
    },
    "given": [
        {"ref": "obj.angle", "value": "각"},
        {"ref": "obj.point.d", "value": "ㄷ"},
        {"ref": "obj.point.r", "value": "ㄹ"},
        {"ref": "obj.point.m", "value": "ㅁ"},
    ],
    "target": {"ref": "answer.target", "type": "vertex_label"},
    "method": "vertex_identification",
    "plan": ["두 반직선이 만나는 점을 찾는다.", "그 점에 붙은 보기의 글자를 고른다."],
    "steps": [{"id": "step.1", "expr": "두 반직선이 만나는 점 확인", "value": "ㄹ"}],
    "checks": [
        {
            "id": "check.1",
            "expr": "만나는 점이 각의 꼭짓점인지 확인",
            "expected": "ㄹ",
            "actual": "ㄹ",
            "pass": True,
        }
    ],
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {"type": "vertex_label", "description": "각의 꼭짓점에 해당하는 점"},
        "value": "ㄹ",
        "unit": "",
    },
}
