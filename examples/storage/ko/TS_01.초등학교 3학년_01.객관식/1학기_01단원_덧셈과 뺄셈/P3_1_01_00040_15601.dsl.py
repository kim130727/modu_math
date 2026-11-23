from __future__ import annotations

from modu_math.dsl import (
    BlankSlot,
    Canvas,
    ProblemTemplate,
    Region,
    TextBoxSlot,
RectSlot)


PROBLEM_ID = "P3_1_01_00040_15601"
PROBLEM_TITLE = "동민이의 우표 수"


ANSWER = {
    "type": "numeric",
    "value": 648,
    "unit": "장",
    "target_ref": "quantity.total_stamp_count",
    "derived_from": "step.add_stamp_counts",
}


SEMANTIC = {
    "problem_id": PROBLEM_ID,
    "problem_type": "numeric_answer_addition_word_problem",
    "metadata": {
        "grade": 3,
        "semester": 1,
        "subject": "수학",
        "topic": "세 자리 수의 덧셈",
        "language": "ko-KR",
        "question": (
            "동민이가 가지고 있는 우표책에는 327장의 외국 우표와 "
            "321장의 한국 우표가 있습니다. 우표는 모두 몇 장입니까?"
        ),
        "instruction": "외국 우표 수와 한국 우표 수를 더합니다.",
    },
    "domain": {
        "objects": [
            {
                "id": "person.dongmin",
                "type": "person",
                "label": "동민이",
            },
            {
                "id": "object.stamp_album",
                "type": "container",
                "label": "우표책",
            },
            {
                "id": "object.foreign_stamp",
                "type": "countable_object",
                "label": "외국 우표",
                "unit": "장",
            },
            {
                "id": "object.korean_stamp",
                "type": "countable_object",
                "label": "한국 우표",
                "unit": "장",
            },
            {
                "id": "quantity.foreign_stamp_count",
                "type": "quantity",
                "label": "외국 우표 수",
                "value": 327,
                "unit": "장",
            },
            {
                "id": "quantity.korean_stamp_count",
                "type": "quantity",
                "label": "한국 우표 수",
                "value": 321,
                "unit": "장",
            },
            {
                "id": "quantity.total_stamp_count",
                "type": "unknown_quantity",
                "label": "우표의 전체 수",
                "unit": "장",
            },
        ],
        "relations": [
            {
                "id": "relation.dongmin_owns_album",
                "type": "owns",
                "from_id": "person.dongmin",
                "to_id": "object.stamp_album",
            },
            {
                "id": "relation.album_contains_foreign_stamps",
                "type": "contains",
                "from_id": "object.stamp_album",
                "to_id": "object.foreign_stamp",
                "quantity": "quantity.foreign_stamp_count",
            },
            {
                "id": "relation.album_contains_korean_stamps",
                "type": "contains",
                "from_id": "object.stamp_album",
                "to_id": "object.korean_stamp",
                "quantity": "quantity.korean_stamp_count",
            },
            {
                "id": "relation.total_is_sum",
                "type": "sum_of",
                "subject": "quantity.total_stamp_count",
                "objects": [
                    "quantity.foreign_stamp_count",
                    "quantity.korean_stamp_count",
                ],
            },
        ],
        "problem_solving": {
            "understand": {
                "given_refs": [
                    "quantity.foreign_stamp_count",
                    "quantity.korean_stamp_count",
                ],
                "target_ref": "quantity.total_stamp_count",
                "condition_refs": ["relation.total_is_sum"],
            },
            "plan": {
                "method": "part_part_whole_addition",
                "description": "두 종류의 우표 수를 더하여 전체 우표 수를 구합니다.",
            },
            "execute": {
                "expected_operations": ["addition"],
            },
            "review": {
                "check_methods": ["subtraction_check", "column_addition_check"],
            },
        },
    },
    "answer": ANSWER,
}

SEMANTIC_OVERRIDE = SEMANTIC


