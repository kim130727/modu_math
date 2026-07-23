from __future__ import annotations

from modu_math.dsl import (
    BlankSlot,
    Canvas,
    LineSlot,
    ProblemTemplate,
    RectSlot,
    Region,
    TextBoxSlot,
    TextSlot,
)


PROBLEM_ID = "P3_1_01_00040_15629"
PROBLEM_TITLE = "431과 세 자리 수의 덧셈 빈칸 채우기"


def build_problem_template() -> ProblemTemplate:
    return ProblemTemplate(
        id=PROBLEM_ID,
        title=PROBLEM_TITLE,
        canvas=Canvas(
            width=765,
            height=98,
            coordinate_mode="logical",
        ),
        regions=(
            Region(
                id="region.stem",
                role="stem",
                flow="absolute",
                slot_ids=("slot.instruction",),
            ),
            Region(
                id="region.vertical_addition",
                role="work",
                flow="absolute",
                slot_ids=(
                    "slot.first_number",
                    "slot.plus",
                    "slot.second.hundreds",
                    "slot.second.blank_box",
                    "slot.second.ones",
                    "slot.rule",
                    "slot.result.blank_box",
                    "slot.result.tens_ones",
                    "slot.blank1",
                    "slot.blank2",
                ),
            ),
        ),
        slots=(
            TextBoxSlot(
                id="slot.instruction",
                prompt="빈칸에 알맞은 수를 쓰라는 안내",
                text="□ 안에 알맞은 수를 써넣으시오.",
                semantic_role="instruction",
                x=20,
                y=1,
                width=290,
                height=20,
                font_size=14,
                font_family="Noto Sans KR",
                fill="#111111",
                align="left",
                valign="top",
            ),
            TextSlot(
                id="slot.first_number",
                prompt="첫 번째 수 431",
                text="431",
                semantic_role="given_number",
                x=58,
                y=38,
                font_size=15,
                fill="#111111",
            ),
            TextSlot(
                id="slot.plus",
                prompt="덧셈 기호",
                text="+",
                semantic_role="operator",
                x=38,
                y=61,
                font_size=15,
                fill="#111111",
            ),
            TextSlot(
                id="slot.second.hundreds",
                prompt="두 번째 수의 백의 자리 숫자 2",
                text="2",
                semantic_role="given_digit",
                x=58,
                y=61,
                font_size=15,
                fill="#111111",
            ),
            RectSlot(
                id="slot.second.blank_box",
                prompt="두 번째 수의 십의 자리 숫자를 쓰는 첫 번째 빈칸",
                semantic_role="answer_blank",
                x=70,
                y=46,
                width=14,
                height=19,
                fill="#ffffff",
                stroke="#111111",
                stroke_width=1,
            ),
            TextSlot(
                id="slot.second.ones",
                prompt="두 번째 수의 일의 자리 숫자 1",
                text="1",
                semantic_role="given_digit",
                x=87,
                y=61,
                font_size=15,
                fill="#111111",
            ),
            LineSlot(
                id="slot.rule",
                prompt="덧셈 계산선",
                semantic_role="calculation_rule",
                x1=31,
                y1=69,
                x2=99,
                y2=69,
                stroke="#111111",
                stroke_width=1,
            ),
            RectSlot(
                id="slot.result.blank_box",
                prompt="합의 백의 자리 숫자를 쓰는 두 번째 빈칸",
                semantic_role="answer_blank",
                x=56,
                y=75,
                width=14,
                height=19,
                fill="#ffffff",
                stroke="#111111",
                stroke_width=1,
            ),
            TextSlot(
                id="slot.result.tens_ones",
                prompt="합의 십의 자리와 일의 자리 숫자 62",
                text="62",
                semantic_role="result_digits",
                x=73,
                y=90,
                font_size=15,
                fill="#111111",
            ),
            BlankSlot(
                id="slot.blank1",
                prompt="두 번째 수의 십의 자리 숫자",
                answer_key="3",
                placeholder="",
            ),
            BlankSlot(
                id="slot.blank2",
                prompt="합의 백의 자리 숫자",
                answer_key="6",
                placeholder="",
            ),
        ),
        diagrams=(),
        groups=(),
        constraints=(),
        tags=(
            "grade-3",
            "addition",
            "three-digit-addition",
            "vertical-calculation",
            "fill-in-the-blank",
        ),
    )


PROBLEM_TEMPLATE = build_problem_template()


