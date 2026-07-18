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

PROBLEM_ID = "P3_1_01_00040_02155"
PROBLEM_TITLE = "세 자리 수의 덧셈 계산"


def build_problem_template() -> ProblemTemplate:
    return ProblemTemplate(
        id=PROBLEM_ID,
        title=PROBLEM_TITLE,
        canvas=Canvas(
            width=760,
            height=250,
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
                    "slot.label_3",
                    "slot.addend_3_1",
                    "slot.plus_3",
                    "slot.addend_3_2",
                    "slot.line_3",
                ),
            ),
        ),
        slots=(
            TextBoxSlot(
                id="slot.instruction",
                text="다음을 계산하세요.",
                prompt="세 개의 세 자리 수 덧셈을 계산하라는 안내",
                semantic_role="instruction",
                x=24,
                y=18,
                width=300,
                height=38,
                font_size=25,
                line_height=1.2,
                fill="#111111",
                align="left",
            ),
            # ---------------------------------------------------------
            # (1) 379 + 855
            # ---------------------------------------------------------
            TextSlot(
                id="slot.label_1",
                text="(1)",
                prompt="첫 번째 계산 번호",
                x=40,
                y=88,
                font_size=24,
                anchor="start",
                fill="#111111",
            ),
            TextSlot(
                id="slot.addend_1_1",
                text="379",
                prompt="첫 번째 덧셈의 위 수 379",
                x=176,
                y=88,
                font_size=28,
                anchor="end",
                fill="#111111",
            ),
            TextSlot(
                id="slot.plus_1",
                text="+",
                prompt="첫 번째 덧셈 기호",
                x=111,
                y=135,
                font_size=28,
                anchor="middle",
                fill="#111111",
            ),
            TextSlot(
                id="slot.addend_1_2",
                text="855",
                prompt="첫 번째 덧셈의 아래 수 855",
                x=176,
                y=135,
                font_size=28,
                anchor="end",
                fill="#111111",
            ),
            LineSlot(
                id="slot.line_1",
                prompt="첫 번째 세로셈의 계산선",
                x1=91,
                y1=151,
                x2=188,
                y2=151,
                stroke="#111111",
                stroke_width=2,
            ),
            BlankSlot(
                id="slot.answer_1",
                prompt="379와 855의 합",
                answer_key="1234",
                placeholder="",
            ),
            # ---------------------------------------------------------
            # (2) 654 + 758
            # ---------------------------------------------------------
            TextSlot(
                id="slot.label_2",
                text="(2)",
                prompt="두 번째 계산 번호",
                x=260,
                y=88,
                font_size=24,
                anchor="start",
                fill="#111111",
            ),
            TextSlot(
                id="slot.addend_2_1",
                text="654",
                prompt="두 번째 덧셈의 위 수 654",
                x=396,
                y=88,
                font_size=28,
                anchor="end",
                fill="#111111",
            ),
            TextSlot(
                id="slot.plus_2",
                text="+",
                prompt="두 번째 덧셈 기호",
                x=331,
                y=135,
                font_size=28,
                anchor="middle",
                fill="#111111",
            ),
            TextSlot(
                id="slot.addend_2_2",
                text="758",
                prompt="두 번째 덧셈의 아래 수 758",
                x=396,
                y=135,
                font_size=28,
                anchor="end",
                fill="#111111",
            ),
            LineSlot(
                id="slot.line_2",
                prompt="두 번째 세로셈의 계산선",
                x1=311,
                y1=151,
                x2=408,
                y2=151,
                stroke="#111111",
                stroke_width=2,
            ),
            BlankSlot(
                id="slot.answer_2",
                prompt="654와 758의 합",
                answer_key="1412",
                placeholder="",
            ),
            # ---------------------------------------------------------
            # (3) 296 + 758
            # ---------------------------------------------------------
            TextSlot(
                id="slot.label_3",
                text="(3)",
                prompt="세 번째 계산 번호",
                x=480,
                y=88,
                font_size=24,
                anchor="start",
                fill="#111111",
            ),
            TextSlot(
                id="slot.addend_3_1",
                text="296",
                prompt="세 번째 덧셈의 위 수 296",
                x=616,
                y=88,
                font_size=28,
                anchor="end",
                fill="#111111",
            ),
            TextSlot(
                id="slot.plus_3",
                text="+",
                prompt="세 번째 덧셈 기호",
                x=551,
                y=135,
                font_size=28,
                anchor="middle",
                fill="#111111",
            ),
            TextSlot(
                id="slot.addend_3_2",
                text="758",
                prompt="세 번째 덧셈의 아래 수 758",
                x=616,
                y=135,
                font_size=28,
                anchor="end",
                fill="#111111",
            ),
            LineSlot(
                id="slot.line_3",
                prompt="세 번째 세로셈의 계산선",
                x1=531,
                y1=151,
                x2=628,
                y2=151,
                stroke="#111111",
                stroke_width=2,
            ),
            BlankSlot(
                id="slot.answer_3",
                prompt="296과 758의 합",
                answer_key="1054",
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
            Group(
                id="group.problem_3",
                role="vertical_addition",
                member_ids=(
                    "slot.label_3",
                    "slot.addend_3_1",
                    "slot.plus_3",
                    "slot.addend_3_2",
                    "slot.line_3",
                    "slot.answer_3",
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
    "problem_type": "multi_numeric_answer_vertical_addition",
    "metadata": {
        "grade": 3,
        "semester": 1,
        "subject": "수학",
        "topic": "세 자리 수의 덧셈",
        "language": "ko-KR",
        "question": "다음을 계산하세요.",
    },
    "domain": {
        "objects": [
            {
                "id": "calculation.1",
                "type": "vertical_addition",
                "label": "첫 번째 덧셈",
                "addends": [379, 855],
            },
            {
                "id": "calculation.2",
                "type": "vertical_addition",
                "label": "두 번째 덧셈",
                "addends": [654, 758],
            },
            {
                "id": "calculation.3",
                "type": "vertical_addition",
                "label": "세 번째 덧셈",
                "addends": [296, 758],
            },
        ],
        "relations": [
            {
                "id": "relation.1",
                "type": "addition",
                "from_ids": ["number.379", "number.855"],
                "to_id": "answer.1",
                "equation": "379 + 855 = 1234",
            },
            {
                "id": "relation.2",
                "type": "addition",
                "from_ids": ["number.654", "number.758"],
                "to_id": "answer.2",
                "equation": "654 + 758 = 1412",
            },
            {
                "id": "relation.3",
                "type": "addition",
                "from_ids": ["number.296", "number.758"],
                "to_id": "answer.3",
                "equation": "296 + 758 = 1054",
            },
        ],
    },
    "answer": {
        "blanks": [
            {"id": "slot.answer_1", "type": "number", "value": 1234},
            {"id": "slot.answer_2", "type": "number", "value": 1412},
            {"id": "slot.answer_3", "type": "number", "value": 1054},
        ],
        "choices": [],
        "answer_key": [
            {"blank_id": "slot.answer_1", "value": 1234},
            {"blank_id": "slot.answer_2", "value": 1412},
            {"blank_id": "slot.answer_3", "value": 1054},
        ],
    },
}

SOLVABLE = {
    "schema": "modu.solvable.v1.2",
    "problem_id": PROBLEM_ID,
    "problem_type": "multi_numeric_answer_vertical_addition",
    "inputs": {
        "target_label": "각 덧셈의 계산 결과",
        "quantities": {
            "problem_1": {"addends": [379, 855]},
            "problem_2": {"addends": [654, 758]},
            "problem_3": {"addends": [296, 758]},
        },
        "conditions": [
            "같은 자리의 숫자끼리 맞추어 더합니다.",
            "각 자리의 합이 10 이상이면 바로 윗자리로 받아올림합니다.",
        ],
    },
    "given": [
        {"ref": "calculation.1", "value": {"addends": [379, 855]}},
        {"ref": "calculation.2", "value": {"addends": [654, 758]}},
        {"ref": "calculation.3", "value": {"addends": [296, 758]}},
    ],
    "target": {
        "ref": "answer.all",
        "type": "addition_results",
    },
    "understanding": {
        "summary": "세로로 놓인 세 자리 수끼리 일의 자리부터 차례대로 더하는 문제입니다.",
        "facts": [
            {
                "ref": "rule.place_value_alignment",
                "label": "자리 맞추기",
                "source": "implicit",
                "meaning": "일의 자리, 십의 자리, 백의 자리를 각각 맞추어 계산합니다.",
            },
            {
                "ref": "rule.carrying",
                "label": "받아올림",
                "source": "implicit",
                "meaning": "한 자리의 합이 10 이상이면 십의 자리 숫자를 다음 자리로 올립니다.",
            },
        ],
        "unknowns": [
            {"ref": "answer.1", "label": "379 + 855의 값"},
            {"ref": "answer.2", "label": "654 + 758의 값"},
            {"ref": "answer.3", "label": "296 + 758의 값"},
        ],
        "relation": {
            "type": "place_value_addition",
            "statement": "일의 자리부터 더하고 받아올림을 다음 자리에 더합니다.",
            "symbolic": "ones → tens → hundreds → thousands",
            "uses": ["rule.place_value_alignment", "rule.carrying"],
            "result": "answer.all",
        },
    },
    "method": "vertical_addition_with_carrying",
    "plan": [
        "두 수의 같은 자리끼리 맞춥니다.",
        "일의 자리부터 더합니다.",
        "합이 10 이상이면 받아올림합니다.",
        "십의 자리와 백의 자리를 차례대로 계산합니다.",
    ],
    "steps": [
        {
            "id": "step.1",
            "goal": "379 + 855를 계산합니다.",
            "uses": ["calculation.1"],
            "expr": "379 + 855",
            "substeps": [
                "9 + 5 = 14이므로 4를 쓰고 1을 받아올림합니다.",
                "7 + 5 + 1 = 13이므로 3을 쓰고 1을 받아올림합니다.",
                "3 + 8 + 1 = 12입니다.",
            ],
            "value": {"sum": 1234, "ref": "answer.1"},
            "explanation": "각 자리의 받아올림을 반영하면 1234입니다.",
        },
        {
            "id": "step.2",
            "goal": "654 + 758을 계산합니다.",
            "uses": ["calculation.2"],
            "expr": "654 + 758",
            "substeps": [
                "4 + 8 = 12이므로 2를 쓰고 1을 받아올림합니다.",
                "5 + 5 + 1 = 11이므로 1을 쓰고 1을 받아올림합니다.",
                "6 + 7 + 1 = 14입니다.",
            ],
            "value": {"sum": 1412, "ref": "answer.2"},
            "explanation": "각 자리의 받아올림을 반영하면 1412입니다.",
        },
        {
            "id": "step.3",
            "goal": "296 + 758을 계산합니다.",
            "uses": ["calculation.3"],
            "expr": "296 + 758",
            "substeps": [
                "6 + 8 = 14이므로 4를 쓰고 1을 받아올림합니다.",
                "9 + 5 + 1 = 15이므로 5를 쓰고 1을 받아올림합니다.",
                "2 + 7 + 1 = 10입니다.",
            ],
            "value": {"sum": 1054, "ref": "answer.3"},
            "explanation": "각 자리의 받아올림을 반영하면 1054입니다.",
        },
    ],
    "checks": [
        {
            "id": "check.1",
            "description": "1234에서 855를 빼서 첫 번째 덧셈을 확인합니다.",
            "expr": "1234 - 855",
            "expected": 379,
            "actual": 379,
            "pass": True,
        },
        {
            "id": "check.2",
            "description": "1412에서 758을 빼서 두 번째 덧셈을 확인합니다.",
            "expr": "1412 - 758",
            "expected": 654,
            "actual": 654,
            "pass": True,
        },
        {
            "id": "check.3",
            "description": "1054에서 758을 빼서 세 번째 덧셈을 확인합니다.",
            "expr": "1054 - 758",
            "expected": 296,
            "actual": 296,
            "pass": True,
        },
    ],
    "answer": {
        "blanks": [
            {"id": "slot.answer_1", "type": "number", "value": 1234},
            {"id": "slot.answer_2", "type": "number", "value": 1412},
            {"id": "slot.answer_3", "type": "number", "value": 1054},
        ],
        "choices": [],
        "answer_key": [
            {"blank_id": "slot.answer_1", "value": 1234},
            {"blank_id": "slot.answer_2", "value": 1412},
            {"blank_id": "slot.answer_3", "value": 1054},
        ],
        "value": [1234, 1412, 1054],
        "sentence": "(1) 1234, (2) 1412, (3) 1054입니다.",
    },
}

SOLVABLE.update(
    {
        "inputs": {
            "target_label": "각 덧셈의 계산 결과",
            "unit": "",
            "quantities": {
                "problem_1": {"addends": [379, 855]},
                "problem_2": {"addends": [654, 758]},
                "problem_3": {"addends": [296, 758]},
            },
            "conditions": [
                "같은 자리의 숫자끼리 맞추어 더합니다.",
                "각 자리의 합이 10 이상이면 바로 윗자리로 받아올림합니다.",
            ],
        },
        "given": [
            {"ref": "calculation.1", "value": {"addends": [379, 855]}},
            {"ref": "calculation.2", "value": {"addends": [654, 758]}},
            {"ref": "calculation.3", "value": {"addends": [296, 758]}},
        ],
        "target": {"ref": "answer.all", "type": "addition_results"},
        "understanding": {
            "summary": "세 개의 세 자리 수 덧셈을 차례로 계산해 각 빈칸에 알맞은 합을 쓰는 문제입니다.",
            "facts": [
                {
                    "ref": "calculation.1",
                    "label": "첫 번째 덧셈식",
                    "value": "379 + 855",
                    "unit": "",
                    "source": "explicit",
                },
                {
                    "ref": "calculation.2",
                    "label": "두 번째 덧셈식",
                    "value": "654 + 758",
                    "unit": "",
                    "source": "explicit",
                },
                {
                    "ref": "calculation.3",
                    "label": "세 번째 덧셈식",
                    "value": "296 + 758",
                    "unit": "",
                    "source": "explicit",
                },
            ],
            "unknowns": [
                {
                    "ref": "answer.1",
                    "label": "379 + 855의 계산 결과",
                    "unit": "",
                    "source": "unknown",
                },
                {
                    "ref": "answer.2",
                    "label": "654 + 758의 계산 결과",
                    "unit": "",
                    "source": "unknown",
                },
                {
                    "ref": "answer.3",
                    "label": "296 + 758의 계산 결과",
                    "unit": "",
                    "source": "unknown",
                },
            ],
            "relation": {
                "type": "place_value_addition",
                "statement": "일의 자리부터 더하고, 합이 10 이상이면 받아올림하여 다음 자리 계산에 더합니다.",
                "symbolic": "ones -> tens -> hundreds -> thousands",
                "uses": ["calculation.1", "calculation.2", "calculation.3"],
                "result": "answer.all",
            },
            "diagnostic_questions": [
                {
                    "id": "understand.target",
                    "type": "multiple_choice",
                    "prompt": "이 문제에서 구해야 하는 것은 무엇인가요?",
                    "choices": [
                        "각 덧셈식의 계산 결과",
                        "덧셈식에 들어갈 숫자",
                        "가장 큰 덧셈식 하나",
                    ],
                    "answer_index": 0,
                },
                {
                    "id": "understand.method",
                    "type": "multiple_choice",
                    "prompt": "세 자리 수 덧셈은 어느 자리부터 계산하나요?",
                    "choices": ["일의 자리", "백의 자리", "큰 수가 있는 자리"],
                    "answer_index": 0,
                },
            ],
            "student_restatement": {
                "prompt": "문제의 뜻을 말해 볼까요?",
                "template": "세 덧셈식 {exprs}의 값을 각각 계산합니다.",
                "answer": "379+855, 654+758, 296+758을 각각 계산해 빈칸에 씁니다.",
            },
        },
        "method": "같은 자리끼리 맞추어 일의 자리부터 더하고, 받아올림을 반영해 계산합니다.",
        "plan": [
            "각 덧셈식의 숫자를 같은 자리끼리 맞춥니다.",
            "일의 자리부터 차례로 더합니다.",
            "합이 10 이상이면 받아올림을 다음 자리 계산에 더합니다.",
            "각 덧셈식의 결과를 빈칸에 씁니다.",
        ],
        "steps": [
            {
                "id": "step.1",
                "goal": "379 + 855를 계산합니다.",
                "uses": ["calculation.1"],
                "expr": "379 + 855",
                "value": {"sum": 1234, "ref": "answer.1"},
                "explanation": "일의 자리 9+5=14에서 4를 쓰고 1을 받아올림합니다. 십의 자리 7+5+1=13에서 3을 쓰고 1을 받아올림합니다. 백의 자리 3+8+1=12이므로 379 + 855 = 1234입니다.",
            },
            {
                "id": "step.2",
                "goal": "654 + 758을 계산합니다.",
                "uses": ["calculation.2"],
                "expr": "654 + 758",
                "value": {"sum": 1412, "ref": "answer.2"},
                "explanation": "일의 자리 4+8=12에서 2를 쓰고 1을 받아올림합니다. 십의 자리 5+5+1=11에서 1을 쓰고 1을 받아올림합니다. 백의 자리 6+7+1=14이므로 654 + 758 = 1412입니다.",
            },
            {
                "id": "step.3",
                "goal": "296 + 758을 계산합니다.",
                "uses": ["calculation.3"],
                "expr": "296 + 758",
                "value": {"sum": 1054, "ref": "answer.3"},
                "explanation": "일의 자리 6+8=14에서 4를 쓰고 1을 받아올림합니다. 십의 자리 9+5+1=15에서 5를 쓰고 1을 받아올림합니다. 백의 자리 2+7+1=10이므로 296 + 758 = 1054입니다.",
            },
        ],
        "checks": [
            {
                "id": "check.1",
                "description": "1234에서 855를 빼면 첫 번째 덧셈식의 다른 수인 379가 됩니다.",
                "expr": "1234 - 855",
                "expected": 379,
                "actual": 379,
                "pass": True,
            },
            {
                "id": "check.2",
                "description": "1412에서 758을 빼면 두 번째 덧셈식의 다른 수인 654가 됩니다.",
                "expr": "1412 - 758",
                "expected": 654,
                "actual": 654,
                "pass": True,
            },
            {
                "id": "check.3",
                "description": "1054에서 758을 빼면 세 번째 덧셈식의 다른 수인 296이 됩니다.",
                "expr": "1054 - 758",
                "expected": 296,
                "actual": 296,
                "pass": True,
            },
        ],
        "answer": {
            "blanks": [
                {"id": "slot.answer_1", "type": "number", "value": 1234, "unit": ""},
                {"id": "slot.answer_2", "type": "number", "value": 1412, "unit": ""},
                {"id": "slot.answer_3", "type": "number", "value": 1054, "unit": ""},
            ],
            "choices": [],
            "answer_key": [
                {"blank_id": "slot.answer_1", "value": 1234, "unit": ""},
                {"blank_id": "slot.answer_2", "value": 1412, "unit": ""},
                {"blank_id": "slot.answer_3", "value": 1054, "unit": ""},
            ],
            "value": [1234, 1412, 1054],
            "unit": "",
            "sentence": "(1) 1234, (2) 1412, (3) 1054입니다.",
        },
    }
)

SEMANTIC_OVERRIDE["answer"] = SOLVABLE["answer"]
