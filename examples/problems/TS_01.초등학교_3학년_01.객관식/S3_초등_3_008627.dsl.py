from __future__ import annotations
from modu_math.dsl import Canvas, ProblemTemplate, Region, TextSlot


def build_problem_template() -> ProblemTemplate:
    return ProblemTemplate(
        id="S3_초등_3_008627",
        title="나머지가 다른 하나는 어느 것일까요?",
        canvas=Canvas(width=736.0, height=317.0, coordinate_mode="logical"),
        regions=(
            Region(
                id="region.stem",
                role="stem",
                flow="absolute",
                slot_ids=(
                    "slot.q",
                    "slot.opt1",
                    "slot.opt2",
                    "slot.opt3",
                    "slot.opt4",
                    "slot.opt5",
                    
                ),
            ),
        ),
        slots=(
            TextSlot(
                id="slot.q",
                prompt="",
                text = '나머지가 다른 하나는 어느 것일까요?', style_role="question",
                x = 25, y = 40, font_size = 30),
            TextSlot(
                id="slot.opt1",
                prompt="",
                text = '① 37 ÷ 7', style_role="question",
                x = 20, y = 105, font_size = 30),
            TextSlot(
                id="slot.opt2",
                prompt="",
                text = '② 22 ÷ 5', style_role="question",
                x = 240, y = 105, font_size = 30),
            TextSlot(
                id="slot.opt3",
                prompt="",
                text = '③ 26 ÷ 4', style_role="question",
                x = 480, y = 105, font_size = 30),
            TextSlot(
                id="slot.opt4",
                prompt="",
                text = '④ 58 ÷ 9', style_role="question",
                x = 20, y = 150, font_size = 30),
            TextSlot(
                id="slot.opt5",
                prompt="",
                text = '⑤ 66 ÷ 8', style_role="question",
                x = 240, y = 150, font_size = 30),
            
        ),
        diagrams=(),
        groups=(),
        constraints=(),
        tags=(),
    )


PROBLEM_TEMPLATE = build_problem_template()

SEMANTIC_OVERRIDE = {
    "problem_id": "S3_초등_3_008627",
    "problem_type": "division_remainder_comparison",
    "metadata": {
        "language": "ko",
        "question": "나머지가 다른 하나는 어느 것일까요?",
        "instruction": "보기 중 나머지가 다른 하나를 찾는다.",
    },
    "domain": {
        "objects": [
            {"id": "obj.div1", "type": "division_expression", "expression": "37 ÷ 7"},
            {"id": "obj.div2", "type": "division_expression", "expression": "22 ÷ 5"},
            {"id": "obj.div3", "type": "division_expression", "expression": "26 ÷ 4"},
            {"id": "obj.div4", "type": "division_expression", "expression": "58 ÷ 9"},
            {"id": "obj.div5", "type": "division_expression", "expression": "66 ÷ 8"},
        ],
        "relations": [],
        "problem_solving": {
            "understand": {
                "given_refs": [
                    "obj.div1",
                    "obj.div2",
                    "obj.div3",
                    "obj.div4",
                    "obj.div5",
                ],
                "target_ref": "answer.target",
                "condition_refs": ["rel.compare_remainders"],
            },
            "plan": {
                "method": "compare_remainders",
                "description": "각 나눗셈식의 나머지를 비교해서 다른 항목을 찾는다.",
            },
            "execute": {
                "expected_operations": [
                    "identify_remainders",
                    "compare_values",
                    "select_unique_item",
                ]
            },
            "review": {"check_methods": ["remainder_consistency_check"]},
        },
    },
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {"type": "option_number", "description": "나머지가 다른 보기"},
        "value": 4,
        "unit": "",
    },
}

SOLVABLE = {
    "schema": "modu.solvable.v1.1",
    "problem_id": "S3_초등_3_008627",
    "problem_type": "division_remainder_comparison",
    "inputs": {
        "total_ticks": 5,
        "target_label": "나머지가 다른 보기",
        "target_ticks": 1,
        "target_count": 1,
        "unit": "",
    },
    "given": [
        {"ref": "obj.div1", "value": {"expression": "37 ÷ 7"}},
        {"ref": "obj.div2", "value": {"expression": "22 ÷ 5"}},
        {"ref": "obj.div3", "value": {"expression": "26 ÷ 4"}},
        {"ref": "obj.div4", "value": {"expression": "58 ÷ 9"}},
        {"ref": "obj.div5", "value": {"expression": "66 ÷ 8"}},
    ],
    "target": {"ref": "answer.target", "type": "option_number"},
    "method": "compare_remainders",
    "plan": [
        "각 나눗셈식의 나머지를 확인한다.",
        "나머지가 같은 보기들과 다른 보기를 비교한다.",
    ],
    "steps": [
        {"id": "step.1", "expr": "37 ÷ 7의 나머지 확인", "value": 2},
        {"id": "step.2", "expr": "22 ÷ 5의 나머지 확인", "value": 2},
        {"id": "step.3", "expr": "26 ÷ 4의 나머지 확인", "value": 2},
        {"id": "step.4", "expr": "58 ÷ 9의 나머지 확인", "value": 4},
        {"id": "step.5", "expr": "66 ÷ 8의 나머지 확인", "value": 2},
        {"id": "step.6", "expr": "다른 나머지를 가진 보기 선택", "value": 4},
    ],
    "checks": [
        {
            "id": "check.1",
            "expr": "나머지 집합에 4만 홀로 존재하는가",
            "expected": 1,
            "actual": 1,
            "pass": True,
        },
        {
            "id": "check.2",
            "expr": "정답이 ④인가",
            "expected": 4,
            "actual": 4,
            "pass": True,
        },
    ],
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {"type": "option_number", "description": "나머지가 다른 보기"},
        "value": 4,
        "unit": "",
    },
}
