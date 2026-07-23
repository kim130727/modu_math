from __future__ import annotations

from modu_math.dsl import (
    BlankSlot,
    Canvas,
    ProblemTemplate,
    Region,
    TextBoxSlot,
)


PROBLEM_ID = "P3_1_01_00040_15614"
PROBLEM_TITLE = "영진이가 처음 가지고 있던 돈"


ANSWER = {
    "type": "numeric",
    "value": 880,
    "unit": "원",
    "target_ref": "quantity.initial_money",
    "derived_from": "step.restore_initial_money",
}


SEMANTIC = {
    "problem_id": PROBLEM_ID,
    "problem_type": "numeric_answer_two_step_addition_money_word_problem",
    "metadata": {
        "grade": 3,
        "semester": 1,
        "subject": "수학",
        "topic": "세 자리 수의 덧셈",
        "language": "ko-KR",
    },
    "domain": {
        "objects": [
            {
                "id": "person.yeongjin",
                "type": "person",
                "label": "영진이",
            },
            {
                "id": "place.store",
                "type": "place",
                "label": "가게",
            },
            {
                "id": "place.stationery_store",
                "type": "place",
                "label": "문구점",
            },
            {
                "id": "object.snack",
                "type": "purchasable_object",
                "label": "과자",
            },
            {
                "id": "object.notebook",
                "type": "purchasable_object",
                "label": "공책",
            },
            {
                "id": "quantity.snack_price",
                "type": "money",
                "label": "과자값",
                "value": 120,
                "unit": "원",
            },
            {
                "id": "quantity.notebook_price",
                "type": "money",
                "label": "공책값",
                "value": 340,
                "unit": "원",
            },
            {
                "id": "quantity.total_spent",
                "type": "money",
                "label": "물건을 사는 데 쓴 돈",
                "value": 460,
                "unit": "원",
            },
            {
                "id": "quantity.remaining_money",
                "type": "money",
                "label": "남은 돈",
                "value": 420,
                "unit": "원",
            },
            {
                "id": "quantity.initial_money",
                "type": "money",
                "label": "처음에 가지고 있던 돈",
                "value": 880,
                "unit": "원",
            },
        ],
        "relations": [
            {
                "id": "relation.snack_purchased_at_store",
                "type": "purchased_at",
                "from_id": "object.snack",
                "to_id": "place.store",
                "buyer": "person.yeongjin",
                "price": "quantity.snack_price",
            },
            {
                "id": "relation.notebook_purchased_at_stationery_store",
                "type": "purchased_at",
                "from_id": "object.notebook",
                "to_id": "place.stationery_store",
                "buyer": "person.yeongjin",
                "price": "quantity.notebook_price",
            },
            {
                "id": "relation.total_spent_sum",
                "type": "part_part_whole",
                "whole": "quantity.total_spent",
                "parts": [
                    "quantity.snack_price",
                    "quantity.notebook_price",
                ],
            },
            {
                "id": "relation.initial_money_partition",
                "type": "whole_part_relation",
                "whole": "quantity.initial_money",
                "parts": [
                    "quantity.total_spent",
                    "quantity.remaining_money",
                ],
            },
        ],
    },
    "answer": ANSWER,
}

SEMANTIC_OVERRIDE = SEMANTIC


