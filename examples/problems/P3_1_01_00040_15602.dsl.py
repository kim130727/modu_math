from __future__ import annotations

from modu_math.dsl import (
    BlankSlot,
    Canvas,
    ProblemTemplate,
    Region,
    TextBoxSlot,
)


PROBLEM_ID = "P3_1_01_00040_15602"
PROBLEM_TITLE = "사진첩에 있는 사진의 수"


ANSWER = {
    "type": "numeric",
    "value": 842,
    "unit": "장",
    "target_ref": "quantity.total_photos",
    "derived_from": "step.add_photo_counts",
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
        "question": "동윤이의 사진첩에 있는 사진은 모두 몇 장입니까?",
        "instruction": "가족 사진 수와 친구 사진 수를 더합니다.",
    },
    "domain": {
        "objects": [
            {
                "id": "person.dongyun",
                "type": "person",
                "label": "동윤이",
            },
            {
                "id": "collection.dongyun_photo_album",
                "type": "photo_album",
                "label": "동윤이의 사진첩",
                "owner": "person.dongyun",
            },
            {
                "id": "object.family_photo",
                "type": "photo_category",
                "label": "가족 사진",
            },
            {
                "id": "object.friend_photo",
                "type": "photo_category",
                "label": "친구 사진",
            },
            {
                "id": "quantity.family_photos",
                "type": "quantity",
                "label": "가족 사진 수",
                "value": 527,
                "unit": "장",
            },
            {
                "id": "quantity.friend_photos",
                "type": "quantity",
                "label": "친구 사진 수",
                "value": 315,
                "unit": "장",
            },
            {
                "id": "quantity.total_photos",
                "type": "unknown_quantity",
                "label": "사진첩에 있는 전체 사진 수",
                "unit": "장",
            },
        ],
        "relations": [
            {
                "id": "relation.album_contains_family_photos",
                "type": "contains",
                "subject": "collection.dongyun_photo_album",
                "object": "object.family_photo",
                "quantity": "quantity.family_photos",
            },
            {
                "id": "relation.album_contains_friend_photos",
                "type": "contains",
                "subject": "collection.dongyun_photo_album",
                "object": "object.friend_photo",
                "quantity": "quantity.friend_photos",
            },
            {
                "id": "relation.total_is_sum",
                "type": "sum_of",
                "subject": "quantity.total_photos",
                "objects": [
                    "quantity.family_photos",
                    "quantity.friend_photos",
                ],
            },
        ],
        "problem_solving": {
            "understand": {
                "given_refs": [
                    "quantity.family_photos",
                    "quantity.friend_photos",
                ],
                "target_ref": "quantity.total_photos",
                "condition_refs": ["relation.total_is_sum"],
            },
            "plan": {
                "method": "part_part_whole_addition",
                "description": "가족 사진 수와 친구 사진 수를 더합니다.",
            },
            "execute": {
                "expected_operations": ["addition"],
            },
            "review": {
                "check_methods": ["subtraction_check", "magnitude_check"],
            },
        },
    },
    "answer": ANSWER,
}


SEMANTIC = SEMANTIC_OVERRIDE


