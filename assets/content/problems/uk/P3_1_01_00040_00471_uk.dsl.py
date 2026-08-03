from __future__ import annotations

from modu_math.dsl import Canvas, ProblemTemplate, Region, TextBoxSlot


PROBLEM_ID = "P3_1_01_00040_00471"
PROBLEM_TITLE = "Порівняння значень виразів"


def build_problem_template() -> ProblemTemplate:
    return ProblemTemplate(
        id=PROBLEM_ID,
        title=PROBLEM_TITLE,
        canvas=Canvas(width=900, height=220, coordinate_mode="logical"),
        regions=(
            Region(
                id="region.stem",
                role="stem",
                flow="absolute",
                slot_ids=(
                    "slot.instruction",
                    "slot.problem_1_number",
                    "slot.problem_1_left",
                    "slot.problem_1_blank",
                    "slot.problem_1_right",
                    "slot.problem_2_number",
                    "slot.problem_2_left",
                    "slot.problem_2_blank",
                    "slot.problem_2_right",
                ),
            ),
        ),
        slots=(
            TextBoxSlot(
                id="slot.instruction",
                x=38,
                y=22,
                width=824,
                height=38,
                text="Порівняй значення і впиши у порожні місця >, = або <.",
                font_size=24,
                font_family="Noto Sans",
                fill="#202124",
                align="left",
                valign="middle",
            ),
            TextBoxSlot(
                id="slot.problem_1_number",
                x=40,
                y=76,
                width=55,
                height=38,
                text="(1)",
                font_size=24,
                font_family="Noto Sans",
                fill="#202124",
                align="left",
                valign="middle",
            ),
            TextBoxSlot(
                id="slot.problem_1_left",
                x=105,
                y=76,
                width=90,
                height=38,
                text="532",
                font_size=24,
                font_family="Noto Sans",
                fill="#202124",
                align="center",
                valign="middle",
            ),
            TextBoxSlot(
                id="slot.problem_1_blank",
                x=202,
                y=71,
                width=52,
                height=48,
                text="□",
                font_size=40,
                font_family="Noto Sans",
                fill="#111111",
                align="center",
                valign="middle",
            ),
            TextBoxSlot(
                id="slot.problem_1_right",
                x=264,
                y=76,
                width=160,
                height=38,
                text="248+274",
                font_size=24,
                font_family="Noto Sans",
                fill="#202124",
                align="left",
                valign="middle",
            ),
            TextBoxSlot(
                id="slot.problem_2_number",
                x=40,
                y=132,
                width=55,
                height=38,
                text="(2)",
                font_size=24,
                font_family="Noto Sans",
                fill="#202124",
                align="left",
                valign="middle",
            ),
            TextBoxSlot(
                id="slot.problem_2_left",
                x=105,
                y=132,
                width=135,
                height=38,
                text="346+667",
                font_size=24,
                font_family="Noto Sans",
                fill="#202124",
                align="center",
                valign="middle",
            ),
            TextBoxSlot(
                id="slot.problem_2_blank",
                x=247,
                y=127,
                width=52,
                height=48,
                text="□",
                font_size=40,
                font_family="Noto Sans",
                fill="#111111",
                align="center",
                valign="middle",
            ),
            TextBoxSlot(
                id="slot.problem_2_right",
                x=309,
                y=132,
                width=160,
                height=38,
                text="428+585",
                font_size=24,
                font_family="Noto Sans",
                fill="#202124",
                align="left",
                valign="middle",
            ),
        ),
    )


PROBLEM_TEMPLATE = build_problem_template()


SEMANTIC = {
    "problem_id": PROBLEM_ID,
    "problem_type": "multi_answer_expression_comparison",
    "metadata": {
        "grade": 3,
        "semester": 1,
        "subject": "математика",
        "topic": "додавання трицифрових чисел і порівняння",
        "language": "uk-UA",
        "title": PROBLEM_TITLE,
        "question": "Порівняй значення і впиши у порожні місця >, = або <.",
    },
    "domain": {
        "objects": [
            {
                "id": "expression.problem_1_left",
                "type": "number_expression",
                "label": "ліва частина першого порівняння",
                "expression": "532",
                "value": 532,
            },
            {
                "id": "expression.problem_1_right",
                "type": "addition_expression",
                "label": "права частина першого порівняння",
                "expression": "248 + 274",
                "value": 522,
            },
            {
                "id": "comparison.problem_1",
                "type": "comparison",
                "label": "перше порівняння",
                "left": "expression.problem_1_left",
                "right": "expression.problem_1_right",
                "operator": ">",
            },
            {
                "id": "expression.problem_2_left",
                "type": "addition_expression",
                "label": "ліва частина другого порівняння",
                "expression": "346 + 667",
                "value": 1013,
            },
            {
                "id": "expression.problem_2_right",
                "type": "addition_expression",
                "label": "права частина другого порівняння",
                "expression": "428 + 585",
                "value": 1013,
            },
            {
                "id": "comparison.problem_2",
                "type": "comparison",
                "label": "друге порівняння",
                "left": "expression.problem_2_left",
                "right": "expression.problem_2_right",
                "operator": "=",
            },
        ],
        "relations": [
            {
                "id": "relation.problem_1_left_greater_than_right",
                "type": "greater_than",
                "subject": "expression.problem_1_left",
                "object": "expression.problem_1_right",
            },
            {
                "id": "relation.problem_2_left_equals_right",
                "type": "equal_to",
                "subject": "expression.problem_2_left",
                "object": "expression.problem_2_right",
            },
        ],
    },
    "answer": {
        "value": [">", "="],
        "unit": "",
        "items": [
            {"id": "answer.problem_1", "value": ">"},
            {"id": "answer.problem_2", "value": "="},
        ],
    },
}

