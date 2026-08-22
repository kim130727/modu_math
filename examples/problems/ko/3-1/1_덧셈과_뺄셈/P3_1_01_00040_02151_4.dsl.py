from __future__ import annotations

from modu_math.dsl import (
    Canvas,
    LineSlot,
    ProblemTemplate,
    RectSlot,
    Region,
    TextBoxSlot,
)

PROBLEM_ID = "P3_1_01_00040_02151_4"
PROBLEM_TITLE = "세 자리 수의 덧셈 계산 (4)"


def build_problem_template() -> ProblemTemplate:
    return ProblemTemplate(
        id=PROBLEM_ID,
        title=PROBLEM_TITLE,
        canvas=Canvas(
            width=400,
            height=300,
            coordinate_mode="logical",
        ),
        regions=(
            Region(
                id="region.stem",
                role="stem",
                flow="absolute",
                slot_ids=(
                    "slot.instruction",
                    "slot.first_addend",
                    "slot.plus_sign",
                    "slot.second_addend",
                    "slot.calc_line",
                    "slot.answer_box",
                ),
            ),
        ),
        slots=(
            TextBoxSlot(
                id="slot.instruction",
                x=30,
                y=24,
                width=340,
                height=38,
                text="□ 안에 알맞은 수를 써넣으시오.",
                font_size=24,
                font_family='"Poor Story", "Noto Sans KR", sans-serif',
                fill="#202124",
                align="left",
                valign="middle",
            ),
            TextBoxSlot(
                id="slot.first_addend",
                x=120,
                y=96,
                width=120,
                height=40,
                text="6 5 8",
                font_size=26,
                font_family='"Poor Story", "Noto Sans KR", sans-serif',
                fill="#202124",
                align="center",
                line_height=1.25,
            ),
            TextBoxSlot(
                id="slot.plus_sign",
                x=96,
                y=136,
                width=30,
                height=40,
                text="+",
                font_size=26,
                font_family='"Poor Story", "Noto Sans KR", sans-serif',
                fill="#202124",
                align="center",
                line_height=1.25,
            ),
            TextBoxSlot(
                id="slot.second_addend",
                x=120,
                y=136,
                width=120,
                height=40,
                text="1 9 4",
                font_size=26,
                font_family='"Poor Story", "Noto Sans KR", sans-serif',
                fill="#202124",
                align="center",
                line_height=1.25,
            ),
            LineSlot(
                id="slot.calc_line",
                x1=96.0,
                y1=180.0,
                x2=254.0,
                y2=180.0,
                stroke="#111111",
                stroke_width=1.6,
            ),
            RectSlot(
                id="slot.answer_box",
                x=120.0,
                y=188.0,
                width=120.0,
                height=38.0,
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
                    "max_font_size": 32,
                    "font_weight": 700,
                    "horizontal_align": "center",
                    "vertical_align": "middle",
                    "padding": 4,
                    "text_color": "#222222",
                },
            ),
        ),
    )


PROBLEM_TEMPLATE = build_problem_template()

ANSWER = {
    "value": 852,
    "unit": "",
    "values": [852],
    "choices": [],
    "blanks": [
        {
            "id": "slot.answer_box",
            "slot_id": "slot.answer_box",
            "expected": 852,
        },
    ],
    "answer_key": [
        {"slot_id": "slot.answer_box", "value": 852},
    ],
}

SEMANTIC = {
    "problem_id": PROBLEM_ID,
    "problem_type": "vertical_addition",
    "metadata": {
        "title": PROBLEM_TITLE,
        "grade": 3,
        "semester": 1,
        "subject": "수학",
        "topic": "세 자리 수의 덧셈 계산",
        "language": "ko-KR",
        "required_layout_ids": [
            "slot.answer_box",
        ],
    },
    "domain": {
        "objects": [
            {
                "id": "addition.problem_4",
                "type": "vertical_addition",
                "label": "세로셈",
                "first_addend": 658,
                "second_addend": 194,
                "sum": 852,
            },
        ],
        "relations": [
            {
                "id": "relation.problem_4_sum",
                "type": "sum_of",
                "subject": "addition.problem_4",
                "values": [658, 194],
            },
        ],
    },
    "answer": ANSWER,
}

SEMANTIC_OVERRIDE = SEMANTIC

SOLVABLE = {
    "schema": "modu.solvable.v1.2",
    "problem_id": PROBLEM_ID,
    "problem_type": "vertical_addition",
    "inputs": {
        "target_label": "세로셈 계산 결과",
        "unit": "",
        "quantities": {
            "first_addend": 658,
            "second_addend": 194,
        },
        "conditions": [
            "일의 자리부터 차례대로 계산합니다.",
            "각 자리의 합이 10 이상이면 바로 윗자리로 1을 받아올림합니다.",
        ],
    },
    "given": [
        {
            "ref": "addition.problem_4",
            "value": {
                "first_addend": 658,
                "second_addend": 194,
            },
        },
    ],
    "target": {
        "ref": "answer.value",
        "type": "number",
    },
    "method": "일의 자리부터 더하고 받아올림을 다음 자리 계산에 포함한다.",
    "plan": [
        "일의 자리 8+4=12를 계산하여 1을 올리고 2를 쓴다.",
        "십의 자리 1+5+9=15를 계산하여 1을 올리고 5를 쓴다.",
        "백의 자리 1+6+1=8을 쓴다.",
    ],
    "steps": [
        {
            "id": "step.add_numbers",
            "expr": "658 + 194",
            "value": 852,
            "explanation": "658과 194를 더하면 852입니다.",
        },
    ],
    "checks": [
        {
            "id": "check.total",
            "expr": "658 + 194",
            "expected": 852,
            "actual": 852,
            "pass": True,
        },
    ],
    "answer": ANSWER,
    "understanding": {
        "summary": "658과 194의 합을 계산합니다.",
        "facts": [
            {
                "ref": "first_addend",
                "label": "첫 번째 수",
                "value": 658,
                "unit": "",
                "source": "explicit",
            },
            {
                "ref": "second_addend",
                "label": "두 번째 수",
                "value": 194,
                "unit": "",
                "source": "explicit",
            },
        ],
        "unknowns": [
            {
                "ref": "answer.value",
                "label": "계산 결과",
                "unit": "",
                "source": "unknown",
            },
        ],
        "relation": {
            "type": "sum_of",
            "statement": "두 수의 합을 구합니다.",
            "symbolic": "658 + 194",
            "uses": ["first_addend", "second_addend"],
            "result": "852",
        },
    },
}
