from __future__ import annotations

from modu_math.dsl import (
    BlankSlot,
    Canvas,
    ProblemTemplate,
    Region,
    TextBoxSlot,
    TextSlot,
)


PROBLEM_ID = "P3_1_01_00040_00469"
PROBLEM_TITLE = "두 가족이 캔 고구마의 수"


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
                "id": "person.sanghyeon",
                "type": "person",
                "label": "상현이",
            },
            {
                "id": "person.yongjin",
                "type": "person",
                "label": "용진이",
            },
            {
                "id": "group.sanghyeon_family",
                "type": "family",
                "label": "상현이네 가족",
            },
            {
                "id": "group.yongjin_family",
                "type": "family",
                "label": "용진이네 가족",
            },
            {
                "id": "object.sweet_potato",
                "type": "countable_object",
                "label": "고구마",
                "unit": "개",
            },
            {
                "id": "quantity.sanghyeon_family_sweet_potatoes",
                "type": "quantity",
                "label": "상현이네 가족이 캔 고구마 수",
                "value": 259,
                "unit": "개",
            },
            {
                "id": "quantity.yongjin_family_sweet_potatoes",
                "type": "quantity",
                "label": "용진이네 가족이 캔 고구마 수",
                "value": 248,
                "unit": "개",
            },
            {
                "id": "quantity.total_sweet_potatoes",
                "type": "quantity",
                "label": "두 가족이 캔 고구마 수",
                "value": 507,
                "unit": "개",
            },
        ],
        "relations": [
            {
                "id": "relation.sanghyeon_belongs_to_family",
                "type": "member_of",
                "from_id": "person.sanghyeon",
                "to_id": "group.sanghyeon_family",
            },
            {
                "id": "relation.yongjin_belongs_to_family",
                "type": "member_of",
                "from_id": "person.yongjin",
                "to_id": "group.yongjin_family",
            },
            {
                "id": "relation.sanghyeon_family_collected",
                "type": "collected",
                "from_id": "group.sanghyeon_family",
                "to_id": "object.sweet_potato",
                "quantity": "quantity.sanghyeon_family_sweet_potatoes",
            },
            {
                "id": "relation.yongjin_family_collected",
                "type": "collected",
                "from_id": "group.yongjin_family",
                "to_id": "object.sweet_potato",
                "quantity": "quantity.yongjin_family_sweet_potatoes",
            },
            {
                "id": "relation.sanghyeon_count_part_of_total",
                "type": "part_of_sum",
                "from_id": "quantity.sanghyeon_family_sweet_potatoes",
                "to_id": "quantity.total_sweet_potatoes",
            },
            {
                "id": "relation.yongjin_count_part_of_total",
                "type": "part_of_sum",
                "from_id": "quantity.yongjin_family_sweet_potatoes",
                "to_id": "quantity.total_sweet_potatoes",
            },
        ],
    },
    "answer": {
        "value": 507,
        "unit": "개",
    },
}

SEMANTIC_OVERRIDE = SEMANTIC


