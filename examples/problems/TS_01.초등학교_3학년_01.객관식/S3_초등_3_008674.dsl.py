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
                slot_ids=("slot.header.text",),
            ),
            Region(
                id="region.options.top",
                role="diagram",
                flow="absolute",
                slot_ids=("slot.top.square", "slot.top.center"),
            ),
            Region(
                id="region.options.middle",
                role="diagram",
                flow="absolute",
                slot_ids=("slot.mid.left.square",
                    "slot.mid.left.red",
                    "slot.mid.left.center",
                    "slot.mid.mid.square",
                    "slot.mid.mid.arc",
                    "slot.mid.mid.red",
                    "slot.mid.mid.center",
                    "slot.mid.right.square",
                    "slot.mid.right.arc",
                    "slot.mid.right.red",
                    "slot.mid.right.center",'slot.mid.mid.arc.copy4', 'slot.mid.right.arc.copy1', 'slot.mid.right.arc.copy2'),
            ),
            Region(
                id="region.answer",
                role="diagram",
                flow="absolute",
                slot_ids=(
                    
                    
                ),
            ),
            Region(id="region.explanation", role="stem", flow="absolute", slot_ids=()),
        ),
        slots=(TextSlot(
                id="slot.header.text",
                prompt="",
                text = '원을 바르게 완성한 것을 선택하세요.', style_role="question",
                x = 50, y = 55, font_size = 30),
            RectSlot(
                id="slot.top.square",
                prompt="",
                x = 330, y = 120, width = 160, height = 160, fill = '#ffffff', stroke = '#111111', stroke_width = 1.5),
            CircleSlot(
                id="slot.top.center",
                prompt="",
                cx = 410, cy = 200, r = 5, fill = '#e91e63', stroke = '#111111', stroke_width = 2),
            RectSlot(
                id="slot.mid.left.square",
                prompt="",
                x = 90, y = 325, width = 160, height = 160, fill = '#ffffff', stroke = '#111111', stroke_width = 1.5),
            PathSlot(
                id="slot.mid.left.red",
                prompt="",
                d = 'M 158.87208557128906 318.676513671875 A 80 80 0 0 0 238.87208557128906 398.676513671875', stroke = '#111111', stroke_width = 2, transform = 'rotate(-15 198.87 358.67)'),
            CircleSlot(
                id="slot.mid.left.center",
                prompt="",
                cx = 170, cy = 410, r = 5, fill = '#e91e63', stroke = '#111111', stroke_width = 2),
            RectSlot(
                id="slot.mid.mid.square",
                prompt="",
                x = 320, y = 325, width = 160, height = 160, fill = '#ffffff', stroke = '#111111', stroke_width = 1.5),
            PathSlot(
                id="slot.mid.mid.arc",
                prompt="",
                d = 'M 572.6286888122559 291.1735076904297 A 80 80 0 1 1 652.6286888122559 211.1735076904297', stroke = '#111111', stroke_width = 2, transform = 'rotate(255 446.14 462.67)'),
            LineSlot(
                id="slot.mid.mid.red", prompt="", x1 = 385, y1 = 325, x2 = 480, y2 = 395, stroke = '#111111', stroke_width = 2),
            CircleSlot(
                id="slot.mid.mid.center",
                prompt="",
                cx = 400, cy = 410, r = 5, fill = '#e91e63', stroke = '#111111', stroke_width = 2),
            RectSlot(
                id="slot.mid.right.square",
                prompt="",
                x = 565, y = 325, width = 160, height = 160, fill = '#ffffff', stroke = '#111111', stroke_width = 1.5),
            PathSlot(
                id="slot.mid.right.arc",
                prompt="",
                d = 'M 552.7106018066406 169.6031494140625 A 80 80 0 1 1 632.7106018066406 89.6031494140625', stroke = '#111111', stroke_width = 2, transform = 'rotate(260 527.16 204.4)'),
            PathSlot(
                id="slot.mid.right.red",
                prompt="",
                d = 'M 633.7328491210938 193.20587158203125 A 85 65 0 0 1 718.7328491210938 268.20587158203125', stroke = '#111111', stroke_width = 2),
            CircleSlot(
                id="slot.mid.right.center",
                prompt="",
                cx = 645, cy = 405, r = 5, fill = '#e91e63', stroke = '#111111', stroke_width = 2),PathSlot(id = 'slot.mid.mid.arc.copy4', prompt = '', d = 'M 470 366 A 140 140 60 61 61 550 286', stroke = '#111111', stroke_width = 2, transform = 'rotate(255 410 226)'), PathSlot(id = 'slot.mid.right.arc.copy1', prompt = '', d = 'M 593.1247253417969 530.2952117919922 A 80 80 0 1 1 673.1247253417969 450.2952117919922', stroke = '#111111', stroke_width = 2, transform = 'rotate(260 477.77 509.56)'), PathSlot(id = 'slot.mid.right.arc.copy2', prompt = '', d = 'M 581.9780883789062 209.81005859375 A 80 80 0 1 1 661.9780883789062 129.81005859375', stroke = '#111111', stroke_width = 2, transform = 'rotate(260 727.9 241.23)')),
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
