from __future__ import annotations

from modu_math.dsl import (
    BlankSlot,
    Canvas,
    ProblemTemplate,
    Region,
    TextBoxSlot,
RectSlot)


PROBLEM_ID = "P3_1_01_00040_15607"
PROBLEM_TITLE = "처음 주차장에 있던 차의 수"


ANSWER = {
    "type": "numeric",
    "value": 377,
    "unit": "대",
    "target_ref": "quantity.initial_cars",
    "derived_from": "step.reconstruct_initial_count",
}


SEMANTIC_OVERRIDE = {
    "problem_id": PROBLEM_ID,
    "problem_type": "numeric_answer_initial_quantity_addition_word_problem",
    "metadata": {
        "grade": 3,
        "semester": 1,
        "subject": "수학",
        "topic": "세 자리 수의 덧셈",
        "language": "ko-KR",
        "question": "처음 주차장에 있던 차는 모두 몇 대입니까?",
    },
    "domain": {
        "objects": [
            {
                "id": "place.parking_lot",
                "type": "place",
                "label": "주차장",
            },
            {
                "id": "object.car",
                "type": "countable_object",
                "label": "차",
                "unit": "대",
            },
            {
                "id": "quantity.departed_cars",
                "type": "quantity",
                "label": "주차장에서 나간 차의 수",
                "value": 146,
                "unit": "대",
            },
            {
                "id": "quantity.remaining_cars",
                "type": "quantity",
                "label": "주차장에 남은 차의 수",
                "value": 231,
                "unit": "대",
            },
            {
                "id": "quantity.initial_cars",
                "type": "quantity",
                "label": "처음 주차장에 있던 차의 수",
                "value": 377,
                "unit": "대",
            },
        ],
        "relations": [
            {
                "id": "relation.cars_departed",
                "type": "departed_from",
                "subject": "quantity.departed_cars",
                "object": "object.car",
                "place": "place.parking_lot",
            },
            {
                "id": "relation.cars_remained",
                "type": "remained_at",
                "subject": "quantity.remaining_cars",
                "object": "object.car",
                "place": "place.parking_lot",
            },
            {
                "id": "relation.initial_count_is_sum",
                "type": "sum_of",
                "subject": "quantity.initial_cars",
                "objects": [
                    "quantity.departed_cars",
                    "quantity.remaining_cars",
                ],
            },
        ],
    },
    "answer": ANSWER,
}


SOLVABLE = {
    "schema": "modu.solvable.v1.2",
    "problem_id": PROBLEM_ID,
    "problem_type": "numeric_answer_initial_quantity_addition_word_problem",
    "inputs": {
        "target_label": "처음 주차장에 있던 차의 수",
        "unit": "대",
        "quantities": {
            "departed_count": 146,
            "remaining_count": 231,
        },
        "conditions": [
            "주차장에 있던 차 중에서 146대가 나갔습니다.",
            "차가 나간 뒤 주차장에 231대가 남았습니다.",
            "나간 차와 남은 차는 모두 처음 주차장에 있던 차에 포함됩니다.",
        ],
    },
    "given": [
        {
            "ref": "quantity.departed_cars",
            "value": {
                "count": 146,
                "unit": "대",
                "object": "object.car",
                "place": "place.parking_lot",
                "state": "departed",
            },
        },
        {
            "ref": "quantity.remaining_cars",
            "value": {
                "count": 231,
                "unit": "대",
                "object": "object.car",
                "place": "place.parking_lot",
                "state": "remaining",
            },
        },
    ],
    "target": {
        "ref": "quantity.initial_cars",
        "type": "number",
    },
    "understanding": {
        "summary": "주차장에서 나간 차와 남은 차를 합하여 처음 주차장에 있던 차의 수를 구하는 문제입니다.",
        "facts": [
            {
                "ref": "quantity.departed_cars",
                "label": "주차장에서 나간 차의 수",
                "value": 146,
                "unit": "대",
                "source": "explicit",
            },
            {
                "ref": "quantity.remaining_cars",
                "label": "주차장에 남은 차의 수",
                "value": 231,
                "unit": "대",
                "source": "explicit",
            },
        ],
        "unknowns": [
            {
                "ref": "quantity.initial_cars",
                "label": "처음 주차장에 있던 차의 수",
                "unit": "대",
                "source": "unknown",
            },
        ],
        "relation": {
            "type": "change_start_unknown_addition",
            "statement": "처음 있던 차는 나간 차와 남은 차를 합한 수입니다.",
            "symbolic": "처음 차의 수 = 나간 차의 수 + 남은 차의 수",
            "uses": [
                "quantity.departed_cars",
                "quantity.remaining_cars",
            ],
            "result": "quantity.initial_cars",
        },
        "diagnostic_questions": [
            {
                "id": "understand.target",
                "type": "multiple_choice",
                "prompt": "이 문제에서 구해야 하는 것은 무엇인가요?",
                "choices": [
                    "주차장에서 나간 차의 수",
                    "주차장에 남은 차의 수",
                    "처음 주차장에 있던 차의 수",
                ],
                "answer_index": 2,
            },
            {
                "id": "understand.parts",
                "type": "multiple_choice",
                "prompt": "처음 주차장에 있던 차는 어느 두 부분으로 나누어졌나요?",
                "choices": [
                    "나간 차와 남은 차",
                    "나간 차와 새로 들어온 차",
                    "남은 차와 새로 들어온 차",
                ],
                "answer_index": 0,
            },
            {
                "id": "understand.operation",
                "type": "multiple_choice",
                "prompt": "처음 차의 수를 구하는 식은 무엇인가요?",
                "choices": ["146 + 231", "231 - 146", "146 - 231"],
                "answer_index": 0,
            },
        ],
        "student_restatement": {
            "prompt": "문제의 요지를 말해 볼까요?",
            "template": "나간 {departed_count}대와 남은 {remaining_count}대를 더해 처음 차의 수를 구합니다.",
            "answer": "나간 146대와 남은 231대를 더해 처음 주차장에 있던 차의 수를 구합니다.",
        },
    },
    "method": "나간 차 146대와 남은 차 231대를 더해 처음 차의 수를 복원합니다.",
    "plan": [
        "주차장에서 나간 차의 수 146대를 확인합니다.",
        "주차장에 남은 차의 수 231대를 확인합니다.",
        "두 수를 더하여 처음 주차장에 있던 차의 수를 구합니다.",
    ],
    "steps": [
        {
            "id": "step.reconstruct_initial_count",
            "goal": "처음 주차장에 있던 차의 수를 구합니다.",
            "uses": [
                "quantity.departed_cars",
                "quantity.remaining_cars",
            ],
            "relation_expr": "처음 차의 수 = 나간 차의 수 + 남은 차의 수",
            "expr": "146 + 231",
            "value": 377,
            "explanation": "처음 있던 차는 나간 차와 남은 차로 나누어지므로 146과 231을 더합니다.",
        },
    ],
    "checks": [
        {
            "id": "check.subtract_departed_count",
            "expr": "377 - 146",
            "expected": 231,
            "actual": 231,
            "pass": True,
        },
        {
            "id": "check.subtract_remaining_count",
            "expr": "377 - 231",
            "expected": 146,
            "actual": 146,
            "pass": True,
        },
        {
            "id": "check.initial_is_larger",
            "expr": "377 > 146 and 377 > 231",
            "expected": True,
            "actual": True,
            "pass": True,
        },
    ],
    "answer": ANSWER,
}


