from __future__ import annotations

from modu_math.dsl import (
    BlankSlot,
    Canvas,
    ProblemTemplate,
    Region,
    TextBoxSlot,
)


PROBLEM_ID = "P3_1_01_00040_15608"
PROBLEM_TITLE = "합이 가장 큰 덧셈식"


ANSWER = {
    "type": "choice",
    "value": 5,
    "unit": "",
    "target_ref": "choice.option_5",
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
        "question": "다음 중 합이 가장 큰 것은 어느 것입니까?",
    },
    "domain": {
        "objects": [
            {
                "id": "choice.option_1",
                "type": "arithmetic_choice",
                "label": "① 530+140",
                "expression": "530 + 140",
                "value": 670,
            },
            {
                "id": "choice.option_2",
                "type": "arithmetic_choice",
                "label": "② 420+220",
                "expression": "420 + 220",
                "value": 640,
            },
            {
                "id": "choice.option_3",
                "type": "arithmetic_choice",
                "label": "③ 610+100",
                "expression": "610 + 100",
                "value": 710,
            },
            {
                "id": "choice.option_4",
                "type": "arithmetic_choice",
                "label": "④ 140+550",
                "expression": "140 + 550",
                "value": 690,
            },
            {
                "id": "choice.option_5",
                "type": "arithmetic_choice",
                "label": "⑤ 545+235",
                "expression": "545 + 235",
                "value": 780,
            },
        ],
        "relations": [
            {
                "id": "relation.option_5_has_largest_sum",
                "type": "maximum_of",
                "subject": "choice.option_5",
                "objects": [
                    "choice.option_1",
                    "choice.option_2",
                    "choice.option_3",
                    "choice.option_4",
                    "choice.option_5",
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
        "target_label": "합이 가장 큰 덧셈식의 번호",
        "unit": "",
        "options": [
            {"number": 1, "expression": "530 + 140"},
            {"number": 2, "expression": "420 + 220"},
            {"number": 3, "expression": "610 + 100"},
            {"number": 4, "expression": "140 + 550"},
            {"number": 5, "expression": "545 + 235"},
        ],
    },
    "given": [
        {
            "ref": "choice.option_1",
            "value": {"number": 1, "expression": "530 + 140"},
        },
        {
            "ref": "choice.option_2",
            "value": {"number": 2, "expression": "420 + 220"},
        },
        {
            "ref": "choice.option_3",
            "value": {"number": 3, "expression": "610 + 100"},
        },
        {
            "ref": "choice.option_4",
            "value": {"number": 4, "expression": "140 + 550"},
        },
        {
            "ref": "choice.option_5",
            "value": {"number": 5, "expression": "545 + 235"},
        },
    ],
    "target": {
        "ref": "choice.option_5",
        "type": "choice",
    },
    "understanding": {
        "summary": "다섯 덧셈식의 합을 각각 구하고, 그중 가장 큰 합을 가진 보기를 찾는 문제입니다.",
        "facts": [
            {
                "ref": "choice.option_1",
                "label": "첫 번째 덧셈식",
                "value": "530 + 140",
                "unit": "",
                "source": "explicit",
            },
            {
                "ref": "choice.option_2",
                "label": "두 번째 덧셈식",
                "value": "420 + 220",
                "unit": "",
                "source": "explicit",
            },
            {
                "ref": "choice.option_3",
                "label": "세 번째 덧셈식",
                "value": "610 + 100",
                "unit": "",
                "source": "explicit",
            },
            {
                "ref": "choice.option_4",
                "label": "네 번째 덧셈식",
                "value": "140 + 550",
                "unit": "",
                "source": "explicit",
            },
            {
                "ref": "choice.option_5",
                "label": "다섯 번째 덧셈식",
                "value": "545 + 235",
                "unit": "",
                "source": "explicit",
            },
        ],
        "unknowns": [
            {
                "ref": "choice.option_5",
                "label": "합이 가장 큰 덧셈식의 번호",
                "unit": "",
                "source": "unknown",
            },
        ],
        "relation": {
            "type": "evaluate_and_compare",
            "statement": "각 덧셈식의 값을 계산한 뒤 가장 큰 값을 가진 보기를 선택합니다.",
            "symbolic": "max(530+140, 420+220, 610+100, 140+550, 545+235)",
            "uses": [
                "choice.option_1",
                "choice.option_2",
                "choice.option_3",
                "choice.option_4",
                "choice.option_5",
            ],
            "result": "choice.option_5",
        },
        "diagnostic_questions": [
            {
                "id": "understand.target",
                "type": "multiple_choice",
                "prompt": "이 문제에서 찾아야 하는 것은 무엇인가요?",
                "choices": [
                    "가장 작은 덧셈식의 합",
                    "합이 가장 큰 덧셈식",
                    "첫 번째 덧셈식의 합",
                ],
                "answer_index": 1,
            },
            {
                "id": "understand.method",
                "type": "multiple_choice",
                "prompt": "가장 정확한 해결 방법은 무엇인가요?",
                "choices": [
                    "각 덧셈식의 합을 구해 비교합니다.",
                    "첫째 수만 비교합니다.",
                    "둘째 수만 비교합니다.",
                ],
                "answer_index": 0,
            },
        ],
        "student_restatement": {
            "prompt": "문제의 요지를 말해 볼까요?",
            "template": "다섯 덧셈식의 합을 구해 가장 큰 합을 가진 보기를 찾습니다.",
            "answer": "각 보기의 합을 계산하고 가장 큰 합인 보기를 고릅니다.",
        },
    },
    "method": "다섯 덧셈식의 합을 각각 계산한 다음 결과를 비교하여 가장 큰 합을 고릅니다.",
    "plan": [
        "각 보기의 덧셈을 계산합니다.",
        "계산 결과 670, 640, 710, 690, 780을 비교합니다.",
        "가장 큰 값 780에 해당하는 ⑤를 선택합니다.",
    ],
    "steps": [
        {
            "id": "step.calculate_option_1",
            "expr": "530 + 140",
            "value": 670,
            "explanation": "①의 합은 670입니다.",
        },
        {
            "id": "step.calculate_option_2",
            "expr": "420 + 220",
            "value": 640,
            "explanation": "②의 합은 640입니다.",
        },
        {
            "id": "step.calculate_option_3",
            "expr": "610 + 100",
            "value": 710,
            "explanation": "③의 합은 710입니다.",
        },
        {
            "id": "step.calculate_option_4",
            "expr": "140 + 550",
            "value": 690,
            "explanation": "④의 합은 690입니다.",
        },
        {
            "id": "step.calculate_option_5",
            "expr": "545 + 235",
            "value": 780,
            "explanation": "⑤의 합은 780입니다.",
        },
        {
            "id": "step.select_largest_sum",
            "expr": "max(670, 640, 710, 690, 780)",
            "value": 780,
            "explanation": "780이 가장 크므로 ⑤를 선택합니다.",
        },
    ],
    "checks": [
        {
            "id": "check.option_5_addition",
            "expr": "545 + 235",
            "expected": 780,
            "actual": 780,
            "pass": True,
        },
        {
            "id": "check.option_5_is_maximum",
            "expr": "780 > 670 and 780 > 640 and 780 > 710 and 780 > 690",
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
            width=900,
            height=300,
            coordinate_mode="logical",
        ),
        regions=(
            Region(
                id="region.stem",
                role="stem",
                flow="absolute",
                slot_ids=(
                    "slot.question",
                    "slot.option_1",
                    "slot.option_2",
                    "slot.option_3",
                    "slot.option_4",
                    "slot.option_5",
                    "slot.answer",
                ),
            ),
        ),
        slots=(
            TextBoxSlot(
                id="slot.question",
                x=20,
                y=12,
                width=860,
                height=34,
                text="다음 중 합이 가장 큰 것은 어느 것입니까?",
                font_size=21,
                font_family="Noto Sans KR",
                fill="#202124",
                align="left",
                valign="middle",
            ),
            TextBoxSlot(
                id="slot.option_1",
                x=20,
                y=48,
                width=300,
                height=30,
                text="① 530+140",
                font_size=21,
                font_family="Noto Sans KR",
                fill="#202124",
                align="left",
                valign="middle",
            ),
            TextBoxSlot(
                id="slot.option_2",
                x=20,
                y=80,
                width=300,
                height=30,
                text="② 420+220",
                font_size=21,
                font_family="Noto Sans KR",
                fill="#202124",
                align="left",
                valign="middle",
            ),
            TextBoxSlot(
                id="slot.option_3",
                x=20,
                y=112,
                width=300,
                height=30,
                text="③ 610+100",
                font_size=21,
                font_family="Noto Sans KR",
                fill="#202124",
                align="left",
                valign="middle",
            ),
            TextBoxSlot(
                id="slot.option_4",
                x=20,
                y=144,
                width=300,
                height=30,
                text="④ 140+550",
                font_size=21,
                font_family="Noto Sans KR",
                fill="#202124",
                align="left",
                valign="middle",
            ),
            TextBoxSlot(
                id="slot.option_5",
                x=20,
                y=176,
                width=300,
                height=30,
                text="⑤ 545+235",
                font_size=21,
                font_family="Noto Sans KR",
                fill="#202124",
                align="left",
                valign="middle",
            ),
            BlankSlot(
                id="slot.answer",
                prompt="정답 번호",
                answer_key="5",
                placeholder="번호",
            ),
        ),
    )


PROBLEM_TEMPLATE = build_problem_template()
