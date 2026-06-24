from __future__ import annotations
from modu_math.dsl import Canvas, ProblemTemplate, Region, TextSlot, RectSlot


def build_problem_template() -> ProblemTemplate:
    return ProblemTemplate(
        id="S3_초등_3_008853",
        title="책가방 무게 비교",
        canvas=Canvas(width=825.0, height=408.0, coordinate_mode="logical"),
        regions=(
            Region(
                id="region.stem",
                role="stem",
                flow="absolute",
                slot_ids=(
                    "slot.q.box",
                    "slot.q.num",
                    "slot.q.text",
                    "slot.left.name",
                    "slot.left.weight",
                    "slot.right.name",
                    "slot.right.weight",
                ),
            ),
            Region(id="region.answer", role="answer", flow="absolute", slot_ids=()),
        ),
        slots=(
            RectSlot(id="slot.q.box", prompt="", x=10.0, y=11.0, width=13.0, height=13.0),
            TextSlot(
                id="slot.q.num",
                prompt="",
                text="99.",
                style_role="question",
                x=30.0,
                y=24.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.q.text",
                prompt="",
                text="민재와 소라 중 누구의 책가방이 더 무거운지 선택해 보세요.",
                style_role="question",
                x=79.0,
                y=24.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.left.name",
                prompt="",
                text="민재",
                style_role="label",
                x=313.0,
                y=129.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.left.weight",
                prompt="",
                text="3 kg 700 g",
                style_role="label",
                x=300.0,
                y=177.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.right.name",
                prompt="",
                text="소라",
                style_role="label",
                x=572.0,
                y=129.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.right.weight",
                prompt="",
                text="3080 g",
                style_role="label",
                x=585.0,
                y=177.0,
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
    "problem_id": "S3_초등_3_008853",
    "problem_type": "compare_weight",
    "metadata": {
        "language": "ko",
        "question": "민재와 소라 중 누구의 책가방이 더 무거운지 선택하는 문제",
        "instruction": "무게를 비교하여 더 무거운 사람을 고른다.",
    },
    "domain": {
        "objects": [
            {"id": "obj.minj.a", "type": "person", "name": "민재", "weight_text": "3 kg 700 g"},
            {"id": "obj.sora", "type": "person", "name": "소라", "weight_text": "3080 g"},
        ],
        "relations": [],
        "problem_solving": {
            "understand": {
                "given_refs": ["obj.minj.a", "obj.sora"],
                "target_ref": "answer.target",
                "condition_refs": ["rel.compare.weight"],
            },
            "plan": {
                "method": "unit_conversion_and_comparison",
                "description": "같은 단위로 바꾼 뒤 두 무게를 비교한다.",
            },
            "execute": {
                "expected_operations": [
                    "convert_weight_unit",
                    "compare_values",
                    "choose_heavier_object",
                ]
            },
            "review": {"check_methods": ["unit_consistency_check", "comparison_sign_check"]},
        },
    },
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {"type": "heavier_person", "description": "더 무거운 책가방의 주인"},
        "value": "민재",
        "unit": "",
    },
}

SOLVABLE = {
    "schema": "modu.solvable.v1.1",
    "problem_id": "S3_초등_3_008853",
    "problem_type": "compare_weight",
    "inputs": {
        "total_ticks": 0,
        "target_label": "더 무거운 사람",
        "target_ticks": 0,
        "target_count": 2,
        "unit": "g",
    },
    "given": [{"ref": "obj.minj.a", "value": "3 kg 700 g"}, {"ref": "obj.sora", "value": "3080 g"}],
    "target": {"ref": "answer.target", "type": "heavier_person"},
    "method": "unit_conversion_and_comparison",
    "plan": [
        "민재의 무게를 g 단위로 바꾼다.",
        "두 무게를 비교한다.",
        "더 큰 무게의 주인을 답으로 고른다.",
    ],
    "steps": [
        {"id": "step.1", "expr": "3 kg 700 g = 3700 g", "value": 3700},
        {"id": "step.2", "expr": "3700 g > 3080 g", "value": True},
        {"id": "step.3", "expr": "더 무거운 사람 = 민재", "value": "민재"},
    ],
    "checks": [
        {"id": "check.1", "expr": "3700 > 3080", "expected": True, "actual": True, "pass": True},
        {
            "id": "check.2",
            "expr": "답이 민재인지 확인",
            "expected": "민재",
            "actual": "민재",
            "pass": True,
        },
    ],
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {"type": "heavier_person", "description": "더 무거운 책가방의 주인"},
        "value": "민재",
        "unit": "",
    },
}
