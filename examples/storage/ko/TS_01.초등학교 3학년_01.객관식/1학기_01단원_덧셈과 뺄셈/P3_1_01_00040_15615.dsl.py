from __future__ import annotations

from modu_math.dsl import (
    BlankSlot,
    Canvas,
    ProblemTemplate,
    Region,
    TextBoxSlot,
RectSlot)


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
    "schema": "modu.solvable.v1.3",
    "problem_id": PROBLEM_ID,
    "problem_type": "numeric_answer_addition_word_problem",
    "given": [
        {"id": "first_book_pages", "ref": "quantity.first_book_pages", "value": 230},
        {"id": "second_book_pages", "ref": "quantity.second_book_pages", "value": 450},
    ],
    "target": {"id": "total_pages", "ref": "quantity.total_pages"},
    "method": "add_parts",
    "steps": [
        {"expr": "230 + 450", "value": 680},
    ],
    "checks": [
        "680 - 230 = 450",
        "680 - 450 = 230",
    ],
    "answer": ANSWER,
    "diagnostics": {
        "skills": ["add.part_part_whole", "add.basic"],
        "errors": {
            "220": "execute.add_fact",
            "450": "plan.copy_one_part",
        },
    },
}

SEMANTIC_ANSWER = SOLVABLE["answer"]


def build_problem_template() -> ProblemTemplate:
    return ProblemTemplate(
        id=PROBLEM_ID,
        title=PROBLEM_TITLE,
        canvas=Canvas(
            width = 600, height = 170, coordinate_mode="logical",
        ),
        regions=(
            Region(
                id="region.stem",
                role="stem",
                flow="vertical",
                slot_ids=("slot.question",'konva_1786410614957_rect_47608'),
            ),
        ),
        slots=(TextBoxSlot(
                id="slot.question",
                x = 6.66, y = 5.654, width = 561.344, height = 143.689, text=(
                    "동화책이 두 권 있습니다. 한 권은 230쪽이고 다른 한 권은 450쪽입니다. "
                    "두 동화책의 쪽수를 더하면 모두 몇 쪽입니까?"
                ),
                font_size = 30, font_family='"Poor Story", "Noto Sans KR", sans-serif',
                fill="#202124",
                line_height=1.45,
                align="left",
                valign="top",
            ),
            RectSlot(id = 'konva_1786410614957_rect_47608', prompt = '', x = 421.524, y = 109.303, width = 146.413, height = 46.857, fill = '#ffffff', stroke = '#111827', stroke_width = 1.2, interaction = {'type': 'input', 'role': 'answer', 'value_type': 'digit', 'max_length': 1, 'include_in_submission': True, 'order': 0, 'group_id': 'final_answer', 'auto_advance': True, 'keyboard': 'number'}, input_style = {'font_size_mode': 'auto', 'font_size_adjust': 0, 'min_font_size': 14, 'max_font_size': 52, 'font_weight': 700, 'horizontal_align': 'center', 'vertical_align': 'middle', 'padding': 6, 'text_color': '#222222'})),
    )


PROBLEM_TEMPLATE = build_problem_template()
