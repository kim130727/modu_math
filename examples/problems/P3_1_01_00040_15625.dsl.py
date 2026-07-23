from __future__ import annotations

from modu_math.dsl import (
    BlankSlot,
    Canvas,
    ProblemTemplate,
    Region,
    TextBoxSlot,
)


PROBLEM_ID = "P3_1_01_00040_15625"
PROBLEM_TITLE = "재형이의 앨범에 있는 사진 수"


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
                    "재형이의 앨범에는 324장의 가족 사진과 133장의 친구 사진이 있습니다. "
                    "그리고 혼자 찍은 사진도 102장이 있습니다. 사진은 모두 몇 장입니까?"
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
                answer_key="559",
                placeholder="장",
            ),
        ),
    )


PROBLEM_TEMPLATE = build_problem_template()


ANSWER = {
    "type": "numeric",
    "value": 559,
    "unit": "장",
    "target_ref": "quantity.total_photos",
    "derived_from": "step.add_single_photos",
}


SEMANTIC_OVERRIDE = {
    "problem_id": PROBLEM_ID,
    "problem_type": "numeric_answer_three_addends_word_problem",
    "metadata": {
        "grade": 3,
        "semester": 1,
        "subject": "수학",
        "topic": "세 자리 수의 덧셈",
        "language": "ko-KR",
        "question": (
            "재형이의 앨범에는 324장의 가족 사진과 133장의 친구 사진이 있습니다. "
            "그리고 혼자 찍은 사진도 102장이 있습니다. 사진은 모두 몇 장입니까?"
        ),
        "instruction": "가족 사진, 친구 사진, 혼자 찍은 사진의 수를 모두 더합니다.",
    },
    "domain": {
        "objects": [
            {
                "id": "person.jaehyeong",
                "type": "person",
                "label": "재형이",
            },
            {
                "id": "object.album",
                "type": "container",
                "label": "재형이의 앨범",
            },
            {
                "id": "object.photo",
                "type": "countable_object",
                "label": "사진",
                "unit": "장",
            },
            {
                "id": "category.family_photo",
                "type": "photo_category",
                "label": "가족 사진",
            },
            {
                "id": "category.friend_photo",
                "type": "photo_category",
                "label": "친구 사진",
            },
            {
                "id": "category.single_photo",
                "type": "photo_category",
                "label": "혼자 찍은 사진",
            },
            {
                "id": "quantity.family_photos",
                "type": "quantity",
                "label": "가족 사진 수",
                "value": 324,
                "unit": "장",
            },
            {
                "id": "quantity.friend_photos",
                "type": "quantity",
                "label": "친구 사진 수",
                "value": 133,
                "unit": "장",
            },
            {
                "id": "quantity.single_photos",
                "type": "quantity",
                "label": "혼자 찍은 사진 수",
                "value": 102,
                "unit": "장",
            },
            {
                "id": "quantity.family_and_friend_photos",
                "type": "derived_quantity",
                "label": "가족 사진과 친구 사진의 합",
                "value": 457,
                "unit": "장",
            },
            {
                "id": "quantity.total_photos",
                "type": "unknown_quantity",
                "label": "앨범에 있는 전체 사진 수",
                "unit": "장",
            },
        ],
        "relations": [
            {
                "id": "relation.album_belongs_to_jaehyeong",
                "type": "belongs_to",
                "subject": "object.album",
                "owner": "person.jaehyeong",
            },
            {
                "id": "relation.album_contains_family_photos",
                "type": "contains",
                "container": "object.album",
                "object": "category.family_photo",
                "quantity_ref": "quantity.family_photos",
            },
            {
                "id": "relation.album_contains_friend_photos",
                "type": "contains",
                "container": "object.album",
                "object": "category.friend_photo",
                "quantity_ref": "quantity.friend_photos",
            },
            {
                "id": "relation.album_contains_single_photos",
                "type": "contains",
                "container": "object.album",
                "object": "category.single_photo",
                "quantity_ref": "quantity.single_photos",
            },
            {
                "id": "relation.total_is_sum",
                "type": "sum_of",
                "subject": "quantity.total_photos",
                "objects": [
                    "quantity.family_photos",
                    "quantity.friend_photos",
                    "quantity.single_photos",
                ],
            },
        ],
        "problem_solving": {
            "understand": {
                "given_refs": [
                    "quantity.family_photos",
                    "quantity.friend_photos",
                    "quantity.single_photos",
                ],
                "target_ref": "quantity.total_photos",
                "condition_refs": [
                    "relation.total_is_sum",
                ],
            },
            "plan": {
                "method": "sequential_addition",
                "description": "가족 사진과 친구 사진을 먼저 더한 뒤 혼자 찍은 사진을 더합니다.",
            },
            "execute": {
                "expected_operations": [
                    "addition",
                    "addition",
                ],
            },
            "review": {
                "check_methods": [
                    "inverse_subtraction",
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
    "problem_type": "numeric_answer_three_addends_word_problem",
    "inputs": {
        "target_label": "재형이의 앨범에 있는 전체 사진 수",
        "unit": "장",
        "quantities": {
            "family_photo_count": 324,
            "friend_photo_count": 133,
            "single_photo_count": 102,
        },
        "conditions": [
            "가족 사진은 324장입니다.",
            "친구 사진은 133장입니다.",
            "혼자 찍은 사진은 102장입니다.",
            "세 종류의 사진 수를 모두 구합니다.",
        ],
    },
    "given": [
        {
            "ref": "quantity.family_photos",
            "value": {
                "count": 324,
                "unit": "장",
                "category": "category.family_photo",
                "container": "object.album",
            },
        },
        {
            "ref": "quantity.friend_photos",
            "value": {
                "count": 133,
                "unit": "장",
                "category": "category.friend_photo",
                "container": "object.album",
            },
        },
        {
            "ref": "quantity.single_photos",
            "value": {
                "count": 102,
                "unit": "장",
                "category": "category.single_photo",
                "container": "object.album",
            },
        },
    ],
    "target": {
        "ref": "quantity.total_photos",
        "type": "number",
    },
    "understanding": {
        "summary": (
            "재형이의 앨범에 있는 가족 사진, 친구 사진, 혼자 찍은 사진의 수를 "
            "모두 더하여 전체 사진 수를 구하는 문제입니다."
        ),
        "facts": [
            {
                "ref": "quantity.family_photos",
                "label": "가족 사진 수",
                "value": 324,
                "unit": "장",
                "source": "explicit",
            },
            {
                "ref": "quantity.friend_photos",
                "label": "친구 사진 수",
                "value": 133,
                "unit": "장",
                "source": "explicit",
            },
            {
                "ref": "quantity.single_photos",
                "label": "혼자 찍은 사진 수",
                "value": 102,
                "unit": "장",
                "source": "explicit",
            },
        ],
        "unknowns": [
            {
                "ref": "quantity.total_photos",
                "label": "앨범에 있는 전체 사진 수",
                "unit": "장",
                "source": "unknown",
            },
        ],
        "relation": {
            "type": "part_part_part_whole_addition",
            "statement": "전체 사진 수는 세 종류의 사진 수를 모두 더한 값입니다.",
            "symbolic": "전체 = 가족 사진 + 친구 사진 + 혼자 찍은 사진",
            "uses": [
                "quantity.family_photos",
                "quantity.friend_photos",
                "quantity.single_photos",
            ],
            "result": "quantity.total_photos",
        },
        "diagnostic_questions": [
            {
                "id": "understand.target",
                "type": "multiple_choice",
                "prompt": "이 문제에서 구해야 하는 것은 무엇인가요?",
                "choices": [
                    "가족 사진 수",
                    "친구 사진 수",
                    "앨범에 있는 전체 사진 수",
                ],
                "answer_index": 2,
            },
            {
                "id": "understand.operation",
                "type": "multiple_choice",
                "prompt": "사진이 모두 몇 장인지 구하려면 어떻게 해야 하나요?",
                "choices": [
                    "324, 133, 102를 모두 더합니다.",
                    "324에서 133과 102를 뺍니다.",
                    "가장 큰 수와 가장 작은 수만 더합니다.",
                ],
                "answer_index": 0,
            },
        ],
        "student_restatement": {
            "prompt": "문제의 요지를 말해 볼까요?",
            "template": (
                "{family_count}장, {friend_count}장, {single_count}장을 모두 더해 "
                "{target_label}를 구합니다."
            ),
            "answer": "324장, 133장, 102장을 모두 더해 앨범에 있는 전체 사진 수를 구합니다.",
        },
    },
    "method": "324와 133을 먼저 더한 뒤, 그 결과에 102를 더합니다.",
    "plan": [
        "가족 사진, 친구 사진, 혼자 찍은 사진의 수를 확인합니다.",
        "가족 사진 324장과 친구 사진 133장을 더합니다.",
        "앞에서 구한 수에 혼자 찍은 사진 102장을 더합니다.",
    ],
    "steps": [
        {
            "id": "step.add_family_and_friend_photos",
            "goal": "가족 사진과 친구 사진을 합한 수를 구합니다.",
            "uses": [
                "quantity.family_photos",
                "quantity.friend_photos",
            ],
            "relation_expr": "중간 합 = 가족 사진 + 친구 사진",
            "expr": "324 + 133",
            "value": 457,
            "explanation": "가족 사진 324장과 친구 사진 133장을 더하면 457장입니다.",
        },
        {
            "id": "step.add_single_photos",
            "goal": "앨범에 있는 전체 사진 수를 구합니다.",
            "uses": [
                "quantity.family_and_friend_photos",
                "quantity.single_photos",
            ],
            "relation_expr": "전체 = 중간 합 + 혼자 찍은 사진",
            "expr": "457 + 102",
            "value": 559,
            "explanation": "457장에 혼자 찍은 사진 102장을 더하면 모두 559장입니다.",
        },
    ],
    "checks": [
        {
            "id": "check.subtract_single_photos",
            "expr": "559 - 102",
            "expected": 457,
            "actual": 457,
            "pass": True,
        },
        {
            "id": "check.subtract_friend_photos",
            "expr": "457 - 133",
            "expected": 324,
            "actual": 324,
            "pass": True,
        },
        {
            "id": "check.direct_addition",
            "expr": "324 + 133 + 102",
            "expected": 559,
            "actual": 559,
            "pass": True,
        },
    ],
    "answer": ANSWER,
}


SEMANTIC_ANSWER = SOLVABLE["answer"]