SOLVABLE = {
    "schema": "modu.solvable.v1.2",
    "problem_id": PROBLEM_ID,
    "problem_type": "numeric_answer_addition_word_problem",
    "inputs": {
        "target_label": "두 가족이 캔 고구마의 수",
        "unit": "개",
        "quantities": {
            "sanghyeon_family_count": 259,
            "yongjin_family_count": 248,
        },
        "conditions": [
            "상현이네 가족은 고구마를 259개 캤습니다.",
            "용진이네 가족은 고구마를 248개 캤습니다.",
            "두 가족이 캔 고구마 수를 모두 구합니다.",
        ],
    },
    "given": [
        {
            "ref": "quantity.sanghyeon_family_sweet_potatoes",
            "value": {
                "count": 259,
                "unit": "개",
                "owner": "group.sanghyeon_family",
                "object": "object.sweet_potato",
            },
        },
        {
            "ref": "quantity.yongjin_family_sweet_potatoes",
            "value": {
                "count": 248,
                "unit": "개",
                "owner": "group.yongjin_family",
                "object": "object.sweet_potato",
            },
        },
    ],
    "target": {
        "ref": "quantity.total_sweet_potatoes",
        "type": "number",
    },
    "understanding": {
        "summary": "두 가족이 각각 캔 고구마 수를 모두 합해 전체 고구마 수를 구하는 문제입니다.",
        "facts": [
            {
                "ref": "quantity.sanghyeon_family_sweet_potatoes",
                "label": "상현이네 가족이 캔 고구마 수",
                "value": 259,
                "unit": "개",
                "source": "explicit",
            },
            {
                "ref": "quantity.yongjin_family_sweet_potatoes",
                "label": "용진이네 가족이 캔 고구마 수",
                "value": 248,
                "unit": "개",
                "source": "explicit",
            },
        ],
        "unknowns": [
            {
                "ref": "quantity.total_sweet_potatoes",
                "label": "두 가족이 캔 고구마 수",
                "unit": "개",
                "source": "unknown",
            },
        ],
        "relation": {
            "type": "part_part_whole_addition",
            "statement": "두 가족이 캔 고구마 수를 모두 구하려면 각각 캔 수를 더합니다.",
            "symbolic": "전체 = 상현이네 수 + 용진이네 수",
            "uses": [
                "quantity.sanghyeon_family_sweet_potatoes",
                "quantity.yongjin_family_sweet_potatoes",
            ],
            "result": "quantity.total_sweet_potatoes",
        },
        "diagnostic_questions": [
            {
                "id": "understand.target",
                "type": "multiple_choice",
                "prompt": "이 문제에서 구해야 하는 것은 무엇인가요?",
                "choices": [
                    "상현이네 가족이 캔 고구마 수",
                    "용진이네 가족이 캔 고구마 수",
                    "두 가족이 캔 고구마 수",
                ],
                "answer_index": 2,
            },
            {
                "id": "understand.relation",
                "type": "multiple_choice",
                "prompt": "두 가족이 캔 고구마 수를 모두 구하려면 어떻게 해야 하나요?",
                "choices": [
                    "259와 248을 더합니다.",
                    "259에서 248을 뺍니다.",
                    "259와 248을 비교합니다.",
                ],
                "answer_index": 0,
            },
        ],
        "student_restatement": {
            "prompt": "문제의 요지를 말해 볼까요?",
            "template": "{first_count}개와 {second_count}개를 더해 {target_label}를 구합니다.",
            "answer": "259개와 248개를 더해 두 가족이 캔 고구마 수를 구합니다.",
        },
    },
    "method": "두 가족이 캔 고구마 수를 덧셈으로 구한다.",
    "plan": [
        "상현이네 가족이 캔 고구마 수를 확인한다.",
        "용진이네 가족이 캔 고구마 수를 확인한다.",
        "두 수를 더하여 전체 고구마 수를 구한다.",
    ],
    "steps": [
        {
            "id": "step.add_counts",
            "goal": "두 가족이 캔 고구마 수를 모두 구합니다.",
            "uses": [
                "quantity.sanghyeon_family_sweet_potatoes",
                "quantity.yongjin_family_sweet_potatoes",
            ],
            "relation_expr": "전체 = 상현이네 수 + 용진이네 수",
            "expr": "259 + 248",
            "value": {
                "count": 507,
                "unit": "개",
                "ref": "quantity.total_sweet_potatoes",
            },
            "explanation": "두 가족이 캔 고구마 수를 모두 구해야 하므로 259와 248을 더합니다.",
        },
    ],
    "checks": [
        {
            "id": "check.inverse_subtraction",
            "expr": "507 - 248",
            "expected": 259,
            "actual": 259,
            "pass": True,
        },
        {
            "id": "check.minimum_total",
            "expr": "507 > 259 and 507 > 248",
            "expected": True,
            "actual": True,
            "pass": True,
        },
    ],
    "answer": {
        "value": 507,
        "unit": "개",
    },
}

SEMANTIC_ANSWER = SOLVABLE["answer"]


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
                    "slot.question",
                    "slot.expression",
                    "slot.answer",
                ),
            ),
        ),
        slots=(
            TextBoxSlot(
                id="slot.question",
                x=48,
                y=34,
                width=804,
                height=72,
                text=(
                    "지난 일요일 상현이네와 용진이네 가족은 주말 농장에 갔습니다. "
                    "고구마를 상현이네는 259개, 용진이네는\n"
                    "248개 캤습니다. 이 두 가족이 캔 고구마는 모두 몇 개입니까?"
                ),
                font_size=24,
                font_family="Noto Sans KR",
                fill="#202124",
                line_height=1.55,
                align="left",
                valign="top",
            ),
            TextBoxSlot(
                id="slot.expression",
                x=48,
                y=125,
                width=804,
                height=34,
                text="식",
                font_size=24,
                font_family="Noto Sans KR",
                fill="#202124",
                align="left",
                valign="middle",
            ),
            BlankSlot(
                id="slot.answer",
                prompt="답",
                answer_key="507",
                placeholder="개",
            ),
        ),
    )


PROBLEM_TEMPLATE = build_problem_template()
