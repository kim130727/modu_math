from __future__ import annotations

from modu_math.dsl import (
    BlankSlot,
    Canvas,
    ProblemTemplate,
    Region,
    TextBoxSlot,
    TextSlot,
)


PROBLEM_ID = "P3_1_01_00040_15630"
PROBLEM_TITLE = "차가 123인 두 수 찾기"


def build_problem_template() -> ProblemTemplate:
    return ProblemTemplate(
        id=PROBLEM_ID,
        title=PROBLEM_TITLE,
        canvas=Canvas(
            width=619,
            height=133,
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
                role="choices",
                flow="absolute",
                slot_ids=(
                    "slot.choice1",
                    "slot.choice2",
                    "slot.choice3",
                    "slot.choice4",
                    "slot.choice5",
                    "slot.answer",
                ),
            ),
        ),
        slots=(
            TextBoxSlot(
                id="slot.question",
                prompt="차가 123인 두 수를 고르는 질문",
                text="다음 두 수의 차가 123인 것은 어느 것입니까?",
                semantic_role="question",
                x=20,
                y=2,
                width=430,
                height=22,
                font_size=14,
                font_family="Noto Sans KR",
                fill="#111111",
                align="left",
                valign="top",
            ),
            TextSlot(
                id="slot.choice1",
                prompt="첫 번째 선택지",
                text="① 647, 341",
                semantic_role="choice",
                x=20,
                y=38,
                font_size=14,
                font_family="Noto Sans KR",
                fill="#111111",
            ),
            TextSlot(
                id="slot.choice2",
                prompt="두 번째 선택지",
                text="② 488, 227",
                semantic_role="choice",
                x=20,
                y=60,
                font_size=14,
                font_family="Noto Sans KR",
                fill="#111111",
            ),
            TextSlot(
                id="slot.choice3",
                prompt="세 번째 선택지",
                text="③ 847, 740",
                semantic_role="choice",
                x=20,
                y=82,
                font_size=14,
                font_family="Noto Sans KR",
                fill="#111111",
            ),
            TextSlot(
                id="slot.choice4",
                prompt="네 번째 선택지",
                text="④ 528, 405",
                semantic_role="choice",
                x=20,
                y=104,
                font_size=14,
                font_family="Noto Sans KR",
                fill="#111111",
            ),
            TextSlot(
                id="slot.choice5",
                prompt="다섯 번째 선택지",
                text="⑤ 386, 223",
                semantic_role="choice",
                x=20,
                y=126,
                font_size=14,
                font_family="Noto Sans KR",
                fill="#111111",
            ),
            BlankSlot(
                id="slot.answer",
                prompt="정답 번호",
                answer_key="4",
                placeholder="번",
            ),
        ),
        diagrams=(),
        groups=(),
        constraints=(),
        tags=(
            "grade-3",
            "subtraction",
            "three-digit-subtraction",
            "multiple-choice",
            "difference",
        ),
    )


PROBLEM_TEMPLATE = build_problem_template()


ANSWER = {
    "type": "multiple_choice",
    "value": 4,
    "unit": "",
    "choice_index": 3,
    "choice_label": "④",
    "choice_value": [528, 405],
    "target_ref": "choice.4",
    "derived_from": "step.evaluate_choice4",
}


SEMANTIC_OVERRIDE = {
    "problem_id": PROBLEM_ID,
    "problem_type": "multiple_choice_difference_identification",
    "metadata": {
        "grade": 3,
        "semester": 1,
        "subject": "수학",
        "topic": "세 자리 수의 뺄셈",
        "language": "ko-KR",
        "question": "다음 두 수의 차가 123인 것은 어느 것입니까?",
        "instruction": "각 선택지에서 큰 수에서 작은 수를 빼어 차가 123인지 확인합니다.",
    },
    "domain": {
        "objects": [
            {
                "id": "target.difference",
                "type": "number",
                "label": "목표 차",
                "value": 123,
            },
            {
                "id": "choice.1",
                "type": "number_pair",
                "label": "①",
                "values": [647, 341],
                "difference": 306,
            },
            {
                "id": "choice.2",
                "type": "number_pair",
                "label": "②",
                "values": [488, 227],
                "difference": 261,
            },
            {
                "id": "choice.3",
                "type": "number_pair",
                "label": "③",
                "values": [847, 740],
                "difference": 107,
            },
            {
                "id": "choice.4",
                "type": "number_pair",
                "label": "④",
                "values": [528, 405],
                "difference": 123,
            },
            {
                "id": "choice.5",
                "type": "number_pair",
                "label": "⑤",
                "values": [386, 223],
                "difference": 163,
            },
        ],
        "relations": [
            {
                "id": "relation.choice_differences",
                "type": "subtraction_comparison",
                "from_ids": [
                    "choice.1",
                    "choice.2",
                    "choice.3",
                    "choice.4",
                    "choice.5",
                ],
                "to_id": "target.difference",
                "matching_id": "choice.4",
            },
            {
                "id": "relation.correct_choice",
                "type": "difference_equals",
                "from_id": "choice.4",
                "to_id": "target.difference",
                "equation": "528 - 405 = 123",
            },
        ],
        "problem_solving": {
            "understand": {
                "given_refs": [
                    "target.difference",
                    "choice.1",
                    "choice.2",
                    "choice.3",
                    "choice.4",
                    "choice.5",
                ],
                "target_ref": "choice.4",
                "condition_refs": ["relation.choice_differences"],
            },
            "plan": {
                "method": "evaluate_each_difference",
                "description": "각 쌍에서 큰 수에서 작은 수를 빼고 결과를 123과 비교합니다.",
            },
            "execute": {
                "expected_operations": [
                    "647-341",
                    "488-227",
                    "847-740",
                    "528-405",
                    "386-223",
                ],
            },
            "review": {
                "check_methods": [
                    "inverse_addition",
                    "uniqueness_check",
                ],
            },
        },
    },
    "answer": ANSWER,
}


