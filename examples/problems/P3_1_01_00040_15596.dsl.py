from __future__ import annotations

from modu_math.dsl import (
    BlankSlot,
    Canvas,
    ProblemTemplate,
    Region,
    TextSlot,
)


PROBLEM_ID = "P3_1_01_00040_15596"
PROBLEM_TITLE = "자리 숫자로 만든 수보다 534 큰 수"


def build_problem_template() -> ProblemTemplate:
    return ProblemTemplate(
        id=PROBLEM_ID,
        title=PROBLEM_TITLE,
        canvas=Canvas(
            width=960,
            height=210,
            coordinate_mode="logical",
        ),
        regions=(
            Region(
                id="region.stem",
                role="stem",
                flow="absolute",
                slot_ids=("slot.question",),
            ),
        ),
        slots=(
            TextSlot(
                id="slot.question",
                prompt="",
                text=(
                    "백의 자리 숫자가 4, 십의 자리 숫자가 3, 일의 자리 숫자가 5인 "
                    "수보다 534 많은 수는 얼마입니까?"
                ),
                style_role="question",
                x=30,
                y=35,
                font_size=24,
                fill="#111111",
            ),
            BlankSlot(
                id="slot.answer",
                prompt="답",
                answer_key="969",
                placeholder="수",
            ),
        ),
    )


PROBLEM_TEMPLATE = build_problem_template()


ANSWER = {
    "type": "numeric",
    "value": 969,
    "unit": "",
    "target_ref": "number.target",
    "derived_from": "step.add_534",
}


SEMANTIC_OVERRIDE = {
    "problem_id": PROBLEM_ID,
    "problem_type": "numeric_answer_place_value_then_addition_problem",
    "metadata": {
        "language": "ko-KR",
        "question": (
            "백의 자리 숫자가 4, 십의 자리 숫자가 3, 일의 자리 숫자가 5인 "
            "수보다 534 많은 수는 얼마입니까?"
        ),
        "instruction": "자리 숫자로 수를 만든 뒤 534만큼 큰 수를 구합니다.",
    },
    "domain": {
        "objects": [
            {
                "id": "digit.hundreds",
                "type": "place_digit",
                "label": "백의 자리 숫자",
                "place": "hundreds",
                "value": 4,
            },
            {
                "id": "digit.tens",
                "type": "place_digit",
                "label": "십의 자리 숫자",
                "place": "tens",
                "value": 3,
            },
            {
                "id": "digit.ones",
                "type": "place_digit",
                "label": "일의 자리 숫자",
                "place": "ones",
                "value": 5,
            },
            {
                "id": "number.base",
                "type": "place_value_number",
                "label": "세 자리 숫자로 만든 수",
            },
            {
                "id": "quantity.increase",
                "type": "quantity",
                "label": "더 많은 수량",
                "value": 534,
                "unit": "",
            },
            {
                "id": "number.target",
                "type": "unknown_number",
                "label": "기준 수보다 534 큰 수",
            },
        ],
        "relations": [
            {
                "id": "relation.base_from_digits",
                "type": "composed_by_place_value",
                "subject": "number.base",
                "digits": [
                    "digit.hundreds",
                    "digit.tens",
                    "digit.ones",
                ],
            },
            {
                "id": "relation.target_is_greater_by",
                "type": "greater_by",
                "subject": "number.target",
                "object": "number.base",
                "difference": "quantity.increase",
            },
        ],
        "problem_solving": {
            "understand": {
                "given_refs": [
                    "digit.hundreds",
                    "digit.tens",
                    "digit.ones",
                    "quantity.increase",
                ],
                "target_ref": "number.target",
                "condition_refs": [
                    "relation.base_from_digits",
                    "relation.target_is_greater_by",
                ],
            },
            "plan": {
                "method": "compose_number_then_add",
                "description": "각 자리 숫자로 기준 수를 만든 다음 534를 더합니다.",
            },
            "execute": {
                "expected_operations": [
                    "place_value_composition",
                    "addition",
                ],
            },
            "review": {
                "check_methods": ["subtraction_check"],
            },
        },
    },
    "answer": ANSWER,
}


