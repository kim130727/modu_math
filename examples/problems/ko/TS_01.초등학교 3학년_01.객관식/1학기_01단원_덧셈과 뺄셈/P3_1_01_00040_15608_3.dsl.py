from __future__ import annotations

from modu_math.dsl import (
    Canvas,
    ProblemTemplate,
    Region,
    TextSlot,
)


PROBLEM_ID = "P3_1_01_00040_15608_3"
PROBLEM_TITLE = "합이 더 큰 덧셈식 (3)"


ANSWER = {
    "type": "choice",
    "value": 2,
    "unit": "",
    "target_ref": "choice.option_2",
    "derived_from": "step.select_largest_sum",
}


SEMANTIC_OVERRIDE = {
    "problem_id": PROBLEM_ID,
    "problem_type": "multiple_choice_largest_addition_sum",
    "metadata": {
        "grade": 3,
        "semester": 1,
        "subject": "수학",
        "topic": "세 자리 수의 덧셈",
        "language": "ko-KR",
        "question": "다음 중 합이 더 큰 것은 어느 것입니까?",
    },
    "domain": {
        "objects": [
            {
                "id": "choice.option_1",
                "type": "arithmetic_choice",
                "label": "① 140+550",
                "expression": "140 + 550",
                "value": 690,
            },
            {
                "id": "choice.option_2",
                "type": "arithmetic_choice",
                "label": "② 545+235",
                "expression": "545 + 235",
                "value": 780,
            },
        ],
        "relations": [
            {
                "id": "relation.option_2_has_largest_sum",
                "type": "maximum_of",
                "from_id": "choice.option_2",
                "to_id": "choice.option_1",
                "subject": "choice.option_2",
                "objects": [
                    "choice.option_1",
                    "choice.option_2",
                ],
            },
        ],
    },
    "answer": ANSWER,
}


SOLVABLE = {
    "schema": "modu.solvable.v1.2",
    "problem_id": PROBLEM_ID,
    "problem_type": "multiple_choice_largest_addition_sum",
    "inputs": {
        "target_label": "합이 더 큰 덧셈식의 번호",
        "unit": "",
        "options": [
            {"number": 1, "expression": "140 + 550"},
            {"number": 2, "expression": "545 + 235"},
        ],
    },
    "given": [
        {
            "ref": "choice.option_1",
            "value": {"number": 1, "expression": "140 + 550"},
        },
        {
            "ref": "choice.option_2",
            "value": {"number": 2, "expression": "545 + 235"},
        },
    ],
    "target": {
        "ref": "choice.option_2",
        "type": "choice",
    },
    "understanding": {
        "summary": "두 덧셈식의 합을 각각 구하고, 그중 더 큰 합을 가진 보기를 찾는 문제입니다.",
        "facts": [
            {
                "ref": "choice.option_1",
                "label": "첫 번째 덧셈식",
                "value": "140 + 550",
                "unit": "",
                "source": "explicit",
            },
            {
                "ref": "choice.option_2",
                "label": "두 번째 덧셈식",
                "value": "545 + 235",
                "unit": "",
                "source": "explicit",
            },
        ],
        "unknowns": [
            {
                "ref": "choice.option_2",
                "label": "합이 더 큰 덧셈식의 번호",
                "unit": "",
                "source": "unknown",
            },
        ],
        "relation": {
            "type": "evaluate_and_compare",
            "statement": "각 덧셈식의 값을 계산한 뒤 더 큰 값을 가진 보기를 선택합니다.",
            "symbolic": "max(140+550, 545+235)",
            "uses": ["choice.option_1", "choice.option_2"],
            "result": "choice.option_2",
        },
    },
    "method": "두 덧셈식의 합을 각각 계산한 다음 결과를 비교하여 더 큰 합을 고릅니다.",
    "plan": [
        "각 보기의 덧셈을 계산합니다.",
        "계산 결과 690과 780을 비교합니다.",
        "더 큰 값 780에 해당하는 ②를 선택합니다.",
    ],
    "steps": [
        {
            "id": "step.calculate_option_1",
            "expr": "140 + 550",
            "value": 690,
            "explanation": "①의 합은 690입니다.",
        },
        {
            "id": "step.calculate_option_2",
            "expr": "545 + 235",
            "value": 780,
            "explanation": "②의 합은 780입니다.",
        },
        {
            "id": "step.select_largest_sum",
            "expr": "max(690, 780)",
            "value": 780,
            "explanation": "780이 더 크므로 ②를 선택합니다.",
        },
    ],
    "checks": [
        {
            "id": "check.option_2_is_maximum",
            "expr": "780 > 690",
            "expected": True,
            "actual": True,
            "pass": True,
        },
    ],
    "answer": ANSWER,
}


SEMANTIC_ANSWER = SOLVABLE["answer"]


def build_problem_template() -> ProblemTemplate:
    return ProblemTemplate(
        id=PROBLEM_ID,
        title=PROBLEM_TITLE,
        canvas=Canvas(
            width=400,
            height=130,
            coordinate_mode="logical",
        ),
        regions=(
            Region(
                id="region.stem",
                role="stem",
                flow="absolute",
                slot_ids=("slot.question",),
            ),
            Region(
                id="region.choices",
                role="diagram",
                flow="absolute",
                slot_ids=(
                    "slot.choice_1.number",
                    "slot.choice_1.expression",
                    "slot.choice_2.number",
                    "slot.choice_2.expression",
                ),
            ),
        ),
        slots=(
            TextSlot(
                id="slot.question",
                prompt="",
                text="다음 중 합이 더 큰 것은 어느 것입니까?",
                style_role="question",
                x=24,
                y=28,
                font_size=22,
                fill="#222222",
            ),
            TextSlot(
                id="slot.choice_1.number",
                prompt="",
                text="①",
                style_role="diagram_label",
                semantic_role="canvas",
                x=40,
                y=80,
                font_size=22,
                fill="#2F80C9",
            ),
            TextSlot(
                id="slot.choice_1.expression",
                prompt="",
                text="140+550",
                style_role="diagram_label",
                semantic_role="canvas",
                x=70,
                y=80,
                font_size=22,
                fill="#111111",
            ),
            TextSlot(
                id="slot.choice_2.number",
                prompt="",
                text="②",
                style_role="diagram_label",
                semantic_role="canvas",
                x=210,
                y=80,
                font_size=22,
                fill="#2F80C9",
            ),
            TextSlot(
                id="slot.choice_2.expression",
                prompt="",
                text="545+235",
                style_role="diagram_label",
                semantic_role="canvas",
                x=240,
                y=80,
                font_size=22,
                fill="#111111",
            ),
        ),
    )


PROBLEM_TEMPLATE = build_problem_template()
