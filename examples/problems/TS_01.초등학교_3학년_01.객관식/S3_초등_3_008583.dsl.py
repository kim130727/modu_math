from __future__ import annotations

from modu_math.dsl import Canvas, ProblemTemplate, RectSlot, Region, TextSlot


def build_problem_template() -> ProblemTemplate:
    return ProblemTemplate(
        id="S3_초등_3_008583",
        title="몫이 가장 큰 것을 선택하세요.",
        canvas=Canvas(width=855.0, height=266.0, coordinate_mode="logical"),
        regions=(
            Region(
                id="region.stem",
                role="stem",
                flow="absolute",
                slot_ids=("slot.icon", "slot.qnum", "slot.qtext"),
            ),
            Region(
                id="region.choices",
                role="diagram",
                flow="absolute",
                slot_ids=(
                    "slot.choice.1",
                    "slot.choice.1.text",
                    "slot.choice.2",
                    "slot.choice.2.text",
                    "slot.choice.3",
                    "slot.choice.3.text",
                ),
            ),
            Region(
                id="region.explanation",
                role="supporting",
                flow="absolute",
                slot_ids=(
                    "slot.answer",
                    "slot.solution",
                    "slot.solution.final",
                    "slot.t10",
                    "slot.t18",
                    "slot.t20",
                    "slot.lt",
                    "slot.comp",
                ),
            ),
        ),
        slots=(
            RectSlot(id="slot.icon", prompt="", x=5.0, y=18.0, width=12.0, height=12.0),
            TextSlot(
                id="slot.qnum",
                prompt="",
                text="50.",
                style_role="question",
                x=28.0,
                y=29.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.qtext",
                prompt="",
                text="몫이 가장 큰 것을 선택하세요.",
                style_role="question",
                x=80.0,
                y=29.0,
                font_size=28,
            ),
            RectSlot(
                id="slot.choice.1", prompt="", x=114.0, y=49.0, width=186.0, height=68.0
            ),
            TextSlot(
                id="slot.choice.1.text",
                prompt="",
                text="70 ÷ 7",
                style_role="choice",
                x=183.0,
                y=93.0,
                font_size=28,
            ),
            RectSlot(
                id="slot.choice.2", prompt="", x=357.0, y=49.0, width=186.0, height=68.0
            ),
            TextSlot(
                id="slot.choice.2.text",
                prompt="",
                text="90 ÷ 5",
                style_role="choice",
                x=425.0,
                y=93.0,
                font_size=28,
            ),
            RectSlot(
                id="slot.choice.3", prompt="", x=604.0, y=49.0, width=186.0, height=68.0
            ),
            TextSlot(
                id="slot.choice.3.text",
                prompt="",
                text="60 ÷ 3",
                style_role="choice",
                x=672.0,
                y=93.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.answer",
                prompt="",
                text="(정답) 60 ÷ 3",
                style_role="body",
                x=96.0,
                y=165.0,
                font_size=22,
            ),
            TextSlot(
                id="slot.solution",
                prompt="",
                text="(해설) 70 ÷ 7 = 10, 90 ÷ 5 = 18, 60 ÷ 3 = 20",
                style_role="body",
                x=96.0,
                y=194.0,
                font_size=20,
            ),
            TextSlot(
                id="slot.solution.final",
                prompt="",
                text="따라서 10<18<20 이므로 몫이 가장 큰 것은 60 ÷ 3 입니다.",
                style_role="body",
                x=96.0,
                y=220.0,
                font_size=20,
            ),
            TextSlot(
                id="slot.t10",
                prompt="",
                text="10",
                style_role="body",
                x=10.0,
                y=252.0,
                font_size=1,
            ),
            TextSlot(
                id="slot.t18",
                prompt="",
                text="18",
                style_role="body",
                x=14.0,
                y=252.0,
                font_size=1,
            ),
            TextSlot(
                id="slot.t20",
                prompt="",
                text="20",
                style_role="body",
                x=18.0,
                y=252.0,
                font_size=1,
            ),
            TextSlot(
                id="slot.lt",
                prompt="",
                text="<",
                style_role="body",
                x=22.0,
                y=252.0,
                font_size=1,
            ),
            TextSlot(
                id="slot.comp",
                prompt="",
                text="10<18<20",
                style_role="body",
                x=26.0,
                y=252.0,
                font_size=1,
            ),
        ),
        diagrams=(),
        groups=(),
        constraints=(),
        tags=(),
    )


