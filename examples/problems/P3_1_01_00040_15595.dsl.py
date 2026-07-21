from __future__ import annotations

from modu_math.dsl import (
    BlankSlot,
    Canvas,
    LineSlot,
    ProblemTemplate,
    Region,
    TextSlot,
)


PROBLEM_ID = "P3_1_01_00040_15595"
PROBLEM_TITLE = "세 자리 수의 덧셈 계산하기"


def build_problem_template() -> ProblemTemplate:
    return ProblemTemplate(
        id=PROBLEM_ID,
        title=PROBLEM_TITLE,
        canvas=Canvas(
            width=760,
            height=260,
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
                id="region.calculation.1",
                role="body",
                flow="absolute",
                slot_ids=(
                    "slot.calculation.1.label",
                    "slot.calculation.1.top",
                    "slot.calculation.1.plus",
                    "slot.calculation.1.bottom",
                    "slot.calculation.1.line",
                ),
            ),
            Region(
                id="region.calculation.2",
                role="body",
                flow="absolute",
                slot_ids=(
                    "slot.calculation.2.label",
                    "slot.calculation.2.top",
                    "slot.calculation.2.plus",
                    "slot.calculation.2.bottom",
                    "slot.calculation.2.line",
                ),
            ),
        ),
        slots=(
            TextSlot(
                id="slot.instruction",
                prompt="",
                text="다음 계산을 하시오.",
                style_role="question",
                x=25,
                y=28,
                font_size=24,
                fill="#111111",
            ),
            TextSlot(
                id="slot.calculation.1.label",
                prompt="",
                text="(1)",
                style_role="label",
                x=28,
                y=77,
                font_size=22,
                fill="#111111",
            ),
            TextSlot(
                id="slot.calculation.1.top",
                prompt="",
                text="270",
                style_role="math",
                x=120,
                y=77,
                font_size=25,
                max_width=80,
                anchor="middle",
                fill="#111111",
            ),
            TextSlot(
                id="slot.calculation.1.plus",
                prompt="",
                text="+",
                style_role="math",
                x=73,
                y=119,
                font_size=25,
                max_width=30,
                anchor="middle",
                fill="#111111",
            ),
            TextSlot(
                id="slot.calculation.1.bottom",
                prompt="",
                text="125",
                style_role="math",
                x=120,
                y=119,
                font_size=25,
                max_width=80,
                anchor="middle",
                fill="#111111",
            ),
            LineSlot(
                id="slot.calculation.1.line",
                prompt="",
                x1=72,
                y1=142,
                x2=162,
                y2=142,
                stroke="#111111",
                stroke_width=1.5,
            ),
            TextSlot(
                id="slot.calculation.2.label",
                prompt="",
                text="(2)",
                style_role="label",
                x=205,
                y=77,
                font_size=22,
                fill="#111111",
            ),
            TextSlot(
                id="slot.calculation.2.top",
                prompt="",
                text="394",
                style_role="math",
                x=297,
                y=77,
                font_size=25,
                max_width=80,
                anchor="middle",
                fill="#111111",
            ),
            TextSlot(
                id="slot.calculation.2.plus",
                prompt="",
                text="+",
                style_role="math",
                x=250,
                y=119,
                font_size=25,
                max_width=30,
                anchor="middle",
                fill="#111111",
            ),
            TextSlot(
                id="slot.calculation.2.bottom",
                prompt="",
                text="205",
                style_role="math",
                x=297,
                y=119,
                font_size=25,
                max_width=80,
                anchor="middle",
                fill="#111111",
            ),
            LineSlot(
                id="slot.calculation.2.line",
                prompt="",
                x1=249,
                y1=142,
                x2=339,
                y2=142,
                stroke="#111111",
                stroke_width=1.5,
            ),
            BlankSlot(
                id="slot.answer.1",
                prompt="(1)",
                answer_key="395",
                placeholder="답",
            ),
            BlankSlot(
                id="slot.answer.2",
                prompt="(2)",
                answer_key="599",
                placeholder="답",
            ),
        ),
    )


PROBLEM_TEMPLATE = build_problem_template()


ANSWER = {
    "type": "multi_numeric",
    "value": [395, 599],
    "unit": "",
    "values": [
        {
            "value": 395,
            "unit": "",
            "target_ref": "answer.calculation_1",
        },
        {
            "value": 599,
            "unit": "",
            "target_ref": "answer.calculation_2",
        },
    ],
    "derived_from": "step.calculate_both",
}