SOLVABLE = {
    "schema": "modu.solvable.v1.2",
    "problem_id": PROBLEM_ID,
    "problem_type": "numeric_answer_addition_word_problem",
    "inputs": {
        "target_label": "사진첩에 있는 전체 사진 수",
        "unit": "장",
        "quantities": {
            "family_photo_count": 527,
            "friend_photo_count": 315,
        },
        "conditions": [
            "동윤이의 사진첩에는 가족 사진이 527장 있습니다.",
            "동윤이의 사진첩에는 친구 사진이 315장 있습니다.",
            "두 종류의 사진을 합한 전체 사진 수를 구합니다.",
        ],
    },
    "given": [
        {
            "ref": "quantity.family_photos",
            "value": {
                "count": 527,
                "unit": "장",
                "category": "object.family_photo",
                "container": "collection.dongyun_photo_album",
            },
        },
        {
            "ref": "quantity.friend_photos",
            "value": {
                "count": 315,
                "unit": "장",
                "category": "object.friend_photo",
                "container": "collection.dongyun_photo_album",
            },
        },
    ],
    "target": {
        "ref": "quantity.total_photos",
        "type": "number",
    },
    "understanding": {
        "summary": "가족 사진 527장과 친구 사진 315장을 합하여 사진첩에 있는 전체 사진 수를 구하는 문제입니다.",
        "facts": [
            {
                "ref": "quantity.family_photos",
                "label": "가족 사진 수",
                "value": 527,
                "unit": "장",
                "source": "explicit",
            },
            {
                "ref": "quantity.friend_photos",
                "label": "친구 사진 수",
                "value": 315,
                "unit": "장",
                "source": "explicit",
            },
        ],
        "unknowns": [
            {
                "ref": "quantity.total_photos",
                "label": "사진첩에 있는 전체 사진 수",
                "unit": "장",
                "source": "unknown",
            },
        ],
        "relation": {
            "type": "part_part_whole_addition",
            "statement": "가족 사진 수와 친구 사진 수를 더하면 사진첩에 있는 전체 사진 수가 됩니다.",
            "symbolic": "527 + 315 = □",
            "uses": [
                "quantity.family_photos",
                "quantity.friend_photos",
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
                    "사진첩에 있는 전체 사진 수",
                ],
                "answer_index": 2,
            },
            {
                "id": "understand.operation",
                "type": "multiple_choice",
                "prompt": "사진이 모두 몇 장인지 구하려면 어떻게 해야 하나요?",
                "choices": [
                    "527과 315를 더합니다.",
                    "527에서 315를 뺍니다.",
                    "527과 315를 비교합니다.",
                ],
                "answer_index": 0,
            },
        ],
        "student_restatement": {
            "prompt": "문제의 요지를 말해 볼까요?",
            "template": "{family_count}장과 {friend_count}장을 더해 {target_label}를 구합니다.",
            "answer": "가족 사진 527장과 친구 사진 315장을 더해 전체 사진 수를 구합니다.",
        },
    },
    "method": "가족 사진 수와 친구 사진 수를 덧셈으로 합합니다.",
    "plan": [
        "가족 사진 수 527장을 확인합니다.",
        "친구 사진 수 315장을 확인합니다.",
        "두 수를 더하여 전체 사진 수를 구합니다.",
    ],
    "steps": [
        {
            "id": "step.add_photo_counts",
            "goal": "사진첩에 있는 전체 사진 수를 구합니다.",
            "uses": [
                "quantity.family_photos",
                "quantity.friend_photos",
            ],
            "relation_expr": "전체 사진 수 = 가족 사진 수 + 친구 사진 수",
            "expr": "527 + 315",
            "value": 842,
            "explanation": "사진이 모두 몇 장인지 구해야 하므로 가족 사진 527장과 친구 사진 315장을 더합니다.",
        },
    ],
    "checks": [
        {
            "id": "check.inverse_subtraction_family",
            "expr": "842 - 315",
            "expected": 527,
            "actual": 527,
            "pass": True,
        },
        {
            "id": "check.inverse_subtraction_friend",
            "expr": "842 - 527",
            "expected": 315,
            "actual": 315,
            "pass": True,
        },
        {
            "id": "check.total_is_larger",
            "expr": "842 > 527 and 842 > 315",
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
            width=960,
            height=180,
            coordinate_mode="logical",
        ),
        regions=(
            Region(
                id="region.stem",
                role="stem",
                flow="vertical",
                slot_ids=(
                    "slot.question",
                    "slot.expression_blank",
                    "slot.answer_blank",
                ),
            ),
        ),
        slots=(
            TextBoxSlot(
                id="slot.question",
                x=24,
                y=20,
                width=912,
                height=48,
                text=(
                    "동윤이의 사진첩에는 527장의 가족 사진과 315장의 친구 사진이 있습니다. "
                    "사진은 모두 몇 장입니까?"
                ),
                font_size=22,
                font_family="Noto Sans KR",
                fill="#202124",
                line_height=1.4,
                align="left",
                valign="top",
            ),
            BlankSlot(
                id="slot.expression_blank",
                prompt="식",
                answer_key="527 + 315 = 842",
                placeholder="",
            ),
            BlankSlot(
                id="slot.answer_blank",
                prompt="답",
                answer_key="842",
                placeholder="장",
            ),
        ),
    )


PROBLEM_TEMPLATE = build_problem_template()
