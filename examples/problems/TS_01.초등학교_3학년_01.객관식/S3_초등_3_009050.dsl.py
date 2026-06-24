from __future__ import annotations
from modu_math.dsl import Canvas, ProblemTemplate, Region, TextSlot, CircleSlot, LineSlot


def build_problem_template() -> ProblemTemplate:
    return ProblemTemplate(
        id="S3_초등_3_009050",
        title="선분을 찾아 선택하세요",
        canvas=Canvas(width=728.0, height=262.0, coordinate_mode="logical"),
        regions=(
            Region(
                id="region.stem",
                role="stem",
                flow="absolute",
                slot_ids=(
                    "slot.q_num",
                    "slot.q_text",
                    "slot.shape.top_left.line",
                    "slot.shape.top_left.p1",
                    "slot.shape.top_left.p2",
                    "slot.shape.top_mid.curve",
                    "slot.shape.top_mid.p1",
                    "slot.shape.top_mid.p2",
                    "slot.shape.top_right.curve",
                    "slot.shape.top_right.p1",
                    "slot.shape.top_right.p2",
                ),
            ),
            Region(
                id="region.answer",
                role="answer",
                flow="absolute",
                slot_ids=("slot.shape.answer.line", "slot.shape.answer.p1", "slot.shape.answer.p2"),
            ),
            Region(id="region.explanation", role="explanation", flow="absolute", slot_ids=()),
        ),
        slots=(
            TextSlot(
                id="slot.q_num",
                prompt="",
                text="88.",
                style_role="question",
                x=13.0,
                y=19.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.q_text",
                prompt="",
                text="선분을 찾아 선택하세요.",
                style_role="question",
                x=64.0,
                y=19.0,
                font_size=28,
            ),
            LineSlot(
                id="slot.shape.top_left.line", prompt="", x1=169.0, y1=61.0, x2=231.0, y2=101.0
            ),
            CircleSlot(
                id="slot.shape.top_left.p1", prompt="", cx=169.0, cy=61.0, r=2.6, fill="#222222"
            ),
            CircleSlot(
                id="slot.shape.top_left.p2", prompt="", cx=231.0, cy=101.0, r=2.6, fill="#222222"
            ),
            LineSlot(
                id="slot.shape.top_mid.curve", prompt="", x1=372.0, y1=103.0, x2=502.0, y2=72.0
            ),
            CircleSlot(
                id="slot.shape.top_mid.p1", prompt="", cx=372.0, cy=103.0, r=2.6, fill="#222222"
            ),
            CircleSlot(
                id="slot.shape.top_mid.p2", prompt="", cx=502.0, cy=72.0, r=2.6, fill="#222222"
            ),
            LineSlot(
                id="slot.shape.top_right.curve", prompt="", x1=621.0, y1=57.0, x2=678.0, y2=117.0
            ),
            CircleSlot(
                id="slot.shape.top_right.p1", prompt="", cx=621.0, cy=57.0, r=2.6, fill="#222222"
            ),
            CircleSlot(
                id="slot.shape.top_right.p2", prompt="", cx=678.0, cy=117.0, r=2.6, fill="#222222"
            ),
            LineSlot(id="slot.shape.answer.line", prompt="", x1=49.0, y1=150.0, x2=149.0, y2=197.0),
            CircleSlot(
                id="slot.shape.answer.p1", prompt="", cx=49.0, cy=150.0, r=2.6, fill="#222222"
            ),
            CircleSlot(
                id="slot.shape.answer.p2", prompt="", cx=149.0, cy=197.0, r=2.6, fill="#222222"
            ),
        ),
        diagrams=(),
        groups=(),
        constraints=(),
        tags=("초등수학", "선분", "직선", "굽은선"),
    )


PROBLEM_TEMPLATE = build_problem_template()

SEMANTIC_OVERRIDE = {
    "problem_id": "S3_초등_3_009050",
    "problem_type": "shape_classification",
    "metadata": {
        "language": "ko",
        "question": "선분을 찾아 선택하세요.",
        "instruction": "여러 선 그림 중에서 선분을 찾는 문제",
    },
    "domain": {
        "objects": [
            {"id": "obj.line_1", "type": "line_figure", "kind": "straight"},
            {"id": "obj.line_2", "type": "line_figure", "kind": "curved"},
            {"id": "obj.line_3", "type": "line_figure", "kind": "curved"},
        ],
        "relations": [],
        "problem_solving": {
            "understand": {
                "given_refs": ["obj.line_1", "obj.line_2", "obj.line_3"],
                "target_ref": "answer.target",
                "condition_refs": ["rel.classify_1", "rel.classify_2", "rel.classify_3"],
            },
            "plan": {
                "method": "shape_classification",
                "description": "곧은 선인지 굽은 선인지 보고 선분을 찾는다.",
            },
            "execute": {
                "expected_operations": [
                    "compare_shape",
                    "identify_straight_line",
                    "exclude_curved_line",
                ]
            },
            "review": {"check_methods": ["shape_type_check", "curved_line_exclusion_check"]},
        },
    },
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {"type": "selected_line_segment", "description": "선분"},
        "value": 1,
        "unit": "",
    },
}

SOLVABLE = {
    "schema": "modu.solvable.v1.1",
    "problem_id": "S3_초등_3_009050",
    "problem_type": "shape_classification",
    "inputs": {
        "total_ticks": 3,
        "target_label": "선분",
        "target_ticks": 1,
        "target_count": 1,
        "unit": "",
    },
    "given": [
        {"ref": "obj.line_1", "value": {"kind": "straight"}},
        {"ref": "obj.line_2", "value": {"kind": "curved"}},
        {"ref": "obj.line_3", "value": {"kind": "curved"}},
    ],
    "target": {"ref": "answer.target", "type": "selected_line_segment"},
    "method": "shape_classification",
    "plan": [
        "그림의 모양이 곧은 선인지 굽은 선인지 구분한다.",
        "선분에 해당하는 곧은 선을 찾는다.",
    ],
    "steps": [
        {"id": "step.1", "expr": "obj.line_1.kind", "value": "straight"},
        {"id": "step.2", "expr": "obj.line_2.kind", "value": "curved"},
        {"id": "step.3", "expr": "obj.line_3.kind", "value": "curved"},
        {"id": "step.4", "expr": "선분으로 분류되는 그림의 수", "value": 1},
    ],
    "checks": [
        {
            "id": "check.1",
            "expr": "둘째와 셋째는 굽은 선인가?",
            "expected": True,
            "actual": True,
            "pass": True,
        }
    ],
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {"type": "selected_line_segment", "description": "선분"},
        "value": 1,
        "unit": "",
    },
}
