from __future__ import annotations

from modu_math.dsl import (
    BlankSlot,
    Canvas,
    ProblemTemplate,
    Region,
    TextBoxSlot,
)


PROBLEM_ID = "P3_1_01_00040_15606"
PROBLEM_TITLE = "지영이가 가지고 있는 구슬 수"


ANSWER = {
    "type": "numeric",
    "value": 377,
    "unit": "개",
    "target_ref": "quantity.jiyeong_marbles",
    "derived_from": "step.add_difference",
}


SEMANTIC_OVERRIDE = {
    "problem_id": PROBLEM_ID,
    "problem_type": "numeric_answer_more_than_addition_word_problem",
    "metadata": {
        "grade": 3,
        "semester": 1,
        "subject": "수학",
        "topic": "세 자리 수의 덧셈",
        "language": "ko-KR",
        "question": "지영이가 가지고 있는 구슬은 모두 몇 개입니까?",
    },
    "domain": {
        "objects": [
            {
                "id": "person.gyeongmin",
                "type": "person",
                "label": "경민이",
            },
            {
                "id": "person.jiyeong",
                "type": "person",
                "label": "지영이",
            },
            {
                "id": "object.marble",
                "type": "countable_object",
                "label": "구슬",
                "unit": "개",
            },
            {
                "id": "quantity.gyeongmin_marbles",
                "type": "quantity",
                "label": "경민이가 가진 구슬 수",
                "value": 254,
                "unit": "개",
            },
            {
                "id": "quantity.more_marbles",
                "type": "quantity",
                "label": "지영이가 더 가진 구슬 수",
                "value": 123,
                "unit": "개",
            },
            {
                "id": "quantity.jiyeong_marbles",
                "type": "quantity",
                "label": "지영이가 가진 구슬 수",
                "value": 377,
                "unit": "개",
            },
        ],
        "relations": [
            {
                "id": "relation.gyeongmin_has_marbles",
                "type": "has_quantity",
                "subject": "person.gyeongmin",
                "object": "object.marble",
                "quantity": "quantity.gyeongmin_marbles",
            },
            {
                "id": "relation.jiyeong_more_than_gyeongmin",
                "type": "more_than",
                "subject": "quantity.jiyeong_marbles",
                "reference": "quantity.gyeongmin_marbles",
                "difference": "quantity.more_marbles",
            },
            {
                "id": "relation.jiyeong_count_is_sum",
                "type": "sum_of",
                "subject": "quantity.jiyeong_marbles",
                "objects": [
                    "quantity.gyeongmin_marbles",
                    "quantity.more_marbles",
                ],
            },
        ],
    },
    "answer": ANSWER,
}


