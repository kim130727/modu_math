from __future__ import annotations

from modu_math.dsl import Canvas, ProblemTemplate, RectSlot, Region, TextBoxSlot


PROBLEM_ID = "P3_1_01_00040_00469"
PROBLEM_TITLE = "Скільки бататів зібрали дві родини?"
PROBLEM_QUESTION = (
    "Подивіться на малюнок. Родини Санхьона і Йонджіна на вихідних пішли на поле. "
    "Родина Санхьона зібрала 259 бататів, а родина Йонджіна зібрала 248 бататів. "
    "Скільки бататів зібрали обидві родини разом?"
)


SEMANTIC = {
    "problem_id": PROBLEM_ID,
    "problem_type": "numeric_answer_addition_word_problem",
    "metadata": {
        "grade": 3,
        "semester": 1,
        "subject": "математика",
        "topic": "додавання трицифрових чисел",
        "language": "uk-UA",
        "title": PROBLEM_TITLE,
        "question": PROBLEM_QUESTION,
    },
    "domain": {
        "objects": [
            {"id": "person.sanghyeon", "type": "person", "label": "Санхьон"},
            {"id": "person.yongjin", "type": "person", "label": "Йонджін"},
            {"id": "group.sanghyeon_family", "type": "family", "label": "родина Санхьона"},
            {"id": "group.yongjin_family", "type": "family", "label": "родина Йонджіна"},
            {"id": "object.sweet_potato", "type": "countable_object", "label": "батат", "unit": "шт."},
            {
                "id": "quantity.sanghyeon_family_sweet_potatoes",
                "type": "quantity",
                "label": "батати родини Санхьона",
                "value": 259,
                "unit": "шт.",
            },
            {
                "id": "quantity.yongjin_family_sweet_potatoes",
                "type": "quantity",
                "label": "батати родини Йонджіна",
                "value": 248,
                "unit": "шт.",
            },
            {
                "id": "quantity.total_sweet_potatoes",
                "type": "quantity",
                "label": "батати обох родин разом",
                "value": 507,
                "unit": "шт.",
            },
        ],
        "relations": [
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
                "id": "relation.parts_make_total",
                "type": "part_of_sum",
                "from_id": "quantity.sanghyeon_family_sweet_potatoes",
                "to_id": "quantity.total_sweet_potatoes",
            },
            {
                "id": "relation.parts_make_total_2",
                "type": "part_of_sum",
                "from_id": "quantity.yongjin_family_sweet_potatoes",
                "to_id": "quantity.total_sweet_potatoes",
            },
        ],
    },
    "answer": {"value": 507, "unit": "шт."},
}

SEMANTIC_OVERRIDE = SEMANTIC


