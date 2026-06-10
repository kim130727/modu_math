from __future__ import annotations
from modu_math.dsl import Canvas, ProblemTemplate, Region, RectSlot, TextSlot


def build_problem_template() -> ProblemTemplate:
    return ProblemTemplate(
        id="S3_초등_3_008628",
        title="나머지가 가장 큰 것",
        canvas=Canvas(width=944, height=376, coordinate_mode="logical"),
        regions=(
            Region(
                id="region.header",
                role="stem",
                flow="absolute",
                slot_ids=("slot.stem",),
            ),
            Region(
                id="region.choice_box",
                role="diagram",
                flow="absolute",
                slot_ids=(
                    "slot.box",
                    "slot.choice.a",
                    "slot.choice.b",
                    "slot.choice.c",
                    
                ),
            ),
            Region(
                id="region.choice_list",
                role="diagram",
                flow="absolute",
                slot_ids=("slot.choice_list",),
            ),
            Region(
                id="region.answer_explanation",
                role="solution",
                flow="absolute",
                slot_ids=(),
            ),
        ),
        slots=(
            TextSlot(
                id="slot.stem",
                prompt="",
                text="나머지가 가장 큰 것을 찾는 기호를 선택하세요.",
                style_role="question",
                x=84.0,
                y=22.0,
                font_size=28,
            ),
            RectSlot(
                id="slot.box", prompt="", x = 85, y = 45, width = 610, height = 75),
            TextSlot(
                id="slot.choice.a",
                prompt="",
                text = '㉠ 583 ÷ 5', style_role="question",
                x = 115, y = 95, font_size = 30),
            TextSlot(
                id="slot.choice.b",
                prompt="",
                text = '㉡ 584 ÷ 6', style_role="question",
                x = 325, y = 95, font_size = 30),
            TextSlot(
                id="slot.choice.c",
                prompt="",
                text = '㉢ 585 ÷ 7', style_role="question",
                x = 530, y = 95, font_size = 30),
            TextSlot(
                id="slot.choice_list",
                prompt="",
                text = '( ㄱ , ㄴ , ㄷ )', style_role="label",
                x = 95, y = 180, font_size = 30),
        ),
        diagrams=(),
        groups=(),
        constraints=(),
        tags=(),
    )


PROBLEM_TEMPLATE = build_problem_template()

SEMANTIC_OVERRIDE = {
    "problem_id": "S3_초등_3_008628",
    "problem_type": "remainder_comparison",
    "metadata": {
        "language": "ko",
        "question": "나머지가 가장 큰 것을 찾는 기호를 선택하는 문제",
        "instruction": "나머지가 가장 큰 것을 찾는 기호를 선택하세요.",
    },
    "domain": {
        "objects": [
            {
                "id": "obj.choice.a",
                "type": "division_expression",
                "symbol": "ㄱ",
                "dividend": 583,
                "divisor": 5,
            },
            {
                "id": "obj.choice.b",
                "type": "division_expression",
                "symbol": "ㄴ",
                "dividend": 584,
                "divisor": 6,
            },
            {
                "id": "obj.choice.c",
                "type": "division_expression",
                "symbol": "ㄷ",
                "dividend": 585,
                "divisor": 7,
            },
        ],
        "relations": [],
        "problem_solving": {
            "understand": {
                "given_refs": ["obj.choice.a", "obj.choice.b", "obj.choice.c"],
                "target_ref": "answer.target",
                "condition_refs": ["rel.compare_remainder"],
            },
            "plan": {
                "method": "compare_remainders",
                "description": "각 나눗셈의 나머지를 비교하여 가장 큰 기호를 찾는다.",
            },
            "execute": {
                "expected_operations": [
                    "divide_and_find_remainder",
                    "compare_remainders",
                ]
            },
            "review": {"check_methods": ["remainder_comparison_check"]},
        },
    },
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {
            "type": "symbol_selection",
            "description": "나머지가 가장 큰 보기의 기호",
        },
        "value": "ㄷ",
        "unit": "",
    },
}

SOLVABLE = {
    "schema": "modu.solvable.v1.1",
    "problem_id": "S3_초등_3_008628",
    "problem_type": "remainder_comparison",
    "inputs": {
        "total_ticks": 3,
        "target_label": "나머지가 가장 큰 것",
        "target_ticks": 1,
        "target_count": 3,
        "unit": "",
    },
    "given": [
        {
            "ref": "obj.choice.a",
            "value": {"symbol": "ㄱ", "dividend": 583, "divisor": 5},
        },
        {
            "ref": "obj.choice.b",
            "value": {"symbol": "ㄴ", "dividend": 584, "divisor": 6},
        },
        {
            "ref": "obj.choice.c",
            "value": {"symbol": "ㄷ", "dividend": 585, "divisor": 7},
        },
    ],
    "target": {"ref": "answer.target", "type": "symbol_selection"},
    "method": "compare_remainders",
    "plan": [
        "각 나눗셈의 나머지를 확인한다.",
        "나머지들을 비교하여 가장 큰 기호를 고른다.",
    ],
    "steps": [
        {"id": "step.1", "expr": "583 ÷ 5 = 116···3", "value": 3},
        {"id": "step.2", "expr": "584 ÷ 6 = 97···2", "value": 2},
        {"id": "step.3", "expr": "585 ÷ 7 = 83···4", "value": 4},
        {"id": "step.4", "expr": "3, 2, 4 중 가장 큰 나머지 선택", "value": "ㄷ"},
    ],
    "checks": [
        {
            "id": "check.1",
            "expr": "3 < 4 and 2 < 4",
            "expected": True,
            "actual": True,
            "pass": True,
        }
    ],
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {
            "type": "symbol_selection",
            "description": "나머지가 가장 큰 보기의 기호",
        },
        "value": "ㄷ",
        "unit": "",
    },
}
