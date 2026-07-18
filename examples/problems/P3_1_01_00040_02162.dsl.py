from __future__ import annotations

from modu_math.dsl import (
    BlankSlot,
    Canvas,
    Group,
    LineSlot,
    ProblemTemplate,
    Region,
    TextBoxSlot,
    TextSlot,
)

PROBLEM_ID = "P3_1_01_00040_02162"
PROBLEM_TITLE = "세 자리 수의 덧셈 계산"


def build_problem_template() -> ProblemTemplate:
    return ProblemTemplate(
        id=PROBLEM_ID,
        title=PROBLEM_TITLE,
        canvas=Canvas(
            width=360,
            height=145,
            coordinate_mode="logical",
        ),
        regions=(
            Region(
                id="region.stem",
                role="stem",
                flow="vertical",
                slot_ids=("slot.instruction",),
            ),
            Region(
                id="region.problems",
                role="diagram",
                flow="absolute",
                slot_ids=(
                    "slot.label_1",
                    "slot.addend_1_1",
                    "slot.plus_1",
                    "slot.addend_1_2",
                    "slot.line_1",
                    "slot.label_2",
                    "slot.addend_2_1",
                    "slot.plus_2",
                    "slot.addend_2_2",
                    "slot.line_2",
                ),
            ),
        ),
        slots=(
            TextBoxSlot(
                id="slot.instruction",
                text="다음 덧셈을 하시오.",
                prompt="두 개의 세 자리 수 덧셈을 계산하라는 안내",
                semantic_role="instruction",
                x=20,
                y=8,
                width=220,
                height=30,
                font_size=18,
                line_height=1.2,
                fill="#111111",
                align="left",
            ),
            # ---------------------------------------------------------
            # (1) 235 + 486
            # ---------------------------------------------------------
            TextSlot(
                id="slot.label_1",
                text="(1)",
                prompt="첫 번째 계산 번호",
                x=22,
                y=50,
                font_size=18,
                anchor="start",
                fill="#111111",
            ),
            TextSlot(
                id="slot.addend_1_1",
                text="235",
                prompt="첫 번째 덧셈의 위 수 235",
                x=100,
                y=50,
                font_size=21,
                anchor="end",
                fill="#111111",
            ),
            TextSlot(
                id="slot.plus_1",
                text="+",
                prompt="첫 번째 덧셈 기호",
                x=52,
                y=80,
                font_size=21,
                anchor="middle",
                fill="#111111",
            ),
            TextSlot(
                id="slot.addend_1_2",
                text="486",
                prompt="첫 번째 덧셈의 아래 수 486",
                x=100,
                y=80,
                font_size=21,
                anchor="end",
                fill="#111111",
            ),
            LineSlot(
                id="slot.line_1",
                prompt="첫 번째 세로셈의 계산선",
                x1=41,
                y1=94,
                x2=103,
                y2=94,
                stroke="#111111",
                stroke_width=1.5,
            ),
            BlankSlot(
                id="slot.answer_1",
                prompt="235와 486의 합",
                answer_key="721",
                placeholder="",
            ),
            # ---------------------------------------------------------
            # (2) 529 + 898
            # ---------------------------------------------------------
            TextSlot(
                id="slot.label_2",
                text="(2)",
                prompt="두 번째 계산 번호",
                x=145,
                y=50,
                font_size=18,
                anchor="start",
                fill="#111111",
            ),
            TextSlot(
                id="slot.addend_2_1",
                text="529",
                prompt="두 번째 덧셈의 위 수 529",
                x=223,
                y=50,
                font_size=21,
                anchor="end",
                fill="#111111",
            ),
            TextSlot(
                id="slot.plus_2",
                text="+",
                prompt="두 번째 덧셈 기호",
                x=175,
                y=80,
                font_size=21,
                anchor="middle",
                fill="#111111",
            ),
            TextSlot(
                id="slot.addend_2_2",
                text="898",
                prompt="두 번째 덧셈의 아래 수 898",
                x=223,
                y=80,
                font_size=21,
                anchor="end",
                fill="#111111",
            ),
            LineSlot(
                id="slot.line_2",
                prompt="두 번째 세로셈의 계산선",
                x1=164,
                y1=94,
                x2=226,
                y2=94,
                stroke="#111111",
                stroke_width=1.5,
            ),
            BlankSlot(
                id="slot.answer_2",
                prompt="529와 898의 합",
                answer_key="1427",
                placeholder="",
            ),
        ),
        diagrams=(),
        groups=(
            Group(
                id="group.problem_1",
                role="vertical_addition",
                member_ids=(
                    "slot.label_1",
                    "slot.addend_1_1",
                    "slot.plus_1",
                    "slot.addend_1_2",
                    "slot.line_1",
                    "slot.answer_1",
                ),
            ),
            Group(
                id="group.problem_2",
                role="vertical_addition",
                member_ids=(
                    "slot.label_2",
                    "slot.addend_2_1",
                    "slot.plus_2",
                    "slot.addend_2_2",
                    "slot.line_2",
                    "slot.answer_2",
                ),
            ),
        ),
        constraints=(),
        tags=(
            "grade-3",
            "addition",
            "three-digit-addition",
            "vertical-calculation",
            "numeric-answer",
        ),
    )


