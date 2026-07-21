from __future__ import annotations

from modu_math.dsl import (
    BlankSlot,
    Canvas,
    ProblemTemplate,
    Region,
    TextBoxSlot,
)


PROBLEM_ID = "P3_1_01_00040_07648"
PROBLEM_TITLE = "작은 수의 2배인 큰 수 구하기"


def build_problem_template() -> ProblemTemplate:
    return ProblemTemplate(
        id=PROBLEM_ID,
        title=PROBLEM_TITLE,
        canvas=Canvas(
            width=900,
            height=230,
            coordinate_mode="logical",
        ),
        regions=(
            Region(
                id="region.stem",
                role="stem",
                flow="vertical",
                slot_ids=("slot.question",),
            ),
        ),
        slots=(
            TextBoxSlot(
                id="slot.question",
                x=48,
                y=30,
                width=804,
                height=90,
                text=(
                    "서로 다른 두 수가 있습니다. 두 수 중 큰 수는 작은 수의 "
                    "2배입니다. 두 수의 합이 735라면 큰 수는 얼마입니까?"
                ),
                font_size=24,
                font_family="Noto Sans KR",
                fill="#202124",
                line_height=1.5,
                align="left",
                valign="top",
            ),
            BlankSlot(
                id="slot.answer",
                prompt="답",
                answer_key="490",
                placeholder="",
            ),
        ),
    )


PROBLEM_TEMPLATE = build_problem_template()


SEMANTIC = {
    "problem_id": PROBLEM_ID,
    "problem_type": "numeric_answer_ratio_part_whole_problem",
    "metadata": {
        "grade": 3,
        "semester": 1,
        "subject": "수학",
        "topic": "곱셈과 나눗셈을 활용한 문제 해결",
        "language": "ko-KR",
    },
    "domain": {
        "objects": [
            {
                "id": "number.smaller",
                "type": "number",
                "label": "작은 수",
                "value": 245,
            },
            {
                "id": "number.larger",
                "type": "number",
                "label": "큰 수",
                "value": 490,
            },
            {
                "id": "number.sum",
                "type": "number",
                "label": "두 수의 합",
                "value": 735,
            },
            {
                "id": "quantity.smaller_part_count",
                "type": "quantity",
                "label": "작은 수의 묶음 수",
                "value": 1,
                "unit": "묶음",
            },
            {
                "id": "quantity.larger_part_count",
                "type": "quantity",
                "label": "큰 수의 묶음 수",
                "value": 2,
                "unit": "묶음",
            },
            {
                "id": "quantity.total_part_count",
                "type": "quantity",
                "label": "두 수를 나타내는 전체 묶음 수",
                "value": 3,
                "unit": "묶음",
            },
        ],
        "relations": [
            {
                "id": "relation.larger_is_double",
                "type": "multiple_of",
                "subject": "number.larger",
                "object": "number.smaller",
                "multiplier": 2,
            },
            {
                "id": "relation.sum_of_two_numbers",
                "type": "sum_of",
                "subject": "number.sum",
                "objects": [
                    "number.smaller",
                    "number.larger",
                ],
            },
            {
                "id": "relation.total_parts",
                "type": "sum_of",
                "subject": "quantity.total_part_count",
                "objects": [
                    "quantity.smaller_part_count",
                    "quantity.larger_part_count",
                ],
            },
        ],
    },
    "answer": {
        "type": "numeric",
        "value": 490,
        "unit": "",
        "target_ref": "number.larger",
    },
}

SEMANTIC_OVERRIDE = SEMANTIC


