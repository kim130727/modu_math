from __future__ import annotations

from modu_math.dsl import (
    BlankSlot,
    Canvas,
    ProblemTemplate,
    Region,
    TextBoxSlot,
    TextSlot,
)

PROBLEM_ID = "P3_1_01_00040_00470"
PROBLEM_TITLE = "올해 수확한 사과 수"


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
                slot_ids=("slot.question",),
            ),
        ),
        slots=(
            TextBoxSlot(
                id="slot.question",
                x=48,
                y=30,
                width=804,
                height=80,
                text="진이네 과수원에서는 작년에 사과 725개를 수확하였고, 올해는 작년보다 287개를 더 수확하였습니다. 올해에 수확한 사과는 모두 몇 개입니까?",
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
                answer_key="1012",
                placeholder="개",
            ),
        ),
    )


PROBLEM_TEMPLATE = build_problem_template()


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
                "id": "place.jini_orchard",
                "type": "orchard",
                "label": "진이네 과수원",
            },
            {
                "id": "object.apple",
                "type": "countable_object",
                "label": "사과",
                "unit": "개",
            },
            {
                "id": "quantity.last_year_apple_count",
                "type": "quantity",
                "label": "작년에 수확한 사과 수",
                "value": 725,
                "unit": "개",
            },
            {
                "id": "quantity.increased_apple_count",
                "type": "quantity",
                "label": "올해 더 수확한 사과 수",
                "value": 287,
                "unit": "개",
            },
            {
                "id": "quantity.this_year_apple_count",
                "type": "quantity",
                "label": "올해 수확한 사과 수",
                "value": 1012,
                "unit": "개",
            },
        ],
        "relations": [
            {
                "id": "relation.last_year_harvest",
                "type": "harvested",
                "subject": "place.jini_orchard",
                "object": "object.apple",
                "quantity": "quantity.last_year_apple_count",
                "time": "last_year",
            },
            {
                "id": "relation.this_year_more_than_last_year",
                "type": "greater_by",
                "subject": "quantity.this_year_apple_count",
                "object": "quantity.last_year_apple_count",
                "difference": "quantity.increased_apple_count",
            },
            {
                "id": "relation.this_year_is_sum",
                "type": "sum_of",
                "subject": "quantity.this_year_apple_count",
                "objects": [
                    "quantity.last_year_apple_count",
                    "quantity.increased_apple_count",
                ],
            },
        ],
    },
    "answer": {
        "type": "numeric",
        "value": 1012,
        "unit": "개",
        "target_ref": "quantity.this_year_apple_count",
    },
}

SEMANTIC_OVERRIDE = SEMANTIC


SOLVABLE = {
    "schema": "modu.solvable.v1.2",
    "problem_id": "P3_1_01_00040_00470",
    "problem_type": "numeric_answer_addition_word_problem",
    "inputs": {
        "target_label": "올해 수확한 사과 수",
        "unit": "개",
        "quantities": {"last_year_apple_count": 725, "increased_apple_count": 287},
        "conditions": [
            "진이네 과수원에서는 작년에 사과 725개를 수확했습니다.",
            "올해는 작년보다 사과를 287개 더 수확했습니다.",
            "올해 수확한 사과 수를 구합니다.",
        ],
    },
    "given": [
        {
            "ref": "quantity.last_year_apple_count",
            "value": {
                "count": 725,
                "unit": "개",
                "place": "place.jini_orchard",
                "object": "object.apple",
                "time": "last_year",
            },
        },
        {
            "ref": "quantity.increased_apple_count",
            "value": {"count": 287, "unit": "개", "comparison": "more_than_last_year"},
        },
    ],
    "target": {"ref": "quantity.this_year_apple_count", "type": "number"},
    "method": "작년에 수확한 사과 수와 올해 더 수확한 사과 수를 더한다.",
    "plan": [
        "작년에 수확한 사과 수를 확인한다.",
        "올해 작년보다 더 수확한 사과 수를 확인한다.",
        "두 수를 더하여 올해 수확한 사과 수를 구한다.",
    ],
    "steps": [
        {
            "id": "step.add_apple_counts",
            "expr": "725 + 287",
            "value": 1012,
            "explanation": "올해는 작년보다 287개를 더 수확했으므로 작년에 수확한 725개에 287개를 더합니다.",
        }
    ],
    "checks": [
        {
            "id": "check.inverse_subtraction",
            "expr": "1012 - 287",
            "expected": 725,
            "actual": 725,
            "pass": True,
        },
        {
            "id": "check.increased_amount",
            "expr": "1012 - 725",
            "expected": 287,
            "actual": 287,
            "pass": True,
        },
    ],
    "answer": {
        "type": "numeric",
        "value": 1012,
        "unit": "개",
        "target_ref": "quantity.this_year_apple_count",
    },
    "understanding": {
        "summary": "Find 올해 수확한 사과 수 using the given information.",
        "facts": [
            {
                "ref": "quantity.last_year_apple_count",
                "label": "last year apple count",
                "value": 725,
                "unit": "개",
                "source": "explicit",
            },
            {
                "ref": "quantity.increased_apple_count",
                "label": "increased apple count",
                "value": 287,
                "unit": "개",
                "source": "explicit",
            },
        ],
        "unknowns": [
            {
                "ref": "quantity.this_year_apple_count",
                "label": "올해 수확한 사과 수",
                "unit": "개",
                "source": "unknown",
            }
        ],
        "relation": {
            "type": "작년에 수확한 사과 수와 올해 더 수확한 사과 수를 더한다.",
            "statement": "작년에 수확한 사과 수를 확인한다.",
            "symbolic": "725 + 287",
            "uses": ["quantity.last_year_apple_count", "quantity.increased_apple_count"],
            "result": "quantity.this_year_apple_count",
        },
        "diagnostic_questions": [
            {
                "id": "understand.target",
                "type": "multiple_choice",
                "prompt": "What should we find?",
                "choices": [
                    "last year apple count",
                    "increased apple count",
                    "올해 수확한 사과 수",
                ],
                "answer_index": 2,
            }
        ],
    },
}

