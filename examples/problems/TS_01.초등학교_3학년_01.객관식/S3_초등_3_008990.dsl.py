from __future__ import annotations
from modu_math.dsl import (
    Canvas,
    CircleSlot,
    LineSlot,
    PolygonSlot,
    ProblemTemplate,
    RectSlot,
    Region,
    TextSlot,
)


def build_problem_template() -> ProblemTemplate:
    return ProblemTemplate(
        id="S3_초등_3_008990",
        title="직사각형 판별",
        canvas=Canvas(width=688, height=328, coordinate_mode="logical"),
        regions=(
            Region(
                id="region.stem",
                role="stem",
                flow="absolute",
                slot_ids=("slot.q1", "slot.shape.top", "slot.mark.left", "slot.mark.right"),
            ),
            Region(id="region.answer", role="answer", flow="absolute", slot_ids=()),
            Region(
                id="region.explanation",
                role="explanation",
                flow="absolute",
                slot_ids=("slot.shape.bottom", "slot.rt.mark1", "slot.rt.mark2"),
            ),
        ),
        slots=(
            TextSlot(
                id="slot.q1",
                prompt="",
                text="28.  직사각형이면 ○, 직사각형이 아니면 ×를 선택하세요.",
                style_role="question",
                x=12.0,
                y=28.0,
                font_size=28,
            ),
            PolygonSlot(
                id="slot.shape.top",
                prompt="",
                points=((383.0, 39.0), (483.0, 39.0), (483.0, 112.0), (383.0, 79.0)),
            ),
            CircleSlot(id="slot.mark.left", prompt="", cx=28.0, cy=124.0, r=7.0, fill="#FFFFFF"),
            TextSlot(
                id="slot.mark.left.text",
                prompt="",
                text="○",
                style_role="label",
                x=20.0,
                y=130.0,
                font_size=24,
            ),
            CircleSlot(id="slot.mark.right", prompt="", cx=427.0, cy=125.0, r=7.0, fill="#FFFFFF"),
            TextSlot(
                id="slot.mark.right.text",
                prompt="",
                text="×",
                style_role="label",
                x=419.0,
                y=131.0,
                font_size=24,
            ),
            RectSlot(id="slot.shape.bottom", prompt="", x=52.0, y=196.0, width=95.0, height=48.0),
            LineSlot(id="slot.rt.mark1", prompt="", x1=57.0, y1=201.0, x2=57.0, y2=210.0),
            LineSlot(id="slot.rt.mark2", prompt="", x1=57.0, y1=201.0, x2=66.0, y2=201.0),
        ),
        diagrams=(),
        groups=(),
        constraints=(),
        tags=(),
    )


PROBLEM_TEMPLATE = build_problem_template()

SEMANTIC_OVERRIDE = {
    "problem_id": "S3_초등_3_008990",
    "problem_type": "도형_판별",
    "metadata": {
        "language": "ko",
        "question": "직사각형인지 아닌지 판별하여 ○ 또는 ×를 선택하는 문제",
        "instruction": "직사각형이면 ○, 직사각형이 아니면 ×를 선택하세요.",
    },
    "domain": {
        "objects": [
            {"id": "obj.shape.target", "type": "quadrilateral"},
            {"id": "obj.choice.circle", "type": "choice_marker", "symbol": "○"},
            {"id": "obj.choice.cross", "type": "choice_marker", "symbol": "×"},
        ],
        "relations": [],
        "problem_solving": {
            "understand": {
                "given_refs": ["obj.shape.target"],
                "target_ref": "answer.target",
                "condition_refs": ["rel.definition"],
            },
            "plan": {
                "method": "정의_판별",
                "description": "도형의 네 각이 모두 직각인지 확인하여 직사각형 여부를 판단한다.",
            },
            "execute": {
                "expected_operations": [
                    "각의 직각 여부 확인",
                    "직사각형/비직사각형 판정",
                    "선택 기호 대응",
                ]
            },
            "review": {"check_methods": ["정의와 판정 결과 일치 여부 확인"]},
        },
    },
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {"type": "choice_symbol", "description": "직사각형이 아니면 선택하는 기호"},
        "value": 0,
        "unit": "",
    },
}

SOLVABLE = {
    "schema": "modu.solvable.v1.1",
    "problem_id": "S3_초등_3_008990",
    "problem_type": "도형_판별",
    "inputs": {
        "total_ticks": 0,
        "target_label": "직사각형 여부에 대한 선택 기호",
        "target_ticks": 0,
        "target_count": 1,
        "unit": "",
    },
    "given": [{"ref": "obj.shape.target", "value": {"type": "quadrilateral"}}],
    "target": {"ref": "answer.target", "type": "choice_symbol"},
    "method": "정의_판별",
    "plan": ["도형의 성질을 보고 직사각형인지 판단한다.", "직사각형이 아니면 ×를 고른다."],
    "steps": [
        {"id": "step.1", "expr": "도형의 네 각이 모두 직각인지 확인", "value": "확인 필요"},
        {"id": "step.2", "expr": "직사각형 여부에 따라 선택 기호 결정", "value": "×"},
    ],
    "checks": [
        {
            "id": "check.1",
            "expr": "정의: 네 각이 모두 직각인 사각형인가?",
            "expected": False,
            "actual": False,
            "pass": True,
        }
    ],
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {"type": "choice_symbol", "description": "직사각형이 아니면 선택하는 기호"},
        "value": 0,
        "unit": "",
    },
}
