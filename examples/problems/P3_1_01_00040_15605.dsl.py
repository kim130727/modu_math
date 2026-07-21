from __future__ import annotations

from modu_math.dsl import (
    BlankSlot,
    Canvas,
    ProblemTemplate,
    Region,
    TextBoxSlot,
)


PROBLEM_ID = "P3_1_01_00040_15605"
PROBLEM_TITLE = "동민이와 가희가 가진 구슬 수"


ANSWER = {
    "type": "numeric",
    "value": 347,
    "unit": "개",
    "target_ref": "quantity.total_marbles",
    "derived_from": "step.add_marbles",
}


SEMANTIC_OVERRIDE = {
    "problem_id": PROBLEM_ID,
    "problem_type": "numeric_answer_addition_word_problem",
    "metadata": {
        "grade": 3,
        "semester": 1,
        "subject": "수학",
        "topic": "세 자리 수의 덧셈",
        "language": "ko-KR",
        "question": "두 사람이 가지고 있는 구슬은 모두 몇 개입니까?",
    },
    "domain": {
        "objects": [
            {
                "id": "person.dongmin",
                "type": "person",
                "label": "동민이",
            },
            {
                "id": "person.gahui",
                "type": "person",
                "label": "가희",
            },
            {
                "id": "object.marble",
                "type": "countable_object",
                "label": "구슬",
                "unit": "개",
            },
            {
                "id": "quantity.dongmin_marbles",
                "type": "quantity",
                "label": "동민이가 가진 구슬 수",
                "value": 215,
                "unit": "개",
            },
            {
                "id": "quantity.gahui_marbles",
                "type": "quantity",
                "label": "가희가 가진 구슬 수",
                "value": 132,
                "unit": "개",
            },
            {
                "id": "quantity.total_marbles",
                "type": "quantity",
                "label": "두 사람이 가진 구슬 수",
                "value": 347,
                "unit": "개",
            },
        ],
        "relations": [
            {
                "id": "relation.dongmin_has_marbles",
                "type": "has_quantity",
                "subject": "person.dongmin",
                "object": "object.marble",
                "quantity": "quantity.dongmin_marbles",
            },
            {
                "id": "relation.gahui_has_marbles",
                "type": "has_quantity",
                "subject": "person.gahui",
                "object": "object.marble",
                "quantity": "quantity.gahui_marbles",
            },
            {
                "id": "relation.total_is_sum",
                "type": "sum_of",
                "subject": "quantity.total_marbles",
                "objects": [
                    "quantity.dongmin_marbles",
                    "quantity.gahui_marbles",
                ],
            },
        ],
    },
    "answer": ANSWER,
}


