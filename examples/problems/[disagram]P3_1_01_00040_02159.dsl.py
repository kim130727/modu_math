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
                slot_ids=("slot.start_oval",
                    "slot.start_value",
                    "slot.operation_1_box",
                    "slot.operation_1",
                    "slot.arrow_1_curve",
                    "slot.arrow_1_head",
                    "slot.operation_2_box",
                    "slot.operation_2",
                    "slot.arrow_2_curve",
                    "slot.arrow_2_head",
                    'konva_1784592333289_arrow_2136844', 'konva_1784592333289_arrow_2144100', 'konva_1784592333289_arrow_2159396', 'konva_1784592333289_arrow_2165492', 'konva_1785110879232_rect_187005', 'konva_1785110879232_paste_195947_0', 'konva_1785110879232_paste_197056_0', 'konva_1785110879232_paste_235457_0'),
            ),
        ),
        slots=(TextBoxSlot(
                id="slot.instruction",
                text = '빈 곳에 알맞은 수를 써넣으시오.', prompt="연속 덧셈의 계산 결과를 빈칸에 쓰라는 안내",
                semantic_role="instruction",
                x = 16.254, y = 7.545, width = 222.057, height = 43, font_size = 15, line_height = 1.15, fill = '#111111', align = 'left'),
            PathSlot(
                id="slot.start_oval",
                prompt="시작 수 156이 들어 있는 타원",
                d = 'M 15.888 83.947 C 15.888 65.914 83.21 65.914 83.21 83.947 C 83.21 101.979 15.888 101.979 15.888 83.947 Z', fill = '#fff7ff', stroke = '#ead5e9', stroke_width = 1.2, semantic_role="given_value",
            ),
            TextSlot(
                id="slot.start_value",
                text = '156', prompt="연속 계산을 시작하는 수 156",
                x = 49.563, y = 89.854, font_size = 15, anchor = 'middle', fill = '#111111', semantic_role="given_value",
            ),
            RectSlot(
                id="slot.operation_1_box",
                prompt="첫 번째 덧셈 +278이 들어 있는 상자",
                x = 83.929, y = 31.109, width = 64, height = 28, fill = '#e9f8dd', stroke = '#a9ce93', stroke_width = 1.2, semantic_role="operation",
            ),
            TextSlot(
                id="slot.operation_1",
                text = '+278', prompt="첫 번째 연산 278 더하기",
                x = 116.366, y = 50.545, font_size = 15, anchor = 'middle', fill = '#111111', semantic_role="operation",
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
            BlankSlot(
                id="slot.answer_1",
                prompt="156과 278의 합",
                answer_key="434",
                placeholder="",
            ),
            RectSlot(
                id="slot.operation_2_box",
                prompt="두 번째 덧셈 +697이 들어 있는 상자",
                x = 206.563, y = 32.854, width = 64, height = 28, fill = '#e9f8dd', stroke = '#a9ce93', stroke_width = 1.2, semantic_role="operation",
            ),
            TextSlot(
                id="slot.operation_2",
                text = '+697', prompt="두 번째 연산 697 더하기",
                x = 239.056, y = 51.854, font_size = 15, anchor = 'middle', fill = '#111111', semantic_role="operation",
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
            BlankSlot(
                id="slot.answer_2",
                prompt="434와 697의 합",
                answer_key="1131",
                placeholder="",
            ),PathSlot(id = 'konva_1784592333289_arrow_2136844', prompt = '', d = 'M 52.393 69.402 L 79.023 46.272 M 79.023 46.272 L 74.673 56.372 M 79.023 46.272 L 68.413 49.172', fill = 'none', stroke = '#111827', stroke_width = 1.2), PathSlot(id = 'konva_1784592333289_arrow_2144100', prompt = '', d = 'M 153.679 44.088 L 172.449 65.028 M 172.449 65.028 L 162.279 60.838 M 172.449 65.028 L 169.389 54.458', fill = 'none', stroke = '#111827', stroke_width = 1.2), PathSlot(id = 'konva_1784592333289_arrow_2159396', prompt = '', d = 'M 183.813 67.222 L 203.893 46.282 M 203.893 46.282 L 200.483 56.742 M 203.893 46.282 L 193.593 50.132', fill = 'none', stroke = '#111827', stroke_width = 1.2), PathSlot(id = 'konva_1784592333289_arrow_2165492', prompt = '', d = 'M 275.493 46.712 L 298.633 69.842 M 298.633 69.842 L 288.253 66.212 M 298.633 69.842 L 294.993 59.462', fill = 'none', stroke = '#111827', stroke_width = 1.2), RectSlot(id = 'konva_1785110879232_rect_187005', prompt = '', x = 156.946, y = 99.877, width = 41.659, height = 22.218, fill = '#ffffff', stroke = '#111827', stroke_width = 1.2, interaction = {'type': 'input', 'role': 'answer', 'value_type': 'digit', 'max_length': 1, 'include_in_submission': True, 'order': 0, 'group_id': 'final_answer', 'auto_advance': True, 'keyboard': 'number'}, input_style = {'font_size_mode': 'auto', 'font_size_adjust': 0, 'min_font_size': 14, 'max_font_size': 52, 'font_weight': 700, 'horizontal_align': 'center', 'vertical_align': 'middle', 'padding': 6, 'text_color': '#222222'}), PathSlot(id = 'konva_1785110879232_paste_195947_0', prompt = '', d = 'M 140.306 82.639 C 140.306 64.606 207.628 64.606 207.628 82.639 C 207.628 100.671 140.306 100.671 140.306 82.639 Z', fill = '#fff7ff', stroke = '#ead5e9', stroke_width = 1.2), PathSlot(id = 'konva_1785110879232_paste_197056_0', prompt = '', d = 'M 267.781 83.694 C 267.781 65.661 335.103 65.661 335.103 83.694 C 335.103 101.726 267.781 101.726 267.781 83.694 Z', fill = '#fff7ff', stroke = '#ead5e9', stroke_width = 1.2), RectSlot(id = 'konva_1785110879232_paste_235457_0', prompt = '', x = 282.477, y = 99.314, width = 41.659, height = 22.218, fill = '#ffffff', stroke = '#111827', stroke_width = 1.2, interaction = {'type': 'input', 'role': 'answer', 'value_type': 'digit', 'max_length': 1, 'include_in_submission': True, 'order': 1, 'group_id': 'final_answer', 'auto_advance': True, 'keyboard': 'number'}, input_style = {'font_size_mode': 'auto', 'font_size_adjust': 0, 'min_font_size': 14, 'max_font_size': 52, 'font_weight': 700, 'horizontal_align': 'center', 'vertical_align': 'middle', 'padding': 6, 'text_color': '#222222'})),
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