SOLVABLE = {
    "schema": "modu.solvable.v1.2",
    "problem_id": PROBLEM_ID,
    "problem_type": "multiple_choice_difference_identification",
    "inputs": {
        "target_label": "차가 123인 두 수의 선택지 번호",
        "unit": "",
        "target_difference": 123,
        "choices": [
            {"number": 1, "values": [647, 341]},
            {"number": 2, "values": [488, 227]},
            {"number": 3, "values": [847, 740]},
            {"number": 4, "values": [528, 405]},
            {"number": 5, "values": [386, 223]},
        ],
        "conditions": [
            "각 선택지의 앞 수가 뒤 수보다 큽니다.",
            "두 수의 차는 큰 수에서 작은 수를 빼서 구합니다.",
            "계산 결과가 123인 선택지는 하나입니다.",
        ],
    },
    "given": [
        {
            "ref": "target.difference",
            "value": 123,
        },
        {
            "ref": "choices.number_pairs",
            "value": [
                [647, 341],
                [488, 227],
                [847, 740],
                [528, 405],
                [386, 223],
            ],
        },
    ],
    "target": {
        "ref": "choice.4",
        "type": "choice_number",
    },
    "method": "각 선택지에서 큰 수에서 작은 수를 빼고, 차가 123인 선택지를 고릅니다.",
    "understanding": {
        "summary": "다섯 개의 두 수 쌍 가운데 차가 123인 쌍의 선택지 번호를 찾는 문제입니다.",
        "facts": [
            {
                "ref": "target.difference",
                "label": "찾아야 하는 두 수의 차",
                "value": 123,
                "unit": "",
                "source": "explicit",
            },
            {
                "ref": "choices.number_pairs",
                "label": "다섯 선택지의 두 수",
                "value": [
                    [647, 341],
                    [488, 227],
                    [847, 740],
                    [528, 405],
                    [386, 223],
                ],
                "unit": "",
                "source": "explicit",
            },
        ],
        "unknowns": [
            {
                "ref": "choice.4",
                "label": "차가 123인 선택지 번호",
                "unit": "",
                "source": "unknown",
            },
        ],
        "relation": {
            "type": "difference_matching",
            "statement": "각 선택지의 큰 수에서 작은 수를 뺀 값이 123과 같은지 비교합니다.",
            "symbolic": "앞 수 - 뒤 수 = 123",
            "uses": [
                "target.difference",
                "choices.number_pairs",
            ],
            "result": "choice.4",
        },
        "diagnostic_questions": [
            {
                "id": "understand.operation",
                "type": "multiple_choice",
                "prompt": "두 수의 차를 구하려면 어떤 계산을 해야 하나요?",
                "choices": [
                    "큰 수에서 작은 수를 뺍니다.",
                    "두 수를 더합니다.",
                    "작은 수에서 큰 수를 뺍니다.",
                ],
                "answer_index": 0,
            },
            {
                "id": "understand.match",
                "type": "multiple_choice",
                "prompt": "계산 결과가 얼마인 선택지를 찾아야 하나요?",
                "choices": [
                    "107",
                    "123",
                    "163",
                ],
                "answer_index": 1,
            },
        ],
        "student_restatement": {
            "prompt": "이 문제를 어떤 방법으로 풀어야 하나요?",
            "template": "각 선택지의 두 수를 빼서 차가 {target_difference}인 것을 찾습니다.",
            "answer": "각 선택지의 두 수를 빼서 차가 123인 것을 찾습니다.",
        },
    },
    "plan": [
        "각 선택지에서 앞의 큰 수에서 뒤의 작은 수를 뺍니다.",
        "각 차를 123과 비교합니다.",
        "차가 123인 선택지 번호를 고릅니다.",
        "정답 쌍에 123을 다시 더해 검산합니다.",
    ],
    "steps": [
        {
            "id": "step.evaluate_choice1",
            "expr": "647 - 341",
            "value": 306,
            "explanation": "①의 차는 306이므로 123이 아닙니다.",
        },
        {
            "id": "step.evaluate_choice2",
            "expr": "488 - 227",
            "value": 261,
            "explanation": "②의 차는 261이므로 123이 아닙니다.",
        },
        {
            "id": "step.evaluate_choice3",
            "expr": "847 - 740",
            "value": 107,
            "explanation": "③의 차는 107이므로 123이 아닙니다.",
        },
        {
            "id": "step.evaluate_choice4",
            "expr": "528 - 405",
            "value": 123,
            "explanation": "④의 차는 123이므로 조건을 만족합니다.",
        },
        {
            "id": "step.evaluate_choice5",
            "expr": "386 - 223",
            "value": 163,
            "explanation": "⑤의 차는 163이므로 123이 아닙니다.",
        },
        {
            "id": "step.select_answer",
            "expr": "difference(choice) = 123",
            "value": 4,
            "explanation": "차가 123인 것은 ④뿐이므로 정답은 ④입니다.",
        },
    ],
    "checks": [
        {
            "id": "check.inverse_addition",
            "expr": "405 + 123",
            "expected": 528,
            "actual": 528,
            "pass": True,
        },
        {
            "id": "check.uniqueness",
            "expr": "[306, 261, 107, 123, 163]에서 123의 개수",
            "expected": 1,
            "actual": 1,
            "pass": True,
        },
        {
            "id": "check.answer_pair",
            "expr": "528 - 405",
            "expected": 123,
            "actual": 123,
            "pass": True,
        },
    ],
    "answer": ANSWER,
}


SEMANTIC_ANSWER = SOLVABLE["answer"]
