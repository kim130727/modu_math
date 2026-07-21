from __future__ import annotations

from modu_math.dsl import (
    BlankSlot,
    Canvas,
    ProblemTemplate,
    Region,
    TextBoxSlot,
)


PROBLEM_ID = "P3_1_01_00040_15603"
PROBLEM_TITLE = "기영이가 처음 가지고 있던 구슬 수"


ANSWER = {
    "value": 470,
    "unit": "개",
}


SEMANTIC = {
    "problem_id": PROBLEM_ID,
    "problem_type": "numeric_answer_addition_word_problem",
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
                "id": "person.giyeong",
                "type": "person",
                "label": "기영이",
            },
            {
                "id": "person.hogeun",
                "type": "person",
                "label": "호근이",
            },
            {
                "id": "person.hyeongu",
                "type": "person",
                "label": "형우",
            },
            {
                "id": "object.marble",
                "type": "countable_object",
                "label": "구슬",
                "unit": "개",
            },
            {
                "id": "quantity.given_to_hogeun",
                "type": "quantity",
                "label": "호근이에게 준 구슬 수",
                "value": 120,
                "unit": "개",
            },
            {
                "id": "quantity.given_to_hyeongu",
                "type": "quantity",
                "label": "형우에게 준 구슬 수",
                "value": 130,
                "unit": "개",
            },
            {
                "id": "quantity.remaining_marbles",
                "type": "quantity",
                "label": "남은 구슬 수",
                "value": 220,
                "unit": "개",
            },
            {
                "id": "quantity.total_given_marbles",
                "type": "quantity",
                "label": "두 사람에게 준 구슬 수",
                "value": 250,
                "unit": "개",
            },
            {
                "id": "quantity.initial_marbles",
                "type": "quantity",
                "label": "처음 가지고 있던 구슬 수",
                "value": 470,
                "unit": "개",
            },
        ],
        "relations": [
            {
                "id": "relation.give_to_hogeun",
                "type": "transfer_out",
                "from_id": "person.giyeong",
                "to_id": "person.hogeun",
                "object_id": "object.marble",
                "quantity": "quantity.given_to_hogeun",
            },
            {
                "id": "relation.give_to_hyeongu",
                "type": "transfer_out",
                "from_id": "person.giyeong",
                "to_id": "person.hyeongu",
                "object_id": "object.marble",
                "quantity": "quantity.given_to_hyeongu",
            },
            {
                "id": "relation.total_given_marbles",
                "type": "part_part_whole",
                "parts": [
                    "quantity.given_to_hogeun",
                    "quantity.given_to_hyeongu",
                ],
                "whole": "quantity.total_given_marbles",
            },
            {
                "id": "relation.initial_decomposition",
                "type": "part_part_whole",
                "parts": [
                    "quantity.given_to_hogeun",
                    "quantity.given_to_hyeongu",
                    "quantity.remaining_marbles",
                ],
                "whole": "quantity.initial_marbles",
            },
        ],
    },
    "answer": ANSWER,
}

SEMANTIC_OVERRIDE = SEMANTIC


