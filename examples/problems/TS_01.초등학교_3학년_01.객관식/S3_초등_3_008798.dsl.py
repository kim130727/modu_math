from __future__ import annotations
from modu_math.dsl import Canvas, ProblemTemplate, Region, TextSlot, RectSlot


def build_problem_template() -> ProblemTemplate:
    return ProblemTemplate(
        id="S3_초등_3_008798",
        title="알맞은 단위를 선택하세요",
        canvas=Canvas(width=820, height=340, coordinate_mode="logical"),
        regions=(
            Region(
                id="region.header",
                role="stem",
                flow="absolute",
                slot_ids=("slot.qnum", "slot.instruction"),
            ),
            Region(
                id="region.diagram",
                role="diagram",
                flow="absolute",
                slot_ids=("slot.jar_box", "slot.jar_art"),
            ),
            Region(id="region.body", role="stem", flow="absolute", slot_ids="slot.body"),
            Region(id="region.answer", role="answer", flow="absolute", slot_ids=()),
        ),
        slots=(
            TextSlot(
                id="slot.qnum",
                prompt="",
                text="□ 27.",
                style_role="question",
                x=20.0,
                y=38.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.instruction",
                prompt="",
                text="알맞은 단위를 선택하세요.",
                style_role="question",
                x=78.0,
                y=38.0,
                font_size=28,
            ),
            RectSlot(id="slot.jar_box", prompt="", x=92.0, y=70.0, width=150.0, height=120.0),
            TextSlot(
                id="slot.jar_art",
                prompt="",
                text="항아리 그림",
                style_role="diagram",
                x=120.0,
                y=136.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.body",
                prompt="",
                text="항아리의 둘이는 약 24 ( mL , L )입니다.",
                style_role="question",
                x=320.0,
                y=138.0,
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
    "problem_id": "S3_초등_3_008798",
    "problem_type": "unit_selection",
    "metadata": {
        "language": "ko",
        "question": "알맞은 단위를 선택하는 문제",
        "instruction": "알맞은 단위를 선택하세요.",
    },
    "domain": {
        "objects": [
            {"id": "obj.jar", "type": "container", "name": "항아리"},
            {"id": "obj.quantity", "type": "measure_value", "value": 24},
            {"id": "obj.unit_choices", "type": "unit_choices", "choices": ["mL", "L"]},
        ],
        "relations": [],
        "problem_solving": {
            "understand": {
                "given_refs": ["obj.jar", "obj.quantity", "obj.unit_choices"],
                "target_ref": "answer.target",
                "condition_refs": ["rel.select_unit"],
            },
            "plan": {
                "method": "unit_choice",
                "description": "수치와 물체의 크기에 맞는 알맞은 단위를 고른다.",
            },
            "execute": {"expected_operations": ["compare_unit_scale", "select_best_unit"]},
            "review": {"check_methods": ["unit_reasonableness_check"]},
        },
    },
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {"type": "selected_unit", "description": "24에 알맞은 단위"},
        "value": "L",
        "unit": "",
    },
}

SOLVABLE = {
    "schema": "modu.solvable.v1.1",
    "problem_id": "S3_초등_3_008798",
    "problem_type": "unit_selection",
    "inputs": {
        "total_ticks": 0,
        "target_label": "selected_unit",
        "target_ticks": 1,
        "target_count": 1,
        "unit": "",
    },
    "given": [
        {"ref": "obj.quantity", "value": 24},
        {"ref": "obj.unit_choices", "value": ["mL", "L"]},
    ],
    "target": {"ref": "answer.target", "type": "selected_unit"},
    "method": "unit_choice",
    "plan": [
        "수치 24와 항아리의 크기에 맞는 단위를 고른다.",
        "보기 중에서 더 알맞은 단위를 선택한다.",
    ],
    "steps": [
        {"id": "step.1", "expr": "24에 대한 단위 후보를 확인한다.", "value": ["mL", "L"]},
        {"id": "step.2", "expr": "항아리의 크기에 맞는 단위를 선택한다.", "value": "L"},
    ],
    "checks": [
        {
            "id": "check.1",
            "expr": "선택한 단위가 보기 안에 있는가",
            "expected": True,
            "actual": True,
            "pass": True,
        }
    ],
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {"type": "selected_unit", "description": "24에 알맞은 단위"},
        "value": "L",
        "unit": "",
    },
}
