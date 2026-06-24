from __future__ import annotations
from modu_math.dsl import Canvas, ProblemTemplate, Region, TextSlot, RectSlot, LineSlot, CircleSlot


def build_problem_template() -> ProblemTemplate:
    return ProblemTemplate(
        id="S3_초등_3_008833",
        title="저울 비교 결과 알맞은 말 선택",
        canvas=Canvas(width=920, height=530, coordinate_mode="logical"),
        regions=(
            Region(
                id="region.top",
                role="stem",
                flow="absolute",
                slot_ids=("slot.top.qmark", "slot.top.title"),
            ),
            Region(
                id="region.character",
                role="supporting",
                flow="absolute",
                slot_ids=("slot.name", "slot.bubble", "slot.guide"),
            ),
            Region(
                id="region.diagram",
                role="diagram",
                flow="absolute",
                slot_ids=(
                    "slot.arrow",
                    "slot.scale.left.base",
                    "slot.scale.left.pan.left",
                    "slot.scale.left.pan.right",
                    "slot.scale.left.body",
                    "slot.scale.right.base",
                    "slot.scale.right.pan.left",
                    "slot.scale.right.pan.right",
                    "slot.scale.right.body",
                    "slot.scale.right.apple_label",
                    "slot.scale.right.apple",
                    "slot.scale.right.peach_label",
                    "slot.scale.right.peach",
                ),
            ),
            Region(id="region.bottom", role="answer", flow="absolute", slot_ids=()),
        ),
        slots=(
            TextSlot(
                id="slot.top.qmark",
                prompt="",
                text="□",
                style_role="question",
                x=4.0,
                y=30.0,
                font_size=24,
            ),
            TextSlot(
                id="slot.top.title",
                prompt="",
                text="71. 정현이가 자두와 배의 무게를 비교하려고 합니다. 알맞은 말을 선택하세요.",
                style_role="question",
                x=42.0,
                y=30.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.name",
                prompt="",
                text="정현",
                style_role="label",
                x=60.0,
                y=130.0,
                font_size=28,
            ),
            RectSlot(id="slot.name.box", prompt="", x=40.0, y=110.0, width=90.0, height=38.0),
            TextSlot(
                id="slot.bubble",
                prompt="",
                text="저울을 사용하여 자두와 배의 무게를 비교해아지.",
                style_role="speech",
                x=170.0,
                y=122.0,
                font_size=28,
            ),
            RectSlot(id="slot.bubble.box", prompt="", x=150.0, y=90.0, width=430.0, height=72.0),
            TextSlot(
                id="slot.guide",
                prompt="",
                text="윗접시저울로 무게를 비교하려면 우선 저울의 영점을 맞춰야 해요.",
                style_role="instruction",
                x=430.0,
                y=195.0,
                font_size=28,
            ),
            LineSlot(id="slot.guide.arrow", prompt="", x1=412.0, y1=200.0, x2=370.0, y2=150.0),
            TextSlot(
                id="slot.arrow",
                prompt="",
                text="→",
                style_role="symbol",
                x=505.0,
                y=315.0,
                font_size=44,
            ),
            LineSlot(id="slot.scale.left.base", prompt="", x1=330.0, y1=388.0, x2=430.0, y2=388.0),
            LineSlot(
                id="slot.scale.left.pan.left", prompt="", x1=360.0, y1=250.0, x2=330.0, y2=250.0
            ),
            LineSlot(
                id="slot.scale.left.pan.right", prompt="", x1=430.0, y1=250.0, x2=460.0, y2=250.0
            ),
            LineSlot(id="slot.scale.left.body", prompt="", x1=395.0, y1=250.0, x2=395.0, y2=388.0),
            LineSlot(id="slot.scale.right.base", prompt="", x1=645.0, y1=388.0, x2=745.0, y2=388.0),
            LineSlot(
                id="slot.scale.right.pan.left", prompt="", x1=675.0, y1=250.0, x2=645.0, y2=250.0
            ),
            LineSlot(
                id="slot.scale.right.pan.right", prompt="", x1=745.0, y1=250.0, x2=775.0, y2=250.0
            ),
            LineSlot(id="slot.scale.right.body", prompt="", x1=710.0, y1=250.0, x2=710.0, y2=388.0),
            TextSlot(
                id="slot.scale.right.apple_label",
                prompt="",
                text="자두",
                style_role="label",
                x=665.0,
                y=190.0,
                font_size=24,
            ),
            RectSlot(
                id="slot.scale.right.apple_label.box",
                prompt="",
                x=655.0,
                y=172.0,
                width=56.0,
                height=30.0,
            ),
            CircleSlot(
                id="slot.scale.right.apple", prompt="", cx=686.0, cy=235.0, r=13.0, fill="#d95555"
            ),
            TextSlot(
                id="slot.scale.right.peach_label",
                prompt="",
                text="배",
                style_role="label",
                x=800.0,
                y=190.0,
                font_size=24,
            ),
            RectSlot(
                id="slot.scale.right.peach_label.box",
                prompt="",
                x=790.0,
                y=172.0,
                width=42.0,
                height=30.0,
            ),
            CircleSlot(
                id="slot.scale.right.peach", prompt="", cx=808.0, cy=235.0, r=15.0, fill="#f0b04b"
            ),
        ),
        diagrams=(),
        groups=(),
        constraints=(),
        tags=(),
    )


