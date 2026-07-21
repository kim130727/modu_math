from __future__ import annotations
from modu_math.dsl import Canvas, ProblemTemplate, RectSlot, Region, TextSlot


def build_problem_template() -> ProblemTemplate:
    return ProblemTemplate(
        id="S3_초등_3_008601",
        title="나머지가 3이 될 수 없는 나눗셈식",
        canvas=Canvas(width=960, height=380, coordinate_mode="logical"),
        regions=(
            Region(
                id="region.stem",
                role="stem",
                flow="absolute",
                slot_ids=("slot.q_text",),
            ),
            Region(
                id="region.options",
                role="body",
                flow="absolute",
                slot_ids=(
                    "slot.box",
                    "slot.opt1.sym",
                    "slot.opt1.blank",
                    "slot.opt1.div",
                    "slot.opt1.num",
                    "slot.opt2.sym",
                    "slot.opt2.blank",
                    "slot.opt2.div",
                    "slot.opt2.num",
                    "slot.opt3.sym",
                    "slot.opt3.blank",
                    "slot.opt3.div",
                    "slot.opt3.num",
                ),
            ),
            Region(id="region.answer", role="answer", flow="absolute", slot_ids=()),
        ),
        slots=(
            TextSlot(
                id="slot.q_text",
                prompt="",
                text = '나머지가 3이 될 수 없는 나눗셈식을 찾아 기호를 선택해 보세요.', style_role="question",
                x = 75, y = 50, font_size = 30),
            RectSlot(
                id="slot.box",
                prompt="",
                x = 75, y = 95, width = 760, height = 80, fill="none",
            ),
            TextSlot(
                id="slot.opt1.sym",
                prompt="",
                text = '㉠', style_role="body",
                x = 165, y = 150, font_size = 30),
            RectSlot(
                id="slot.opt1.blank",
                prompt="",
                x = 210, y = 125, width = 25, height = 25, fill="none",
            ),
            TextSlot(
                id="slot.opt1.div",
                prompt="",
                text = '÷', style_role="body",
                x = 245, y = 150, font_size = 30),
            TextSlot(
                id="slot.opt1.num",
                prompt="",
                text="2",
                style_role="body",
                x=285.0,
                y=150.0,
                font_size=30,
            ),
            TextSlot(
                id="slot.opt2.sym",
                prompt="",
                text = '㉡', style_role="body",
                x = 380, y = 150, font_size = 30),
            RectSlot(
                id="slot.opt2.blank",
                prompt="",
                x = 425, y = 125, width = 25, height = 25, fill="none",
            ),
            TextSlot(
                id="slot.opt2.div",
                prompt="",
                text = '÷', style_role="body",
                x = 455, y = 150, font_size = 30),
            TextSlot(
                id="slot.opt2.num",
                prompt="",
                text="7",
                style_role="body",
                x=490.0,
                y=150.0,
                font_size=30,
            ),
            TextSlot(
                id="slot.opt3.sym",
                prompt="",
                text = '㉢', style_role="body",
                x = 585, y = 150, font_size = 30),
            RectSlot(
                id="slot.opt3.blank",
                prompt="",
                x = 635, y = 125, width = 25, height = 25, fill="none",
            ),
            TextSlot(
                id="slot.opt3.div",
                prompt="",
                text = '÷', style_role="body",
                x = 670, y = 150, font_size = 30),
            TextSlot(
                id="slot.opt3.num",
                prompt="",
                text="5",
                style_role="body",
                x=705.0,
                y=150.0,
                font_size=30,
            ),
        ),
        diagrams=(),
        groups=(),
        constraints=(),
        tags=(),
    )


PROBLEM_TEMPLATE = build_problem_template()

SEMANTIC_OVERRIDE = {
    "problem_id": "S3_초등_3_008601",
    "problem_type": "multiple_choice_division_remainder",
    "metadata": {
        "language": "ko",
        "question": "나머지가 3이 될 수 없는 나눗셈식을 찾아 기호를 선택해 보세요.",
        "instruction": "기호를 선택하시오.",
    },
    "domain": {
        "objects": [
            {
                "id": "obj.choice_1",
                "type": "division_expression_choice",
                "label": "㉠",
                "divisor": 2,
            },
            {
                "id": "obj.choice_2",
                "type": "division_expression_choice",
                "label": "㉡",
                "divisor": 7,
            },
            {
                "id": "obj.choice_3",
                "type": "division_expression_choice",
                "label": "㉢",
                "divisor": 5,
            },
        ],
        "relations": [],
        "problem_solving": {
            "understand": {
                "given_refs": [
                    "obj.choice_1",
                    "obj.choice_2",
                    "obj.choice_3",
                    "rel.remainder_constraint",
                ],
                "target_ref": "answer.target",
                "condition_refs": ["rel.answer_choice"],
            },
            "plan": {
                "method": "remainder_comparison",
                "description": "각 나눗셈식에서 나머지가 3이 가능한지 나누는 수와 비교해 판단한다.",
            },
            "execute": {
                "expected_operations": [
                    "compare_remainder_with_divisor",
                    "select_impossible_case",
                ]
            },
            "review": {"check_methods": ["remainder_less_than_divisor_check"]},
        },
    },
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {
            "type": "selected_symbol",
            "description": "나머지가 3이 될 수 없는 나눗셈식의 기호",
        },
        "value": "㉠",
        "unit": "",
    },
}

SOLVABLE = {
    "schema": "modu.solvable.v1.1",
    "problem_id": "S3_초등_3_008601",
    "problem_type": "multiple_choice_division_remainder",
    "inputs": {
        "total_ticks": 3,
        "target_label": "㉠",
        "target_ticks": 1,
        "target_count": 1,
        "unit": "",
    },
    "given": [
        {"ref": "obj.choice_1", "value": {"label": "㉠", "divisor": 2}},
        {"ref": "obj.choice_2", "value": {"label": "㉡", "divisor": 7}},
        {"ref": "obj.choice_3", "value": {"label": "㉢", "divisor": 5}},
    ],
    "target": {"ref": "answer.target", "type": "selected_symbol"},
    "method": "remainder_comparison",
    "plan": [
        "나머지는 나누는 수보다 작아야 하는 성질을 확인한다.",
        "각 선택지의 나누는 수와 3을 비교해 나머지 3이 가능한지 판단한다.",
        "가능하지 않은 선택지를 고른다.",
    ],
    "steps": [
        {"id": "step.1", "expr": "3 < 2", "value": False},
        {"id": "step.2", "expr": "3 < 7", "value": True},
        {"id": "step.3", "expr": "3 < 5", "value": True},
        {"id": "step.4", "expr": "나머지가 3이 될 수 없는 선택지 = ㉠", "value": "㉠"},
    ],
    "checks": [
        {
            "id": "check.1",
            "expr": "나머지 < 나누는 수",
            "expected": True,
            "actual": True,
            "pass": True,
        },
        {
            "id": "check.2",
            "expr": "선택지 ㉠의 나누는 수는 2이므로 나머지 3은 불가능",
            "expected": True,
            "actual": True,
            "pass": True,
        },
    ],
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {
            "type": "selected_symbol",
            "description": "나머지가 3이 될 수 없는 나눗셈식의 기호",
        },
        "value": "㉠",
        "unit": "",
    },
}
