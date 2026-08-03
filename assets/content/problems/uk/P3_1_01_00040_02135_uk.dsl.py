from __future__ import annotations

from modu_math.dsl import Canvas, ProblemTemplate, RectSlot, Region, TextBoxSlot


PROBLEM_ID = "P3_1_01_00040_02135"
PROBLEM_TITLE = "Додавання трицифрових чисел з переходом через розряд"


def build_problem_template() -> ProblemTemplate:
    return ProblemTemplate(
        id=PROBLEM_ID,
        title=PROBLEM_TITLE,
        canvas=Canvas(width=900, height=320, coordinate_mode="logical"),
        regions=(
            Region(
                id="region.stem",
                role="stem",
                flow="absolute",
                slot_ids=(
                    "slot.instruction",
                    "slot.first_number",
                    "slot.plus_sign",
                    "slot.second_number",
                    "slot.horizontal_line",
                    "konva_1785065387111_rect_91826",
                    "konva_1785065387111_paste_117760_0",
                    "konva_1785065387111_paste_146425_0",
                    "konva_1785065387111_paste_146425_1",
                    "konva_1785065387111_paste_166216_0",
                ),
            ),
        ),
        slots=(
            TextBoxSlot(
                id="slot.instruction",
                x=10.8,
                y=22.4,
                width=520,
                height=42,
                text="Впиши у порожні місця правильні цифри.",
                font_size=24,
                font_family="Noto Sans",
                fill="#202124",
                align="left",
                valign="middle",
            ),
            TextBoxSlot(
                id="slot.first_number",
                x=130,
                y=112.4,
                width=64.4,
                height=42,
                text="6 6 4",
                font_size=28,
                font_family="Noto Sans",
                fill="#202124",
                align="left",
                valign="middle",
            ),
            TextBoxSlot(
                id="slot.plus_sign",
                x=90.4,
                y=143.2,
                width=32,
                height=42,
                text="+",
                font_size=28,
                font_family="Noto Sans",
                fill="#202124",
                align="center",
                valign="middle",
            ),
            TextBoxSlot(
                id="slot.second_number",
                x=130.4,
                y=143.2,
                width=61.2,
                height=42,
                text="2 5 7",
                font_size=28,
                font_family="Noto Sans",
                fill="#202124",
                align="left",
                valign="middle",
            ),
            TextBoxSlot(
                id="slot.horizontal_line",
                x=84.8,
                y=168.4,
                width=121.2,
                height=19.2,
                text="────────",
                font_size=24,
                font_family="Noto Sans",
                fill="#111111",
                align="left",
                valign="middle",
            ),
            RectSlot(
                id="konva_1785065387111_rect_91826",
                prompt="",
                x=146.4,
                y=88.6,
                width=19.147,
                height=19.699,
                fill="#ffffff",
                stroke="#111827",
                stroke_width=1.2,
            ),
            RectSlot(
                id="konva_1785065387111_paste_117760_0",
                prompt="",
                x=123.2,
                y=88.8,
                width=19.147,
                height=19.699,
                fill="#ffffff",
                stroke="#111827",
                stroke_width=1.2,
            ),
            RectSlot(
                id="konva_1785065387111_paste_146425_0",
                prompt="",
                x=148.8,
                y=188.6,
                width=19.147,
                height=19.699,
                fill="#ffffff",
                stroke="#111827",
                stroke_width=1.2,
            ),
            RectSlot(
                id="konva_1785065387111_paste_146425_1",
                prompt="",
                x=125.6,
                y=188.8,
                width=19.147,
                height=19.699,
                fill="#ffffff",
                stroke="#111827",
                stroke_width=1.2,
            ),
            RectSlot(
                id="konva_1785065387111_paste_166216_0",
                prompt="",
                x=171.2,
                y=188.6,
                width=19.147,
                height=19.699,
                fill="#ffffff",
                stroke="#111827",
                stroke_width=1.2,
            ),
        ),
    )


PROBLEM_TEMPLATE = build_problem_template()


