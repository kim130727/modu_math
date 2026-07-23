from __future__ import annotations

from modu_math.dsl import (
    BlankSlot,
    Canvas,
    ProblemTemplate,
    RectSlot,
    Region,
    TextSlot,
)


PROBLEM_ID = "P3_1_01_00040_15726"
PROBLEM_TITLE = "수 모형으로 알아보는 262와 271의 합"


def _model_slot_ids(prefix: str, hundreds: int, tens: int, ones: int) -> tuple[str, ...]:
    return (
        *(f"slot.{prefix}.hundred.{index}" for index in range(1, hundreds + 1)),
        *(f"slot.{prefix}.ten.{index}" for index in range(1, tens + 1)),
        *(f"slot.{prefix}.one.{index}" for index in range(1, ones + 1)),
        f"slot.{prefix}.label",
    )


def _model_slots(
    prefix: str,
    *,
    x: int,
    y: int,
    number: int,
    hundreds: int,
    tens: int,
    ones: int,
) -> tuple[object, ...]:
    slots: list[object] = []

    for index in range(hundreds):
        slots.append(
            RectSlot(
                id=f"slot.{prefix}.hundred.{index + 1}",
                prompt="백 모형",
                semantic_role="hundred_block",
                x=x + index * 39,
                y=y,
                width=34,
                height=34,
                fill="#dcead5",
                stroke="#557260",
                stroke_width=1,
            )
        )

    tens_x = x + hundreds * 39 + 2
    for index in range(tens):
        slots.append(
            RectSlot(
                id=f"slot.{prefix}.ten.{index + 1}",
                prompt="십 모형",
                semantic_role="ten_rod",
                x=tens_x + index * 8,
                y=y,
                width=5,
                height=34,
                fill="#d7e8f2",
                stroke="#54758b",
                stroke_width=1,
            )
        )

    ones_x = tens_x + tens * 8 + 2
    for index in range(ones):
        slots.append(
            RectSlot(
                id=f"slot.{prefix}.one.{index + 1}",
                prompt="낱개 모형",
                semantic_role="one_block",
                x=ones_x,
                y=y + 24 + index * 7,
                width=5,
                height=5,
                fill="#f2d8d8",
                stroke="#9a5f63",
                stroke_width=1,
            )
        )

    slots.append(
        TextSlot(
            id=f"slot.{prefix}.label",
            prompt="수 모형 아래의 수",
            text=str(number),
            semantic_role="number_label",
            x=x + 64,
            y=y + 53,
            font_size=12,
            anchor="middle",
            fill="#222222",
        )
    )
    return tuple(slots)


