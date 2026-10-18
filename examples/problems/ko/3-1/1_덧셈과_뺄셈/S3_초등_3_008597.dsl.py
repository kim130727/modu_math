from __future__ import annotations
from modu_math.dsl import Canvas, ProblemTemplate, Region, RectSlot, TextSlot


def build_problem_template() -> ProblemTemplate:
    return ProblemTemplate(
        id="S3_초등_3_008597",
        title="4로 나누어떨어지는 수가 아닌 것을 모두 고르기",
        canvas=Canvas(width=840, height=334, coordinate_mode="logical"),
        regions=(
            Region(
                id="region.stem",
                role="stem",
                flow="absolute",
                slot_ids=(
                    "slot.question",
                    "slot.choice.1",
                    "slot.choice.2",
                    "slot.choice.3",
                    "slot.choice.4",
                    "slot.choice.5",
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
                id="slot.question",
                prompt="",
                text = '4로 나누어떨어지는 수가 아닌 것을 모두 고르세요.', style_role="question",
                x = 40, y = 55, font_size = 30),
            TextSlot(
                id="slot.choice.1",
                prompt="",
                text = '① 28', style_role="choice",
                x = 40, y = 115, font_size = 30),
            TextSlot(
                id="slot.choice.2",
                prompt="",
                text = '② 56', style_role="choice",
                x = 210, y = 115, font_size = 30),
            TextSlot(
                id="slot.choice.3",
                prompt="",
                text = '③ 84', style_role="choice",
                x = 385, y = 115, font_size = 30),
            TextSlot(
                id="slot.choice.4",
                prompt="",
                text = '④ 62', style_role="choice",
                x = 560, y = 115, font_size = 30),
            TextSlot(
                id="slot.choice.5",
                prompt="",
                text = '⑤ 70', style_role="choice",
                x = 730, y = 115, font_size = 30),
        ),
        diagrams=(),
        groups=(),
        constraints=(),
        tags=(),
    )


PROBLEM_TEMPLATE = build_problem_template()

SEMANTIC_OVERRIDE = {
    "problem_id": "S3_초등_3_008597",
    "problem_type": "multiple_choice_divisibility",
    "metadata": {
        "language": "ko",
        "question": "4로 나누어떨어지는 수가 아닌 것을 모두 고르세요.",
        "instruction": "(정답)과 (해설)이 함께 제시된 객관식 문항",
    },
    "domain": {
        "objects": [
            {"id": "obj.divisor", "type": "number", "value": 4},
            {"id": "obj.choice_1", "type": "number", "value": 28},
            {"id": "obj.choice_2", "type": "number", "value": 56},
            {"id": "obj.choice_3", "type": "number", "value": 84},
            {"id": "obj.choice_4", "type": "number", "value": 62},
            {"id": "obj.choice_5", "type": "number", "value": 70},
        ],
        "relations": [],
        "problem_solving": {
            "understand": {
                "given_refs": [
                    "obj.divisor",
                    "obj.choice_1",
                    "obj.choice_2",
                    "obj.choice_3",
                    "obj.choice_4",
                    "obj.choice_5",
                ],
                "target_ref": "answer.target",
                "condition_refs": ["rel.divisibility_test"],
            },
            "plan": {
                "method": "divisibility_check",
                "description": "각 수가 4로 나누어떨어지는지 확인하여 아닌 보기를 고른다.",
            },
            "execute": {
                "expected_operations": [
                    "check_remainder_by_division",
                    "select_non_divisible_candidates",
                ]
            },
            "review": {
                "check_methods": ["division_result_review", "remainder_presence_check"]
            },
        },
    },
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {
            "type": "multiple_choice_selection",
            "description": "4로 나누어떨어지는 수가 아닌 보기",
        },
        "value": 2,
        "unit": "",
    },
}

SOLVABLE = {
    "schema": "modu.solvable.v1.1",
    "problem_id": "S3_초등_3_008597",
    "problem_type": "multiple_choice_divisibility",
    "inputs": {
        "total_ticks": 5,
        "target_label": "4로 나누어떨어지는 수가 아닌 보기",
        "target_ticks": 2,
        "target_count": 2,
        "unit": "",
    },
    "given": [
        {"ref": "obj.divisor", "value": 4},
        {"ref": "obj.choice_1", "value": 28},
        {"ref": "obj.choice_2", "value": 56},
        {"ref": "obj.choice_3", "value": 84},
        {"ref": "obj.choice_4", "value": 62},
        {"ref": "obj.choice_5", "value": 70},
    ],
    "target": {"ref": "answer.target", "type": "multiple_choice_selection"},
    "method": "divisibility_check",
    "plan": [
        "각 보기의 수를 4로 나누어 나머지가 있는지 확인한다.",
        "나누어떨어지지 않는 보기를 고른다.",
    ],
    "steps": [
        {"id": "step.1", "expr": "28 ÷ 4", "value": 7},
        {"id": "step.2", "expr": "56 ÷ 4", "value": 14},
        {"id": "step.3", "expr": "84 ÷ 4", "value": 21},
        {"id": "step.4", "expr": "62 ÷ 4", "value": "15··2"},
        {"id": "step.5", "expr": "70 ÷ 4", "value": "17··2"},
    ],
    "checks": [
        {
            "id": "check.1",
            "expr": "28 is divisible by 4",
            "expected": True,
            "actual": True,
            "pass": True,
        },
        {
            "id": "check.2",
            "expr": "56 is divisible by 4",
            "expected": True,
            "actual": True,
            "pass": True,
        },
        {
            "id": "check.3",
            "expr": "84 is divisible by 4",
            "expected": True,
            "actual": True,
            "pass": True,
        },
        {
            "id": "check.4",
            "expr": "62 is divisible by 4",
            "expected": False,
            "actual": False,
            "pass": True,
        },
        {
            "id": "check.5",
            "expr": "70 is divisible by 4",
            "expected": False,
            "actual": False,
            "pass": True,
        },
    ],
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {
            "type": "multiple_choice_selection",
            "description": "4로 나누어떨어지는 수가 아닌 보기",
        },
        "value": 2,
        "unit": "",
    },
}
