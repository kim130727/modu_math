from __future__ import annotations

from modu_math.dsl import (
    Canvas,
    LineSlot,
    ProblemTemplate,
    RectSlot,
    Region,
    TextSlot,
)


PROBLEM_ID = "P3_1_01_00040_15598_1"
PROBLEM_TITLE = "자리값별 부분합으로 덧셈하기"


def _expanded_addition_slots(
    *,
    prefix: str,
    label: str,
    x: float,
    top: str,
    bottom: str,
) -> tuple[object, ...]:
    center_x = x + 92
    return (
        TextSlot(
            id=f"slot.{prefix}.top",
            prompt="",
            text=top,
            style_role="math",
            x=center_x,
            y=78,
            font_size=25,
            max_width=80,
            anchor="middle",
            fill="#111111",
        ),
        TextSlot(
            id=f"slot.{prefix}.plus",
            prompt="",
            text="+",
            style_role="math",
            x=x + 45,
            y=120,
            font_size=25,
            max_width=30,
            anchor="middle",
            fill="#111111",
        ),
        TextSlot(
            id=f"slot.{prefix}.bottom",
            prompt="",
            text=bottom,
            style_role="math",
            x=center_x,
            y=120,
            font_size=25,
            max_width=80,
            anchor="middle",
            fill="#111111",
        ),
        LineSlot(
            id=f"slot.{prefix}.line.top",
            prompt="",
            x1=x + 44,
            y1=143,
            x2=x + 136,
            y2=143,
            stroke="#111111",
            stroke_width=1.5,
        ),
        RectSlot(
            id=f"slot.{prefix}.box.tens",
            prompt="",
            x=x + 89,
            y=198,
            width=43,
            height=27,
            fill="#ffffff",
            stroke="#111111",
            stroke_width=1,
        ),
        RectSlot(
            id=f"slot.{prefix}.box.hundreds",
            prompt="",
            x=x + 74,
            y=239,
            width=58,
            height=27,
            fill="#ffffff",
            stroke="#111111",
            stroke_width=1,
        ),
        LineSlot(
            id=f"slot.{prefix}.line.bottom",
            prompt="",
            x1=x + 44,
            y1=278,
            x2=x + 136,
            y2=278,
            stroke="#111111",
            stroke_width=1.5,
        ),
        RectSlot(
            id=f"slot.{prefix}.box.total",
            prompt="",
            x=x + 74,
            y=291,
            width=58,
            height=29,
            fill="#ffffff",
            stroke="#111111",
            stroke_width=1,
        ),
    )


def build_problem_template() -> ProblemTemplate:
    calculation_1_ids = (
        "slot.calculation.1.top",
        "slot.calculation.1.plus",
        "slot.calculation.1.bottom",
        "slot.calculation.1.line.top",
        "konva_1786192274303_paste_279482_0",
        "slot.calculation.1.box.tens",
        "slot.calculation.1.box.hundreds",
        "slot.calculation.1.line.bottom",
        "slot.calculation.1.box.total",
    )

    return ProblemTemplate(
        id=PROBLEM_ID,
        title=PROBLEM_TITLE,
        canvas=Canvas(
            width=350,
            height=350,
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
                slot_ids=calculation_1_ids,
            ),
        ),
        slots=(TextSlot(
                id="slot.instruction",
                prompt="",
                text="□ 안에 알맞은 수를 써넣으시오.",
                style_role="question",
                x=25,
                y=30,
                font_size=24,
                fill="#111111",
            ),
            *_expanded_addition_slots(
                prefix="calculation.1",
                label="(1)",
                x=25,
                top="217",
                bottom="542",
            ),
            RectSlot(
                id='konva_1786192274303_paste_279482_0',
                prompt='',
                x=181.833,
                y=172.757,
                width=20.242,
                height=27,
                fill='#ffffff',
                stroke='#111111',
                stroke_width=1,
                interaction={
                    'type': 'input',
                    'role': 'answer',
                    'value_type': 'digit',
                    'max_length': 1,
                    'include_in_submission': True,
                    'order': 0,
                    'group_id': 'final_answer',
                    'answer_key_index': 0,
                    'answer_ref': 'answer_key[0]',
                    'auto_advance': True,
                    'keyboard': 'number',
                },
                input_style={
                    'font_size_mode': 'auto',
                    'font_size_adjust': 0,
                    'min_font_size': 14,
                    'max_font_size': 52,
                    'font_weight': 700,
                    'horizontal_align': 'center',
                    'vertical_align': 'middle',
                    'padding': 6,
                    'text_color': '#222222',
                },
            ),
        ),
    )


PROBLEM_TEMPLATE = build_problem_template()


ANSWER_VALUES = [9, 50, 700, 759]

ANSWER = {
    "type": "multi_numeric",
    "value": ANSWER_VALUES,
    "unit": "",
    "values": [
        {"value": 9, "unit": "", "target_ref": "answer.1.ones"},
        {"value": 50, "unit": "", "target_ref": "answer.1.tens"},
        {"value": 700, "unit": "", "target_ref": "answer.1.hundreds"},
        {"value": 759, "unit": "", "target_ref": "answer.1.total"},
    ],
    "derived_from": "step.collect_answers",
}


