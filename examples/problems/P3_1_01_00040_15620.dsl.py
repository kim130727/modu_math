from __future__ import annotations

from modu_math.dsl import (
    BlankSlot,
    Canvas,
    ProblemTemplate,
    Region,
    TextBoxSlot,
)


PROBLEM_ID = "P3_1_01_00040_15620"
PROBLEM_TITLE = "인호가 처음 가지고 있던 돈"


def build_problem_template() -> ProblemTemplate:
    return ProblemTemplate(
        id=PROBLEM_ID,
        title=PROBLEM_TITLE,
        canvas=Canvas(
            width=960,
            height=150,
            coordinate_mode="logical",
        ),
        regions=(
            Region(
                id="region.stem",
                role="stem",
                flow="vertical",
                slot_ids=(
                    "slot.question",
                    "slot.answer",
                ),
            ),
        ),
        slots=(
            TextBoxSlot(
                id="slot.question",
                x=24,
                y=24,
                width=912,
                height=48,
                text=(
                    "인호가 340원짜리 연필을 사고 나니 540원이 남았습니다. "
                    "인호가 처음에 가지고 있던 돈은 얼마입니까?"
                ),
                font_size=24,
                font_family="Noto Sans KR",
                fill="#202124",
                line_height=1.45,
                align="left",
                valign="top",
            ),
            BlankSlot(
                id="slot.answer",
                prompt="답",
                answer_key="880",
                placeholder="원",
            ),
        ),
    )


PROBLEM_TEMPLATE = build_problem_template()


ANSWER = {
    "type": "numeric",
    "value": 880,
    "unit": "원",
    "target_ref": "quantity.initial_money",
    "derived_from": "step.add_spent_and_remaining",
}


SEMANTIC_OVERRIDE = {
    "problem_id": PROBLEM_ID,
    "problem_type": "numeric_answer_addition_word_problem",
    "metadata": {
        "grade": 3,
        "semester": 1,
        "subject": "수학",
        "topic": "세 자리 수의 덧셈",
        "language": "ko-KR",
        "question": (
            "인호가 340원짜리 연필을 사고 나니 540원이 남았습니다. "
            "인호가 처음에 가지고 있던 돈은 얼마입니까?"
        ),
        "instruction": "사용한 돈과 남은 돈을 더하여 처음 가지고 있던 돈을 구합니다.",
    },
    "domain": {
        "objects": [
            {
                "id": "person.inho",
                "type": "person",
                "label": "인호",
            },
            {
                "id": "object.pencil",
                "type": "purchasable_object",
                "label": "연필",
            },
            {
                "id": "quantity.pencil_price",
                "type": "quantity",
                "label": "연필값",
                "value": 340,
                "unit": "원",
            },
            {
                "id": "quantity.remaining_money",
                "type": "quantity",
                "label": "연필을 사고 남은 돈",
                "value": 540,
                "unit": "원",
            },
            {
                "id": "quantity.initial_money",
                "type": "unknown_quantity",
                "label": "인호가 처음 가지고 있던 돈",
                "unit": "원",
            },
        ],
        "relations": [
            {
                "id": "relation.inho_bought_pencil",
                "type": "purchased",
                "subject": "person.inho",
                "object": "object.pencil",
                "price_ref": "quantity.pencil_price",
            },
            {
                "id": "relation.initial_money_is_sum",
                "type": "sum_of",
                "subject": "quantity.initial_money",
                "objects": [
                    "quantity.pencil_price",
                    "quantity.remaining_money",
                ],
            },
        ],
        "problem_solving": {
            "understand": {
                "given_refs": [
                    "quantity.pencil_price",
                    "quantity.remaining_money",
                ],
                "target_ref": "quantity.initial_money",
                "condition_refs": ["relation.initial_money_is_sum"],
            },
            "plan": {
                "method": "add_spent_and_remaining_money",
                "description": "연필을 사는 데 쓴 돈과 사고 나서 남은 돈을 더합니다.",
            },
            "execute": {
                "expected_operations": ["addition"],
            },
            "review": {
                "check_methods": ["inverse_subtraction"],
            },
        },
    },
    "answer": ANSWER,
}


