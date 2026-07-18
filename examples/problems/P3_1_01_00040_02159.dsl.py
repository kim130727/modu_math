from __future__ import annotations

from modu_math.dsl import (
    BlankSlot,
    Canvas,
    Group,
    PathSlot,
    PolygonSlot,
    ProblemTemplate,
    RectSlot,
    Region,
    TextBoxSlot,
    TextSlot,
)

PROBLEM_ID = "P3_1_01_00040_02159"
PROBLEM_TITLE = "연속 덧셈의 빈칸 채우기"


def _oval_path(cx: float, cy: float, rx: float, ry: float) -> str:
    return (
        f"M {cx - rx} {cy} "
        f"C {cx - rx} {cy - ry}, {cx + rx} {cy - ry}, {cx + rx} {cy} "
        f"C {cx + rx} {cy + ry}, {cx - rx} {cy + ry}, {cx - rx} {cy} Z"
    )


def build_problem_template() -> ProblemTemplate:
    return ProblemTemplate(
        id=PROBLEM_ID,
        title=PROBLEM_TITLE,
        canvas=Canvas(
            width=365,
            height=125,
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
                id="region.diagram",
                role="diagram",
                flow="absolute",
                slot_ids=(
                    "slot.start_oval",
                    "slot.start_value",
                    "slot.operation_1_box",
                    "slot.operation_1",
                    "slot.arrow_1_curve",
                    "slot.arrow_1_head",
                    "slot.answer_1_oval",
                    "slot.operation_2_box",
                    "slot.operation_2",
                    "slot.arrow_2_curve",
                    "slot.arrow_2_head",
                    "slot.answer_2_oval",
                ),
            ),
        ),
        slots=(
            TextBoxSlot(
                id="slot.instruction",
                text="빈 곳에 알맞은 수를 써넣으시오.",
                prompt="연속 덧셈의 계산 결과를 빈칸에 쓰라는 안내",
                semantic_role="instruction",
                x=18,
                y=1,
                width=250,
                height=24,
                font_size=15,
                line_height=1.15,
                fill="#111111",
                align="left",
            ),
            PathSlot(
                id="slot.start_oval",
                prompt="시작 수 156이 들어 있는 타원",
                d=_oval_path(50, 76, 28, 15),
                fill="#fff7ff",
                stroke="#ead5e9",
                stroke_width=1.2,
                semantic_role="given_value",
            ),
            TextSlot(
                id="slot.start_value",
                text="156",
                prompt="연속 계산을 시작하는 수 156",
                x=50,
                y=82,
                font_size=15,
                anchor="middle",
                fill="#111111",
                semantic_role="given_value",
            ),
            RectSlot(
                id="slot.operation_1_box",
                prompt="첫 번째 덧셈 +278이 들어 있는 상자",
                x=80,
                y=25,
                width=64,
                height=28,
                fill="#e9f8dd",
                stroke="#a9ce93",
                stroke_width=1.2,
                semantic_role="operation",
            ),
            TextSlot(
                id="slot.operation_1",
                text="+278",
                prompt="첫 번째 연산 278 더하기",
                x=112,
                y=44,
                font_size=15,
                anchor="middle",
                fill="#111111",
                semantic_role="operation",
            ),
            PathSlot(
                id="slot.arrow_1_curve",
                prompt="156에서 첫 번째 빈칸으로 이어지는 곡선 화살표",
                d="M 77 74 C 91 58, 108 55, 127 63",
                fill="none",
                stroke="#111111",
                stroke_width=1.1,
                semantic_role="flow_arrow",
            ),
            PolygonSlot(
                id="slot.arrow_1_head",
                prompt="첫 번째 화살표 머리",
                points=((127, 63), (118, 58), (120, 68)),
                fill="#111111",
                stroke="#111111",
                stroke_width=1,
                semantic_role="flow_arrow",
            ),
            PathSlot(
                id="slot.answer_1_oval",
                prompt="156에 278을 더한 결과를 쓰는 첫 번째 빈 타원",
                d=_oval_path(174, 76, 28, 15),
                fill="#ffffff",
                stroke="#ead5e9",
                stroke_width=1.2,
                semantic_role="answer_blank",
            ),
            BlankSlot(
                id="slot.answer_1",
                prompt="156과 278의 합",
                answer_key="434",
                placeholder="",
            ),
            RectSlot(
                id="slot.operation_2_box",
                prompt="두 번째 덧셈 +697이 들어 있는 상자",
                x=204,
                y=25,
                width=64,
                height=28,
                fill="#e9f8dd",
                stroke="#a9ce93",
                stroke_width=1.2,
                semantic_role="operation",
            ),
            TextSlot(
                id="slot.operation_2",
                text="+697",
                prompt="두 번째 연산 697 더하기",
                x=236,
                y=44,
                font_size=15,
                anchor="middle",
                fill="#111111",
                semantic_role="operation",
            ),
            PathSlot(
                id="slot.arrow_2_curve",
                prompt="첫 번째 빈칸에서 두 번째 빈칸으로 이어지는 곡선 화살표",
                d="M 201 74 C 215 58, 232 55, 251 63",
                fill="none",
                stroke="#111111",
                stroke_width=1.1,
                semantic_role="flow_arrow",
            ),
            PolygonSlot(
                id="slot.arrow_2_head",
                prompt="두 번째 화살표 머리",
                points=((251, 63), (242, 58), (244, 68)),
                fill="#111111",
                stroke="#111111",
                stroke_width=1,
                semantic_role="flow_arrow",
            ),
            PathSlot(
                id="slot.answer_2_oval",
                prompt="첫 번째 결과에 697을 더한 결과를 쓰는 두 번째 빈 타원",
                d=_oval_path(298, 76, 28, 15),
                fill="#ffffff",
                stroke="#ead5e9",
                stroke_width=1.2,
                semantic_role="answer_blank",
            ),
            BlankSlot(
                id="slot.answer_2",
                prompt="434와 697의 합",
                answer_key="1131",
                placeholder="",
            ),
        ),
        diagrams=(),
        groups=(
            Group(
                id="group.calculation_chain",
                role="sequential_addition",
                member_ids=(
                    "slot.start_oval",
                    "slot.start_value",
                    "slot.operation_1_box",
                    "slot.operation_1",
                    "slot.arrow_1_curve",
                    "slot.arrow_1_head",
                    "slot.answer_1_oval",
                    "slot.answer_1",
                    "slot.operation_2_box",
                    "slot.operation_2",
                    "slot.arrow_2_curve",
                    "slot.arrow_2_head",
                    "slot.answer_2_oval",
                    "slot.answer_2",
                ),
            ),
        ),
        constraints=(),
        tags=(
            "grade-3",
            "addition",
            "three-digit-addition",
            "sequential-calculation",
            "fill-in-the-blank",
            "diagram",
        ),
    )


