from __future__ import annotations
from modu_math.dsl import Canvas, ProblemTemplate, RectSlot, Region, TextSlot


def build_problem_template() -> ProblemTemplate:
    return ProblemTemplate(
        id="S3_초등_3_008602",
        title="나머지가 가장 작은 것을 찾아 기호를 선택하세요.",
        canvas=Canvas(width=860.0, height=360.0, coordinate_mode="logical"),
        regions=(
            Region(id="region.stem", role="stem", flow="absolute", slot_ids=("slot.q.text",)),
            Region(
                id="region.choices",
                role="choices",
                flow="absolute",
                slot_ids=("slot.choice.1", "slot.choice.2", "slot.choice.3"),
            ),
            Region(id="region.explain", role="explanation", flow="absolute", slot_ids=()),
        ),
        slots=(
            TextSlot(
                id="slot.q.text",
                prompt="",
                text="나머지가 가장 작은 것을 찾아 기호를 선택하세요.",
                style_role="question",
                x=55.995,
                y=88,
                font_size=30,
                fill="#111111",
            ),
            TextSlot(
                id="slot.choice.1",
                prompt="",
                text="㉠ 77 ÷ 6",
                style_role="choice",
                x=105.995,
                y=153,
                font_size=28,
                fill="#111111",
            ),
            TextSlot(
                id="slot.choice.2",
                prompt="",
                text="㉡ 264 ÷ 5",
                style_role="choice",
                x=325.995,
                y=153,
                font_size=28,
                fill="#111111",
            ),
            TextSlot(
                id="slot.choice.3",
                prompt="",
                text="㉢ 307 ÷ 3",
                style_role="choice",
                x=565.995,
                y=153,
                font_size=28,
                fill="#111111",
            ),
        ),
        diagrams=(),
        groups=(),
        constraints=(),
        tags=("초등", "수학", "나눗셈", "나머지", "비교"),
    )


PROBLEM_TEMPLATE = build_problem_template()
SEMANTIC_OVERRIDE = {
    "problem_id": "S3_초등_3_008602",
    "problem_type": "multiple_choice_comparison",
    "metadata": {
        "language": "ko",
        "question": "나머지가 가장 작은 것을 찾아 기호를 선택하는 문제",
        "instruction": "나머지가 가장 작은 것을 찾아 기호를 선택하세요.",
    },
    "domain": {
        "objects": [
            {
                "id": "obj.choice_1",
                "type": "division_expression",
                "symbol": "㉠",
                "dividend": 77,
                "divisor": 6,
            },
            {
                "id": "obj.choice_2",
                "type": "division_expression",
                "symbol": "㉡",
                "dividend": 264,
                "divisor": 5,
            },
            {
                "id": "obj.choice_3",
                "type": "division_expression",
                "symbol": "㉢",
                "dividend": 307,
                "divisor": 3,
            },
        ],
        "relations": [],
        "problem_solving": {
            "understand": {
                "given_refs": ["obj.choice_1", "obj.choice_2", "obj.choice_3"],
                "target_ref": "answer.target",
                "condition_refs": ["rel.compare_remainders"],
            },
            "plan": {
                "method": "compare_remainders",
                "description": "각 나눗셈식의 나머지를 비교해 가장 작은 기호를 찾는다.",
            },
            "execute": {
                "expected_operations": [
                    "identify_remainders",
                    "compare_values",
                    "select_smallest_symbol",
                ]
            },
            "review": {"check_methods": ["compare_all_candidates"]},
        },
    },
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {"type": "selected_symbol", "description": "나머지가 가장 작은 보기의 기호"},
        "value": "㉢",
        "unit": "",
    },
}
SOLVABLE = {
    "schema": "modu.solvable.v1.1",
    "problem_id": "S3_초등_3_008602",
    "problem_type": "multiple_choice_comparison",
    "inputs": {
        "total_ticks": 3,
        "target_label": "selected_symbol",
        "target_ticks": 1,
        "target_count": 1,
        "unit": "",
    },
    "given": [
        {"ref": "obj.choice_1", "value": {"symbol": "㉠", "dividend": 77, "divisor": 6}},
        {"ref": "obj.choice_2", "value": {"symbol": "㉡", "dividend": 264, "divisor": 5}},
        {"ref": "obj.choice_3", "value": {"symbol": "㉢", "dividend": 307, "divisor": 3}},
    ],
    "target": {"ref": "answer.target", "type": "selected_symbol"},
    "method": "compare_remainders",
    "plan": [
        "각 식의 나머지를 계산한다.",
        "나머지 중 가장 작은 값을 찾는다.",
        "해당 기호를 선택한다.",
    ],
    "steps": [
        {"id": "step.1", "expr": "77 ÷ 6의 나머지", "value": 5},
        {"id": "step.2", "expr": "264 ÷ 5의 나머지", "value": 4},
        {"id": "step.3", "expr": "307 ÷ 3의 나머지", "value": 1},
        {"id": "step.4", "expr": "가장 작은 나머지의 기호", "value": "㉢"},
    ],
    "checks": [{"id": "check.1", "expr": "min(5,4,1)=1", "expected": 1, "actual": 1, "pass": True}],
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {"type": "selected_symbol", "description": "나머지가 가장 작은 보기의 기호"},
        "value": "㉢",
        "unit": "",
    },
}
