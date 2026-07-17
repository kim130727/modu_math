from __future__ import annotations
from modu_math.dsl import Canvas, ProblemTemplate, Region, RectSlot, TextSlot, ImageSlot


def build_problem_template() -> ProblemTemplate:
    return ProblemTemplate(
        id="S3_초등_3_008770",
        title="무게를 알맞게 어림한 것을 찾아 선택하세요",
        canvas=Canvas(width=690, height=330, coordinate_mode="logical"),
        regions=(
            Region(
                id="region.stem",
                role="stem",
                flow="absolute",
                slot_ids=("slot.q2", "slot.q2.copy2", "slot.inserted.image.1"),
            ),
            Region(
                id="region.box",
                role="diagram",
                flow="absolute",
                slot_ids=("slot.cat",),
            ),
            Region(id="region.ans", role="answer", flow="absolute", slot_ids=()),
        ),
        slots=(
            TextSlot(
                id="slot.q2",
                prompt="",
                text="무게를 알맞게 어림한 것을 찾아 선택하세요.",
                style_role="question",
                x=97,
                y=36,
                font_size=28,
                fill="#111111",
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
                id="slot.q2.copy2",
                prompt="",
                text="약 (3g, 3kg, 3t)",
                x=252,
                y=276,
                font_size=28,
                fill="#111111",
            ),
            ImageSlot(
                id="slot.inserted.image.1",
                prompt="",
                href="data:image/png;base64,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",
                x=250,
                y=75,
                width=180,
                height=145,
                preserve_aspect_ratio="xMidYMid meet",
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
