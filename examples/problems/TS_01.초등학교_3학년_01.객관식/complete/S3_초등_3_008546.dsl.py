from __future__ import annotations
from modu_math.dsl import Canvas, ProblemTemplate, Region, RectSlot, TextSlot


def build_problem_template() -> ProblemTemplate:
    return ProblemTemplate(
        id="S3_초등_3_008546",
        title="계산 결과가 가장 큰 것을 찾아 기호를 선택하세요.",
        canvas=Canvas(width=870, height=360, coordinate_mode="logical"),
        regions=(
            Region(
                id="region.stem",
                role="stem",
                flow="absolute",
                slot_ids=(
                    "slot.q.num",
                    "slot.q.text",
                    "slot.choice_box",
                    "slot.choice.1",
                    "slot.choice.2",
                    "slot.choice.3",
                ),
            ),
            Region(
                id="region.answer",
                role="answer",
                flow="absolute",
                slot_ids=(),
            ),
            Region(
                id="region.explanation",
                role="explanation",
                flow="absolute",
                slot_ids=(
                    
                ),
            ),
        ),
        slots=(
            TextSlot(
                id="slot.q.text",
                prompt="",
                text="계산 결과가 가장 큰 것을 찾아 기호를 선택하세요.",
                style_role="question",
                x=54.0,
                y=50.0,
                font_size=28,
            ),
            RectSlot(
                id="slot.choice_box",
                prompt="",
                x=98.0,
                y=80.0,
                width=726.0,
                height=120.0,
                fill="#dfeec8",
            ),
            TextSlot(
                id="slot.choice.1",
                prompt="",
                text="ㄱ. 18 × 50",
                style_role="body",
                x=145.0,
                y=140.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.choice.2",
                prompt="",
                text="ㄴ. 66 × 20",
                style_role="body",
                x=389.0,
                y=140.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.choice.3",
                prompt="",
                text="ㄷ. 42 × 30",
                style_role="body",
                x=630.0,
                y=140.0,
                font_size=28,
            ),
            
        ),
        diagrams=(),
        groups=(),
        constraints=(),
        tags=("선택형", "곱셈", "비교"),
    )


PROBLEM_TEMPLATE = build_problem_template()

SEMANTIC_OVERRIDE = {
    "problem_id": "S3_초등_3_008546",
    "problem_type": "multiple_choice_comparison",
    "metadata": {
        "language": "ko",
        "question": "계산 결과가 가장 큰 것을 찾아 기호를 선택하세요.",
        "instruction": "보기의 곱셈 결과를 비교하여 가장 큰 기호를 고른다.",
    },
    "domain": {
        "objects": [
            {
                "id": "obj.choice_a",
                "type": "multiplication_expression",
                "symbol": "ㄱ",
                "left": 18,
                "right": 50,
            },
            {
                "id": "obj.choice_b",
                "type": "multiplication_expression",
                "symbol": "ㄴ",
                "left": 66,
                "right": 20,
            },
            {
                "id": "obj.choice_c",
                "type": "multiplication_expression",
                "symbol": "ㄷ",
                "left": 42,
                "right": 30,
            },
        ],
        "relations": [],
        "problem_solving": {
            "understand": {
                "given_refs": ["obj.choice_a", "obj.choice_b", "obj.choice_c"],
                "target_ref": "answer.target",
                "condition_refs": ["rel.compare_1", "rel.compare_2"],
            },
            "plan": {
                "method": "compare_products",
                "description": "각 곱셈식의 결과를 비교하여 가장 큰 기호를 찾는다.",
            },
            "execute": {
                "expected_operations": ["calculate_product", "compare_results"]
            },
            "review": {"check_methods": ["largest_value_check"]},
        },
    },
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {
            "type": "selected_symbol",
            "description": "계산 결과가 가장 큰 보기의 기호",
        },
        "value": "ㄴ",
        "unit": "",
    },
}

SOLVABLE = {
    "schema": "modu.solvable.v1.1",
    "problem_id": "S3_초등_3_008546",
    "problem_type": "multiple_choice_comparison",
    "inputs": {
        "total_ticks": 3,
        "target_label": "계산 결과가 가장 큰 기호",
        "target_ticks": 1,
        "target_count": 1,
        "unit": "",
    },
    "given": [
        {"ref": "obj.choice_a", "value": {"symbol": "ㄱ", "left": 18, "right": 50}},
        {"ref": "obj.choice_b", "value": {"symbol": "ㄴ", "left": 66, "right": 20}},
        {"ref": "obj.choice_c", "value": {"symbol": "ㄷ", "left": 42, "right": 30}},
    ],
    "target": {"ref": "answer.target", "type": "selected_symbol"},
    "method": "compare_products",
    "plan": ["각 보기의 곱을 계산한 뒤 가장 큰 값을 찾는다."],
    "steps": [
        {"id": "step.1", "expr": "18 × 50", "value": 900},
        {"id": "step.2", "expr": "66 × 20", "value": 1320},
        {"id": "step.3", "expr": "42 × 30", "value": 1260},
        {"id": "step.4", "expr": "max(900, 1320, 1260)", "value": 1320},
    ],
    "checks": [
        {
            "id": "check.1",
            "expr": "1320 > 1260 and 1320 > 900",
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
            "type": "selected_symbol",
            "description": "계산 결과가 가장 큰 보기의 기호",
        },
        "value": "ㄴ",
        "unit": "",
    },
}