SOLVABLE.update(
    {
        "inputs": {
            "target_label": "올해 수확한 사과 수",
            "unit": "개",
            "quantities": {
                "last_year_apple_count": 725,
                "increased_apple_count": 287,
            },
            "conditions": [
                "진이네 과수원에서는 작년에 사과 725개를 수확했습니다.",
                "올해에는 작년보다 사과를 287개 더 수확했습니다.",
                "올해 수확한 사과 수를 구합니다.",
            ],
        },
        "given": [
            {
                "ref": "quantity.last_year_apple_count",
                "value": {
                    "count": 725,
                    "unit": "개",
                    "place": "place.jini_orchard",
                    "object": "object.apple",
                    "time": "last_year",
                },
            },
            {
                "ref": "quantity.increased_apple_count",
                "value": {
                    "count": 287,
                    "unit": "개",
                    "comparison": "more_than_last_year",
                },
            },
        ],
        "target": {"ref": "quantity.this_year_apple_count", "type": "number"},
        "method": "작년에 수확한 사과 수에 올해 더 수확한 사과 수를 더합니다.",
        "plan": [
            "작년에 수확한 사과 수가 725개임을 확인합니다.",
            "올해는 작년보다 287개 더 수확했다는 뜻을 확인합니다.",
            "작년 수확량에 더 늘어난 수를 더해 올해 수확량을 구합니다.",
        ],
        "steps": [
            {
                "id": "step.add_apple_counts",
                "goal": "올해 수확한 사과 수를 구합니다.",
                "uses": [
                    "quantity.last_year_apple_count",
                    "quantity.increased_apple_count",
                ],
                "relation_expr": "올해 수확량 = 작년 수확량 + 더 수확한 수",
                "expr": "725 + 287",
                "value": 1012,
                "explanation": "올해는 작년보다 287개 더 수확했으므로, 작년에 수확한 725개에 287개를 더합니다.",
            }
        ],
        "checks": [
            {
                "id": "check.inverse_subtraction",
                "description": "올해 수확량에서 더 수확한 수를 빼면 작년 수확량이 됩니다.",
                "expr": "1012 - 287",
                "expected": 725,
                "actual": 725,
                "pass": True,
            },
            {
                "id": "check.increased_amount",
                "description": "올해 수확량과 작년 수확량의 차이는 287개입니다.",
                "expr": "1012 - 725",
                "expected": 287,
                "actual": 287,
                "pass": True,
            },
        ],
        "answer": {
            "type": "numeric",
            "value": 1012,
            "unit": "개",
            "target_ref": "quantity.this_year_apple_count",
        },
        "understanding": {
            "summary": "작년에 수확한 사과 수와 올해 더 수확한 사과 수를 더해 올해 수확한 사과 수를 구하는 문제입니다.",
            "facts": [
                {
                    "ref": "quantity.last_year_apple_count",
                    "label": "작년에 수확한 사과 수",
                    "value": 725,
                    "unit": "개",
                    "source": "explicit",
                },
                {
                    "ref": "quantity.increased_apple_count",
                    "label": "올해 더 수확한 사과 수",
                    "value": 287,
                    "unit": "개",
                    "source": "explicit",
                },
            ],
            "unknowns": [
                {
                    "ref": "quantity.this_year_apple_count",
                    "label": "올해 수확한 사과 수",
                    "unit": "개",
                    "source": "unknown",
                }
            ],
            "relation": {
                "type": "increase_addition",
                "statement": "올해 수확량은 작년 수확량보다 287개 많으므로 작년 수확량에 287개를 더합니다.",
                "symbolic": "725 + 287 = 1012",
                "uses": [
                    "quantity.last_year_apple_count",
                    "quantity.increased_apple_count",
                ],
                "result": "quantity.this_year_apple_count",
            },
            "diagnostic_questions": [
                {
                    "id": "understand.target",
                    "type": "multiple_choice",
                    "prompt": "이 문제에서 구해야 하는 것은 무엇인가요?",
                    "choices": [
                        "작년에 수확한 사과 수",
                        "올해 더 수확한 사과 수",
                        "올해 수확한 사과 수",
                    ],
                    "answer_index": 2,
                },
                {
                    "id": "understand.relation",
                    "type": "multiple_choice",
                    "prompt": "올해는 작년보다 287개 더 수확했다면 어떻게 계산해야 하나요?",
                    "choices": [
                        "725에 287을 더합니다.",
                        "725에서 287을 뺍니다.",
                        "287에서 725를 뺍니다.",
                    ],
                    "answer_index": 0,
                },
            ],
            "student_restatement": {
                "prompt": "문제의 뜻을 말해 볼까요?",
                "template": "작년에 {last_year}개를 수확했고 올해는 {increase}개 더 수확했으므로, {target}를 구합니다.",
                "answer": "작년에 725개를 수확했고 올해는 287개 더 수확했으므로, 올해 수확한 사과 수를 구합니다.",
            },
        },
    }
)

SEMANTIC_ANSWER = SOLVABLE["answer"]