SOLVABLE = {
    "schema": "modu.solvable.v1.2",
    "problem_id": PROBLEM_ID,
    "problem_type": "numeric_answer_addition_word_problem",
    "inputs": {
        "target_label": "батати обох родин разом",
        "unit": "шт.",
        "quantities": {
            "sanghyeon_family_count": 259,
            "yongjin_family_count": 248,
        },
        "conditions": [
            "Родина Санхьона зібрала 259 бататів.",
            "Родина Йонджіна зібрала 248 бататів.",
            "Потрібно знайти, скільки бататів зібрали обидві родини разом.",
        ],
    },
    "given": [
        {
            "ref": "quantity.sanghyeon_family_sweet_potatoes",
            "value": {"count": 259, "unit": "шт.", "owner": "group.sanghyeon_family"},
        },
        {
            "ref": "quantity.yongjin_family_sweet_potatoes",
            "value": {"count": 248, "unit": "шт.", "owner": "group.yongjin_family"},
        },
    ],
    "target": {"ref": "quantity.total_sweet_potatoes", "type": "number"},
    "method": "додати кількості бататів, які зібрали дві родини",
    "plan": [
        "Перевірити, скільки бататів зібрала родина Санхьона.",
        "Перевірити, скільки бататів зібрала родина Йонджіна.",
        "Додати ці дві кількості.",
    ],
    "steps": [
        {
            "id": "step.add_counts",
            "goal": "знайти загальну кількість бататів",
            "uses": [
                "quantity.sanghyeon_family_sweet_potatoes",
                "quantity.yongjin_family_sweet_potatoes",
            ],
            "relation_expr": "усього = батати Санхьона + батати Йонджіна",
            "expr": "259 + 248",
            "value": {"count": 507, "unit": "шт.", "ref": "quantity.total_sweet_potatoes"},
            "explanation": "Щоб знайти загальну кількість, додаємо 259 і 248.",
        }
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
    "answer": {"value": 507, "unit": "шт."},
    "understanding": {
        "summary": "Це задача на додавання частин: потрібно додати кількість бататів двох родин.",
        "facts": [
            {
                "ref": "quantity.sanghyeon_family_sweet_potatoes",
                "label": "батати родини Санхьона",
                "value": 259,
                "unit": "шт.",
                "source": "explicit",
            },
            {
                "ref": "quantity.yongjin_family_sweet_potatoes",
                "label": "батати родини Йонджіна",
                "value": 248,
                "unit": "шт.",
                "source": "explicit",
            },
        ],
        "unknowns": [
            {
                "ref": "quantity.total_sweet_potatoes",
                "label": "батати обох родин разом",
                "unit": "шт.",
                "source": "unknown",
            }
        ],
        "relation": {
            "type": "part_part_whole_addition",
            "statement": "Щоб знайти, скільки бататів зібрали обидві родини разом, потрібно додати кількості бататів кожної родини.",
            "symbolic": "усього = 259 + 248",
            "uses": [
                "quantity.sanghyeon_family_sweet_potatoes",
                "quantity.yongjin_family_sweet_potatoes",
            ],
            "result": "quantity.total_sweet_potatoes",
        },
    },
}

SEMANTIC_ANSWER = SOLVABLE["answer"]


def build_problem_template() -> ProblemTemplate:
    return ProblemTemplate(
        id=PROBLEM_ID,
        title=PROBLEM_TITLE,
        canvas=Canvas(width=900, height=340, coordinate_mode="logical"),
        regions=(
            Region(
                id="region.stem",
                role="stem",
                flow="vertical",
                slot_ids=(
                    "slot.question",
                    "konva_1785063642549_rect_11081",
                    "konva_1785063642549_text_21880",
                ),
            ),
        ),
        slots=(
            TextBoxSlot(
                id="slot.question",
                x=48,
                y=30,
                width=804,
                height=215,
                text=PROBLEM_QUESTION,
                font_size=24,
                font_family='"Noto Sans", sans-serif',
                fill="#202124",
                line_height=1.55,
                align="left",
                valign="top",
            ),
            RectSlot(
                id="konva_1785063642549_rect_11081",
                prompt="",
                x=654,
                y=270,
                width=78.73,
                height=41.989,
                fill="#ffffff",
                stroke="#111827",
                stroke_width=1.2,
                interaction={
                    "type": "input",
                    "role": "answer",
                    "value_type": "digit",
                    "max_length": 3,
                    "include_in_submission": True,
                    "order": 0,
                    "group_id": "final_answer",
                    "auto_advance": True,
                    "keyboard": "number",
                },
                input_style={
                    "font_size_mode": "auto",
                    "font_size_adjust": 0,
                    "min_font_size": 14,
                    "max_font_size": 52,
                    "font_weight": 700,
                    "horizontal_align": "center",
                    "vertical_align": "middle",
                    "padding": 6,
                    "text_color": "#222222",
                },
            ),
            TextBoxSlot(
                id="konva_1785063642549_text_21880",
                prompt="",
                text="шт.",
                x=760,
                y=269,
                font_size=30,
                font_family='"Noto Sans", sans-serif',
                fill="#111827",
                width=98,
                height=46,
                align="left",
                line_height=1.25,
            ),
        ),
    )


PROBLEM_TEMPLATE = build_problem_template()
