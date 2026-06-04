from __future__ import annotations
from modu_math.dsl import Canvas, ProblemTemplate, RectSlot, Region, TextSlot


def build_problem_template() -> ProblemTemplate:
    return ProblemTemplate(
        id="S3_초등_3_008609",
        title="바르게 계산한 것을 찾아 기호를 선택해 보세요.",
        canvas=Canvas(width=880, height=280, coordinate_mode="logical"),
        regions=(
            Region(
                id="region.header",
                role="stem",
                flow="absolute",
                slot_ids=("slot.qnum", "slot.stem"),
            ),
            Region(
                id="region.choice_box",
                role="content",
                flow="absolute",
                slot_ids=("slot.box", "slot.choice.left", "slot.choice.right"),
            ),
            Region(
                id="region.answer_explain",
                role="supporting",
                flow="absolute",
                slot_ids=("slot.conclusion",),
            ),
        ),
        slots=(
            TextSlot(
                id="slot.qnum",
                prompt="",
                text="79.",
                style_role="question",
                x=18.0,
                y=33.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.stem",
                prompt="",
                text="바르게 계산한 것을 찾아 기호를 선택해 보세요.",
                style_role="question",
                x=72.0,
                y=33.0,
                font_size=28,
            ),
            RectSlot(
                id="slot.box",
                prompt="",
                x=95.0,
                y=50.0,
                width=740.0,
                height=80.0,
                fill="none",
                stroke="#F2A34A",
            ),
            TextSlot(
                id="slot.choice.left",
                prompt="",
                text="㉠ 28 ÷ 2 = 14",
                style_role="question",
                x=210.0,
                y=101.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.choice.right",
                prompt="",
                text="㉡ 55 ÷ 5 = 15",
                style_role="question",
                x=575.0,
                y=101.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.conclusion",
                prompt="",
                text="따라서 바르게 계산한 것은 ㉠입니다.",
                style_role="question",
                x=18.0,
                y=264.0,
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
    "problem_id": "S3_초등_3_008609",
    "problem_type": "multiple_choice_division_correctness",
    "metadata": {
        "language": "ko",
        "question": "바르게 계산한 것을 찾아 기호를 선택해 보세요.",
        "instruction": "보기의 계산이 바른지 판단하여 정답 기호를 고른다.",
    },
    "domain": {
        "objects": [
            {
                "id": "obj.choice.a",
                "type": "calculation_option",
                "label": "㉠",
                "expression": "28 ÷ 2 = 14",
            },
            {
                "id": "obj.choice.b",
                "type": "calculation_option",
                "label": "㉡",
                "expression": "55 ÷ 5 = 15",
            },
            {
                "id": "obj.explanation.b",
                "type": "explanation_statement",
                "label": "㉡",
                "expression": "55 ÷ 5 = 11",
            },
        ],
        "relations": [],
        "problem_solving": {
            "understand": {
                "given_refs": ["obj.choice.a", "obj.choice.b", "obj.explanation.b"],
                "target_ref": "answer.target",
                "condition_refs": ["rel.compare_options"],
            },
            "plan": {
                "method": "compare_calculation_results",
                "description": "각 보기의 나눗셈이 바른지 비교하여 맞는 기호를 고른다.",
            },
            "execute": {
                "expected_operations": [
                    "inspect_options",
                    "compare_correctness",
                    "select_label",
                ]
            },
            "review": {"check_methods": ["answer_key_match", "statement_consistency"]},
        },
    },
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {
            "type": "correct_option_label",
            "description": "바르게 계산한 보기의 기호",
        },
        "value": "㉠",
        "unit": "",
    },
}

SOLVABLE = {
    "schema": "modu.solvable.v1.1",
    "problem_id": "S3_초등_3_008609",
    "problem_type": "multiple_choice_division_correctness",
    "inputs": {
        "total_ticks": 2,
        "target_label": "정답 기호",
        "target_ticks": 1,
        "target_count": 1,
        "unit": "",
    },
    "given": [
        {"ref": "obj.choice.a", "value": {"label": "㉠", "expression": "28 ÷ 2 = 14"}},
        {"ref": "obj.choice.b", "value": {"label": "㉡", "expression": "55 ÷ 5 = 15"}},
        {
            "ref": "obj.explanation.b",
            "value": {"label": "㉡", "expression": "55 ÷ 5 = 11"},
        },
    ],
    "target": {"ref": "answer.target", "type": "correct_option_label"},
    "method": "compare_calculation_results",
    "plan": [
        "각 보기의 계산 결과가 식과 맞는지 비교한다.",
        "바르게 계산된 보기를 선택한다.",
    ],
    "steps": [
        {"id": "step.1", "expr": "28 ÷ 2 = 14", "value": True},
        {"id": "step.2", "expr": "55 ÷ 5 = 15", "value": False},
        {"id": "step.3", "expr": "정답 기호 선택", "value": "㉠"},
    ],
    "checks": [
        {
            "id": "check.1",
            "expr": "보기 ㉠의 계산이 맞는가",
            "expected": True,
            "actual": True,
            "pass": True,
        },
        {
            "id": "check.2",
            "expr": "보기 ㉡의 계산이 맞는가",
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
            "type": "correct_option_label",
            "description": "바르게 계산한 보기의 기호",
        },
        "value": "㉠",
        "unit": "",
    },
}
