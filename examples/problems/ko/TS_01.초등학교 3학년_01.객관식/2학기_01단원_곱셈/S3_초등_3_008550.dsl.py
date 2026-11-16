from __future__ import annotations
from modu_math.dsl import (
    Canvas,
    CircleSlot,
    ProblemTemplate,
    RectSlot,
    Region,
    TextSlot,
)


def build_problem_template() -> ProblemTemplate:
    return ProblemTemplate(
        id="S3_초등_3_008550",
        title="□ 안의 수가 다른 하나를 찾아 기호를 선택해보세요.",
        canvas=Canvas(width=700.0, height=300.0, coordinate_mode="logical"),
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
                slot_ids=(
                    "slot.box",
                    "slot.choice.1",
                    "slot.choice.2",
                    "slot.choice.3",
                ),
            ),
            Region(
                id="region.answer",
                role="note",
                flow="absolute",
                slot_ids=(
                    
                    
                ),
            ),
        ),
        slots=(
            TextSlot(
                id="slot.q.text",
                prompt="",
                text="□ 안의 수가 다른 하나를 찾아 기호를 선택해보세요.",
                style_role="question",
                x = 20, y = 35, font_size=28,
            ),
            RectSlot(
                id="slot.box", prompt="", x = 145, y = 55, width=370.0, height=186.0
            ),
            TextSlot(
                id="slot.choice.1",
                prompt="",
                text="ㄱ. 60 × 40 = □ 00",
                style_role="question",
                x = 205, y = 110, font_size=28,
            ),
            TextSlot(
                id="slot.choice.2",
                prompt="",
                text="ㄴ. 90 × 30 = □ 00",
                style_role="question",
                x = 205, y = 160, font_size=28,
            ),
            TextSlot(
                id="slot.choice.3",
                prompt="",
                text="ㄷ. 30 × 80 = □ 00",
                style_role="question",
                x = 205, y = 210, font_size=28,
            ),
            
            
        ),
        diagrams=(),
        groups=(),
        constraints=(),
        tags=("선택형", "곱셈", "수비교"),
    )


PROBLEM_TEMPLATE = build_problem_template()

SEMANTIC_OVERRIDE = {
    "problem_id": "S3_초등_3_008550",
    "problem_type": "multiple_choice_number_pattern",
    "metadata": {
        "language": "ko",
        "question": "□ 안의 수가 다른 하나를 찾아 기호를 선택해보세요.",
        "instruction": "세 보기의 곱셈 결과를 비교해 다른 하나의 기호를 찾는다.",
    },
    "domain": {
        "objects": [
            {
                "id": "obj.choice1",
                "type": "multiplication",
                "expression": "60 × 40",
                "result_pattern": "□00",
            },
            {
                "id": "obj.choice2",
                "type": "multiplication",
                "expression": "90 × 30",
                "result_pattern": "□00",
            },
            {
                "id": "obj.choice3",
                "type": "multiplication",
                "expression": "30 × 80",
                "result_pattern": "□00",
            },
        ],
        "relations": [],
        "problem_solving": {
            "understand": {
                "given_refs": ["obj.choice1", "obj.choice2", "obj.choice3"],
                "target_ref": "answer.target",
                "condition_refs": ["rel.compare_results"],
            },
            "plan": {
                "method": "compare_products",
                "description": "각 곱셈의 결과를 비교하여 다른 값을 만드는 보기를 찾는다.",
            },
            "execute": {"expected_operations": ["multiply_numbers", "compare_results"]},
            "review": {"check_methods": ["result_consistency_check"]},
        },
    },
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {
            "type": "choice_symbol",
            "description": "□ 안의 수가 다른 보기의 기호",
        },
        "value": "ㄴ",
        "unit": "",
    },
}

SOLVABLE = {
    "schema": "modu.solvable.v1.1",
    "problem_id": "S3_초등_3_008550",
    "problem_type": "multiple_choice_number_pattern",
    "inputs": {
        "total_ticks": 3,
        "target_label": "□ 안의 수가 다른 보기의 기호",
        "target_ticks": 1,
        "target_count": 1,
        "unit": "",
    },
    "given": [
        {"ref": "obj.choice1", "value": {"expression": "60 × 40"}},
        {"ref": "obj.choice2", "value": {"expression": "90 × 30"}},
        {"ref": "obj.choice3", "value": {"expression": "30 × 80"}},
    ],
    "target": {"ref": "answer.target", "type": "choice_symbol"},
    "method": "compare_products",
    "plan": [
        "각 식의 곱을 구한다.",
        "같은 결과 패턴끼리 비교한다.",
        "다른 결과를 가진 보기의 기호를 찾는다.",
    ],
    "steps": [
        {"id": "step.1", "expr": "60 × 40", "value": 2400},
        {"id": "step.2", "expr": "90 × 30", "value": 2700},
        {"id": "step.3", "expr": "30 × 80", "value": 2400},
        {"id": "step.4", "expr": "2400, 2700, 2400 비교", "value": "둘째 보기만 다름"},
    ],
    "checks": [
        {
            "id": "check.1",
            "expr": "60 × 40 = 2400",
            "expected": 2400,
            "actual": 2400,
            "pass": True,
        },
        {
            "id": "check.2",
            "expr": "90 × 30 = 2700",
            "expected": 2700,
            "actual": 2700,
            "pass": True,
        },
        {
            "id": "check.3",
            "expr": "30 × 80 = 2400",
            "expected": 2400,
            "actual": 2400,
            "pass": True,
        },
    ],
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {
            "type": "choice_symbol",
            "description": "□ 안의 수가 다른 보기의 기호",
        },
        "value": "ㄴ",
        "unit": "",
    },
}