SOLVABLE = {
    "schema": "modu.solvable.v1.2",
    "problem_id": PROBLEM_ID,
    "problem_type": "numeric_answer_more_than_addition_word_problem",
    "inputs": {
        "target_label": "지영이가 가지고 있는 구슬 수",
        "unit": "개",
        "quantities": {
            "gyeongmin_count": 254,
            "jiyeong_more_count": 123,
        },
        "conditions": [
            "경민이는 구슬을 254개 가지고 있습니다.",
            "지영이는 경민이보다 구슬을 123개 더 가지고 있습니다.",
        ],
    },
    "given": [
        {
            "ref": "quantity.gyeongmin_marbles",
            "value": {
                "count": 254,
                "unit": "개",
                "owner": "person.gyeongmin",
                "object": "object.marble",
            },
        },
        {
            "ref": "quantity.more_marbles",
            "value": {
                "count": 123,
                "unit": "개",
                "comparison_subject": "person.jiyeong",
                "comparison_reference": "person.gyeongmin",
                "object": "object.marble",
            },
        },
    ],
    "target": {
        "ref": "quantity.jiyeong_marbles",
        "type": "number",
    },
    "understanding": {
        "summary": (
            "경민이의 구슬 수에 지영이가 더 가진 구슬 수를 더하여 "
            "지영이의 전체 구슬 수를 구하는 문제입니다."
        ),
        "facts": [
            {
                "ref": "quantity.gyeongmin_marbles",
                "label": "경민이가 가진 구슬 수",
                "value": 254,
                "unit": "개",
                "source": "explicit",
            },
            {
                "ref": "quantity.more_marbles",
                "label": "지영이가 경민이보다 더 가진 구슬 수",
                "value": 123,
                "unit": "개",
                "source": "explicit",
            },
        ],
        "unknowns": [
            {
                "ref": "quantity.jiyeong_marbles",
                "label": "지영이가 가진 구슬 수",
                "unit": "개",
                "source": "unknown",
            },
        ],
        "relation": {
            "type": "compare_more_unknown_larger_addition",
            "statement": "더 많이 가진 지영이의 구슬 수는 경민이의 구슬 수와 더 가진 수의 합입니다.",
            "symbolic": "지영이의 구슬 수 = 254 + 123",
            "uses": [
                "quantity.gyeongmin_marbles",
                "quantity.more_marbles",
            ],
            "result": "quantity.jiyeong_marbles",
        },
        "diagnostic_questions": [
            {
                "id": "understand.target",
                "type": "multiple_choice",
                "prompt": "이 문제에서 구해야 하는 것은 무엇인가요?",
                "choices": [
                    "경민이가 가진 구슬 수",
                    "지영이가 더 가진 구슬 수",
                    "지영이가 가진 구슬 수",
                ],
                "answer_index": 2,
            },
            {
                "id": "understand.comparison",
                "type": "multiple_choice",
                "prompt": "구슬을 더 많이 가지고 있는 사람은 누구인가요?",
                "choices": ["경민이", "지영이", "두 사람의 수가 같습니다."],
                "answer_index": 1,
            },
            {
                "id": "understand.operation",
                "type": "multiple_choice",
                "prompt": "지영이의 구슬 수를 구하는 식은 무엇인가요?",
                "choices": ["254 + 123", "254 - 123", "123 - 254"],
                "answer_index": 0,
            },
        ],
        "student_restatement": {
            "prompt": "문제의 요지를 말해 볼까요?",
            "template": "{base_count}개보다 {more_count}개 더 많은 수를 덧셈으로 구합니다.",
            "answer": "254개보다 123개 더 많은 구슬 수를 덧셈으로 구합니다.",
        },
    },
    "method": "기준이 되는 254개에 더 많은 123개를 더합니다.",
    "plan": [
        "경민이가 가진 구슬 수 254개를 확인합니다.",
        "지영이가 더 가진 구슬 수 123개를 확인합니다.",
        "254와 123을 더하여 지영이의 구슬 수를 구합니다.",
    ],
    "steps": [
        {
            "id": "step.add_difference",
            "goal": "지영이가 가진 구슬 수를 구합니다.",
            "uses": [
                "quantity.gyeongmin_marbles",
                "quantity.more_marbles",
            ],
            "relation_expr": "지영이의 구슬 수 = 경민이의 구슬 수 + 더 가진 구슬 수",
            "expr": "254 + 123",
            "value": 377,
            "explanation": "지영이가 123개 더 가지고 있으므로 254와 123을 더합니다.",
        },
    ],
    "checks": [
        {
            "id": "check.inverse_subtraction",
            "expr": "377 - 123",
            "expected": 254,
            "actual": 254,
            "pass": True,
        },
        {
            "id": "check.difference",
            "expr": "377 - 254",
            "expected": 123,
            "actual": 123,
            "pass": True,
        },
        {
            "id": "check.jiyeong_has_more",
            "expr": "377 > 254",
            "expected": True,
            "actual": True,
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
            height=190,
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
                    "경민이는 구슬을 254개 가지고 있고, 지영이는 경민이보다 123개 더 가지고 있습니다. "
                    "지영이가 가지고 있는 구슬은 모두 몇 개입니까?"
                ),
                font_size=21,
                font_family="Noto Sans KR",
                fill="#202124",
                line_height=1.45,
                align="left",
                valign="top",
            ),
            BlankSlot(
                id="slot.expression",
                prompt="식",
                answer_key="254 + 123 = 377",
                placeholder="",
            ),
            BlankSlot(
                id="slot.answer",
                prompt="답",
                answer_key="377",
                placeholder="개",
            ),
        ),
    )


PROBLEM_TEMPLATE = build_problem_template()
