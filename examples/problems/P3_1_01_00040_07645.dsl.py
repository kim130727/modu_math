from __future__ import annotations

from modu_math.dsl import (
    BlankSlot,
    Canvas,
    ProblemTemplate,
    Region,
    TextBoxSlot,
)


PROBLEM_ID = "P3_1_01_00040_07645"
PROBLEM_TITLE = "미정이가 읽는 동화책의 전체 쪽수"


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
                    "미정이는 어제 동화책을 처음부터 119쪽까지 읽었더니 "
                    "167쪽이 남았습니다. 미정이가 읽는 동화책의 전체 쪽수를 구하시오."
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
                answer_key="286",
                placeholder="쪽",
            ),
        ),
    )


PROBLEM_TEMPLATE = build_problem_template()


SEMANTIC = {
    "problem_id": PROBLEM_ID,
    "problem_type": "numeric_answer_part_whole_addition_word_problem",
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
                "id": "object.storybook",
                "type": "book",
                "label": "동화책",
            },
            {
                "id": "quantity.pages_read",
                "type": "quantity",
                "label": "처음부터 읽은 쪽수",
                "value": 119,
                "unit": "쪽",
            },
            {
                "id": "quantity.pages_remaining",
                "type": "quantity",
                "label": "남은 쪽수",
                "value": 167,
                "unit": "쪽",
            },
            {
                "id": "quantity.total_pages",
                "type": "quantity",
                "label": "동화책의 전체 쪽수",
                "value": 286,
                "unit": "쪽",
            },
        ],
        "relations": [
            {
                "id": "relation.mijeong_read_storybook",
                "type": "read",
                "subject": "person.mijeong",
                "object": "object.storybook",
                "quantity": "quantity.pages_read",
                "time": "yesterday",
                "range": {
                    "start_page": 1,
                    "end_page": 119,
                },
            },
            {
                "id": "relation.storybook_has_remaining_pages",
                "type": "has_remaining_quantity",
                "subject": "object.storybook",
                "quantity": "quantity.pages_remaining",
            },
            {
                "id": "relation.total_pages_is_sum",
                "type": "sum_of",
                "subject": "quantity.total_pages",
                "objects": [
                    "quantity.pages_read",
                    "quantity.pages_remaining",
                ],
            },
        ],
    },
    "answer": {
        "type": "numeric",
        "value": 286,
        "unit": "쪽",
        "target_ref": "quantity.total_pages",
    },
}

SEMANTIC_OVERRIDE = SEMANTIC


