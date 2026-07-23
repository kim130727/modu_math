from __future__ import annotations

from modu_math.dsl import (
    BlankSlot,
    Canvas,
    ProblemTemplate,
    Region,
    TextBoxSlot,
)


PROBLEM_ID = "P3_1_01_00040_15622"
PROBLEM_TITLE = "진우와 윤지가 주운 밤의 수"


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
                    "진우는 윤지와 함께 밤을 주웠습니다. 진우는 231개를 주웠고, "
                    "윤지는 진우보다 26개를 더 주웠습니다. 두 사람이 주운 밤은 "
                    "모두 몇 개입니까?"
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
                answer_key="488",
                placeholder="개",
            ),
        ),
    )


PROBLEM_TEMPLATE = build_problem_template()


ANSWER = {
    "type": "numeric",
    "value": 488,
    "unit": "개",
    "target_ref": "quantity.total_chestnuts",
    "derived_from": "step.add_two_counts",
}


SEMANTIC_OVERRIDE = {
    "problem_id": PROBLEM_ID,
    "problem_type": "numeric_answer_comparison_then_addition_word_problem",
    "metadata": {
        "grade": 3,
        "semester": 1,
        "subject": "수학",
        "topic": "세 자리 수의 덧셈",
        "language": "ko-KR",
        "question": (
            "진우는 윤지와 함께 밤을 주웠습니다. 진우는 231개를 주웠고, "
            "윤지는 진우보다 26개를 더 주웠습니다. 두 사람이 주운 밤은 "
            "모두 몇 개입니까?"
        ),
        "instruction": "윤지가 주운 밤의 수를 먼저 구한 뒤 두 사람이 주운 수를 더합니다.",
    },
    "domain": {
        "objects": [
            {
                "id": "person.jinwoo",
                "type": "person",
                "label": "진우",
            },
            {
                "id": "person.yoonji",
                "type": "person",
                "label": "윤지",
            },
            {
                "id": "object.chestnut",
                "type": "countable_object",
                "label": "밤",
                "unit": "개",
            },
            {
                "id": "quantity.jinwoo_chestnuts",
                "type": "quantity",
                "label": "진우가 주운 밤의 수",
                "value": 231,
                "unit": "개",
            },
            {
                "id": "quantity.more_chestnuts",
                "type": "quantity_difference",
                "label": "윤지가 진우보다 더 주운 밤의 수",
                "value": 26,
                "unit": "개",
            },
            {
                "id": "quantity.yoonji_chestnuts",
                "type": "derived_quantity",
                "label": "윤지가 주운 밤의 수",
                "value": 257,
                "unit": "개",
            },
            {
                "id": "quantity.total_chestnuts",
                "type": "unknown_quantity",
                "label": "두 사람이 주운 밤의 수",
                "unit": "개",
            },
        ],
        "relations": [
            {
                "id": "relation.jinwoo_collected_chestnuts",
                "type": "collected",
                "subject": "person.jinwoo",
                "object": "object.chestnut",
                "quantity_ref": "quantity.jinwoo_chestnuts",
            },
            {
                "id": "relation.yoonji_collected_chestnuts",
                "type": "collected",
                "subject": "person.yoonji",
                "object": "object.chestnut",
                "quantity_ref": "quantity.yoonji_chestnuts",
            },
            {
                "id": "relation.yoonji_has_more",
                "type": "additive_comparison",
                "greater_ref": "quantity.yoonji_chestnuts",
                "smaller_ref": "quantity.jinwoo_chestnuts",
                "difference_ref": "quantity.more_chestnuts",
            },
            {
                "id": "relation.total_is_sum",
                "type": "sum_of",
                "subject": "quantity.total_chestnuts",
                "objects": [
                    "quantity.jinwoo_chestnuts",
                    "quantity.yoonji_chestnuts",
                ],
            },
        ],
        "problem_solving": {
            "understand": {
                "given_refs": [
                    "quantity.jinwoo_chestnuts",
                    "quantity.more_chestnuts",
                ],
                "target_ref": "quantity.total_chestnuts",
                "condition_refs": [
                    "relation.yoonji_has_more",
                    "relation.total_is_sum",
                ],
            },
            "plan": {
                "method": "comparison_addition_then_total_addition",
                "description": "윤지가 주운 수를 구하고, 그 수와 진우가 주운 수를 더합니다.",
            },
            "execute": {
                "expected_operations": [
                    "addition",
                    "addition",
                ],
            },
            "review": {
                "check_methods": [
                    "difference_check",
                    "recomposition",
                ],
            },
        },
    },
    "answer": ANSWER,
}


