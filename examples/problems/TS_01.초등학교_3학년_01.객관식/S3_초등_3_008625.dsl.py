from __future__ import annotations
from modu_math.dsl import Canvas, ProblemTemplate, RectSlot, Region, TextSlot


def build_problem_template() -> ProblemTemplate:
    return ProblemTemplate(
        id="S3_초등_3_008625",
        title="몫이 더 큰 것을 선택하세요",
        canvas=Canvas(width=648, height=283, coordinate_mode="logical"),
        regions=(
            Region(
                id="region.header",
                role="stem",
                flow="absolute",
                slot_ids=("slot.box", "slot.qmark", "slot.no"),
            ),
            Region(
                id="region.choice_box",
                role="diagram",
                flow="absolute",
                slot_ids=("slot.frame", "slot.eq1", "slot.eq2"),
            ),
            Region(id="region.answer", role="answer", flow="absolute", slot_ids=()),
            Region(
                id="region.explanation",
                role="explanation",
                flow="absolute",
                slot_ids=(),
            ),
        ),
        slots=(
            RectSlot(id="slot.box", prompt="", x=8.0, y=10.0, width=10.0, height=10.0),
            TextSlot(
                id="slot.qmark",
                prompt="",
                text="95.",
                style_role="question",
                x=34.0,
                y=28.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.no",
                prompt="",
                text="몫이 더 큰 것을 선택하세요.",
                style_role="question",
                x=72.0,
                y=28.0,
                font_size=28,
            ),
            RectSlot(
                id="slot.frame", prompt="", x=316.0, y=48.0, width=270.0, height=74.0
            ),
            TextSlot(
                id="slot.eq1",
                prompt="",
                text="64 ÷ 4",
                style_role="diagram",
                x=364.0,
                y=95.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.eq2",
                prompt="",
                text="84 ÷ 3",
                style_role="diagram",
                x=468.0,
                y=95.0,
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
    "problem_id": "S3_초등_3_008625",
    "problem_type": "quotient_comparison_selection",
    "metadata": {
        "language": "ko",
        "question": "몫이 더 큰 것을 선택하세요.",
        "instruction": "두 나눗셈식의 몫을 비교하여 더 큰 것을 고른다.",
    },
    "domain": {
        "objects": [
            {
                "id": "obj.choice_1",
                "type": "division_expression",
                "expression": "64 ÷ 4",
            },
            {
                "id": "obj.choice_2",
                "type": "division_expression",
                "expression": "84 ÷ 3",
            },
        ],
        "relations": [],
        "problem_solving": {
            "understand": {
                "given_refs": ["obj.choice_1", "obj.choice_2"],
                "target_ref": "answer.target",
                "condition_refs": ["rel.compare_quotients"],
            },
            "plan": {
                "method": "quotient_comparison",
                "description": "두 나눗셈의 몫을 비교하여 더 큰 식을 선택한다.",
            },
            "execute": {
                "expected_operations": [
                    "evaluate_division_expressions",
                    "compare_quotients",
                    "select_larger_quotient",
                ]
            },
            "review": {"check_methods": ["compare_results_consistency"]},
        },
    },
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {
            "type": "selected_division_expression",
            "description": "몫이 더 큰 나눗셈식",
        },
        "value": None,
        "unit": "",
    },
}

SOLVABLE = {
    "schema": "modu.solvable.v1",
    "problem_id": "S3_초등_3_008625",
    "problem_type": "quotient_comparison_selection",
    "inputs": {
        "total_ticks": 0,
        "target_label": "몫이 더 큰 것",
        "target_ticks": 0,
        "target_count": 1,
        "unit": "",
    },
    "given": [
        {"ref": "obj.choice_1", "value": {"expression": "64 ÷ 4"}},
        {"ref": "obj.choice_2", "value": {"expression": "84 ÷ 3"}},
    ],
    "target": {"ref": "answer.target", "type": "selected_division_expression"},
    "method": "quotient_comparison",
    "plan": ["두 나눗셈식의 몫을 구해 비교한다.", "몫이 더 큰 나눗셈식을 선택한다."],
    "steps": [
        {"id": "step.1", "expr": "64 ÷ 4", "value": 16},
        {"id": "step.2", "expr": "84 ÷ 3", "value": 28},
        {"id": "step.3", "expr": "16 < 28", "value": True},
        {"id": "step.4", "expr": "더 큰 몫을 가진 식 선택", "value": "84 ÷ 3"},
    ],
    "checks": [
        {
            "id": "check.1",
            "expr": "16 < 28",
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
            "type": "selected_division_expression",
            "description": "몫이 더 큰 나눗셈식",
        },
        "value": None,
        "unit": "",
    },
}
