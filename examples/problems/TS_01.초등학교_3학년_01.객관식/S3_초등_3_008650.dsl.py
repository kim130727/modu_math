from __future__ import annotations
from modu_math.dsl import (
    Canvas,
    CircleSlot,
    LineSlot,
    PathSlot,
    ProblemTemplate,
    RectSlot,
    Region,
    TextSlot,
)


def build_problem_template() -> ProblemTemplate:
    return ProblemTemplate(
        id="S3_초등_3_008650",
        title="지름과 반지름의 관계",
        canvas=Canvas(width=960, height=514, coordinate_mode="logical"),
        regions=(
            Region(
                id="region.header",
                role="stem",
                flow="absolute",
                slot_ids=("slot.q1", ),
            ),
            Region(
                id="region.diagram",
                role="diagram",
                flow="absolute",
                slot_ids=(
                    "slot.circle",
                    "slot.center",
                    "slot.diameter",
                    "slot.arc.right",
                    "slot.guide.diameter.curve",
                    "slot.guide.radius.curve",
                    "slot.len4",
                    "slot.len2",
                    
                ),
            ),
            Region(
                id="region.choice",
                role="stem",
                flow="absolute",
                slot_ids=("slot.choice.box", "slot.choice.text"),
            ),
            Region(id="region.footer", role="answer", flow="absolute", slot_ids=()),
        ),
        slots=(
            TextSlot(
                id="slot.q1",
                prompt="",
                text = '\n    \n    그림을 보고 지름과 반지름 사이의 관계를 알아보려고 합니다.\n    알맞은 것을 선택하세요.\n  ', style_role="question",
                x = 20, y = 15, font_size = 30),
            CircleSlot(
                id="slot.circle", prompt="", cx = 430, cy = 260, r = 120, fill="none"
            ),
            CircleSlot(
                id="slot.center", prompt="", cx = 433, cy = 260, r = 5, fill="#d81b60"
            ),
            LineSlot(
                id="slot.diameter", prompt="", x1 = 370, y1 = 360, x2 = 495, y2 = 160),
            LineSlot(
                id="slot.arc.right", prompt="", x1 = 430, y1 = 260, x2 = 550, y2 = 260),
            PathSlot(
                id="slot.guide.diameter.curve",
                prompt="",
                d = 'M 370 360 C 335 300 360 210 495 160', stroke="#37bdf8",
                stroke_width=1.6,
                stroke_dasharray="5 4",
                fill="none",
            ),
            PathSlot(
                id="slot.guide.radius.curve",
                prompt="",
                d="M 438 267 C 470 288, 517 287, 548 262",
                stroke="#37bdf8",
                stroke_width=1.6,
                stroke_dasharray="5 4",
                fill="none",
            ),
            TextSlot(
                id="slot.len4",
                prompt="",
                text = '4 cm', style_role="label",
                x = 345, y = 210, font_size = 25, fill = '#111111'),
            TextSlot(
                id="slot.len2",
                prompt="",
                text = '2 cm', style_role="label",
                x = 460, y = 310, font_size = 25, fill = '#111111'),
            RectSlot(
                id="slot.choice.box",
                prompt="",
                x = 30, y = 410, width = 795, height = 80, fill="none",
            ),
            TextSlot(
                id="slot.choice.text",
                prompt="",
                text = '한 원에서 ( 지름 , 반지름 )은 ( 지름 , 반지름 )의 2배입니다.', style_role="question",
                x = 65, y = 455, font_size = 30),
        ),
        diagrams=(),
        groups=(),
        constraints=(),
        tags=(),
    )


PROBLEM_TEMPLATE = build_problem_template()

SEMANTIC_OVERRIDE = {
    "problem_id": "S3_초등_3_008650",
    "problem_type": "circle_relationship_choice",
    "metadata": {
        "language": "ko",
        "question": "그림을 보고 지름과 반지름 사이의 관계를 알아보려고 합니다. 알맞은 것을 선택하세요.",
        "instruction": "알맞은 것을 선택하세요.",
    },
    "domain": {
        "objects": [
            {"id": "obj.circle", "type": "circle"},
            {"id": "obj.diameter", "type": "segment", "role": "지름"},
            {"id": "obj.radius", "type": "segment", "role": "반지름"},
        ],
        "relations": [],
        "problem_solving": {
            "understand": {
                "given_refs": ["obj.circle", "obj.diameter", "obj.radius"],
                "target_ref": "answer.target",
                "condition_refs": ["rel.diameter_radius"],
            },
            "plan": {
                "method": "개념_판별",
                "description": "그림과 설명을 보고 지름과 반지름의 관계를 선택한다.",
            },
            "execute": {"expected_operations": ["관계_확인", "보기_선택"]},
            "review": {"check_methods": ["설명문_일치확인"]},
        },
    },
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {
            "type": "choice",
            "description": "지름과 반지름의 관계를 나타내는 알맞은 것을 선택",
        },
        "value": "지름, 반지름",
        "unit": "",
    },
}

SOLVABLE = {
    "schema": "modu.solvable.v1.1",
    "problem_id": "S3_초등_3_008650",
    "problem_type": "circle_relationship_choice",
    "inputs": {
        "total_ticks": 0,
        "target_label": "지름과 반지름의 관계",
        "target_ticks": 0,
        "target_count": 0,
        "unit": "",
    },
    "given": [
        {"ref": "obj.circle", "value": {"type": "circle"}},
        {"ref": "obj.diameter", "value": {"role": "지름"}},
        {"ref": "obj.radius", "value": {"role": "반지름"}},
    ],
    "target": {"ref": "answer.target", "type": "choice"},
    "method": "개념_판별",
    "plan": [
        "그림과 해설 문장을 보고 지름과 반지름의 관계를 확인한다.",
        "보기에서 알맞은 말을 고른다.",
    ],
    "steps": [
        {
            "id": "step.1",
            "expr": "한 원에서 지름은 반지름의 2배이다.",
            "value": "지름, 반지름",
        }
    ],
    "checks": [
        {
            "id": "check.1",
            "expr": "해설 문장과 선택 결과가 일치하는가",
            "expected": "지름, 반지름",
            "actual": "지름, 반지름",
            "pass": True,
        }
    ],
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {
            "type": "choice",
            "description": "지름과 반지름의 관계를 나타내는 알맞은 것을 선택",
        },
        "value": "지름, 반지름",
        "unit": "",
    },
}
