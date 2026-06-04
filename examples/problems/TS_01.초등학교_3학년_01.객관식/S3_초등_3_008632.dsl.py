from __future__ import annotations
from modu_math.dsl import Canvas, ProblemTemplate, Region, TextSlot, RectSlot


def build_problem_template() -> ProblemTemplate:
    return ProblemTemplate(
        id="S3_초등_3_008632",
        title="나눗셈에서 나머지가 다른 것 고르기",
        canvas=Canvas(width=760, height=500, coordinate_mode="logical"),
        regions=(
            Region(
                id="region.stem",
                role="stem",
                flow="absolute",
                slot_ids=("slot.q.box", "slot.q.number", "slot.q.text"),
            ),
            Region(
                id="region.choices",
                role="body",
                flow="absolute",
                slot_ids=(
                    "slot.choice.1",
                    "slot.choice.2",
                    "slot.choice.3",
                    "slot.choice.4",
                    "slot.choice.5",
                ),
            ),
            Region(
                id="region.answer_explanation",
                role="explanation",
                flow="absolute",
                slot_ids=(
                    "slot.ans",
                    "slot.exp",
                    "slot.exp1",
                    "slot.exp2",
                    "slot.exp3",
                    "slot.exp4",
                    "slot.exp5",
                    "slot.concl",
                ),
            ),
        ),
        slots=(
            RectSlot(
                id="slot.q.box",
                prompt="",
                x=14.0,
                y=10.0,
                width=16.0,
                height=16.0,
                stroke="#333333",
                stroke_width=1.5,
                fill="none",
            ),
            TextSlot(
                id="slot.q.number",
                prompt="",
                text="3.",
                style_role="question",
                x=38.0,
                y=28.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.q.text",
                prompt="",
                text="나눗셈 중에서 나머지가 다른 하나를 고르세요.",
                style_role="question",
                x=82.0,
                y=28.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.choice.1",
                prompt="",
                text="① 39 ÷ 3",
                style_role="question",
                x=26.0,
                y=86.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.choice.2",
                prompt="",
                text="② 17 ÷ 4",
                style_role="question",
                x=327.0,
                y=86.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.choice.3",
                prompt="",
                text="③ 16 ÷ 5",
                style_role="question",
                x=580.0,
                y=86.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.choice.4",
                prompt="",
                text="④ 31 ÷ 6",
                style_role="question",
                x=26.0,
                y=131.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.choice.5",
                prompt="",
                text="⑤ 27 ÷ 2",
                style_role="question",
                x=327.0,
                y=131.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.ans",
                prompt="",
                text="(정답) ①",
                style_role="supporting",
                x=26.0,
                y=190.0,
                font_size=22,
            ),
            TextSlot(
                id="slot.exp",
                prompt="",
                text="(해설)",
                style_role="supporting",
                x=26.0,
                y=230.0,
                font_size=22,
            ),
            TextSlot(
                id="slot.exp1",
                prompt="",
                text="① 39 ÷ 3 = 13이므로 나머지가 0입니다.",
                style_role="supporting",
                x=26.0,
                y=270.0,
                font_size=20,
            ),
            TextSlot(
                id="slot.exp2",
                prompt="",
                text="② 17 ÷ 4 = 4···1이므로 나머지가 1입니다.",
                style_role="supporting",
                x=26.0,
                y=305.0,
                font_size=20,
            ),
            TextSlot(
                id="slot.exp3",
                prompt="",
                text="③ 16 ÷ 5 = 3···1이므로 나머지가 1입니다.",
                style_role="supporting",
                x=26.0,
                y=340.0,
                font_size=20,
            ),
            TextSlot(
                id="slot.exp4",
                prompt="",
                text="④ 31 ÷ 6 = 5···1이므로 나머지가 1입니다.",
                style_role="supporting",
                x=26.0,
                y=375.0,
                font_size=20,
            ),
            TextSlot(
                id="slot.exp5",
                prompt="",
                text="⑤ 27 ÷ 2 = 13···1이므로 나머지가 1입니다.",
                style_role="supporting",
                x=26.0,
                y=410.0,
                font_size=20,
            ),
            TextSlot(
                id="slot.concl",
                prompt="",
                text="따라서 나머지가 다른 하나는 ① 39 ÷ 3입니다.",
                style_role="supporting",
                x=26.0,
                y=445.0,
                font_size=20,
            ),
        ),
        diagrams=(),
        groups=(),
        constraints=(),
        tags=(),
    )


