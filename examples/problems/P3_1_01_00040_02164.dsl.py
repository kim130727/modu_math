from __future__ import annotations

from modu_math.dsl import (
    BlankSlot,
    Canvas,
    Group,
    PathSlot,
    ProblemTemplate,
    RectSlot,
    Region,
    TextBoxSlot,
    TextSlot,
)


PROBLEM_ID = "P3_1_01_00040_02164"
PROBLEM_TITLE = "원 안의 두 수를 더하는 규칙"


def _circle_path(cx: float, cy: float, r: float) -> str:
    k = r * 0.5522847498
    return (
        f"M {cx - r} {cy} "
        f"C {cx - r} {cy - k}, {cx - k} {cy - r}, {cx} {cy - r} "
        f"C {cx + k} {cy - r}, {cx + r} {cy - k}, {cx + r} {cy} "
        f"C {cx + r} {cy + k}, {cx + k} {cy + r}, {cx} {cy + r} "
        f"C {cx - k} {cy + r}, {cx - r} {cy + k}, {cx - r} {cy} Z"
    )


def build_problem_template() -> ProblemTemplate:
    return ProblemTemplate(
        id=PROBLEM_ID,
        title=PROBLEM_TITLE,
        canvas=Canvas(
            width=619,
            height=300,
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
                id="region.example",
                role="example",
                flow="absolute",
                slot_ids=(
                    "slot.example_label",
                    "slot.example_box",
                    "slot.example_circle",
                    "slot.example_horizontal_line",
                    "slot.example_vertical_line",
                    "slot.example_left_value",
                    "slot.example_right_value",
                    "slot.example_sum",
                ),
            ),
            Region(
                id="region.diagram",
                role="diagram",
                flow="absolute",
                slot_ids=(
                    "slot.item_1_label",
                    "slot.item_1_circle",
                    "slot.item_1_horizontal_line",
                    "slot.item_1_vertical_line",
                    "slot.item_1_left_value",
                    "slot.item_1_right_value",
                    "slot.item_2_label",
                    "slot.item_2_circle",
                    "slot.item_2_horizontal_line",
                    "slot.item_2_vertical_line",
                    "slot.item_2_left_value",
                    "slot.item_2_right_value",
                ),
            ),
        ),
        slots=(
            TextBoxSlot(
                id="slot.instruction",
                text="다음 <보기>와 같이 빈 곳에 알맞은 수를 써넣으시오.",
                prompt="보기의 규칙을 찾아 두 빈칸에 알맞은 수를 쓰라는 안내",
                semantic_role="instruction",
                x=20,
                y=2,
                width=410,
                height=24,
                font_size=15,
                line_height=1.15,
                fill="#222222",
                align="left",
            ),
            TextSlot(
                id="slot.example_label",
                text="<보기>",
                prompt="보기 표시",
                x=82,
                y=35,
                font_size=14,
                anchor="middle",
                fill="#333333",
                semantic_role="example_label",
            ),
            RectSlot(
                id="slot.example_box",
                prompt="덧셈 규칙을 보여 주는 보기 상자",
                x=22,
                y=32,
                width=120,
                height=121,
                fill="#ffffff",
                stroke="#888888",
                stroke_width=1.2,
                semantic_role="example_container",
            ),
            PathSlot(
                id="slot.example_circle",
                prompt="보기의 세 부분으로 나뉜 원",
                d=_circle_path(82, 96, 50),
                fill="#fff5d9",
                stroke="#efc66a",
                stroke_width=1.1,
                semantic_role="addition_rule_diagram",
            ),
            PathSlot(
                id="slot.example_horizontal_line",
                prompt="보기 원의 위쪽과 아래쪽을 나누는 선",
                d="M 32 96 L 132 96",
                fill="none",
                stroke="#efc66a",
                stroke_width=1.1,
                semantic_role="partition_line",
            ),
            PathSlot(
                id="slot.example_vertical_line",
                prompt="보기 원의 위쪽 두 수를 나누는 선",
                d="M 82 46 L 82 96",
                fill="none",
                stroke="#efc66a",
                stroke_width=1.1,
                semantic_role="partition_line",
            ),
            TextSlot(
                id="slot.example_left_value",
                text="259",
                prompt="보기의 첫 번째 수 259",
                x=58,
                y=82,
                font_size=15,
                anchor="middle",
                fill="#222222",
                semantic_role="given_value",
            ),
            TextSlot(
                id="slot.example_right_value",
                text="287",
                prompt="보기의 두 번째 수 287",
                x=106,
                y=82,
                font_size=15,
                anchor="middle",
                fill="#222222",
                semantic_role="given_value",
            ),
            TextSlot(
                id="slot.example_sum",
                text="546",
                prompt="보기의 두 수를 더한 값 546",
                x=82,
                y=126,
                font_size=15,
                anchor="middle",
                fill="#222222",
                semantic_role="example_result",
            ),
            TextSlot(
                id="slot.item_1_label",
                text="(1)",
                prompt="첫 번째 문항 번호",
                x=20,
                y=171,
                font_size=14,
                anchor="start",
                fill="#222222",
                semantic_role="item_label",
            ),
            PathSlot(
                id="slot.item_1_circle",
                prompt="236과 465의 합을 쓰는 첫 번째 원",
                d=_circle_path(84, 210, 49),
                fill="#ffffff",
                stroke="#efc66a",
                stroke_width=1.1,
                semantic_role="answer_diagram",
            ),
            PathSlot(
                id="slot.item_1_horizontal_line",
                prompt="첫 번째 원의 위쪽과 아래쪽을 나누는 선",
                d="M 35 210 L 133 210",
                fill="none",
                stroke="#efc66a",
                stroke_width=1.1,
                semantic_role="partition_line",
            ),
            PathSlot(
                id="slot.item_1_vertical_line",
                prompt="첫 번째 원의 위쪽 두 수를 나누는 선",
                d="M 84 161 L 84 210",
                fill="none",
                stroke="#efc66a",
                stroke_width=1.1,
                semantic_role="partition_line",
            ),
            TextSlot(
                id="slot.item_1_left_value",
                text="236",
                prompt="첫 번째 문항의 첫 번째 수 236",
                x=60,
                y=196,
                font_size=15,
                anchor="middle",
                fill="#222222",
                semantic_role="given_value",
            ),
            TextSlot(
                id="slot.item_1_right_value",
                text="465",
                prompt="첫 번째 문항의 두 번째 수 465",
                x=108,
                y=196,
                font_size=15,
                anchor="middle",
                fill="#222222",
                semantic_role="given_value",
            ),
            BlankSlot(
                id="slot.answer_1",
                prompt="236과 465의 합",
                answer_key="701",
                placeholder="",
            ),
            TextSlot(
                id="slot.item_2_label",
                text="(2)",
                prompt="두 번째 문항 번호",
                x=168,
                y=171,
                font_size=14,
                anchor="start",
                fill="#222222",
                semantic_role="item_label",
            ),
            PathSlot(
                id="slot.item_2_circle",
                prompt="756과 549의 합을 쓰는 두 번째 원",
                d=_circle_path(238, 210, 49),
                fill="#ffffff",
                stroke="#efc66a",
                stroke_width=1.1,
                semantic_role="answer_diagram",
            ),
            PathSlot(
                id="slot.item_2_horizontal_line",
                prompt="두 번째 원의 위쪽과 아래쪽을 나누는 선",
                d="M 189 210 L 287 210",
                fill="none",
                stroke="#efc66a",
                stroke_width=1.1,
                semantic_role="partition_line",
            ),
            PathSlot(
                id="slot.item_2_vertical_line",
                prompt="두 번째 원의 위쪽 두 수를 나누는 선",
                d="M 238 161 L 238 210",
                fill="none",
                stroke="#efc66a",
                stroke_width=1.1,
                semantic_role="partition_line",
            ),
            TextSlot(
                id="slot.item_2_left_value",
                text="756",
                prompt="두 번째 문항의 첫 번째 수 756",
                x=214,
                y=196,
                font_size=15,
                anchor="middle",
                fill="#222222",
                semantic_role="given_value",
            ),
            TextSlot(
                id="slot.item_2_right_value",
                text="549",
                prompt="두 번째 문항의 두 번째 수 549",
                x=262,
                y=196,
                font_size=15,
                anchor="middle",
                fill="#222222",
                semantic_role="given_value",
            ),
            BlankSlot(
                id="slot.answer_2",
                prompt="756과 549의 합",
                answer_key="1305",
                placeholder="",
            ),
        ),
        diagrams=(),
        groups=(
            Group(
                id="group.example",
                role="addition_rule_example",
                member_ids=(
                    "slot.example_box",
                    "slot.example_circle",
                    "slot.example_horizontal_line",
                    "slot.example_vertical_line",
                    "slot.example_left_value",
                    "slot.example_right_value",
                    "slot.example_sum",
                ),
            ),
            Group(
                id="group.item_1",
                role="addition_rule_item",
                member_ids=(
                    "slot.item_1_circle",
                    "slot.item_1_horizontal_line",
                    "slot.item_1_vertical_line",
                    "slot.item_1_left_value",
                    "slot.item_1_right_value",
                    "slot.answer_1",
                ),
            ),
            Group(
                id="group.item_2",
                role="addition_rule_item",
                member_ids=(
                    "slot.item_2_circle",
                    "slot.item_2_horizontal_line",
                    "slot.item_2_vertical_line",
                    "slot.item_2_left_value",
                    "slot.item_2_right_value",
                    "slot.answer_2",
                ),
            ),
        ),
        constraints=(),
        tags=(
            "grade-3",
            "addition",
            "three-digit-addition",
            "find-the-rule",
            "fill-in-the-blank",
            "diagram",
        ),
    )