PROBLEM_TEMPLATE = build_problem_template()


SEMANTIC_OVERRIDE = {
    "problem_id": PROBLEM_ID,
    "problem_type": "sequential_addition_fill_blank",
    "metadata": {
        "grade": 3,
        "semester": 1,
        "subject": "수학",
        "topic": "세 자리 수의 덧셈",
        "language": "ko-KR",
        "question": "빈 곳에 알맞은 수를 써넣으시오.",
    },
    "domain": {
        "objects": [
            {
                "id": "number.start",
                "type": "number",
                "label": "처음 수",
                "value": 156,
            },
            {
                "id": "operation.add_278",
                "type": "addition_operation",
                "label": "278 더하기",
                "value": 278,
            },
            {
                "id": "number.middle",
                "type": "number",
                "label": "첫 번째 빈칸의 수",
                "value": 434,
            },
            {
                "id": "operation.add_697",
                "type": "addition_operation",
                "label": "697 더하기",
                "value": 697,
            },
            {
                "id": "number.end",
                "type": "number",
                "label": "두 번째 빈칸의 수",
                "value": 1131,
            },
        ],
        "relations": [
            {
                "id": "relation.step_1",
                "type": "addition",
                "from_ids": ["number.start", "operation.add_278"],
                "to_id": "number.middle",
                "equation": "156 + 278 = 434",
            },
            {
                "id": "relation.step_2",
                "type": "addition",
                "from_ids": ["number.middle", "operation.add_697"],
                "to_id": "number.end",
                "equation": "434 + 697 = 1131",
            },
        ],
    },
    "answer": {
        "blanks": [
            {"id": "slot.answer_1", "type": "number", "value": 434, "unit": ""},
            {"id": "slot.answer_2", "type": "number", "value": 1131, "unit": ""},
        ],
        "choices": [],
        "answer_key": [
            {"blank_id": "slot.answer_1", "value": 434, "unit": ""},
            {"blank_id": "slot.answer_2", "value": 1131, "unit": ""},
        ],
        "value": [434, 1131],
        "unit": "",
        "sentence": "첫 번째 빈칸은 434, 두 번째 빈칸은 1131입니다.",
    },
}


