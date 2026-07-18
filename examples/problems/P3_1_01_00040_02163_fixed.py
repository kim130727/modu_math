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


PROBLEM_ID = "P3_1_01_00040_02163"
PROBLEM_TITLE = "덧셈식의 빈칸에 알맞은 수 쓰기"


def build_problem_template() -> ProblemTemplate:
    return ProblemTemplate(
        id=PROBLEM_ID,
        title=PROBLEM_TITLE,
        canvas=Canvas(
            width=430,
            height=165,
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
                    "slot.number_1_top",
                    "slot.plus_1",
                    "slot.number_1_bottom_hundreds",
                    "slot.blank_1_tens",
                    "slot.number_1_bottom_ones",
                    "slot.line_1",
                    "slot.blank_1_answer_hundreds",
                    "slot.number_1_answer_rest",
                    "slot.label_2",
                    "slot.blank_2_top_hundreds",
                    "slot.number_2_top_rest",
                    "slot.plus_2",
                    "slot.number_2_bottom_hundreds",
                    "slot.blank_2_bottom_tens",
                    "slot.number_2_bottom_ones",
                    "slot.line_2",
                    "slot.number_2_answer",
                ),
            ),
        ),
        slots=(
            TextBoxSlot(
                id="slot.instruction",
                text="다음 계산이 맞도록 □ 안에 알맞은 수를 써넣으시오.",
                prompt="덧셈식이 성립하도록 네 개의 빈칸에 알맞은 숫자를 쓰라는 안내",
                semantic_role="instruction",
                x=18,
                y=7,
                width=390,
                height=30,
                font_size=17,
                line_height=1.2,
                fill="#111111",
                align="left",
            ),
            # ---------------------------------------------------------
            # (1) 653 + 2□8 = □31
            # 정답: 653 + 278 = 931
            # ---------------------------------------------------------
            TextSlot(
                id="slot.label_1",
                text="(1)",
                prompt="첫 번째 계산 번호",
                x=20,
                y=48,
                font_size=18,
                anchor="start",
                fill="#111111",
            ),
            TextSlot(
                id="slot.number_1_top",
                text="653",
                prompt="첫 번째 덧셈의 위 수 653",
                x=111,
                y=48,
                font_size=22,
                anchor="end",
                fill="#111111",
            ),
            TextSlot(
                id="slot.plus_1",
                text="+",
                prompt="첫 번째 덧셈 기호",
                x=49,
                y=79,
                font_size=22,
                anchor="middle",
                fill="#111111",
            ),
            TextSlot(
                id="slot.number_1_bottom_hundreds",
                text="2",
                prompt="첫 번째 덧셈 아래 수의 백의 자리 2",
                x=76,
                y=79,
                font_size=22,
                anchor="middle",
                fill="#111111",
            ),
            TextSlot(
                id="slot.blank_1_tens",
                text="□",
                prompt="첫 번째 덧셈 아래 수의 십의 자리 빈칸",
                x=90,
                y=79,
                font_size=22,
                anchor="middle",
                fill="#111111",
            ),
            TextSlot(
                id="slot.number_1_bottom_ones",
                text="8",
                prompt="첫 번째 덧셈 아래 수의 일의 자리 8",
                x=104,
                y=79,
                font_size=22,
                anchor="middle",
                fill="#111111",
            ),
            LineSlot(
                id="slot.line_1",
                prompt="첫 번째 세로셈의 계산선",
                x1=43,
                y1=94,
                x2=116,
                y2=94,
                stroke="#111111",
                stroke_width=1.5,
            ),
            TextSlot(
                id="slot.blank_1_answer_hundreds",
                text="□",
                prompt="첫 번째 덧셈 결과의 백의 자리 빈칸",
                x=76,
                y=126,
                font_size=22,
                anchor="middle",
                fill="#111111",
            ),
            TextSlot(
                id="slot.number_1_answer_rest",
                text="31",
                prompt="첫 번째 덧셈 결과의 십의 자리와 일의 자리 31",
                x=110,
                y=126,
                font_size=22,
                anchor="end",
                fill="#111111",
            ),
            # ---------------------------------------------------------
            # (2) □25 + 3□9 = 804
            # 정답: 425 + 379 = 804
            # ---------------------------------------------------------
            TextSlot(
                id="slot.label_2",
                text="(2)",
                prompt="두 번째 계산 번호",
                x=145,
                y=48,
                font_size=18,
                anchor="start",
                fill="#111111",
            ),
            TextSlot(
                id="slot.blank_2_top_hundreds",
                text="□",
                prompt="두 번째 덧셈 위 수의 백의 자리 빈칸",
                x=201,
                y=48,
                font_size=22,
                anchor="middle",
                fill="#111111",
            ),
            TextSlot(
                id="slot.number_2_top_rest",
                text="25",
                prompt="두 번째 덧셈 위 수의 십의 자리와 일의 자리 25",
                x=235,
                y=48,
                font_size=22,
                anchor="end",
                fill="#111111",
            ),
            TextSlot(
                id="slot.plus_2",
                text="+",
                prompt="두 번째 덧셈 기호",
                x=174,
                y=79,
                font_size=22,
                anchor="middle",
                fill="#111111",
            ),
            TextSlot(
                id="slot.number_2_bottom_hundreds",
                text="3",
                prompt="두 번째 덧셈 아래 수의 백의 자리 3",
                x=201,
                y=79,
                font_size=22,
                anchor="middle",
                fill="#111111",
            ),
            TextSlot(
                id="slot.blank_2_bottom_tens",
                text="□",
                prompt="두 번째 덧셈 아래 수의 십의 자리 빈칸",
                x=215,
                y=79,
                font_size=22,
                anchor="middle",
                fill="#111111",
            ),
            TextSlot(
                id="slot.number_2_bottom_ones",
                text="9",
                prompt="두 번째 덧셈 아래 수의 일의 자리 9",
                x=229,
                y=79,
                font_size=22,
                anchor="middle",
                fill="#111111",
            ),
            LineSlot(
                id="slot.line_2",
                prompt="두 번째 세로셈의 계산선",
                x1=168,
                y1=94,
                x2=241,
                y2=94,
                stroke="#111111",
                stroke_width=1.5,
            ),
            TextSlot(
                id="slot.number_2_answer",
                text="804",
                prompt="두 번째 덧셈의 결과 804",
                x=235,
                y=126,
                font_size=22,
                anchor="end",
                fill="#111111",
            ),
            # 실제 정답 데이터용 빈칸 슬롯
            # 화면의 네모는 위 TextSlot(text="□")에서 표시합니다.
            BlankSlot(
                id="answer.problem_1.tens",
                prompt="첫 번째 덧셈 아래 수의 십의 자리",
                answer_key="7",
                placeholder="",
            ),
            BlankSlot(
                id="answer.problem_1.result_hundreds",
                prompt="첫 번째 덧셈 결과의 백의 자리",
                answer_key="9",
                placeholder="",
            ),
            BlankSlot(
                id="answer.problem_2.top_hundreds",
                prompt="두 번째 덧셈 위 수의 백의 자리",
                answer_key="4",
                placeholder="",
            ),
            BlankSlot(
                id="answer.problem_2.bottom_tens",
                prompt="두 번째 덧셈 아래 수의 십의 자리",
                answer_key="7",
                placeholder="",
            ),
        ),
        diagrams=(),
        groups=(
            Group(
                id="group.problem_1",
                role="vertical_addition_with_blanks",
                member_ids=(
                    "slot.label_1",
                    "slot.number_1_top",
                    "slot.plus_1",
                    "slot.number_1_bottom_hundreds",
                    "slot.blank_1_tens",
                    "slot.number_1_bottom_ones",
                    "slot.line_1",
                    "slot.blank_1_answer_hundreds",
                    "slot.number_1_answer_rest",
                ),
            ),
            Group(
                id="group.problem_2",
                role="vertical_addition_with_blanks",
                member_ids=(
                    "slot.label_2",
                    "slot.blank_2_top_hundreds",
                    "slot.number_2_top_rest",
                    "slot.plus_2",
                    "slot.number_2_bottom_hundreds",
                    "slot.blank_2_bottom_tens",
                    "slot.number_2_bottom_ones",
                    "slot.line_2",
                    "slot.number_2_answer",
                ),
            ),
        ),
        constraints=(),
        tags=(
            "grade-3",
            "addition",
            "three-digit-addition",
            "vertical-calculation",
            "missing-digit",
            "numeric-answer",
        ),
    )


