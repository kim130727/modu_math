from __future__ import annotations

from modu_math.dsl import (
    BlankSlot,
    Canvas,
    ProblemTemplate,
    Region,
    TextBoxSlot,
)


PROBLEM_ID = "P3_1_01_00040_15616"
PROBLEM_TITLE = "두 사람이 넘은 줄넘기의 총횟수"


ANSWER = {
    "type": "numeric",
    "value": 465,
    "unit": "회",
    "target_ref": "quantity.total_jumps",
    "derived_from": "step.add_jump_counts",
}


SEMANTIC = {
    "problem_id": PROBLEM_ID,
    "problem_type": "numeric_answer_addition_word_problem",
    "metadata": {
        "grade": 3,
        "semester": 1,
        "subject": "수학",
        "topic": "세 자리 수의 덧셈",
        "language": "ko-KR",
    },
    "domain": {
        "objects": [
            {
                "id": "person.juyeong",
                "type": "person",
                "label": "주영이",
            },
            {
                "id": "person.yeongsu",
                "type": "person",
                "label": "영수",
            },
            {
                "id": "activity.jump_rope",
                "type": "physical_activity",
                "label": "줄넘기",
                "unit": "회",
            },
            {
                "id": "quantity.juyeong_jumps",
                "type": "quantity",
                "label": "주영이가 넘은 줄넘기 횟수",
                "value": 123,
                "unit": "회",
            },
            {
                "id": "quantity.yeongsu_jumps",
                "type": "quantity",
                "label": "영수가 넘은 줄넘기 횟수",
                "value": 342,
                "unit": "회",
            },
            {
                "id": "quantity.total_jumps",
                "type": "quantity",
                "label": "두 사람이 넘은 줄넘기의 총횟수",
                "value": 465,
                "unit": "회",
            },
        ],
        "relations": [
            {
                "id": "relation.juyeong_did_jump_rope",
                "type": "performed",
                "from_id": "person.juyeong",
                "to_id": "activity.jump_rope",
                "quantity": "quantity.juyeong_jumps",
            },
            {
                "id": "relation.yeongsu_did_jump_rope",
                "type": "performed",
                "from_id": "person.yeongsu",
                "to_id": "activity.jump_rope",
                "quantity": "quantity.yeongsu_jumps",
            },
            {
                "id": "relation.juyeong_jumps_part_of_total",
                "type": "part_of_sum",
                "from_id": "quantity.juyeong_jumps",
                "to_id": "quantity.total_jumps",
            },
            {
                "id": "relation.yeongsu_jumps_part_of_total",
                "type": "part_of_sum",
                "from_id": "quantity.yeongsu_jumps",
                "to_id": "quantity.total_jumps",
            },
        ],
    },
    "answer": ANSWER,
}

SEMANTIC_OVERRIDE = SEMANTIC