SOLVABLE = {
    "schema": "modu.solvable.v1.2",
    "problem_id": PROBLEM_ID,
    "problem_type": "numeric_answer_comparison_then_addition_word_problem",
    "inputs": {
        "target_label": "두 사람이 주운 밤의 수",
        "unit": "개",
        "quantities": {
            "jinwoo_count": 231,
            "yoonji_more_count": 26,
        },
        "conditions": [
            "진우는 밤을 231개 주웠습니다.",
            "윤지는 진우보다 밤을 26개 더 주웠습니다.",
            "두 사람이 주운 밤의 수를 모두 구합니다.",
        ],
    },
    "given": [
        {
            "ref": "quantity.jinwoo_chestnuts",
            "value": {
                "count": 231,
                "unit": "개",
                "owner": "person.jinwoo",
                "object": "object.chestnut",
            },
        },
        {
            "ref": "quantity.more_chestnuts",
            "value": {
                "count": 26,
                "unit": "개",
                "greater_owner": "person.yoonji",
                "smaller_owner": "person.jinwoo",
            },
        },
    ],
    "target": {
        "ref": "quantity.total_chestnuts",
        "type": "number",
    },
    "understanding": {
        "summary": (
            "진우가 주운 밤의 수와 윤지가 진우보다 더 주운 수를 이용해 "
            "윤지가 주운 수를 먼저 구한 뒤, 두 사람의 수를 합하는 문제입니다."
        ),
        "facts": [
            {
                "ref": "quantity.jinwoo_chestnuts",
                "label": "진우가 주운 밤의 수",
                "value": 231,
                "unit": "개",
                "source": "explicit",
            },
            {
                "ref": "quantity.more_chestnuts",
                "label": "윤지가 진우보다 더 주운 밤의 수",
                "value": 26,
                "unit": "개",
                "source": "explicit",
            },
        ],
        "unknowns": [
            {
                "ref": "quantity.yoonji_chestnuts",
                "label": "윤지가 주운 밤의 수",
                "unit": "개",
                "source": "derived",
            },
            {
                "ref": "quantity.total_chestnuts",
                "label": "두 사람이 주운 밤의 수",
                "unit": "개",
                "source": "unknown",
            },
        ],
        "relation": {
            "type": "comparison_then_part_part_whole_addition",
            "statement": (
                "윤지가 주운 밤은 진우가 주운 밤보다 26개 많고, "
                "두 사람이 주운 밤은 두 사람 각각의 수를 더한 값입니다."
            ),
            "symbolic": "윤지 = 진우 + 26; 전체 = 진우 + 윤지",
            "uses": [
                "quantity.jinwoo_chestnuts",
                "quantity.more_chestnuts",
                "quantity.yoonji_chestnuts",
            ],
            "result": "quantity.total_chestnuts",
        },
        "diagnostic_questions": [
            {
                "id": "understand.intermediate",
                "type": "multiple_choice",
                "prompt": "두 사람의 전체 수를 구하기 전에 먼저 알아야 하는 것은 무엇인가요?",
                "choices": [
                    "윤지가 주운 밤의 수",
                    "두 사람이 주운 밤의 차",
                    "진우가 더 주운 밤의 수",
                ],
                "answer_index": 0,
            },
            {
                "id": "understand.comparison",
                "type": "multiple_choice",
                "prompt": "윤지가 주운 밤의 수를 구하려면 어떻게 해야 하나요?",
                "choices": [
                    "231과 26을 더합니다.",
                    "231에서 26을 뺍니다.",
                    "231과 26을 곱합니다.",
                ],
                "answer_index": 0,
            },
            {
                "id": "understand.target",
                "type": "multiple_choice",
                "prompt": "마지막에 구해야 하는 것은 무엇인가요?",
                "choices": [
                    "진우가 주운 밤의 수",
                    "윤지가 주운 밤의 수",
                    "두 사람이 주운 밤의 수",
                ],
                "answer_index": 2,
            },
        ],
        "student_restatement": {
            "prompt": "문제의 요지를 말해 볼까요?",
            "template": (
                "{jinwoo_count}개보다 {more_count}개 많은 윤지의 수를 먼저 구하고, "
                "두 사람의 수를 더해 {target_label}를 구합니다."
            ),
            "answer": (
                "231개보다 26개 많은 윤지의 밤 수를 먼저 구하고, "
                "진우와 윤지의 밤 수를 더해 전체를 구합니다."
            ),
        },
    },
    "method": "231에 26을 더해 윤지가 주운 수를 구한 뒤, 231과 그 결과를 더합니다.",
    "plan": [
        "진우가 주운 밤의 수가 231개임을 확인합니다.",
        "231에 26을 더하여 윤지가 주운 밤의 수를 구합니다.",
        "진우와 윤지가 주운 밤의 수를 더하여 전체를 구합니다.",
    ],
    "steps": [
        {
            "id": "step.find_yoonji_count",
            "goal": "윤지가 주운 밤의 수를 구합니다.",
            "uses": [
                "quantity.jinwoo_chestnuts",
                "quantity.more_chestnuts",
            ],
            "relation_expr": "윤지 = 진우 + 더 주운 수",
            "expr": "231 + 26",
            "value": 257,
            "explanation": "윤지는 진우보다 26개 더 주웠으므로 231과 26을 더합니다.",
        },
        {
            "id": "step.add_two_counts",
            "goal": "두 사람이 주운 밤의 수를 모두 구합니다.",
            "uses": [
                "quantity.jinwoo_chestnuts",
                "quantity.yoonji_chestnuts",
            ],
            "relation_expr": "전체 = 진우 + 윤지",
            "expr": "231 + 257",
            "value": 488,
            "explanation": "두 사람이 주운 밤의 수를 모두 구하므로 231과 257을 더합니다.",
        },
    ],
    "checks": [
        {
            "id": "check.yoonji_difference",
            "expr": "257 - 231",
            "expected": 26,
            "actual": 26,
            "pass": True,
        },
        {
            "id": "check.total_minus_jinwoo",
            "expr": "488 - 231",
            "expected": 257,
            "actual": 257,
            "pass": True,
        },
        {
            "id": "check.recalculate_total",
            "expr": "231 + (231 + 26)",
            "expected": 488,
            "actual": 488,
            "pass": True,
        },
    ],
    "answer": ANSWER,
}


SEMANTIC_ANSWER = SOLVABLE["answer"]
