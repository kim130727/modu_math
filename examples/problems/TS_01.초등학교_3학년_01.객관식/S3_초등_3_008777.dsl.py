from __future__ import annotations
from modu_math.dsl import Canvas, ProblemTemplate, RectSlot, Region, TextSlot


def build_problem_template() -> ProblemTemplate:
    return ProblemTemplate(
        id="S3_초등_3_008777",
        title="알맞은 단위를 선택하세요",
        canvas=Canvas(width=760, height=330, coordinate_mode="logical"),
        regions=(
            Region(
                id="region.stem",
                role="stem",
                flow="absolute",
                slot_ids=(
                    "slot.q0",
                    "slot.q1",
                    "slot.q2",
                    "slot.q3",
                    "slot.q6",
                    "slot.q7",
                    "slot.q8",
                    "slot.q9",
                    "slot.q10",
                ),
            ),
        ),
        slots=(
            TextSlot(
                id="slot.q0",
                prompt="",
                text="□",
                style_role="question",
                x=14.0,
                y=34.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.q1",
                prompt="",
                text="90.",
                style_role="question",
                x=38.0,
                y=34.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.q2",
                prompt="",
                text="알맞은 단위를 선택하세요.",
                style_role="question",
                x=90.0,
                y=34.0,
                font_size=28,
            ),
            RectSlot(
                id="slot.img.placeholder", prompt="", x=150.0, y=82.0, width=150.0, height=120.0
            ),
            TextSlot(
                id="slot.q3",
                prompt="",
                text="주전자의 들이는 약 1 ( mL , L )입니다.",
                style_role="question",
                x=305.0,
                y=126.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.q6",
                prompt="",
                text="mL",
                style_role="question",
                x=470.0,
                y=126.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.q7",
                prompt="",
                text=",",
                style_role="question",
                x=524.0,
                y=126.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.q8",
                prompt="",
                text="L",
                style_role="question",
                x=550.0,
                y=126.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.q9",
                prompt="",
                text=")",
                style_role="question",
                x=578.0,
                y=126.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.q10",
                prompt="",
                text="주전자 그림",
                style_role="question",
                x=0.0,
                y=0.0,
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
    "problem_id": "S3_초등_3_008777",
    "problem_type": "unit_selection",
    "metadata": {
        "language": "ko",
        "question": "알맞은 단위를 선택하세요.",
        "instruction": "주전자의 들이에 알맞은 단위를 고르는 문제입니다.",
    },
    "domain": {
        "objects": [
            {"id": "obj.kettle", "type": "container", "name": "주전자"},
            {"id": "obj.quantity", "type": "capacity", "value": 1, "unit_candidates": ["mL", "L"]},
        ],
        "relations": [],
        "problem_solving": {
            "understand": {
                "given_refs": ["obj.kettle", "obj.quantity"],
                "target_ref": "answer.target",
                "condition_refs": ["rel.choose_unit"],
            },
            "plan": {
                "method": "unit_selection",
                "description": "대상에 어울리는 들이의 단위를 고른다.",
            },
            "execute": {"expected_operations": ["compare_unit_scale", "select_appropriate_unit"]},
            "review": {"check_methods": ["context_unit_check"]},
        },
    },
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {"type": "unit", "description": "주전자의 들이에 알맞은 단위"},
        "value": "L",
        "unit": "",
    },
}

SOLVABLE = {
    "schema": "modu.solvable.v1.1",
    "problem_id": "S3_초등_3_008777",
    "problem_type": "unit_selection",
    "inputs": {
        "total_ticks": 0,
        "target_label": "주전자의 들이에 알맞은 단위",
        "target_ticks": 0,
        "target_count": 1,
        "unit": "",
    },
    "given": [
        {"ref": "obj.kettle", "value": {"name": "주전자"}},
        {"ref": "obj.quantity", "value": {"value": 1, "unit_candidates": ["mL", "L"]}},
    ],
    "target": {"ref": "answer.target", "type": "unit"},
    "method": "unit_selection",
    "plan": ["대상의 들이 크기를 보고 알맞은 단위를 고른다."],
    "steps": [
        {"id": "step.1", "expr": "주전자의 들이 단위 후보를 확인한다.", "value": ["mL", "L"]},
        {"id": "step.2", "expr": "주전자에 알맞은 단위를 선택한다.", "value": "L"},
    ],
    "checks": [
        {
            "id": "check.1",
            "expr": "문장과 해설에 제시된 단위가 일치하는지 확인한다.",
            "expected": "L",
            "actual": "L",
            "pass": True,
        }
    ],
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {"type": "unit", "description": "주전자의 들이에 알맞은 단위"},
        "value": "L",
        "unit": "",
    },
}
