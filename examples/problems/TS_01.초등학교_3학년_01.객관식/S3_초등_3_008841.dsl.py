from __future__ import annotations
from modu_math.dsl import (
    Canvas,
    ProblemTemplate,
    Region,
    TextSlot,
    RectSlot,
    CircleSlot,
    LineSlot,
    PolygonSlot,
)


def build_problem_template() -> ProblemTemplate:
    return ProblemTemplate(
        id="S3_초등_3_008841",
        title="저울로 무게 비교하기",
        canvas=Canvas(width=944, height=507, coordinate_mode="logical"),
        regions=(
            Region(
                id="region.header",
                role="stem",
                flow="absolute",
                slot_ids=("slot.title1", "slot.title2"),
            ),
            Region(
                id="region.diagram.left",
                role="diagram",
                flow="absolute",
                slot_ids=(
                    "slot.l_label_ga",
                    "slot.l.fruit.daejoo",
                    "slot.l.fruit.banana",
                ),
            ),
            Region(
                id="region.diagram.right",
                role="diagram",
                flow="absolute",
                slot_ids=(
                    "slot.r_label_na",
                    "slot.r.fruit.banana",
                    "slot.r.fruit.grape",
                ),
            ),
            Region(id="region.body", role="stem", flow="absolute", slot_ids=("slot.q1",)),
        ),
        slots=(
            TextSlot(
                id="slot.title1",
                prompt="",
                text="저울로 대추, 바나나, 포도의 무게를 비교하고 있습니다. 가장 무거운 것",
                style_role="question",
                x=26.553,
                y=54.893,
                font_size=28,
                fill="#111111",
            ),
            TextSlot(
                id="slot.title2",
                prompt="",
                text="은 무엇인지 알맞은 말을 선택해 보세요.",
                style_role="question",
                x=25.059,
                y=101.328,
                font_size=28,
                fill="#111111",
            ),
            TextSlot(
                id="slot.l_label_ga",
                prompt="",
                text="가",
                style_role="label",
                x=164.601,
                y=209.114,
                font_size=28,
                fill="#111111",
            ),
            CircleSlot(
                id="slot.l.fruit.daejoo", prompt="", cx=286.0, cy=187.0, r=10.0, fill="#222222"
            ),
            CircleSlot(
                id="slot.l.fruit.banana", prompt="", cx=386.0, cy=197.0, r=10.0, fill="#222222"
            ),
            TextSlot(
                id="slot.r_label_na",
                prompt="",
                text="나",
                style_role="label",
                x=533.929,
                y=206.126,
                font_size=28,
                fill="#111111",
            ),
            CircleSlot(
                id="slot.r.fruit.banana", prompt="", cx=612.0, cy=187.0, r=10.0, fill="#222222"
            ),
            CircleSlot(
                id="slot.r.fruit.grape", prompt="", cx=717.0, cy=197.0, r=10.0, fill="#222222"
            ),
            TextSlot(
                id="slot.q1",
                prompt="",
                text="(1) 가에서 대추와 바나나 중 더 무거운 것은 ( 대추, 바나나 )이고,\n   나에서 바나나와 포도 중 더 무거운 것은 ( 바나나, 포도 )입니다.",
                style_role="question",
                x=53.858,
                y=437.114,
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
    "problem_id": "S3_초등_3_008841",
    "problem_type": "무게 비교",
    "metadata": {
        "language": "ko",
        "question": "저울로 대추, 바나나, 포도의 무게를 비교하고 있습니다. 가장 무거운 것은 무엇인지 알맞은 말을 선택해 보세요.",
        "instruction": "저울의 기울어짐을 보고 더 무거운 것을 고른다.",
    },
    "domain": {
        "objects": [
            {"id": "obj.daejoo", "type": "fruit", "name": "대추"},
            {"id": "obj.banana", "type": "fruit", "name": "바나나"},
            {"id": "obj.grape", "type": "fruit", "name": "포도"},
            {"id": "obj.scale.ga", "type": "balance_scale", "name": "가"},
            {"id": "obj.scale.na", "type": "balance_scale", "name": "나"},
        ],
        "relations": [],
        "problem_solving": {
            "understand": {
                "given_refs": ["obj.scale.ga", "obj.scale.na"],
                "target_ref": "answer.target",
                "condition_refs": ["rel.ga_compare", "rel.na_compare"],
            },
            "plan": {
                "method": "balance_comparison",
                "description": "각 저울에서 더 내려간 접시 쪽의 물체가 더 무거운지 확인한다.",
            },
            "execute": {
                "expected_operations": [
                    "compare_two_objects_on_scale",
                    "identify_heavier_side",
                    "select_heaviest_among_candidates",
                ]
            },
            "review": {"check_methods": ["compare_consistency_between_scales"]},
        },
    },
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {
            "type": "heaviest_fruits",
            "description": "가와 나의 비교 결과를 바탕으로 가장 무거운 것",
        },
        "value": "포도",
        "unit": "",
    },
}

SOLVABLE = {
    "schema": "modu.solvable.v1.1",
    "problem_id": "S3_초등_3_008841",
    "problem_type": "무게 비교",
    "inputs": {
        "total_ticks": 2,
        "target_label": "가장 무거운 것",
        "target_ticks": 1,
        "target_count": 1,
        "unit": "",
    },
    "given": [
        {"ref": "obj.scale.ga", "value": {"comparison": "대추 vs 바나나"}},
        {"ref": "obj.scale.na", "value": {"comparison": "바나나 vs 포도"}},
    ],
    "target": {"ref": "answer.target", "type": "heaviest_fruits"},
    "method": "balance_comparison",
    "plan": [
        "각 저울에서 더 내려간 접시 쪽의 과일이 더 무거운지 확인한다.",
        "두 비교 결과를 읽어 가장 무거운 대상을 찾는다.",
    ],
    "steps": [
        {"id": "step.1", "expr": "가에서 바나나 쪽 접시가 더 내려감", "value": "바나나 > 대추"},
        {"id": "step.2", "expr": "나에서 포도 쪽 접시가 더 내려감", "value": "포도 > 바나나"},
        {"id": "step.3", "expr": "두 비교를 종합하면 가장 무거운 것 결정", "value": "포도"},
    ],
    "checks": [
        {"id": "check.1", "expr": "바나나 > 대추", "expected": True, "actual": True, "pass": True},
        {"id": "check.2", "expr": "포도 > 바나나", "expected": True, "actual": True, "pass": True},
    ],
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {
            "type": "heaviest_fruits",
            "description": "가와 나의 비교 결과를 바탕으로 가장 무거운 것",
        },
        "value": "포도",
        "unit": "",
    },
}