PROBLEM_TEMPLATE = build_problem_template()


SEMANTIC_OVERRIDE = {
    "problem_id": PROBLEM_ID,
    "problem_type": "addition_rule_circle_fill_blank",
    "metadata": {
        "grade": 3,
        "semester": 1,
        "subject": "수학",
        "topic": "세 자리 수의 덧셈",
        "language": "ko-KR",
        "question": "다음 <보기>와 같이 빈 곳에 알맞은 수를 써넣으시오.",
    },
    "domain": {
        "objects": [
            {
                "id": "example.addend_left",
                "type": "number",
                "label": "보기의 왼쪽 수",
                "value": 259,
            },
            {
                "id": "example.addend_right",
                "type": "number",
                "label": "보기의 오른쪽 수",
                "value": 287,
            },
            {
                "id": "example.sum",
                "type": "number",
                "label": "보기의 아래 수",
                "value": 546,
            },
            {
                "id": "item_1.addend_left",
                "type": "number",
                "label": "(1)의 왼쪽 수",
                "value": 236,
            },
            {
                "id": "item_1.addend_right",
                "type": "number",
                "label": "(1)의 오른쪽 수",
                "value": 465,
            },
            {
                "id": "item_1.sum",
                "type": "number",
                "label": "(1)의 아래 빈칸 수",
                "value": 701,
            },
            {
                "id": "item_2.addend_left",
                "type": "number",
                "label": "(2)의 왼쪽 수",
                "value": 756,
            },
            {
                "id": "item_2.addend_right",
                "type": "number",
                "label": "(2)의 오른쪽 수",
                "value": 549,
            },
            {
                "id": "item_2.sum",
                "type": "number",
                "label": "(2)의 아래 빈칸 수",
                "value": 1305,
            },
        ],
        "relations": [
            {
                "id": "relation.example",
                "type": "addition",
                "from_ids": [
                    "example.addend_left",
                    "example.addend_right",
                ],
                "to_id": "example.sum",
                "equation": "259 + 287 = 546",
            },
            {
                "id": "relation.item_1",
                "type": "addition",
                "from_ids": [
                    "item_1.addend_left",
                    "item_1.addend_right",
                ],
                "to_id": "item_1.sum",
                "equation": "236 + 465 = 701",
            },
            {
                "id": "relation.item_2",
                "type": "addition",
                "from_ids": [
                    "item_2.addend_left",
                    "item_2.addend_right",
                ],
                "to_id": "item_2.sum",
                "equation": "756 + 549 = 1305",
            },
        ],
    },
    "answer": {
        "blanks": [
            {
                "id": "slot.answer_1",
                "type": "number",
                "value": 701,
                "unit": "",
            },
            {
                "id": "slot.answer_2",
                "type": "number",
                "value": 1305,
                "unit": "",
            },
        ],
        "choices": [],
        "answer_key": [
            {
                "blank_id": "slot.answer_1",
                "value": 701,
                "unit": "",
            },
            {
                "blank_id": "slot.answer_2",
                "value": 1305,
                "unit": "",
            },
        ],
        "value": [701, 1305],
        "unit": "",
        "sentence": "(1)은 701, (2)는 1305입니다.",
    },
}