SEMANTIC_ANSWER = SOLVABLE["answer"]


def build_problem_template() -> ProblemTemplate:
    return ProblemTemplate(
        id=PROBLEM_ID,
        title=PROBLEM_TITLE,
        canvas=Canvas(
            width = 600, height = 180, coordinate_mode="logical",
        ),
        regions=(
            Region(
                id="region.stem",
                role="stem",
                flow="vertical",
                slot_ids=("slot.question",
                    "slot.expression",'konva_1786318975740_paste_229834_0', 'konva_1786319433892_rect_505049'),
            ),
        ),
        slots=(TextBoxSlot(
                id="slot.question",
                x = 24.065, y = 8.892, width = 449.62, height = 135.525, text=(
                    "주차장에 있던 차 중에서 146대가 나가고 231대가 남았습니다. "
                    "처음 주차장에 있던 차는 모두 몇 대입니까?"
                ),
                font_size = 30, font_family='"Poor Story", "Noto Sans KR", sans-serif',
                fill="#202124",
                line_height=1.45,
                align="left",
                valign="top",
            ),
            TextBoxSlot(
                id="slot.expression",
                x=20,
                y=84,
                width=860,
                height=32,
                text="식",
                font_size=22,
                font_family='"Poor Story", "Noto Sans KR", sans-serif',
                fill="#202124",
                align="left",
                valign="middle",
            ),
            TextBoxSlot(id = 'konva_1786318975740_paste_229834_0', prompt = '', text = '대', x = 489.934, y = 126.868, font_size = 30, fill = '#202124', width = 49.95, height = 52, align = 'left', line_height = 1.45), RectSlot(id = 'konva_1786319433892_rect_505049', prompt = '', x = 380.353, y = 129.995, width = 98.185, height = 39.96, fill = '#ffffff', stroke = '#111827', stroke_width = 1.2, interaction = {'type': 'input', 'role': 'answer', 'value_type': 'digit', 'max_length': 1, 'include_in_submission': True, 'order': 0, 'group_id': 'final_answer', 'auto_advance': True, 'keyboard': 'number'}, input_style = {'font_size_mode': 'auto', 'font_size_adjust': 0, 'min_font_size': 14, 'max_font_size': 52, 'font_weight': 700, 'horizontal_align': 'center', 'vertical_align': 'middle', 'padding': 6, 'text_color': '#222222'})),
    )


PROBLEM_TEMPLATE = build_problem_template()