SOLVABLE = {
    "schema": "modu.solvable.v1.2",
    "problem_id": PROBLEM_ID,
    "problem_type": "numeric_answer_part_whole_addition_word_problem",
    "inputs": {
        "target_label": "미정이가 읽는 동화책의 전체 쪽수",
        "unit": "쪽",
        "quantities": {
            "pages_read": 119,
            "pages_remaining": 167,
        },
        "conditions": [
            "미정이는 동화책을 처음부터 119쪽까지 읽었습니다.",
            "읽고 나서 167쪽이 남았습니다.",
            "읽은 쪽수와 남은 쪽수를 합하여 전체 쪽수를 구합니다.",
        ],
    },
    "given": [
        {
            "ref": "quantity.pages_read",
            "value": {
                "count": 119,
                "unit": "쪽",
                "person": "person.mijeong",
                "object": "object.storybook",
                "range": {
                    "start_page": 1,
                    "end_page": 119,
                },
                "time": "yesterday",
            },
        },
        {
            "ref": "quantity.pages_remaining",
            "value": {
                "count": 167,
                "unit": "쪽",
                "object": "object.storybook",
            },
        },
    ],
    "target": {
        "ref": "quantity.total_pages",
        "type": "number",
    },
    "method": "처음부터 읽은 쪽수와 읽고 남은 쪽수를 더합니다.",
    "plan": [
        "미정이가 처음부터 119쪽까지 읽었음을 확인합니다.",
        "읽고 나서 167쪽이 남았음을 확인합니다.",
        "읽은 쪽수와 남은 쪽수를 더하여 동화책의 전체 쪽수를 구합니다.",
    ],
    "steps": [
        {
            "id": "step.add_read_and_remaining_pages",
            "goal": "동화책의 전체 쪽수를 구합니다.",
            "uses": [
                "quantity.pages_read",
                "quantity.pages_remaining",
            ],
            "relation_expr": "전체 쪽수 = 읽은 쪽수 + 남은 쪽수",
            "expr": "119 + 167",
            "value": 286,
            "explanation": (
                "동화책 전체는 미정이가 읽은 119쪽과 아직 읽지 않은 "
                "167쪽으로 이루어져 있으므로 두 수를 더합니다."
            ),
        },
    ],
    "checks": [
        {
            "id": "check.subtract_read_pages",
            "description": "전체 쪽수에서 읽은 쪽수를 빼면 남은 쪽수가 됩니다.",
            "expr": "286 - 119",
            "expected": 167,
            "actual": 167,
            "pass": True,
        },
        {
            "id": "check.subtract_remaining_pages",
            "description": "전체 쪽수에서 남은 쪽수를 빼면 읽은 쪽수가 됩니다.",
            "expr": "286 - 167",
            "expected": 119,
            "actual": 119,
            "pass": True,
        },
    ],
    "answer": {
        "type": "numeric",
        "value": 286,
        "unit": "쪽",
        "target_ref": "quantity.total_pages",
    },
    "understanding": {
        "summary": (
            "미정이가 처음부터 읽은 119쪽과 아직 남아 있는 167쪽을 "
            "합하여 동화책의 전체 쪽수를 구하는 문제입니다."
        ),
        "facts": [
            {
                "ref": "quantity.pages_read",
                "label": "미정이가 처음부터 읽은 쪽수",
                "value": 119,
                "unit": "쪽",
                "source": "explicit",
            },
            {
                "ref": "quantity.pages_remaining",
                "label": "읽고 남은 쪽수",
                "value": 167,
                "unit": "쪽",
                "source": "explicit",
            },
        ],
        "unknowns": [
            {
                "ref": "quantity.total_pages",
                "label": "동화책의 전체 쪽수",
                "unit": "쪽",
                "source": "unknown",
            },
        ],
        "relation": {
            "type": "part_part_whole_addition",
            "statement": "읽은 쪽수와 남은 쪽수를 합하면 동화책의 전체 쪽수가 됩니다.",
            "symbolic": "119 + 167 = 286",
            "uses": [
                "quantity.pages_read",
                "quantity.pages_remaining",
            ],
            "result": "quantity.total_pages",
        },
        "diagnostic_questions": [
            {
                "id": "understand.target",
                "type": "multiple_choice",
                "prompt": "이 문제에서 구해야 하는 것은 무엇인가요?",
                "choices": [
                    "미정이가 읽은 쪽수",
                    "읽고 남은 쪽수",
                    "동화책의 전체 쪽수",
                ],
                "answer_index": 2,
            },
            {
                "id": "understand.parts",
                "type": "multiple_choice",
                "prompt": "동화책의 전체 쪽수를 이루는 두 부분은 무엇인가요?",
                "choices": [
                    "읽은 쪽수와 남은 쪽수",
                    "읽은 쪽수와 전체 쪽수",
                    "남은 쪽수와 전체 쪽수",
                ],
                "answer_index": 0,
            },
            {
                "id": "understand.operation",
                "type": "multiple_choice",
                "prompt": "동화책의 전체 쪽수를 구하려면 어떻게 계산해야 하나요?",
                "choices": [
                    "119와 167을 더합니다.",
                    "167에서 119를 뺍니다.",
                    "119에서 167을 뺍니다.",
                ],
                "answer_index": 0,
            },
        ],
        "student_restatement": {
            "prompt": "문제의 뜻을 말해 볼까요?",
            "template": (
                "미정이가 처음부터 {read}쪽까지 읽었고 {remaining}쪽이 남았으므로, "
                "읽은 쪽수와 남은 쪽수를 더하여 동화책의 {target}를 구합니다."
            ),
            "answer": (
                "미정이가 처음부터 119쪽까지 읽었고 167쪽이 남았으므로, "
                "읽은 쪽수와 남은 쪽수를 더하여 동화책의 전체 쪽수를 구합니다."
            ),
        },
    },
}


SEMANTIC_ANSWER = SOLVABLE["answer"]
