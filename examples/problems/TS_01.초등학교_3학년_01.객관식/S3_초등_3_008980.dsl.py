from __future__ import annotations
from modu_math.dsl import Canvas, ProblemTemplate, Region, TextSlot, LineSlot, CircleSlot


def build_problem_template() -> ProblemTemplate:
    return ProblemTemplate(
        id="S3_초등_3_008980",
        title="직각 판별",
        canvas=Canvas(width=850.0, height=426.0, coordinate_mode="logical"),
        regions=(
            Region(
                id="region.stem",
                role="stem",
                flow="absolute",
                slot_ids=("slot.q1", "slot.choice.o1", "slot.choice.x1", "slot.answer.circle"),
            ),
            Region(
                id="region.diagram.top",
                role="diagram",
                flow="absolute",
                slot_ids=("slot.diagram.top.v", "slot.diagram.top.h"),
            ),
            Region(
                id="region.explanation",
                role="explanation",
                flow="absolute",
                slot_ids=("slot.diagram.bottom.v", "slot.diagram.bottom.h"),
            ),
        ),
        slots=(
            TextSlot(
                id="slot.q1",
                prompt="",
                text="15.  직각이면 ○, 직각이 아니면 ×를 선택하세요.",
                style_role="question",
                x=12.0,
                y=16.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.choice.o1",
                prompt="",
                text="○",
                style_role="auxiliary",
                x=24.0,
                y=138.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.choice.x1",
                prompt="",
                text="×",
                style_role="auxiliary",
                x=442.0,
                y=140.0,
                font_size=28,
            ),
            CircleSlot(
                id="slot.answer.circle", prompt="", cx=78.0, cy=182.0, r=10.0, fill="#FFFFFF"
            ),
            LineSlot(
                id="slot.diagram.top.v",
                prompt="",
                x1=360.0,
                y1=38.0,
                x2=360.0,
                y2=119.0,
                stroke="#7A7A7A",
                stroke_width=1.4,
            ),
            LineSlot(
                id="slot.diagram.top.h",
                prompt="",
                x1=360.0,
                y1=38.0,
                x2=484.0,
                y2=38.0,
                stroke="#7A7A7A",
                stroke_width=1.4,
            ),
            LineSlot(
                id="slot.diagram.bottom.v",
                prompt="",
                x1=34.0,
                y1=309.0,
                x2=34.0,
                y2=400.0,
                stroke="#7A7A7A",
                stroke_width=1.4,
            ),
            LineSlot(
                id="slot.diagram.bottom.h",
                prompt="",
                x1=34.0,
                y1=309.0,
                x2=129.0,
                y2=309.0,
                stroke="#7A7A7A",
                stroke_width=1.4,
            ),
        ),
        diagrams=(),
        groups=(),
        constraints=(),
        tags=(),
    )


PROBLEM_TEMPLATE = build_problem_template()

SEMANTIC_OVERRIDE = {
    "problem_id": "S3_초등_3_008980",
    "problem_type": "직각 판별",
    "metadata": {
        "language": "ko",
        "question": "직각이면 ○, 직각이 아니면 ×를 선택하는 문제",
        "instruction": "도형이 직각인지 판단하여 선택한다.",
    },
    "domain": {
        "objects": [
            {"id": "obj.figure.top", "type": "angle_figure"},
            {"id": "obj.figure.bottom", "type": "angle_figure"},
            {"id": "obj.choice.o", "type": "symbol", "symbol": "○"},
            {"id": "obj.choice.x", "type": "symbol", "symbol": "×"},
        ],
        "relations": [],
        "problem_solving": {
            "understand": {
                "given_refs": ["obj.figure.top", "obj.figure.bottom"],
                "target_ref": "answer.target",
                "condition_refs": ["rel.classify.angle"],
            },
            "plan": {
                "method": "직각 판별",
                "description": "도형의 각이 직각인지 확인한 뒤 알맞은 기호를 고른다.",
            },
            "execute": {"expected_operations": ["check_right_angle", "select_symbol"]},
            "review": {"check_methods": ["definition_consistency_check"]},
        },
    },
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {"type": "selection", "description": "직각이면 ○, 직각이 아니면 ×"},
        "value": 0,
        "unit": "",
    },
}

SOLVABLE = {
    "schema": "modu.solvable.v1.1",
    "problem_id": "S3_초등_3_008980",
    "problem_type": "직각 판별",
    "inputs": {
        "total_ticks": 1,
        "target_label": "직각 여부",
        "target_ticks": 1,
        "target_count": 1,
        "unit": "",
    },
    "given": [
        {"ref": "obj.figure.top", "value": {"type": "angle_figure"}},
        {"ref": "obj.figure.bottom", "value": {"type": "angle_figure"}},
    ],
    "target": {"ref": "answer.target", "type": "selection"},
    "method": "직각 판별",
    "plan": ["도형의 각이 직각인지 확인한다.", "지시에 따라 ○ 또는 ×를 고른다."],
    "steps": [
        {"id": "step.1", "expr": "도형의 각이 직각인지 확인한다.", "value": None},
        {"id": "step.2", "expr": "판단 결과에 따라 ○ 또는 ×를 선택한다.", "value": None},
    ],
    "checks": [
        {
            "id": "check.1",
            "expr": "직각 여부에 따른 기호 선택이 문제 지시와 일치하는가",
            "expected": True,
            "actual": True,
            "pass": True,
        }
    ],
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {"type": "selection", "description": "직각이면 ○, 직각이 아니면 ×"},
        "value": 0,
        "unit": "",
    },
}
