from __future__ import annotations

from modu_math.dsl import (
    BlankSlot,
    Canvas,
    ProblemTemplate,
    Region,
    TextBoxSlot,
)


PROBLEM_ID = "P3_1_01_00040_07643"
PROBLEM_TITLE = "미정이와 하윤이가 읽은 동화책 쪽수"


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
                    "어제까지 동화책을 미정이는 129쪽 읽었고, 하윤이는 188쪽 읽었습니다. "
                    "미정이와 하윤이가 어제까지 읽은 동화책은 모두 몇 쪽입니까?"
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
                answer_key="317",
                placeholder="쪽",
            ),
        ),
    )


PROBLEM_TEMPLATE = build_problem_template()


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
                "id": "person.mijeong",
                "type": "person",
                "label": "미정이",
            },
            {
                "id": "person.hayoon",
                "type": "person",
                "label": "하윤이",
            },
            {
                "id": "object.storybook",
                "type": "book",
                "label": "동화책",
            },
            {
                "id": "quantity.mijeong_pages_read",
                "type": "quantity",
                "label": "미정이가 어제까지 읽은 쪽수",
                "value": 129,
                "unit": "쪽",
            },
            {
                "id": "quantity.hayoon_pages_read",
                "type": "quantity",
                "label": "하윤이가 어제까지 읽은 쪽수",
                "value": 188,
                "unit": "쪽",
            },
            {
                "id": "quantity.total_pages_read",
                "type": "quantity",
                "label": "두 사람이 어제까지 읽은 전체 쪽수",
                "value": 317,
                "unit": "쪽",
            },
        ],
        "relations": [
            {
                "id": "relation.mijeong_read_storybook",
                "type": "read",
                "subject": "person.mijeong",
                "object": "object.storybook",
                "quantity": "quantity.mijeong_pages_read",
                "time": "until_yesterday",
            },
            {
                "id": "relation.hayoon_read_storybook",
                "type": "read",
                "subject": "person.hayoon",
                "object": "object.storybook",
                "quantity": "quantity.hayoon_pages_read",
                "time": "until_yesterday",
            },
            {
                "id": "relation.total_pages_is_sum",
                "type": "sum_of",
                "subject": "quantity.total_pages_read",
                "objects": [
                    "quantity.mijeong_pages_read",
                    "quantity.hayoon_pages_read",
                ],
            },
        ],
    },
    "answer": {
        "type": "numeric",
        "value": 317,
        "unit": "쪽",
        "target_ref": "quantity.total_pages_read",
    },
}

SEMANTIC_OVERRIDE = SEMANTIC