SOLVABLE = {
    "schema": "modu.solvable.v1.2",
    "problem_id": PROBLEM_ID,
    "problem_type": "numeric_answer_addition_word_problem",
    "inputs": {
        "target_label": "동민이와 가희가 가진 구슬의 전체 수",
        "unit": "개",
        "quantities": {
            "dongmin_count": 215,
            "gahui_count": 132,
        },
        "conditions": [
            "동민이는 구슬을 215개 가지고 있습니다.",
            "가희는 구슬을 132개 가지고 있습니다.",
            "두 사람이 가진 구슬을 모두 셉니다.",
        ],
    },
    "given": [
        {
            "ref": "quantity.dongmin_marbles",
            "value": {
                "count": 215,
                "unit": "개",
                "owner": "person.dongmin",
                "object": "object.marble",
            },
        },
        {
            "ref": "quantity.gahui_marbles",
            "value": {
                "count": 132,
                "unit": "개",
                "owner": "person.gahui",
                "object": "object.marble",
            },
        },
    ],
    "target": {
        "ref": "quantity.total_marbles",
        "type": "number",
    },
    "understanding": {
        "summary": "동민이와 가희가 각각 가진 구슬 수를 더해 전체 구슬 수를 구하는 문제입니다.",
        "facts": [
            {
                "ref": "quantity.dongmin_marbles",
                "label": "동민이가 가진 구슬 수",
                "value": 215,
                "unit": "개",
                "source": "explicit",
            },
            {
                "ref": "quantity.gahui_marbles",
                "label": "가희가 가진 구슬 수",
                "value": 132,
                "unit": "개",
                "source": "explicit",
            },
        ],
        "unknowns": [
            {
                "ref": "quantity.total_marbles",
                "label": "두 사람이 가진 구슬 수",
                "unit": "개",
                "source": "unknown",
            },
        ],
        "relation": {
            "type": "part_part_whole_addition",
            "statement": "두 사람이 가진 구슬 수를 모두 구하려면 각각의 구슬 수를 더합니다.",
            "symbolic": "전체 구슬 수 = 동민이의 구슬 수 + 가희의 구슬 수",
            "uses": [
                "quantity.dongmin_marbles",
                "quantity.gahui_marbles",
            ],
            "result": "quantity.total_marbles",
        },
        "diagnostic_questions": [
            {
                "id": "understand.target",
                "type": "multiple_choice",
                "prompt": "이 문제에서 구해야 하는 것은 무엇인가요?",
                "choices": [
                    "동민이가 가진 구슬 수",
                    "가희가 가진 구슬 수",
                    "두 사람이 가진 구슬 수",
                ],
                "answer_index": 2,
            },
            {
                "id": "understand.operation",
                "type": "multiple_choice",
                "prompt": "두 사람이 가진 구슬을 모두 구하려면 어떻게 해야 하나요?",
                "choices": [
                    "215와 132를 더합니다.",
                    "215에서 132를 뺍니다.",
                    "215와 132의 크기만 비교합니다.",
                ],
                "answer_index": 0,
            },
        ],
        "student_restatement": {
            "prompt": "문제의 요지를 말해 볼까요?",
            "template": "{first_count}개와 {second_count}개를 더해 {target_label}를 구합니다.",
            "answer": "215개와 132개를 더해 두 사람이 가진 구슬 수를 구합니다.",
        },
    },
    "method": "동민이와 가희가 가진 구슬 수를 덧셈으로 합합니다.",
    "plan": [
        "동민이가 가진 구슬 수 215개를 확인합니다.",
        "가희가 가진 구슬 수 132개를 확인합니다.",
        "두 수를 더하여 전체 구슬 수를 구합니다.",
    ],
    "steps": [
        {
            "id": "step.add_marbles",
            "goal": "두 사람이 가진 구슬 수를 모두 구합니다.",
            "uses": [
                "quantity.dongmin_marbles",
                "quantity.gahui_marbles",
            ],
            "relation_expr": "전체 구슬 수 = 동민이의 구슬 수 + 가희의 구슬 수",
            "expr": "215 + 132",
            "value": 347,
            "explanation": "두 사람이 가진 구슬을 모두 세어야 하므로 215와 132를 더합니다.",
        },
    ],
    "checks": [
        {
            "id": "check.subtract_gahui_count",
            "expr": "347 - 132",
            "expected": 215,
            "actual": 215,
            "pass": True,
        },
        {
            "id": "check.subtract_dongmin_count",
            "expr": "347 - 215",
            "expected": 132,
            "actual": 132,
            "pass": True,
        },
        {
            "id": "check.total_is_larger",
            "expr": "347 > 215 and 347 > 132",
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
            height=190,
            coordinate_mode="logical",
        ),
        regions=(
            Region(
                id="region.stem",
                role="stem",
                flow="vertical",
                slot_ids=(
                    "slot.question",
                    "slot.expression",
                    "slot.answer",
                ),
            ),
        ),
        slots=(
            TextBoxSlot(
                id="slot.question",
                x=20,
                y=18,
                width=860,
                height=50,
                text=(
                    "동민이는 구슬을 215개 가지고 있고, 가희는 구슬을 132개 가지고 있습니다. "
                    "두 사람이 가지고 있는 구슬은 모두 몇 개입니까?"
                ),
                font_size=21,
                font_family="Noto Sans KR",
                fill="#202124",
                line_height=1.45,
                align="left",
                valign="top",
            ),
            TextBoxSlot(
                id="slot.expression",
                x=20,
                y=92,
                width=860,
                height=32,
                text="식",
                font_size=22,
                font_family="Noto Sans KR",
                fill="#202124",
                align="left",
                valign="middle",
            ),
            BlankSlot(
                id="slot.answer",
                prompt="답",
                answer_key="347",
                placeholder="개",
            ),
        ),
    )


PROBLEM_TEMPLATE = build_problem_template()
