from __future__ import annotations

from modu_math.dsl import (
    BlankSlot,
    Canvas,
    ProblemTemplate,
    Region,
    TextBoxSlot,
)


PROBLEM_ID = "P3_1_01_00040_07649"
PROBLEM_TITLE = "3학년 학생들에게 필요한 연필 수"


def build_problem_template() -> ProblemTemplate:
    return ProblemTemplate(
        id=PROBLEM_ID,
        title=PROBLEM_TITLE,
        canvas=Canvas(
            width=900,
            height=250,
            coordinate_mode="logical",
        ),
        regions=(
            Region(
                id="region.stem",
                role="stem",
                flow="vertical",
                slot_ids=("slot.question",),
            ),
        ),
        slots=(
            TextBoxSlot(
                id="slot.question",
                x=48,
                y=30,
                width=804,
                height=120,
                text=(
                    "경진이네 학교 3학년 학생은 남학생이 87명, 여학생이 66명입니다. "
                    "3학년 학생 모두에게 연필을 2자루씩 나누어 주려고 합니다. "
                    "학생들에게 나누어 주기 위해 필요한 연필은 모두 몇 자루입니까?"
                ),
                font_size=24,
                font_family="Noto Sans KR",
                fill="#202124",
                line_height=1.5,
                align="left",
                valign="top",
            ),
            BlankSlot(
                id="slot.answer",
                prompt="답",
                answer_key="306",
                placeholder="자루",
            ),
        ),
    )


PROBLEM_TEMPLATE = build_problem_template()


SEMANTIC = {
    "problem_id": PROBLEM_ID,
    "problem_type": "numeric_answer_total_then_multiply_word_problem",
    "metadata": {
        "grade": 3,
        "semester": 1,
        "subject": "수학",
        "topic": "덧셈과 곱셈을 활용한 문제 해결",
        "language": "ko-KR",
    },
    "domain": {
        "objects": [
            {
                "id": "school.gyeongjin",
                "type": "school",
                "label": "경진이네 학교",
            },
            {
                "id": "group.grade3_male_students",
                "type": "student_group",
                "label": "3학년 남학생",
            },
            {
                "id": "group.grade3_female_students",
                "type": "student_group",
                "label": "3학년 여학생",
            },
            {
                "id": "group.grade3_all_students",
                "type": "student_group",
                "label": "3학년 전체 학생",
            },
            {
                "id": "object.pencil",
                "type": "school_supply",
                "label": "연필",
            },
            {
                "id": "quantity.male_student_count",
                "type": "quantity",
                "label": "3학년 남학생 수",
                "value": 87,
                "unit": "명",
            },
            {
                "id": "quantity.female_student_count",
                "type": "quantity",
                "label": "3학년 여학생 수",
                "value": 66,
                "unit": "명",
            },
            {
                "id": "quantity.total_student_count",
                "type": "quantity",
                "label": "3학년 전체 학생 수",
                "value": 153,
                "unit": "명",
            },
            {
                "id": "quantity.pencils_per_student",
                "type": "quantity",
                "label": "학생 한 명에게 주는 연필 수",
                "value": 2,
                "unit": "자루/명",
            },
            {
                "id": "quantity.total_pencil_count",
                "type": "quantity",
                "label": "필요한 전체 연필 수",
                "value": 306,
                "unit": "자루",
            },
        ],
        "relations": [
            {
                "id": "relation.total_students_is_sum",
                "type": "sum_of",
                "subject": "quantity.total_student_count",
                "objects": [
                    "quantity.male_student_count",
                    "quantity.female_student_count",
                ],
            },
            {
                "id": "relation.pencils_distributed_equally",
                "type": "equal_distribution_per_person",
                "subject": "object.pencil",
                "recipient_group": "group.grade3_all_students",
                "quantity_per_person": "quantity.pencils_per_student",
            },
            {
                "id": "relation.total_pencils_is_product",
                "type": "product_of",
                "subject": "quantity.total_pencil_count",
                "factors": [
                    "quantity.total_student_count",
                    "quantity.pencils_per_student",
                ],
            },
        ],
    },
    "answer": {
        "type": "numeric",
        "value": 306,
        "unit": "자루",
        "target_ref": "quantity.total_pencil_count",
    },
}

SEMANTIC_OVERRIDE = SEMANTIC