PROBLEM_TEMPLATE = build_problem_template()

SEMANTIC_OVERRIDE = {
    "problem_id": "S3_초등_3_008632",
    "problem_type": "multiple_choice_division_remainder_comparison",
    "metadata": {
        "language": "ko",
        "question": "나눗셈 중에서 나머지가 다른 하나를 고르세요.",
        "instruction": "보기의 나눗셈식들에서 나머지를 비교하여 다른 하나를 찾는다.",
    },
    "domain": {
        "objects": [
            {
                "id": "obj.choice.1",
                "type": "division_expression",
                "expression": "39 ÷ 3",
            },
            {
                "id": "obj.choice.2",
                "type": "division_expression",
                "expression": "17 ÷ 4",
            },
            {
                "id": "obj.choice.3",
                "type": "division_expression",
                "expression": "16 ÷ 5",
            },
            {
                "id": "obj.choice.4",
                "type": "division_expression",
                "expression": "31 ÷ 6",
            },
            {
                "id": "obj.choice.5",
                "type": "division_expression",
                "expression": "27 ÷ 2",
            },
        ],
        "relations": [],
        "problem_solving": {
            "understand": {
                "given_refs": [
                    "obj.choice.1",
                    "obj.choice.2",
                    "obj.choice.3",
                    "obj.choice.4",
                    "obj.choice.5",
                ],
                "target_ref": "answer.target",
                "condition_refs": ["rel.compare.remainder"],
            },
            "plan": {
                "method": "remainder_comparison",
                "description": "각 나눗셈식의 나머지를 비교하여 다른 하나를 찾는다.",
            },
            "execute": {
                "expected_operations": [
                    "identify_remainder",
                    "compare_remainders",
                    "select_different_one",
                ]
            },
            "review": {
                "check_methods": [
                    "verify_remainder_pattern",
                    "confirm_selected_choice_matches_statement",
                ]
            },
        },
    },
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {
            "type": "different_remainder_choice",
            "description": "나머지가 다른 하나",
        },
        "value": 1,
        "unit": "",
    },
}

SOLVABLE = {
    "schema": "modu.solvable.v1.1",
    "problem_id": "S3_초등_3_008632",
    "problem_type": "multiple_choice_division_remainder_comparison",
    "inputs": {
        "total_ticks": 5,
        "target_label": "나머지가 다른 하나",
        "target_ticks": 1,
        "target_count": 1,
        "unit": "",
    },
    "given": [
        {"ref": "obj.choice.1", "value": {"expression": "39 ÷ 3"}},
        {"ref": "obj.choice.2", "value": {"expression": "17 ÷ 4"}},
        {"ref": "obj.choice.3", "value": {"expression": "16 ÷ 5"}},
        {"ref": "obj.choice.4", "value": {"expression": "31 ÷ 6"}},
        {"ref": "obj.choice.5", "value": {"expression": "27 ÷ 2"}},
    ],
    "target": {"ref": "answer.target", "type": "different_remainder_choice"},
    "method": "remainder_comparison",
    "plan": ["각 식의 나머지를 확인하고, 다른 나머지를 가진 보기를 찾는다."],
    "steps": [
        {"id": "step.1", "expr": "39 ÷ 3", "value": {"quotient": 13, "remainder": 0}},
        {"id": "step.2", "expr": "17 ÷ 4", "value": {"quotient": 4, "remainder": 1}},
        {"id": "step.3", "expr": "16 ÷ 5", "value": {"quotient": 3, "remainder": 1}},
        {"id": "step.4", "expr": "31 ÷ 6", "value": {"quotient": 5, "remainder": 1}},
        {"id": "step.5", "expr": "27 ÷ 2", "value": {"quotient": 13, "remainder": 1}},
        {"id": "step.6", "expr": "나머지가 다른 보기 선택", "value": 1},
    ],
    "checks": [
        {
            "id": "check.1",
            "expr": "obj.choice.1.remainder != obj.choice.2.remainder",
            "expected": True,
            "actual": True,
            "pass": True,
        },
        {
            "id": "check.2",
            "expr": "선택된 답이 ①인지 확인",
            "expected": 1,
            "actual": 1,
            "pass": True,
        },
    ],
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {
            "type": "different_remainder_choice",
            "description": "나머지가 다른 하나",
        },
        "value": 1,
        "unit": "",
    },
}