def build_problem_template() -> ProblemTemplate:
    first_model_ids = _model_slot_ids("model262", 2, 6, 2)
    second_model_ids = _model_slot_ids("model271", 2, 7, 1)

    return ProblemTemplate(
        id=PROBLEM_ID,
        title=PROBLEM_TITLE,
        canvas=Canvas(
            width=765,
            height=193,
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
                id="region.models",
                role="diagram",
                flow="absolute",
                slot_ids=(
                    "slot.model262.container",
                    *first_model_ids,
                    "slot.model271.container",
                    *second_model_ids,
                ),
            ),
            Region(
                id="region.questions",
                role="work",
                flow="absolute",
                slot_ids=(
                    "slot.question1",
                    "slot.question2",
                    "slot.question3",
                    "slot.question4",
                    "slot.answer.ones",
                    "slot.answer.regrouped_hundreds",
                    "slot.answer.regrouped_tens",
                    "slot.answer.direct_hundreds",
                    "slot.answer.total",
                ),
            ),
        ),
        slots=(
            TextSlot(
                id="slot.instruction",
                prompt="수 모형으로 덧셈을 알아보라는 안내",
                text="262+271을 수 모형으로 알아보시오.",
                semantic_role="instruction",
                x=20,
                y=14,
                font_size=14,
                fill="#222222",
            ),
            RectSlot(
                id="slot.model262.container",
                prompt="262의 수 모형을 묶는 영역",
                semantic_role="model_container",
                x=20,
                y=24,
                width=143,
                height=62,
                fill="#ffffff",
                stroke="#e36b72",
                stroke_width=1,
            ),
            *_model_slots(
                "model262",
                x=32,
                y=37,
                number=262,
                hundreds=2,
                tens=6,
                ones=2,
            ),
            RectSlot(
                id="slot.model271.container",
                prompt="271의 수 모형을 묶는 영역",
                semantic_role="model_container",
                x=188,
                y=24,
                width=141,
                height=62,
                fill="#ffffff",
                stroke="#e36b72",
                stroke_width=1,
            ),
            *_model_slots(
                "model271",
                x=190,
                y=37,
                number=271,
                hundreds=2,
                tens=7,
                ones=1,
            ),
            TextSlot(
                id="slot.question1",
                prompt="낱개 모형의 합을 묻는 첫 번째 질문",
                text="(1) 낱개 모형끼리 더하면 몇 개입니까?",
                semantic_role="subquestion",
                x=20,
                y=119,
                font_size=14,
                fill="#222222",
            ),
            TextSlot(
                id="slot.question2",
                prompt="십 모형을 받아올림한 결과를 묻는 두 번째 질문",
                text="(2) 십 모형끼리 더한 것은 백 모형 몇 개와 십 모형 몇 개가 됩니까?",
                semantic_role="subquestion",
                x=20,
                y=141,
                font_size=14,
                fill="#222222",
            ),
            TextSlot(
                id="slot.question3",
                prompt="백 모형의 직접 합을 묻는 세 번째 질문",
                text="(3) 백 모형끼리 더하면 몇 개입니까?",
                semantic_role="subquestion",
                x=20,
                y=163,
                font_size=14,
                fill="#222222",
            ),
            TextSlot(
                id="slot.question4",
                prompt="최종 덧셈 결과를 묻는 네 번째 질문",
                text="(4) 262+271은 얼마입니까?",
                semantic_role="subquestion",
                x=20,
                y=185,
                font_size=14,
                fill="#222222",
            ),
            BlankSlot(
                id="slot.answer.ones",
                prompt="(1) 낱개 모형끼리 더한 개수",
                answer_key="3",
                placeholder="개",
            ),
            BlankSlot(
                id="slot.answer.regrouped_hundreds",
                prompt="(2) 십 모형 13개를 바꾼 백 모형의 개수",
                answer_key="1",
                placeholder="개",
            ),
            BlankSlot(
                id="slot.answer.regrouped_tens",
                prompt="(2) 십 모형 13개를 바꾼 뒤 남는 십 모형의 개수",
                answer_key="3",
                placeholder="개",
            ),
            BlankSlot(
                id="slot.answer.direct_hundreds",
                prompt="(3) 두 수의 백 모형끼리 더한 개수",
                answer_key="4",
                placeholder="개",
            ),
            BlankSlot(
                id="slot.answer.total",
                prompt="(4) 262와 271의 합",
                answer_key="533",
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
            "base-ten-blocks",
            "regrouping",
            "multi-answer",
        ),
    )


PROBLEM_TEMPLATE = build_problem_template()


ANSWER = {
    "type": "multi_numeric",
    "value": [3, 1, 3, 4, 533],
    "unit": "",
    "blanks": [
        {
            "id": "slot.answer.ones",
            "type": "number",
            "value": 3,
            "unit": "개",
        },
        {
            "id": "slot.answer.regrouped_hundreds",
            "type": "number",
            "value": 1,
            "unit": "개",
        },
        {
            "id": "slot.answer.regrouped_tens",
            "type": "number",
            "value": 3,
            "unit": "개",
        },
        {
            "id": "slot.answer.direct_hundreds",
            "type": "number",
            "value": 4,
            "unit": "개",
        },
        {
            "id": "slot.answer.total",
            "type": "number",
            "value": 533,
            "unit": "",
        },
    ],
    "choices": [],
    "answer_key": [
        {"blank_id": "slot.answer.ones", "value": 3, "unit": "개"},
        {
            "blank_id": "slot.answer.regrouped_hundreds",
            "value": 1,
            "unit": "개",
        },
        {
            "blank_id": "slot.answer.regrouped_tens",
            "value": 3,
            "unit": "개",
        },
        {
            "blank_id": "slot.answer.direct_hundreds",
            "value": 4,
            "unit": "개",
        },
        {"blank_id": "slot.answer.total", "value": 533, "unit": ""},
    ],
    "sentence": (
        "(1) 3개, (2) 백 모형 1개와 십 모형 3개, "
        "(3) 4개, (4) 533입니다."
    ),
}