SOLVABLE = {
    "schema": "modu.solvable.v1.2",
    "problem_id": PROBLEM_ID,
    "problem_type": "numeric_answer_addition_word_problem",
    "inputs": {
        "target_label": "우표의 전체 수",
        "unit": "장",
        "quantities": {
            "foreign_stamp_count": 327,
            "korean_stamp_count": 321,
        },
        "conditions": [
            "동민이의 우표책에는 외국 우표가 327장 있습니다.",
            "동민이의 우표책에는 한국 우표가 321장 있습니다.",
            "두 종류의 우표를 합한 전체 수를 구합니다.",
        ],
    },
    "given": [
        {
            "ref": "quantity.foreign_stamp_count",
            "value": {
                "count": 327,
                "unit": "장",
                "object": "object.foreign_stamp",
                "container": "object.stamp_album",
            },
        },
        {
            "ref": "quantity.korean_stamp_count",
            "value": {
                "count": 321,
                "unit": "장",
                "object": "object.korean_stamp",
                "container": "object.stamp_album",
            },
        },
    ],
    "target": {
        "ref": "quantity.total_stamp_count",
        "type": "number",
    },
    "understanding": {
        "summary": "외국 우표 327장과 한국 우표 321장을 합해 전체 우표 수를 구하는 문제입니다.",
        "facts": [
            {
                "ref": "quantity.foreign_stamp_count",
                "label": "외국 우표 수",
                "value": 327,
                "unit": "장",
                "source": "explicit",
            },
            {
                "ref": "quantity.korean_stamp_count",
                "label": "한국 우표 수",
                "value": 321,
                "unit": "장",
                "source": "explicit",
            },
        ],
        "unknowns": [
            {
                "ref": "quantity.total_stamp_count",
                "label": "우표의 전체 수",
                "unit": "장",
                "source": "unknown",
            },
        ],
        "relation": {
            "type": "part_part_whole_addition",
            "statement": "외국 우표 수와 한국 우표 수를 더하면 우표의 전체 수가 됩니다.",
            "symbolic": "327 + 321 = □",
            "uses": [
                "quantity.foreign_stamp_count",
                "quantity.korean_stamp_count",
            ],
            "result": "quantity.total_stamp_count",
        },
        "diagnostic_questions": [
            {
                "id": "understand.target",
                "type": "multiple_choice",
                "prompt": "이 문제에서 구해야 하는 것은 무엇인가요?",
                "choices": [
                    "외국 우표 수",
                    "한국 우표 수",
                    "우표의 전체 수",
                ],
                "answer_index": 2,
            },
            {
                "id": "understand.operation",
                "type": "multiple_choice",
                "prompt": "우표의 전체 수를 구하려면 어떻게 해야 하나요?",
                "choices": [
                    "327과 321을 더합니다.",
                    "327에서 321을 뺍니다.",
                    "327과 321을 비교합니다.",
                ],
                "answer_index": 0,
            },
        ],
        "student_restatement": {
            "prompt": "문제의 뜻을 자신의 말로 나타내어 보세요.",
            "template": "{foreign_count}장과 {korean_count}장을 더해 {target_label}를 구합니다.",
            "answer": "외국 우표 327장과 한국 우표 321장을 더해 우표의 전체 수를 구합니다.",
        },
    },
    "method": "외국 우표 수와 한국 우표 수를 덧셈하여 전체 우표 수를 구합니다.",
    "plan": [
        "외국 우표 수 327장을 확인합니다.",
        "한국 우표 수 321장을 확인합니다.",
        "두 수를 더하여 우표의 전체 수를 구합니다.",
    ],
    "steps": [
        {
            "id": "step.add_stamp_counts",
            "goal": "우표의 전체 수를 구합니다.",
            "uses": [
                "quantity.foreign_stamp_count",
                "quantity.korean_stamp_count",
            ],
            "relation_expr": "전체 우표 수 = 외국 우표 수 + 한국 우표 수",
            "expr": "327 + 321",
            "value": 648,
            "explanation": "두 종류의 우표를 모두 세어야 하므로 327과 321을 더합니다.",
        },
    ],
    "checks": [
        {
            "id": "check.inverse_subtraction",
            "expr": "648 - 321",
            "expected": 327,
            "actual": 327,
            "pass": True,
        },
        {
            "id": "check.column_addition",
            "expr": "7 + 1 = 8, 2 + 2 = 4, 3 + 3 = 6",
            "expected": 648,
            "actual": 648,
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
            width=900,
            height=180,
            coordinate_mode="logical",
        ),
        regions=(
            Region(
                id="region.stem",
                role="stem",
                flow="vertical",
                slot_ids=("slot.answer",'konva_1785806283023_text_716753', 'konva_1785806283023_text_736409', 'konva_1785806283023_rect_753834'),
            ),
        ),
        slots=(BlankSlot(
                id="slot.answer",
                prompt="답",
                answer_key="648",
                placeholder="장",
            ),TextBoxSlot(id = 'konva_1785806283023_text_716753', prompt = '', text = '장', x = 806.532, y = 114.194, font_size = 30, fill = '#111827', width = 51.495, height = 46, align = 'left', line_height = 1.25), TextBoxSlot(id = 'konva_1785806283023_text_736409', prompt = '', text = '동민이가 가지고 있는 우표책에는 327장의 외국 우표와 321장의 한국 우표가 있습니다. 우표는 모두 몇 장입니까?', x = 19.815, y = 10.735, font_size = 30, fill = '#111827', width = 860, height = 83, align = 'left', line_height = 1.25), RectSlot(id = 'konva_1785806283023_rect_753834', prompt = '', x = 612.713, y = 107.579, width = 180, height = 54.616, fill = '#ffffff', stroke = '#111827', stroke_width = 1.2, interaction = {'type': 'input', 'role': 'answer', 'value_type': 'digit', 'max_length': 1, 'include_in_submission': True, 'order': 0, 'group_id': 'final_answer', 'auto_advance': True, 'keyboard': 'number'}, input_style = {'font_size_mode': 'auto', 'font_size_adjust': 0, 'min_font_size': 14, 'max_font_size': 52, 'font_weight': 700, 'horizontal_align': 'center', 'vertical_align': 'middle', 'padding': 6, 'text_color': '#222222'})),
    )


PROBLEM_TEMPLATE = build_problem_template()
