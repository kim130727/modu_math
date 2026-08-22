from __future__ import annotations
from modu_math.dsl import Canvas, ProblemTemplate, Region, RectSlot, TextSlot


def build_problem_template() -> ProblemTemplate:
    return ProblemTemplate(
        id="S3_초등_3_008606",
        title="나머지가 더 큰 것을 선택하세요",
        canvas=Canvas(width=720, height=265, coordinate_mode="logical"),
        regions=(
            Region(
                id="region.stem",
                role="stem",
                flow="absolute",
                slot_ids=(
                    "slot.q",
                    "slot.box1",
                    "slot.box2",
                    
                    
                ),
            ),
        ),
        slots=(
            TextSlot(
                id="slot.q",
                prompt="",
                text = '나머지가 더 큰 것을 선택하세요.', style_role="question",
                x = 30, y = 45, font_size = 30),
            RectSlot(
                id="slot.box1", prompt="", x = 85, y = 95, width = 190, height = 80),
            RectSlot(
                id="slot.box2", prompt="", x = 340, y = 95, width = 190, height = 80),
            TextSlot(
                id="slot.box1.text",
                prompt="",
                text = '491 ÷ 3', style_role="body",
                x = 125, y = 145, font_size = 30),
            TextSlot(
                id="slot.box2.text",
                prompt="",
                text = '709 ÷ 6', style_role="body",
                x = 385, y = 145, font_size = 30),
            
            
        ),
        diagrams=(),
        groups=(),
        constraints=(),
        tags=(),
    )


PROBLEM_TEMPLATE = build_problem_template()

SEMANTIC_OVERRIDE = {
    "problem_id": "S3_초등_3_008606",
    "problem_type": "compare_remainder",
    "metadata": {
        "language": "ko",
        "question": "나머지가 더 큰 것을 선택하세요.",
        "instruction": "두 나눗셈의 나머지를 비교하여 더 큰 것을 고른다.",
    },
    "domain": {
        "objects": [
            {"id": "obj.div1", "type": "division_expression", "expression": "491 ÷ 3"},
            {"id": "obj.div2", "type": "division_expression", "expression": "709 ÷ 6"},
            {"id": "obj.remainder1", "type": "remainder"},
            {"id": "obj.remainder2", "type": "remainder"},
        ],
        "relations": [],
        "problem_solving": {
            "understand": {
                "given_refs": ["obj.div1", "obj.div2"],
                "target_ref": "answer.target",
                "condition_refs": ["rel.compare_remainder"],
            },
            "plan": {
                "method": "remainder_comparison",
                "description": "각 나눗셈의 나머지를 비교한다.",
            },
            "execute": {
                "expected_operations": ["identify_remainders", "compare_remainders"]
            },
            "review": {"check_methods": ["compare_two_numbers"]},
        },
    },
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {
            "type": "selected_expression",
            "description": "나머지가 더 큰 나눗셈",
        },
        "value": 491,
        "unit": "",
    },
}

SOLVABLE = {
    "schema": "modu.solvable.v1.1",
    "problem_id": "S3_초등_3_008606",
    "problem_type": "compare_remainder",
    "inputs": {
        "total_ticks": 2,
        "target_label": "나머지가 더 큰 것",
        "target_ticks": 1,
        "target_count": 1,
        "unit": "",
    },
    "given": [
        {"ref": "obj.div1", "value": {"expression": "491 ÷ 3"}},
        {"ref": "obj.div2", "value": {"expression": "709 ÷ 6"}},
    ],
    "target": {"ref": "answer.target", "type": "selected_expression"},
    "method": "remainder_comparison",
    "plan": ["두 나눗셈의 나머지를 확인한 뒤 더 큰 나머지를 가진 식을 고른다."],
    "steps": [
        {"id": "step.1", "expr": "491 ÷ 3의 나머지 확인", "value": 2},
        {"id": "step.2", "expr": "709 ÷ 6의 나머지 확인", "value": 1},
        {"id": "step.3", "expr": "2 > 1", "value": True},
    ],
    "checks": [
        {
            "id": "check.1",
            "expr": "491 ÷ 3의 나머지가 709 ÷ 6의 나머지보다 큰가",
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
            "type": "selected_expression",
            "description": "나머지가 더 큰 나눗셈",
        },
        "value": 491,
        "unit": "",
    },
}
