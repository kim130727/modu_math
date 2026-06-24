from __future__ import annotations
from modu_math.dsl import Canvas, ProblemTemplate, Region, RectSlot, TextSlot


def build_problem_template() -> ProblemTemplate:
    return ProblemTemplate(
        id="S3_초등_3_008973",
        title="계산 결과가 가장 큰 것을 찾아 기호를 선택해 보세요.",
        canvas=Canvas(width=496, height=203, coordinate_mode="logical"),
        regions=(
            Region(
                id="region.stem",
                role="stem",
                flow="absolute",
                slot_ids=("slot.q1", "slot.box", "slot.eq1", "slot.eq2", "slot.eq3", "slot.choice"),
            ),
        ),
        slots=(
            TextSlot(
                id="slot.q1",
                prompt="",
                text="7. 계산 결과가 가장 큰 것을 찾아 기호를 선택해 보세요.",
                style_role="question",
                x=18.0,
                y=20.0,
                font_size=28,
            ),
            RectSlot(id="slot.box", prompt="", x=110.0, y=25.0, width=375.0, height=32.0),
            TextSlot(
                id="slot.eq1",
                prompt="",
                text="① 201 + 339",
                style_role="body",
                x=145.0,
                y=44.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.eq2",
                prompt="",
                text="② 622 - 115",
                style_role="body",
                x=268.0,
                y=44.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.eq3",
                prompt="",
                text="③ 746 - 228",
                style_role="body",
                x=390.0,
                y=44.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.choice",
                prompt="",
                text="( ① , ② , ③ )",
                style_role="body",
                x=195.0,
                y=74.0,
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
    "problem_id": "S3_초등_3_008973",
    "problem_type": "comparison_of_calculations",
    "metadata": {
        "language": "ko",
        "question": "계산 결과가 가장 큰 것을 찾아 기호를 선택하는 문제",
        "instruction": "계산 결과가 가장 큰 것을 찾아 기호를 선택해 보세요.",
    },
    "domain": {
        "objects": [
            {
                "id": "obj.calc1",
                "type": "arithmetic_expression",
                "expression": "201 + 339",
                "label": "①",
            },
            {
                "id": "obj.calc2",
                "type": "arithmetic_expression",
                "expression": "622 - 115",
                "label": "②",
            },
            {
                "id": "obj.calc3",
                "type": "arithmetic_expression",
                "expression": "746 - 228",
                "label": "③",
            },
        ],
        "relations": [],
        "problem_solving": {
            "understand": {
                "given_refs": ["obj.calc1", "obj.calc2", "obj.calc3"],
                "target_ref": "answer.target",
                "condition_refs": ["rel.compare_results"],
            },
            "plan": {
                "method": "compute_and_compare",
                "description": "각 식의 계산 결과를 구한 뒤 가장 큰 값을 찾는다.",
            },
            "execute": {
                "expected_operations": [
                    "calculate_expression",
                    "compare_values",
                    "select_largest_symbol",
                ]
            },
            "review": {"check_methods": ["result_comparison_check"]},
        },
    },
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {"type": "symbol_with_largest_result", "description": "계산 결과가 가장 큰 기호"},
        "value": 1,
        "unit": "",
    },
}

SOLVABLE = {
    "schema": "modu.solvable.v1.1",
    "problem_id": "S3_초등_3_008973",
    "problem_type": "comparison_of_calculations",
    "inputs": {
        "total_ticks": 3,
        "target_label": "①",
        "target_ticks": 1,
        "target_count": 1,
        "unit": "",
    },
    "given": [
        {"ref": "obj.calc1", "value": {"expression": "201 + 339"}},
        {"ref": "obj.calc2", "value": {"expression": "622 - 115"}},
        {"ref": "obj.calc3", "value": {"expression": "746 - 228"}},
    ],
    "target": {"ref": "answer.target", "type": "symbol_with_largest_result"},
    "plan": "각 식의 값을 구해 비교한 뒤 가장 큰 기호를 찾는다.",
    "steps": [
        {"id": "step.1", "expr": "201 + 339", "value": 540},
        {"id": "step.2", "expr": "622 - 115", "value": 507},
        {"id": "step.3", "expr": "746 - 228", "value": 518},
        {"id": "step.4", "expr": "540 > 518 > 507", "value": 540},
    ],
    "checks": [
        {
            "id": "check.1",
            "expr": "max(540, 507, 518)",
            "expected": 540,
            "actual": 540,
            "pass": True,
        },
        {"id": "check.2", "expr": "largest_symbol", "expected": "①", "actual": "①", "pass": True},
    ],
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {"type": "symbol_with_largest_result", "description": "계산 결과가 가장 큰 기호"},
        "value": 1,
        "unit": "",
    },
}