PROBLEM_TEMPLATE = build_problem_template()

SEMANTIC_OVERRIDE = {
    "problem_id": "S3_초등_3_008583",
    "problem_type": "multiple_choice_comparison",
    "metadata": {
        "language": "ko",
        "question": "몫이 가장 큰 것을 선택하세요.",
        "instruction": "나눗셈 식의 결과를 비교하여 가장 큰 것을 고른다.",
    },
    "domain": {
        "objects": [
            {
                "id": "obj.choice1",
                "type": "division_expression",
                "expression": "70 ÷ 7",
            },
            {
                "id": "obj.choice2",
                "type": "division_expression",
                "expression": "90 ÷ 5",
            },
            {
                "id": "obj.choice3",
                "type": "division_expression",
                "expression": "60 ÷ 3",
            },
        ],
        "relations": [],
        "problem_solving": {
            "understand": {
                "given_refs": ["obj.choice1", "obj.choice2", "obj.choice3"],
                "target_ref": "answer.target",
                "condition_refs": ["rel.compare"],
            },
            "plan": {
                "method": "compute_and_compare",
                "description": "각 나눗셈 식의 값을 구한 뒤 가장 큰 값을 가지는 선택지를 찾는다.",
            },
            "execute": {"expected_operations": ["division", "comparison"]},
            "review": {"check_methods": ["largest_value_check"]},
        },
    },
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {
            "type": "largest_expression",
            "description": "결과가 가장 큰 나눗셈 식",
        },
        "value": "60 ÷ 3",
        "unit": "",
    },
}

SOLVABLE = {
    "schema": "modu.solvable.v1.1",
    "problem_id": "S3_초등_3_008583",
    "problem_type": "multiple_choice_comparison",
    "inputs": {
        "total_ticks": 3,
        "target_label": "가장 큰 나눗셈 식",
        "target_ticks": 1,
        "target_count": 1,
        "unit": "",
    },
    "given": [
        {"ref": "obj.choice1", "value": {"expression": "70 ÷ 7"}},
        {"ref": "obj.choice2", "value": {"expression": "90 ÷ 5"}},
        {"ref": "obj.choice3", "value": {"expression": "60 ÷ 3"}},
    ],
    "target": {"ref": "answer.target", "type": "largest_expression"},
    "method": "compute_and_compare",
    "plan": [
        "각 나눗셈 식의 값을 구한다.",
        "구한 값들을 비교하여 가장 큰 값을 찾는다.",
    ],
    "steps": [
        {"id": "step.1", "expr": "70 ÷ 7", "value": 10},
        {"id": "step.2", "expr": "90 ÷ 5", "value": 18},
        {"id": "step.3", "expr": "60 ÷ 3", "value": 20},
        {"id": "step.4", "expr": "10 < 18 < 20", "value": "60 ÷ 3"},
    ],
    "checks": [
        {
            "id": "check.1",
            "expr": "70 ÷ 7 = 10",
            "expected": 10,
            "actual": 10,
            "pass": True,
        },
        {
            "id": "check.2",
            "expr": "90 ÷ 5 = 18",
            "expected": 18,
            "actual": 18,
            "pass": True,
        },
        {
            "id": "check.3",
            "expr": "60 ÷ 3 = 20",
            "expected": 20,
            "actual": 20,
            "pass": True,
        },
    ],
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {
            "type": "largest_expression",
            "description": "결과가 가장 큰 나눗셈 식",
        },
        "value": "60 ÷ 3",
        "unit": "",
    },
}
