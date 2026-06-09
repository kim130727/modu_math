from __future__ import annotations
from modu_math.dsl import Canvas, ProblemTemplate, Region, RectSlot, TextSlot


def build_problem_template() -> ProblemTemplate:
    return ProblemTemplate(
        id="S3_초등_3_008592",
        title="나머지가 5가 될 수 없는 식",
        canvas=Canvas(width=936, height=276, coordinate_mode="logical"),
        regions=(
            Region(
                id="region.header",
                role="stem",
                flow="absolute",
                slot_ids=("slot.question",),
            ),
            Region(
                id="region.choices",
                role="body",
                flow="absolute",
                slot_ids=(
                    "slot.choice.1.no",
                    "slot.choice.1.box",
                    "slot.choice.1.div",
                    "slot.choice.1.den",
                    "slot.choice.2.no",
                    "slot.choice.2.box",
                    "slot.choice.2.div",
                    "slot.choice.2.den",
                    "slot.choice.3.no",
                    "slot.choice.3.box",
                    "slot.choice.3.div",
                    "slot.choice.3.den",
                    "slot.choice.4.no",
                    "slot.choice.4.box",
                    "slot.choice.4.div",
                    "slot.choice.4.den",
                    "slot.choice.5.no",
                    "slot.choice.5.box",
                    "slot.choice.5.div",
                    "slot.choice.5.den",
                ),
            ),
            Region(
                id="region.footer",
                role="answer_explanation",
                flow="absolute",
                slot_ids=(),
            ),
        ),
        slots=(
            TextSlot(
                id="slot.question",
                prompt="",
                text = '나머지가 5가 될 수 없는 식을 모두 고르세요.', style_role="question",
                x = 75, y = 40, font_size = 30),
            TextSlot(
                id="slot.choice.1.no",
                prompt="",
                text = '①', style_role="question",
                x = 535, y = 160, font_size = 30),
            RectSlot(
                id="slot.choice.1.box",
                prompt="",
                x = 95, y = 85, width = 25, height = 25),
            TextSlot(
                id="slot.choice.1.div",
                prompt="",
                text = '÷', style_role="question",
                x = 170, y = 105, font_size = 30),
            TextSlot(
                id="slot.choice.1.den",
                prompt="",
                text="5",
                style_role="question",
                x=104.0,
                y=78.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.choice.2.no",
                prompt="",
                text = '②', style_role="question",
                x = 290, y = 90, font_size = 30),
            RectSlot(
                id="slot.choice.2.box",
                prompt="",
                x=341.0,
                y=60.0,
                width=24.0,
                height=24.0,
            ),
            TextSlot(
                id="slot.choice.2.div",
                prompt="",
                text="÷",
                style_role="question",
                x=373.0,
                y=78.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.choice.2.den",
                prompt="",
                text="4",
                style_role="question",
                x=400.0,
                y=78.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.choice.3.no",
                prompt="",
                text = '③', style_role="question",
                x = 490, y = 90, font_size = 30),
            RectSlot(
                id="slot.choice.3.box",
                prompt="",
                x=631.0,
                y=60.0,
                width=24.0,
                height=24.0,
            ),
            TextSlot(
                id="slot.choice.3.div",
                prompt="",
                text="÷",
                style_role="question",
                x=663.0,
                y=78.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.choice.3.den",
                prompt="",
                text="8",
                style_role="question",
                x=690.0,
                y=78.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.choice.4.no",
                prompt="",
                text = '④', style_role="question",
                x = 415, y = 175, font_size = 30),
            RectSlot(
                id="slot.choice.4.box",
                prompt="",
                x = 130, y = 160, width = 25, height = 25),
            TextSlot(
                id="slot.choice.4.div",
                prompt="",
                text = '÷', style_role="question",
                x = 170, y = 150, font_size = 30),
            TextSlot(
                id="slot.choice.4.den",
                prompt="",
                text="7",
                style_role="question",
                x=104.0,
                y=122.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.choice.5.no",
                prompt="",
                text="⑤",
                style_role="question",
                x = 295, y = 175, font_size = 30),
            RectSlot(
                id="slot.choice.5.box",
                prompt="",
                x = 345, y = 155, width = 25, height = 25),
            TextSlot(
                id="slot.choice.5.div",
                prompt="",
                text="÷",
                style_role="question",
                x=373.0,
                y=122.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.choice.5.den",
                prompt="",
                text="6",
                style_role="question",
                x=400.0,
                y=122.0,
                font_size=28,
            ),
        ),
        diagrams=(),
        groups=(),
        constraints=(),
        tags=("초등수학", "나눗셈", "나머지", "객관식"),
    )