SEMANTIC = {
    "problem_id": PROBLEM_ID,
    "problem_type": "multi_blank_vertical_addition",
    "metadata": {
        "grade": 3,
        "semester": 1,
        "subject": "математика",
        "topic": "додавання трицифрових чисел з переходом через розряд",
        "language": "uk-UA",
        "title": PROBLEM_TITLE,
        "question": "Впиши у порожні місця правильні цифри.",
    },
    "domain": {
        "objects": [
            {"id": "number.addend_1", "type": "number", "label": "перший доданок", "value": 664},
            {"id": "number.addend_2", "type": "number", "label": "другий доданок", "value": 257},
            {
                "id": "carry.ones_to_tens",
                "type": "carry",
                "label": "перенесення з одиниць у десятки",
                "value": 1,
            },
            {
                "id": "carry.tens_to_hundreds",
                "type": "carry",
                "label": "перенесення з десятків у сотні",
                "value": 1,
            },
            {
                "id": "digit.answer_hundreds",
                "type": "place_value_digit",
                "label": "цифра сотень у сумі",
                "place": "hundreds",
                "value": 9,
            },
            {
                "id": "digit.answer_tens",
                "type": "place_value_digit",
                "label": "цифра десятків у сумі",
                "place": "tens",
                "value": 2,
            },
            {
                "id": "digit.answer_ones",
                "type": "place_value_digit",
                "label": "цифра одиниць у сумі",
                "place": "ones",
                "value": 1,
            },
            {"id": "number.sum", "type": "number", "label": "сума 664 і 257", "value": 921},
        ],
        "relations": [
            {
                "id": "relation.sum_of_addends",
                "type": "sum_of",
                "subject": "number.sum",
                "objects": ["number.addend_1", "number.addend_2"],
            },
            {
                "id": "relation.ones_carry",
                "type": "carry_to",
                "subject": "carry.ones_to_tens",
                "from_place": "ones",
                "to_place": "tens",
            },
            {
                "id": "relation.tens_carry",
                "type": "carry_to",
                "subject": "carry.tens_to_hundreds",
                "from_place": "tens",
                "to_place": "hundreds",
            },
        ],
    },
    "answer": {
        "value": [1, 1, 9, 2, 1],
        "unit": "",
        "expression": "664 + 257 = 921",
        "items": [
            {"id": "answer.carry_hundreds", "value": 1},
            {"id": "answer.carry_tens", "value": 1},
            {"id": "answer.hundreds", "value": 9},
            {"id": "answer.tens", "value": 2},
            {"id": "answer.ones", "value": 1},
        ],
    },
}

SEMANTIC_OVERRIDE = SEMANTIC


SOLVABLE = {
    "schema": "modu.solvable.v1.2",
    "problem_id": PROBLEM_ID,
    "problem_type": "multi_blank_vertical_addition",
    "inputs": {
        "target_label": "цифри перенесення і цифри результату",
        "unit": "",
        "answer_type": "digit_list",
        "quantities": {"first_addend": 664, "second_addend": 257},
        "place_values": {
            "first_addend": {"hundreds": 6, "tens": 6, "ones": 4},
            "second_addend": {"hundreds": 2, "tens": 5, "ones": 7},
        },
        "conditions": [
            "Починай додавання з розряду одиниць.",
            "Якщо сума в розряді 10 або більше, перенеси 1 у наступний розряд.",
            "Запиши цифри перенесення і цифри результату у порожні місця.",
        ],
    },
    "given": [
        {"ref": "number.addend_1", "value": 664},
        {"ref": "number.addend_2", "value": 257},
    ],
    "target": {"ref": "answer.vertical_addition_blanks", "type": "digit_list"},
    "method": "додавати справа наліво і враховувати перенесення",
    "plan": [
        "Додати цифри одиниць: 4 і 7.",
        "Записати 1 в одиницях і перенести 1 у десятки.",
        "Додати цифри десятків: 6, 5 і перенесену 1.",
        "Записати 2 в десятках і перенести 1 у сотні.",
        "Додати цифри сотень: 6, 2 і перенесену 1.",
        "Записати результат 921.",
    ],
    "steps": [
        {
            "id": "step.add_ones",
            "expr": "4 + 7",
            "value": 11,
            "explanation": "У розряді одиниць: 4 + 7 = 11.",
        },
        {
            "id": "step.write_ones_and_carry",
            "expr": "11 = 1 * 10 + 1",
            "value": {"carry": 1, "digit": 1},
            "explanation": "Пишемо 1 в одиницях і переносимо 1 у десятки.",
        },
        {
            "id": "step.add_tens",
            "expr": "6 + 5 + 1",
            "value": 12,
            "explanation": "У розряді десятків: 6 + 5 + 1 = 12.",
        },
        {
            "id": "step.write_tens_and_carry",
            "expr": "12 = 1 * 10 + 2",
            "value": {"carry": 1, "digit": 2},
            "explanation": "Пишемо 2 в десятках і переносимо 1 у сотні.",
        },
        {
            "id": "step.add_hundreds",
            "expr": "6 + 2 + 1",
            "value": 9,
            "explanation": "У розряді сотень: 6 + 2 + 1 = 9.",
        },
        {
            "id": "step.compose_answer",
            "expr": "900 + 20 + 1",
            "value": 921,
            "explanation": "Разом отримуємо число 921.",
        },
    ],
    "answer": SEMANTIC["answer"],
    "understanding": {
        "summary": "Потрібно виконати письмове додавання 664 + 257 з перенесенням.",
        "facts": [
            {"ref": "number.addend_1", "label": "перший доданок", "value": 664, "unit": "", "source": "explicit"},
            {"ref": "number.addend_2", "label": "другий доданок", "value": 257, "unit": "", "source": "explicit"},
        ],
        "unknowns": [
            {
                "ref": "answer.vertical_addition_blanks",
                "label": "цифри у порожніх місцях",
                "unit": "",
                "source": "unknown",
            }
        ],
    },
}

SEMANTIC_ANSWER = SOLVABLE["answer"]
