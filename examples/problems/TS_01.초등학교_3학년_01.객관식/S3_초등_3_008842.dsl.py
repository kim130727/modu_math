from __future__ import annotations
from modu_math.dsl import (
    Canvas,
    ProblemTemplate,
    Region,
    TextSlot,
    RectSlot,
    LineSlot,
    CircleSlot,
    PolygonSlot,
    PathSlot,
)


def build_problem_template() -> ProblemTemplate:
    return ProblemTemplate(
        id="S3_초등_3_008842",
        title="무게 비교",
        canvas=Canvas(width=940, height=560, coordinate_mode="logical"),
        regions=(
            Region(
                id="region.stem",
                role="stem",
                flow="absolute",
                slot_ids=(
                    "slot.q.line1",
                    "slot.q.line2",
                    "slot.scale.label.ga",
                    "slot.scale.label.na",
                    "slot.scale.tag.daechu_1",
                    "slot.scale.tag.banana_1",
                    "slot.scale.tag.banana_2",
                    "slot.scale.tag.podo",
                ),
            ),
        ),
        slots=(
            TextSlot(
                id="slot.q.line1",
                prompt="",
                text="저울로 대추, 바나나, 포도의 무게를 비교하고 있습니다.",
                style_role="question",
                x=20.703,
                y=35.813,
                font_size=28,
                fill="#111111",
            ),
            TextSlot(
                id="slot.q.line2",
                prompt="",
                text="가장 무거운 것은 무엇인지 알맞은 말을 선택해 보세요.",
                style_role="question",
                x=18,
                y=66,
                font_size=28,
                fill="#111111",
            ),
            TextSlot(
                id="slot.scale.label.ga",
                prompt="",
                text="가",
                style_role="label",
                x=97.014,
                y=217.53,
                font_size=28,
                fill="#111111",
            ),
            TextSlot(
                id="slot.scale.tag.daechu_1",
                prompt="",
                text="대추",
                style_role="label",
                x=152.014,
                y=217.53,
                font_size=28,
                fill="#111111",
            ),
            TextSlot(
                id="slot.scale.tag.banana_1",
                prompt="",
                text="바나나",
                style_role="label",
                x=264.014,
                y=217.53,
                font_size=28,
                fill="#111111",
            ),
            TextSlot(
                id="slot.scale.label.na",
                prompt="",
                text="나",
                style_role="label",
                x=450.014,
                y=217.53,
                font_size=28,
                fill="#111111",
            ),
            TextSlot(
                id="slot.scale.tag.banana_2",
                prompt="",
                text="바나나",
                style_role="label",
                x=507.014,
                y=217.53,
                font_size=28,
                fill="#111111",
            ),
            TextSlot(
                id="slot.scale.tag.podo",
                prompt="",
                text="포도",
                style_role="label",
                x=621.014,
                y=217.53,
                font_size=28,
                fill="#111111",
            ),
        ),
        diagrams=(),
        groups=(),
        constraints=(),
        tags=(),
    )


PROBLEM_TEMPLATE = build_problem_template()

SEMANTIC_OVERRIDE = {
    "problem_id": "S3_초등_3_008842",
    "problem_type": "무게비교",
    "metadata": {
        "language": "ko",
        "question": "저울로 대추, 바나나, 포도의 무게를 비교하고 있습니다. 가장 무거운 것은 무엇인지 알맞은 말을 선택해 보세요.",
        "instruction": "가장 무거운 것을 고른다.",
    },
    "domain": {
        "objects": [
            {"id": "obj.daechu", "type": "fruit", "name": "대추"},
            {"id": "obj.banana", "type": "fruit", "name": "바나나"},
            {"id": "obj.podo", "type": "fruit", "name": "포도"},
        ],
        "relations": [],
        "problem_solving": {
            "understand": {
                "given_refs": [
                    "obj.daechu",
                    "obj.banana",
                    "obj.podo",
                    "rel.daechu_vs_banana",
                    "rel.banana_vs_podo",
                ],
                "target_ref": "answer.target",
                "condition_refs": ["rel.daechu_vs_banana", "rel.banana_vs_podo"],
            },
            "plan": {
                "method": "comparative_order",
                "description": "저울과 문장으로 주어진 비교 관계를 따라 가장 무거운 대상을 찾는다.",
            },
            "execute": {
                "expected_operations": ["compare_weights", "follow_heavier_than_relations"]
            },
            "review": {"check_methods": ["relation_consistency_check"]},
        },
    },
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {"type": "heaviest_fruit", "description": "가장 무거운 것"},
        "value": 0,
        "unit": "",
    },
}

SOLVABLE = {
    "schema": "modu.solvable.v1.1",
    "problem_id": "S3_초등_3_008842",
    "problem_type": "무게비교",
    "inputs": {
        "total_ticks": 0,
        "target_label": "가장 무거운 것",
        "target_ticks": 0,
        "target_count": 3,
        "unit": "",
    },
    "given": [
        {"ref": "obj.daechu", "value": {"name": "대추"}},
        {"ref": "obj.banana", "value": {"name": "바나나"}},
        {"ref": "obj.podo", "value": {"name": "포도"}},
        {
            "ref": "rel.daechu_vs_banana",
            "value": {"heavier": "obj.banana", "lighter": "obj.daechu"},
        },
        {"ref": "rel.banana_vs_podo", "value": {"heavier": "obj.podo", "lighter": "obj.banana"}},
    ],
    "target": {"ref": "answer.target", "type": "heaviest_fruit"},
    "method": "comparative_order",
    "plan": [
        "저울에서 주어진 비교 관계를 읽는다.",
        "더 무거운 대상을 따라가며 가장 무거운 대상을 찾는다.",
    ],
    "steps": [
        {"id": "step.1", "expr": "바나나 > 대추", "value": "obj.banana"},
        {"id": "step.2", "expr": "포도 > 바나나", "value": "obj.podo"},
        {"id": "step.3", "expr": "가장 무거운 것 찾기", "value": "obj.podo"},
    ],
    "checks": [
        {
            "id": "check.1",
            "expr": "obj.podo가 obj.banana보다 무겁고 obj.banana가 obj.daechu보다 무거운가",
            "expected": True,
            "actual": True,
            "pass": True,
        }
    ],
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {"type": "heaviest_fruit", "description": "가장 무거운 것"},
        "value": 0,
        "unit": "",
    },
}