SEMANTIC_OVERRIDE = {
    "problem_id": PROBLEM_ID,
    "problem_type": "multi_numeric_answer_vertical_addition_problem",
    "metadata": {
        "language": "ko-KR",
        "question": "다음 계산을 하시오.",
        "instruction": "두 세 자리 수의 덧셈을 각각 계산합니다.",
    },
    "domain": {
        "objects": [
            {
                "id": "calculation.1",
                "type": "addition_expression",
                "label": "첫 번째 덧셈",
                "addends": [270, 125],
            },
            {
                "id": "calculation.2",
                "type": "addition_expression",
                "label": "두 번째 덧셈",
                "addends": [394, 205],
            },
            {
                "id": "answer.calculation_1",
                "type": "unknown_number",
                "label": "첫 번째 계산의 답",
            },
            {
                "id": "answer.calculation_2",
                "type": "unknown_number",
                "label": "두 번째 계산의 답",
            },
            {
                "id": "answer.values",
                "type": "number_pair",
                "label": "두 덧셈의 답",
            },
        ],
        "relations": [
            {
                "id": "relation.calculation_1_sum",
                "type": "sum_result",
                "subject": "answer.calculation_1",
                "object": "calculation.1",
            },
            {
                "id": "relation.calculation_2_sum",
                "type": "sum_result",
                "subject": "answer.calculation_2",
                "object": "calculation.2",
            },
        ],
        "problem_solving": {
            "understand": {
                "given_refs": [
                    "calculation.1",
                    "calculation.2",
                ],
                "target_ref": "answer.values",
                "condition_refs": [
                    "relation.calculation_1_sum",
                    "relation.calculation_2_sum",
                ],
            },
            "plan": {
                "method": "vertical_addition_by_place_value",
                "description": "각 계산에서 같은 자리의 수끼리 더합니다.",
            },
            "execute": {
                "expected_operations": ["addition"],
            },
            "review": {
                "check_methods": ["subtraction_check"],
            },
        },
    },
    "answer": ANSWER,
}


SOLVABLE = {
    "schema": "modu.solvable.v1.2",
    "problem_id": PROBLEM_ID,
    "problem_type": "multi_numeric_answer_vertical_addition_problem",
    "inputs": {
        "target_label": "두 덧셈의 답",
        "unit": "",
        "calculations": [
            {
                "id": "calculation.1",
                "addends": [270, 125],
            },
            {
                "id": "calculation.2",
                "addends": [394, 205],
            },
        ],
    },
    "given": [
        {
            "ref": "calculation.1",
            "value": {
                "operator": "+",
                "left": 270,
                "right": 125,
            },
        },
        {
            "ref": "calculation.2",
            "value": {
                "operator": "+",
                "left": 394,
                "right": 205,
            },
        },
    ],
    "target": {
        "ref": "answer.values",
        "type": "number_pair",
    },
    "method": "각 세로셈에서 같은 자리의 수끼리 더해 두 계산의 답을 각각 구합니다.",
    "understanding": {
        "summary": "주어진 두 세 자리 수의 덧셈을 각각 계산하는 문제입니다.",
        "facts": [
            {
                "ref": "calculation.1",
                "label": "첫 번째 계산",
                "value": "270 + 125",
                "unit": "",
                "source": "explicit",
            },
            {
                "ref": "calculation.2",
                "label": "두 번째 계산",
                "value": "394 + 205",
                "unit": "",
                "source": "explicit",
            },
        ],
        "unknowns": [
            {
                "ref": "answer.calculation_1",
                "label": "270과 125의 합",
                "unit": "",
            },
            {
                "ref": "answer.calculation_2",
                "label": "394와 205의 합",
                "unit": "",
            },
        ],
        "relation": {
            "type": "independent_additions",
            "statement": "각 식에서 두 수를 더하여 각각의 답을 구합니다.",
            "symbolic": "270 + 125 = □, 394 + 205 = □",
            "uses": [
                "calculation.1",
                "calculation.2",
            ],
            "result": "answer.values",
        },
        "diagnostic_questions": [
            {
                "id": "understand.operation",
                "type": "multiple_choice",
                "prompt": "두 식에서 공통으로 해야 하는 계산은 무엇인가요?",
                "choices": [
                    "덧셈",
                    "뺄셈",
                    "곱셈",
                ],
                "answer_index": 0,
            },
            {
                "id": "understand.place_value",
                "type": "multiple_choice",
                "prompt": "세로셈에서는 어떤 수끼리 먼저 더하나요?",
                "choices": [
                    "같은 자리의 수끼리 더합니다.",
                    "가장 큰 숫자끼리 더합니다.",
                    "서로 다른 자리의 수끼리 더합니다.",
                ],
                "answer_index": 0,
            },
        ],
    },
    "plan": [
        "각 식에서 일의 자리부터 같은 자리의 수끼리 더합니다.",
        "십의 자리와 백의 자리도 차례로 더합니다.",
        "각 덧셈의 결과를 뺄셈으로 검산합니다.",
    ],
    "steps": [
        {
            "id": "step.calculate_1",
            "expr": "270 + 125",
            "value": 395,
            "explanation": "일의 자리, 십의 자리, 백의 자리 순서로 더하면 395입니다.",
        },
        {
            "id": "step.calculate_2",
            "expr": "394 + 205",
            "value": 599,
            "explanation": "일의 자리, 십의 자리, 백의 자리 순서로 더하면 599입니다.",
        },
        {
            "id": "step.calculate_both",
            "expr": "[270 + 125, 394 + 205]",
            "value": [395, 599],
            "explanation": "두 계산의 결과를 문제 번호 순서대로 정리합니다.",
        },
    ],
    "checks": [
        {
            "id": "check.calculation_1",
            "expr": "395 - 125",
            "expected": 270,
            "actual": 270,
            "pass": True,
        },
        {
            "id": "check.calculation_2",
            "expr": "599 - 205",
            "expected": 394,
            "actual": 394,
            "pass": True,
        },
    ],
    "answer": ANSWER,
}


SEMANTIC_ANSWER = SOLVABLE["answer"]
