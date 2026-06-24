from __future__ import annotations
from modu_math.dsl import Canvas, CircleSlot, LineSlot, ProblemTemplate, RectSlot, Region, TextSlot


def build_problem_template() -> ProblemTemplate:
    return ProblemTemplate(
        id="S3_초등_3_008794",
        title="알맞은 단위를 선택하세요",
        canvas=Canvas(width=720, height=300, coordinate_mode="logical"),
        regions=(
            Region(id="region.stem", role="stem", flow="absolute", slot_ids=("slot.q_title",)),
            Region(
                id="region.diagram",
                role="diagram",
                flow="absolute",
                slot_ids=(
                    "slot.syringe_barrel",
                    "slot.syringe_plunger",
                    "slot.syringe_tip",
                    "slot.syringe_tick1",
                    "slot.syringe_tick2",
                    "slot.syringe_tick3",
                    "slot.syringe_tick4",
                    "slot.syringe_tick5",
                    "slot.syringe_tick6",
                    "slot.choice_box",
                    "slot.choice_divider",
                    "slot.choice_ml",
                    "slot.choice_l",
                ),
            ),
            Region(id="region.answer", role="answer", flow="absolute", slot_ids=()),
        ),
        slots=(
            TextSlot(
                id="slot.q_title",
                prompt="",
                text="□ 19. 알맞은 단위를 선택하세요.",
                style_role="question",
                x=12.0,
                y=28.0,
                font_size=28,
            ),
            RectSlot(id="slot.syringe_barrel", prompt="", x=438.0, y=48.0, width=90.0, height=18.0),
            RectSlot(id="slot.syringe_plunger", prompt="", x=420.0, y=54.0, width=26.0, height=8.0),
            RectSlot(id="slot.syringe_tip", prompt="", x=520.0, y=51.0, width=22.0, height=6.0),
            LineSlot(id="slot.syringe_tick1", prompt="", x1=455.0, y1=56.0, x2=455.0, y2=64.0),
            LineSlot(id="slot.syringe_tick2", prompt="", x1=465.0, y1=56.0, x2=465.0, y2=64.0),
            LineSlot(id="slot.syringe_tick3", prompt="", x1=475.0, y1=56.0, x2=475.0, y2=64.0),
            LineSlot(id="slot.syringe_tick4", prompt="", x1=485.0, y1=56.0, x2=485.0, y2=64.0),
            LineSlot(id="slot.syringe_tick5", prompt="", x1=495.0, y1=56.0, x2=495.0, y2=64.0),
            LineSlot(id="slot.syringe_tick6", prompt="", x1=505.0, y1=56.0, x2=505.0, y2=64.0),
            RectSlot(id="slot.choice_box", prompt="", x=275.0, y=103.0, width=360.0, height=66.0),
            LineSlot(id="slot.choice_divider", prompt="", x1=455.0, y1=103.0, x2=455.0, y2=169.0),
            TextSlot(
                id="slot.choice_ml",
                prompt="",
                text="mL",
                style_role="label",
                x=345.0,
                y=145.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.choice_l",
                prompt="",
                text="L",
                style_role="label",
                x=560.0,
                y=145.0,
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
    "problem_id": "S3_초등_3_008794",
    "problem_type": "unit_selection",
    "metadata": {
        "language": "ko",
        "question": "알맞은 단위를 선택하세요.",
        "instruction": "그림을 보고 알맞은 들이 단위를 고른다.",
    },
    "domain": {
        "objects": [
            {"id": "obj.syringe", "type": "container", "name": "주사기"},
            {"id": "obj.unit_ml", "type": "unit", "name": "mL"},
            {"id": "obj.unit_l", "type": "unit", "name": "L"},
        ],
        "relations": [],
        "problem_solving": {
            "understand": {
                "given_refs": ["obj.syringe", "obj.unit_ml", "obj.unit_l"],
                "target_ref": "answer.target",
                "condition_refs": ["rel.measure_unit"],
            },
            "plan": {
                "method": "unit_selection",
                "description": "그림의 대상에 알맞은 들이 단위를 고른다.",
            },
            "execute": {"expected_operations": ["compare_units", "select_appropriate_unit"]},
            "review": {"check_methods": ["unit_fit_check"]},
        },
    },
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {"type": "selected_unit", "description": "주사기에 알맞은 단위"},
        "value": "mL",
        "unit": "",
    },
}

SOLVABLE = {
    "schema": "modu.solvable.v1.1",
    "problem_id": "S3_초등_3_008794",
    "problem_type": "unit_selection",
    "inputs": {
        "total_ticks": 0,
        "target_label": "주사기에 알맞은 단위",
        "target_ticks": 0,
        "target_count": 1,
        "unit": "",
    },
    "given": [
        {"ref": "obj.syringe", "value": {"name": "주사기"}},
        {"ref": "obj.unit_ml", "value": {"name": "mL"}},
        {"ref": "obj.unit_l", "value": {"name": "L"}},
    ],
    "target": {"ref": "answer.target", "type": "selected_unit"},
    "method": "unit_selection",
    "plan": ["그림을 보고 주사기에 맞는 들이 단위를 고른다."],
    "steps": [
        {
            "id": "step.1",
            "expr": "주사기의 들이 단위 후보는 mL, L이다.",
            "value": {"candidates": ["mL", "L"]},
        },
        {"id": "step.2", "expr": "주사기에 알맞은 단위를 선택한다.", "value": "mL"},
    ],
    "checks": [
        {
            "id": "check.1",
            "expr": "선택한 단위가 주사기의 들이 단위와 일치하는지 확인",
            "expected": "mL",
            "actual": "mL",
            "pass": True,
        }
    ],
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {"type": "selected_unit", "description": "주사기에 알맞은 단위"},
        "value": "mL",
        "unit": "",
    },
}