SEMANTIC = SEMANTIC_OVERRIDE


SOLVABLE = {
    "schema": "modu.solvable.v1.2",
    "problem_id": PROBLEM_ID,
    "problem_type": "addition_rule_circle_fill_blank",
    "inputs": {
        "target_label": "두 원의 아래 빈칸에 들어갈 수",
        "unit": "",
        "quantities": {
            "example_left": 259,
            "example_right": 287,
            "example_result": 546,
            "item_1_left": 236,
            "item_1_right": 465,
            "item_2_left": 756,
            "item_2_right": 549,
        },
        "conditions": [
            "보기에서 위쪽 두 수 259와 287을 더하면 아래 수 546이 됩니다.",
            "각 원의 아래 빈칸에는 위쪽 두 수의 합을 씁니다.",
        ],
    },
    "given": [
        {
            "ref": "relation.example",
            "value": {
                "left": 259,
                "right": 287,
                "result": 546,
            },
        },
        {
            "ref": "item_1.addends",
            "value": {
                "left": 236,
                "right": 465,
            },
        },
        {
            "ref": "item_2.addends",
            "value": {
                "left": 756,
                "right": 549,
            },
        },
    ],
    "target": {
        "ref": "answer.all",
        "type": "addition_rule_results",
    },
    "understanding": {
        "summary": "보기에서 원의 위쪽 두 수를 더한 값이 아래 수가 되는 규칙을 찾아 두 빈칸을 구하는 문제입니다.",
        "facts": [
            {
                "ref": "relation.example",
                "label": "보기의 수 관계",
                "value": "259 + 287 = 546",
                "unit": "",
                "source": "explicit",
            },
            {
                "ref": "item_1.addends",
                "label": "(1)의 위쪽 두 수",
                "value": [236, 465],
                "unit": "",
                "source": "explicit",
            },
            {
                "ref": "item_2.addends",
                "label": "(2)의 위쪽 두 수",
                "value": [756, 549],
                "unit": "",
                "source": "explicit",
            },
        ],
        "unknowns": [
            {
                "ref": "item_1.sum",
                "label": "(1)의 아래 빈칸 수",
                "unit": "",
                "source": "unknown",
            },
            {
                "ref": "item_2.sum",
                "label": "(2)의 아래 빈칸 수",
                "unit": "",
                "source": "unknown",
            },
        ],
        "relation": {
            "type": "addition_rule",
            "statement": "원의 위쪽 왼쪽 수와 오른쪽 수를 더하면 아래쪽 수가 됩니다.",
            "symbolic": "bottom = top_left + top_right",
            "uses": [
                "item_1.addends",
                "item_2.addends",
            ],
            "result": "answer.all",
        },
        "diagnostic_questions": [
            {
                "id": "understand.example_rule",
                "type": "multiple_choice",
                "prompt": "보기에서 546은 어떻게 구했나요?",
                "choices": [
                    "259와 287을 더했습니다.",
                    "287에서 259를 뺐습니다.",
                    "259에 2를 곱했습니다.",
                ],
                "answer_index": 0,
            },
            {
                "id": "understand.apply_rule",
                "type": "multiple_choice",
                "prompt": "(1)의 빈칸을 구하는 식은 무엇인가요?",
                "choices": [
                    "236 + 465",
                    "465 - 236",
                    "236 + 236",
                ],
                "answer_index": 0,
            },
        ],
        "student_restatement": {
            "prompt": "문제의 규칙을 말해 볼까요?",
            "template": "원의 위쪽 두 수 {left}와 {right}를 {operation}하여 아래 수를 구합니다.",
            "answer": "원의 위쪽 두 수를 더하여 아래 빈칸에 그 합을 씁니다.",
        },
    },
    "method": "보기에서 찾은 규칙에 따라 각 원의 위쪽 두 수를 더합니다.",
    "plan": [
        "보기의 259, 287, 546 사이에서 덧셈 규칙을 찾습니다.",
        "(1)의 위쪽 두 수 236과 465를 더합니다.",
        "(2)의 위쪽 두 수 756과 549를 더합니다.",
        "구한 합을 각각 아래 빈칸에 씁니다.",
    ],
    "steps": [
        {
            "id": "step.find_rule",
            "goal": "보기의 수 관계에서 규칙을 찾습니다.",
            "uses": [
                "example.addend_left",
                "example.addend_right",
                "example.sum",
            ],
            "expr": "259 + 287",
            "value": {
                "sum": 546,
                "ref": "example.sum",
            },
            "explanation": "259와 287을 더하면 546이므로 위쪽 두 수의 합을 아래에 쓰는 규칙입니다.",
        },
        {
            "id": "step.item_1",
            "goal": "(1)의 빈칸에 들어갈 수를 구합니다.",
            "uses": [
                "item_1.addend_left",
                "item_1.addend_right",
            ],
            "expr": "236 + 465",
            "value": {
                "sum": 701,
                "ref": "item_1.sum",
            },
            "explanation": "236과 465를 더하면 701이므로 (1)의 빈칸에는 701을 씁니다.",
        },
        {
            "id": "step.item_2",
            "goal": "(2)의 빈칸에 들어갈 수를 구합니다.",
            "uses": [
                "item_2.addend_left",
                "item_2.addend_right",
            ],
            "expr": "756 + 549",
            "value": {
                "sum": 1305,
                "ref": "item_2.sum",
            },
            "explanation": "756과 549를 더하면 1305이므로 (2)의 빈칸에는 1305를 씁니다.",
        },
    ],
    "checks": [
        {
            "id": "check.item_1",
            "description": "(1)의 합에서 465를 빼면 236이 됩니다.",
            "expr": "701 - 465",
            "expected": 236,
            "actual": 236,
            "pass": True,
        },
        {
            "id": "check.item_2",
            "description": "(2)의 합에서 549를 빼면 756이 됩니다.",
            "expr": "1305 - 549",
            "expected": 756,
            "actual": 756,
            "pass": True,
        },
    ],
    "answer": SEMANTIC_OVERRIDE["answer"],
}


SEMANTIC_OVERRIDE["answer"] = SOLVABLE["answer"]
SEMANTIC_ANSWER = SOLVABLE["answer"]