SEMANTIC_OVERRIDE = {
    "problem_id": PROBLEM_ID,
    "problem_type": "multi_numeric_answer_expanded_vertical_addition_problem",
    "metadata": {
        "language": "ko-KR",
        "question": "□ 안에 알맞은 수를 써넣으시오.",
        "instruction": "각 자리의 부분합과 전체 합을 차례로 씁니다.",
    },
    "domain": {
        "objects": [
            {
                "id": "calculation.1",
                "type": "expanded_addition",
                "label": "첫 번째 덧셈",
                "addends": [217, 542],
            },
            {
                "id": "answer.values",
                "type": "number_list",
                "label": "첫 번째 덧셈의 자리별 부분합과 전체 합",
            },
        ],
        "relations": [
            {
                "id": "relation.calculation_1_expansion",
                "type": "sum_by_place_value",
                "subject": "calculation.1",
                "result": "answer.values",
            },
        ],
        "problem_solving": {
            "understand": {
                "given_refs": [
                    "calculation.1",
                ],
                "target_ref": "answer.values",
                "condition_refs": [
                    "relation.calculation_1_expansion",
                ],
            },
            "plan": {
                "method": "expanded_addition_by_place_value",
                "description": "일, 십, 백의 자리 부분합을 각각 구한 뒤 모두 더합니다.",
            },
            "execute": {
                "expected_operations": [
                    "place_value_decomposition",
                    "addition",
                ],
            },
            "review": {
                "check_methods": [
                    "partial_sum_total_check",
                    "direct_addition_check",
                ],
            },
        },
    },
    "answer": ANSWER,
}


SOLVABLE = {
    "schema": "modu.solvable.v1.2",
    "problem_id": PROBLEM_ID,
    "problem_type": "multi_numeric_answer_expanded_vertical_addition_problem",
    "inputs": {
        "target_label": "첫 번째 덧셈의 자리별 부분합과 전체 합",
        "unit": "",
        "calculations": [
            {
                "id": "calculation.1",
                "addends": [217, 542],
            },
        ],
        "answer_order": [
            "1.ones",
            "1.tens",
            "1.hundreds",
            "1.total",
        ],
    },
    "given": [
        {
            "ref": "calculation.1",
            "value": {
                "operator": "+",
                "left": 217,
                "right": 542,
            },
        },
    ],
    "target": {
        "ref": "answer.values",
        "type": "number_list",
    },
    "understanding": {
        "summary": (
            "217 + 542에서 일의 자리, 십의 자리, 백의 자리의 부분합을 "
            "각각 구하고 이를 더해 전체 합을 구하는 문제입니다."
        ),
        "facts": [
            {
                "ref": "calculation.1",
                "label": "첫 번째 계산",
                "value": "217 + 542",
                "unit": "",
                "source": "explicit",
            },
        ],
        "unknowns": [
            {
                "ref": "answer.values",
                "label": "네 빈칸에 들어갈 수",
                "unit": "",
            },
        ],
        "relation": {
            "type": "expanded_addition_by_place_value",
            "statement": (
                "덧셈을 일의 자리 부분합, 십의 자리 부분합, 백의 자리 부분합으로 "
                "나누고 세 부분합을 더하여 전체 합을 구합니다."
            ),
            "symbolic": "(217 + 542) = (7 + 2) + (10 + 40) + (200 + 500)",
            "uses": [
                "calculation.1",
            ],
            "result": "answer.values",
        },
        "diagnostic_questions": [
            {
                "id": "understand.first_box",
                "type": "multiple_choice",
                "prompt": "각 계산의 첫 번째 작은 칸에는 무엇을 쓰나요?",
                "choices": [
                    "일의 자리끼리 더한 값",
                    "십의 자리끼리 더한 값",
                    "두 수의 전체 합",
                ],
                "answer_index": 0,
            },
            {
                "id": "understand.tens_value",
                "type": "multiple_choice",
                "prompt": "217의 십의 자리 숫자 1이 나타내는 값은 무엇인가요?",
                "choices": [
                    "1",
                    "10",
                    "100",
                ],
                "answer_index": 1,
            },
        ],
    },
    "method": "각 수를 자리값으로 나누어 같은 자리끼리 더한 뒤 부분합들을 더합니다.",
    "plan": [
        "첫 번째 덧셈의 일, 십, 백의 자리 부분합을 차례로 구합니다.",
        "첫 번째 계산의 세 부분합을 더해 전체 합을 구합니다.",
        "부분합의 합이 직접 계산한 덧셈 결과와 같은지 확인합니다.",
    ],
    "steps": [
        {
            "id": "step.1.ones",
            "expr": "7 + 2",
            "value": 9,
            "explanation": "217과 542의 일의 자리끼리 더합니다.",
        },
        {
            "id": "step.1.tens",
            "expr": "10 + 40",
            "value": 50,
            "explanation": "십의 자리 숫자가 나타내는 값 10과 40을 더합니다.",
        },
        {
            "id": "step.1.hundreds",
            "expr": "200 + 500",
            "value": 700,
            "explanation": "백의 자리 숫자가 나타내는 값 200과 500을 더합니다.",
        },
        {
            "id": "step.1.total",
            "expr": "9 + 50 + 700",
            "value": 759,
            "explanation": "세 자리의 부분합을 모두 더합니다.",
        },
        {
            "id": "step.collect_answers",
            "expr": "[9, 50, 700, 759]",
            "value": ANSWER_VALUES,
            "explanation": "빈칸의 위에서 아래 순서대로 답을 정리합니다.",
        },
    ],
    "checks": [
        {
            "id": "check.1.partial_sum",
            "expr": "9 + 50 + 700",
            "expected": 759,
            "actual": 759,
            "pass": True,
        },
        {
            "id": "check.1.direct_addition",
            "expr": "217 + 542",
            "expected": 759,
            "actual": 759,
            "pass": True,
        },
    ],
    "answer": ANSWER,
}


SEMANTIC_ANSWER = SOLVABLE["answer"]
