from __future__ import annotations
from modu_math.dsl import Canvas, ProblemTemplate, Region, TextSlot, RectSlot


def build_problem_template() -> ProblemTemplate:
    return ProblemTemplate(
        id="S3_초등_3_008763",
        title="저울 비교",
        canvas=Canvas(width=940, height=399, coordinate_mode="logical"),
        regions=(
            Region(
                id="region.stem",
                role="stem",
                flow="absolute",
                slot_ids=("slot.q1", "slot.q2", "slot.q3"),
            ),
            Region(id="region.answer", role="answer", flow="absolute", slot_ids=()),
        ),
        slots=(
            TextSlot(
                id="slot.q1",
                prompt="",
                text="65. 저울을 사용하여 물건의 무게를 비교하려고 합니다. 더 가벼운 것을 선택하세요.",
                style_role="question",
                x=16.0,
                y=26.0,
                font_size=28,
            ),
            RectSlot(
                id="slot.label.potato",
                prompt="",
                x=377.0,
                y=89.0,
                width=54.0,
                height=29.0,
                fill="#F8E7B6",
                stroke="#D6C18A",
                stroke_width=1.0,
            ),
            RectSlot(
                id="slot.label.sweetpotato",
                prompt="",
                x=483.0,
                y=89.0,
                width=72.0,
                height=29.0,
                fill="#F8E7B6",
                stroke="#D6C18A",
                stroke_width=1.0,
            ),
            TextSlot(
                id="slot.q2",
                prompt="",
                text="감자",
                style_role="label",
                x=390.0,
                y=109.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.q3",
                prompt="",
                text="고구마",
                style_role="label",
                x=494.0,
                y=109.0,
                font_size=28,
            ),
        ),
        diagrams=(),
        groups=(),
        constraints=(),
        tags=(),
    )


PROBLEM_TEMPLATE = build_problem_template()

SEMANTIC_OVERRIDE = {
    "problem_id": "S3_초등_3_008763",
    "problem_type": "weight_comparison",
    "metadata": {
        "language": "ko",
        "question": "저울을 사용하여 물건의 무게를 비교하는 문제",
        "instruction": "더 가벼운 것을 선택하세요.",
    },
    "domain": {
        "objects": [
            {"id": "obj.potato", "type": "food", "name": "감자"},
            {"id": "obj.sweet_potato", "type": "food", "name": "고구마"},
            {"id": "obj.balance", "type": "balance_scale"},
        ],
        "relations": [],
        "problem_solving": {
            "understand": {
                "given_refs": ["obj.potato", "obj.sweet_potato", "obj.balance"],
                "target_ref": "answer.target",
                "condition_refs": ["rel.compare_weight"],
            },
            "plan": {
                "method": "visual_balance_comparison",
                "description": "저울에서 위로 올라간 쪽이 더 가벼운지 판단한다.",
            },
            "execute": {
                "expected_operations": [
                    "observe_balance_tilt",
                    "identify_higher_pan",
                    "select_lighter_object",
                ]
            },
            "review": {"check_methods": ["match_answer_with_visual_evidence"]},
        },
    },
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {"type": "lighter_object", "description": "더 가벼운 것"},
        "value": "고구마",
        "unit": "",
    },
}

SOLVABLE = {
    "schema": "modu.solvable.v1.1",
    "problem_id": "S3_초등_3_008763",
    "problem_type": "weight_comparison",
    "inputs": {
        "total_ticks": 0,
        "target_label": "더 가벼운 것",
        "target_ticks": 0,
        "target_count": 1,
        "unit": "",
    },
    "given": [
        {"ref": "obj.potato", "value": "감자"},
        {"ref": "obj.sweet_potato", "value": "고구마"},
        {"ref": "obj.balance", "value": "저울"},
    ],
    "target": {"ref": "answer.target", "type": "lighter_object"},
    "method": "visual_balance_comparison",
    "plan": [
        "저울의 기울어진 방향을 확인한다.",
        "위로 올라간 접시에 놓인 물건이 더 가벼운지 판단한다.",
        "더 가벼운 물건을 선택한다.",
    ],
    "steps": [
        {"id": "step.1", "expr": "고구마가 놓인 접시가 위로 올라가 보인다.", "value": "고구마"},
        {"id": "step.2", "expr": "위로 올라간 쪽은 더 가볍다.", "value": "고구마"},
    ],
    "checks": [
        {
            "id": "check.1",
            "expr": "정답이 그림의 시각적 비교와 일치하는가",
            "expected": "고구마",
            "actual": "고구마",
            "pass": True,
        }
    ],
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {"type": "lighter_object", "description": "더 가벼운 것"},
        "value": "고구마",
        "unit": "",
    },
}
