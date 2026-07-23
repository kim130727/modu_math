from __future__ import annotations

from modu_math.dsl import (
    BlankSlot,
    Canvas,
    ProblemTemplate,
    Region,
    TextBoxSlot,
)


PROBLEM_ID = "P3_1_01_00040_15613"
PROBLEM_TITLE = "처음에 딴 배의 수"


ANSWER = {
    "type": "numeric",
    "value": 438,
    "unit": "개",
    "target_ref": "quantity.initial_pears",
    "derived_from": "step.restore_initial_count",
}


SEMANTIC = {
    "problem_id": PROBLEM_ID,
    "problem_type": "numeric_answer_partitive_change_addition_word_problem",
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
                "id": "place.orchard",
                "type": "place",
                "label": "과수원",
            },
            {
                "id": "place.front_house",
                "type": "place",
                "label": "앞집",
            },
            {
                "id": "object.pear",
                "type": "countable_object",
                "label": "배",
                "unit": "개",
            },
            {
                "id": "quantity.given_pears",
                "type": "quantity",
                "label": "앞집에 준 배의 수",
                "value": 113,
                "unit": "개",
            },
            {
                "id": "quantity.remaining_pears",
                "type": "quantity",
                "label": "남은 배의 수",
                "value": 325,
                "unit": "개",
            },
            {
                "id": "quantity.initial_pears",
                "type": "quantity",
                "label": "처음에 딴 배의 수",
                "value": 438,
                "unit": "개",
            },
        ],
        "relations": [
            {
                "id": "relation.pears_picked_at_orchard",
                "type": "picked_at",
                "from_id": "object.pear",
                "to_id": "place.orchard",
                "quantity": "quantity.initial_pears",
            },
            {
                "id": "relation.pears_given_to_front_house",
                "type": "transferred_to",
                "from_id": "object.pear",
                "to_id": "place.front_house",
                "quantity": "quantity.given_pears",
            },
            {
                "id": "relation.initial_split_into_given_and_remaining",
                "type": "whole_part_relation",
                "whole": "quantity.initial_pears",
                "parts": [
                    "quantity.given_pears",
                    "quantity.remaining_pears",
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
    "problem_type": "numeric_answer_partitive_change_addition_word_problem",
    "inputs": {
        "target_label": "처음에 딴 배의 수",
        "unit": "개",
        "quantities": {
            "given_count": 113,
            "remaining_count": 325,
        },
        "conditions": [
            "과수원에서 딴 배 중 113개를 앞집에 주었습니다.",
            "앞집에 주고 나서 배가 325개 남았습니다.",
            "처음에 딴 배의 수를 구합니다.",
        ],
    },
    "given": [
        {
            "ref": "quantity.given_pears",
            "value": {
                "count": 113,
                "unit": "개",
                "object": "object.pear",
                "destination": "place.front_house",
            },
        },
        {
            "ref": "quantity.remaining_pears",
            "value": {
                "count": 325,
                "unit": "개",
                "object": "object.pear",
            },
        },
    ],
    "target": {
        "ref": "quantity.initial_pears",
        "type": "number",
    },
    "understanding": {
        "summary": "처음에 딴 배 중 일부를 앞집에 주고 남은 수가 주어졌을 때, 처음의 전체 수를 구하는 문제입니다.",
        "facts": [
            {
                "ref": "quantity.given_pears",
                "label": "앞집에 준 배의 수",
                "value": 113,
                "unit": "개",
                "source": "explicit",
            },
            {
                "ref": "quantity.remaining_pears",
                "label": "남은 배의 수",
                "value": 325,
                "unit": "개",
                "source": "explicit",
            },
        ],
        "unknowns": [
            {
                "ref": "quantity.initial_pears",
                "label": "처음에 딴 배의 수",
                "unit": "개",
                "source": "unknown",
            },
        ],
        "relation": {
            "type": "whole_part_addition",
            "statement": "처음에 딴 배는 앞집에 준 배와 남은 배를 합한 수입니다.",
            "symbolic": "처음에 딴 배 = 앞집에 준 배 + 남은 배",
            "uses": [
                "quantity.given_pears",
                "quantity.remaining_pears",
            ],
            "result": "quantity.initial_pears",
        },
        "diagnostic_questions": [
            {
                "id": "understand.target",
                "type": "multiple_choice",
                "prompt": "이 문제에서 구해야 하는 것은 무엇인가요?",
                "choices": [
                    "앞집에 준 배의 수",
                    "남은 배의 수",
                    "처음에 딴 배의 수",
                ],
                "answer_index": 2,
            },
            {
                "id": "understand.relation",
                "type": "multiple_choice",
                "prompt": "처음에 딴 배의 수를 구하려면 어떻게 해야 하나요?",
                "choices": [
                    "113과 325를 더합니다.",
                    "325에서 113을 뺍니다.",
                    "113에서 325를 뺍니다.",
                ],
                "answer_index": 0,
            },
        ],
        "student_restatement": {
            "prompt": "문제의 요지를 말해 볼까요?",
            "template": "{given_count}개와 {remaining_count}개를 더해 {target_label}를 구합니다.",
            "answer": "앞집에 준 113개와 남은 325개를 더해 처음에 딴 배의 수를 구합니다.",
        },
    },
    "method": "앞집에 준 배의 수와 남은 배의 수를 더하여 처음에 딴 배의 수를 구합니다.",
    "plan": [
        "앞집에 준 배의 수 113개를 확인합니다.",
        "남은 배의 수 325개를 확인합니다.",
        "준 수와 남은 수를 더하여 처음의 전체 수를 구합니다.",
    ],
    "steps": [
        {
            "id": "step.restore_initial_count",
            "goal": "처음에 딴 배의 수를 구합니다.",
            "uses": [
                "quantity.given_pears",
                "quantity.remaining_pears",
            ],
            "relation_expr": "처음에 딴 배 = 앞집에 준 배 + 남은 배",
            "expr": "113 + 325",
            "value": {
                "count": 438,
                "unit": "개",
                "ref": "quantity.initial_pears",
            },
            "explanation": "처음의 전체 수는 앞집에 준 113개와 남은 325개를 더하여 구합니다.",
        },
    ],
    "checks": [
        {
            "id": "check.subtract_given_count",
            "expr": "438 - 113",
            "expected": 325,
            "actual": 325,
            "pass": True,
        },
        {
            "id": "check.subtract_remaining_count",
            "expr": "438 - 325",
            "expected": 113,
            "actual": 113,
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
                height=74,
                text=(
                    "과수원에서 배를 따서 앞집에 113개를 주었더니 325개가 남았습니다. "
                    "처음에 딴 배는 모두 몇 개입니까?"
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
                answer_key="438",
                placeholder="개",
            ),
        ),
    )


PROBLEM_TEMPLATE = build_problem_template()
