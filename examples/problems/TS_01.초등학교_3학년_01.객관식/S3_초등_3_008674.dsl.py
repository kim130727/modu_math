from __future__ import annotations
from modu_math.dsl import (
    Canvas,
    ProblemTemplate,
    Region,
    TextSlot,
    RectSlot,
    CircleSlot,
    LineSlot,
    PathSlot,
)


def build_problem_template() -> ProblemTemplate:
    return ProblemTemplate(
        id="S3_초등_3_008674",
        title="원을 바르게 완성한 것을 선택하세요",
        canvas=Canvas(width=926.0, height=658.0, coordinate_mode="logical"),
        regions=(
            Region(
                id="region.header",
                role="stem",
                flow="absolute",
                slot_ids=("slot.header.mark", "slot.header.text"),
            ),
            Region(
                id="region.options.top",
                role="diagram",
                flow="absolute",
                slot_ids=("slot.top.square", "slot.top.arc", "slot.top.center"),
            ),
            Region(
                id="region.options.middle",
                role="diagram",
                flow="absolute",
                slot_ids=(
                    "slot.mid.left.square",
                    "slot.mid.left.arc",
                    "slot.mid.left.red",
                    "slot.mid.left.center",
                    "slot.mid.mid.square",
                    "slot.mid.mid.arc",
                    "slot.mid.mid.red",
                    "slot.mid.mid.center",
                    "slot.mid.right.square",
                    "slot.mid.right.arc",
                    "slot.mid.right.red",
                    "slot.mid.right.center",
                ),
            ),
            Region(
                id="region.answer",
                role="diagram",
                flow="absolute",
                slot_ids=(
                    "slot.answer.square",
                    "slot.answer.arc",
                    "slot.answer.center",
                ),
            ),
            Region(id="region.explanation", role="stem", flow="absolute", slot_ids=()),
        ),
        slots=(
            TextSlot(
                id="slot.header.mark",
                prompt="",
                text="☐ 55.",
                style_role="question",
                x=10.0,
                y=32.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.header.text",
                prompt="",
                text="원을 바르게 완성한 것을 선택하세요.",
                style_role="question",
                x=70.0,
                y=32.0,
                font_size=28,
            ),
            RectSlot(
                id="slot.top.square",
                prompt="",
                x=410.0,
                y=48.0,
                width=160.0,
                height=160.0,
            ),
            PathSlot(
                id="slot.top.arc",
                prompt="",
                d="M 490.0 48.0 A 80.0 80.0 0 1 0 570.0 128.0",
            ),
            CircleSlot(
                id="slot.top.center",
                prompt="",
                cx=490.0,
                cy=128.0,
                r=4.0,
                fill="#e91e63",
            ),
            RectSlot(
                id="slot.mid.left.square",
                prompt="",
                x=140.0,
                y=226.0,
                width=160.0,
                height=160.0,
            ),
            PathSlot(
                id="slot.mid.left.arc",
                prompt="",
                d="M 140.0 306.0 A 80.0 80.0 0 1 1 220.0 226.0",
            ),
            PathSlot(
                id="slot.mid.left.red",
                prompt="",
                d="M 220.0 226.0 A 80.0 80.0 0 0 0 300.0 306.0",
            ),
            CircleSlot(
                id="slot.mid.left.center",
                prompt="",
                cx=220.0,
                cy=306.0,
                r=4.0,
                fill="#e91e63",
            ),
            RectSlot(
                id="slot.mid.mid.square",
                prompt="",
                x=410.0,
                y=226.0,
                width=160.0,
                height=160.0,
            ),
            PathSlot(
                id="slot.mid.mid.arc",
                prompt="",
                d="M 410.0 306.0 A 80.0 80.0 0 1 1 490.0 226.0",
            ),
            LineSlot(
                id="slot.mid.mid.red", prompt="", x1=490.0, y1=226.0, x2=570.0, y2=306.0
            ),
            CircleSlot(
                id="slot.mid.mid.center",
                prompt="",
                cx=490.0,
                cy=306.0,
                r=4.0,
                fill="#e91e63",
            ),
            RectSlot(
                id="slot.mid.right.square",
                prompt="",
                x=700.0,
                y=226.0,
                width=160.0,
                height=160.0,
            ),
            PathSlot(
                id="slot.mid.right.arc",
                prompt="",
                d="M 700.0 306.0 A 80.0 80.0 0 1 1 780.0 226.0",
            ),
            PathSlot(
                id="slot.mid.right.red",
                prompt="",
                d="M 780.0 226.0 A 80.0 80.0 0 0 1 860.0 306.0",
            ),
            CircleSlot(
                id="slot.mid.right.center",
                prompt="",
                cx=780.0,
                cy=306.0,
                r=4.0,
                fill="#e91e63",
            ),
            RectSlot(
                id="slot.answer.square",
                prompt="",
                x=60.0,
                y=412.0,
                width=160.0,
                height=160.0,
            ),
            PathSlot(
                id="slot.answer.arc",
                prompt="",
                d="M 60.0 492.0 A 80.0 80.0 0 1 1 140.0 412.0",
            ),
            CircleSlot(
                id="slot.answer.center",
                prompt="",
                cx=140.0,
                cy=492.0,
                r=4.0,
                fill="#e91e63",
            ),
        ),
        diagrams=(),
        groups=(),
        constraints=(),
        tags=(),
    )


