from __future__ import annotations
from modu_math.dsl import Canvas, ProblemTemplate, RectSlot, Region, TextSlot


def build_problem_template() -> ProblemTemplate:
    return ProblemTemplate(
        id="S3_초등_3_008626",
        title="나머지가 4가 될 수 없는 식",
        canvas=Canvas(width=784.0, height=274.0, coordinate_mode="logical"),
        regions=(
            Region(
                id="region.stem",
                role="stem",
                flow="absolute",
                slot_ids=("slot.icon", "slot.qnum", "slot.question"),
            ),
            Region(
                id="region.options",
                role="choices",
                flow="absolute",
                slot_ids=(
                    "slot.choice.1",
                    "slot.choice.2",
                    "slot.choice.3",
                    "slot.choice.4",
                    "slot.choice.5",
                ),
            ),
            Region(
                id="region.answer_explanation",
                role="explanation",
                flow="absolute",
                slot_ids=(),
            ),
        ),
        slots=(
            RectSlot(id="slot.icon", prompt="", x=8.0, y=19.0, width=13.0, height=13.0),
            TextSlot(
                id="slot.qnum",
                prompt="",
                text="96.",
                style_role="question",
                x=33.0,
                y=29.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.question",
                prompt="",
                text="나머지가 4가 될 수 없는 식은 어느 것일까요?",
                style_role="question",
                x=67.0,
                y=29.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.choice.1",
                prompt="",
                text="① □ ÷ 5",
                style_role="choice",
                x=22.0,
                y=79.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.choice.2",
                prompt="",
                text="② □ ÷ 9",
                style_role="choice",
                x=328.0,
                y=79.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.choice.3",
                prompt="",
                text="③ □ ÷ 4",
                style_role="choice",
                x=645.0,
                y=79.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.choice.4",
                prompt="",
                text="④ □ ÷ 8",
                style_role="choice",
                x=22.0,
                y=122.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.choice.5",
                prompt="",
                text="⑤ □ ÷ 6",
                style_role="choice",
                x=328.0,
                y=122.0,
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
    "problem_id": "S3_초등_3_008626",
    "problem_type": "multiple_choice",
    "metadata": {
        "language": "ko",
        "question": "나머지가 4가 될 수 없는 식은 어느 것일까요?",
        "instruction": "보기에서 나머지가 4가 될 수 없는 식을 고르기",
    },
    "domain": {
        "objects": [
            {"id": "obj.option1", "type": "division_expression", "divisor": 5},
            {"id": "obj.option2", "type": "division_expression", "divisor": 9},
            {"id": "obj.option3", "type": "division_expression", "divisor": 4},
            {"id": "obj.option4", "type": "division_expression", "divisor": 8},
            {"id": "obj.option5", "type": "division_expression", "divisor": 6},
            {
                "id": "obj.remainder_rule",
                "type": "remainder_constraint",
                "divisor": 4,
                "possible_remainders": [0, 1, 2, 3],
            },
        ],
        "relations": [],
        "problem_solving": {
            "understand": {
                "given_refs": [
                    "obj.option1",
                    "obj.option2",
                    "obj.option3",
                    "obj.option4",
                    "obj.option5",
                    "obj.remainder_rule",
                ],
                "target_ref": "answer.target",
                "condition_refs": ["rel.correct_option"],
            },
            "plan": {
                "method": "remainder_range_check",
                "description": "나누는 수가 4일 때 가능한 나머지 범위를 보고 보기 중 해당되지 않는 식을 찾는다.",
            },
            "execute": {
                "expected_operations": [
                    "compare_divisor_to_remainder_rule",
                    "identify_impossible_option",
                ]
            },
            "review": {
                "check_methods": [
                    "remainder_is_less_than_divisor",
                    "option_match_check",
                ]
            },
        },
    },
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {
            "type": "multiple_choice_option",
            "description": "나머지가 4가 될 수 없는 식",
        },
        "value": 3,
        "unit": "",
    },
}

SOLVABLE = {
    "schema": "modu.solvable.v1.1",
    "problem_id": "S3_초등_3_008626",
    "problem_type": "multiple_choice",
    "inputs": {
        "total_ticks": 5,
        "target_label": "정답",
        "target_ticks": 1,
        "target_count": 1,
        "unit": "",
    },
    "given": [
        {"ref": "obj.option1", "value": {"divisor": 5}},
        {"ref": "obj.option2", "value": {"divisor": 9}},
        {"ref": "obj.option3", "value": {"divisor": 4}},
        {"ref": "obj.option4", "value": {"divisor": 8}},
        {"ref": "obj.option5", "value": {"divisor": 6}},
    ],
    "target": {"ref": "answer.target", "type": "multiple_choice_option"},
    "method": "remainder_range_check",
    "plan": [
        "나누는 수가 4일 때 가능한 나머지는 0, 1, 2, 3이다.",
        "보기 중 나누는 수가 4인 식이 나머지 4가 될 수 없는지 확인한다.",
    ],
    "steps": [
        {"id": "step.1", "expr": "4의 나머지 가능 범위", "value": [0, 1, 2, 3]},
        {"id": "step.2", "expr": "보기 ③의 나누는 수", "value": 4},
        {"id": "step.3", "expr": "나머지 4가 가능한지 여부", "value": False},
        {"id": "step.4", "expr": "정답 보기", "value": 3},
    ],
    "checks": [
        {
            "id": "check.1",
            "expr": "4로 나눌 때 나머지는 4보다 작아야 한다",
            "expected": True,
            "actual": True,
            "pass": True,
        },
        {
            "id": "check.2",
            "expr": "정답이 ③인지 확인",
            "expected": 3,
            "actual": 3,
            "pass": True,
        },
    ],
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {
            "type": "multiple_choice_option",
            "description": "나머지가 4가 될 수 없는 식",
        },
        "value": 3,
        "unit": "",
    },
}