SEMANTIC_OVERRIDE = {
    "problem_id": PROBLEM_ID,
    "problem_type": "base_ten_model_addition_multi_answer",
    "metadata": {
        "grade": 3,
        "semester": 1,
        "subject": "수학",
        "topic": "세 자리 수의 덧셈",
        "language": "ko-KR",
        "question": "262+271을 수 모형으로 알아보시오.",
        "instruction": "같은 종류의 수 모형끼리 더하고 십 모형 10개를 백 모형 1개로 바꿉니다.",
    },
    "domain": {
        "objects": [
            {
                "id": "number.first",
                "type": "number",
                "label": "첫 번째 수",
                "value": 262,
            },
            {
                "id": "number.second",
                "type": "number",
                "label": "두 번째 수",
                "value": 271,
            },
            {
                "id": "model.first",
                "type": "base_ten_model",
                "label": "262의 수 모형",
                "hundreds": 2,
                "tens": 6,
                "ones": 2,
            },
            {
                "id": "model.second",
                "type": "base_ten_model",
                "label": "271의 수 모형",
                "hundreds": 2,
                "tens": 7,
                "ones": 1,
            },
            {
                "id": "quantity.ones_sum",
                "type": "quantity",
                "label": "낱개 모형의 합",
                "value": 3,
                "unit": "개",
            },
            {
                "id": "quantity.tens_sum_before_regrouping",
                "type": "quantity",
                "label": "받아올림 전 십 모형의 합",
                "value": 13,
                "unit": "개",
            },
            {
                "id": "quantity.regrouped_hundreds",
                "type": "quantity",
                "label": "십 모형에서 바꾼 백 모형",
                "value": 1,
                "unit": "개",
            },
            {
                "id": "quantity.remaining_tens",
                "type": "quantity",
                "label": "받아올림 뒤 남은 십 모형",
                "value": 3,
                "unit": "개",
            },
            {
                "id": "quantity.direct_hundreds_sum",
                "type": "quantity",
                "label": "두 수의 백 모형끼리 더한 수",
                "value": 4,
                "unit": "개",
            },
            {
                "id": "quantity.final_hundreds",
                "type": "quantity",
                "label": "받아올림을 포함한 백 모형의 수",
                "value": 5,
                "unit": "개",
            },
            {
                "id": "sum.total",
                "type": "number",
                "label": "262와 271의 합",
                "value": 533,
            },
        ],
        "relations": [
            {
                "id": "relation.add_ones",
                "type": "add_same_base_ten_units",
                "from_ids": ["model.first", "model.second"],
                "to_id": "quantity.ones_sum",
                "equation": "2+1=3",
            },
            {
                "id": "relation.add_and_regroup_tens",
                "type": "base_ten_regrouping",
                "from_ids": ["model.first", "model.second"],
                "to_ids": [
                    "quantity.regrouped_hundreds",
                    "quantity.remaining_tens",
                ],
                "equation": "6+7=13=10+3",
            },
            {
                "id": "relation.add_hundreds",
                "type": "add_same_base_ten_units",
                "from_ids": ["model.first", "model.second"],
                "to_id": "quantity.direct_hundreds_sum",
                "equation": "2+2=4",
            },
            {
                "id": "relation.compose_total",
                "type": "place_value_composition",
                "from_ids": [
                    "quantity.ones_sum",
                    "quantity.remaining_tens",
                    "quantity.final_hundreds",
                ],
                "to_id": "sum.total",
                "equation": "(4+1)×100+3×10+3=533",
            },
        ],
        "problem_solving": {
            "understand": {
                "given_refs": [
                    "number.first",
                    "number.second",
                    "model.first",
                    "model.second",
                ],
                "target_ref": "answer.all",
                "condition_refs": [
                    "relation.add_ones",
                    "relation.add_and_regroup_tens",
                    "relation.add_hundreds",
                    "relation.compose_total",
                ],
            },
            "plan": {
                "method": "add_base_ten_models_with_regrouping",
                "description": "낱개, 십, 백 모형끼리 더하고 십 모형 10개를 백 모형 1개로 바꿉니다.",
            },
            "execute": {
                "expected_operations": [
                    "addition",
                    "regrouping",
                    "place_value_composition",
                ],
            },
            "review": {
                "check_methods": [
                    "model_recomposition",
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
    "problem_type": "base_ten_model_addition_multi_answer",
    "inputs": {
        "target_label": "수 모형 덧셈 과정과 262+271의 결과",
        "unit": "",
        "quantities": {
            "first_number": 262,
            "second_number": 271,
            "first_model": {
                "hundreds": 2,
                "tens": 6,
                "ones": 2,
            },
            "second_model": {
                "hundreds": 2,
                "tens": 7,
                "ones": 1,
            },
        },
        "conditions": [
            "같은 종류의 수 모형끼리 더합니다.",
            "십 모형 10개는 백 모형 1개로 바꿉니다.",
            "받아올림 전 백 모형끼리 더한 개수와 최종 합을 구분합니다.",
        ],
    },
    "given": [
        {
            "ref": "number.first",
            "value": 262,
        },
        {
            "ref": "number.second",
            "value": 271,
        },
        {
            "ref": "model.first",
            "value": {
                "hundreds": 2,
                "tens": 6,
                "ones": 2,
            },
        },
        {
            "ref": "model.second",
            "value": {
                "hundreds": 2,
                "tens": 7,
                "ones": 1,
            },
        },
    ],
    "target": {
        "ref": "answer.all",
        "type": "number_list",
    },
    "method": "같은 수 모형끼리 더한 뒤 십 모형 10개를 백 모형 1개로 받아올림하여 합을 구합니다.",
    "understanding": {
        "summary": "262와 271을 나타낸 수 모형을 자리별로 더하고 받아올림하여 합을 구하는 문제입니다.",
        "facts": [
            {
                "ref": "model.first",
                "label": "262의 수 모형",
                "value": {
                    "hundreds": 2,
                    "tens": 6,
                    "ones": 2,
                },
                "unit": "",
                "source": "explicit",
            },
            {
                "ref": "model.second",
                "label": "271의 수 모형",
                "value": {
                    "hundreds": 2,
                    "tens": 7,
                    "ones": 1,
                },
                "unit": "",
                "source": "explicit",
            },
            {
                "ref": "rule.regroup_tens",
                "label": "십 모형의 받아올림 규칙",
                "value": "십 모형 10개는 백 모형 1개",
                "unit": "",
                "source": "implicit",
            },
        ],
        "unknowns": [
            {
                "ref": "quantity.ones_sum",
                "label": "낱개 모형끼리 더한 개수",
                "unit": "개",
                "source": "unknown",
            },
            {
                "ref": "quantity.regrouped_hundreds",
                "label": "십 모형을 바꾸어 얻은 백 모형의 개수",
                "unit": "개",
                "source": "unknown",
            },
            {
                "ref": "quantity.remaining_tens",
                "label": "받아올림 뒤 남은 십 모형의 개수",
                "unit": "개",
                "source": "unknown",
            },
            {
                "ref": "quantity.direct_hundreds_sum",
                "label": "백 모형끼리 직접 더한 개수",
                "unit": "개",
                "source": "unknown",
            },
            {
                "ref": "sum.total",
                "label": "262와 271의 합",
                "unit": "",
                "source": "unknown",
            },
        ],
        "relation": {
            "type": "base_ten_model_addition_with_regrouping",
            "statement": "같은 자리의 수 모형끼리 더하고 십 모형 13개 중 10개를 백 모형 1개로 바꿉니다.",
            "symbolic": "ones:2+1=3; tens:6+7=13=1 hundred+3 tens; hundreds:2+2=4; total:(4+1) hundreds+3 tens+3 ones=533",
            "uses": [
                "model.first",
                "model.second",
            ],
            "result": "answer.all",
        },
        "diagnostic_questions": [
            {
                "id": "understand.regroup_tens",
                "type": "multiple_choice",
                "prompt": "십 모형 13개를 바르게 바꾼 것은 무엇인가요?",
                "choices": [
                    "백 모형 1개와 십 모형 3개",
                    "백 모형 3개와 십 모형 1개",
                    "백 모형 1개와 십 모형 13개",
                ],
                "answer_index": 0,
            },
            {
                "id": "understand.hundreds",
                "type": "multiple_choice",
                "prompt": "받아올림을 포함한 최종 백 모형의 수는 몇 개인가요?",
                "choices": [
                    "4개",
                    "5개",
                    "6개",
                ],
                "answer_index": 1,
            },
        ],
        "student_restatement": {
            "prompt": "수 모형으로 어떻게 더해야 하나요?",
            "template": "낱개, 십, 백 모형끼리 더하고 십 모형 {regroup_count}개를 백 모형 1개로 바꿉니다.",
            "answer": "낱개, 십, 백 모형끼리 더하고 십 모형 10개를 백 모형 1개로 바꿉니다.",
        },
    },
    "plan": [
        "낱개 모형 2개와 1개를 더합니다.",
        "십 모형 6개와 7개를 더해 13개를 만듭니다.",
        "십 모형 13개를 백 모형 1개와 십 모형 3개로 바꿉니다.",
        "백 모형 2개와 2개를 더한 뒤 받아올린 백 모형 1개를 합칩니다.",
        "백 모형 5개, 십 모형 3개, 낱개 모형 3개를 수로 나타냅니다.",
    ],
    "steps": [
        {
            "id": "step.add_ones",
            "expr": "2+1",
            "value": 3,
            "explanation": "낱개 모형끼리 더하면 3개입니다.",
        },
        {
            "id": "step.add_tens",
            "expr": "6+7",
            "value": 13,
            "explanation": "십 모형끼리 더하면 13개입니다.",
        },
        {
            "id": "step.regroup_tens",
            "expr": "13 tens = 1 hundred + 3 tens",
            "value": [1, 3],
            "explanation": "십 모형 10개를 백 모형 1개로 바꾸면 백 모형 1개와 십 모형 3개가 됩니다.",
        },
        {
            "id": "step.add_direct_hundreds",
            "expr": "2+2",
            "value": 4,
            "explanation": "두 수에 처음부터 있던 백 모형끼리 더하면 4개입니다.",
        },
        {
            "id": "step.add_carried_hundred",
            "expr": "4+1",
            "value": 5,
            "explanation": "백 모형 4개에 십 모형에서 바꾼 백 모형 1개를 더하면 5개입니다.",
        },
        {
            "id": "step.compose_total",
            "expr": "5×100+3×10+3",
            "value": 533,
            "explanation": "백 모형 5개, 십 모형 3개, 낱개 모형 3개는 533입니다.",
        },
    ],
    "checks": [
        {
            "id": "check.first_model",
            "expr": "2×100+6×10+2",
            "expected": 262,
            "actual": 262,
            "pass": True,
        },
        {
            "id": "check.second_model",
            "expr": "2×100+7×10+1",
            "expected": 271,
            "actual": 271,
            "pass": True,
        },
        {
            "id": "check.inverse_subtraction",
            "expr": "533-271",
            "expected": 262,
            "actual": 262,
            "pass": True,
        },
        {
            "id": "check.column_addition",
            "expr": "262+271",
            "expected": 533,
            "actual": 533,
            "pass": True,
        },
    ],
    "answer": ANSWER,
}


SEMANTIC_ANSWER = SOLVABLE["answer"]
