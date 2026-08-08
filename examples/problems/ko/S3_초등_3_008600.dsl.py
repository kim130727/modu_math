from __future__ import annotations
from modu_math.dsl import Canvas, ProblemTemplate, Region, RectSlot, TextSlot


def build_problem_template() -> ProblemTemplate:
    return ProblemTemplate(
        id="S3_초등_3_008600",
        title="몫이 다른 나눗셈식을 찾아 기호를 선택해 보세요.",
        canvas=Canvas(width=880, height=366, coordinate_mode="logical"),
        regions=(
            Region(
                id="region.stem",
                role="stem",
                flow="absolute",
                slot_ids=(
                    "slot.question",
                    "slot.choice_box",
                    "slot.choice.a",
                    "slot.choice.b",
                    "slot.choice.c",
                ),
            ),
            Region(id="region.answer", role="answer", flow="absolute", slot_ids=()),
        ),
        slots=(
            TextSlot(
                id="slot.question",
                prompt="",
                text="몫이 다른 나눗셈식을 찾아 기호를 선택해 보세요.",
                style_role="question",
                x=61.997,
                y=65,
                font_size=30,
                fill="#111111",
            ),
            RectSlot(
                id="slot.choice_box",
                prompt="",
                x=146.024,
                y=151,
                width=617.958,
                height=80,
                fill="#ffffff",
                stroke="#111111",
                stroke_width=1.5,
            ),
            TextSlot(
                id="slot.choice.a",
                prompt="",
                text="① 39 ÷ 5",
                style_role="question",
                x=206.004,
                y=196,
                font_size=30,
                fill="#111111",
            ),
            TextSlot(
                id="slot.choice.b",
                prompt="",
                text="② 45 ÷ 6",
                style_role="question",
                x=406.004,
                y=196,
                font_size=30,
                fill="#111111",
            ),
            TextSlot(
                id="slot.choice.c",
                prompt="",
                text="③ 62 ÷ 9",
                style_role="question",
                x=596.004,
                y=196,
                font_size=30,
                fill="#111111",
            ),
        ),
        diagrams=(),
        groups=(),
        constraints=(),
        tags=(),
    )


PROBLEM_TEMPLATE = build_problem_template()

SEMANTIC_OVERRIDE = {
    "problem_id": "S3_초등_3_008600",
    "problem_type": "multiple_choice_division",
    "metadata": {
        "language": "ko",
        "question": "몫이 다른 나눗셈식을 찾아 기호를 선택해 보세요.",
        "instruction": "보기 중 몫이 다른 나눗셈식을 고르기",
    },
    "domain": {
        "objects": [
            {
                "id": "obj.choice.a",
                "type": "division_expression",
                "label": "①",
                "dividend": 39,
                "divisor": 5,
            },
            {
                "id": "obj.choice.b",
                "type": "division_expression",
                "label": "②",
                "dividend": 45,
                "divisor": 6,
            },
            {
                "id": "obj.choice.c",
                "type": "division_expression",
                "label": "③",
                "dividend": 62,
                "divisor": 9,
            },
        ],
        "relations": [],
        "problem_solving": {
            "understand": {
                "given_refs": ["obj.choice.a", "obj.choice.b", "obj.choice.c"],
                "target_ref": "answer.target",
                "condition_refs": ["rel.compare_quotients"],
            },
            "plan": {
                "method": "compare_division_results",
                "description": "각 나눗셈식의 몫을 비교하여 다른 것을 고른다.",
            },
            "execute": {
                "expected_operations": [
                    "read_each_division_expression",
                    "compare_quotients",
                    "select_distinct_choice",
                ]
            },
            "review": {
                "check_methods": [
                    "answer_matches_printed_mark",
                    "choice_consistency_check",
                ]
            },
        },
    },
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {"type": "choice_symbol", "description": "몫이 다른 나눗셈식의 기호"},
        "value": "③",
        "unit": "",
    },
}

SOLVABLE = {
    "schema": "modu.solvable.v1.1",
    "problem_id": "S3_초등_3_008600",
    "problem_type": "multiple_choice_division",
    "inputs": {
        "total_ticks": 3,
        "target_label": "몫이 다른 나눗셈식의 기호",
        "target_ticks": 1,
        "target_count": 3,
        "unit": "",
    },
    "given": [
        {"ref": "obj.choice.a", "value": {"dividend": 39, "divisor": 5}},
        {"ref": "obj.choice.b", "value": {"dividend": 45, "divisor": 6}},
        {"ref": "obj.choice.c", "value": {"dividend": 62, "divisor": 9}},
    ],
    "target": {"ref": "answer.target", "type": "choice_symbol"},
    "method": "compare_division_results",
    "plan": ["각 나눗셈식의 몫을 비교해서 다른 보기의 기호를 찾는다."],
    "steps": [
        {"id": "step.1", "expr": "39 ÷ 5", "value": {"quotient": 7, "remainder": 4}},
        {"id": "step.2", "expr": "45 ÷ 6", "value": {"quotient": 7, "remainder": 3}},
        {"id": "step.3", "expr": "62 ÷ 9", "value": {"quotient": 6, "remainder": 8}},
    ],
    "checks": [
        {
            "id": "check.1",
            "expr": "몫 비교",
            "expected": {"a": 7, "b": 7, "c": 6},
            "actual": {"a": 7, "b": 7, "c": 6},
            "pass": True,
        },
        {
            "id": "check.2",
            "expr": "정답 기호 일치",
            "expected": "③",
            "actual": "③",
            "pass": True,
        },
    ],
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {"type": "choice_symbol", "description": "몫이 다른 나눗셈식의 기호"},
        "value": "③",
        "unit": "",
    },
}
