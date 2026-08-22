from __future__ import annotations
from modu_math.dsl import Canvas, ProblemTemplate, Region, RectSlot, TextSlot


def build_problem_template() -> ProblemTemplate:
    return ProblemTemplate(
        id="S3_초등_3_008579",
        title="곱의 크기를 바르게 비교한 것을 찾아 기호를 선택하세요",
        canvas=Canvas(width=760, height=470, coordinate_mode="logical"),
        regions=(
            Region(
                id="region.stem",
                role="stem",
                flow="absolute",
                slot_ids=("slot.q2",),
            ),
            Region(
                id="region.choice_box",
                role="body",
                flow="absolute",
                slot_ids=("slot.box", "slot.a1", "slot.a2", "slot.a3", "slot.choices"),
            ),
            Region(
                id="region.answer_explain",
                role="explanation",
                flow="absolute",
                slot_ids=(),
            ),
        ),
        slots=(
            TextSlot(
                id="slot.q2",
                prompt="",
                text="곱의 크기를 바르게 비교한 것을 찾아 기호를 선택하세요.",
                style_role="question",
                x=49.997,
                y=67,
                font_size=30,
                fill="#111111",
            ),
            RectSlot(
                id="slot.box",
                prompt="",
                x=182.998,
                y=118,
                width=380,
                height=158,
                fill="#ffffff",
                stroke="#111111",
                stroke_width=1.5,
            ),
            TextSlot(
                id="slot.a1",
                prompt="",
                text="㉠ 224 × 6 < 1160",
                style_role="body",
                x=237.998,
                y=166,
                font_size=30,
                fill="#111111",
            ),
            TextSlot(
                id="slot.a2",
                prompt="",
                text="㉡ 2023 > 337 × 6",
                style_role="body",
                x=237.998,
                y=208,
                font_size=30,
                fill="#111111",
            ),
            TextSlot(
                id="slot.a3",
                prompt="",
                text="㉢ 2907 < 352 × 8",
                style_role="body",
                x=237.998,
                y=251,
                font_size=30,
                fill="#111111",
            ),
            TextSlot(
                id="slot.choices",
                prompt="",
                text="( ㉠ , ㉡ , ㉢ )",
                style_role="body",
                x=282.998,
                y=326,
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
    "problem_id": "S3_초등_3_008579",
    "problem_type": "comparison_of_products",
    "metadata": {
        "language": "ko",
        "question": "곱의 크기를 바르게 비교한 것을 찾아 기호를 선택하는 문제",
        "instruction": "곱의 크기를 바르게 비교한 것을 찾아 기호를 선택하세요.",
    },
    "domain": {
        "objects": [
            {"id": "obj.choice.1", "type": "comparison_expression", "label": "㉠"},
            {"id": "obj.choice.2", "type": "comparison_expression", "label": "㉡"},
            {"id": "obj.choice.3", "type": "comparison_expression", "label": "㉢"},
        ],
        "relations": [],
        "problem_solving": {
            "understand": {
                "given_refs": ["obj.choice.1", "obj.choice.2", "obj.choice.3"],
                "target_ref": "answer.target",
                "condition_refs": ["rel.verify_1", "rel.verify_2", "rel.verify_3"],
            },
            "plan": {
                "method": "compute_and_check",
                "description": "각 보기의 곱을 계산한 뒤, 부등호가 계산값과 맞는지 확인한다.",
            },
            "execute": {
                "expected_operations": [
                    "multiply",
                    "compare_with_number",
                    "select_correct_choice",
                ]
            },
            "review": {
                "check_methods": [
                    "compare_each_expression",
                    "confirm_single_correct_choice",
                ]
            },
        },
    },
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {
            "type": "correct_choice",
            "description": "곱의 크기를 바르게 비교한 보기의 기호",
        },
        "value": 2,
        "unit": "",
    },
}

SOLVABLE = {
    "schema": "modu.solvable.v1.1",
    "problem_id": "S3_초등_3_008579",
    "problem_type": "comparison_of_products",
    "inputs": {
        "total_ticks": 3,
        "target_label": "㉡",
        "target_ticks": 1,
        "target_count": 1,
        "unit": "",
    },
    "given": [
        {"ref": "obj.choice.1", "value": {"expression": "224 × 6<1160"}},
        {"ref": "obj.choice.2", "value": {"expression": "2023>337 × 6"}},
        {"ref": "obj.choice.3", "value": {"expression": "2907<352 × 8"}},
    ],
    "target": {"ref": "answer.target", "type": "correct_choice"},
    "method": "compute_and_check",
    "plan": [
        "각 보기의 곱을 계산한다.",
        "계산한 값으로 부등호가 맞는지 확인한다.",
        "맞는 비교식을 고른다.",
    ],
    "steps": [
        {"id": "step.1", "expr": "224 × 6", "value": 1344},
        {"id": "step.2", "expr": "337 × 6", "value": 2022},
        {"id": "step.3", "expr": "352 × 8", "value": 2816},
        {"id": "step.4", "expr": "비교식 확인", "value": "㉡ 2023>337 × 6"},
    ],
    "checks": [
        {
            "id": "check.1",
            "expr": "224 × 6<1160",
            "expected": False,
            "actual": True,
            "pass": False,
        },
        {
            "id": "check.2",
            "expr": "2023>337 × 6",
            "expected": True,
            "actual": True,
            "pass": True,
        },
        {
            "id": "check.3",
            "expr": "2907<352 × 8",
            "expected": False,
            "actual": False,
            "pass": True,
        },
    ],
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {
            "type": "correct_choice",
            "description": "곱의 크기를 바르게 비교한 보기의 기호",
        },
        "value": 2,
        "unit": "",
    },
}