SOLVABLE = {
    "schema": "modu.solvable.v1.2",
    "problem_id": PROBLEM_ID,
    "problem_type": "numeric_answer_two_step_addition_money_word_problem",
    "inputs": {
        "target_label": "영진이가 처음에 가지고 있던 돈",
        "unit": "원",
        "quantities": {
            "snack_price": 120,
            "notebook_price": 340,
            "remaining_money": 420,
        },
        "conditions": [
            "영진이는 가게에서 120원짜리 과자를 샀습니다.",
            "영진이는 문구점에서 340원짜리 공책을 샀습니다.",
            "두 물건을 산 뒤 420원이 남았습니다.",
            "영진이가 처음에 가지고 있던 돈을 구합니다.",
        ],
    },
    "given": [
        {
            "ref": "quantity.snack_price",
            "value": {
                "amount": 120,
                "unit": "원",
                "object": "object.snack",
                "place": "place.store",
            },
        },
        {
            "ref": "quantity.notebook_price",
            "value": {
                "amount": 340,
                "unit": "원",
                "object": "object.notebook",
                "place": "place.stationery_store",
            },
        },
        {
            "ref": "quantity.remaining_money",
            "value": {
                "amount": 420,
                "unit": "원",
                "owner": "person.yeongjin",
            },
        },
    ],
    "target": {
        "ref": "quantity.initial_money",
        "type": "number",
    },
    "understanding": {
        "summary": "과자와 공책을 사고 남은 돈이 주어졌을 때, 두 물건값과 남은 돈을 더해 처음 가지고 있던 돈을 구하는 문제입니다.",
        "facts": [
            {
                "ref": "quantity.snack_price",
                "label": "과자값",
                "value": 120,
                "unit": "원",
                "source": "explicit",
            },
            {
                "ref": "quantity.notebook_price",
                "label": "공책값",
                "value": 340,
                "unit": "원",
                "source": "explicit",
            },
            {
                "ref": "quantity.remaining_money",
                "label": "남은 돈",
                "value": 420,
                "unit": "원",
                "source": "explicit",
            },
        ],
        "unknowns": [
            {
                "ref": "quantity.initial_money",
                "label": "영진이가 처음에 가지고 있던 돈",
                "unit": "원",
                "source": "unknown",
            },
        ],
        "relation": {
            "type": "two_step_part_part_whole_addition",
            "statement": "처음 가지고 있던 돈은 과자값, 공책값, 남은 돈을 모두 합한 금액입니다.",
            "symbolic": "처음 돈 = (과자값 + 공책값) + 남은 돈",
            "uses": [
                "quantity.snack_price",
                "quantity.notebook_price",
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
                    "과자값",
                    "공책값",
                    "영진이가 처음에 가지고 있던 돈",
                ],
                "answer_index": 2,
            },
            {
                "id": "understand.relation",
                "type": "multiple_choice",
                "prompt": "처음 가지고 있던 돈을 구하려면 어떻게 해야 하나요?",
                "choices": [
                    "과자값과 공책값만 더합니다.",
                    "과자값과 공책값을 더한 뒤 남은 돈을 더합니다.",
                    "남은 돈에서 두 물건값을 뺍니다.",
                ],
                "answer_index": 1,
            },
        ],
        "student_restatement": {
            "prompt": "문제의 요지를 말해 볼까요?",
            "template": "{snack_price}원과 {notebook_price}원을 쓴 뒤 {remaining_money}원이 남았으므로 세 금액을 더해 {target_label}을 구합니다.",
            "answer": "과자값 120원과 공책값 340원을 쓴 뒤 420원이 남았으므로 세 금액을 더해 처음 가지고 있던 돈을 구합니다.",
        },
    },
    "method": "두 물건값을 먼저 더한 다음 남은 돈을 더하여 처음 가지고 있던 돈을 구합니다.",
    "plan": [
        "과자값 120원과 공책값 340원을 더해 물건을 사는 데 쓴 돈을 구합니다.",
        "물건을 사는 데 쓴 돈에 남은 돈 420원을 더합니다.",
        "구한 금액이 처음 가지고 있던 돈인지 뺄셈으로 확인합니다.",
    ],
    "steps": [
        {
            "id": "step.calculate_total_spent",
            "goal": "두 물건을 사는 데 쓴 돈을 구합니다.",
            "uses": [
                "quantity.snack_price",
                "quantity.notebook_price",
            ],
            "relation_expr": "쓴 돈 = 과자값 + 공책값",
            "expr": "120 + 340",
            "value": {
                "amount": 460,
                "unit": "원",
                "ref": "quantity.total_spent",
            },
            "explanation": "과자값 120원과 공책값 340원을 더하면 모두 460원을 썼습니다.",
        },
        {
            "id": "step.restore_initial_money",
            "goal": "영진이가 처음에 가지고 있던 돈을 구합니다.",
            "uses": [
                "quantity.total_spent",
                "quantity.remaining_money",
            ],
            "relation_expr": "처음 돈 = 쓴 돈 + 남은 돈",
            "expr": "460 + 420",
            "value": {
                "amount": 880,
                "unit": "원",
                "ref": "quantity.initial_money",
            },
            "explanation": "쓴 돈 460원과 남은 돈 420원을 더하면 처음 가지고 있던 돈은 880원입니다.",
        },
    ],
    "checks": [
        {
            "id": "check.subtract_total_spent",
            "expr": "880 - 460",
            "expected": 420,
            "actual": 420,
            "pass": True,
        },
        {
            "id": "check.subtract_each_purchase",
            "expr": "880 - 120 - 340",
            "expected": 420,
            "actual": 420,
            "pass": True,
        },
    ],
    "answer": ANSWER,
}

SEMANTIC_ANSWER = SOLVABLE["answer"]


def build_problem_template() -> ProblemTemplate:
    return ProblemTemplate(
        id=PROBLEM_ID,
        title=PROBLEM_TITLE,
        canvas=Canvas(
            width=900,
            height=210,
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
                y=28,
                width=852,
                height=76,
                text=(
                    "영진이는 가게에서 120원짜리 과자를 사고, 문구점에서 340원짜리 "
                    "공책을 샀더니 420원이 남았습니다. 영진이가 처음에 가지고 있던 "
                    "돈은 얼마입니까?"
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
                answer_key="880",
                placeholder="원",
            ),
        ),
    )


PROBLEM_TEMPLATE = build_problem_template()