PROBLEM_TEMPLATE = build_problem_template()

SEMANTIC_OVERRIDE = {
    "problem_id": "S3_초등_3_008674",
    "problem_type": "도형_선택",
    "metadata": {
        "language": "ko",
        "question": "원을 바르게 완성한 것을 선택하세요.",
        "instruction": "정답을 고르는 도형 문제",
    },
    "domain": {
        "objects": [
            {
                "id": "obj.circle_completion",
                "type": "circle_completion_task",
                "description": "원호가 이어져 원이 완성되는 그림을 고르는 문제",
            }
        ],
        "relations": [],
        "problem_solving": {
            "understand": {
                "given_refs": ["obj.circle_completion"],
                "target_ref": "answer.target",
                "condition_refs": ["rel.compare_options"],
            },
            "plan": {
                "method": "visual_comparison",
                "description": "각 그림에서 원호가 자연스럽게 이어져 원이 완성되는지 비교한다.",
            },
            "execute": {
                "expected_operations": ["compare_shapes", "identify_completed_circle"]
            },
            "review": {
                "check_methods": ["completion_of_curve", "consistency_with_explanation"]
            },
        },
    },
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {
            "type": "selected_picture",
            "description": "원을 바르게 완성한 그림",
        },
        "value": 0,
        "unit": "",
    },
}

SOLVABLE = {
    "schema": "modu.solvable.v1.1",
    "problem_id": "S3_초등_3_008674",
    "problem_type": "도형_선택",
    "inputs": {
        "total_ticks": 0,
        "target_label": "원을 바르게 완성한 그림",
        "target_ticks": 0,
        "target_count": 1,
        "unit": "",
    },
    "given": [{"ref": "obj.circle_completion", "value": "여러 개의 원호 그림"}],
    "target": {"ref": "answer.target", "type": "selected_picture"},
    "method": "visual_comparison",
    "plan": [
        "각 그림의 원호가 끊기지 않고 자연스럽게 이어지는지 확인한다.",
        "원으로 완성된 모양인지 비교한다.",
    ],
    "steps": [
        {
            "id": "step.1",
            "expr": "그림들에서 원호의 연결 상태를 비교한다.",
            "value": "비교 수행",
        },
        {
            "id": "step.2",
            "expr": "원이 바르게 완성된 그림을 고른다.",
            "value": "정답 선택 필요",
        },
    ],
    "checks": [
        {
            "id": "check.1",
            "expr": "선택한 그림이 원의 시작점과 끝점이 자연스럽게 만나도록 완성되었는지 확인한다.",
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
            "type": "selected_picture",
            "description": "원을 바르게 완성한 그림",
        },
        "value": 0,
        "unit": "",
    },
}
