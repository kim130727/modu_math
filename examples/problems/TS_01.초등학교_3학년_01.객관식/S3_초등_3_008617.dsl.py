from __future__ import annotations
from modu_math.dsl import Canvas, ProblemTemplate, RectSlot, Region, TextSlot


def build_problem_template() -> ProblemTemplate:
    return ProblemTemplate(
        id="S3_초등_3_008617",
        title="바르게 계산한 것을 찾아 선택하세요",
        canvas=Canvas(width=810, height=376, coordinate_mode="logical"),
        regions=(
            Region(
                id="region.stem", role="stem", flow="absolute", slot_ids=("slot.q1",)
            ),
            Region(
                id="region.choices",
                role="choices",
                flow="absolute",
                slot_ids=(
                    "slot.choice.left.box",
                    "slot.choice.left.text",
                    "slot.choice.right.box",
                    "slot.choice.right.text",
                ),
            ),
            Region(id="region.answer", role="answer", flow="absolute", slot_ids=()),
            Region(
                id="region.explanation",
                role="explanation",
                flow="absolute",
                slot_ids=(),
            ),
        ),
        slots=(
            TextSlot(
                id="slot.q1",
                prompt="",
                text="□ 87. 바르게 계산한 것을 찾아 선택하세요.",
                style_role="question",
                x=10.0,
                y=27.0,
                font_size=28,
            ),
            RectSlot(
                id="slot.choice.left.box",
                prompt="",
                x=162.0,
                y=47.0,
                width=250.0,
                height=72.0,
                fill="#F9E1E1",
                stroke="#FF8FA3",
            ),
            TextSlot(
                id="slot.choice.left.text",
                prompt="",
                text="420 ÷ 5 = 104",
                style_role="choice",
                x=187.0,
                y=92.0,
                font_size=28,
            ),
            RectSlot(
                id="slot.choice.right.box",
                prompt="",
                x=494.0,
                y=47.0,
                width=245.0,
                height=72.0,
                fill="#F9E1E1",
                stroke="#FF8FA3",
            ),
            TextSlot(
                id="slot.choice.right.text",
                prompt="",
                text="420 ÷ 5 = 84",
                style_role="choice",
                x=524.0,
                y=92.0,
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
    "problem_id": "S3_초등_3_008617",
    "problem_type": "multiple_choice_division_correctness",
    "metadata": {
        "language": "ko",
        "question": "바르게 계산한 것을 찾아 선택하세요.",
        "instruction": "420 ÷ 5의 계산 결과를 바르게 고르기",
    },
    "domain": {
        "objects": [
            {"id": "obj.dividend", "type": "number", "value": 420},
            {"id": "obj.divisor", "type": "number", "value": 5},
            {"id": "obj.choice.left", "type": "division_result_choice", "value": 104},
            {"id": "obj.choice.right", "type": "division_result_choice", "value": 84},
        ],
        "relations": [],
        "problem_solving": {
            "understand": {
                "given_refs": [
                    "obj.dividend",
                    "obj.divisor",
                    "obj.choice.left",
                    "obj.choice.right",
                ],
                "target_ref": "answer.target",
                "condition_refs": ["rel.compare_choices"],
            },
            "plan": {
                "method": "division_verification",
                "description": "같은 나눗셈식의 두 결과를 비교하고, 세로셈 해설과 맞는 결과를 찾는다.",
            },
            "execute": {
                "expected_operations": ["compare_choice_results", "match_explanation"]
            },
            "review": {"check_methods": ["consistency_with_explanation"]},
        },
    },
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {
            "type": "correct_division_result",
            "description": "420 ÷ 5의 바른 계산 결과",
        },
        "value": 84,
        "unit": "",
    },
}

SOLVABLE = {
    "schema": "modu.solvable.v1.1",
    "problem_id": "S3_초등_3_008617",
    "problem_type": "multiple_choice_division_correctness",
    "inputs": {
        "total_ticks": 0,
        "target_label": "420 ÷ 5의 바른 계산 결과",
        "target_ticks": 0,
        "target_count": 1,
        "unit": "",
    },
    "given": [
        {"ref": "obj.dividend", "value": 420},
        {"ref": "obj.divisor", "value": 5},
        {"ref": "obj.choice.left", "value": 104},
        {"ref": "obj.choice.right", "value": 84},
    ],
    "target": {"ref": "answer.target", "type": "correct_division_result"},
    "method": "division_verification",
    "plan": [
        "주어진 나눗셈식 420 ÷ 5의 결과와 보기의 결과를 비교한다.",
        "해설의 세로셈과 맞는 결과를 확인한다.",
    ],
    "steps": [
        {"id": "step.1", "expr": "420 ÷ 5", "value": 84},
        {"id": "step.2", "expr": "보기의 결과 104와 비교", "value": False},
        {"id": "step.3", "expr": "보기의 결과 84와 비교", "value": True},
    ],
    "checks": [
        {
            "id": "check.1",
            "expr": "5 × 84 = 420",
            "expected": 420,
            "actual": 420,
            "pass": True,
        },
        {
            "id": "check.2",
            "expr": "5 × 104 = 420",
            "expected": 420,
            "actual": 520,
            "pass": False,
        },
    ],
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {
            "type": "correct_division_result",
            "description": "420 ÷ 5의 바른 계산 결과",
        },
        "value": 84,
        "unit": "",
    },
}