SOLVABLE = {
    "schema": "modu.solvable.v1.2",
    "problem_id": PROBLEM_ID,
    "problem_type": "numeric_answer_place_value_then_addition_problem",
    "inputs": {
        "digits": {
            "hundreds": 4,
            "tens": 3,
            "ones": 5,
        },
        "increase": 534,
        "target_label": "자리 숫자로 만든 수보다 534 큰 수",
        "unit": "",
    },
    "given": [
        {
            "ref": "digit.hundreds",
            "value": {
                "digit": 4,
                "place": "hundreds",
            },
        },
        {
            "ref": "digit.tens",
            "value": {
                "digit": 3,
                "place": "tens",
            },
        },
        {
            "ref": "digit.ones",
            "value": {
                "digit": 5,
                "place": "ones",
            },
        },
        {
            "ref": "quantity.increase",
            "value": 534,
        },
    ],
    "target": {
        "ref": "number.target",
        "type": "number",
    },
    "method": "백의 자리, 십의 자리, 일의 자리 숫자로 기준 수를 만든 뒤 534를 더합니다.",
    "understanding": {
        "summary": (
            "백의 자리, 십의 자리, 일의 자리 숫자로 세 자리 수를 만든 뒤, "
            "그 수보다 534 큰 수를 구하는 문제입니다."
        ),
        "facts": [
            {
                "ref": "digit.hundreds",
                "label": "백의 자리 숫자",
                "value": 4,
                "unit": "",
                "source": "explicit",
            },
            {
                "ref": "digit.tens",
                "label": "십의 자리 숫자",
                "value": 3,
                "unit": "",
                "source": "explicit",
            },
            {
                "ref": "digit.ones",
                "label": "일의 자리 숫자",
                "value": 5,
                "unit": "",
                "source": "explicit",
            },
            {
                "ref": "quantity.increase",
                "label": "기준 수보다 큰 정도",
                "value": 534,
                "unit": "",
                "source": "explicit",
            },
        ],
        "unknowns": [
            {
                "ref": "number.target",
                "label": "자리 숫자로 만든 수보다 534 큰 수",
                "unit": "",
            },
        ],
        "relation": {
            "type": "place_value_composition_then_increase",
            "statement": (
                "각 자리 숫자로 기준 수를 만들고, '534 많은 수'는 "
                "기준 수에 534를 더하여 구합니다."
            ),
            "symbolic": "(4×100 + 3×10 + 5) + 534 = □",
            "uses": [
                "digit.hundreds",
                "digit.tens",
                "digit.ones",
                "quantity.increase",
            ],
            "result": "number.target",
        },
        "diagnostic_questions": [
            {
                "id": "understand.base_number",
                "type": "multiple_choice",
                "prompt": "주어진 자리 숫자로 만든 세 자리 수는 무엇인가요?",
                "choices": [
                    "435",
                    "453",
                    "345",
                ],
                "answer_index": 0,
            },
            {
                "id": "understand.operation",
                "type": "multiple_choice",
                "prompt": "435보다 534 많은 수를 구하려면 어떻게 계산해야 하나요?",
                "choices": [
                    "435 + 534",
                    "534 - 435",
                    "435 - 534",
                ],
                "answer_index": 0,
            },
        ],
    },
    "plan": [
        "백의 자리 숫자 4, 십의 자리 숫자 3, 일의 자리 숫자 5로 세 자리 수를 만듭니다.",
        "만든 수에 534를 더합니다.",
        "구한 수에서 534를 빼서 기준 수가 되는지 확인합니다.",
    ],
    "steps": [
        {
            "id": "step.compose_base_number",
            "expr": "4 * 100 + 3 * 10 + 5",
            "value": 435,
            "explanation": "4는 백의 자리, 3은 십의 자리, 5는 일의 자리이므로 만든 수는 435입니다.",
        },
        {
            "id": "step.add_534",
            "expr": "435 + 534",
            "value": 969,
            "explanation": "435보다 534 많은 수를 구해야 하므로 435에 534를 더합니다.",
        },
    ],
    "checks": [
        {
            "id": "check.subtract_increase",
            "expr": "969 - 534",
            "expected": 435,
            "actual": 435,
            "pass": True,
        },
        {
            "id": "check.place_digits",
            "expr": "hundreds(435) == 4 and tens(435) == 3 and ones(435) == 5",
            "expected": True,
            "actual": True,
            "pass": True,
        },
    ],
    "answer": ANSWER,
}


SEMANTIC_ANSWER = SOLVABLE["answer"]