ANSWER = {
    "type": "multi_numeric",
    "value": [3, 6],
    "unit": "",
    "blanks": [
        {"id": "slot.blank1", "type": "number", "value": 3, "unit": ""},
        {"id": "slot.blank2", "type": "number", "value": 6, "unit": ""},
    ],
    "choices": [],
    "answer_key": [
        {"blank_id": "slot.blank1", "value": 3, "unit": ""},
        {"blank_id": "slot.blank2", "value": 6, "unit": ""},
    ],
    "sentence": "빈칸에 위에서부터 3, 6을 씁니다.",
}


SEMANTIC_OVERRIDE = {
    "problem_id": PROBLEM_ID,
    "problem_type": "vertical_addition_digit_fill_blank",
    "metadata": {
        "grade": 3,
        "semester": 1,
        "subject": "수학",
        "topic": "세 자리 수의 덧셈",
        "language": "ko-KR",
        "question": "□ 안에 알맞은 수를 써넣으시오.",
        "instruction": "일의 자리부터 같은 자리끼리 더하여 빈칸의 숫자를 구합니다.",
    },
    "domain": {
        "objects": [
            {
                "id": "number.augend",
                "type": "number",
                "label": "첫 번째 수",
                "value": 431,
            },
            {
                "id": "number.addend",
                "type": "partially_hidden_number",
                "label": "두 번째 수",
                "value": 231,
            },
            {
                "id": "digit.addend.tens",
                "type": "unknown_digit",
                "label": "두 번째 수의 십의 자리 숫자",
                "value": 3,
            },
            {
                "id": "number.sum",
                "type": "partially_hidden_number",
                "label": "두 수의 합",
                "value": 662,
            },
            {
                "id": "digit.sum.hundreds",
                "type": "unknown_digit",
                "label": "합의 백의 자리 숫자",
                "value": 6,
            },
        ],
        "relations": [
            {
                "id": "relation.vertical_addition",
                "type": "addition",
                "from_ids": [
                    "number.augend",
                    "number.addend",
                ],
                "to_id": "number.sum",
                "equation": "431 + 231 = 662",
            },
            {
                "id": "relation.tens_column",
                "type": "digit_addition_without_carry",
                "from_values": [3, 3],
                "to_value": 6,
                "equation": "3 + 3 = 6",
            },
            {
                "id": "relation.hundreds_column",
                "type": "digit_addition_without_carry",
                "from_values": [4, 2],
                "to_value": 6,
                "equation": "4 + 2 = 6",
            },
        ],
        "problem_solving": {
            "understand": {
                "given_refs": [
                    "number.augend",
                    "number.addend",
                    "number.sum",
                ],
                "target_ref": "answer.all",
                "condition_refs": [
                    "relation.vertical_addition",
                    "relation.tens_column",
                    "relation.hundreds_column",
                ],
            },
            "plan": {
                "method": "column_addition",
                "description": "일의 자리부터 같은 자리의 숫자끼리 더하여 빈칸을 구합니다.",
            },
            "execute": {
                "expected_operations": [
                    "ones_column_addition",
                    "tens_column_addition",
                    "hundreds_column_addition",
                ],
            },
            "review": {
                "check_methods": [
                    "full_addition_check",
                    "inverse_subtraction",
                ],
            },
        },
    },
    "answer": ANSWER,
}