PROBLEM_TEMPLATE = build_problem_template()


SEMANTIC_OVERRIDE = {
    "problem_id": PROBLEM_ID,
    "problem_type": "multi_missing_digit_addition",
    "metadata": {
        "grade": 3,
        "semester": 1,
        "subject": "수학",
        "topic": "세 자리 수의 덧셈",
        "language": "ko-KR",
        "question": "다음 계산이 맞도록 □ 안에 알맞은 수를 써넣으시오.",
    },
    "domain": {
        "objects": [
            {
                "id": "calculation.1",
                "type": "vertical_addition_with_blanks",
                "label": "첫 번째 덧셈",
                "expression_pattern": "653 + 2□8 = □31",
                "completed_expression": "653 + 278 = 931",
            },
            {
                "id": "calculation.2",
                "type": "vertical_addition_with_blanks",
                "label": "두 번째 덧셈",
                "expression_pattern": "□25 + 3□9 = 804",
                "completed_expression": "425 + 379 = 804",
            },
        ],
        "relations": [
            {
                "id": "relation.1",
                "type": "place_value_addition",
                "from_ids": [
                    "number.653",
                    "number.278",
                ],
                "to_id": "number.931",
                "equation": "653 + 278 = 931",
            },
            {
                "id": "relation.2",
                "type": "place_value_addition",
                "from_ids": [
                    "number.425",
                    "number.379",
                ],
                "to_id": "number.804",
                "equation": "425 + 379 = 804",
            },
        ],
    },
    "answer": {
        "blanks": [
            {
                "id": "answer.problem_1.tens",
                "type": "digit",
                "value": 7,
            },
            {
                "id": "answer.problem_1.result_hundreds",
                "type": "digit",
                "value": 9,
            },
            {
                "id": "answer.problem_2.top_hundreds",
                "type": "digit",
                "value": 4,
            },
            {
                "id": "answer.problem_2.bottom_tens",
                "type": "digit",
                "value": 7,
            },
        ],
        "choices": [],
        "answer_key": [
            {
                "blank_id": "answer.problem_1.tens",
                "value": 7,
            },
            {
                "blank_id": "answer.problem_1.result_hundreds",
                "value": 9,
            },
            {
                "blank_id": "answer.problem_2.top_hundreds",
                "value": 4,
            },
            {
                "blank_id": "answer.problem_2.bottom_tens",
                "value": 7,
            },
        ],
    },
}


