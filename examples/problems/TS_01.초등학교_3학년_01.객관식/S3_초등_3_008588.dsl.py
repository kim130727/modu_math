from __future__ import annotations
from modu_math.dsl import Canvas, ProblemTemplate, Region, RectSlot, TextSlot


def build_problem_template() -> ProblemTemplate:
    return ProblemTemplate(
        id="S3_초등_3_008588",
        title="나머지가 4가 될 수 없는 식을 찾아 선택하세요",
        canvas=Canvas(width=904, height=344, coordinate_mode="logical"),
        regions=(
            Region(
                id="region.stem",
                role="stem",
                flow="absolute",
                slot_ids=("slot.q_num", "slot.q_text"),
            ),
            Region(
                id="region.choices",
                role="body",
                flow="absolute",
                slot_ids=(
                    "slot.box",
                    "slot.choice_1_blank",
                    "slot.choice_1_div",
                    "slot.choice_1_num",
                    "slot.choice_2_blank",
                    "slot.choice_2_div",
                    "slot.choice_2_num",
                    "slot.choice_3_blank",
                    "slot.choice_3_div",
                    "slot.choice_3_num",
                    "slot.choice_4_blank",
                    "slot.choice_4_div",
                    "slot.choice_4_num",
                ),
            ),
            Region(
                id="region.answer_explanation",
                role="answer",
                flow="absolute",
                slot_ids=("slot.answer_blank",),
            ),
        ),
        slots=(
            TextSlot(
                id="slot.q_num",
                prompt="",
                text="55.",
                style_role="question",
                x=15.0,
                y=26.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.q_text",
                prompt="",
                text="나머지가 4가 될 수 없는 식을 찾아 선택하세요.",
                style_role="question",
                x=69.0,
                y=26.0,
                font_size=28,
            ),
            RectSlot(
                id="slot.box", prompt="", x=88.0, y=48.0, width=744.0, height=46.0
            ),
            RectSlot(
                id="slot.choice_1_blank",
                prompt="",
                x=161.0,
                y=76.0,
                width=24.0,
                height=26.0,
            ),
            TextSlot(
                id="slot.choice_1_div",
                prompt="",
                text="÷",
                style_role="body",
                x=193.0,
                y=97.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.choice_1_num",
                prompt="",
                text="6",
                style_role="body",
                x=217.0,
                y=97.0,
                font_size=28,
            ),
            RectSlot(
                id="slot.choice_2_blank",
                prompt="",
                x=352.0,
                y=76.0,
                width=24.0,
                height=26.0,
            ),
            TextSlot(
                id="slot.choice_2_div",
                prompt="",
                text="÷",
                style_role="body",
                x=384.0,
                y=97.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.choice_2_num",
                prompt="",
                text="5",
                style_role="body",
                x=408.0,
                y=97.0,
                font_size=28,
            ),
            RectSlot(
                id="slot.choice_3_blank",
                prompt="",
                x=546.0,
                y=76.0,
                width=24.0,
                height=26.0,
            ),
            TextSlot(
                id="slot.choice_3_div",
                prompt="",
                text="÷",
                style_role="body",
                x=578.0,
                y=97.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.choice_3_num",
                prompt="",
                text="9",
                style_role="body",
                x=602.0,
                y=97.0,
                font_size=28,
            ),
            RectSlot(
                id="slot.choice_4_blank",
                prompt="",
                x=739.0,
                y=76.0,
                width=24.0,
                height=26.0,
            ),
            TextSlot(
                id="slot.choice_4_div",
                prompt="",
                text="÷",
                style_role="body",
                x=771.0,
                y=97.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.choice_4_num",
                prompt="",
                text="4",
                style_role="body",
                x=795.0,
                y=97.0,
                font_size=28,
            ),
            RectSlot(
                id="slot.answer_blank",
                prompt="",
                x=56.0,
                y=144.0,
                width=24.0,
                height=26.0,
            ),
        ),
        diagrams=(),
        groups=(),
        constraints=(),
        tags=(),
    )


PROBLEM_TEMPLATE = build_problem_template()

SEMANTIC_OVERRIDE = {
    "problem_id": "S3_초등_3_008588",
    "problem_type": "multiple_choice",
    "metadata": {
        "language": "ko",
        "question": "나머지가 4가 될 수 없는 식을 찾아 선택하세요.",
        "instruction": "보기 중에서 조건에 맞는 식을 고른다.",
    },
    "domain": {
        "objects": [
            {"id": "obj.choice1", "type": "division_expression", "divisor": 6},
            {"id": "obj.choice2", "type": "division_expression", "divisor": 5},
            {"id": "obj.choice3", "type": "division_expression", "divisor": 9},
            {"id": "obj.choice4", "type": "division_expression", "divisor": 4},
        ],
        "relations": [],
        "problem_solving": {
            "understand": {
                "given_refs": [
                    "obj.choice1",
                    "obj.choice2",
                    "obj.choice3",
                    "obj.choice4",
                ],
                "target_ref": "answer.target",
                "condition_refs": ["rel.evaluate_remainder_condition"],
            },
            "plan": {
                "method": "compare_divisors",
                "description": "각 보기의 나누는 수가 나머지 4를 만들 수 있는지 조건을 비교한다.",
            },
            "execute": {
                "expected_operations": [
                    "inspect_divisors",
                    "select_incompatible_expression",
                ]
            },
            "review": {"check_methods": ["answer_matches_prompt_condition"]},
        },
    },
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {
            "type": "select_expression",
            "description": "나머지가 4가 될 수 없는 식",
        },
        "value": 4,
        "unit": "",
    },
}

SOLVABLE = {
    "schema": "modu.solvable.v1.1",
    "problem_id": "S3_초등_3_008588",
    "problem_type": "multiple_choice",
    "inputs": {
        "total_ticks": 4,
        "target_label": "나머지가 4가 될 수 없는 식",
        "target_ticks": 1,
        "target_count": 1,
        "unit": "",
    },
    "given": [
        {"ref": "obj.choice1", "value": {"divisor": 6}},
        {"ref": "obj.choice2", "value": {"divisor": 5}},
        {"ref": "obj.choice3", "value": {"divisor": 9}},
        {"ref": "obj.choice4", "value": {"divisor": 4}},
    ],
    "target": {"ref": "answer.target", "type": "select_expression"},
    "method": "compare_divisors",
    "plan": ["보기의 나누는 수를 비교하여 나머지 4가 될 수 없는 식을 고른다."],
    "steps": [
        {"id": "step.1", "expr": "6은 4보다 큼", "value": True},
        {"id": "step.2", "expr": "5는 4보다 큼", "value": True},
        {"id": "step.3", "expr": "9는 4보다 큼", "value": True},
        {"id": "step.4", "expr": "4는 4보다 작지 않음", "value": True},
    ],
    "checks": [
        {
            "id": "check.1",
            "expr": "보기 중 조건에 맞지 않는 식이 하나인지 확인",
            "expected": 1,
            "actual": 1,
            "pass": True,
        }
    ],
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {
            "type": "select_expression",
            "description": "나머지가 4가 될 수 없는 식",
        },
        "value": 4,
        "unit": "",
    },
}
