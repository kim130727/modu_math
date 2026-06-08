from __future__ import annotations
from modu_math.dsl import Canvas, ProblemTemplate, Region, RectSlot, TextSlot


def build_problem_template() -> ProblemTemplate:
    return ProblemTemplate(
        id="S3_초등_3_008586",
        title="나누어떨어지는 나눗셈을 찾아 선택하세요.",
        canvas=Canvas(width=692, height=308, coordinate_mode="logical"),
        regions=(
            Region(
                id="region.stem",
                role="stem",
                flow="absolute",
                slot_ids=("slot.question",),
            ),
            Region(
                id="region.choices",
                role="choices",
                flow="absolute",
                slot_ids=("slot.choice_box", "slot.choice.a", "slot.choice.b"),
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
                text = '나누어떨어지는 나눗셈을 찾아 선택하세요.', style_role="question",
                x = 90, y = 40, font_size = 30),
            RectSlot(
                id="slot.choice_box",
                prompt="",
                x = 130, y = 100, width = 385, height = 75),
            TextSlot(
                id="slot.choice.a",
                prompt="",
                text = '㉠ 16 ÷ 3', style_role="choice",
                x = 175, y = 145, font_size = 30),
            TextSlot(
                id="slot.choice.b",
                prompt="",
                text = '㉡ 49 ÷ 7', style_role="choice",
                x = 355, y = 145, font_size = 30),
        ),
        diagrams=(),
        groups=(),
        constraints=(),
        tags=(),
    )


PROBLEM_TEMPLATE = build_problem_template()

SEMANTIC_OVERRIDE = {
    "problem_id": "S3_초등_3_008586",
    "problem_type": "multiple_choice_division",
    "metadata": {
        "language": "ko",
        "question": "나누어떨어지는 나눗셈을 찾아 선택하세요.",
        "instruction": "나누어떨어지는 나눗셈을 찾아 선택하세요.",
    },
    "domain": {
        "objects": [
            {
                "id": "obj.choice_a",
                "type": "division_expression",
                "label": "ㄱ",
                "dividend": 16,
                "divisor": 3,
            },
            {
                "id": "obj.choice_b",
                "type": "division_expression",
                "label": "ㄴ",
                "dividend": 49,
                "divisor": 7,
            },
        ],
        "relations": [],
        "problem_solving": {
            "understand": {
                "given_refs": ["obj.choice_a", "obj.choice_b"],
                "target_ref": "answer.target",
                "condition_refs": ["rel.select_divisible"],
            },
            "plan": {
                "method": "check_remainder",
                "description": "각 나눗셈의 나머지를 보고 나머지가 0인 식을 고른다.",
            },
            "execute": {
                "expected_operations": [
                    "division_check",
                    "remainder_identification",
                    "choice_selection",
                ]
            },
            "review": {"check_methods": ["zero_remainder_check"]},
        },
    },
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {"type": "selected_choice", "description": "나누어떨어지는 나눗셈"},
        "value": "ㄴ",
        "unit": "",
    },
}

SOLVABLE = {
    "schema": "modu.solvable.v1.1",
    "problem_id": "S3_초등_3_008586",
    "problem_type": "multiple_choice_division",
    "inputs": {
        "total_ticks": 0,
        "target_label": "ㄴ",
        "target_ticks": 0,
        "target_count": 1,
        "unit": "",
    },
    "given": [
        {"ref": "obj.choice_a", "value": {"label": "ㄱ", "dividend": 16, "divisor": 3}},
        {"ref": "obj.choice_b", "value": {"label": "ㄴ", "dividend": 49, "divisor": 7}},
    ],
    "target": {"ref": "answer.target", "type": "selected_choice"},
    "method": "check_remainder",
    "plan": ["각 나눗셈의 나머지를 확인한다.", "나머지가 0인 선택지를 고른다."],
    "steps": [
        {"id": "step.1", "expr": "16 ÷ 3", "value": {"quotient": 5, "remainder": 1}},
        {"id": "step.2", "expr": "49 ÷ 7", "value": {"quotient": 7, "remainder": 0}},
        {"id": "step.3", "expr": "나머지가 0인 선택지", "value": "ㄴ"},
    ],
    "checks": [
        {
            "id": "check.1",
            "expr": "16 ÷ 3의 나머지",
            "expected": 1,
            "actual": 1,
            "pass": True,
        },
        {
            "id": "check.2",
            "expr": "49 ÷ 7의 나머지",
            "expected": 0,
            "actual": 0,
            "pass": True,
        },
    ],
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {"type": "selected_choice", "description": "나누어떨어지는 나눗셈"},
        "value": "ㄴ",
        "unit": "",
    },
}