PROBLEM_TEMPLATE = build_problem_template()


SEMANTIC_OVERRIDE = {
    "problem_id": PROBLEM_ID,
    "problem_type": "multi_numeric_answer_addition",
    "metadata": {
        "grade": 3,
        "semester": 1,
        "subject": "수학",
        "topic": "세 자리 수의 덧셈",
        "language": "ko-KR",
        "question": "다음 덧셈을 하시오.",
    },
    "domain": {
        "objects": [
            {
                "id": "calculation.1",
                "type": "vertical_addition",
                "label": "첫 번째 덧셈",
                "addends": [235, 486],
            },
            {
                "id": "calculation.2",
                "type": "vertical_addition",
                "label": "두 번째 덧셈",
                "addends": [529, 898],
            },
        ],
        "relations": [
            {
                "id": "relation.1",
                "type": "addition",
                "from_ids": ["number.235", "number.486"],
                "to_id": "answer.1",
                "equation": "235 + 486 = 721",
            },
            {
                "id": "relation.2",
                "type": "addition",
                "from_ids": ["number.529", "number.898"],
                "to_id": "answer.2",
                "equation": "529 + 898 = 1427",
            },
        ],
    },
    "answer": {
        "blanks": [
            {"id": "slot.answer_1", "type": "number", "value": 721},
            {"id": "slot.answer_2", "type": "number", "value": 1427},
        ],
        "choices": [],
        "answer_key": [
            {"blank_id": "slot.answer_1", "value": 721},
            {"blank_id": "slot.answer_2", "value": 1427},
        ],
    },
}


