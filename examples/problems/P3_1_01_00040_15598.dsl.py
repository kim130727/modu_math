from __future__ import annotations

from modu_math.dsl import (
    BlankSlot,
    Canvas,
    LineSlot,
    ProblemTemplate,
    RectSlot,
    Region,
    TextSlot,
)


PROBLEM_ID = "P3_1_01_00040_15598"
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
            id=f"slot.{prefix}.label",
            prompt="",
            text=label,
            style_role="label",
            x=x,
            y=78,
            font_size=22,
            fill="#111111",
        ),
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
            id=f"slot.{prefix}.box.ones",
            prompt="",
            x=x + 104,
            y=157,
            width=28,
            height=27,
            fill="#ffffff",
            stroke="#111111",
            stroke_width=1,
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
        "slot.calculation.1.label",
        "slot.calculation.1.top",
        "slot.calculation.1.plus",
        "slot.calculation.1.bottom",
        "slot.calculation.1.line.top",
        "slot.calculation.1.box.ones",
        "slot.calculation.1.box.tens",
        "slot.calculation.1.box.hundreds",
        "slot.calculation.1.line.bottom",
        "slot.calculation.1.box.total",
    )
    calculation_2_ids = (
        "slot.calculation.2.label",
        "slot.calculation.2.top",
        "slot.calculation.2.plus",
        "slot.calculation.2.bottom",
        "slot.calculation.2.line.top",
        "slot.calculation.2.box.ones",
        "slot.calculation.2.box.tens",
        "slot.calculation.2.box.hundreds",
        "slot.calculation.2.line.bottom",
        "slot.calculation.2.box.total",
    )

    return ProblemTemplate(
        id=PROBLEM_ID,
        title=PROBLEM_TITLE,
        canvas=Canvas(
            width=760,
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
            Region(
                id="region.calculation.2",
                role="body",
                flow="absolute",
                slot_ids=calculation_2_ids,
            ),
        ),
        slots=(
            TextSlot(
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
            *_expanded_addition_slots(
                prefix="calculation.2",
                label="(2)",
                x=225,
                top="386",
                bottom="211",
            ),
            BlankSlot(
                id="slot.answer.1.ones",
                prompt="(1) 일의 자리 부분합",
                answer_key="9",
                placeholder="수",
            ),
            BlankSlot(
                id="slot.answer.1.tens",
                prompt="(1) 십의 자리 부분합",
                answer_key="50",
                placeholder="수",
            ),
            BlankSlot(
                id="slot.answer.1.hundreds",
                prompt="(1) 백의 자리 부분합",
                answer_key="700",
                placeholder="수",
            ),
            BlankSlot(
                id="slot.answer.1.total",
                prompt="(1) 합",
                answer_key="759",
                placeholder="수",
            ),
            BlankSlot(
                id="slot.answer.2.ones",
                prompt="(2) 일의 자리 부분합",
                answer_key="7",
                placeholder="수",
            ),
            BlankSlot(
                id="slot.answer.2.tens",
                prompt="(2) 십의 자리 부분합",
                answer_key="90",
                placeholder="수",
            ),
            BlankSlot(
                id="slot.answer.2.hundreds",
                prompt="(2) 백의 자리 부분합",
                answer_key="500",
                placeholder="수",
            ),
            BlankSlot(
                id="slot.answer.2.total",
                prompt="(2) 합",
                answer_key="597",
                placeholder="수",
            ),
        ),
    )


PROBLEM_TEMPLATE = build_problem_template()


ANSWER_VALUES = [9, 50, 700, 759, 7, 90, 500, 597]

ANSWER = {
    "type": "multi_numeric",
    "value": ANSWER_VALUES,
    "unit": "",
    "values": [
        {"value": 9, "unit": "", "target_ref": "answer.1.ones"},
        {"value": 50, "unit": "", "target_ref": "answer.1.tens"},
        {"value": 700, "unit": "", "target_ref": "answer.1.hundreds"},
        {"value": 759, "unit": "", "target_ref": "answer.1.total"},
        {"value": 7, "unit": "", "target_ref": "answer.2.ones"},
        {"value": 90, "unit": "", "target_ref": "answer.2.tens"},
        {"value": 500, "unit": "", "target_ref": "answer.2.hundreds"},
        {"value": 597, "unit": "", "target_ref": "answer.2.total"},
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
                "id": "calculation.2",
                "type": "expanded_addition",
                "label": "두 번째 덧셈",
                "addends": [386, 211],
            },
            {
                "id": "answer.values",
                "type": "number_list",
                "label": "두 덧셈의 자리별 부분합과 전체 합",
            },
        ],
        "relations": [
            {
                "id": "relation.calculation_1_expansion",
                "type": "sum_by_place_value",
                "subject": "calculation.1",
                "result": "answer.values",
            },
            {
                "id": "relation.calculation_2_expansion",
                "type": "sum_by_place_value",
                "subject": "calculation.2",
                "result": "answer.values",
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
                    "relation.calculation_1_expansion",
                    "relation.calculation_2_expansion",
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
        "target_label": "두 덧셈의 자리별 부분합과 전체 합",
        "unit": "",
        "calculations": [
            {
                "id": "calculation.1",
                "addends": [217, 542],
            },
            {
                "id": "calculation.2",
                "addends": [386, 211],
            },
        ],
        "answer_order": [
            "1.ones",
            "1.tens",
            "1.hundreds",
            "1.total",
            "2.ones",
            "2.tens",
            "2.hundreds",
            "2.total",
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
        {
            "ref": "calculation.2",
            "value": {
                "operator": "+",
                "left": 386,
                "right": 211,
            },
        },
    ],
    "target": {
        "ref": "answer.values",
        "type": "number_list",
    },
    "understanding": {
        "summary": (
            "두 덧셈에서 일의 자리, 십의 자리, 백의 자리의 부분합을 "
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
            {
                "ref": "calculation.2",
                "label": "두 번째 계산",
                "value": "386 + 211",
                "unit": "",
                "source": "explicit",
            },
        ],
        "unknowns": [
            {
                "ref": "answer.values",
                "label": "여덟 빈칸에 들어갈 수",
                "unit": "",
            },
        ],
        "relation": {
            "type": "expanded_addition_by_place_value",
            "statement": (
                "각 덧셈을 일의 자리 부분합, 십의 자리 부분합, 백의 자리 부분합으로 "
                "나누고 세 부분합을 더하여 전체 합을 구합니다."
            ),
            "symbolic": (
                "(217 + 542) = (7 + 2) + (10 + 40) + (200 + 500); "
                "(386 + 211) = (6 + 1) + (80 + 10) + (300 + 200)"
            ),
            "uses": [
                "calculation.1",
                "calculation.2",
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
        "두 번째 덧셈도 같은 방법으로 자리별 부분합과 전체 합을 구합니다.",
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
            "id": "step.2.ones",
            "expr": "6 + 1",
            "value": 7,
            "explanation": "386과 211의 일의 자리끼리 더합니다.",
        },
        {
            "id": "step.2.tens",
            "expr": "80 + 10",
            "value": 90,
            "explanation": "십의 자리 숫자가 나타내는 값 80과 10을 더합니다.",
        },
        {
            "id": "step.2.hundreds",
            "expr": "300 + 200",
            "value": 500,
            "explanation": "백의 자리 숫자가 나타내는 값 300과 200을 더합니다.",
        },
        {
            "id": "step.2.total",
            "expr": "7 + 90 + 500",
            "value": 597,
            "explanation": "세 자리의 부분합을 모두 더합니다.",
        },
        {
            "id": "step.collect_answers",
            "expr": "[9, 50, 700, 759, 7, 90, 500, 597]",
            "value": ANSWER_VALUES,
            "explanation": "빈칸의 위에서 아래 순서대로 두 계산의 답을 정리합니다.",
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
        {
            "id": "check.2.partial_sum",
            "expr": "7 + 90 + 500",
            "expected": 597,
            "actual": 597,
            "pass": True,
        },
        {
            "id": "check.2.direct_addition",
            "expr": "386 + 211",
            "expected": 597,
            "actual": 597,
            "pass": True,
        },
    ],
    "answer": ANSWER,
}


SEMANTIC_ANSWER = SOLVABLE["answer"]
