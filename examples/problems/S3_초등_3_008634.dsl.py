from __future__ import annotations
from modu_math.dsl import Canvas, ProblemTemplate, Region, TextSlot, RectSlot


def build_problem_template() -> ProblemTemplate:
    return ProblemTemplate(
        id="S3_초등_3_008634",
        title="나머지가 다른 하나를 찾아 기호를 선택해 보세요.",
        canvas=Canvas(width=800, height=400, coordinate_mode="logical"),
        regions=(
            Region(
                id="region.stem",
                role="stem",
                flow="absolute",
                slot_ids=(
                    "slot.q.text",
                    "slot.box",
                    "slot.opt.1",
                    "slot.opt.2",
                    "slot.opt.3",
                    "slot.opt.4",
                    "slot.list",
                ),
            ),
            Region(
                id="region.answer_explanation",
                role="explanation",
                flow="absolute",
                slot_ids=(
                    
                ),
            ),
        ),
        slots=(
            TextSlot(
                id="slot.q.text",
                prompt="",
                text = '나머지가 다른 하나를 찾아 기호를 선택해 보세요.', style_role="question",
                x = 70, y = 50, font_size = 30),
            RectSlot(
                id="slot.box",
                prompt="",
                x = 130, y = 95, width = 430, height = 105, fill="none",
            ),
            TextSlot(
                id="slot.opt.1",
                prompt="",
                text = '① 29 ÷ 7', style_role="body",
                x = 175, y = 140, font_size = 30),
            TextSlot(
                id="slot.opt.2",
                prompt="",
                text = '② 31 ÷ 6', style_role="body",
                x = 385, y = 140, font_size = 30),
            TextSlot(
                id="slot.opt.3",
                prompt="",
                text = '③ 74 ÷ 8', style_role="body",
                x = 175, y = 175, font_size = 30),
            TextSlot(
                id="slot.opt.4",
                prompt="",
                text = '④ 64 ÷ 9', style_role="body",
                x = 385, y = 175, font_size = 30),
            TextSlot(
                id="slot.list",
                prompt="",
                text = '( ① , ② , ③ , ④ )', style_role="body",
                x = 245, y = 260, font_size = 30),
            
        ),
        diagrams=(),
        groups=(),
        constraints=(),
        tags=(),
    )


PROBLEM_TEMPLATE = build_problem_template()

SEMANTIC_OVERRIDE = {
    "problem_id": "S3_초등_3_008634",
    "problem_type": "multiple_choice_division_remainder",
    "metadata": {
        "language": "ko",
        "question": "나머지가 다른 하나를 찾아 기호를 선택해 보세요.",
        "instruction": "보기의 나눗셈 결과를 비교하여 나머지가 다른 하나를 고른다.",
    },
    "domain": {
        "objects": [
            {
                "id": "obj.1",
                "type": "division_expression",
                "dividend": 29,
                "divisor": 7,
            },
            {
                "id": "obj.2",
                "type": "division_expression",
                "dividend": 31,
                "divisor": 6,
            },
            {
                "id": "obj.3",
                "type": "division_expression",
                "dividend": 74,
                "divisor": 8,
            },
            {
                "id": "obj.4",
                "type": "division_expression",
                "dividend": 64,
                "divisor": 9,
            },
            {"id": "obj.choice.1", "type": "choice", "label": "①"},
            {"id": "obj.choice.2", "type": "choice", "label": "②"},
            {"id": "obj.choice.3", "type": "choice", "label": "③"},
            {"id": "obj.choice.4", "type": "choice", "label": "④"},
        ],
        "relations": [],
        "problem_solving": {
            "understand": {
                "given_refs": ["obj.1", "obj.2", "obj.3", "obj.4"],
                "target_ref": "answer.target",
                "condition_refs": ["rel.compare_remainder"],
            },
            "plan": {
                "method": "division_remainder_comparison",
                "description": "각 나눗셈의 나머지를 비교해 다른 나머지를 찾는다.",
            },
            "execute": {
                "expected_operations": [
                    "divide_each_expression",
                    "compare_remainders",
                    "select_different_choice",
                ]
            },
            "review": {
                "check_methods": ["remainder_consistency_check", "choice_match_check"]
            },
        },
    },
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {"type": "choice", "description": "나머지가 다른 하나의 기호"},
        "value": "③ 74 ÷ 8",
        "unit": "",
    },
}

SOLVABLE = {
    "schema": "modu.solvable.v1.1",
    "problem_id": "S3_초등_3_008634",
    "problem_type": "multiple_choice_division_remainder",
    "inputs": {
        "total_ticks": 4,
        "target_label": "나머지가 다른 하나의 기호",
        "target_ticks": 1,
        "target_count": 1,
        "unit": "",
    },
    "given": [
        {"ref": "obj.1", "value": {"dividend": 29, "divisor": 7}},
        {"ref": "obj.2", "value": {"dividend": 31, "divisor": 6}},
        {"ref": "obj.3", "value": {"dividend": 74, "divisor": 8}},
        {"ref": "obj.4", "value": {"dividend": 64, "divisor": 9}},
    ],
    "target": {"ref": "answer.target", "type": "choice"},
    "method": "division_remainder_comparison",
    "plan": [
        "각 보기의 나눗셈을 하고 나머지를 비교한다.",
        "나머지가 다른 보기를 찾는다.",
    ],
    "steps": [
        {"id": "step.1", "expr": "29 ÷ 7", "value": {"quotient": 4, "remainder": 1}},
        {"id": "step.2", "expr": "31 ÷ 6", "value": {"quotient": 5, "remainder": 1}},
        {"id": "step.3", "expr": "74 ÷ 8", "value": {"quotient": 9, "remainder": 2}},
        {"id": "step.4", "expr": "64 ÷ 9", "value": {"quotient": 7, "remainder": 1}},
        {"id": "step.5", "expr": "compare remainders 1, 1, 2, 1", "value": "③"},
    ],
    "checks": [
        {
            "id": "check.1",
            "expr": "remainder_pattern == [1, 1, 2, 1]",
            "expected": [1, 1, 2, 1],
            "actual": [1, 1, 2, 1],
            "pass": True,
        },
        {
            "id": "check.2",
            "expr": "selected_choice == ③",
            "expected": "③",
            "actual": "③",
            "pass": True,
        },
    ],
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {"type": "choice", "description": "나머지가 다른 하나의 기호"},
        "value": "③ 74 ÷ 8",
        "unit": "",
    },
}
