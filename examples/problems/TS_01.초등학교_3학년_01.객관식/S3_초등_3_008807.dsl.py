from __future__ import annotations
from modu_math.dsl import Canvas, ProblemTemplate, Region, TextSlot


def build_problem_template() -> ProblemTemplate:
    return ProblemTemplate(
        id="S3_초등_3_008807",
        title="필통의 무게 단위 선택",
        canvas=Canvas(width=943, height=354, coordinate_mode="logical"),
        regions=(
            Region(
                id="region.stem",
                role="stem",
                flow="absolute",
                slot_ids=(
                    "slot.q1",
                    "slot.diagram.scale",
                    "slot.diagram.animal.left",
                    "slot.diagram.animal.center",
                    "slot.diagram.animal.right",
                    "slot.choice",
                ),
            ),
        ),
        slots=(
            TextSlot(
                id="slot.q1",
                prompt="",
                text="□ 36. 필통의 무게를 나타내는 데 알맞은 단위를 선택하세요.",
                style_role="question",
                x=12.0,
                y=28.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.diagram.scale",
                prompt="",
                text="TODO: 저울 삽화",
                style_role="body",
                x=380.0,
                y=88.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.diagram.animal.left",
                prompt="",
                text="TODO: 동물 그림",
                style_role="body",
                x=410.0,
                y=80.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.diagram.animal.center",
                prompt="",
                text="TODO: 동물 그림",
                style_role="body",
                x=468.0,
                y=80.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.diagram.animal.right",
                prompt="",
                text="TODO: 동물 그림",
                style_role="body",
                x=526.0,
                y=80.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.choice",
                prompt="",
                text="( g , kg )",
                style_role="choice",
                x=785.0,
                y=126.0,
                font_size=28,
            ),
        ),
        diagrams=(),
        groups=(),
        constraints=(),
        tags=("무게", "단위", "g", "kg"),
    )


PROBLEM_TEMPLATE = build_problem_template()

SEMANTIC_OVERRIDE = {
    "problem_id": "S3_초등_3_008807",
    "problem_type": "unit_selection",
    "metadata": {
        "language": "ko",
        "question": "필통의 무게를 나타내는 데 알맞은 단위를 선택하세요.",
        "instruction": "무게 단위를 고르기",
    },
    "domain": {
        "objects": [
            {"id": "obj.pen_case", "type": "object", "name": "필통"},
            {"id": "obj.unit_g", "type": "unit", "name": "g"},
            {"id": "obj.unit_kg", "type": "unit", "name": "kg"},
        ],
        "relations": [],
        "problem_solving": {
            "understand": {
                "given_refs": ["obj.pen_case", "obj.unit_g", "obj.unit_kg"],
                "target_ref": "answer.target",
                "condition_refs": ["rel.choose_unit"],
            },
            "plan": {"method": "unit_choice", "description": "물건의 무게에 알맞은 단위를 고른다."},
            "execute": {"expected_operations": ["compare_weight_scale", "select_unit"]},
            "review": {"check_methods": ["compare_with_1kg_threshold"]},
        },
    },
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {"type": "unit", "description": "필통의 무게를 나타내는 단위"},
        "value": 0,
        "unit": "g",
    },
}

SOLVABLE = {
    "schema": "modu.solvable.v1.1",
    "problem_id": "S3_초등_3_008807",
    "problem_type": "unit_selection",
    "inputs": {
        "total_ticks": 0,
        "target_label": "필통의 무게를 나타내는 단위",
        "target_ticks": 0,
        "target_count": 1,
        "unit": "",
    },
    "given": [
        {"ref": "obj.pen_case", "value": {"name": "필통"}},
        {"ref": "obj.unit_g", "value": {"name": "g"}},
        {"ref": "obj.unit_kg", "value": {"name": "kg"}},
    ],
    "target": {"ref": "answer.target", "type": "unit"},
    "method": "unit_choice",
    "plan": [
        "물건의 무게를 나타내기에 알맞은 단위를 고른다.",
        "1 kg보다 가벼운 물건이면 g를 선택한다.",
    ],
    "steps": [
        {"id": "step.1", "expr": "필통의 무게 단위 후보를 확인한다.", "value": ["g", "kg"]},
        {"id": "step.2", "expr": "1 kg보다 가벼운 물건의 단위를 고른다.", "value": "g"},
    ],
    "checks": [
        {
            "id": "check.1",
            "expr": "선택한 단위가 g인지 확인한다.",
            "expected": "g",
            "actual": "g",
            "pass": True,
        }
    ],
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {"type": "unit", "description": "필통의 무게를 나타내는 단위"},
        "value": 0,
        "unit": "g",
    },
}
