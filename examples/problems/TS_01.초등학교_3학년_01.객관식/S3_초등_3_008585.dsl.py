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
        id="S3_초등_3_008585",
        title="나눗셈의 몫이 큰 것부터 기호를 쓰기",
        canvas=Canvas(width=960, height=380, coordinate_mode="logical"),
        regions=(
            Region(
                id="region.stem",
                role="stem",
                flow="absolute",
                slot_ids=(
                    "slot.q1",
                    "slot.box",
                    "slot.item1",
                    "slot.item2",
                    "slot.item3",
                ),
            ),
            Region(
                id="region.choices",
                role="choices",
                flow="absolute",
                slot_ids=(
                    "slot.choice1",
                    "slot.choice2",
                    "slot.choice3",
                    "slot.choice4",
                ),
            ),
            Region(
                id="region.explain",
                role="explanation",
                flow="absolute",
                slot_ids=(),
            ),
        ),
        slots=(
            TextSlot(
                id="slot.q1",
                prompt="",
                text = '몫이 큰 것부터 차례로 기호를 쓴 것으로 알맞은 것을 선택하세요.', style_role="question",
                x=24.0,
                y=28.0,
                font_size=28,
            ),
            RectSlot(
                id="slot.box",
                prompt="",
                x = 120, y = 50, width = 625, height = 80, fill="none",
                stroke="#ff9a45",
            ),
            TextSlot(
                id="slot.item1",
                prompt="",
                text = '㉠ 51 ÷ 3', style_role="body",
                x = 150, y = 100, font_size = 30),
            TextSlot(
                id="slot.item2",
                prompt="",
                text = '㉡ 44 ÷ 2', style_role="body",
                x = 365, y = 100, font_size = 30),
            TextSlot(
                id="slot.item3",
                prompt="",
                text = '㉢ 77 ÷ 7', style_role="body",
                x = 570, y = 100, font_size = 30),
            TextSlot(
                id="slot.choice1",
                prompt="",
                text = '① ㄱ ㄴ ㄷ', style_role="choice",
                x = 95, y = 175, font_size = 30),
            TextSlot(
                id="slot.choice2",
                prompt="",
                text = '② ㄴ ㄷ ㄱ', style_role="choice",
                x = 550, y = 175, font_size = 30),
            TextSlot(
                id="slot.choice3",
                prompt="",
                text = '③ ㄴ ㄱ ㄷ', style_role="choice",
                x = 95, y = 225, font_size = 30),
            TextSlot(
                id="slot.choice4",
                prompt="",
                text = '④ ㄷ ㄱ ㄴ', style_role="choice",
                x = 550, y = 225, font_size = 30),
            
        ),
        diagrams=(),
        groups=(),
        constraints=(),
        tags=(),
    )


PROBLEM_TEMPLATE = build_problem_template()

SEMANTIC_OVERRIDE = {
    "problem_id": "S3_초등_3_008585",
    "problem_type": "comparison_ordering",
    "metadata": {
        "language": "ko",
        "question": "묵이 큰 것부터 차례로 기호를 쓴 것으로 알맞은 것을 선택하는 문제",
        "instruction": "나눗셈의 몫이 큰 것부터 차례로 기호를 고른다.",
        "points": 5,
    },
    "domain": {
        "objects": [
            {
                "id": "obj.a",
                "type": "division_expression",
                "symbol": "ㄱ",
                "dividend": 51,
                "divisor": 3,
            },
            {
                "id": "obj.b",
                "type": "division_expression",
                "symbol": "ㄴ",
                "dividend": 44,
                "divisor": 2,
            },
            {
                "id": "obj.c",
                "type": "division_expression",
                "symbol": "ㄷ",
                "dividend": 77,
                "divisor": 7,
            },
        ],
        "relations": [],
        "problem_solving": {
            "understand": {
                "given_refs": ["obj.a", "obj.b", "obj.c"],
                "target_ref": "answer.target",
                "condition_refs": ["rel.order"],
            },
            "plan": {
                "method": "compute_and_compare",
                "description": "각 나눗셈의 몫을 구한 뒤 큰 것부터 순서를 정한다.",
            },
            "execute": {"expected_operations": ["division", "comparison", "ordering"]},
            "review": {"check_methods": ["compare_quotients", "match_choice_order"]},
        },
    },
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {"type": "symbol_order", "description": "몫이 큰 것부터의 기호 순서"},
        "value": 3,
        "unit": "",
    },
}

SOLVABLE = {
    "schema": "modu.solvable.v1.1",
    "problem_id": "S3_초등_3_008585",
    "problem_type": "comparison_ordering",
    "inputs": {
        "total_ticks": 3,
        "target_label": "기호 순서",
        "target_ticks": 3,
        "target_count": 3,
        "unit": "",
    },
    "given": [
        {"ref": "obj.a", "value": {"symbol": "ㄱ", "dividend": 51, "divisor": 3}},
        {"ref": "obj.b", "value": {"symbol": "ㄴ", "dividend": 44, "divisor": 2}},
        {"ref": "obj.c", "value": {"symbol": "ㄷ", "dividend": 77, "divisor": 7}},
    ],
    "target": {"ref": "answer.target", "type": "symbol_order"},
    "method": "compute_and_compare",
    "plan": [
        "각 나눗셈의 몫을 구합니다.",
        "몫을 큰 것부터 작은 것 순으로 비교합니다.",
        "그 순서에 맞는 기호 배열을 찾습니다.",
    ],
    "steps": [
        {"id": "step.1", "expr": "51 ÷ 3", "value": 17},
        {"id": "step.2", "expr": "44 ÷ 2", "value": 22},
        {"id": "step.3", "expr": "77 ÷ 7", "value": 11},
        {"id": "step.4", "expr": "22 > 17 > 11", "value": ["ㄴ", "ㄱ", "ㄷ"]},
    ],
    "checks": [
        {
            "id": "check.1",
            "expr": "17 == 51 ÷ 3",
            "expected": 17,
            "actual": 17,
            "pass": True,
        },
        {
            "id": "check.2",
            "expr": "22 == 44 ÷ 2",
            "expected": 22,
            "actual": 22,
            "pass": True,
        },
        {
            "id": "check.3",
            "expr": "11 == 77 ÷ 7",
            "expected": 11,
            "actual": 11,
            "pass": True,
        },
    ],
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {"type": "symbol_order", "description": "몫이 큰 것부터의 기호 순서"},
        "value": 3,
        "unit": "",
    },
}
