from __future__ import annotations
from modu_math.dsl import (
    Canvas,
    ProblemTemplate,
    Region,
    TextSlot,
    RectSlot,
    CircleSlot,
    LineSlot,
    PolygonSlot,
)


def build_problem_template() -> ProblemTemplate:
    return ProblemTemplate(
        id="S3_초등_3_008541",
        title="계산 결과가 큰 것부터 차례대로 나열한 것을 고르시오",
        canvas=Canvas(width=940, height=394, coordinate_mode="logical"),
        regions=(
            Region(
                id="region.stem",
                role="stem",
                flow="absolute",
                slot_ids=(
                    "slot.q0",
                    "slot.q1",
                    "slot.box",
                    "slot.expr1",
                    "slot.expr2",
                    "slot.expr3",
                    "slot.opt1",
                    "slot.opt2",
                    "slot.opt3",
                    "slot.opt4",
                    
                ),
            ),
        ),
        slots=(
            TextSlot(
                id="slot.q1",
                prompt="",
                text="계산 결과가 큰 것부터 차례대로 나열한 것을 고르시오.",
                style_role="question",
                x = 50, y = 30, font_size=28,
            ),
            RectSlot(
                id="slot.box",
                prompt="",
                x = 45, y = 50, width=765.0,
                height=78.0,
                fill="#FBE7C4",
                stroke="#FBE7C4",
                stroke_width=1.0,
            ),
            TextSlot(
                id="slot.expr1",
                prompt="",
                text="ㄱ. 397 × 6",
                style_role="body",
                x = 145, y = 100, font_size=28,
            ),
            TextSlot(
                id="slot.expr2",
                prompt="",
                text="ㄴ. 549 × 4",
                style_role="body",
                x = 355, y = 100, font_size=28,
            ),
            TextSlot(
                id="slot.expr3",
                prompt="",
                text="ㄷ. 456 × 5",
                style_role="body",
                x = 585, y = 100, font_size=28,
            ),
            TextSlot(
                id="slot.opt1",
                prompt="",
                text = '① ㄱ ㄴ ㄷ', style_role="body",
                x = 105, y = 190, font_size=28,
            ),
            TextSlot(
                id="slot.opt2",
                prompt="",
                text="② ㄱ ㄷ ㄴ",
                style_role="body",
                x = 475, y = 190, font_size=28,
            ),
            TextSlot(
                id="slot.opt3",
                prompt="",
                text="③ ㄴ ㄷ ㄱ",
                style_role="body",
                x = 105, y = 250, font_size=28,
            ),
            TextSlot(
                id="slot.opt4",
                prompt="",
                text="④ ㄷ ㄴ ㄱ",
                style_role="body",
                x = 475, y = 245, font_size=28,
            ),
            
        ),
        diagrams=(),
        groups=(),
        constraints=(),
        tags=(),
    )


PROBLEM_TEMPLATE = build_problem_template()

SEMANTIC_OVERRIDE = {
    "problem_id": "S3_초등_3_008541",
    "problem_type": "multiple_choice_ordering",
    "metadata": {
        "language": "ko",
        "question": "계산 결과가 큰 것부터 차례대로 나열한 것을 고르시오.",
        "instruction": "보기에서 계산 결과가 큰 것부터 차례대로 나열한 것을 고르시오.",
    },
    "domain": {
        "objects": [
            {
                "id": "obj.a",
                "type": "expression",
                "label": "ㄱ",
                "operation": "397 × 6",
            },
            {
                "id": "obj.b",
                "type": "expression",
                "label": "ㄴ",
                "operation": "549 × 4",
            },
            {
                "id": "obj.c",
                "type": "expression",
                "label": "ㄷ",
                "operation": "456 × 5",
            },
            {
                "id": "obj.option2",
                "type": "choice",
                "label": "②",
                "sequence": ["ㄱ", "ㄷ", "ㄴ"],
            },
        ],
        "relations": [
            {
                "id": "rel.order",
                "type": "descending_order",
                "from_id": "obj.a",
                "to_id": "obj.b",
            }
        ],
    },
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {
            "type": "choice_number",
            "description": "계산 결과가 큰 것부터 차례대로 나열한 보기 번호",
        },
        "value": 2,
        "unit": "",
    },
}

SOLVABLE = {
    "schema": "modu.solvable.v1.1",
    "problem_id": "S3_초등_3_008541",
    "problem_type": "multiple_choice_ordering",
    "inputs": {
        "total_ticks": 3,
        "target_label": "보기 번호",
        "target_ticks": 1,
        "target_count": 1,
        "unit": "",
    },
    "given": [
        {"ref": "obj.a", "value": {"label": "ㄱ", "expr": "397 × 6"}},
        {"ref": "obj.b", "value": {"label": "ㄴ", "expr": "549 × 4"}},
        {"ref": "obj.c", "value": {"label": "ㄷ", "expr": "456 × 5"}},
    ],
    "target": {"ref": "answer.target", "type": "choice_number"},
    "method": "compare_results_descending",
    "plan": [
        "각 곱셈식의 결과를 구한 뒤 큰 값부터 작은 값 순서로 비교합니다.",
        "비교한 순서와 같은 보기 번호를 찾습니다.",
    ],
    "steps": [
        {"id": "step.1", "expr": "397 × 6", "value": 2382},
        {"id": "step.2", "expr": "549 × 4", "value": 2196},
        {"id": "step.3", "expr": "456 × 5", "value": 2280},
        {"id": "step.4", "expr": "2382 > 2280 > 2196", "value": "ㄱ, ㄷ, ㄴ"},
        {"id": "step.5", "expr": "보기 대조", "value": "②"},
    ],
    "checks": [
        {
            "id": "check.1",
            "expr": "2382 > 2280 > 2196",
            "expected": True,
            "actual": True,
            "pass": True,
        },
        {
            "id": "check.2",
            "expr": "보기 ②의 순서",
            "expected": "ㄱ, ㄷ, ㄴ",
            "actual": "ㄱ, ㄷ, ㄴ",
            "pass": True,
        },
    ],
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {
            "type": "choice_number",
            "description": "계산 결과가 큰 것부터 차례대로 나열한 보기 번호",
        },
        "value": 2,
        "unit": "",
    },
}