SOLVABLE = {
    "schema": "modu.solvable.v1.2",
    "problem_id": PROBLEM_ID,
    "problem_type": "numeric_answer_ratio_part_whole_problem",
    "inputs": {
        "target_label": "큰 수",
        "unit": "",
        "quantities": {
            "sum": 735,
            "smaller_multiplier": 1,
            "larger_multiplier": 2,
            "total_part_count": 3,
        },
        "conditions": [
            "서로 다른 두 수가 있습니다.",
            "큰 수는 작은 수의 2배입니다.",
            "두 수의 합은 735입니다.",
        ],
    },
    "given": [
        {
            "ref": "number.sum",
            "value": 735,
        },
        {
            "ref": "relation.larger_is_double",
            "value": {
                "larger_ref": "number.larger",
                "smaller_ref": "number.smaller",
                "multiplier": 2,
            },
        },
    ],
    "target": {
        "ref": "number.larger",
        "type": "number",
    },
    "method": (
        "작은 수를 1묶음으로 보면 큰 수는 2묶음이므로 두 수의 합은 "
        "3묶음입니다. 735를 3으로 나누어 한 묶음의 값을 구한 뒤 2배합니다."
    ),
    "plan": [
        "작은 수를 1묶음으로 나타냅니다.",
        "큰 수는 작은 수의 2배이므로 2묶음으로 나타냅니다.",
        "두 수의 합 735가 모두 3묶음임을 확인합니다.",
        "735를 3으로 나누어 작은 수를 구합니다.",
        "작은 수를 2배하여 큰 수를 구합니다.",
    ],
    "steps": [
        {
            "id": "step.find_total_part_count",
            "goal": "두 수의 합이 몇 묶음인지 구합니다.",
            "uses": [
                "quantity.smaller_part_count",
                "quantity.larger_part_count",
            ],
            "relation_expr": "전체 묶음 수 = 작은 수의 묶음 수 + 큰 수의 묶음 수",
            "expr": "1 + 2",
            "value": 3,
            "explanation": "작은 수는 1묶음이고 큰 수는 2묶음이므로 모두 3묶음입니다.",
        },
        {
            "id": "step.find_smaller_number",
            "goal": "한 묶음인 작은 수를 구합니다.",
            "uses": [
                "number.sum",
                "quantity.total_part_count",
            ],
            "relation_expr": "작은 수 = 두 수의 합 ÷ 전체 묶음 수",
            "expr": "735 / 3",
            "value": 245,
            "explanation": "두 수의 합 735를 같은 크기의 3묶음으로 나눕니다.",
        },
        {
            "id": "step.find_larger_number",
            "goal": "작은 수의 2배인 큰 수를 구합니다.",
            "uses": [
                "number.smaller",
                "relation.larger_is_double",
            ],
            "relation_expr": "큰 수 = 작은 수 × 2",
            "expr": "245 * 2",
            "value": 490,
            "explanation": "큰 수는 작은 수 245의 2배이므로 245에 2를 곱합니다.",
        },
    ],
    "checks": [
        {
            "id": "check.sum",
            "description": "작은 수와 큰 수를 더하면 735가 되는지 확인합니다.",
            "expr": "245 + 490",
            "expected": 735,
            "actual": 735,
            "pass": True,
        },
        {
            "id": "check.double_relation",
            "description": "큰 수가 작은 수의 2배인지 확인합니다.",
            "expr": "245 * 2",
            "expected": 490,
            "actual": 490,
            "pass": True,
        },
        {
            "id": "check_numbers_are_different",
            "description": "두 수가 서로 다른지 확인합니다.",
            "expr": "245 != 490",
            "expected": True,
            "actual": True,
            "pass": True,
        },
    ],
    "answer": {
        "type": "numeric",
        "value": 490,
        "unit": "",
        "target_ref": "number.larger",
    },
    "understanding": {
        "summary": (
            "큰 수가 작은 수의 2배이고 두 수의 합이 735일 때, "
            "두 수를 모두 3개의 같은 묶음으로 나타내어 큰 수를 구하는 문제입니다."
        ),
        "facts": [
            {
                "ref": "number.sum",
                "label": "두 수의 합",
                "value": 735,
                "source": "explicit",
            },
            {
                "ref": "relation.larger_is_double",
                "label": "큰 수와 작은 수의 관계",
                "value": 2,
                "unit": "배",
                "source": "explicit",
            },
        ],
        "unknowns": [
            {
                "ref": "number.larger",
                "label": "큰 수",
                "source": "unknown",
            },
        ],
        "relation": {
            "type": "part_ratio_sum",
            "statement": (
                "작은 수를 1묶음으로 나타내면 큰 수는 2묶음이고, "
                "두 수의 합은 3묶음입니다."
            ),
            "symbolic": "x + 2x = 735, 3x = 735",
            "uses": [
                "number.smaller",
                "number.larger",
                "number.sum",
            ],
            "result": "number.larger",
        },
        "diagnostic_questions": [
            {
                "id": "understand.target",
                "type": "multiple_choice",
                "prompt": "이 문제에서 구해야 하는 것은 무엇인가요?",
                "choices": [
                    "작은 수",
                    "큰 수",
                    "두 수의 합",
                ],
                "answer_index": 1,
            },
            {
                "id": "understand.part_count",
                "type": "multiple_choice",
                "prompt": "작은 수를 1묶음으로 보면 두 수의 합은 모두 몇 묶음인가요?",
                "choices": [
                    "2묶음",
                    "3묶음",
                    "4묶음",
                ],
                "answer_index": 1,
            },
            {
                "id": "understand.first_operation",
                "type": "multiple_choice",
                "prompt": "작은 수를 구하려면 먼저 어떻게 계산해야 하나요?",
                "choices": [
                    "735를 2로 나눕니다.",
                    "735를 3으로 나눕니다.",
                    "735에 2를 곱합니다.",
                ],
                "answer_index": 1,
            },
        ],
        "student_restatement": {
            "prompt": "문제의 뜻을 말해 볼까요?",
            "template": (
                "작은 수를 {small_parts}묶음으로 보면 큰 수는 {large_parts}묶음이고, "
                "두 수의 합 {sum}을 이용하여 {target}를 구합니다."
            ),
            "answer": (
                "작은 수를 1묶음으로 보면 큰 수는 2묶음이고, "
                "두 수의 합 735를 이용하여 큰 수를 구합니다."
            ),
        },
    },
}


SEMANTIC_ANSWER = SOLVABLE["answer"]
