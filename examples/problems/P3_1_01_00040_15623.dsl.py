from __future__ import annotations

from modu_math.dsl import (
    BlankSlot,
    Canvas,
    ProblemTemplate,
    Region,
    TextBoxSlot,
)


PROBLEM_ID = "P3_1_01_00040_15623"
PROBLEM_TITLE = "현석이가 어머니로부터 받은 용돈"


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
                height=52,
                text=(
                    "현석이는 어머니로부터 용돈을 받아 310원어치 준비물을 사고, "
                    "420원짜리 빵을 사 먹었더니 130원이 남았습니다. "
                    "어머니로부터 받은 용돈은 얼마입니까?"
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
                answer_key="860",
                placeholder="원",
            ),
        ),
    )


PROBLEM_TEMPLATE = build_problem_template()


ANSWER = {
    "type": "numeric",
    "value": 860,
    "unit": "원",
    "target_ref": "quantity.initial_allowance",
    "derived_from": "step.find_initial_allowance",
}


SEMANTIC_OVERRIDE = {
    "problem_id": PROBLEM_ID,
    "problem_type": "numeric_answer_reverse_sequential_subtraction_word_problem",
    "metadata": {
        "grade": 3,
        "semester": 1,
        "subject": "수학",
        "topic": "세 자리 수의 덧셈과 뺄셈",
        "language": "ko-KR",
        "question": (
            "현석이는 어머니로부터 용돈을 받아 310원어치 준비물을 사고, "
            "420원짜리 빵을 사 먹었더니 130원이 남았습니다. "
            "어머니로부터 받은 용돈은 얼마입니까?"
        ),
        "instruction": "두 번 사용한 돈과 남은 돈을 더하여 처음 받은 용돈을 구합니다.",
    },
    "domain": {
        "objects": [
            {
                "id": "person.hyeonseok",
                "type": "person",
                "label": "현석이",
            },
            {
                "id": "person.mother",
                "type": "person",
                "label": "어머니",
            },
            {
                "id": "object.supplies",
                "type": "purchasable_object",
                "label": "준비물",
            },
            {
                "id": "object.bread",
                "type": "purchasable_object",
                "label": "빵",
            },
            {
                "id": "quantity.supplies_cost",
                "type": "quantity",
                "label": "준비물을 사는 데 쓴 돈",
                "value": 310,
                "unit": "원",
            },
            {
                "id": "quantity.bread_cost",
                "type": "quantity",
                "label": "빵을 사는 데 쓴 돈",
                "value": 420,
                "unit": "원",
            },
            {
                "id": "quantity.remaining_money",
                "type": "quantity",
                "label": "준비물과 빵을 사고 남은 돈",
                "value": 130,
                "unit": "원",
            },
            {
                "id": "quantity.total_spent",
                "type": "derived_quantity",
                "label": "현석이가 모두 사용한 돈",
                "value": 730,
                "unit": "원",
            },
            {
                "id": "quantity.initial_allowance",
                "type": "unknown_quantity",
                "label": "어머니로부터 받은 용돈",
                "unit": "원",
            },
        ],
        "relations": [
            {
                "id": "relation.mother_gave_allowance",
                "type": "gave",
                "subject": "person.mother",
                "recipient": "person.hyeonseok",
                "quantity_ref": "quantity.initial_allowance",
            },
            {
                "id": "relation.hyeonseok_bought_supplies",
                "type": "purchased",
                "subject": "person.hyeonseok",
                "object": "object.supplies",
                "price_ref": "quantity.supplies_cost",
            },
            {
                "id": "relation.hyeonseok_bought_bread",
                "type": "purchased",
                "subject": "person.hyeonseok",
                "object": "object.bread",
                "price_ref": "quantity.bread_cost",
            },
            {
                "id": "relation.total_spent_is_sum",
                "type": "sum_of",
                "subject": "quantity.total_spent",
                "objects": [
                    "quantity.supplies_cost",
                    "quantity.bread_cost",
                ],
            },
            {
                "id": "relation.initial_allowance_is_sum",
                "type": "sum_of",
                "subject": "quantity.initial_allowance",
                "objects": [
                    "quantity.supplies_cost",
                    "quantity.bread_cost",
                    "quantity.remaining_money",
                ],
            },
        ],
        "problem_solving": {
            "understand": {
                "given_refs": [
                    "quantity.supplies_cost",
                    "quantity.bread_cost",
                    "quantity.remaining_money",
                ],
                "target_ref": "quantity.initial_allowance",
                "condition_refs": [
                    "relation.total_spent_is_sum",
                    "relation.initial_allowance_is_sum",
                ],
            },
            "plan": {
                "method": "add_all_spent_and_remaining_money",
                "description": "준비물값과 빵값을 더한 뒤 남은 돈을 더합니다.",
            },
            "execute": {
                "expected_operations": [
                    "addition",
                    "addition",
                ],
            },
            "review": {
                "check_methods": [
                    "forward_sequential_subtraction",
                    "reverse_addition",
                ],
            },
        },
    },
    "answer": ANSWER,
}


