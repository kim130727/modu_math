from __future__ import annotations

from modu_math.dsl import BlankSlot, Canvas, ProblemTemplate, RectSlot, Region, TextBoxSlot


PROBLEM_ID = "P3_1_01_00040_00469"
PROBLEM_TITLE = "Скільки бататів зібрали дві родини?"


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
        "question": (
            "Подивіться на малюнок. Родини Санхьона і Йонджіна на вихідних "
            "пішли на поле. Родина Санхьона зібрала 259 бататів, а родина "
            "Йонджіна зібрала 248 бататів. Скільки бататів зібрали обидві "
            "родини разом?"
        ),
    },
    "domain": {
        "objects": [
            {"id": "person.sanghyeon", "type": "person", "label": "Санхьон"},
            {"id": "person.yongjin", "type": "person", "label": "Йонджін"},
            {
                "id": "group.sanghyeon_family",
                "type": "family",
                "label": "родина Санхьона",
            },
            {
                "id": "group.yongjin_family",
                "type": "family",
                "label": "родина Йонджіна",
            },
            {
                "id": "object.sweet_potato",
                "type": "countable_object",
                "label": "батат",
                "unit": "шт.",
            },
            {
                "id": "quantity.sanghyeon_family_sweet_potatoes",
                "type": "quantity",
                "label": "батати, які зібрала родина Санхьона",
                "value": 259,
                "unit": "шт.",
            },
            {
                "id": "quantity.yongjin_family_sweet_potatoes",
                "type": "quantity",
                "label": "батати, які зібрала родина Йонджіна",
                "value": 248,
                "unit": "шт.",
            },
            {
                "id": "quantity.total_sweet_potatoes",
                "type": "quantity",
                "label": "батати, які зібрали обидві родини",
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
        "target_label": "кількість бататів, які зібрали обидві родини",
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
    "target": {"ref": "quantity.total_sweet_potatoes", "type": "number"},
    "method": "додати кількості бататів, які зібрали дві родини",
    "plan": [
        "Перевірити, скільки бататів зібрала родина Санхьона.",
        "Перевірити, скільки бататів зібрала родина Йонджіна.",
        "Додати ці дві кількості, щоб знайти загальну кількість.",
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
            "value": {
                "count": 507,
                "unit": "шт.",
                "ref": "quantity.total_sweet_potatoes",
            },
            "explanation": "Щоб знайти загальну кількість, додаємо 259 і 248.",
        },
    ],
    "answer": {"value": 507, "unit": "шт."},
    "understanding": {
        "summary": (
            "Це задача на додавання частин: потрібно додати кількість бататів "
            "двох родин."
        ),
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
    },
}

SEMANTIC_ANSWER = SOLVABLE["answer"]


def build_problem_template() -> ProblemTemplate:
    return ProblemTemplate(
        id=PROBLEM_ID,
        title=PROBLEM_TITLE,
        canvas=Canvas(width=900, height=230, coordinate_mode="logical"),
        regions=(
            Region(
                id="region.stem",
                role="stem",
                flow="vertical",
                slot_ids=(
                    "slot.question",
                    "slot.expression",
                    "slot.answer",
                    "konva_1785063642549_rect_11081",
                    "konva_1785063642549_text_21880",
                ),
            ),
        ),
        slots=(
            TextBoxSlot(
                id="slot.question",
                x=48,
                y=34,
                width=804,
                height=72,
                text=SEMANTIC["metadata"]["question"],
                font_size=24,
                font_family="Noto Sans",
                fill="#202124",
                line_height=1.55,
                align="left",
                valign="top",
            ),
            TextBoxSlot(
                id="slot.expression",
                x=48,
                y=125,
                width=804,
                height=34,
                text="",
                font_size=24,
                font_family="Noto Sans",
                fill="#202124",
                align="left",
                valign="middle",
            ),
            BlankSlot(
                id="slot.answer",
                prompt="",
                answer_key="507",
                placeholder="шт.",
            ),
            RectSlot(
                id="konva_1785063642549_rect_11081",
                prompt="",
                x=588.852,
                y=151.967,
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
                x=684.59,
                y=151.393,
                font_size=30,
                fill="#111827",
                width=98,
                height=46,
                align="left",
                line_height=1.25,
            ),
        ),
    )


PROBLEM_TEMPLATE = build_problem_template()