SOLVABLE = {
    "schema": "modu.solvable.v1.2",
    "problem_id": PROBLEM_ID,
    "problem_type": "numeric_answer_total_then_multiply_word_problem",
    "inputs": {
        "target_label": "3학년 학생들에게 필요한 전체 연필 수",
        "unit": "자루",
        "quantities": {
            "male_student_count": 87,
            "female_student_count": 66,
            "pencils_per_student": 2,
        },
        "conditions": [
            "3학년 남학생은 87명입니다.",
            "3학년 여학생은 66명입니다.",
            "3학년 모든 학생에게 연필을 2자루씩 줍니다.",
        ],
    },
    "given": [
        {
            "ref": "quantity.male_student_count",
            "value": {
                "count": 87,
                "unit": "명",
                "group": "group.grade3_male_students",
            },
        },
        {
            "ref": "quantity.female_student_count",
            "value": {
                "count": 66,
                "unit": "명",
                "group": "group.grade3_female_students",
            },
        },
        {
            "ref": "quantity.pencils_per_student",
            "value": {
                "count": 2,
                "unit": "자루/명",
                "object": "object.pencil",
                "recipient_group": "group.grade3_all_students",
            },
        },
    ],
    "target": {
        "ref": "quantity.total_pencil_count",
        "type": "number",
    },
    "method": "남학생 수와 여학생 수를 더한 뒤, 전체 학생 수에 한 명당 연필 수 2를 곱합니다.",
    "plan": [
        "남학생 87명과 여학생 66명을 더하여 3학년 전체 학생 수를 구합니다.",
        "전체 학생 수에 학생 한 명당 필요한 연필 2자루를 곱합니다.",
    ],
    "steps": [
        {
            "id": "step.find_total_students",
            "goal": "3학년 전체 학생 수를 구합니다.",
            "uses": [
                "quantity.male_student_count",
                "quantity.female_student_count",
            ],
            "relation_expr": "전체 학생 수 = 남학생 수 + 여학생 수",
            "expr": "87 + 66",
            "value": 153,
            "explanation": "연필을 받을 학생은 남학생과 여학생 모두이므로 두 학생 수를 더합니다.",
        },
        {
            "id": "step.find_total_pencils",
            "goal": "학생들에게 필요한 전체 연필 수를 구합니다.",
            "uses": [
                "quantity.total_student_count",
                "quantity.pencils_per_student",
            ],
            "relation_expr": "전체 연필 수 = 전체 학생 수 × 한 명당 연필 수",
            "expr": "153 * 2",
            "value": 306,
            "explanation": "153명 모두에게 2자루씩 주므로 153에 2를 곱합니다.",
        },
    ],
    "checks": [
        {
            "id": "check.total_students",
            "description": "전체 학생 수에서 여학생 수를 빼면 남학생 수가 되는지 확인합니다.",
            "expr": "153 - 66",
            "expected": 87,
            "actual": 87,
            "pass": True,
        },
        {
            "id": "check_total_pencils_by_addition",
            "description": "전체 연필 수가 153을 두 번 더한 값과 같은지 확인합니다.",
            "expr": "153 + 153",
            "expected": 306,
            "actual": 306,
            "pass": True,
        },
        {
            "id": "check_pencils_per_student",
            "description": "전체 연필을 전체 학생에게 똑같이 나누면 한 명당 2자루인지 확인합니다.",
            "expr": "306 / 153",
            "expected": 2,
            "actual": 2,
            "pass": True,
        },
    ],
    "answer": {
        "type": "numeric",
        "value": 306,
        "unit": "자루",
        "target_ref": "quantity.total_pencil_count",
    },
    "understanding": {
        "summary": (
            "3학년 남학생과 여학생의 수를 더해 전체 학생 수를 구한 다음, "
            "모든 학생에게 2자루씩 줄 때 필요한 연필 수를 구하는 문제입니다."
        ),
        "facts": [
            {
                "ref": "quantity.male_student_count",
                "label": "3학년 남학생 수",
                "value": 87,
                "unit": "명",
                "source": "explicit",
            },
            {
                "ref": "quantity.female_student_count",
                "label": "3학년 여학생 수",
                "value": 66,
                "unit": "명",
                "source": "explicit",
            },
            {
                "ref": "quantity.pencils_per_student",
                "label": "학생 한 명에게 주는 연필 수",
                "value": 2,
                "unit": "자루",
                "source": "explicit",
            },
        ],
        "unknowns": [
            {
                "ref": "quantity.total_pencil_count",
                "label": "필요한 전체 연필 수",
                "unit": "자루",
                "source": "unknown",
            },
        ],
        "relation": {
            "type": "group_total_then_equal_quantity_product",
            "statement": (
                "남학생 수와 여학생 수를 합한 전체 학생 수에 "
                "한 명당 연필 수를 곱하면 필요한 전체 연필 수가 됩니다."
            ),
            "symbolic": "(87 + 66) × 2 = 306",
            "uses": [
                "quantity.male_student_count",
                "quantity.female_student_count",
                "quantity.pencils_per_student",
            ],
            "result": "quantity.total_pencil_count",
        },
        "diagnostic_questions": [
            {
                "id": "understand.target",
                "type": "multiple_choice",
                "prompt": "이 문제에서 구해야 하는 것은 무엇인가요?",
                "choices": [
                    "3학년 전체 학생 수",
                    "남학생에게만 필요한 연필 수",
                    "3학년 모두에게 필요한 연필 수",
                ],
                "answer_index": 2,
            },
            {
                "id": "understand.first_step",
                "type": "multiple_choice",
                "prompt": "먼저 무엇을 구해야 하나요?",
                "choices": [
                    "3학년 전체 학생 수",
                    "연필 한 자루의 가격",
                    "남학생과 여학생 수의 차이",
                ],
                "answer_index": 0,
            },
            {
                "id": "understand.operation_order",
                "type": "multiple_choice",
                "prompt": "필요한 연필 수를 구하는 계산은 무엇인가요?",
                "choices": [
                    "(87 + 66) × 2",
                    "(87 - 66) × 2",
                    "87 + 66 + 2",
                ],
                "answer_index": 0,
            },
        ],
        "student_restatement": {
            "prompt": "문제의 뜻을 말해 볼까요?",
            "template": (
                "남학생 {male}명과 여학생 {female}명을 더해 전체 학생 수를 구하고, "
                "한 명에게 {per_student}자루씩 줄 때 필요한 {target}를 구합니다."
            ),
            "answer": (
                "남학생 87명과 여학생 66명을 더해 전체 학생 수를 구하고, "
                "한 명에게 2자루씩 줄 때 필요한 전체 연필 수를 구합니다."
            ),
        },
    },
}


SEMANTIC_ANSWER = SOLVABLE["answer"]