SOLVABLE = {
    "schema": "modu.solvable.v1.2",
    "problem_id": PROBLEM_ID,
    "problem_type": "sequential_addition_fill_blank",
    "inputs": {
        "target_label": "두 빈칸에 들어갈 수",
        "unit": "",
        "quantities": {
            "start_value": 156,
            "first_addend": 278,
            "second_addend": 697,
        },
        "conditions": [
            "156에서 시작합니다.",
            "첫 번째 화살표에서는 278을 더합니다.",
            "두 번째 화살표에서는 앞에서 구한 수에 697을 더합니다.",
        ],
    },
    "given": [
        {"ref": "number.start", "value": 156},
        {"ref": "operation.add_278", "value": 278},
        {"ref": "operation.add_697", "value": 697},
    ],
    "target": {
        "ref": "answer.all",
        "type": "sequential_addition_results",
    },
    "understanding": {
        "summary": "156에서 시작해 화살표 순서대로 278과 697을 더하고, 각 단계의 결과를 빈칸에 쓰는 문제입니다.",
        "facts": [
            {
                "ref": "number.start",
                "label": "처음 수",
                "value": 156,
                "unit": "",
                "source": "explicit",
            },
            {
                "ref": "operation.add_278",
                "label": "첫 번째로 더할 수",
                "value": 278,
                "unit": "",
                "source": "explicit",
            },
            {
                "ref": "operation.add_697",
                "label": "두 번째로 더할 수",
                "value": 697,
                "unit": "",
                "source": "explicit",
            },
        ],
        "unknowns": [
            {
                "ref": "number.middle",
                "label": "156에 278을 더한 값",
                "unit": "",
                "source": "unknown",
            },
            {
                "ref": "number.end",
                "label": "첫 번째 결과에 697을 더한 값",
                "unit": "",
                "source": "unknown",
            },
        ],
        "relation": {
            "type": "sequential_addition",
            "statement": "앞에서 구한 결과를 다음 덧셈의 시작 수로 사용합니다.",
            "symbolic": "156 + 278 = middle; middle + 697 = end",
            "uses": [
                "number.start",
                "operation.add_278",
                "operation.add_697",
            ],
            "result": "answer.all",
        },
        "diagnostic_questions": [
            {
                "id": "understand.first_operation",
                "type": "multiple_choice",
                "prompt": "156에 가장 먼저 더해야 하는 수는 무엇인가요?",
                "choices": ["278", "697", "156"],
                "answer_index": 0,
            },
            {
                "id": "understand.second_start",
                "type": "multiple_choice",
                "prompt": "697은 어느 수에 더해야 하나요?",
                "choices": [
                    "첫 번째 빈칸에서 구한 수",
                    "처음 수 156",
                    "278",
                ],
                "answer_index": 0,
            },
        ],
        "student_restatement": {
            "prompt": "문제의 뜻을 말해 볼까요?",
            "template": "{start}에서 시작해 {first}를 더하고, 그 결과에 {second}를 더합니다.",
            "answer": "156에 278을 더해 첫 번째 빈칸을 구하고, 그 수에 697을 더해 두 번째 빈칸을 구합니다.",
        },
    },
    "method": "화살표 방향을 따라 앞 단계의 결과에 표시된 수를 차례대로 더합니다.",
    "plan": [
        "156에 278을 더해 첫 번째 빈칸의 수를 구합니다.",
        "첫 번째 빈칸의 수에 697을 더해 두 번째 빈칸의 수를 구합니다.",
        "두 계산 결과를 각각 알맞은 빈칸에 씁니다.",
    ],
    "steps": [
        {
            "id": "step.1",
            "goal": "첫 번째 빈칸의 수를 구합니다.",
            "uses": ["number.start", "operation.add_278"],
            "expr": "156 + 278",
            "value": {"sum": 434, "ref": "number.middle"},
            "explanation": "156에 278을 더하면 434이므로 첫 번째 빈칸에는 434를 씁니다.",
        },
        {
            "id": "step.2",
            "goal": "두 번째 빈칸의 수를 구합니다.",
            "uses": ["number.middle", "operation.add_697"],
            "expr": "434 + 697",
            "value": {"sum": 1131, "ref": "number.end"},
            "explanation": "앞에서 구한 434에 697을 더하면 1131이므로 두 번째 빈칸에는 1131을 씁니다.",
        },
    ],
    "checks": [
        {
            "id": "check.1",
            "description": "첫 번째 결과 434에서 278을 빼면 처음 수 156이 됩니다.",
            "expr": "434 - 278",
            "expected": 156,
            "actual": 156,
            "pass": True,
        },
        {
            "id": "check.2",
            "description": "두 번째 결과 1131에서 697을 빼면 첫 번째 결과 434가 됩니다.",
            "expr": "1131 - 697",
            "expected": 434,
            "actual": 434,
            "pass": True,
        },
    ],
    "answer": SEMANTIC_OVERRIDE["answer"],
}


SEMANTIC_OVERRIDE["answer"] = SOLVABLE["answer"]
SEMANTIC_ANSWER = SOLVABLE["answer"]