SOLVABLE = {
    "schema": "modu.solvable.v1.2",
    "problem_id": PROBLEM_ID,
    "problem_type": "numeric_answer_addition_word_problem",
    "inputs": {
        "target_label": "인호가 처음 가지고 있던 돈",
        "unit": "원",
        "quantities": {
            "pencil_price": 340,
            "remaining_money": 540,
        },
        "conditions": [
            "인호가 340원짜리 연필 한 자루를 샀습니다.",
            "연필을 사고 나서 540원이 남았습니다.",
        ],
    },
    "given": [
        {
            "ref": "quantity.pencil_price",
            "value": {
                "amount": 340,
                "unit": "원",
                "object": "object.pencil",
            },
        },
        {
            "ref": "quantity.remaining_money",
            "value": {
                "amount": 540,
                "unit": "원",
                "owner": "person.inho",
            },
        },
    ],
    "target": {
        "ref": "quantity.initial_money",
        "type": "number",
    },
    "understanding": {
        "summary": "연필을 사는 데 쓴 돈과 사고 나서 남은 돈을 합해 처음 가지고 있던 돈을 구하는 문제입니다.",
        "facts": [
            {
                "ref": "quantity.pencil_price",
                "label": "연필을 사는 데 쓴 돈",
                "value": 340,
                "unit": "원",
                "source": "explicit",
            },
            {
                "ref": "quantity.remaining_money",
                "label": "연필을 사고 남은 돈",
                "value": 540,
                "unit": "원",
                "source": "explicit",
            },
        ],
        "unknowns": [
            {
                "ref": "quantity.initial_money",
                "label": "인호가 처음 가지고 있던 돈",
                "unit": "원",
                "source": "unknown",
            },
        ],
        "relation": {
            "type": "part_part_whole_addition",
            "statement": "처음 가지고 있던 돈은 연필을 사는 데 쓴 돈과 사고 남은 돈의 합입니다.",
            "symbolic": "처음 가진 돈 = 연필값 + 남은 돈",
            "uses": [
                "quantity.pencil_price",
                "quantity.remaining_money",
            ],
            "result": "quantity.initial_money",
        },
        "diagnostic_questions": [
            {
                "id": "understand.target",
                "type": "multiple_choice",
                "prompt": "이 문제에서 구해야 하는 것은 무엇인가요?",
                "choices": [
                    "연필의 가격",
                    "연필을 사고 남은 돈",
                    "인호가 처음 가지고 있던 돈",
                ],
                "answer_index": 2,
            },
            {
                "id": "understand.relation",
                "type": "multiple_choice",
                "prompt": "처음 가지고 있던 돈을 구하려면 어떻게 해야 하나요?",
                "choices": [
                    "340과 540을 더합니다.",
                    "540에서 340을 뺍니다.",
                    "340에서 540을 뺍니다.",
                ],
                "answer_index": 0,
            },
        ],
        "student_restatement": {
            "prompt": "문제의 요지를 말해 볼까요?",
            "template": "{spent_money}원과 {remaining_money}원을 더해 {target_label}을 구합니다.",
            "answer": "연필값 340원과 남은 돈 540원을 더해 처음 가지고 있던 돈을 구합니다.",
        },
    },
    "method": "연필을 사는 데 쓴 340원과 사고 나서 남은 540원을 더합니다.",
    "plan": [
        "연필을 사는 데 쓴 돈이 340원임을 확인합니다.",
        "연필을 사고 남은 돈이 540원임을 확인합니다.",
        "쓴 돈과 남은 돈을 더하여 처음 가지고 있던 돈을 구합니다.",
    ],
    "steps": [
        {
            "id": "step.add_spent_and_remaining",
            "goal": "인호가 처음 가지고 있던 돈을 구합니다.",
            "uses": [
                "quantity.pencil_price",
                "quantity.remaining_money",
            ],
            "relation_expr": "처음 가진 돈 = 연필값 + 남은 돈",
            "expr": "340 + 540",
            "value": 880,
            "explanation": "처음 가지고 있던 돈은 사용한 돈과 남은 돈을 합한 것이므로 340과 540을 더합니다.",
        },
    ],
    "checks": [
        {
            "id": "check.subtract_pencil_price",
            "expr": "880 - 340",
            "expected": 540,
            "actual": 540,
            "pass": True,
        },
        {
            "id": "check.subtract_remaining_money",
            "expr": "880 - 540",
            "expected": 340,
            "actual": 340,
            "pass": True,
        },
    ],
    "answer": ANSWER,
}


SEMANTIC_ANSWER = SOLVABLE["answer"]
