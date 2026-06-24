from __future__ import annotations
from modu_math.dsl import Canvas, CircleSlot, LineSlot, ProblemTemplate, Region, TextSlot


def build_problem_template() -> ProblemTemplate:
    return ProblemTemplate(
        id="S3_초등_3_008984",
        title="선분을 선택하세요.",
        canvas=Canvas(width=788, height=170, coordinate_mode="logical"),
        regions=(
            Region(id="region.stem", role="stem", flow="absolute", slot_ids=("slot.q1",)),
            Region(
                id="region.choices",
                role="diagram",
                flow="absolute",
                slot_ids=(
                    "slot.choice1.line",
                    "slot.choice1.p1",
                    "slot.choice1.p2",
                    "slot.choice2.line",
                    "slot.choice2.p1",
                    "slot.choice2.p2",
                    "slot.choice3.line",
                    "slot.choice3.p1",
                    "slot.choice3.p2",
                    "slot.choice4.line",
                    "slot.choice4.p1",
                    "slot.choice4.p2",
                ),
            ),
            Region(
                id="region.answer", role="answer", flow="absolute", slot_ids=("slot.answer.line",)
            ),
            Region(id="region.explanation", role="explanation", flow="absolute", slot_ids=()),
        ),
        slots=(
            TextSlot(
                id="slot.q1",
                prompt="",
                text="□ 21. 선분을 선택하세요.",
                style_role="question",
                x=14.0,
                y=20.0,
                font_size=28,
            ),
            LineSlot(id="slot.choice1.line", prompt="", x1=116.0, y1=49.0, x2=210.0, y2=49.0),
            CircleSlot(id="slot.choice1.p1", prompt="", cx=115.0, cy=49.0, r=3.0, fill="#222222"),
            CircleSlot(id="slot.choice1.p2", prompt="", cx=210.0, cy=49.0, r=3.0, fill="#222222"),
            LineSlot(id="slot.choice2.line", prompt="", x1=300.0, y1=51.0, x2=399.0, y2=51.0),
            CircleSlot(id="slot.choice2.p1", prompt="", cx=300.0, cy=51.0, r=3.0, fill="#222222"),
            CircleSlot(id="slot.choice2.p2", prompt="", cx=399.0, cy=51.0, r=3.0, fill="#222222"),
            LineSlot(id="slot.choice3.line", prompt="", x1=492.0, y1=42.0, x2=597.0, y2=61.0),
            CircleSlot(id="slot.choice3.p1", prompt="", cx=492.0, cy=42.0, r=3.0, fill="#222222"),
            CircleSlot(id="slot.choice3.p2", prompt="", cx=597.0, cy=61.0, r=3.0, fill="#222222"),
            LineSlot(id="slot.choice4.line", prompt="", x1=679.0, y1=51.0, x2=773.0, y2=51.0),
            CircleSlot(id="slot.choice4.p1", prompt="", cx=679.0, cy=51.0, r=3.0, fill="#222222"),
            CircleSlot(id="slot.choice4.p2", prompt="", cx=773.0, cy=51.0, r=3.0, fill="#222222"),
            LineSlot(id="slot.answer.line", prompt="", x1=58.0, y1=100.0, x2=128.0, y2=100.0),
        ),
        diagrams=(),
        groups=(),
        constraints=(),
        tags=(),
    )


PROBLEM_TEMPLATE = build_problem_template()

SEMANTIC_OVERRIDE = {
    "problem_id": "S3_초등_3_008984",
    "problem_type": "객관식_선분_선택",
    "metadata": {
        "language": "ko",
        "question": "선분을 선택하세요.",
        "instruction": "그림 중에서 선분을 고르는 문제이다.",
    },
    "domain": {
        "objects": [
            {"id": "obj.choice1", "type": "line_shape", "property": "곡선"},
            {"id": "obj.choice2", "type": "line_shape", "property": "직선_양끝점"},
            {"id": "obj.choice3", "type": "line_shape", "property": "직선_양끝점"},
            {"id": "obj.choice4", "type": "line_shape", "property": "직선_양끝점"},
        ],
        "relations": [],
        "problem_solving": {
            "understand": {
                "given_refs": ["obj.choice1", "obj.choice2", "obj.choice3", "obj.choice4"],
                "target_ref": "answer.target",
                "condition_refs": ["rel.select_segment"],
            },
            "plan": {
                "method": "definition_match",
                "description": "선분의 정의에 맞는 그림을 찾는다.",
            },
            "execute": {
                "expected_operations": ["compare_shape_types", "match_with_segment_definition"]
            },
            "review": {"check_methods": ["definition_consistency_check"]},
        },
    },
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {"type": "selected_shape", "description": "선분"},
        "value": 0,
        "unit": "",
    },
}

SOLVABLE = {
    "schema": "modu.solvable.v1.1",
    "problem_id": "S3_초등_3_008984",
    "problem_type": "객관식_선분_선택",
    "inputs": {
        "total_ticks": 4,
        "target_label": "선분",
        "target_ticks": 1,
        "target_count": 1,
        "unit": "",
    },
    "given": [
        {"ref": "obj.choice1", "value": {"type": "곡선"}},
        {"ref": "obj.choice2", "value": {"type": "직선_양끝점"}},
        {"ref": "obj.choice3", "value": {"type": "직선_양끝점"}},
        {"ref": "obj.choice4", "value": {"type": "직선_양끝점"}},
    ],
    "target": {"ref": "answer.target", "type": "selected_shape"},
    "method": "definition_match",
    "plan": [
        "그림들의 모양을 보고 선분의 정의와 맞는지 확인한다.",
        "두 점을 곧게 이은 직선 모양을 찾는다.",
    ],
    "steps": [
        {"id": "step.1", "expr": "choice1은 곡선이므로 선분이 아님", "value": 0},
        {"id": "step.2", "expr": "choice2, choice3, choice4는 곧은 선으로 보임", "value": 0},
        {"id": "step.3", "expr": "정답은 선분의 정의에 맞는 그림", "value": 0},
    ],
    "checks": [
        {
            "id": "check.1",
            "expr": "선분은 두 점을 곧게 이은 선이다",
            "expected": True,
            "actual": True,
            "pass": True,
        }
    ],
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {"type": "selected_shape", "description": "선분"},
        "value": 0,
        "unit": "",
    },
}
