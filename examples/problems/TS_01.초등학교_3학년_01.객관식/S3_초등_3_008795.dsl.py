from __future__ import annotations
from modu_math.dsl import Canvas, ProblemTemplate, RectSlot, Region, TextSlot


def build_problem_template() -> ProblemTemplate:
    return ProblemTemplate(
        id="S3_초등_3_008795",
        title="알맞은 단위를 선택하세요",
        canvas=Canvas(width=702, height=352, coordinate_mode="logical"),
        regions=(
            Region(
                id="region.stem",
                role="stem",
                flow="absolute",
                slot_ids=(
                    "slot.q1",
                    "slot.q2",
                    "slot.bathtub",
                    "slot.choice_box",
                    "slot.choice.ml",
                    "slot.choice.l",
                ),
            ),
            Region(id="region.answer_note", role="note", flow="absolute", slot_ids=()),
        ),
        slots=(
            TextSlot(
                id="slot.q1",
                prompt="",
                text="20.",
                style_role="question",
                x=18.0,
                y=30.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.q2",
                prompt="",
                text="알맞은 단위를 선택하세요.",
                style_role="question",
                x=56.0,
                y=30.0,
                font_size=28,
            ),
            RectSlot(id="slot.bathtub", prompt="", x=332.0, y=52.0, width=275.0, height=66.0),
            RectSlot(id="slot.choice_box", prompt="", x=306.0, y=151.0, width=375.0, height=74.0),
            TextSlot(
                id="slot.choice.ml",
                prompt="",
                text="mL",
                style_role="label",
                x=360.0,
                y=199.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.choice.l",
                prompt="",
                text="L",
                style_role="label",
                x=555.0,
                y=199.0,
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
    "problem_id": "S3_초등_3_008795",
    "problem_type": "단위선택",
    "metadata": {
        "language": "ko",
        "question": "그림을 보고 알맞은 들이 단위를 선택하는 문제",
        "instruction": "알맞은 단위를 선택하세요.",
    },
    "domain": {
        "objects": [
            {"id": "obj.bathtub", "type": "container", "name": "욕조", "quantity_kind": "volume"},
            {"id": "obj.unit_ml", "type": "unit", "name": "mL"},
            {"id": "obj.unit_l", "type": "unit", "name": "L"},
        ],
        "relations": [],
        "problem_solving": {
            "understand": {
                "given_refs": ["obj.bathtub", "obj.unit_ml", "obj.unit_l"],
                "target_ref": "answer.target",
                "condition_refs": ["rel.choose_unit"],
            },
            "plan": {
                "method": "생활용기-단위판단",
                "description": "그림의 크기와 용도에 맞는 들이 단위를 고른다.",
            },
            "execute": {
                "expected_operations": ["그림의 용도 판단", "단위 후보 비교", "알맞은 단위 선택"]
            },
            "review": {"check_methods": ["생활용기의 들이 단위 확인"]},
        },
    },
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {"type": "unit_choice", "description": "욕조의 알맞은 들이 단위"},
        "value": "L",
        "unit": "",
    },
}

SOLVABLE = {
    "schema": "modu.solvable.v1.1",
    "problem_id": "S3_초등_3_008795",
    "problem_type": "단위선택",
    "inputs": {
        "total_ticks": 2,
        "target_label": "욕조의 들이 단위",
        "target_ticks": 1,
        "target_count": 1,
        "unit": "",
    },
    "given": [
        {"ref": "obj.bathtub", "value": {"name": "욕조", "quantity_kind": "volume"}},
        {"ref": "obj.unit_ml", "value": {"name": "mL"}},
        {"ref": "obj.unit_l", "value": {"name": "L"}},
    ],
    "target": {"ref": "answer.target", "type": "unit_choice"},
    "method": "생활용기-단위판단",
    "plan": [
        "그림이 나타내는 물건이 큰 용량의 생활용기인지 살핀다.",
        "보기의 두 단위 mL와 L 중 더 알맞은 들이 단위를 고른다.",
    ],
    "steps": [
        {"id": "step.1", "expr": "욕조는 큰 용량의 생활용기이다.", "value": "욕조"},
        {"id": "step.2", "expr": "큰 용량의 들이 단위는 L이다.", "value": "L"},
    ],
    "checks": [
        {
            "id": "check.1",
            "expr": "욕조에 맞는 들이 단위를 고르는가",
            "expected": "L",
            "actual": "L",
            "pass": True,
        }
    ],
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {"type": "unit_choice", "description": "욕조의 알맞은 들이 단위"},
        "value": "L",
        "unit": "",
    },
}