SEMANTIC_OVERRIDE = SEMANTIC


SOLVABLE = {
    "schema": "modu.solvable.v1.2",
    "problem_id": PROBLEM_ID,
    "problem_type": "multi_answer_expression_comparison",
    "inputs": {
        "target_label": "правильні знаки порівняння",
        "unit": "",
        "answer_type": "comparison_operator",
        "allowed_operators": [">", "=", "<"],
        "quantities": {
            "problem_1": {
                "left_expression": "532",
                "left_value": 532,
                "right_expression": "248 + 274",
                "right_value": 522,
            },
            "problem_2": {
                "left_expression": "346 + 667",
                "left_value": 1013,
                "right_expression": "428 + 585",
                "right_value": 1013,
            },
        },
        "conditions": [
            "Обчисли значення кожного виразу.",
            "Порівняй ліву і праву частини.",
            "Запиши правильний знак: >, = або <.",
        ],
    },
    "given": [
        {
            "ref": "comparison.problem_1",
            "value": {
                "left": {"expression": "532", "value": 532},
                "right": {"expression": "248 + 274", "value": 522},
            },
        },
        {
            "ref": "comparison.problem_2",
            "value": {
                "left": {"expression": "346 + 667", "value": 1013},
                "right": {"expression": "428 + 585", "value": 1013},
            },
        },
    ],
    "target": {"ref": "answer.comparison_operators", "type": "operator_list"},
    "method": "обчислити значення виразів і порівняти їх",
    "plan": [
        "Обчислити праву частину першого порівняння: 248 + 274.",
        "Порівняти 532 з отриманим значенням.",
        "Обчислити обидві частини другого порівняння.",
        "Порівняти отримані значення і вибрати знак.",
    ],
    "steps": [
        {
            "id": "step.problem_1_calculate_right",
            "goal": "обчислити праву частину першого порівняння",
            "expr": "248 + 274",
            "value": 522,
            "explanation": "248 + 274 = 522.",
        },
        {
            "id": "step.problem_1_compare",
            "goal": "вибрати знак для першого порівняння",
            "relation_expr": "532 > 522",
            "expr": "532 > 522",
            "value": True,
            "explanation": "532 більше за 522, тому потрібний знак >.",
        },
        {
            "id": "step.problem_2_calculate_left",
            "goal": "обчислити ліву частину другого порівняння",
            "expr": "346 + 667",
            "value": 1013,
            "explanation": "346 + 667 = 1013.",
        },
        {
            "id": "step.problem_2_calculate_right",
            "goal": "обчислити праву частину другого порівняння",
            "expr": "428 + 585",
            "value": 1013,
            "explanation": "428 + 585 = 1013.",
        },
        {
            "id": "step.problem_2_compare",
            "goal": "вибрати знак для другого порівняння",
            "relation_expr": "1013 = 1013",
            "expr": "1013 == 1013",
            "value": True,
            "explanation": "Обидва значення дорівнюють 1013, тому потрібний знак =.",
        },
    ],
    "answer": SEMANTIC["answer"],
    "understanding": {
        "summary": "Потрібно обчислити вирази і вставити правильні знаки порівняння.",
        "facts": [
            {
                "ref": "comparison.problem_1",
                "label": "перше порівняння",
                "value": {"left": "532", "right": "248 + 274"},
                "unit": "",
                "source": "explicit",
            },
            {
                "ref": "comparison.problem_2",
                "label": "друге порівняння",
                "value": {"left": "346 + 667", "right": "428 + 585"},
                "unit": "",
                "source": "explicit",
            },
        ],
        "unknowns": [
            {
                "ref": "answer.comparison_operators",
                "label": "знаки порівняння",
                "unit": "",
                "source": "unknown",
            }
        ],
    },
}

SEMANTIC_ANSWER = SOLVABLE["answer"]
