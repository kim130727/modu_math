from __future__ import annotations
from modu_math.dsl import Canvas, ProblemTemplate, Region, TextSlot, RectSlot


def build_problem_template() -> ProblemTemplate:
    return ProblemTemplate(
        id="S3_초등_3_008828",
        title="알맞은 단위를 선택하세요",
        canvas=Canvas(width=776.0, height=346.0, coordinate_mode="logical"),
        regions=(
            Region(
                id="region.stem",
                role="stem",
                flow="absolute",
                slot_ids=("slot.q1", "slot.illustration", "slot.body"),
            ),
        ),
        slots=(
            TextSlot(
                id="slot.q1",
                prompt="",
                text="□ 61. 알맞은 단위를 선택하세요.",
                style_role="question",
                x=10.0,
                y=30.0,
                font_size=28,
            ),
            RectSlot(id="slot.illustration", prompt="", x=404.0, y=42.0, width=60.0, height=74.0),
            TextSlot(
                id="slot.body",
                prompt="",
                text="요구르트병의 들이는 약 80( mL , L )입니다.",
                style_role="body",
                x=200.0,
                y=160.0,
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
    "problem_id": "S3_초등_3_008828",
    "problem_type": "unit_choice",
    "metadata": {
        "language": "ko",
        "question": "알맞은 단위를 선택하는 문제",
        "instruction": "요구르트병의 들이에 알맞은 단위를 고른다.",
    },
    "domain": {
        "objects": [
            {"id": "obj.container", "type": "container", "name": "요구르트병"},
            {"id": "obj.quantity", "type": "capacity", "value": 80},
            {"id": "obj.unit_mL", "type": "unit", "symbol": "mL"},
            {"id": "obj.unit_L", "type": "unit", "symbol": "L"},
        ],
        "relations": [],
        "problem_solving": {
            "understand": {
                "given_refs": ["obj.container", "obj.quantity", "obj.unit_mL", "obj.unit_L"],
                "target_ref": "answer.target",
                "condition_refs": ["rel.choose_unit"],
            },
            "plan": {
                "method": "unit_comparison",
                "description": "양에 알맞은 들이의 단위를 고른다.",
            },
            "execute": {
                "expected_operations": ["compare_capacity_scale", "select_appropriate_unit"]
            },
            "review": {"check_methods": ["unit_consistency_check"]},
        },
    },
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {"type": "selected_unit", "description": "80에 알맞은 단위"},
        "value": "mL",
        "unit": "mL",
    },
}

SOLVABLE = {
    "schema": "modu.solvable.v1.1",
    "problem_id": "S3_초등_3_008828",
    "problem_type": "unit_choice",
    "inputs": {
        "total_ticks": 1,
        "target_label": "알맞은 단위",
        "target_ticks": 1,
        "target_count": 1,
        "unit": "",
    },
    "given": [
        {"ref": "obj.quantity", "value": 80},
        {"ref": "obj.unit_mL", "value": "mL"},
        {"ref": "obj.unit_L", "value": "L"},
    ],
    "target": {"ref": "answer.target", "type": "selected_unit"},
    "method": "unit_comparison",
    "plan": ["80에 어울리는 들이의 단위를 후보와 비교한다.", "작은 양에는 mL가 알맞은지 확인한다."],
    "steps": [{"id": "step.1", "expr": "80과 mL, L를 비교한다", "value": "mL"}],
    "checks": [
        {
            "id": "check.1",
            "expr": "80은 L보다 작은 들이로 보는 것이 자연스러운가",
            "expected": True,
            "actual": True,
            "pass": True,
        }
    ],
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {"type": "selected_unit", "description": "80에 알맞은 단위"},
        "value": "mL",
        "unit": "mL",
    },
}
