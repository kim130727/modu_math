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

PROBLEM_ID = "P3_1_01_00040_02158"
PROBLEM_TITLE = "세 자리 수의 덧셈 계산"


def build_problem_template() -> ProblemTemplate:
    return ProblemTemplate(
        id=PROBLEM_ID,
        title=PROBLEM_TITLE,
        canvas=Canvas(
            width=620,
            height=170,
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
                    "slot.expression_3",
                    "slot.label_4",
                    "slot.expression_4",
                ),
            ),
        ),
        slots=(
            TextBoxSlot(
                id="slot.instruction",
                text="다음을 계산하세요.",
                prompt="네 개의 세 자리 수 덧셈을 계산하라는 안내",
                semantic_role="instruction",
                x=20,
                y=6,
                width=260,
                height=30,
                font_size=18,
                line_height=1.2,
                fill="#111111",
                align="left",
            ),
            # ---------------------------------------------------------
            # (1) 286 + 435
            # ---------------------------------------------------------
            TextSlot(
                id="slot.label_1",
                text="(1)",
                prompt="첫 번째 계산 번호",
                x=22,
                y=42,
                font_size=18,
                anchor="start",
                fill="#111111",
            ),
            TextSlot(
                id="slot.addend_1_1",
                text="286",
                prompt="첫 번째 덧셈의 위 수 286",
                x=99,
                y=42,
                font_size=21,
                anchor="end",
                fill="#111111",
            ),
            TextSlot(
                id="slot.plus_1",
                text="+",
                prompt="첫 번째 덧셈 기호",
                x=51,
                y=70,
                font_size=21,
                anchor="middle",
                fill="#111111",
            ),
            TextSlot(
                id="slot.addend_1_2",
                text="435",
                prompt="첫 번째 덧셈의 아래 수 435",
                x=99,
                y=70,
                font_size=21,
                anchor="end",
                fill="#111111",
            ),
            LineSlot(
                id="slot.line_1",
                prompt="첫 번째 세로셈의 계산선",
                x1=41,
                y1=82,
                x2=102,
                y2=82,
                stroke="#111111",
                stroke_width=1.5,
            ),
            BlankSlot(
                id="slot.answer_1",
                prompt="286과 435의 합",
                answer_key="721",
                placeholder="",
            ),
            # ---------------------------------------------------------
            # (2) 479 + 837
            # ---------------------------------------------------------
            TextSlot(
                id="slot.label_2",
                text="(2)",
                prompt="두 번째 계산 번호",
                x=176,
                y=42,
                font_size=18,
                anchor="start",
                fill="#111111",
            ),
            TextSlot(
                id="slot.addend_2_1",
                text="479",
                prompt="두 번째 덧셈의 위 수 479",
                x=253,
                y=42,
                font_size=21,
                anchor="end",
                fill="#111111",
            ),
            TextSlot(
                id="slot.plus_2",
                text="+",
                prompt="두 번째 덧셈 기호",
                x=205,
                y=70,
                font_size=21,
                anchor="middle",
                fill="#111111",
            ),
            TextSlot(
                id="slot.addend_2_2",
                text="837",
                prompt="두 번째 덧셈의 아래 수 837",
                x=253,
                y=70,
                font_size=21,
                anchor="end",
                fill="#111111",
            ),
            LineSlot(
                id="slot.line_2",
                prompt="두 번째 세로셈의 계산선",
                x1=195,
                y1=82,
                x2=256,
                y2=82,
                stroke="#111111",
                stroke_width=1.5,
            ),
            BlankSlot(
                id="slot.answer_2",
                prompt="479와 837의 합",
                answer_key="1316",
                placeholder="",
            ),
            # ---------------------------------------------------------
            # (3) 296 + 638
            # ---------------------------------------------------------
            TextSlot(
                id="slot.label_3",
                text="(3)",
                prompt="세 번째 계산 번호",
                x=22,
                y=130,
                font_size=18,
                anchor="start",
                fill="#111111",
            ),
            TextSlot(
                id="slot.expression_3",
                text="296 + 638",
                prompt="세 번째 덧셈식 296 더하기 638",
                x=82,
                y=130,
                font_size=20,
                anchor="start",
                fill="#111111",
            ),
            BlankSlot(
                id="slot.answer_3",
                prompt="296과 638의 합",
                answer_key="934",
                placeholder="",
            ),
            # ---------------------------------------------------------
            # (4) 864 + 459
            # ---------------------------------------------------------
            TextSlot(
                id="slot.label_4",
                text="(4)",
                prompt="네 번째 계산 번호",
                x=176,
                y=130,
                font_size=18,
                anchor="start",
                fill="#111111",
            ),
            TextSlot(
                id="slot.expression_4",
                text="864 + 459",
                prompt="네 번째 덧셈식 864 더하기 459",
                x=236,
                y=130,
                font_size=20,
                anchor="start",
                fill="#111111",
            ),
            BlankSlot(
                id="slot.answer_4",
                prompt="864와 459의 합",
                answer_key="1323",
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
                role="horizontal_addition",
                member_ids=(
                    "slot.label_3",
                    "slot.expression_3",
                    "slot.answer_3",
                ),
            ),
            Group(
                id="group.problem_4",
                role="horizontal_addition",
                member_ids=(
                    "slot.label_4",
                    "slot.expression_4",
                    "slot.answer_4",
                ),
            ),
        ),
        constraints=(),
        tags=(
            "grade-3",
            "addition",
            "three-digit-addition",
            "vertical-calculation",
            "horizontal-calculation",
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
        "question": "다음을 계산하세요.",
    },
    "domain": {
        "objects": [
            {
                "id": "calculation.1",
                "type": "vertical_addition",
                "label": "첫 번째 덧셈",
                "addends": [286, 435],
            },
            {
                "id": "calculation.2",
                "type": "vertical_addition",
                "label": "두 번째 덧셈",
                "addends": [479, 837],
            },
            {
                "id": "calculation.3",
                "type": "horizontal_addition",
                "label": "세 번째 덧셈",
                "addends": [296, 638],
            },
            {
                "id": "calculation.4",
                "type": "horizontal_addition",
                "label": "네 번째 덧셈",
                "addends": [864, 459],
            },
        ],
        "relations": [
            {
                "id": "relation.1",
                "type": "addition",
                "from_ids": ["number.286", "number.435"],
                "to_id": "answer.1",
                "equation": "286 + 435 = 721",
            },
            {
                "id": "relation.2",
                "type": "addition",
                "from_ids": ["number.479", "number.837"],
                "to_id": "answer.2",
                "equation": "479 + 837 = 1316",
            },
            {
                "id": "relation.3",
                "type": "addition",
                "from_ids": ["number.296", "number.638"],
                "to_id": "answer.3",
                "equation": "296 + 638 = 934",
            },
            {
                "id": "relation.4",
                "type": "addition",
                "from_ids": ["number.864", "number.459"],
                "to_id": "answer.4",
                "equation": "864 + 459 = 1323",
            },
        ],
    },
    "answer": {
        "blanks": [
            {"id": "slot.answer_1", "type": "number", "value": 721},
            {"id": "slot.answer_2", "type": "number", "value": 1316},
            {"id": "slot.answer_3", "type": "number", "value": 934},
            {"id": "slot.answer_4", "type": "number", "value": 1323},
        ],
        "choices": [],
        "answer_key": [
            {"blank_id": "slot.answer_1", "value": 721},
            {"blank_id": "slot.answer_2", "value": 1316},
            {"blank_id": "slot.answer_3", "value": 934},
            {"blank_id": "slot.answer_4", "value": 1323},
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
            "problem_1": {"addends": [286, 435]},
            "problem_2": {"addends": [479, 837]},
            "problem_3": {"addends": [296, 638]},
            "problem_4": {"addends": [864, 459]},
        },
        "conditions": [
            "같은 자리의 숫자끼리 맞추어 더합니다.",
            "각 자리의 합이 10 이상이면 바로 윗자리로 받아올림합니다.",
        ],
    },
    "given": [
        {"ref": "calculation.1", "value": {"addends": [286, 435]}},
        {"ref": "calculation.2", "value": {"addends": [479, 837]}},
        {"ref": "calculation.3", "value": {"addends": [296, 638]}},
        {"ref": "calculation.4", "value": {"addends": [864, 459]}},
    ],
    "target": {
        "ref": "answer.all",
        "type": "addition_results",
    },
    "understanding": {
        "summary": "네 개의 세 자리 수 덧셈을 계산하여 각각의 답을 구하는 문제입니다.",
        "facts": [
            {
                "ref": "calculation.1",
                "label": "첫 번째 덧셈식",
                "value": "286 + 435",
                "unit": "",
                "source": "explicit",
            },
            {
                "ref": "calculation.2",
                "label": "두 번째 덧셈식",
                "value": "479 + 837",
                "unit": "",
                "source": "explicit",
            },
            {
                "ref": "calculation.3",
                "label": "세 번째 덧셈식",
                "value": "296 + 638",
                "unit": "",
                "source": "explicit",
            },
            {
                "ref": "calculation.4",
                "label": "네 번째 덧셈식",
                "value": "864 + 459",
                "unit": "",
                "source": "explicit",
            },
        ],
        "unknowns": [
            {"ref": "answer.1", "label": "286 + 435의 계산 결과", "unit": "", "source": "unknown"},
            {"ref": "answer.2", "label": "479 + 837의 계산 결과", "unit": "", "source": "unknown"},
            {"ref": "answer.3", "label": "296 + 638의 계산 결과", "unit": "", "source": "unknown"},
            {"ref": "answer.4", "label": "864 + 459의 계산 결과", "unit": "", "source": "unknown"},
        ],
        "relation": {
            "type": "place_value_addition",
            "statement": "일의 자리부터 더하고, 합이 10 이상이면 받아올림하여 다음 자리 계산에 더합니다.",
            "symbolic": "ones -> tens -> hundreds -> thousands",
            "uses": [
                "calculation.1",
                "calculation.2",
                "calculation.3",
                "calculation.4",
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
                    "가장 큰 수 하나",
                    "덧셈식의 개수",
                ],
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
            "template": "네 덧셈식 {exprs}의 값을 각각 계산합니다.",
            "answer": "286+435, 479+837, 296+638, 864+459를 각각 계산합니다.",
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
            "goal": "286 + 435를 계산합니다.",
            "uses": ["calculation.1"],
            "expr": "286 + 435",
            "value": {"sum": 721, "ref": "answer.1"},
            "explanation": "일의 자리 6+5=11에서 1을 쓰고 1을 받아올림합니다. 십의 자리 8+3+1=12에서 2를 쓰고 1을 받아올림합니다. 백의 자리 2+4+1=7이므로 721입니다.",
        },
        {
            "id": "step.2",
            "goal": "479 + 837을 계산합니다.",
            "uses": ["calculation.2"],
            "expr": "479 + 837",
            "value": {"sum": 1316, "ref": "answer.2"},
            "explanation": "일의 자리 9+7=16에서 6을 쓰고 1을 받아올림합니다. 십의 자리 7+3+1=11에서 1을 쓰고 1을 받아올림합니다. 백의 자리 4+8+1=13이므로 1316입니다.",
        },
        {
            "id": "step.3",
            "goal": "296 + 638을 계산합니다.",
            "uses": ["calculation.3"],
            "expr": "296 + 638",
            "value": {"sum": 934, "ref": "answer.3"},
            "explanation": "일의 자리 6+8=14에서 4를 쓰고 1을 받아올림합니다. 십의 자리 9+3+1=13에서 3을 쓰고 1을 받아올림합니다. 백의 자리 2+6+1=9이므로 934입니다.",
        },
        {
            "id": "step.4",
            "goal": "864 + 459를 계산합니다.",
            "uses": ["calculation.4"],
            "expr": "864 + 459",
            "value": {"sum": 1323, "ref": "answer.4"},
            "explanation": "일의 자리 4+9=13에서 3을 쓰고 1을 받아올림합니다. 십의 자리 6+5+1=12에서 2를 쓰고 1을 받아올림합니다. 백의 자리 8+4+1=13이므로 1323입니다.",
        },
    ],
    "checks": [
        {
            "id": "check.1",
            "description": "721에서 435를 빼면 286이 됩니다.",
            "expr": "721 - 435",
            "expected": 286,
            "actual": 286,
            "pass": True,
        },
        {
            "id": "check.2",
            "description": "1316에서 837을 빼면 479가 됩니다.",
            "expr": "1316 - 837",
            "expected": 479,
            "actual": 479,
            "pass": True,
        },
        {
            "id": "check.3",
            "description": "934에서 638을 빼면 296이 됩니다.",
            "expr": "934 - 638",
            "expected": 296,
            "actual": 296,
            "pass": True,
        },
        {
            "id": "check.4",
            "description": "1323에서 459를 빼면 864가 됩니다.",
            "expr": "1323 - 459",
            "expected": 864,
            "actual": 864,
            "pass": True,
        },
    ],
    "answer": {
        "blanks": [
            {"id": "slot.answer_1", "type": "number", "value": 721, "unit": ""},
            {"id": "slot.answer_2", "type": "number", "value": 1316, "unit": ""},
            {"id": "slot.answer_3", "type": "number", "value": 934, "unit": ""},
            {"id": "slot.answer_4", "type": "number", "value": 1323, "unit": ""},
        ],
        "choices": [],
        "answer_key": [
            {"blank_id": "slot.answer_1", "value": 721, "unit": ""},
            {"blank_id": "slot.answer_2", "value": 1316, "unit": ""},
            {"blank_id": "slot.answer_3", "value": 934, "unit": ""},
            {"blank_id": "slot.answer_4", "value": 1323, "unit": ""},
        ],
        "value": [721, 1316, 934, 1323],
        "unit": "",
        "sentence": "(1) 721, (2) 1316, (3) 934, (4) 1323입니다.",
    },
}


SEMANTIC_OVERRIDE["answer"] = SOLVABLE["answer"]
