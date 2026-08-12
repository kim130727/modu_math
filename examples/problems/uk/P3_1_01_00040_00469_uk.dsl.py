from __future__ import annotations

from modu_math.dsl import (
    BlankSlot,
    Canvas,
    ProblemTemplate,
    Region,
    TextBoxSlot,
    TextSlot,
RectSlot)


PROBLEM_ID = "P3_1_01_00040_00469"
PROBLEM_TITLE = "Кількість бататів, зібраних двома родинами разом"


ANSWER = {'value': 507,
 'unit': 'шт.',
 'values': [507, 507],
 'blanks': [{'id': 'slot.answer', 'slot_id': 'slot.answer', 'expected': 507},
            {'id': 'konva_1785063642549_rect_11081',
             'slot_id': 'konva_1785063642549_rect_11081',
             'expected': 507}],
 'answer_key': [{'slot_id': 'slot.answer', 'value': 507},
                {'slot_id': 'konva_1785063642549_rect_11081', 'value': 507}]}

SEMANTIC = {
    "problem_id": PROBLEM_ID,
    "problem_type": "numeric_answer_addition_word_problem",
    "metadata": {
        "grade": 3,
        "semester": 1,
        "subject": "Математика",
        "topic": "Додавання трицифрових чисел",
        "language": "uk-UA",
    },
    "domain": {
        "objects": [
            {
                "id": "person.sanghyeon",
                "type": "person",
                "label": "Санхьон",
            },
            {
                "id": "person.yongjin",
                "type": "person",
                "label": "Йонджін",
            },
            {
                "id": "group.sanghyeon_family",
                "type": "family",
                "label": "Родина Санхьона",
            },
            {
                "id": "group.yongjin_family",
                "type": "family",
                "label": "Родина Йонджіна",
            },
            {
                "id": "object.sweet_potato",
                "type": "countable_object",
                "label": "Батат",
                "unit": "шт.",
            },
            {
                "id": "quantity.sanghyeon_family_sweet_potatoes",
                "type": "quantity",
                "label": "Кількість бататів, зібраних родиною Санхьона",
                "value": 259,
                "unit": "шт.",
            },
            {
                "id": "quantity.yongjin_family_sweet_potatoes",
                "type": "quantity",
                "label": "Кількість бататів, зібраних родиною Йонджіна",
                "value": 248,
                "unit": "шт.",
            },
            {
                "id": "quantity.total_sweet_potatoes",
                "type": "quantity",
                "label": "Кількість бататів, зібраних двома родинами",
                "value": 507,
                "unit": "шт.",
            },
        ],
        "relations": [
            {
                "id": "relation.sanghyeon_belongs_to_family",
                "type": "member_of",
                "from_id": "person.sanghyeon",
                "to_id": "group.sanghyeon_family",
            },
            {
                "id": "relation.yongjin_belongs_to_family",
                "type": "member_of",
                "from_id": "person.yongjin",
                "to_id": "group.yongjin_family",
            },
            {
                "id": "relation.sanghyeon_family_collected",
                "type": "collected",
                "from_id": "group.sanghyeon_family",
                "to_id": "object.sweet_potato",
                "quantity": "quantity.sanghyeon_family_sweet_potatoes",
            },
            {
                "id": "relation.yongjin_family_collected",
                "type": "collected",
                "from_id": "group.yongjin_family",
                "to_id": "object.sweet_potato",
                "quantity": "quantity.yongjin_family_sweet_potatoes",
            },
            {
                "id": "relation.sanghyeon_count_part_of_total",
                "type": "part_of_sum",
                "from_id": "quantity.sanghyeon_family_sweet_potatoes",
                "to_id": "quantity.total_sweet_potatoes",
            },
            {
                "id": "relation.yongjin_count_part_of_total",
                "type": "part_of_sum",
                "from_id": "quantity.yongjin_family_sweet_potatoes",
                "to_id": "quantity.total_sweet_potatoes",
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
        "target_label": "кількість бататів, зібраних двома родинами",
        "unit": "шт.",
        "quantities": {
            "sanghyeon_family_count": 259,
            "yongjin_family_count": 248,
        },
        "conditions": [
            "Родина Санхьона зібрала 259 бататів.",
            "Родина Йонджіна зібрала 248 бататів.",
            "Потрібно знайти загальну кількість бататів, зібраних двома родинами.",
        ],
    },
    "given": [
        {
            "ref": "quantity.sanghyeon_family_sweet_potatoes",
            "value": {
                "count": 259,
                "unit": "шт.",
                "owner": "group.sanghyeon_family",
                "object": "object.sweet_potato",
            },
        },
        {
            "ref": "quantity.yongjin_family_sweet_potatoes",
            "value": {
                "count": 248,
                "unit": "шт.",
                "owner": "group.yongjin_family",
                "object": "object.sweet_potato",
            },
        },
    ],
    "target": {
        "ref": "quantity.total_sweet_potatoes",
        "type": "number",
    },
    "understanding": {
        "summary": "У цій задачі потрібно додати кількість бататів, зібраних кожною родиною, і знайти їх загальну кількість.",
        "facts": [
            {
                "ref": "quantity.sanghyeon_family_sweet_potatoes",
                "label": "Кількість бататів, зібраних родиною Санхьона",
                "value": 259,
                "unit": "шт.",
                "source": "explicit",
            },
            {
                "ref": "quantity.yongjin_family_sweet_potatoes",
                "label": "Кількість бататів, зібраних родиною Йонджіна",
                "value": 248,
                "unit": "шт.",
                "source": "explicit",
            },
        ],
        "unknowns": [
            {
                "ref": "quantity.total_sweet_potatoes",
                "label": "Кількість бататів, зібраних двома родинами",
                "unit": "шт.",
                "source": "unknown",
            },
        ],
        "relation": {
            "type": "part_part_whole_addition",
            "statement": "Щоб знайти загальну кількість бататів, зібраних двома родинами, потрібно додати кількості, зібрані кожною родиною.",
            "symbolic": "Усього = кількість родини Санхьона + кількість родини Йонджіна",
            "uses": [
                "quantity.sanghyeon_family_sweet_potatoes",
                "quantity.yongjin_family_sweet_potatoes",
            ],
            "result": "quantity.total_sweet_potatoes",
        },
        "diagnostic_questions": [
            {
                "id": "understand.target",
                "type": "multiple_choice",
                "prompt": "Що потрібно знайти в цій задачі?",
                "choices": [
                    "Кількість бататів, зібраних родиною Санхьона",
                    "Кількість бататів, зібраних родиною Йонджіна",
                    "Кількість бататів, зібраних двома родинами",
                ],
                "answer_index": 2,
            },
            {
                "id": "understand.relation",
                "type": "multiple_choice",
                "prompt": "Що потрібно зробити, щоб знайти загальну кількість бататів, зібраних двома родинами?",
                "choices": [
                    "Додати 259 і 248.",
                    "Від 259 відняти 248.",
                    "Порівняти 259 і 248.",
                ],
                "answer_index": 0,
            },
        ],
        "student_restatement": {
            "prompt": "Спробуймо переказати головну думку задачі.",
            "template": "Додаємо {first_count} шт. і {second_count} шт., щоб знайти {target_label}.",
            "answer": "Додаємо 259 і 248, щоб знайти кількість бататів, зібраних двома родинами.",
        },
    },
    "method": "Знаходимо загальну кількість бататів, зібраних двома родинами, за допомогою додавання.",
    "plan": [
        "Визначити кількість бататів, зібраних родиною Санхьона.",
        "Визначити кількість бататів, зібраних родиною Йонджіна.",
        "Додати два числа та знайти загальну кількість бататів.",
    ],
    "steps": [
        {
            "id": "step.add_counts",
            "goal": "Знайти загальну кількість бататів, зібраних двома родинами.",
            "uses": [
                "quantity.sanghyeon_family_sweet_potatoes",
                "quantity.yongjin_family_sweet_potatoes",
            ],
            "relation_expr": "Усього = кількість родини Санхьона + кількість родини Йонджіна",
            "expr": "259 + 248",
            "value": {
                "count": 507,
                "unit": "шт.",
                "ref": "quantity.total_sweet_potatoes",
            },
            "explanation": "Щоб знайти загальну кількість бататів, зібраних двома родинами, додаємо 259 і 248.",
        },
    ],
    "checks": [
        {
            "id": "check.inverse_subtraction",
            "expr": "507 - 248",
            "expected": 259,
            "actual": 259,
            "pass": True,
        },
        {
            "id": "check.minimum_total",
            "expr": "507 > 259 and 507 > 248",
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
            height=230,
            coordinate_mode="logical",
        ),
        regions=(
            Region(
                id="region.stem",
                role="stem",
                flow="vertical",
                slot_ids=("slot.question",
                    "slot.answer",'konva_1785063642549_rect_11081', 'konva_1785063642549_text_21880'),
            ),
        ),
        slots=(TextBoxSlot(
                id="slot.question",
                x=20,
                y=18,
                width=860,
                height=112,
                text=(
                    "Минулої неділі родини Санхьона та Йонджіна поїхали на заміську ферму. "
                    "Родина Санхьона зібрала 259 бататів, а родина Йонджіна —\n"
                    "248 бататів. Скільки всього бататів зібрали обидві родини?"
                ),
                font_size=18,
                font_family='"Noto Sans", "Arial", sans-serif',
                fill="#202124",
                line_height=1.35,
                align="left",
                valign="top",
            ),
            BlankSlot(
                id="slot.answer",
                prompt="Відповідь",
                answer_key=None,
                placeholder="шт.",
            ),RectSlot(id = 'konva_1785063642549_rect_11081', prompt = '', x = 610, y = 160, width = 110, height = 42, fill = '#ffffff', stroke = '#111827', stroke_width = 1.2, interaction = {'type': 'input', 'role': 'answer', 'value_type': 'digit', 'max_length': 3, 'include_in_submission': True, 'order': 0, 'group_id': 'final_answer', 'auto_advance': True, 'keyboard': 'number'}, input_style = {'font_size_mode': 'auto', 'font_size_adjust': 0, 'min_font_size': 14, 'max_font_size': 52, 'font_weight': 700, 'horizontal_align': 'center', 'vertical_align': 'middle', 'padding': 6, 'text_color': '#222222'}), TextBoxSlot(id = 'konva_1785063642549_text_21880', prompt = '', text = 'шт.', x = 738, y = 163, font_size = 28, font_family = '"Noto Sans", "Arial", sans-serif', fill = '#111827', width = 52, height = 40, align = 'left', line_height = 1.25)),
    )


PROBLEM_TEMPLATE = build_problem_template()
