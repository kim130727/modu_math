from __future__ import annotations

from modu_math.dsl import (
    BlankSlot,
    Canvas,
    ProblemTemplate,
    Region,
    TextSlot,
)


PROBLEM_ID = "P3_1_01_00040_15612"
PROBLEM_TITLE = "합이 가장 큰 식 찾기"


def build_problem_template() -> ProblemTemplate:
    return ProblemTemplate(
        id=PROBLEM_ID,
        title=PROBLEM_TITLE,
        canvas=Canvas(
            width=900,
            height=220,
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
                    "slot.choice_1.number",
                    "slot.choice_1.expression",
                    "slot.choice_2.number",
                    "slot.choice_2.expression",
                    "slot.choice_3.number",
                    "slot.choice_3.expression",
                    "slot.choice_4.number",
                    "slot.choice_4.expression",
                    "slot.choice_5.number",
                    "slot.choice_5.expression",
                ),
            ),
        ),
        slots=(
            TextSlot(
                id="slot.question",
                prompt="",
                text="다음 중 합이 가장 큰 것은 어느 것입니까?",
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
                style_role="choice_label",
                x=26,
                y=62,
                font_size=22,
                fill="#2F80C9",
            ),
            TextSlot(
                id="slot.choice_1.expression",
                prompt="",
                text="320+145",
                style_role="choice",
                x=55,
                y=62,
                font_size=22,
                fill="#111111",
            ),
            TextSlot(
                id="slot.choice_2.number",
                prompt="",
                text="②",
                style_role="choice_label",
                x=26,
                y=92,
                font_size=22,
                fill="#2F80C9",
            ),
            TextSlot(
                id="slot.choice_2.expression",
                prompt="",
                text="300+200",
                style_role="choice",
                x=55,
                y=92,
                font_size=22,
                fill="#111111",
            ),
            TextSlot(
                id="slot.choice_3.number",
                prompt="",
                text="③",
                style_role="choice_label",
                x=26,
                y=122,
                font_size=22,
                fill="#2F80C9",
            ),
            TextSlot(
                id="slot.choice_3.expression",
                prompt="",
                text="163+326",
                style_role="choice",
                x=55,
                y=122,
                font_size=22,
                fill="#111111",
            ),
            TextSlot(
                id="slot.choice_4.number",
                prompt="",
                text="④",
                style_role="choice_label",
                x=26,
                y=152,
                font_size=22,
                fill="#2F80C9",
            ),
            TextSlot(
                id="slot.choice_4.expression",
                prompt="",
                text="236+362",
                style_role="choice",
                x=55,
                y=152,
                font_size=22,
                fill="#111111",
            ),
            TextSlot(
                id="slot.choice_5.number",
                prompt="",
                text="⑤",
                style_role="choice_label",
                x=26,
                y=182,
                font_size=22,
                fill="#2F80C9",
            ),
            TextSlot(
                id="slot.choice_5.expression",
                prompt="",
                text="405+104",
                style_role="choice",
                x=55,
                y=182,
                font_size=22,
                fill="#111111",
            ),
            BlankSlot(
                id="slot.answer",
                prompt="답",
                answer_key="4",
                placeholder="번",
            ),
        ),
    )


PROBLEM_TEMPLATE = build_problem_template()


ANSWER = {
    "type": "choice",
    "value": 4,
    "unit": "",
    "target_ref": "choice.option_4",
    "derived_from": "step.select_largest_sum",
}


SEMANTIC_OVERRIDE = {
    "problem_id": PROBLEM_ID,
    "problem_type": "multiple_choice_largest_sum_problem",
    "metadata": {
        "grade": 3,
        "semester": 1,
        "subject": "수학",
        "topic": "세 자리 수의 덧셈",
        "language": "ko-KR",
        "question": "다음 중 합이 가장 큰 것은 어느 것입니까?",
        "instruction": "각 덧셈식의 합을 구해 가장 큰 합을 고릅니다.",
    },
    "domain": {
        "objects": [
            {
                "id": "choice.option_1",
                "type": "addition_choice",
                "label": "① 320+145",
                "left": 320,
                "right": 145,
                "sum": 465,
            },
            {
                "id": "choice.option_2",
                "type": "addition_choice",
                "label": "② 300+200",
                "left": 300,
                "right": 200,
                "sum": 500,
            },
            {
                "id": "choice.option_3",
                "type": "addition_choice",
                "label": "③ 163+326",
                "left": 163,
                "right": 326,
                "sum": 489,
            },
            {
                "id": "choice.option_4",
                "type": "addition_choice",
                "label": "④ 236+362",
                "left": 236,
                "right": 362,
                "sum": 598,
            },
            {
                "id": "choice.option_5",
                "type": "addition_choice",
                "label": "⑤ 405+104",
                "left": 405,
                "right": 104,
                "sum": 509,
            },
        ],
        "relations": [
            {
                "id": "relation.option_4_has_largest_sum",
                "type": "maximum_of",
                "subject": "choice.option_4",
                "objects": [
                    "choice.option_1",
                    "choice.option_2",
                    "choice.option_3",
                    "choice.option_5",
                ],
            },
        ],
        "problem_solving": {
            "understand": {
                "given_refs": [
                    "choice.option_1",
                    "choice.option_2",
                    "choice.option_3",
                    "choice.option_4",
                    "choice.option_5",
                ],
                "target_ref": "choice.option_4",
                "condition_refs": ["relation.option_4_has_largest_sum"],
            },
            "plan": {
                "method": "calculate_and_compare_sums",
                "description": "각 보기의 합을 계산한 뒤 가장 큰 값을 찾습니다.",
            },
            "execute": {
                "expected_operations": ["addition", "comparison"],
            },
            "review": {
                "check_methods": ["recalculation", "maximum_comparison"],
            },
        },
    },
    "answer": ANSWER,
}


