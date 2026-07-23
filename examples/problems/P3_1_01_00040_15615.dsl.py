from __future__ import annotations

from modu_math.dsl import (
    BlankSlot,
    Canvas,
    ProblemTemplate,
    Region,
    TextBoxSlot,
)


PROBLEM_ID = "P3_1_01_00040_15615"
PROBLEM_TITLE = "두 동화책의 전체 쪽수"


ANSWER = {
    "type": "numeric",
    "value": 680,
    "unit": "쪽",
    "target_ref": "quantity.total_pages",
    "derived_from": "step.add_page_counts",
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
                "id": "object.storybook_first",
                "type": "book",
                "label": "한 권의 동화책",
            },
            {
                "id": "object.storybook_second",
                "type": "book",
                "label": "다른 한 권의 동화책",
            },
            {
                "id": "quantity.first_book_pages",
                "type": "quantity",
                "label": "한 권의 동화책 쪽수",
                "value": 230,
                "unit": "쪽",
            },
            {
                "id": "quantity.second_book_pages",
                "type": "quantity",
                "label": "다른 한 권의 동화책 쪽수",
                "value": 450,
                "unit": "쪽",
            },
            {
                "id": "quantity.total_pages",
                "type": "quantity",
                "label": "두 동화책의 전체 쪽수",
                "value": 680,
                "unit": "쪽",
            },
        ],
        "relations": [
            {
                "id": "relation.first_book_has_pages",
                "type": "has_quantity",
                "from_id": "object.storybook_first",
                "to_id": "quantity.first_book_pages",
            },
            {
                "id": "relation.second_book_has_pages",
                "type": "has_quantity",
                "from_id": "object.storybook_second",
                "to_id": "quantity.second_book_pages",
            },
            {
                "id": "relation.first_pages_part_of_total",
                "type": "part_of_sum",
                "from_id": "quantity.first_book_pages",
                "to_id": "quantity.total_pages",
            },
            {
                "id": "relation.second_pages_part_of_total",
                "type": "part_of_sum",
                "from_id": "quantity.second_book_pages",
                "to_id": "quantity.total_pages",
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
        "target_label": "두 동화책의 전체 쪽수",
        "unit": "쪽",
        "quantities": {
            "first_book_pages": 230,
            "second_book_pages": 450,
        },
        "conditions": [
            "동화책이 두 권 있습니다.",
            "한 권은 230쪽이고 다른 한 권은 450쪽입니다.",
            "두 동화책의 쪽수를 더한 전체 쪽수를 구합니다.",
        ],
    },
    "given": [
        {
            "ref": "quantity.first_book_pages",
            "value": {
                "count": 230,
                "unit": "쪽",
                "object": "object.storybook_first",
            },
        },
        {
            "ref": "quantity.second_book_pages",
            "value": {
                "count": 450,
                "unit": "쪽",
                "object": "object.storybook_second",
            },
        },
    ],
    "target": {
        "ref": "quantity.total_pages",
        "type": "number",
    },
    "understanding": {
        "summary": "두 동화책의 쪽수를 합하여 전체 쪽수를 구하는 문제입니다.",
        "facts": [
            {
                "ref": "quantity.first_book_pages",
                "label": "한 권의 동화책 쪽수",
                "value": 230,
                "unit": "쪽",
                "source": "explicit",
            },
            {
                "ref": "quantity.second_book_pages",
                "label": "다른 한 권의 동화책 쪽수",
                "value": 450,
                "unit": "쪽",
                "source": "explicit",
            },
        ],
        "unknowns": [
            {
                "ref": "quantity.total_pages",
                "label": "두 동화책의 전체 쪽수",
                "unit": "쪽",
                "source": "unknown",
            },
        ],
        "relation": {
            "type": "part_part_whole_addition",
            "statement": "두 동화책의 전체 쪽수는 각 동화책의 쪽수를 더한 수입니다.",
            "symbolic": "전체 쪽수 = 첫 번째 책의 쪽수 + 두 번째 책의 쪽수",
            "uses": [
                "quantity.first_book_pages",
                "quantity.second_book_pages",
            ],
            "result": "quantity.total_pages",
        },
        "diagnostic_questions": [
            {
                "id": "understand.target",
                "type": "multiple_choice",
                "prompt": "이 문제에서 구해야 하는 것은 무엇인가요?",
                "choices": [
                    "한 권의 동화책 쪽수",
                    "다른 한 권의 동화책 쪽수",
                    "두 동화책의 전체 쪽수",
                ],
                "answer_index": 2,
            },
            {
                "id": "understand.relation",
                "type": "multiple_choice",
                "prompt": "두 동화책의 전체 쪽수를 구하려면 어떻게 해야 하나요?",
                "choices": [
                    "230과 450을 더합니다.",
                    "450에서 230을 뺍니다.",
                    "230과 450을 비교합니다.",
                ],
                "answer_index": 0,
            },
        ],
        "student_restatement": {
            "prompt": "문제의 요지를 말해 볼까요?",
            "template": "{first_book_pages}쪽과 {second_book_pages}쪽을 더해 {target_label}를 구합니다.",
            "answer": "230쪽과 450쪽을 더해 두 동화책의 전체 쪽수를 구합니다.",
        },
    },
    "method": "두 동화책의 쪽수를 덧셈으로 합하여 전체 쪽수를 구합니다.",
    "plan": [
        "한 권의 동화책 쪽수 230쪽을 확인합니다.",
        "다른 한 권의 동화책 쪽수 450쪽을 확인합니다.",
        "두 쪽수를 더하여 전체 쪽수를 구합니다.",
    ],
    "steps": [
        {
            "id": "step.add_page_counts",
            "goal": "두 동화책의 전체 쪽수를 구합니다.",
            "uses": [
                "quantity.first_book_pages",
                "quantity.second_book_pages",
            ],
            "relation_expr": "전체 쪽수 = 첫 번째 책의 쪽수 + 두 번째 책의 쪽수",
            "expr": "230 + 450",
            "value": {
                "count": 680,
                "unit": "쪽",
                "ref": "quantity.total_pages",
            },
            "explanation": "두 동화책의 쪽수를 모두 구해야 하므로 230과 450을 더합니다.",
        },
    ],
    "checks": [
        {
            "id": "check.subtract_first_book_pages",
            "expr": "680 - 230",
            "expected": 450,
            "actual": 450,
            "pass": True,
        },
        {
            "id": "check.subtract_second_book_pages",
            "expr": "680 - 450",
            "expected": 230,
            "actual": 230,
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
            height=170,
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
                width=852,
                height=54,
                text=(
                    "동화책이 두 권 있습니다. 한 권은 230쪽이고 다른 한 권은 450쪽입니다. "
                    "두 동화책의 쪽수를 더하면 모두 몇 쪽입니까?"
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
                answer_key="680",
                placeholder="쪽",
            ),
        ),
    )


PROBLEM_TEMPLATE = build_problem_template()