SOLVABLE = {
    "schema": "modu.solvable.v1.2",
    "problem_id": PROBLEM_ID,
    "problem_type": "multi_numeric_answer_addition",
    "inputs": {
        "target_label": "각 덧셈의 계산 결과",
        "unit": "",
        "quantities": {
            "problem_1": {"addends": [235, 486]},
            "problem_2": {"addends": [529, 898]},
        },
        "conditions": [
            "같은 자리의 숫자끼리 맞추어 더합니다.",
            "각 자리의 합이 10 이상이면 바로 윗자리로 받아올림합니다.",
        ],
    },
    "given": [
        {"ref": "calculation.1", "value": {"addends": [235, 486]}},
        {"ref": "calculation.2", "value": {"addends": [529, 898]}},
    ],
    "target": {
        "ref": "answer.all",
        "type": "addition_results",
    },
    "understanding": {
        "summary": "두 개의 세 자리 수 덧셈을 계산하여 각각의 답을 구하는 문제입니다.",
        "facts": [
            {
                "ref": "calculation.1",
                "label": "첫 번째 덧셈식",
                "value": "235 + 486",
                "unit": "",
                "source": "explicit",
            },
            {
                "ref": "calculation.2",
                "label": "두 번째 덧셈식",
                "value": "529 + 898",
                "unit": "",
                "source": "explicit",
            },
        ],
        "unknowns": [
            {
                "ref": "answer.1",
                "label": "235 + 486의 계산 결과",
                "unit": "",
                "source": "unknown",
            },
            {
                "ref": "answer.2",
                "label": "529 + 898의 계산 결과",
                "unit": "",
                "source": "unknown",
            },
        ],
        "relation": {
            "type": "place_value_addition",
            "statement": "일의 자리부터 더하고, 합이 10 이상이면 받아올림하여 다음 자리 계산에 더합니다.",
            "symbolic": "ones -> tens -> hundreds -> thousands",
            "uses": [
                "calculation.1",
                "calculation.2",
            ],
            "result": "answer.all",
        },
        "diagnostic_questions": [
            {
                "id": "understand.target",
                "type": "multiple_choice",
                "prompt": "이 문제에서 구해야 하는 것은 무엇인가요?",
                "choices": [
                    "각 덧셈식의 계산 결과",
                    "두 수의 차",
                    "가장 큰 수",
                ],
                "answer_index": 0,
            },
            {
                "id": "understand.method",
                "type": "multiple_choice",
                "prompt": "세 자리 수 덧셈은 어느 자리부터 계산하나요?",
                "choices": [
                    "일의 자리",
                    "백의 자리",
                    "가장 큰 숫자가 있는 자리",
                ],
                "answer_index": 0,
            },
        ],
        "student_restatement": {
            "prompt": "문제의 뜻을 말해 볼까요?",
            "template": "두 덧셈식 {exprs}의 값을 각각 계산합니다.",
            "answer": "235+486과 529+898을 각각 계산합니다.",
        },
    },
    "method": "같은 자리끼리 맞추어 일의 자리부터 더하고, 받아올림을 반영해 계산합니다.",
    "plan": [
        "각 덧셈식의 숫자를 같은 자리끼리 맞춥니다.",
        "일의 자리부터 차례로 더합니다.",
        "합이 10 이상이면 받아올림을 다음 자리 계산에 더합니다.",
        "각 덧셈식의 결과를 답으로 씁니다.",
    ],
    "steps": [
        {
            "id": "step.1",
            "goal": "235 + 486을 계산합니다.",
            "uses": ["calculation.1"],
            "expr": "235 + 486",
            "value": {"sum": 721, "ref": "answer.1"},
            "explanation": "일의 자리 5+6=11에서 1을 쓰고 1을 받아올림합니다. 십의 자리 3+8+1=12에서 2를 쓰고 1을 받아올림합니다. 백의 자리 2+4+1=7이므로 721입니다.",
        },
        {
            "id": "step.2",
            "goal": "529 + 898을 계산합니다.",
            "uses": ["calculation.2"],
            "expr": "529 + 898",
            "value": {"sum": 1427, "ref": "answer.2"},
            "explanation": "일의 자리 9+8=17에서 7을 쓰고 1을 받아올림합니다. 십의 자리 2+9+1=12에서 2를 쓰고 1을 받아올림합니다. 백의 자리 5+8+1=14이므로 1427입니다.",
        },
    ],
    "checks": [
        {
            "id": "check.1",
            "description": "721에서 486을 빼면 235가 됩니다.",
            "expr": "721 - 486",
            "expected": 235,
            "actual": 235,
            "pass": True,
        },
        {
            "id": "check.2",
            "description": "1427에서 898을 빼면 529가 됩니다.",
            "expr": "1427 - 898",
            "expected": 529,
            "actual": 529,
            "pass": True,
        },
    ],
    "answer": {
        "blanks": [
            {"id": "slot.answer_1", "type": "number", "value": 721, "unit": ""},
            {"id": "slot.answer_2", "type": "number", "value": 1427, "unit": ""},
        ],
        "choices": [],
        "answer_key": [
            {"blank_id": "slot.answer_1", "value": 721, "unit": ""},
            {"blank_id": "slot.answer_2", "value": 1427, "unit": ""},
        ],
        "value": [721, 1427],
        "unit": "",
        "sentence": "(1) 721, (2) 1427입니다.",
    },
}