SOLVABLE = {
    "schema": "modu.solvable.v1.2",
    "problem_id": PROBLEM_ID,
    "problem_type": "multiple_choice_largest_sum_problem",
    "inputs": {
        "target_label": "합이 가장 큰 덧셈식의 보기 번호",
        "unit": "",
        "options": [
            {"number": 1, "expression": "320 + 145"},
            {"number": 2, "expression": "300 + 200"},
            {"number": 3, "expression": "163 + 326"},
            {"number": 4, "expression": "236 + 362"},
            {"number": 5, "expression": "405 + 104"},
        ],
    },
    "given": [
        {"ref": "choice.option_1", "value": "320 + 145"},
        {"ref": "choice.option_2", "value": "300 + 200"},
        {"ref": "choice.option_3", "value": "163 + 326"},
        {"ref": "choice.option_4", "value": "236 + 362"},
        {"ref": "choice.option_5", "value": "405 + 104"},
    ],
    "target": {
        "ref": "choice.option_4",
        "type": "choice",
    },
    "understanding": {
        "summary": "다섯 덧셈식의 합을 각각 구하고 그중 합이 가장 큰 식을 찾는 문제입니다.",
        "facts": [
            {
                "ref": "choice.option_1",
                "label": "첫 번째 덧셈식",
                "value": "320 + 145",
                "unit": "",
                "source": "explicit",
            },
            {
                "ref": "choice.option_2",
                "label": "두 번째 덧셈식",
                "value": "300 + 200",
                "unit": "",
                "source": "explicit",
            },
            {
                "ref": "choice.option_3",
                "label": "세 번째 덧셈식",
                "value": "163 + 326",
                "unit": "",
                "source": "explicit",
            },
            {
                "ref": "choice.option_4",
                "label": "네 번째 덧셈식",
                "value": "236 + 362",
                "unit": "",
                "source": "explicit",
            },
            {
                "ref": "choice.option_5",
                "label": "다섯 번째 덧셈식",
                "value": "405 + 104",
                "unit": "",
                "source": "explicit",
            },
        ],
        "unknowns": [
            {
                "ref": "choice.option_4",
                "label": "합이 가장 큰 덧셈식의 보기 번호",
                "unit": "",
            },
        ],
        "relation": {
            "type": "maximum_comparison",
            "statement": "각 보기의 합을 계산해 가장 큰 합을 가진 보기를 선택합니다.",
            "symbolic": "max(465, 500, 489, 598, 509) = 598",
            "uses": [
                "choice.option_1",
                "choice.option_2",
                "choice.option_3",
                "choice.option_4",
                "choice.option_5",
            ],
            "result": "choice.option_4",
        },
        "diagnostic_questions": [
            {
                "id": "understand.target",
                "type": "multiple_choice",
                "prompt": "이 문제에서 찾아야 하는 것은 무엇인가요?",
                "choices": [
                    "가장 작은 두 수",
                    "합이 가장 큰 덧셈식",
                    "첫 번째 덧셈식의 합",
                ],
                "answer_index": 1,
            },
            {
                "id": "understand.method",
                "type": "multiple_choice",
                "prompt": "합이 가장 큰 식을 정확하게 찾는 방법은 무엇인가요?",
                "choices": [
                    "각 보기의 합을 계산하여 비교합니다.",
                    "가장 큰 수가 하나라도 있는 보기를 고릅니다.",
                    "두 수의 차가 가장 큰 보기를 고릅니다.",
                ],
                "answer_index": 0,
            },
        ],
    },
    "method": "다섯 덧셈식의 합을 각각 계산하고 결과를 비교합니다.",
    "plan": [
        "각 보기의 덧셈을 계산합니다.",
        "계산한 다섯 합을 서로 비교합니다.",
        "가장 큰 합을 가진 보기 번호를 선택합니다.",
    ],
    "steps": [
        {
            "id": "step.calculate_option_1",
            "expr": "320 + 145",
            "value": 465,
            "explanation": "①의 합은 465입니다.",
        },
        {
            "id": "step.calculate_option_2",
            "expr": "300 + 200",
            "value": 500,
            "explanation": "②의 합은 500입니다.",
        },
        {
            "id": "step.calculate_option_3",
            "expr": "163 + 326",
            "value": 489,
            "explanation": "③의 합은 489입니다.",
        },
        {
            "id": "step.calculate_option_4",
            "expr": "236 + 362",
            "value": 598,
            "explanation": "④의 합은 598입니다.",
        },
        {
            "id": "step.calculate_option_5",
            "expr": "405 + 104",
            "value": 509,
            "explanation": "⑤의 합은 509입니다.",
        },
        {
            "id": "step.select_largest_sum",
            "expr": "max(465, 500, 489, 598, 509)",
            "value": 4,
            "explanation": "598이 가장 크므로 합이 가장 큰 식은 ④입니다.",
        },
    ],
    "checks": [
        {
            "id": "check.option_4_sum",
            "expr": "236 + 362",
            "expected": 598,
            "actual": 598,
            "pass": True,
        },
        {
            "id": "check.option_4_is_maximum",
            "expr": "598 > 465 and 598 > 500 and 598 > 489 and 598 > 509",
            "expected": True,
            "actual": True,
            "pass": True,
        },
    ],
    "answer": ANSWER,
}


SEMANTIC_ANSWER = SOLVABLE["answer"]
