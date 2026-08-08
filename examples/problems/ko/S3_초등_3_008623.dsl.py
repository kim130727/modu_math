from __future__ import annotations
from modu_math.dsl import (
    Canvas,
    ProblemTemplate,
    Region,
    TextSlot,
    CircleSlot,
    LineSlot,
)


def build_problem_template() -> ProblemTemplate:
    return ProblemTemplate(
        id="S3_초등_3_008623",
        title="나누어떨어지는 나눗셈",
        canvas=Canvas(width=760, height=460, coordinate_mode="logical"),
        regions=(
            Region(
                id="region.stem",
                role="stem",
                flow="absolute",
                slot_ids=("slot.question",),
            ),
            Region(
                id="region.options",
                role="diagram",
                flow="absolute",
                slot_ids=(
                    "slot.opt1.num",
                    "slot.opt1.text",
                    "slot.opt2.num",
                    "slot.opt2.text",
                    "slot.opt3.num",
                    "slot.opt3.text",
                    "slot.opt4.num",
                    "slot.opt4.text",
                    "slot.opt5.num",
                    "slot.opt5.text",
                ),
            ),
            Region(id="region.answer", role="answer", flow="absolute", slot_ids=()),
            Region(
                id="region.explanation",
                role="explanation",
                flow="absolute",
                slot_ids=(),
            ),
            Region(
                id="region.footer",
                role="footer",
                flow="absolute",
                slot_ids=(),
            ),
        ),
        slots=(
            TextSlot(
                id="slot.question",
                prompt="",
                text = '나누어떨어지는 나눗셈은 어느 것일까요?', style_role="question",
                x = 20, y = 55, font_size = 30),
            TextSlot(
                id="slot.opt1.text",
                prompt="",
                text = '① 11 ÷ 2', style_role="label",
                x = 30, y = 115, font_size = 30),
            TextSlot(
                id="slot.opt2.text",
                prompt="",
                text = '② 27 ÷ 3', style_role="label",
                x = 210, y = 115, font_size = 30),
            TextSlot(
                id="slot.opt3.text",
                prompt="",
                text = '③ 35 ÷ 6', style_role="label",
                x = 385, y = 115, font_size = 30),
            TextSlot(
                id="slot.opt4.text",
                prompt="",
                text = '④ 42 ÷ 5', style_role="label",
                x = 30, y = 170, font_size = 30),
            TextSlot(
                id="slot.opt5.text",
                prompt="",
                text = '⑤ 66 ÷ 7', style_role="label",
                x = 210, y = 170, font_size = 30),
            
        ),
        diagrams=(),
        groups=(),
        constraints=(),
        tags=(),
    )


PROBLEM_TEMPLATE = build_problem_template()

SEMANTIC_OVERRIDE = {
    "problem_id": "S3_초등_3_008623",
    "problem_type": "multiple_choice_division",
    "metadata": {
        "language": "ko",
        "question": "나누어떨어지는 나눗셈은 어느 것일까요?",
        "instruction": "보기 중 나머지 없이 나누어떨어지는 식을 고른다.",
    },
    "domain": {
        "objects": [
            {"id": "obj.opt1", "type": "division_expression", "expression": "11 ÷ 2"},
            {"id": "obj.opt2", "type": "division_expression", "expression": "27 ÷ 3"},
            {"id": "obj.opt3", "type": "division_expression", "expression": "35 ÷ 6"},
            {"id": "obj.opt4", "type": "division_expression", "expression": "42 ÷ 5"},
            {"id": "obj.opt5", "type": "division_expression", "expression": "66 ÷ 7"},
            {"id": "obj.answer_choice", "type": "choice_label", "label": "②"},
        ],
        "relations": [],
        "problem_solving": {
            "understand": {
                "given_refs": [
                    "obj.opt1",
                    "obj.opt2",
                    "obj.opt3",
                    "obj.opt4",
                    "obj.opt5",
                ],
                "target_ref": "answer.target",
                "condition_refs": ["rel.select_divisible"],
            },
            "plan": {
                "method": "divisibility_check",
                "description": "각 나눗셈의 나머지 유무를 비교해 나머지 없이 끝나는 보기를 찾는다.",
            },
            "execute": {
                "expected_operations": [
                    "compare_remainders",
                    "identify_no_remainder_choice",
                ]
            },
            "review": {
                "check_methods": ["choice_consistency_check", "expression_match_check"]
            },
        },
    },
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {"type": "divisible_choice", "description": "나누어떨어지는 나눗셈"},
        "value": 2,
        "unit": "",
    },
}

SOLVABLE = {
    "schema": "modu.solvable.v1.1",
    "problem_id": "S3_초등_3_008623",
    "problem_type": "multiple_choice_division",
    "inputs": {
        "total_ticks": 5,
        "target_label": "②",
        "target_ticks": 1,
        "target_count": 1,
        "unit": "",
    },
    "given": [
        {"ref": "obj.opt1", "value": {"expression": "11 ÷ 2"}},
        {"ref": "obj.opt2", "value": {"expression": "27 ÷ 3"}},
        {"ref": "obj.opt3", "value": {"expression": "35 ÷ 6"}},
        {"ref": "obj.opt4", "value": {"expression": "42 ÷ 5"}},
        {"ref": "obj.opt5", "value": {"expression": "66 ÷ 7"}},
    ],
    "target": {"ref": "answer.target", "type": "divisible_choice"},
    "method": "divisibility_check",
    "plan": ["각 보기의 나눗셈 결과를 확인한다.", "나머지가 0인 보기를 찾는다."],
    "steps": [
        {"id": "step.1", "expr": "11 ÷ 2", "value": "5···1"},
        {"id": "step.2", "expr": "27 ÷ 3", "value": "9"},
        {"id": "step.3", "expr": "35 ÷ 6", "value": "5···5"},
        {"id": "step.4", "expr": "42 ÷ 5", "value": "8···2"},
        {"id": "step.5", "expr": "66 ÷ 7", "value": "9···3"},
        {"id": "step.6", "expr": "나머지가 0인 보기 선택", "value": "②"},
    ],
    "checks": [
        {
            "id": "check.1",
            "expr": "27 ÷ 3 는 나머지가 없다",
            "expected": True,
            "actual": True,
            "pass": True,
        }
    ],
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {"type": "divisible_choice", "description": "나누어떨어지는 나눗셈"},
        "value": 2,
        "unit": "",
    },
}