SOLVABLE.update(
    {
        "inputs": {
            "target_label": "각 덧셈의 계산 결과",
            "unit": "",
            "quantities": {
                "problem_1": {"addends": [235, 486]},
                "problem_2": {"addends": [529, 898]},
            },
            "conditions": [
                "같은 자리의 숫자끼리 맞추어 더합니다.",
                "일의 자리부터 차례대로 계산합니다.",
                "각 자리의 합이 10 이상이면 바로 윗자리로 1을 받아올림합니다.",
            ],
        },
        "given": [
            {"ref": "calculation.1", "value": {"addends": [235, 486]}},
            {"ref": "calculation.2", "value": {"addends": [529, 898]}},
        ],
        "target": {
            "ref": "answer.all",
            "type": "addition_results",
        },
        "understanding": {
            "summary": "두 개의 세 자리 수 덧셈을 계산해 각각의 답을 구하는 문제입니다.",
            "facts": [
                {
                    "ref": "calculation.1",
                    "label": "첫 번째 덧셈식",
                    "value": "235 + 486",
                    "unit": "",
                    "source": "explicit",
                },
                {
                    "ref": "calculation.2",
                    "label": "두 번째 덧셈식",
                    "value": "529 + 898",
                    "unit": "",
                    "source": "explicit",
                },
            ],
            "unknowns": [
                {
                    "ref": "answer.1",
                    "label": "235 + 486의 계산 결과",
                    "unit": "",
                    "source": "unknown",
                },
                {
                    "ref": "answer.2",
                    "label": "529 + 898의 계산 결과",
                    "unit": "",
                    "source": "unknown",
                },
            ],
            "relation": {
                "type": "place_value_addition",
                "statement": "일의 자리부터 더하고, 합이 10 이상이면 받아올림하여 다음 자리 계산에 더합니다.",
                "symbolic": "ones -> tens -> hundreds -> thousands",
                "uses": ["calculation.1", "calculation.2"],
                "result": "answer.all",
            },
            "diagnostic_questions": [
                {
                    "id": "understand.target",
                    "type": "multiple_choice",
                    "prompt": "이 문제에서 구해야 하는 것은 무엇인가요?",
                    "choices": ["각 덧셈식의 계산 결과", "두 수의 차", "가장 큰 수"],
                    "answer_index": 0,
                },
                {
                    "id": "understand.method",
                    "type": "multiple_choice",
                    "prompt": "세 자리 수 덧셈은 어느 자리부터 계산하나요?",
                    "choices": ["일의 자리", "백의 자리", "가장 큰 숫자가 있는 자리"],
                    "answer_index": 0,
                },
            ],
            "student_restatement": {
                "prompt": "문제의 뜻을 말해 볼까요?",
                "template": "두 덧셈식 {exprs}의 값을 각각 계산합니다.",
                "answer": "235 + 486과 529 + 898을 각각 계산합니다.",
            },
        },
        "method": "같은 자리끼리 맞추어 일의 자리부터 더하고, 받아올림을 반영해 계산합니다.",
        "plan": [
            "각 덧셈식의 숫자를 같은 자리끼리 맞춥니다.",
            "일의 자리부터 차례로 더합니다.",
            "합이 10 이상이면 받아올림을 다음 자리 계산에 더합니다.",
            "각 덧셈식의 결과를 답으로 씁니다.",
        ],
        "steps": [
            {
                "id": "step.problem_1",
                "goal": "235 + 486을 계산합니다.",
                "uses": ["calculation.1"],
                "expr": "235 + 486",
                "value": {"sum": 721, "ref": "answer.1"},
                "explanation": "일의 자리 5 + 6 = 11에서 1을 쓰고 1을 받아올림합니다. 십의 자리 3 + 8 + 1 = 12에서 2를 쓰고 1을 받아올림합니다. 백의 자리 2 + 4 + 1 = 7이므로 235 + 486 = 721입니다.",
            },
            {
                "id": "step.problem_2",
                "goal": "529 + 898을 계산합니다.",
                "uses": ["calculation.2"],
                "expr": "529 + 898",
                "value": {"sum": 1427, "ref": "answer.2"},
                "explanation": "일의 자리 9 + 8 = 17에서 7을 쓰고 1을 받아올림합니다. 십의 자리 2 + 9 + 1 = 12에서 2를 쓰고 1을 받아올림합니다. 백의 자리 5 + 8 + 1 = 14이므로 529 + 898 = 1427입니다.",
            },
        ],
        "checks": [
            {
                "id": "check.problem_1",
                "description": "721에서 486을 빼면 235가 되는지 확인합니다.",
                "expr": "721 - 486",
                "expected": 235,
                "actual": 235,
                "pass": True,
            },
            {
                "id": "check.problem_2",
                "description": "1427에서 898을 빼면 529가 되는지 확인합니다.",
                "expr": "1427 - 898",
                "expected": 529,
                "actual": 529,
                "pass": True,
            },
        ],
        "answer": {
            "blanks": [
                {"id": "slot.answer_1", "type": "number", "value": 721, "unit": ""},
                {"id": "slot.answer_2", "type": "number", "value": 1427, "unit": ""},
            ],
            "choices": [],
            "answer_key": [
                {"blank_id": "slot.answer_1", "value": 721, "unit": ""},
                {"blank_id": "slot.answer_2", "value": 1427, "unit": ""},
            ],
            "value": [721, 1427],
            "unit": "",
            "sentence": "(1) 721, (2) 1427입니다.",
        },
    }
)


SEMANTIC_OVERRIDE["answer"] = SOLVABLE["answer"]
