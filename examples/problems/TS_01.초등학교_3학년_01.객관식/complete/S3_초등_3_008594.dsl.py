from __future__ import annotations
from modu_math.dsl import Canvas, ProblemTemplate, Region, RectSlot, TextSlot


def build_problem_template() -> ProblemTemplate:
    return ProblemTemplate(
        id="S3_초등_3_008594",
        title="나머지가 더 큰 것을 찾아 보세요",
        canvas=Canvas(width=720, height=360, coordinate_mode="logical"),
        regions=(
            Region(
                id="region.stem",
                role="stem",
                flow="absolute",
                slot_ids=("slot.q.text",),
            ),
            Region(
                id="region.choices",
                role="diagram",
                flow="absolute",
                slot_ids=("slot.choice.box", "slot.choice.a", "slot.choice.b"),
            ),
            Region(
                id="region.answer", role="supporting_text", flow="absolute", slot_ids=()
            ),
        ),
        slots=(
            TextSlot(
                id="slot.q.text",
                prompt="",
                text = '나머지가 더 큰 것을 찾아 선택해 보세요.', style_role="question",
                x = 90, y = 50, font_size = 30),
            RectSlot(
                id="slot.choice.box",
                prompt="",
                x = 90, y = 80, width = 470, height = 80, fill="#DFECCC",
            ),
            TextSlot(
                id="slot.choice.a",
                prompt="",
                text = '㉠ 515 ÷ 4', style_role="label",
                x = 140, y = 130, font_size = 30),
            TextSlot(
                id="slot.choice.b",
                prompt="",
                text = '㉡ 516 ÷ 5', style_role="label",
                x = 370, y = 130, font_size = 30),
        ),
        diagrams=(),
        groups=(),
        constraints=(),
        tags=(),
    )


PROBLEM_TEMPLATE = build_problem_template()

SEMANTIC_OVERRIDE = {
    "problem_id": "S3_초등_3_008594",
    "problem_type": "compare_remainders",
    "metadata": {
        "language": "ko",
        "question": "나머지가 더 큰 것을 찾는 문제",
        "instruction": "두 나눗셈의 나머지를 비교하여 더 큰 보기를 고른다.",
    },
    "domain": {
        "objects": [
            {
                "id": "obj.choice.a",
                "type": "division_expression",
                "label": "㉠",
                "dividend": 515,
                "divisor": 4,
            },
            {
                "id": "obj.choice.b",
                "type": "division_expression",
                "label": "㉡",
                "dividend": 516,
                "divisor": 5,
            },
            {"id": "obj.remainder.a", "type": "remainder", "value": 3},
            {"id": "obj.remainder.b", "type": "remainder", "value": 1},
        ],
        "relations": [],
        "problem_solving": {
            "understand": {
                "given_refs": ["obj.choice.a", "obj.choice.b"],
                "target_ref": "answer.target",
                "condition_refs": ["rel.compare.remainder"],
            },
            "plan": {
                "method": "compare_remainders",
                "description": "각 나눗셈의 나머지를 비교하여 더 큰 보기의 기호를 찾는다.",
            },
            "execute": {
                "expected_operations": ["identify_remainders", "compare_values"]
            },
            "review": {"check_methods": ["remainder_comparison_check"]},
        },
    },
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {"type": "choice_label", "description": "나머지가 더 큰 보기"},
        "value": "㉠",
        "unit": "",
    },
}

SOLVABLE = {
    "schema": "modu.solvable.v1.1",
    "problem_id": "S3_초등_3_008594",
    "problem_type": "compare_remainders",
    "inputs": {
        "total_ticks": 0,
        "target_label": "㉠",
        "target_ticks": 0,
        "target_count": 1,
        "unit": "",
    },
    "given": [
        {"ref": "obj.choice.a", "value": {"dividend": 515, "divisor": 4}},
        {"ref": "obj.choice.b", "value": {"dividend": 516, "divisor": 5}},
        {"ref": "obj.remainder.a", "value": 3},
        {"ref": "obj.remainder.b", "value": 1},
    ],
    "target": {"ref": "answer.target", "type": "choice_label"},
    "method": "compare_remainders",
    "plan": [
        "두 나눗셈의 나머지를 확인한다.",
        "나머지의 크기를 비교한다.",
        "더 큰 나머지를 가진 보기의 기호를 답으로 정한다.",
    ],
    "steps": [
        {"id": "step.1", "expr": "515 ÷ 4의 나머지", "value": 3},
        {"id": "step.2", "expr": "516 ÷ 5의 나머지", "value": 1},
        {"id": "step.3", "expr": "3 > 1", "value": True},
        {"id": "step.4", "expr": "나머지가 더 큰 보기", "value": "㉠"},
    ],
    "checks": [
        {
            "id": "check.1",
            "expr": "515 = 4 × 128 + 3",
            "expected": True,
            "actual": True,
            "pass": True,
        },
        {
            "id": "check.2",
            "expr": "516 = 5 × 103 + 1",
            "expected": True,
            "actual": True,
            "pass": True,
        },
    ],
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {"type": "choice_label", "description": "나머지가 더 큰 보기"},
        "value": "㉠",
        "unit": "",
    },
}
