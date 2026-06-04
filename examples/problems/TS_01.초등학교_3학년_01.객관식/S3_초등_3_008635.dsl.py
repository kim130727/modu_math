from __future__ import annotations
from modu_math.dsl import Canvas, ProblemTemplate, Region, RectSlot, TextSlot


def build_problem_template() -> ProblemTemplate:
    return ProblemTemplate(
        id="S3_초등_3_008635",
        title="두 식의 계산 결과가 같을 때 알맞은 수",
        canvas=Canvas(width=841, height=374, coordinate_mode="logical"),
        regions=(
            Region(
                id="region.stem",
                role="stem",
                flow="absolute",
                slot_ids=(
                    "slot.qbox",
                    "slot.qtext",
                    "slot.expr.left",
                    "slot.expr.right",
                    "slot.opt.1",
                    "slot.opt.2",
                    "slot.opt.3",
                    "slot.opt.4",
                    "slot.opt.5",
                ),
            ),
            Region(
                id="region.answer_explanation",
                role="explanation",
                flow="absolute",
                slot_ids=(
                    "slot.ans",
                    "slot.exp",
                ),
            ),
        ),
        slots=(
            TextSlot(
                id="slot.qbox",
                prompt="",
                text="□",
                style_role="question",
                x=9.0,
                y=28.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.qtext",
                prompt="",
                text="7. 다음 두 식의 계산 결과가 같을 때 □ 안에 알맞은 수를 고르세요.",
                style_role="question",
                x=38.0,
                y=28.0,
                font_size=28,
            ),
            RectSlot(
                id="slot.expr.left",
                prompt="",
                x=231.0,
                y=50.0,
                width=175.0,
                height=43.0,
            ),
            RectSlot(
                id="slot.expr.right",
                prompt="",
                x=462.0,
                y=50.0,
                width=187.0,
                height=43.0,
            ),
            TextSlot(
                id="slot.opt.1",
                prompt="",
                text="① 2",
                style_role="question",
                x=17.0,
                y=130.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.opt.2",
                prompt="",
                text="② 3",
                style_role="question",
                x=250.0,
                y=130.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.opt.3",
                prompt="",
                text="③ 4",
                style_role="question",
                x=582.0,
                y=130.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.opt.4",
                prompt="",
                text="④ 6",
                style_role="question",
                x=17.0,
                y=184.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.opt.5",
                prompt="",
                text="⑤ 8",
                style_role="question",
                x=250.0,
                y=184.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.ans",
                prompt="",
                text="(정답) ③",
                style_role="supporting",
                x=17.0,
                y=240.0,
                font_size=22,
            ),
            TextSlot(
                id="slot.exp",
                prompt="",
                text="(해설) 80 ÷ 5 = 16이고 □ × 4 = 16에서 4 × 4 = 16이므로 □ = 4입니다.",
                style_role="supporting",
                x=17.0,
                y=280.0,
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
    "problem_id": "S3_초등_3_008635",
    "problem_type": "equation_comparison_multiple_choice",
    "metadata": {
        "language": "ko",
        "question": "두 식의 계산 결과가 같을 때 빈칸에 알맞은 수를 고르는 문제",
        "instruction": "□ 안에 알맞은 수를 고르세요.",
    },
    "domain": {
        "objects": [
            {
                "id": "obj.left_expression",
                "type": "arithmetic_expression",
                "expression": "80 ÷ 5",
            },
            {
                "id": "obj.right_expression",
                "type": "arithmetic_expression",
                "expression": "□ × 4",
            },
            {
                "id": "obj.options",
                "type": "multiple_choice_options",
                "choices": [2, 3, 4, 6, 8],
            },
        ],
        "relations": [],
        "problem_solving": {
            "understand": {
                "given_refs": [
                    "obj.left_expression",
                    "obj.right_expression",
                    "obj.options",
                ],
                "target_ref": "answer.target",
                "condition_refs": ["rel.equal_results"],
            },
            "plan": {
                "method": "compare_results",
                "description": "왼쪽 식의 값을 먼저 보고, 오른쪽 식이 같은 값이 되도록 빈칸의 수를 찾는다.",
            },
            "execute": {
                "expected_operations": [
                    "evaluate_left_expression",
                    "match_right_expression_result",
                    "select_matching_option",
                ]
            },
            "review": {
                "check_methods": [
                    "substitute_choice_into_right_expression",
                    "confirm_equal_results",
                ]
            },
        },
    },
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {"type": "missing_number", "description": "□에 들어갈 수"},
        "value": 4,
        "unit": "",
    },
}

SOLVABLE = {
    "schema": "modu.solvable.v1.1",
    "problem_id": "S3_초등_3_008635",
    "problem_type": "equation_comparison_multiple_choice",
    "inputs": {
        "total_ticks": 5,
        "target_label": "□",
        "target_ticks": 1,
        "target_count": 1,
        "unit": "",
    },
    "given": [
        {"ref": "obj.left_expression", "value": "80 ÷ 5"},
        {"ref": "obj.right_expression", "value": "□ × 4"},
        {"ref": "obj.options", "value": [2, 3, 4, 6, 8]},
    ],
    "target": {"ref": "answer.target", "type": "missing_number"},
    "method": "compare_results",
    "plan": [
        "왼쪽 식의 값을 구한다.",
        "오른쪽 식이 같은 값이 되도록 □에 들어갈 수를 찾는다.",
        "보기에서 해당 값을 고른다.",
    ],
    "steps": [
        {"id": "step.1", "expr": "80 ÷ 5", "value": 16},
        {"id": "step.2", "expr": "□ × 4 = 16", "value": 16},
        {"id": "step.3", "expr": "16 ÷ 4", "value": 4},
        {"id": "step.4", "expr": "보기에서 4를 고른다", "value": 4},
    ],
    "checks": [
        {"id": "check.1", "expr": "4 × 4", "expected": 16, "actual": 16, "pass": True},
        {
            "id": "check.2",
            "expr": "80 ÷ 5 == 4 × 4",
            "expected": True,
            "actual": True,
            "pass": True,
        },
    ],
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {"type": "missing_number", "description": "□에 들어갈 수"},
        "value": 4,
        "unit": "",
    },
}