PROBLEM_TEMPLATE = build_problem_template()

SEMANTIC_OVERRIDE = {
    "problem_id": "S3_초등_3_008592",
    "problem_type": "division_remainder_selection",
    "metadata": {
        "language": "ko",
        "question": "나머지가 5가 될 수 없는 식을 모두 고르세요.",
        "instruction": "보기 중 나머지가 5가 될 수 없는 식을 고르기.",
    },
    "domain": {
        "objects": [
            {"id": "obj.choice_1", "type": "division_expression", "divisor": 5},
            {"id": "obj.choice_2", "type": "division_expression", "divisor": 4},
            {"id": "obj.choice_3", "type": "division_expression", "divisor": 8},
            {"id": "obj.choice_4", "type": "division_expression", "divisor": 7},
            {"id": "obj.choice_5", "type": "division_expression", "divisor": 6},
        ],
        "relations": [],
        "problem_solving": {
            "understand": {
                "given_refs": [
                    "obj.choice_1",
                    "obj.choice_2",
                    "obj.choice_3",
                    "obj.choice_4",
                    "obj.choice_5",
                ],
                "target_ref": "answer.target",
                "condition_refs": ["rel.remainder_constraint"],
            },
            "plan": {
                "method": "compare_divisor_to_five",
                "description": "나머지는 나누는 수보다 작다는 성질을 이용해 나머지 5가 가능한지 확인한다.",
            },
            "execute": {
                "expected_operations": [
                    "compare_each_divisor_with_five",
                    "select_divisors_less_than_or_equal_to_five",
                ]
            },
            "review": {
                "check_methods": [
                    "remainder_less_than_divisor_check",
                    "answer_choice_consistency_check",
                ]
            },
        },
    },
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {"type": "selection", "description": "나머지가 5가 될 수 없는 식"},
        "value": 2,
        "unit": "",
    },
}

SOLVABLE = {
    "schema": "modu.solvable.v1.1",
    "problem_id": "S3_초등_3_008592",
    "problem_type": "division_remainder_selection",
    "inputs": {
        "total_ticks": 5,
        "target_label": "나머지가 5가 될 수 없는 식",
        "target_ticks": 2,
        "target_count": 2,
        "unit": "",
    },
    "given": [
        {"ref": "obj.choice_1", "value": {"divisor": 5}},
        {"ref": "obj.choice_2", "value": {"divisor": 4}},
        {"ref": "obj.choice_3", "value": {"divisor": 8}},
        {"ref": "obj.choice_4", "value": {"divisor": 7}},
        {"ref": "obj.choice_5", "value": {"divisor": 6}},
    ],
    "target": {"ref": "answer.target", "type": "selection"},
    "method": "compare_divisor_to_five",
    "plan": [
        "나머지는 나누는 수보다 작아야 한다.",
        "각 보기의 나누는 수가 5 이하인지 확인한다.",
        "5 이하이면 나머지가 5가 될 수 없다고 판단한다.",
    ],
    "steps": [
        {"id": "step.1", "expr": "5 <= 5", "value": True},
        {"id": "step.2", "expr": "4 <= 5", "value": True},
        {"id": "step.3", "expr": "8 <= 5", "value": False},
        {"id": "step.4", "expr": "7 <= 5", "value": False},
        {"id": "step.5", "expr": "6 <= 5", "value": False},
        {"id": "step.6", "expr": "선택할 보기 번호", "value": [1, 2]},
    ],
    "checks": [
        {
            "id": "check.1",
            "expr": "나머지는 나누는 수보다 작아야 한다",
            "expected": True,
            "actual": True,
            "pass": True,
        },
        {
            "id": "check.2",
            "expr": "선택된 보기 번호가 1, 2인가",
            "expected": [1, 2],
            "actual": [1, 2],
            "pass": True,
        },
    ],
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {"type": "selection", "description": "나머지가 5가 될 수 없는 식"},
        "value": 2,
        "unit": "",
    },
}
