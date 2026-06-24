from __future__ import annotations
from modu_math.dsl import Canvas, ProblemTemplate, Region, TextSlot


def build_problem_template() -> ProblemTemplate:
    return ProblemTemplate(
        id="S3_초등_3_008809",
        title="무게가 1 kg보다 더 가벼운 것을 선택하세요",
        canvas=Canvas(width=936.0, height=396.0, coordinate_mode="logical"),
        regions=(
            Region(id="region.stem", role="stem", flow="absolute", slot_ids=("slot.q1", "slot.q2")),
            Region(
                id="region.options",
                role="diagram",
                flow="absolute",
                slot_ids=("slot.opt1", "slot.opt2", "slot.opt3"),
            ),
            Region(id="region.answer", role="support", flow="absolute", slot_ids=()),
            Region(id="region.explanation", role="support", flow="absolute", slot_ids=()),
        ),
        slots=(
            TextSlot(
                id="slot.q1",
                prompt="",
                text="40.",
                style_role="question",
                x=32.0,
                y=26.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.q2",
                prompt="",
                text="무게가 1 kg보다 더 가벼운 것을 선택하세요.",
                style_role="question",
                x=78.0,
                y=26.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.opt1",
                prompt="",
                text="전자레인지 그림 TODO",
                style_role="diagram",
                x=176.0,
                y=96.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.opt2",
                prompt="",
                text="호박 그림 TODO",
                style_role="diagram",
                x=470.0,
                y=96.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.opt3",
                prompt="",
                text="칫솔 그림 TODO",
                style_role="diagram",
                x=717.0,
                y=96.0,
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
    "problem_id": "S3_초등_3_008809",
    "problem_type": "comparison_selection",
    "metadata": {
        "language": "ko",
        "question": "무게가 1 kg보다 더 가벼운 것을 선택하세요.",
        "instruction": "주어진 보기에서 조건에 맞는 물건을 선택하는 문제",
    },
    "domain": {
        "objects": [
            {"id": "obj.ref_1kg", "type": "weight_reference", "label": "1 kg"},
            {"id": "obj.microwave", "type": "object", "label": "전자레인지"},
            {"id": "obj.pumpkin", "type": "object", "label": "호박"},
            {"id": "obj.toothbrush", "type": "object", "label": "칫솔"},
        ],
        "relations": [],
        "problem_solving": {
            "understand": {
                "given_refs": ["obj.ref_1kg", "obj.microwave", "obj.pumpkin", "obj.toothbrush"],
                "target_ref": "answer.target",
                "condition_refs": ["rel.toothbrush_lt_1kg"],
            },
            "plan": {
                "method": "compare_weight_to_reference",
                "description": "기준인 1 kg보다 더 가벼운 물건을 찾는다.",
            },
            "execute": {
                "expected_operations": [
                    "compare_each_object_with_reference",
                    "select_matching_object",
                ]
            },
            "review": {
                "check_methods": ["condition_satisfaction_check", "reference_comparison_check"]
            },
        },
    },
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {"type": "selected_object", "description": "1 kg보다 더 가벼운 것"},
        "value": "칫솔",
        "unit": "",
    },
}

SOLVABLE = {
    "schema": "modu.solvable.v1.1",
    "problem_id": "S3_초등_3_008809",
    "problem_type": "comparison_selection",
    "inputs": {
        "total_ticks": 1,
        "target_label": "1 kg보다 더 가벼운 것",
        "target_ticks": 1,
        "target_count": 1,
        "unit": "kg",
    },
    "given": [
        {"ref": "obj.ref_1kg", "value": {"label": "1 kg"}},
        {"ref": "obj.microwave", "value": {"label": "전자레인지"}},
        {"ref": "obj.pumpkin", "value": {"label": "호박"}},
        {"ref": "obj.toothbrush", "value": {"label": "칫솔"}},
    ],
    "target": {"ref": "answer.target", "type": "selected_object"},
    "method": "compare_weight_to_reference",
    "plan": ["각 보기의 무게가 1 kg보다 더 가벼운지 확인한다.", "조건을 만족하는 물건을 고른다."],
    "steps": [
        {"id": "step.1", "expr": "칫솔 < 1 kg", "value": True},
        {"id": "step.2", "expr": "전자레인지 > 1 kg", "value": True},
        {"id": "step.3", "expr": "호박 > 1 kg", "value": True},
        {"id": "step.4", "expr": "조건을 만족하는 보기 선택", "value": "칫솔"},
    ],
    "checks": [
        {
            "id": "check.1",
            "expr": "칫솔이 1 kg보다 더 가벼운가",
            "expected": True,
            "actual": True,
            "pass": True,
        }
    ],
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {"type": "selected_object", "description": "1 kg보다 더 가벼운 것"},
        "value": "칫솔",
        "unit": "",
    },
}
