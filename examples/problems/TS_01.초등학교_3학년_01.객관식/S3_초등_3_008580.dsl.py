from __future__ import annotations
from modu_math.dsl import Canvas, ProblemTemplate, Region, RectSlot, TextSlot


def build_problem_template() -> ProblemTemplate:
    return ProblemTemplate(
        id="S3_초등_3_008580",
        title="계산한 값이 옳지 않은 것을 고르세요",
        canvas=Canvas(width=680, height=360, coordinate_mode="logical"),
        regions=(
            Region(
                id="region.stem",
                role="stem",
                flow="absolute",
                slot_ids=("slot.box", "slot.num", "slot.question"),
            ),
            Region(
                id="region.options",
                role="options",
                flow="absolute",
                slot_ids=(
                    "slot.opt1",
                    "slot.opt2",
                    "slot.opt3",
                    "slot.opt4",
                    "slot.opt5",
                ),
            ),
            Region(id="region.answer", role="answer", flow="absolute", slot_ids=()),
        ),
        slots=(
            RectSlot(id="slot.box", prompt="", x=8.0, y=8.0, width=12.0, height=12.0),
            TextSlot(
                id="slot.num",
                prompt="",
                text="46.",
                style_role="question",
                x=28.0,
                y=20.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.question",
                prompt="",
                text="계산한 값이 옳지 않은 것을 고르세요.",
                style_role="question",
                x=66.0,
                y=20.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.opt1",
                prompt="",
                text="① 30 × 20 = 600",
                style_role="question",
                x=30.0,
                y=72.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.opt2",
                prompt="",
                text="② 21 × 20 = 420",
                style_role="question",
                x=455.0,
                y=72.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.opt3",
                prompt="",
                text="③ 24 × 80 = 1820",
                style_role="question",
                x=30.0,
                y=122.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.opt4",
                prompt="",
                text="④ 20 × 60 = 1200",
                style_role="question",
                x=455.0,
                y=122.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.opt5",
                prompt="",
                text="⑤ 42 × 30 = 1260",
                style_role="question",
                x=30.0,
                y=172.0,
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
    "problem_id": "S3_초등_3_008580",
    "problem_type": "multiple_choice",
    "metadata": {
        "language": "ko",
        "question": "계산한 값이 옳지 않은 것을 고르세요.",
        "instruction": "옳지 않은 계산식을 고르기",
    },
    "domain": {
        "objects": [
            {
                "id": "obj.option1",
                "type": "multiplication_statement",
                "expression": "30 × 20 = 600",
            },
            {
                "id": "obj.option2",
                "type": "multiplication_statement",
                "expression": "21 × 20 = 420",
            },
            {
                "id": "obj.option3",
                "type": "multiplication_statement",
                "expression": "24 × 80 = 1820",
            },
            {
                "id": "obj.option4",
                "type": "multiplication_statement",
                "expression": "20 × 60 = 1200",
            },
            {
                "id": "obj.option5",
                "type": "multiplication_statement",
                "expression": "42 × 30 = 1260",
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
                ],
                "target_ref": "answer.target",
                "condition_refs": ["rel.choose_incorrect"],
            },
            "plan": {
                "method": "compare_multiplication_statements",
                "description": "각 보기의 곱셈식과 결과값이 맞는지 비교한다.",
            },
            "execute": {
                "expected_operations": [
                    "compare_each_statement",
                    "find_incorrect_statement",
                ]
            },
            "review": {"check_methods": ["statement_result_consistency"]},
        },
    },
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {
            "type": "incorrect_choice",
            "description": "계산한 값이 옳지 않은 보기",
        },
        "value": 3,
        "unit": "",
    },
}

SOLVABLE = {
    "schema": "modu.solvable.v1.1",
    "problem_id": "S3_초등_3_008580",
    "problem_type": "multiple_choice",
    "inputs": {
        "total_ticks": 5,
        "target_label": "옳지 않은 보기",
        "target_ticks": 1,
        "target_count": 1,
        "unit": "",
    },
    "given": [
        {"ref": "obj.option1", "value": "30 × 20 = 600"},
        {"ref": "obj.option2", "value": "21 × 20 = 420"},
        {"ref": "obj.option3", "value": "24 × 80 = 1820"},
        {"ref": "obj.option4", "value": "20 × 60 = 1200"},
        {"ref": "obj.option5", "value": "42 × 30 = 1260"},
    ],
    "target": {"ref": "answer.target", "type": "incorrect_choice"},
    "method": "compare_multiplication_statements",
    "plan": ["각 보기의 곱셈식과 결과값을 비교한다.", "옳지 않은 계산식을 찾는다."],
    "steps": [
        {"id": "step.1", "expr": "30 × 20 = 600", "value": True},
        {"id": "step.2", "expr": "21 × 20 = 420", "value": True},
        {"id": "step.3", "expr": "24 × 80 = 1820", "value": False},
        {"id": "step.4", "expr": "20 × 60 = 1200", "value": True},
        {"id": "step.5", "expr": "42 × 30 = 1260", "value": True},
    ],
    "checks": [
        {
            "id": "check.1",
            "expr": "incorrect_choice_is_option_3",
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
            "type": "incorrect_choice",
            "description": "계산한 값이 옳지 않은 보기",
        },
        "value": 3,
        "unit": "",
    },
}