SOLVABLE = {
    "schema": "modu.solvable.v1.2",
    "problem_id": PROBLEM_ID,
    "problem_type": "numeric_answer_addition_word_problem",
    "inputs": {
        "target_label": "기영이가 처음 가지고 있던 구슬 수",
        "unit": "개",
        "quantities": {
            "given_to_hogeun": 120,
            "given_to_hyeongu": 130,
            "remaining": 220,
        },
        "conditions": [
            "기영이는 호근이에게 구슬 120개를 주었습니다.",
            "기영이는 형우에게 구슬 130개를 주었습니다.",
            "두 사람에게 구슬을 준 뒤 220개가 남았습니다.",
        ],
    },
    "given": [
        {
            "ref": "quantity.given_to_hogeun",
            "value": {
                "count": 120,
                "unit": "개",
                "receiver": "person.hogeun",
                "object": "object.marble",
            },
        },
        {
            "ref": "quantity.given_to_hyeongu",
            "value": {
                "count": 130,
                "unit": "개",
                "receiver": "person.hyeongu",
                "object": "object.marble",
            },
        },
        {
            "ref": "quantity.remaining_marbles",
            "value": {
                "count": 220,
                "unit": "개",
                "owner": "person.giyeong",
                "object": "object.marble",
            },
        },
    ],
    "target": {
        "ref": "quantity.initial_marbles",
        "type": "number",
    },
    "understanding": {
        "summary": (
            "기영이가 두 사람에게 준 구슬 수와 남은 구슬 수를 모두 더하여 "
            "처음 가지고 있던 구슬 수를 구하는 문제입니다."
        ),
        "facts": [
            {
                "ref": "quantity.given_to_hogeun",
                "label": "호근이에게 준 구슬 수",
                "value": 120,
                "unit": "개",
                "source": "explicit",
            },
            {
                "ref": "quantity.given_to_hyeongu",
                "label": "형우에게 준 구슬 수",
                "value": 130,
                "unit": "개",
                "source": "explicit",
            },
            {
                "ref": "quantity.remaining_marbles",
                "label": "남은 구슬 수",
                "value": 220,
                "unit": "개",
                "source": "explicit",
            },
        ],
        "unknowns": [
            {
                "ref": "quantity.initial_marbles",
                "label": "기영이가 처음 가지고 있던 구슬 수",
                "unit": "개",
                "source": "unknown",
            },
        ],
        "relation": {
            "type": "part_part_whole_addition",
            "statement": "처음 구슬은 두 사람에게 준 구슬과 남은 구슬을 합한 것입니다.",
            "symbolic": "처음 구슬 수 = 120 + 130 + 220",
            "uses": [
                "quantity.given_to_hogeun",
                "quantity.given_to_hyeongu",
                "quantity.remaining_marbles",
            ],
            "result": "quantity.initial_marbles",
        },
        "diagnostic_questions": [
            {
                "id": "understand.target",
                "type": "multiple_choice",
                "prompt": "이 문제에서 구해야 하는 것은 무엇인가요?",
                "choices": [
                    "호근이에게 준 구슬 수",
                    "두 사람에게 주고 남은 구슬 수",
                    "기영이가 처음 가지고 있던 구슬 수",
                ],
                "answer_index": 2,
            },
            {
                "id": "understand.relation",
                "type": "multiple_choice",
                "prompt": "처음 가지고 있던 구슬 수를 구하려면 어떻게 해야 하나요?",
                "choices": [
                    "120, 130, 220을 모두 더합니다.",
                    "220에서 120과 130을 뺍니다.",
                    "120과 130만 더합니다.",
                ],
                "answer_index": 0,
            },
        ],
        "student_restatement": {
            "prompt": "문제의 요지를 말해 볼까요?",
            "template": (
                "{first_given}개와 {second_given}개와 {remaining}개를 더해 "
                "{target_label}를 구합니다."
            ),
            "answer": "120개와 130개와 220개를 더해 처음 가지고 있던 구슬 수를 구합니다.",
        },
    },
    "method": "두 사람에게 준 구슬 수와 남은 구슬 수를 덧셈으로 합합니다.",
    "plan": [
        "호근이와 형우에게 준 구슬 수를 더합니다.",
        "두 사람에게 준 구슬 수에 남은 구슬 수를 더합니다.",
    ],
    "steps": [
        {
            "id": "step.add_given_marbles",
            "goal": "두 사람에게 준 구슬 수를 구합니다.",
            "uses": [
                "quantity.given_to_hogeun",
                "quantity.given_to_hyeongu",
            ],
            "relation_expr": "준 구슬 수 = 호근이에게 준 수 + 형우에게 준 수",
            "expr": "120 + 130",
            "value": {
                "count": 250,
                "unit": "개",
                "ref": "quantity.total_given_marbles",
            },
            "explanation": "120과 130을 더하면 두 사람에게 준 구슬은 250개입니다.",
        },
        {
            "id": "step.restore_initial_marbles",
            "goal": "처음 가지고 있던 구슬 수를 구합니다.",
            "uses": [
                "quantity.total_given_marbles",
                "quantity.remaining_marbles",
            ],
            "relation_expr": "처음 구슬 수 = 준 구슬 수 + 남은 구슬 수",
            "expr": "250 + 220",
            "value": {
                "count": 470,
                "unit": "개",
                "ref": "quantity.initial_marbles",
            },
            "explanation": "준 구슬 250개와 남은 구슬 220개를 더하면 처음 구슬은 470개입니다.",
        },
    ],
    "checks": [
        {
            "id": "check.forward_transfer",
            "expr": "470 - 120 - 130",
            "expected": 220,
            "actual": 220,
            "pass": True,
        },
        {
            "id": "check.direct_sum",
            "expr": "120 + 130 + 220",
            "expected": 470,
            "actual": 470,
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
                    "slot.expression",
                    "slot.answer",
                ),
            ),
        ),
        slots=(
            TextBoxSlot(
                id="slot.question",
                x=20,
                y=18,
                width=860,
                height=62,
                text=(
                    "기영이가 가지고 있던 구슬 중 120개를 호근이에게 주고, "
                    "형우에게 130개를 주었더니 남은 구슬은\n"
                    "220개가 되었습니다. 기영이가 처음에 가지고 있던 구슬은 몇 개입니까?"
                ),
                font_size=21,
                font_family="Noto Sans KR",
                fill="#202124",
                line_height=1.45,
                align="left",
                valign="top",
            ),
            TextBoxSlot(
                id="slot.expression",
                x=20,
                y=104,
                width=860,
                height=32,
                text="식",
                font_size=22,
                font_family="Noto Sans KR",
                fill="#202124",
                align="left",
                valign="middle",
            ),
            BlankSlot(
                id="slot.answer",
                prompt="답",
                answer_key="470",
                placeholder="개",
            ),
        ),
    )


PROBLEM_TEMPLATE = build_problem_template()