SOLVABLE = {
    "schema": "modu.solvable.v1.2",
    "problem_id": PROBLEM_ID,
    "problem_type": "numeric_answer_addition_word_problem",
    "inputs": {
        "target_label": "두 사람이 어제까지 읽은 동화책의 전체 쪽수",
        "unit": "쪽",
        "quantities": {
            "mijeong_pages_read": 129,
            "hayoon_pages_read": 188,
        },
        "conditions": [
            "미정이는 어제까지 동화책을 129쪽 읽었습니다.",
            "하윤이는 어제까지 동화책을 188쪽 읽었습니다.",
            "두 사람이 어제까지 읽은 쪽수를 모두 구합니다.",
        ],
    },
    "given": [
        {
            "ref": "quantity.mijeong_pages_read",
            "value": {
                "count": 129,
                "unit": "쪽",
                "person": "person.mijeong",
                "object": "object.storybook",
                "time": "until_yesterday",
            },
        },
        {
            "ref": "quantity.hayoon_pages_read",
            "value": {
                "count": 188,
                "unit": "쪽",
                "person": "person.hayoon",
                "object": "object.storybook",
                "time": "until_yesterday",
            },
        },
    ],
    "target": {
        "ref": "quantity.total_pages_read",
        "type": "number",
    },
    "method": "미정이가 읽은 쪽수와 하윤이가 읽은 쪽수를 더합니다.",
    "plan": [
        "미정이가 어제까지 읽은 쪽수가 129쪽임을 확인합니다.",
        "하윤이가 어제까지 읽은 쪽수가 188쪽임을 확인합니다.",
        "두 사람이 읽은 쪽수를 더하여 전체 쪽수를 구합니다.",
    ],
    "steps": [
        {
            "id": "step.add_pages_read",
            "goal": "두 사람이 어제까지 읽은 전체 쪽수를 구합니다.",
            "uses": [
                "quantity.mijeong_pages_read",
                "quantity.hayoon_pages_read",
            ],
            "relation_expr": "전체 쪽수 = 미정이가 읽은 쪽수 + 하윤이가 읽은 쪽수",
            "expr": "129 + 188",
            "value": 317,
            "explanation": "두 사람이 읽은 동화책의 쪽수를 모두 구해야 하므로 129와 188을 더합니다.",
        }
    ],
    "checks": [
        {
            "id": "check.subtract_hayoon_pages",
            "description": "전체 쪽수에서 하윤이가 읽은 쪽수를 빼면 미정이가 읽은 쪽수가 됩니다.",
            "expr": "317 - 188",
            "expected": 129,
            "actual": 129,
            "pass": True,
        },
        {
            "id": "check.subtract_mijeong_pages",
            "description": "전체 쪽수에서 미정이가 읽은 쪽수를 빼면 하윤이가 읽은 쪽수가 됩니다.",
            "expr": "317 - 129",
            "expected": 188,
            "actual": 188,
            "pass": True,
        },
    ],
    "answer": {
        "type": "numeric",
        "value": 317,
        "unit": "쪽",
        "target_ref": "quantity.total_pages_read",
    },
    "understanding": {
        "summary": "미정이와 하윤이가 어제까지 읽은 동화책의 쪽수를 더해 전체 쪽수를 구하는 문제입니다.",
        "facts": [
            {
                "ref": "quantity.mijeong_pages_read",
                "label": "미정이가 어제까지 읽은 쪽수",
                "value": 129,
                "unit": "쪽",
                "source": "explicit",
            },
            {
                "ref": "quantity.hayoon_pages_read",
                "label": "하윤이가 어제까지 읽은 쪽수",
                "value": 188,
                "unit": "쪽",
                "source": "explicit",
            },
        ],
        "unknowns": [
            {
                "ref": "quantity.total_pages_read",
                "label": "두 사람이 어제까지 읽은 전체 쪽수",
                "unit": "쪽",
                "source": "unknown",
            }
        ],
        "relation": {
            "type": "part_part_whole_addition",
            "statement": "두 사람이 각각 읽은 쪽수를 합하면 두 사람이 읽은 전체 쪽수가 됩니다.",
            "symbolic": "129 + 188 = 317",
            "uses": [
                "quantity.mijeong_pages_read",
                "quantity.hayoon_pages_read",
            ],
            "result": "quantity.total_pages_read",
        },
        "diagnostic_questions": [
            {
                "id": "understand.target",
                "type": "multiple_choice",
                "prompt": "이 문제에서 구해야 하는 것은 무엇인가요?",
                "choices": [
                    "미정이가 읽은 쪽수",
                    "하윤이가 읽은 쪽수",
                    "두 사람이 읽은 전체 쪽수",
                ],
                "answer_index": 2,
            },
            {
                "id": "understand.operation",
                "type": "multiple_choice",
                "prompt": "두 사람이 읽은 쪽수를 모두 구하려면 어떻게 계산해야 하나요?",
                "choices": [
                    "129와 188을 더합니다.",
                    "188에서 129를 뺍니다.",
                    "129에서 188을 뺍니다.",
                ],
                "answer_index": 0,
            },
        ],
        "student_restatement": {
            "prompt": "문제의 뜻을 말해 볼까요?",
            "template": "미정이는 {mijeong}쪽, 하윤이는 {hayoon}쪽을 읽었으므로, 두 사람이 읽은 {target}를 구합니다.",
            "answer": "미정이는 129쪽, 하윤이는 188쪽을 읽었으므로, 두 사람이 읽은 전체 쪽수를 구합니다.",
        },
    },
}


SEMANTIC_ANSWER = SOLVABLE["answer"]