PROBLEM_TEMPLATE = build_problem_template()

SEMANTIC_OVERRIDE = {
    "problem_id": "S3_초등_3_008833",
    "problem_type": "무게비교_선택",
    "metadata": {
        "language": "ko",
        "question": "정현이가 자두와 배의 무게를 비교하려고 합니다. 알맞은 말을 선택하세요.",
        "instruction": "저울의 비교 결과를 보고 더 무거운 쪽을 고른다.",
    },
    "domain": {
        "objects": [
            {"id": "obj.scale.before", "type": "balance_scale", "state": "empty"},
            {"id": "obj.scale.after", "type": "balance_scale", "state": "compared"},
            {"id": "obj.plum", "type": "fruit", "name": "자두"},
            {"id": "obj.peach", "type": "fruit", "name": "배"},
        ],
        "relations": [],
        "problem_solving": {
            "understand": {
                "given_refs": ["obj.scale.after", "obj.plum", "obj.peach"],
                "target_ref": "answer.target",
                "condition_refs": ["rel.compare.weight", "rel.pan.lower"],
            },
            "plan": {
                "method": "compare_weight_by_balance",
                "description": "저울에서 더 내려간 쪽에 놓인 물체가 더 무거운지 확인한다.",
            },
            "execute": {"expected_operations": ["identify_lower_pan", "choose_heavier_fruit"]},
            "review": {"check_methods": ["match_statement_with_balance_result"]},
        },
    },
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {"type": "heavier_fruit", "description": "더 무거운 과일"},
        "value": "배",
        "unit": "",
    },
}

SOLVABLE = {
    "schema": "modu.solvable.v1.1",
    "problem_id": "S3_초등_3_008833",
    "problem_type": "무게비교_선택",
    "inputs": {
        "total_ticks": 0,
        "target_label": "더 무거운 과일",
        "target_ticks": 0,
        "target_count": 1,
        "unit": "",
    },
    "given": [
        {"ref": "obj.plum", "value": {"name": "자두"}},
        {"ref": "obj.peach", "value": {"name": "배"}},
        {"ref": "rel.pan.lower", "value": {"subject": "obj.peach"}},
    ],
    "target": {"ref": "answer.target", "type": "heavier_fruit"},
    "method": "compare_weight_by_balance",
    "plan": [
        "저울에서 아래로 내려간 접시에 놓인 과일을 찾는다.",
        "그 과일이 더 무겁다고 판단한다.",
    ],
    "steps": [
        {"id": "step.1", "expr": "배가 놓인 접시가 아래로 내려감", "value": "배"},
        {"id": "step.2", "expr": "아래로 내려간 쪽이 더 무거움", "value": "배"},
    ],
    "checks": [
        {
            "id": "check.1",
            "expr": "배가 더 무거운지 확인",
            "expected": "배",
            "actual": "배",
            "pass": True,
        }
    ],
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {"type": "heavier_fruit", "description": "더 무거운 과일"},
        "value": "배",
        "unit": "",
    },
}
