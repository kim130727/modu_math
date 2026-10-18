from __future__ import annotations
from modu_math.dsl import Canvas, ProblemTemplate, RectSlot, Region, TextSlot


def build_problem_template() -> ProblemTemplate:
    return ProblemTemplate(
        id="S3_초등_3_008591",
        title="나머지가 가장 큰 것 찾기",
        canvas=Canvas(width=840, height=320, coordinate_mode="logical"),
        regions=(
            Region(
                id="region.stem",
                role="stem",
                flow="absolute",
                slot_ids=("slot.qtext",),
            ),
            Region(
                id="region.choices",
                role="body",
                flow="absolute",
                slot_ids=(
                    "slot.choice.1.box",
                    "slot.choice.1.text",
                    "slot.choice.2.box",
                    "slot.choice.2.text",
                    "slot.choice.3.box",
                    "slot.choice.3.text",
                ),
            ),
            Region(
                id="region.answer",
                role="answer",
                flow="absolute",
                slot_ids=(),
            ),
        ),
        slots=(
            TextSlot(
                id="slot.qtext",
                prompt="",
                text="나머지가 가장 큰 것을 찾아 선택해보세요.",
                style_role="question",
                x=58.0,
                y=32.0,
                font_size=28,
            ),
            RectSlot(
                id="slot.choice.1.box",
                prompt="",
                x=112.0,
                y=90.0,
                width=182.0,
                height=80.0,
            ),
            TextSlot(
                id="slot.choice.1.text",
                prompt="",
                text = '583 ÷ 5', style_role="body",
                x = 150, y = 140, font_size = 30),
            RectSlot(
                id="slot.choice.2.box",
                prompt="",
                x=369.0,
                y=90.0,
                width=182.0,
                height=80.0,
            ),
            TextSlot(
                id="slot.choice.2.text",
                prompt="",
                text = '584 ÷ 6', style_role="body",
                x = 410, y = 140, font_size = 30),
            RectSlot(
                id="slot.choice.3.box",
                prompt="",
                x=625.0,
                y=90.0,
                width=182.0,
                height=80.0,
            ),
            TextSlot(
                id="slot.choice.3.text",
                prompt="",
                text = '585 ÷ 7', style_role="body",
                x = 670, y = 140, font_size = 30),
            
        ),
        diagrams=(),
        groups=(),
        constraints=(),
        tags=(),
    )


PROBLEM_TEMPLATE = build_problem_template()

SEMANTIC_OVERRIDE = {
    "problem_id": "S3_초등_3_008591",
    "problem_type": "multiple_choice_remainder_comparison",
    "metadata": {
        "language": "ko",
        "question": "나머지가 가장 큰 것을 찾아 선택해보세요.",
        "instruction": "나머지가 가장 큰 것을 찾아 선택하는 문제",
    },
    "domain": {
        "objects": [
            {"id": "obj.div1", "type": "division_expression", "expression": "583 ÷ 5"},
            {"id": "obj.div2", "type": "division_expression", "expression": "584 ÷ 6"},
            {"id": "obj.div3", "type": "division_expression", "expression": "585 ÷ 7"},
        ],
        "relations": [],
        "problem_solving": {
            "understand": {
                "given_refs": ["obj.div1", "obj.div2", "obj.div3"],
                "target_ref": "answer.target",
                "condition_refs": ["rel.compare_remainders"],
            },
            "plan": {
                "method": "compare_remainders",
                "description": "각 나눗셈의 나머지를 비교해 가장 큰 값을 찾는다.",
            },
            "execute": {
                "expected_operations": [
                    "find_remainder_each_expression",
                    "compare_remainders",
                    "select_largest_remainder_expression",
                ]
            },
            "review": {
                "check_methods": ["largest_remainder_check", "choice_consistency_check"]
            },
        },
    },
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {
            "type": "expression_with_largest_remainder",
            "description": "나머지가 가장 큰 나눗셈식",
        },
        "value": "585 ÷ 7",
        "unit": "",
    },
}

SOLVABLE = {
    "schema": "modu.solvable.v1.1",
    "problem_id": "S3_초등_3_008591",
    "problem_type": "multiple_choice_remainder_comparison",
    "inputs": {
        "total_ticks": 3,
        "target_label": "나머지가 가장 큰 것",
        "target_ticks": 1,
        "target_count": 1,
        "unit": "",
    },
    "given": [
        {"ref": "obj.div1", "value": "583 ÷ 5"},
        {"ref": "obj.div2", "value": "584 ÷ 6"},
        {"ref": "obj.div3", "value": "585 ÷ 7"},
    ],
    "target": {"ref": "answer.target", "type": "expression_with_largest_remainder"},
    "method": "compare_remainders",
    "plan": [
        "각 나눗셈의 나머지를 확인한다.",
        "나머지들을 비교하여 가장 큰 식을 고른다.",
    ],
    "steps": [
        {"id": "step.1", "expr": "583 ÷ 5의 나머지", "value": 3},
        {"id": "step.2", "expr": "584 ÷ 6의 나머지", "value": 2},
        {"id": "step.3", "expr": "585 ÷ 7의 나머지", "value": 4},
        {"id": "step.4", "expr": "4 > 3 > 2", "value": "585 ÷ 7"},
    ],
    "checks": [
        {
            "id": "check.1",
            "expr": "가장 큰 나머지인지 확인",
            "expected": 4,
            "actual": 4,
            "pass": True,
        },
        {
            "id": "check.2",
            "expr": "선택한 식이 585 ÷ 7인지 확인",
            "expected": "585 ÷ 7",
            "actual": "585 ÷ 7",
            "pass": True,
        },
    ],
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {
            "type": "expression_with_largest_remainder",
            "description": "나머지가 가장 큰 나눗셈식",
        },
        "value": "585 ÷ 7",
        "unit": "",
    },
}
