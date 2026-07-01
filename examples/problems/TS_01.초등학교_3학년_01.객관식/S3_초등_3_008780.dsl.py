from __future__ import annotations
from modu_math.dsl import Canvas, ProblemTemplate, RectSlot, Region, TextSlot


def build_problem_template() -> ProblemTemplate:
    return ProblemTemplate(
        id="S3_초등_3_008780",
        title="계산하여 들이가 더 많은 것의 기호를 선택하세요",
        canvas=Canvas(width=706, height=330, coordinate_mode="logical"),
        regions=(
            Region(
                id="region.stem",
                role="stem",
                flow="absolute",
                slot_ids=("slot.q.text",),
            ),
            Region(
                id="region.choices",
                role="diagram",
                flow="absolute",
                slot_ids=(
                    "slot.choice.box",
                    "slot.choice.a",
                    "slot.choice.b",
                    "slot.choice.a.text",
                    "slot.choice.b.text",
                ),
            ),
            Region(id="region.solution", role="explanation", flow="absolute", slot_ids=()),
        ),
        slots=(
            TextSlot(
                id="slot.q.text",
                prompt="",
                text="계산하여 들이가 더 많은 것의 기호를 선택하세요.",
                style_role="question",
                x=100.0,
                y=29.0,
                font_size=28,
            ),
            RectSlot(
                id="slot.choice.box",
                prompt="",
                x = 170, y = 222, width = 398, height = 100, fill="none",
                stroke = '#F6A24A', stroke_width = 1.5),
            TextSlot(
                id="slot.choice.a",
                prompt="",
                text="①",
                style_role="label",
                x=280.0,
                y=86.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.choice.a.text",
                prompt="",
                text = '①', style_role="question",
                x = 130, y = 111, font_size = 28, fill = '#111111'),
            TextSlot(
                id="slot.choice.b",
                prompt="",
                text="②",
                style_role="label",
                x=280.0,
                y=124.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.choice.b.text",
                prompt="",
                text = '②', style_role="question",
                x = 130, y = 149, font_size = 28, fill = '#111111'),
        ),
        diagrams=(),
        groups=(),
        constraints=(),
        tags=(),
    )


PROBLEM_TEMPLATE = build_problem_template()

SEMANTIC_OVERRIDE = {
    "problem_id": "S3_초등_3_008780",
    "problem_type": "compare_capacity_addition",
    "metadata": {
        "language": "ko",
        "question": "계산하여 들이가 더 많은 것의 기호를 선택하는 문제",
        "instruction": "계산하여 들이가 더 많은 것의 기호를 선택하세요.",
    },
    "domain": {
        "objects": [
            {"id": "obj.choice_a", "type": "expression", "description": "4200 mL + 1400 mL"},
            {"id": "obj.choice_b", "type": "expression", "description": "2 L 800 mL + 3 L 300 mL"},
        ],
        "relations": [],
        "problem_solving": {
            "understand": {
                "given_refs": ["obj.choice_a", "obj.choice_b"],
                "target_ref": "answer.target",
                "condition_refs": ["rel.compare"],
            },
            "plan": {
                "method": "compute_and_compare",
                "description": "각 보기의 들이를 계산한 뒤 더 큰 쪽의 기호를 고른다.",
            },
            "execute": {
                "expected_operations": ["add_capacity_values", "convert_units", "compare_results"]
            },
            "review": {"check_methods": ["compare_final_values", "unit_consistency_check"]},
        },
    },
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {"type": "choice_symbol", "description": "들이가 더 많은 것의 기호"},
        "value": "ㄴ",
        "unit": "",
    },
}

SOLVABLE = {
    "schema": "modu.solvable.v1.1",
    "problem_id": "S3_초등_3_008780",
    "problem_type": "compare_capacity_addition",
    "inputs": {
        "total_ticks": 0,
        "target_label": "들이가 더 많은 것의 기호",
        "target_ticks": 0,
        "target_count": 2,
        "unit": "",
    },
    "given": [
        {"ref": "obj.choice_a", "value": "4200 mL + 1400 mL"},
        {"ref": "obj.choice_b", "value": "2 L 800 mL + 3 L 300 mL"},
    ],
    "target": {"ref": "answer.target", "type": "choice_symbol"},
    "method": "compute_and_compare",
    "plan": ["각 보기의 들이를 계산한 뒤 큰 값을 비교하여 기호를 고른다."],
    "steps": [
        {"id": "step.1", "expr": "4200 + 1400", "value": 5600},
        {"id": "step.2", "expr": "5600 mL = 5 L 600 mL", "value": "5 L 600 mL"},
        {"id": "step.3", "expr": "2 L 800 mL + 3 L 300 mL", "value": "6 L 100 mL"},
        {"id": "step.4", "expr": "5 L 600 mL < 6 L 100 mL", "value": "ㄴ"},
    ],
    "checks": [
        {
            "id": "check.1",
            "expr": "5600 mL = 5 L 600 mL",
            "expected": "5 L 600 mL",
            "actual": "5 L 600 mL",
            "pass": True,
        },
        {
            "id": "check.2",
            "expr": "5 L 600 mL < 6 L 100 mL",
            "expected": "ㄴ",
            "actual": "ㄴ",
            "pass": True,
        },
    ],
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {"type": "choice_symbol", "description": "들이가 더 많은 것의 기호"},
        "value": "ㄴ",
        "unit": "",
    },
}