SOLVABLE = {
    "schema": "modu.solvable.v1.2",
    "problem_id": PROBLEM_ID,
    "problem_type": "vertical_addition_digit_fill_blank",
    "inputs": {
        "target_label": "세로셈의 두 빈칸에 들어갈 숫자",
        "unit": "",
        "quantities": {
            "augend": 431,
            "addend_hundreds_digit": 2,
            "addend_ones_digit": 1,
            "sum_tens_digit": 6,
            "sum_ones_digit": 2,
        },
        "conditions": [
            "같은 자리의 숫자끼리 더합니다.",
            "일의 자리 계산은 1+1=2입니다.",
            "받아올림이 없는 덧셈입니다.",
        ],
    },
    "given": [
        {"ref": "number.augend", "value": 431},
        {
            "ref": "number.addend.visible_digits",
            "value": {
                "hundreds": 2,
                "ones": 1,
            },
        },
        {
            "ref": "number.sum.visible_digits",
            "value": {
                "tens": 6,
                "ones": 2,
            },
        },
    ],
    "target": {
        "ref": "answer.all",
        "type": "number_list",
    },
    "method": "일의 자리부터 같은 자리끼리 더하여 두 번째 수의 십의 자리와 합의 백의 자리 숫자를 구합니다.",
    "understanding": {
        "summary": "431과 2□1을 더한 결과가 □62일 때 두 빈칸의 숫자를 구하는 문제입니다.",
        "facts": [
            {
                "ref": "number.augend",
                "label": "첫 번째 수",
                "value": 431,
                "unit": "",
                "source": "explicit",
            },
            {
                "ref": "digit.addend.hundreds",
                "label": "두 번째 수의 백의 자리 숫자",
                "value": 2,
                "unit": "",
                "source": "explicit",
            },
            {
                "ref": "digit.addend.ones",
                "label": "두 번째 수의 일의 자리 숫자",
                "value": 1,
                "unit": "",
                "source": "explicit",
            },
            {
                "ref": "digit.sum.tens",
                "label": "합의 십의 자리 숫자",
                "value": 6,
                "unit": "",
                "source": "explicit",
            },
            {
                "ref": "digit.sum.ones",
                "label": "합의 일의 자리 숫자",
                "value": 2,
                "unit": "",
                "source": "explicit",
            },
        ],
        "unknowns": [
            {
                "ref": "digit.addend.tens",
                "label": "두 번째 수의 십의 자리 숫자",
                "unit": "",
                "source": "unknown",
            },
            {
                "ref": "digit.sum.hundreds",
                "label": "합의 백의 자리 숫자",
                "unit": "",
                "source": "unknown",
            },
        ],
        "relation": {
            "type": "vertical_column_addition",
            "statement": "같은 자리의 숫자끼리 더하면 431+231=662가 됩니다.",
            "symbolic": "431 + 2□1 = □62",
            "uses": [
                "number.augend",
                "number.addend.visible_digits",
                "number.sum.visible_digits",
            ],
            "result": "answer.all",
        },
        "diagnostic_questions": [
            {
                "id": "understand.ones_column",
                "type": "multiple_choice",
                "prompt": "일의 자리 계산은 무엇인가요?",
                "choices": [
                    "1+1=2",
                    "1+2=3",
                    "3+1=4",
                ],
                "answer_index": 0,
            },
            {
                "id": "understand.tens_column",
                "type": "multiple_choice",
                "prompt": "십의 자리에서 3에 어떤 숫자를 더해야 6이 되나요?",
                "choices": [
                    "3",
                    "2",
                    "6",
                ],
                "answer_index": 0,
            },
        ],
        "student_restatement": {
            "prompt": "어떤 방법으로 빈칸을 구해야 하나요?",
            "template": "일의 자리부터 같은 자리의 숫자끼리 더하여 빈칸을 구합니다.",
            "answer": "일의 자리부터 같은 자리의 숫자끼리 더하여 빈칸을 구합니다.",
        },
    },
    "plan": [
        "일의 자리에서 1+1=2임을 확인합니다.",
        "십의 자리에서 3+□=6을 만족하는 숫자를 구합니다.",
        "백의 자리에서 4+2=□를 계산합니다.",
        "완성된 세로셈 431+231=662를 확인합니다.",
    ],
    "steps": [
        {
            "id": "step.ones_column",
            "expr": "1 + 1",
            "value": 2,
            "explanation": "일의 자리의 합은 2이므로 받아올림이 없습니다.",
        },
        {
            "id": "step.solve_addend_tens",
            "expr": "3 + □ = 6",
            "value": 3,
            "explanation": "십의 자리에서 3에 3을 더하면 6이므로 첫 번째 빈칸은 3입니다.",
        },
        {
            "id": "step.solve_sum_hundreds",
            "expr": "4 + 2",
            "value": 6,
            "explanation": "백의 자리에서 4와 2를 더하면 6이므로 두 번째 빈칸은 6입니다.",
        },
        {
            "id": "step.complete_addition",
            "expr": "431 + 231",
            "value": 662,
            "explanation": "빈칸을 채운 두 수를 더하면 662입니다.",
        },
    ],
    "checks": [
        {
            "id": "check.full_addition",
            "expr": "431 + 231",
            "expected": 662,
            "actual": 662,
            "pass": True,
        },
        {
            "id": "check.inverse_subtraction",
            "expr": "662 - 431",
            "expected": 231,
            "actual": 231,
            "pass": True,
        },
        {
            "id": "check.visible_result_digits",
            "expr": "662의 십의 자리와 일의 자리",
            "expected": 62,
            "actual": 62,
            "pass": True,
        },
    ],
    "answer": ANSWER,
}


SEMANTIC_ANSWER = SOLVABLE["answer"]