SOLVABLE = {
    "schema": "modu.solvable.v1.2",
    "problem_id": PROBLEM_ID,
    "problem_type": "numeric_answer_addition_word_problem",
    "inputs": {
        "target_label": "두 사람이 넘은 줄넘기의 총횟수",
        "unit": "회",
        "quantities": {
            "juyeong_jumps": 123,
            "yeongsu_jumps": 342,
        },
        "conditions": [
            "주영이는 줄넘기를 123회 넘었습니다.",
            "영수는 줄넘기를 342회 넘었습니다.",
            "두 사람이 넘은 줄넘기 횟수를 모두 구합니다.",
        ],
    },
    "given": [
        {
            "ref": "quantity.juyeong_jumps",
            "value": {
                "count": 123,
                "unit": "회",
                "person": "person.juyeong",
                "activity": "activity.jump_rope",
            },
        },
        {
            "ref": "quantity.yeongsu_jumps",
            "value": {
                "count": 342,
                "unit": "회",
                "person": "person.yeongsu",
                "activity": "activity.jump_rope",
            },
        },
    ],
    "target": {
        "ref": "quantity.total_jumps",
        "type": "number",
    },
    "understanding": {
        "summary": "주영이와 영수가 각각 넘은 줄넘기 횟수를 합하여 두 사람의 총횟수를 구하는 문제입니다.",
        "facts": [
            {
                "ref": "quantity.juyeong_jumps",
                "label": "주영이가 넘은 줄넘기 횟수",
                "value": 123,
                "unit": "회",
                "source": "explicit",
            },
            {
                "ref": "quantity.yeongsu_jumps",
                "label": "영수가 넘은 줄넘기 횟수",
                "value": 342,
                "unit": "회",
                "source": "explicit",
            },
        ],
        "unknowns": [
            {
                "ref": "quantity.total_jumps",
                "label": "두 사람이 넘은 줄넘기의 총횟수",
                "unit": "회",
                "source": "unknown",
            },
        ],
        "relation": {
            "type": "part_part_whole_addition",
            "statement": "두 사람이 넘은 줄넘기의 총횟수는 각 사람이 넘은 횟수를 더한 수입니다.",
            "symbolic": "총횟수 = 주영이의 횟수 + 영수의 횟수",
            "uses": [
                "quantity.juyeong_jumps",
                "quantity.yeongsu_jumps",
            ],
            "result": "quantity.total_jumps",
        },
        "diagnostic_questions": [
            {
                "id": "understand.target",
                "type": "multiple_choice",
                "prompt": "이 문제에서 구해야 하는 것은 무엇인가요?",
                "choices": [
                    "주영이가 넘은 줄넘기 횟수",
                    "영수가 넘은 줄넘기 횟수",
                    "두 사람이 넘은 줄넘기의 총횟수",
                ],
                "answer_index": 2,
            },
            {
                "id": "understand.relation",
                "type": "multiple_choice",
                "prompt": "두 사람이 넘은 줄넘기 횟수를 모두 구하려면 어떻게 해야 하나요?",
                "choices": [
                    "123과 342를 더합니다.",
                    "342에서 123을 뺍니다.",
                    "123과 342를 비교합니다.",
                ],
                "answer_index": 0,
            },
        ],
        "student_restatement": {
            "prompt": "문제의 요지를 말해 볼까요?",
            "template": "{juyeong_jumps}회와 {yeongsu_jumps}회를 더해 {target_label}를 구합니다.",
            "answer": "123회와 342회를 더해 두 사람이 넘은 줄넘기의 총횟수를 구합니다.",
        },
    },
    "method": "두 사람이 각각 넘은 줄넘기 횟수를 덧셈으로 합하여 총횟수를 구합니다.",
    "plan": [
        "주영이가 넘은 줄넘기 횟수 123회를 확인합니다.",
        "영수가 넘은 줄넘기 횟수 342회를 확인합니다.",
        "두 횟수를 더하여 총횟수를 구합니다.",
    ],
    "steps": [
        {
            "id": "step.add_jump_counts",
            "goal": "두 사람이 넘은 줄넘기의 총횟수를 구합니다.",
            "uses": [
                "quantity.juyeong_jumps",
                "quantity.yeongsu_jumps",
            ],
            "relation_expr": "총횟수 = 주영이의 횟수 + 영수의 횟수",
            "expr": "123 + 342",
            "value": {
                "count": 465,
                "unit": "회",
                "ref": "quantity.total_jumps",
            },
            "explanation": "두 사람이 넘은 줄넘기 횟수를 모두 구해야 하므로 123과 342를 더합니다.",
        },
    ],
    "checks": [
        {
            "id": "check.subtract_juyeong_jumps",
            "expr": "465 - 123",
            "expected": 342,
            "actual": 342,
            "pass": True,
        },
        {
            "id": "check.subtract_yeongsu_jumps",
            "expr": "465 - 342",
            "expected": 123,
            "actual": 123,
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
            height=170,
            coordinate_mode="logical",
        ),
        regions=(
            Region(
                id="region.stem",
                role="stem",
                flow="vertical",
                slot_ids=(
                    "slot.question",
                    "slot.answer",
                ),
            ),
        ),
        slots=(
            TextBoxSlot(
                id="slot.question",
                x=24,
                y=24,
                width=852,
                height=54,
                text=(
                    "줄넘기를 하였습니다. 주영이는 123회, 영수는 342회를 넘었습니다. "
                    "두 사람이 넘은 줄넘기는 모두 몇 회입니까?"
                ),
                font_size=24,
                font_family="Noto Sans KR",
                fill="#202124",
                line_height=1.45,
                align="left",
                valign="top",
            ),
            BlankSlot(
                id="slot.answer",
                prompt="답",
                answer_key="465",
                placeholder="회",
            ),
        ),
    )


PROBLEM_TEMPLATE = build_problem_template()
