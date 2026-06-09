from __future__ import annotations
from modu_math.dsl import Canvas, ProblemTemplate, Region, RectSlot, TextSlot


def build_problem_template() -> ProblemTemplate:
    return ProblemTemplate(
        id="S3_초등_3_008603",
        title="나누어떨어지는 나눗셈식",
        canvas=Canvas(width=760, height=330, coordinate_mode="logical"),
        regions=(
            Region(
                id="region.stem",
                role="stem",
                flow="absolute",
                slot_ids=("slot.q1", "slot.box", "slot.v1", "slot.v2"),
            ),
            Region(
                id="region.answer_explanation",
                role="explanation",
                flow="absolute",
                slot_ids=(),
            ),
        ),
        slots=(
            TextSlot(
                id="slot.q1",
                prompt="",
                text = '나누어떨어지는 나눗셈식을 찾아 기호를 선택해 보세요.', style_role="question",
                x = 20, y = 45, font_size = 30),
            RectSlot(
                id="slot.box", prompt="", x = 165, y = 75, width = 380, height = 80),
            TextSlot(
                id="slot.v1",
                prompt="",
                text = '㉠ 64 ÷ 6', style_role="question",
                x = 195, y = 125, font_size = 30),
            TextSlot(
                id="slot.v2",
                prompt="",
                text = '㉡ 92 ÷ 4', style_role="question",
                x = 375, y = 125, font_size = 30),
            
        ),
        diagrams=(),
        groups=(),
        constraints=(),
        tags=("나눗셈", "나누어떨어짐", "기호선택"),
    )


PROBLEM_TEMPLATE = build_problem_template()

SEMANTIC_OVERRIDE = {
    "problem_id": "S3_초등_3_008603",
    "problem_type": "divisibility_choice",
    "metadata": {
        "language": "ko",
        "question": "나누어떨어지는 나눗셈식을 찾아 기호를 선택하는 문제",
        "instruction": "보기 중 나누어떨어지는 나눗셈식을 찾는다.",
    },
    "domain": {
        "objects": [
            {"id": "obj.choice_a", "type": "division_expression", "label": "ㄱ"},
            {"id": "obj.choice_b", "type": "division_expression", "label": "ㄴ"},
        ],
        "relations": [],
        "problem_solving": {
            "understand": {
                "given_refs": ["obj.choice_a", "obj.choice_b"],
                "target_ref": "answer.target",
                "condition_refs": ["rel.compare_divisibility"],
            },
            "plan": {
                "method": "divide_and_check_remainder",
                "description": "각 나눗셈식을 계산해 나머지가 있는지 확인한다.",
            },
            "execute": {
                "expected_operations": [
                    "evaluate_choice_a",
                    "evaluate_choice_b",
                    "compare_remainders",
                ]
            },
            "review": {"check_methods": ["remainder_zero_check", "choice_match_check"]},
        },
    },
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {
            "type": "selection",
            "description": "나누어떨어지는 나눗셈식의 기호",
        },
        "value": 0,
        "unit": "",
    },
}

SOLVABLE = {
    "schema": "modu.solvable.v1.1",
    "problem_id": "S3_초등_3_008603",
    "problem_type": "divisibility_choice",
    "inputs": {
        "total_ticks": 2,
        "target_label": "ㄴ",
        "target_ticks": 1,
        "target_count": 1,
        "unit": "",
    },
    "given": [
        {"ref": "obj.choice_a", "value": {"label": "ㄱ", "dividend": 64, "divisor": 6}},
        {"ref": "obj.choice_b", "value": {"label": "ㄴ", "dividend": 92, "divisor": 4}},
    ],
    "target": {"ref": "answer.target", "type": "selection"},
    "method": "divide_and_check_remainder",
    "plan": [
        "각 보기의 나눗셈을 계산하여 나머지가 있는지 확인한다.",
        "나머지가 없는 기호를 고른다.",
    ],
    "steps": [
        {"id": "step.1", "expr": "64 ÷ 6", "value": "10…4"},
        {"id": "step.2", "expr": "92 ÷ 4", "value": 23},
        {"id": "step.3", "expr": "나머지가 없는 보기 선택", "value": "ㄴ"},
    ],
    "checks": [
        {
            "id": "check.1",
            "expr": "64 ÷ 6의 나머지 확인",
            "expected": "나머지 있음",
            "actual": "나머지 있음",
            "pass": True,
        },
        {
            "id": "check.2",
            "expr": "92 ÷ 4의 나머지 확인",
            "expected": "나머지 없음",
            "actual": "나머지 없음",
            "pass": True,
        },
    ],
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {
            "type": "selection",
            "description": "나누어떨어지는 나눗셈식의 기호",
        },
        "value": 0,
        "unit": "",
    },
}
