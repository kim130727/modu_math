from __future__ import annotations
from modu_math.dsl import Canvas, ProblemTemplate, Region, RectSlot, TextSlot


def build_problem_template() -> ProblemTemplate:
    return ProblemTemplate(
        id="S3_초등_3_008761",
        title="저울로 무거운 것 비교하기",
        canvas=Canvas(width=960, height=490, coordinate_mode="logical"),
        regions=(
            Region(
                id="region.header",
                role="stem",
                flow="absolute",
                slot_ids=("slot.no", "slot.title1", "slot.title2"),
            ),
            Region(
                id="region.diagram",
                role="diagram",
                flow="absolute",
                slot_ids=(
                    "slot.scale.base",
                    "slot.scale.pillar",
                    "slot.scale.beam",
                    "slot.scale.left.pan",
                    "slot.scale.right.pan",
                    "slot.apple.box",
                    "slot.apple.text",
                    "slot.pear.box",
                    "slot.pear.text",
                    "slot.apple.draw",
                    "slot.pear.draw",
                ),
            ),
            Region(id="region.body", role="stem", flow="absolute", slot_ids=("slot.s1", "slot.s2")),
        ),
        slots=(
            TextSlot(
                id="slot.no",
                prompt="",
                text="63.",
                style_role="question",
                x=18.0,
                y=34.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.title1",
                prompt="",
                text="저울을 사용하여 사과와 배의 무게를 비교하려고 합니다. 알맞은 말을",
                style_role="question",
                x=72.0,
                y=34.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.title2",
                prompt="",
                text="선택하세요.",
                style_role="question",
                x=18.0,
                y=71.0,
                font_size=28,
            ),
            RectSlot(id="slot.scale.base", prompt="", x=389.0, y=197.0, width=184.0, height=22.0),
            RectSlot(id="slot.scale.pillar", prompt="", x=470.0, y=123.0, width=18.0, height=90.0),
            RectSlot(id="slot.scale.beam", prompt="", x=410.0, y=162.0, width=140.0, height=16.0),
            RectSlot(
                id="slot.scale.left.pan", prompt="", x=370.0, y=135.0, width=82.0, height=26.0
            ),
            RectSlot(
                id="slot.scale.right.pan", prompt="", x=512.0, y=147.0, width=82.0, height=26.0
            ),
            RectSlot(id="slot.apple.box", prompt="", x=382.0, y=85.0, width=48.0, height=26.0),
            TextSlot(
                id="slot.apple.text",
                prompt="",
                text="사과",
                style_role="label",
                x=388.0,
                y=106.0,
                font_size=24,
            ),
            RectSlot(id="slot.pear.box", prompt="", x=539.0, y=85.0, width=48.0, height=26.0),
            TextSlot(
                id="slot.pear.text",
                prompt="",
                text="배",
                style_role="label",
                x=551.0,
                y=106.0,
                font_size=24,
            ),
            TextSlot(
                id="slot.apple.draw",
                prompt="",
                text="🍎",
                style_role="label",
                x=388.0,
                y=132.0,
                font_size=38,
            ),
            TextSlot(
                id="slot.pear.draw",
                prompt="",
                text="🍐",
                style_role="label",
                x=548.0,
                y=136.0,
                font_size=38,
            ),
            TextSlot(
                id="slot.s1",
                prompt="",
                text="(1) ( 사과 , 배 )를 올려놓은 접시가 아래로 내려갔습니다.",
                style_role="question",
                x=18.0,
                y=314.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.s2",
                prompt="",
                text="(2) ( 사과 , 배 )가 더 무겁습니다.",
                style_role="question",
                x=18.0,
                y=352.0,
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
    "problem_id": "S3_초등_3_008761",
    "problem_type": "comparison_by_balance_scale",
    "metadata": {
        "language": "ko",
        "question": "저울을 사용하여 사과와 배의 무게를 비교하는 문제",
        "instruction": "알맞은 말을 선택하세요.",
    },
    "domain": {
        "objects": [
            {"id": "obj.apple", "type": "fruit", "name": "사과"},
            {"id": "obj.pear", "type": "fruit", "name": "배"},
            {"id": "obj.scale", "type": "balance_scale"},
        ],
        "relations": [],
        "problem_solving": {
            "understand": {
                "given_refs": ["obj.apple", "obj.pear", "obj.scale"],
                "target_ref": "answer.target",
                "condition_refs": ["rel.pear_heavier"],
            },
            "plan": {
                "method": "balance_scale_comparison",
                "description": "저울의 아래로 내려간 쪽에 놓인 과일이 더 무거운지 판단한다.",
            },
            "execute": {"expected_operations": ["compare_pan_height", "identify_heavier_fruit"]},
            "review": {"check_methods": ["match_with_explanation"]},
        },
    },
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {"type": "selection", "description": "(1), (2)에 들어갈 알맞은 말"},
        "value": 2,
        "unit": "",
    },
}

SOLVABLE = {
    "schema": "modu.solvable.v1.1",
    "problem_id": "S3_초등_3_008761",
    "problem_type": "comparison_by_balance_scale",
    "inputs": {
        "total_ticks": 1,
        "target_label": "알맞은 말 선택",
        "target_ticks": 1,
        "target_count": 2,
        "unit": "",
    },
    "given": [
        {"ref": "obj.apple", "value": {"name": "사과"}},
        {"ref": "obj.pear", "value": {"name": "배"}},
        {"ref": "obj.scale", "value": {"type": "balance_scale"}},
    ],
    "target": {"ref": "answer.target", "type": "selection"},
    "method": "balance_scale_comparison",
    "plan": [
        "저울에서 더 내려간 쪽에 놓인 과일을 찾는다.",
        "그 과일이 더 무겁다고 판단하여 문장의 빈칸에 맞는 말을 고른다.",
    ],
    "steps": [
        {"id": "step.1", "expr": "오른쪽 접시가 더 아래로 내려감", "value": "right_pan_lower"},
        {"id": "step.2", "expr": "더 무거운 과일 = 배", "value": "배"},
        {"id": "step.3", "expr": "(1), (2)에 들어갈 말 선택", "value": ["배", "배"]},
    ],
    "checks": [
        {
            "id": "check.1",
            "expr": "해설의 문장과 일치하는지 확인",
            "expected": "배가 더 무겁다",
            "actual": "배가 더 무겁다",
            "pass": True,
        },
        {
            "id": "check.2",
            "expr": "(1), (2) 선택값이 동일한지 확인",
            "expected": ["배", "배"],
            "actual": ["배", "배"],
            "pass": True,
        },
    ],
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {"type": "selection", "description": "(1), (2)에 들어갈 알맞은 말"},
        "value": 2,
        "unit": "",
    },
}
