from __future__ import annotations
from modu_math.dsl import (
    Canvas,
    ProblemTemplate,
    Region,
    RectSlot,
    TextSlot,
    CircleSlot,
    LineSlot,
    PathSlot,
)


def build_problem_template() -> ProblemTemplate:
    return ProblemTemplate(
        id="S3_초등_3_008851",
        title="저울을 사용하여 무거운 것 고르기",
        canvas=Canvas(width=952, height=378, coordinate_mode="logical"),
        regions=(
            Region(
                id="region.stem",
                role="stem",
                flow="absolute",
                slot_ids=(
                    "slot.q1",
                    "slot.q2",
                    "slot.scale.base",
                    "slot.scale.orange",
                ),
            ),
            Region(id="region.answer", role="answer", flow="absolute", slot_ids=()),
        ),
        slots=(
            TextSlot(
                id="slot.q1",
                prompt="",
                text="저울을 사용하여 오렌지와 바나나의 무게를 비교했습니다.",
                style_role="question",
                x=45.837,
                y=41.046,
                font_size=28,
                fill="#111111",
            ),
            TextSlot(
                id="slot.q2",
                prompt="",
                text="오렌지와 바나나 중 더 무거운 것을 선택해 보세요.",
                style_role="question",
                x=51.724,
                y=78.41,
                font_size=28,
                fill="#111111",
            ),
            TextSlot(
                id="slot.scale.base",
                prompt="",
                text="",
                style_role="diagram",
                x=0.0,
                y=0.0,
                font_size=28,
            ),
            CircleSlot(
                id="slot.scale.orange", prompt="", cx=420.0, cy=132.0, r=22.0, fill="#F28C28"
            ),
        ),
        diagrams=(),
        groups=(),
        constraints=(),
        tags=(),
    )


PROBLEM_TEMPLATE = build_problem_template()

SEMANTIC_OVERRIDE = {
    "problem_id": "S3_초등_3_008851",
    "problem_type": "comparison_weight",
    "metadata": {
        "language": "ko",
        "question": "저울을 사용하여 오렌지와 바나나의 무게를 비교했습니다. 오렌지와 바나나 중 더 무거운 것을 선택해 보세요.",
        "instruction": "더 무거운 것을 고르기",
    },
    "domain": {
        "objects": [
            {"id": "obj.orange", "type": "fruit", "name": "오렌지"},
            {"id": "obj.banana", "type": "fruit", "name": "바나나"},
            {"id": "obj.scale", "type": "balance_scale", "name": "저울"},
        ],
        "relations": [],
        "problem_solving": {
            "understand": {
                "given_refs": ["obj.orange", "obj.banana", "obj.scale"],
                "target_ref": "answer.target",
                "condition_refs": ["rel.compare_weight", "rel.left_side_down"],
            },
            "plan": {
                "method": "visual_comparison",
                "description": "저울의 기울어짐을 보고 더 무거운 대상을 고른다.",
            },
            "execute": {
                "expected_operations": [
                    "observe_balance_tilt",
                    "identify_heavier_side",
                    "select_heavier_object",
                ]
            },
            "review": {"check_methods": ["tilt_direction_consistency", "image_label_match"]},
        },
    },
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {"type": "heavier_object", "description": "오렌지와 바나나 중 더 무거운 것"},
        "value": "오렌지",
        "unit": "",
    },
}

SOLVABLE = {
    "schema": "modu.solvable.v1.1",
    "problem_id": "S3_초등_3_008851",
    "problem_type": "comparison_weight",
    "inputs": {
        "total_ticks": 0,
        "target_label": "더 무거운 것",
        "target_ticks": 0,
        "target_count": 1,
        "unit": "",
    },
    "given": [
        {"ref": "obj.orange", "value": {"name": "오렌지"}},
        {"ref": "obj.banana", "value": {"name": "바나나"}},
        {"ref": "rel.left_side_down", "value": {"meaning": "왼쪽 접시가 아래로 내려감"}},
    ],
    "target": {"ref": "answer.target", "type": "heavier_object"},
    "method": "visual_comparison",
    "plan": [
        "저울의 기울어진 방향을 확인한다.",
        "더 아래로 내려간 쪽의 물체가 더 무겁다고 판단한다.",
        "해당 물체를 답으로 고른다.",
    ],
    "steps": [
        {"id": "step.1", "expr": "저울의 왼쪽 접시가 더 아래에 보인다", "value": "left_side_down"},
        {"id": "step.2", "expr": "더 아래로 내려간 쪽의 물체를 선택한다", "value": "오렌지"},
    ],
    "checks": [
        {
            "id": "check.1",
            "expr": "선택한 대상이 저울이 더 내려간 쪽과 일치하는가",
            "expected": "오렌지",
            "actual": "오렌지",
            "pass": True,
        }
    ],
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {"type": "heavier_object", "description": "오렌지와 바나나 중 더 무거운 것"},
        "value": "오렌지",
        "unit": "",
    },
}
