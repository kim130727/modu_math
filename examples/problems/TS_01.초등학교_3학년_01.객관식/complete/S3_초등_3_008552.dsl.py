from __future__ import annotations
from modu_math.dsl import (
    Canvas,
    CircleSlot,
    LineSlot,
    ProblemTemplate,
    RectSlot,
    Region,
    TextSlot,
)

def build_problem_template() -> ProblemTemplate:
    return ProblemTemplate(
        id="S3_초등_3_008552",
        title="곱이 큰 것부터 차례대로 나열한 것을 고르기",
        canvas=Canvas(width=750, height=360, coordinate_mode="logical"),
        regions=(
            Region(
                id="region.header",
                role="stem",
                flow="absolute",
                slot_ids=("slot.q.text"),
            ),
            Region(
                id="region.mainbox",
                role="diagram",
                flow="absolute",
                slot_ids=(
                    "slot.box",
                    "slot.a.label",
                    "slot.a.expr",
                    "slot.b.label",
                    "slot.b.expr",
                    "slot.c.label",
                    "slot.c.expr",
                ),
            ),
            Region(
                id="region.options",
                role="choices",
                flow="absolute",
                slot_ids=(
                    "slot.opt1.no",
                    "slot.opt1.text",
                    "slot.opt2.no",
                    "slot.opt2.text",
                    "slot.opt3.no",
                    "slot.opt3.text",
                    "slot.opt4.no",
                    "slot.opt4.text",
                ),
            ),
            Region(
                id="region.answer",
                role="answer",
                flow="absolute",
                slot_ids=("slot.ans.text",),
            ),
            Region(
                id="region.explain",
                role="explanation",
                flow="absolute",
                slot_ids=("slot.exp.text1", "slot.arrow", "slot.exp.result"),
            ),
        ),
        slots=(
            TextSlot(
                id="slot.q.text",
                prompt="",
                text="곱이 큰 것부터 차례대로 나열한 것을 고르세요.",
                style_role="question",
                x=50.0,
                y=30.0,
                font_size=28,
            ),
            RectSlot(
                id="slot.box",
                prompt="",
                x=60.0,
                y=60.0,
                width=600.0,
                height=80.0,
                fill="none",
                stroke="#f6b3bf",
                stroke_width=1.5,
            ),

            TextSlot(
                id="slot.a.expr",
                prompt="",
                text="ㄱ. 7 × 56",
                style_role="question",
                x=150.0,
                y=110.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.b.expr",
                prompt="",
                text="ㄴ. 8 × 18",
                style_role="question",
                x=300.0,
                y=110.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.c.expr",
                prompt="",
                text="ㄷ. 9 × 73",
                style_role="question",
                x=450.0,
                y=110.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.opt1.text",
                prompt="",
                text="① ㄱ ㄴ ㄷ",
                style_role="choice",
                x=100.0,
                y=200.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.opt2.text",
                prompt="",
                text="② ㄴ ㄱ ㄷ",
                style_role="choice",
                x=350.0,
                y=200.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.opt3.text",
                prompt="",
                text="③ ㄷ ㄴ ㄱ",
                style_role="choice",
                x=100.0,
                y=250.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.opt4.text",
                prompt="",
                text="④ ㄷ ㄱ ㄴ",
                style_role="choice",
                x=350.0,
                y=250.0,
                font_size=28,
            ),
        ),
        diagrams=(),
        groups=(),
        constraints=(),
        tags=("초등수학", "곱셈비교", "객관식"),
    )


PROBLEM_TEMPLATE = build_problem_template()

SEMANTIC_OVERRIDE = {
    "problem_id": "S3_초등_3_008552",
    "problem_type": "multiple_choice",
    "metadata": {
        "language": "ko",
        "question": "곱이 큰 것부터 차례대로 나열한 것을 고르세요.",
        "instruction": "세 곱셈식의 값의 크기를 비교하여 순서를 찾는다.",
    },
    "domain": {
        "objects": [
            {
                "id": "obj.g",
                "type": "expression",
                "label": "ㄱ",
                "expression": "7 × 56",
            },
            {
                "id": "obj.n",
                "type": "expression",
                "label": "ㄴ",
                "expression": "8 × 18",
            },
            {
                "id": "obj.d",
                "type": "expression",
                "label": "ㄷ",
                "expression": "9 × 73",
            },
        ],
        "relations": [],
        "problem_solving": {
            "understand": {
                "given_refs": ["obj.g", "obj.n", "obj.d"],
                "target_ref": "answer.target",
                "condition_refs": ["rel.compare", "rel.order"],
            },
            "plan": {
                "method": "compute_products_and_compare",
                "description": "각 곱셈식의 값을 구한 뒤 큰 것부터 작은 것 순서로 기호를 배열한다.",
            },
            "execute": {
                "expected_operations": [
                    "multiply_each_expression",
                    "compare_products",
                    "choose_matching_option",
                ]
            },
            "review": {
                "check_methods": ["descending_order_check", "option_match_check"]
            },
        },
    },
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {
            "type": "choice_number",
            "description": "곱이 큰 것부터 차례대로 나열한 보기 번호",
        },
        "value": 4,
        "unit": "",
    },
}

SOLVABLE = {
    "schema": "modu.solvable.v1.1",
    "problem_id": "S3_초등_3_008552",
    "problem_type": "multiple_choice",
    "inputs": {
        "total_ticks": 3,
        "target_label": "정답 보기 번호",
        "target_ticks": 1,
        "target_count": 1,
        "unit": "",
    },
    "given": [
        {"ref": "obj.g", "value": {"expression": "7 × 56"}},
        {"ref": "obj.n", "value": {"expression": "8 × 18"}},
        {"ref": "obj.d", "value": {"expression": "9 × 73"}},
    ],
    "target": {"ref": "answer.target", "type": "choice_number"},
    "method": "compute_products_and_compare",
    "plan": [
        "각 곱셈식의 값을 구한다.",
        "값을 큰 것부터 작은 것 순서로 비교한다.",
        "그 순서에 해당하는 보기를 찾는다.",
    ],
    "steps": [
        {"id": "step.1", "expr": "7 × 56", "value": 392},
        {"id": "step.2", "expr": "8 × 18", "value": 144},
        {"id": "step.3", "expr": "9 × 73", "value": 657},
        {"id": "step.4", "expr": "657 > 392 > 144", "value": ["ㄷ", "ㄱ", "ㄴ"]},
        {"id": "step.5", "expr": "보기 번호 확인", "value": 4},
    ],
    "checks": [
        {
            "id": "check.1",
            "expr": "657 > 392 > 144",
            "expected": True,
            "actual": True,
            "pass": True,
        },
        {
            "id": "check.2",
            "expr": "정답 보기와 일치 여부",
            "expected": 4,
            "actual": 4,
            "pass": True,
        },
    ],
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {
            "type": "choice_number",
            "description": "곱이 큰 것부터 차례대로 나열한 보기 번호",
        },
        "value": 4,
        "unit": "",
    },
}
