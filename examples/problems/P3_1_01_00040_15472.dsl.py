from __future__ import annotations

from modu_math.dsl import (
    BlankSlot,
    Canvas,
    ProblemTemplate,
    Region,
    TextBoxSlot,
)


PROBLEM_ID = "P3_1_01_00040_15472"
PROBLEM_TITLE = "합이 749가 되는 두 수 찾기"


def build_problem_template() -> ProblemTemplate:
    return ProblemTemplate(
        id=PROBLEM_ID,
        title=PROBLEM_TITLE,
        canvas=Canvas(
            width=900,
            height=230,
            coordinate_mode="logical",
        ),
        regions=(
            Region(
                id="region.stem",
                role="stem",
                flow="vertical",
                slot_ids=(
                    "slot.instruction",
                    "slot.options",
                    "slot.equation",
                ),
            ),
        ),
        slots=(
            TextBoxSlot(
                id="slot.instruction",
                x=24,
                y=18,
                width=840,
                height=35,
                text="다음 <보기>의 수들을 빈칸에 알맞게 써넣으시오.",
                font_size=22,
                font_family="Noto Sans KR",
                fill="#202124",
                line_height=1.3,
                align="left",
                valign="top",
            ),
            TextBoxSlot(
                id="slot.options",
                x=24,
                y=58,
                width=840,
                height=52,
                text="<보기>    325,   532,   334,   985,   415",
                font_size=22,
                font_family="Noto Sans KR",
                fill="#202124",
                line_height=1.3,
                align="left",
                valign="middle",
            ),
            TextBoxSlot(
                id="slot.equation",
                x=24,
                y=130,
                width=360,
                height=45,
                text="(       )+(       )=749",
                font_size=24,
                font_family="Noto Sans KR",
                fill="#202124",
                line_height=1.3,
                align="left",
                valign="middle",
            ),
            BlankSlot(
                id="slot.answer.first",
                prompt="첫 번째 빈칸",
                answer_key="334",
                placeholder="수",
            ),
            BlankSlot(
                id="slot.answer.second",
                prompt="두 번째 빈칸",
                answer_key="415",
                placeholder="수",
            ),
        ),
    )


PROBLEM_TEMPLATE = build_problem_template()


ANSWER = {
    "type": "multi_numeric",
    "value": [334, 415],
    "unit": "",
    "values": [
        {
            "value": 334,
            "unit": "",
            "target_ref": "answer.first_blank",
        },
        {
            "value": 415,
            "unit": "",
            "target_ref": "answer.second_blank",
        },
    ],
    "derived_from": "step.select_pair",
}


SEMANTIC_OVERRIDE = {
    "problem_id": PROBLEM_ID,
    "problem_type": "multi_numeric_answer_select_addends_problem",
    "metadata": {
        "language": "ko-KR",
        "question": "두 빈칸에 들어갈 수를 구합니다.",
        "instruction": "<보기>의 수 중 합이 749가 되는 두 수를 고릅니다.",
    },
    "domain": {
        "objects": [
            {
                "id": "set.options",
                "type": "number_set",
                "label": "보기의 수",
                "values": [325, 532, 334, 985, 415],
            },
            {
                "id": "number.target_sum",
                "type": "number",
                "label": "목표 합",
                "value": 749,
            },
            {
                "id": "answer.first_blank",
                "type": "unknown_number",
                "label": "첫 번째 빈칸의 수",
            },
            {
                "id": "answer.second_blank",
                "type": "unknown_number",
                "label": "두 번째 빈칸의 수",
            },
            {
                "id": "answer.values",
                "type": "number_pair",
                "label": "두 빈칸의 수",
            },
        ],
        "relations": [
            {
                "id": "relation.answers_are_from_options",
                "type": "selected_from",
                "subjects": [
                    "answer.first_blank",
                    "answer.second_blank",
                ],
                "object": "set.options",
            },
            {
                "id": "relation.answers_sum_to_target",
                "type": "sum_equals",
                "subjects": [
                    "answer.first_blank",
                    "answer.second_blank",
                ],
                "object": "number.target_sum",
            },
        ],
        "problem_solving": {
            "understand": {
                "given_refs": [
                    "set.options",
                    "number.target_sum",
                ],
                "target_ref": "answer.values",
                "condition_refs": [
                    "relation.answers_are_from_options",
                    "relation.answers_sum_to_target",
                ],
            },
            "plan": {
                "method": "complement_search",
                "description": "목표 합에서 보기의 수를 빼어 나머지도 보기에 있는지 확인합니다.",
            },
            "execute": {
                "expected_operations": [
                    "subtraction",
                    "addition",
                ],
            },
            "review": {
                "check_methods": [
                    "option_membership",
                    "addition_check",
                ],
            },
        },
    },
    "answer": ANSWER,
}