SOLVABLE = {
    "schema": "modu.solvable.v1.2",
    "problem_id": PROBLEM_ID,
    "problem_type": "numeric_answer_reverse_sequential_subtraction_word_problem",
    "inputs": {
        "target_label": "현석이가 어머니로부터 받은 용돈",
        "unit": "원",
        "quantities": {
            "supplies_cost": 310,
            "bread_cost": 420,
            "remaining_money": 130,
        },
        "conditions": [
            "현석이는 어머니로부터 용돈을 받았습니다.",
            "준비물을 사는 데 310원을 사용했습니다.",
            "빵을 사 먹는 데 420원을 사용했습니다.",
            "두 물건을 사고 130원이 남았습니다.",
        ],
    },
    "given": [
        {
            "ref": "quantity.supplies_cost",
            "value": {
                "amount": 310,
                "unit": "원",
                "object": "object.supplies",
            },
        },
        {
            "ref": "quantity.bread_cost",
            "value": {
                "amount": 420,
                "unit": "원",
                "object": "object.bread",
            },
        },
        {
            "ref": "quantity.remaining_money",
            "value": {
                "amount": 130,
                "unit": "원",
                "owner": "person.hyeonseok",
            },
        },
    ],
    "target": {
        "ref": "quantity.initial_allowance",
        "type": "number",
    },
    "understanding": {
        "summary": (
            "현석이가 준비물과 빵을 사는 데 쓴 돈과 사고 남은 돈을 모두 합해 "
            "어머니로부터 처음 받은 용돈을 구하는 문제입니다."
        ),
        "facts": [
            {
                "ref": "quantity.supplies_cost",
                "label": "준비물을 사는 데 쓴 돈",
                "value": 310,
                "unit": "원",
                "source": "explicit",
            },
            {
                "ref": "quantity.bread_cost",
                "label": "빵을 사는 데 쓴 돈",
                "value": 420,
                "unit": "원",
                "source": "explicit",
            },
            {
                "ref": "quantity.remaining_money",
                "label": "준비물과 빵을 사고 남은 돈",
                "value": 130,
                "unit": "원",
                "source": "explicit",
            },
        ],
        "unknowns": [
            {
                "ref": "quantity.total_spent",
                "label": "현석이가 모두 사용한 돈",
                "unit": "원",
                "source": "derived",
            },
            {
                "ref": "quantity.initial_allowance",
                "label": "현석이가 어머니로부터 받은 용돈",
                "unit": "원",
                "source": "unknown",
            },
        ],
        "relation": {
            "type": "sequential_spending_reverse_addition",
            "statement": (
                "처음 받은 용돈은 준비물값, 빵값, 두 물건을 사고 남은 돈의 합입니다."
            ),
            "symbolic": "처음 받은 용돈 = 준비물값 + 빵값 + 남은 돈",
            "uses": [
                "quantity.supplies_cost",
                "quantity.bread_cost",
                "quantity.remaining_money",
            ],
            "result": "quantity.initial_allowance",
        },
        "diagnostic_questions": [
            {
                "id": "understand.target",
                "type": "multiple_choice",
                "prompt": "이 문제에서 구해야 하는 것은 무엇인가요?",
                "choices": [
                    "준비물의 가격",
                    "빵을 사고 남은 돈",
                    "어머니로부터 받은 용돈",
                ],
                "answer_index": 2,
            },
            {
                "id": "understand.used_money",
                "type": "multiple_choice",
                "prompt": "현석이가 물건을 사는 데 모두 사용한 돈은 어떻게 구하나요?",
                "choices": [
                    "310과 420을 더합니다.",
                    "420에서 310을 뺍니다.",
                    "310에서 130을 뺍니다.",
                ],
                "answer_index": 0,
            },
            {
                "id": "understand.relation",
                "type": "multiple_choice",
                "prompt": "처음 받은 용돈을 구하려면 무엇을 더해야 하나요?",
                "choices": [
                    "준비물값과 빵값만 더합니다.",
                    "빵값과 남은 돈만 더합니다.",
                    "준비물값, 빵값, 남은 돈을 모두 더합니다.",
                ],
                "answer_index": 2,
            },
        ],
        "student_restatement": {
            "prompt": "문제의 요지를 말해 볼까요?",
            "template": (
                "{supplies_cost}원과 {bread_cost}원을 사용하고 "
                "{remaining_money}원이 남았으므로 세 금액을 더해 {target_label}을 구합니다."
            ),
            "answer": (
                "준비물값 310원, 빵값 420원, 남은 돈 130원을 모두 더해 "
                "어머니로부터 받은 용돈을 구합니다."
            ),
        },
    },
    "method": "310원과 420원을 더해 사용한 돈을 구하고, 남은 130원을 더합니다.",
    "plan": [
        "준비물을 사는 데 310원을 사용했음을 확인합니다.",
        "빵을 사는 데 420원을 사용했음을 확인합니다.",
        "두 금액을 더해 모두 사용한 돈을 구합니다.",
        "모두 사용한 돈에 남은 130원을 더해 처음 받은 용돈을 구합니다.",
    ],
    "steps": [
        {
            "id": "step.find_total_spent",
            "goal": "현석이가 모두 사용한 돈을 구합니다.",
            "uses": [
                "quantity.supplies_cost",
                "quantity.bread_cost",
            ],
            "relation_expr": "모두 사용한 돈 = 준비물값 + 빵값",
            "expr": "310 + 420",
            "value": 730,
            "explanation": "준비물과 빵을 사는 데 사용한 돈을 모두 구하므로 310과 420을 더합니다.",
        },
        {
            "id": "step.find_initial_allowance",
            "goal": "현석이가 어머니로부터 받은 용돈을 구합니다.",
            "uses": [
                "quantity.total_spent",
                "quantity.remaining_money",
            ],
            "relation_expr": "처음 받은 용돈 = 모두 사용한 돈 + 남은 돈",
            "expr": "730 + 130",
            "value": 860,
            "explanation": "처음 받은 용돈은 사용한 돈과 남은 돈의 합이므로 730과 130을 더합니다.",
        },
    ],
    "checks": [
        {
            "id": "check.forward_first_purchase",
            "expr": "860 - 310",
            "expected": 550,
            "actual": 550,
            "pass": True,
        },
        {
            "id": "check.forward_second_purchase",
            "expr": "550 - 420",
            "expected": 130,
            "actual": 130,
            "pass": True,
        },
        {
            "id": "check.reverse_addition",
            "expr": "130 + 420 + 310",
            "expected": 860,
            "actual": 860,
            "pass": True,
        },
    ],
    "answer": ANSWER,
}


SEMANTIC_ANSWER = SOLVABLE["answer"]