SOLVABLE = {
    "schema": "modu.solvable.v1.2",
    "problem_id": PROBLEM_ID,
    "problem_type": "multi_missing_digit_addition",
    "inputs": {
        "target_label": "각 빈칸에 들어갈 숫자",
        "unit": "",
        "quantities": {
            "problem_1": {
                "expression_pattern": "653 + 2□8 = □31",
            },
            "problem_2": {
                "expression_pattern": "□25 + 3□9 = 804",
            },
        },
        "conditions": [
            "각 □에는 0부터 9까지의 숫자 하나가 들어갑니다.",
            "같은 자리끼리 더합니다.",
            "각 자리의 합이 10 이상이면 바로 윗자리로 1을 받아올림합니다.",
        ],
    },
    "given": [
        {
            "ref": "calculation.1",
            "value": {
                "expression_pattern": "653 + 2□8 = □31",
            },
        },
        {
            "ref": "calculation.2",
            "value": {
                "expression_pattern": "□25 + 3□9 = 804",
            },
        },
    ],
    "target": {
        "ref": "answer.all_blanks",
        "type": "missing_digits",
    },
    "understanding": {
        "summary": "세로 덧셈의 각 자리 계산과 받아올림을 이용하여 네 개의 빈칸에 들어갈 숫자를 찾는 문제입니다.",
        "facts": [
            {
                "ref": "calculation.1",
                "label": "첫 번째 덧셈",
                "value": "653 + 2□8 = □31",
                "unit": "",
                "source": "explicit",
            },
            {
                "ref": "calculation.2",
                "label": "두 번째 덧셈",
                "value": "□25 + 3□9 = 804",
                "unit": "",
                "source": "explicit",
            },
        ],
        "unknowns": [
            {
                "ref": "answer.problem_1.tens",
                "label": "첫 번째 식의 아래 수 십의 자리",
                "unit": "",
                "source": "unknown",
            },
            {
                "ref": "answer.problem_1.result_hundreds",
                "label": "첫 번째 식의 결과 백의 자리",
                "unit": "",
                "source": "unknown",
            },
            {
                "ref": "answer.problem_2.top_hundreds",
                "label": "두 번째 식의 위 수 백의 자리",
                "unit": "",
                "source": "unknown",
            },
            {
                "ref": "answer.problem_2.bottom_tens",
                "label": "두 번째 식의 아래 수 십의 자리",
                "unit": "",
                "source": "unknown",
            },
        ],
        "relation": {
            "type": "column_addition_with_carry",
            "statement": "일의 자리부터 계산하고, 받아올림을 다음 자리의 합에 포함하여 빈칸의 숫자를 찾습니다.",
            "symbolic": "ones -> carry -> tens -> carry -> hundreds",
            "uses": [
                "calculation.1",
                "calculation.2",
            ],
            "result": "answer.all_blanks",
        },
        "diagnostic_questions": [
            {
                "id": "understand.start_place",
                "type": "multiple_choice",
                "prompt": "빈칸이 있는 세로 덧셈은 어느 자리부터 살펴보는 것이 좋나요?",
                "choices": [
                    "일의 자리",
                    "백의 자리",
                    "아무 자리",
                ],
                "answer_index": 0,
            },
            {
                "id": "understand.carry",
                "type": "multiple_choice",
                "prompt": "한 자리의 합이 10 이상이면 무엇을 해야 하나요?",
                "choices": [
                    "다음 윗자리로 1을 받아올림한다.",
                    "그 자리의 계산을 생략한다.",
                    "항상 0을 쓴다.",
                ],
                "answer_index": 0,
            },
        ],
        "student_restatement": {
            "prompt": "문제의 뜻을 말해 볼까요?",
            "template": "각 자리의 덧셈과 받아올림을 이용하여 {blank_count}개의 빈칸을 채웁니다.",
            "answer": "각 자리의 덧셈과 받아올림을 이용하여 네 개의 빈칸에 알맞은 숫자를 씁니다.",
        },
    },
    "method": "일의 자리부터 같은 자리끼리 계산하고, 받아올림을 반영하여 빈칸의 숫자를 역으로 찾습니다.",
    "plan": [
        "각 식의 일의 자리 계산에서 받아올림이 있는지 확인합니다.",
        "받아올림을 포함하여 십의 자리의 빈칸을 찾습니다.",
        "십의 자리에서 생긴 받아올림을 포함하여 백의 자리의 빈칸을 찾습니다.",
        "완성된 수를 원래 덧셈식에 넣어 검산합니다.",
    ],
    "steps": [
        {
            "id": "step.1",
            "goal": "첫 번째 식의 아래 수 십의 자리 숫자를 찾습니다.",
            "uses": ["calculation.1"],
            "expr": "5 + □ + 1 = 13",
            "value": {
                "digit": 7,
                "ref": "answer.problem_1.tens",
            },
            "explanation": "일의 자리에서 3+8=11이므로 1을 받아올림합니다. 십의 자리 결과가 3이므로 5+□+1=13입니다. 따라서 빈칸은 7입니다.",
        },
        {
            "id": "step.2",
            "goal": "첫 번째 식의 결과 백의 자리 숫자를 찾습니다.",
            "uses": ["calculation.1"],
            "expr": "6 + 2 + 1 = 9",
            "value": {
                "digit": 9,
                "ref": "answer.problem_1.result_hundreds",
            },
            "explanation": "십의 자리에서 5+7+1=13이므로 1을 받아올림합니다. 백의 자리에서 6+2+1=9이므로 결과의 백의 자리 빈칸은 9입니다.",
        },
        {
            "id": "step.3",
            "goal": "두 번째 식의 아래 수 십의 자리 숫자를 찾습니다.",
            "uses": ["calculation.2"],
            "expr": "2 + □ + 1 = 10",
            "value": {
                "digit": 7,
                "ref": "answer.problem_2.bottom_tens",
            },
            "explanation": "일의 자리에서 5+9=14이므로 1을 받아올림합니다. 결과의 십의 자리가 0이므로 2+□+1=10입니다. 따라서 빈칸은 7입니다.",
        },
        {
            "id": "step.4",
            "goal": "두 번째 식의 위 수 백의 자리 숫자를 찾습니다.",
            "uses": ["calculation.2"],
            "expr": "□ + 3 + 1 = 8",
            "value": {
                "digit": 4,
                "ref": "answer.problem_2.top_hundreds",
            },
            "explanation": "십의 자리에서 2+7+1=10이므로 1을 받아올림합니다. 백의 자리에서 □+3+1=8이므로 빈칸은 4입니다.",
        },
    ],
    "checks": [
        {
            "id": "check.1",
            "description": "첫 번째 식에 찾은 숫자를 넣으면 653+278=931이 됩니다.",
            "expr": "653 + 278",
            "expected": 931,
            "actual": 931,
            "pass": True,
        },
        {
            "id": "check.2",
            "description": "두 번째 식에 찾은 숫자를 넣으면 425+379=804가 됩니다.",
            "expr": "425 + 379",
            "expected": 804,
            "actual": 804,
            "pass": True,
        },
    ],
    "answer": {
        "blanks": [
            {
                "id": "answer.problem_1.tens",
                "type": "digit",
                "value": 7,
                "unit": "",
            },
            {
                "id": "answer.problem_1.result_hundreds",
                "type": "digit",
                "value": 9,
                "unit": "",
            },
            {
                "id": "answer.problem_2.top_hundreds",
                "type": "digit",
                "value": 4,
                "unit": "",
            },
            {
                "id": "answer.problem_2.bottom_tens",
                "type": "digit",
                "value": 7,
                "unit": "",
            },
        ],
        "choices": [],
        "answer_key": [
            {
                "blank_id": "answer.problem_1.tens",
                "value": 7,
                "unit": "",
            },
            {
                "blank_id": "answer.problem_1.result_hundreds",
                "value": 9,
                "unit": "",
            },
            {
                "blank_id": "answer.problem_2.top_hundreds",
                "value": 4,
                "unit": "",
            },
            {
                "blank_id": "answer.problem_2.bottom_tens",
                "value": 7,
                "unit": "",
            },
        ],
        "value": [7, 9, 4, 7],
        "unit": "",
        "sentence": "(1)의 빈칸은 7, 9이고, (2)의 빈칸은 4, 7입니다.",
    },
}


SEMANTIC_OVERRIDE["answer"] = SOLVABLE["answer"]