SOLVABLE = {
    "schema": "modu.solvable.v1.2",
    "problem_id": PROBLEM_ID,
    "problem_type": "multi_numeric_answer_select_addends_problem",
    "inputs": {
        "target_label": "빈칸에 들어갈 두 수",
        "unit": "",
        "options": [325, 532, 334, 985, 415],
        "target_sum": 749,
        "blank_count": 2,
    },
    "given": [
        {
            "ref": "set.options",
            "value": [325, 532, 334, 985, 415],
        },
        {
            "ref": "number.target_sum",
            "value": 749,
        },
    ],
    "target": {
        "ref": "answer.values",
        "type": "number_pair",
    },
    "method": "목표 합 749에서 보기의 수를 하나씩 빼고, 남은 수가 보기에 있는지 확인하여 두 수를 고릅니다.",
    "understanding": {
        "summary": "보기의 다섯 수 중 두 수를 골라 합이 749가 되도록 하는 문제입니다.",
        "facts": [
            {
                "ref": "set.options",
                "label": "고를 수 있는 수",
                "value": [325, 532, 334, 985, 415],
                "unit": "",
                "source": "explicit",
            },
            {
                "ref": "number.target_sum",
                "label": "두 수의 합",
                "value": 749,
                "unit": "",
                "source": "explicit",
            },
        ],
        "unknowns": [
            {
                "ref": "answer.first_blank",
                "label": "첫 번째 빈칸의 수",
                "unit": "",
            },
            {
                "ref": "answer.second_blank",
                "label": "두 번째 빈칸의 수",
                "unit": "",
            },
        ],
        "relation": {
            "type": "select_two_addends",
            "statement": "두 빈칸의 수는 모두 보기에 있으며 두 수의 합은 749입니다.",
            "symbolic": "□ + □ = 749",
            "uses": [
                "set.options",
                "number.target_sum",
            ],
            "result": "answer.values",
        },
        "diagnostic_questions": [
            {
                "id": "understand.target",
                "type": "multiple_choice",
                "prompt": "이 문제에서 찾아야 하는 것은 무엇인가요?",
                "choices": [
                    "보기에서 합이 749가 되는 두 수",
                    "보기에서 가장 큰 수",
                    "보기의 모든 수의 합",
                ],
                "answer_index": 0,
            },
            {
                "id": "understand.condition",
                "type": "multiple_choice",
                "prompt": "빈칸에 넣을 수는 어디에서 골라야 하나요?",
                "choices": [
                    "749보다 큰 수 중에서 고릅니다.",
                    "<보기>에 있는 수 중에서 고릅니다.",
                    "아무 수나 만들어 넣습니다.",
                ],
                "answer_index": 1,
            },
        ],
    },
    "plan": [
        "목표 합 749에서 보기의 수를 하나씩 빼 봅니다.",
        "뺀 결과가 보기에 있는 수인지 확인합니다.",
        "찾은 두 수를 더하여 합이 749인지 검산합니다.",
    ],
    "steps": [
        {
            "id": "step.find_complement",
            "expr": "749 - 334",
            "value": 415,
            "explanation": "보기의 334를 749에서 빼면 415이고, 415도 보기에 있습니다.",
        },
        {
            "id": "step.select_pair",
            "expr": "334 + 415",
            "value": [334, 415],
            "explanation": "보기의 334와 415를 두 빈칸에 넣으면 합이 749가 됩니다.",
        },
    ],
    "checks": [
        {
            "id": "check.option_membership",
            "expr": "334 in options and 415 in options",
            "expected": True,
            "actual": True,
            "pass": True,
        },
        {
            "id": "check.target_sum",
            "expr": "334 + 415",
            "expected": 749,
            "actual": 749,
            "pass": True,
        },
    ],
    "answer": ANSWER,
}


SEMANTIC_ANSWER = SOLVABLE["answer"]
