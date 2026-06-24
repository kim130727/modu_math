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
                slot_ids=("slot.num", "slot.title1", "slot.title2"),
            ),
            Region(
                id="region.diagram.left",
                role="diagram",
                flow="absolute",
                slot_ids=(
                    "slot.l_label_ga",
                    "slot.l_label_daejoo",
                    "slot.l_label_banana",
                    "slot.l.scale.base",
                    "slot.l.scale.pillar",
                    "slot.l.scale.beam",
                    "slot.l.scale.left_pan",
                    "slot.l.scale.right_pan",
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
                    "slot.r_label_banana",
                    "slot.r_label_grape",
                    "slot.r.scale.base",
                    "slot.r.scale.pillar",
                    "slot.r.scale.beam",
                    "slot.r.scale.left_pan",
                    "slot.r.scale.right_pan",
                    "slot.r.fruit.banana",
                    "slot.r.fruit.grape",
                ),
            ),
            Region(id="region.body", role="stem", flow="absolute", slot_ids=("slot.q1",)),
        ),
        slots=(
            TextSlot(
                id="slot.num",
                prompt="",
                text="83.",
                style_role="question",
                x=14.0,
                y=28.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.title1",
                prompt="",
                text="저울로 대추, 바나나, 포도의 무게를 비교하고 있습니다. 가장 무거운 것",
                style_role="question",
                x=40.0,
                y=28.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.title2",
                prompt="",
                text="은 무엇인지 알맞은 말을 선택해 보세요.",
                style_role="question",
                x=40.0,
                y=58.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.l_label_ga",
                prompt="",
                text="가",
                style_role="label",
                x=190.0,
                y=112.0,
                font_size=28,
            ),
            RectSlot(id="slot.l_label_daejoo", prompt="", x=244.0, y=86.0, width=54.0, height=30.0),
            TextSlot(
                id="slot.l_label_daejoo_text",
                prompt="",
                text="대추",
                style_role="label",
                x=252.0,
                y=110.0,
                font_size=22,
            ),
            RectSlot(id="slot.l_label_banana", prompt="", x=363.0, y=86.0, width=66.0, height=30.0),
            TextSlot(
                id="slot.l_label_banana_text",
                prompt="",
                text="바나나",
                style_role="label",
                x=367.0,
                y=110.0,
                font_size=22,
            ),
            LineSlot(id="slot.l.scale.base", prompt="", x1=220.0, y1=284.0, x2=448.0, y2=284.0),
            LineSlot(id="slot.l.scale.pillar", prompt="", x1=334.0, y1=284.0, x2=334.0, y2=174.0),
            LineSlot(id="slot.l.scale.beam", prompt="", x1=246.0, y1=164.0, x2=415.0, y2=174.0),
            LineSlot(id="slot.l.scale.left_pan", prompt="", x1=276.0, y1=174.0, x2=257.0, y2=220.0),
            LineSlot(
                id="slot.l.scale.right_pan", prompt="", x1=385.0, y1=175.0, x2=404.0, y2=220.0
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
                x=516.0,
                y=112.0,
                font_size=28,
            ),
            RectSlot(id="slot.r_label_banana", prompt="", x=574.0, y=86.0, width=66.0, height=30.0),
            TextSlot(
                id="slot.r_label_banana_text",
                prompt="",
                text="바나나",
                style_role="label",
                x=578.0,
                y=110.0,
                font_size=22,
            ),
            RectSlot(id="slot.r_label_grape", prompt="", x=703.0, y=86.0, width=54.0, height=30.0),
            TextSlot(
                id="slot.r_label_grape_text",
                prompt="",
                text="포도",
                style_role="label",
                x=711.0,
                y=110.0,
                font_size=22,
            ),
            LineSlot(id="slot.r.scale.base", prompt="", x1=548.0, y1=284.0, x2=776.0, y2=284.0),
            LineSlot(id="slot.r.scale.pillar", prompt="", x1=662.0, y1=284.0, x2=662.0, y2=174.0),
            LineSlot(id="slot.r.scale.beam", prompt="", x1=574.0, y1=164.0, x2=743.0, y2=174.0),
            LineSlot(id="slot.r.scale.left_pan", prompt="", x1=604.0, y1=174.0, x2=585.0, y2=220.0),
            LineSlot(
                id="slot.r.scale.right_pan", prompt="", x1=713.0, y1=175.0, x2=732.0, y2=220.0
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
                x=18.0,
                y=340.0,
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
