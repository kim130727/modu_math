from __future__ import annotations
from modu_math.dsl import Canvas, ProblemTemplate, Region, RectSlot, TextSlot


def build_problem_template() -> ProblemTemplate:
    return ProblemTemplate(
        id="S3_초등_3_008770",
        title="무게를 알맞게 어림한 것을 찾아 선택하세요",
        canvas=Canvas(width=926, height=428, coordinate_mode="logical"),
        regions=(
            Region(id="region.stem", role="stem", flow="absolute", slot_ids=("slot.q1", "slot.q2")),
            Region(
                id="region.box",
                role="diagram",
                flow="absolute",
                slot_ids=("slot.box.frame", "slot.cat", "slot.choice"),
            ),
            Region(id="region.ans", role="answer", flow="absolute", slot_ids=()),
        ),
        slots=(
            TextSlot(
                id="slot.q1",
                prompt="",
                text="□ 72.",
                style_role="question",
                x=10.0,
                y=26.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.q2",
                prompt="",
                text="무게를 알맞게 어림한 것을 찾아 선택하세요.",
                style_role="question",
                x=82.0,
                y=26.0,
                font_size=28,
            ),
            RectSlot(
                id="slot.box.frame",
                prompt="",
                x=280.0,
                y=57.0,
                width=374.0,
                height=209.0,
                fill="none",
            ),
            TextSlot(
                id="slot.cat",
                prompt="",
                text="",
                style_role="diagram",
                x=462.0,
                y=120.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.choice",
                prompt="",
                text="약 ( 3 g , 3 kg , 3 t )",
                style_role="question",
                x=391.0,
                y=212.0,
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
    "problem_id": "S3_초등_3_008770",
    "problem_type": "weight_estimation_choice",
    "metadata": {
        "language": "ko",
        "question": "무게를 알맞게 어림한 것을 찾아 선택하세요.",
        "instruction": "무게를 알맞게 어림한 것을 찾아 선택하세요.",
    },
    "domain": {
        "objects": [
            {"id": "obj.cat", "type": "animal", "name": "고양이"},
            {"id": "obj.choice_1", "type": "mass_unit_choice", "value": "3 g"},
            {"id": "obj.choice_2", "type": "mass_unit_choice", "value": "3 kg"},
            {"id": "obj.choice_3", "type": "mass_unit_choice", "value": "3 t"},
        ],
        "relations": [],
        "problem_solving": {
            "understand": {
                "given_refs": ["obj.cat", "obj.choice_1", "obj.choice_2", "obj.choice_3"],
                "target_ref": "answer.target",
                "condition_refs": ["rel.estimate_by_mass_sense"],
            },
            "plan": {
                "method": "mass_sense_comparison",
                "description": "고양이에 알맞지 않은 단위와 수를 제외하고 가장 자연스러운 무게를 고른다.",
            },
            "execute": {
                "expected_operations": ["compare_choices_by_reasonableness", "select_best_estimate"]
            },
            "review": {"check_methods": ["unit_reasonableness_check"]},
        },
    },
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {"type": "selected_choice", "description": "무게를 알맞게 어림한 것"},
        "value": 3,
        "unit": "kg",
    },
}

SOLVABLE = {
    "schema": "modu.solvable.v1.1",
    "problem_id": "S3_초등_3_008770",
    "problem_type": "weight_estimation_choice",
    "inputs": {
        "total_ticks": 0,
        "target_label": "무게를 알맞게 어림한 것",
        "target_ticks": 0,
        "target_count": 1,
        "unit": "kg",
    },
    "given": [
        {"ref": "obj.cat", "value": {"name": "고양이"}},
        {"ref": "obj.choice_1", "value": "3 g"},
        {"ref": "obj.choice_2", "value": "3 kg"},
        {"ref": "obj.choice_3", "value": "3 t"},
    ],
    "target": {"ref": "answer.target", "type": "selected_choice"},
    "plan": [
        "고양이의 무게에 비해 너무 가볍거나 너무 무거운 선택지를 제외한다.",
        "가장 알맞은 무게를 고른다.",
    ],
    "method": "mass_sense_comparison",
    "steps": [
        {
            "id": "step.1",
            "expr": "3 g, 3 kg, 3 t 중 고양이에 알맞은 무게를 비교한다",
            "value": "비교",
        },
        {"id": "step.2", "expr": "고양이에는 3 g은 너무 가볍고 3 t은 너무 무겁다", "value": "제외"},
        {"id": "step.3", "expr": "남는 알맞은 선택지는 3 kg이다", "value": "3 kg"},
    ],
    "checks": [
        {
            "id": "check.1",
            "expr": "3 kg가 고양이의 무게로 자연스러운가",
            "expected": True,
            "actual": True,
            "pass": True,
        }
    ],
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {"type": "selected_choice", "description": "무게를 알맞게 어림한 것"},
        "value": 3,
        "unit": "kg",
    },
}
