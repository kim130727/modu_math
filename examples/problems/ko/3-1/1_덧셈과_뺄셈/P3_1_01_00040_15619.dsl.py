from __future__ import annotations

from modu_math.dsl import (
    BlankSlot,
    Canvas,
    ProblemTemplate,
    Region,
    TextBoxSlot,
RectSlot)


PROBLEM_ID = "P3_1_01_00040_15619"
PROBLEM_TITLE = "동수가 어제와 오늘 읽은 책의 총쪽수"


ANSWER = {
    "type": "numeric",
    "value": 847,
    "unit": "쪽",
    "target_ref": "quantity.total_pages_read",
    "derived_from": "step.add_pages_read",
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
    },
    "domain": {
        "objects": [
            {
                "id": "person.dongsu",
                "type": "person",
                "label": "동수",
            },
            {
                "id": "object.book",
                "type": "book",
                "label": "책",
                "unit": "쪽",
            },
            {
                "id": "quantity.pages_read_yesterday",
                "type": "quantity",
                "label": "동수가 어제 읽은 책의 쪽수",
                "value": 415,
                "unit": "쪽",
            },
            {
                "id": "quantity.pages_read_today",
                "type": "quantity",
                "label": "동수가 오늘 읽은 책의 쪽수",
                "value": 432,
                "unit": "쪽",
            },
            {
                "id": "quantity.total_pages_read",
                "type": "quantity",
                "label": "동수가 어제와 오늘 읽은 책의 총쪽수",
                "value": 847,
                "unit": "쪽",
            },
        ],
        "relations": [
            {
                "id": "relation.dongsu_read_yesterday",
                "type": "read",
                "from_id": "person.dongsu",
                "to_id": "object.book",
                "quantity": "quantity.pages_read_yesterday",
                "time": "yesterday",
            },
            {
                "id": "relation.dongsu_read_today",
                "type": "read",
                "from_id": "person.dongsu",
                "to_id": "object.book",
                "quantity": "quantity.pages_read_today",
                "time": "today",
            },
            {
                "id": "relation.yesterday_pages_part_of_total",
                "type": "part_of_sum",
                "from_id": "quantity.pages_read_yesterday",
                "to_id": "quantity.total_pages_read",
            },
            {
                "id": "relation.today_pages_part_of_total",
                "type": "part_of_sum",
                "from_id": "quantity.pages_read_today",
                "to_id": "quantity.total_pages_read",
            },
        ],
    },
    "answer": ANSWER,
}

SEMANTIC_OVERRIDE = SEMANTIC


SOLVABLE = {
    "schema": "modu.solvable.v1.2",
    "problem_id": PROBLEM_ID,
    "problem_type": "numeric_answer_addition_word_problem",
    "inputs": {
        "target_label": "동수가 어제와 오늘 읽은 책의 총쪽수",
        "unit": "쪽",
        "quantities": {
            "pages_read_yesterday": 415,
            "pages_read_today": 432,
        },
        "conditions": [
            "동수는 어제 책을 415쪽 읽었습니다.",
            "동수는 오늘 책을 432쪽 읽었습니다.",
            "어제와 오늘 읽은 책의 쪽수를 모두 구합니다.",
        ],
    },
    "given": [
        {
            "ref": "quantity.pages_read_yesterday",
            "value": {
                "count": 415,
                "unit": "쪽",
                "person": "person.dongsu",
                "object": "object.book",
                "time": "yesterday",
            },
        },
        {
            "ref": "quantity.pages_read_today",
            "value": {
                "count": 432,
                "unit": "쪽",
                "person": "person.dongsu",
                "object": "object.book",
                "time": "today",
            },
        },
    ],
    "target": {
        "ref": "quantity.total_pages_read",
        "type": "number",
    },
    "understanding": {
        "summary": "동수가 어제와 오늘 읽은 책의 쪽수를 합하여 이틀 동안 읽은 총쪽수를 구하는 문제입니다.",
        "facts": [
            {
                "ref": "quantity.pages_read_yesterday",
                "label": "어제 읽은 책의 쪽수",
                "value": 415,
                "unit": "쪽",
                "source": "explicit",
            },
            {
                "ref": "quantity.pages_read_today",
                "label": "오늘 읽은 책의 쪽수",
                "value": 432,
                "unit": "쪽",
                "source": "explicit",
            },
        ],
        "unknowns": [
            {
                "ref": "quantity.total_pages_read",
                "label": "어제와 오늘 읽은 책의 총쪽수",
                "unit": "쪽",
                "source": "unknown",
            },
        ],
        "relation": {
            "type": "part_part_whole_addition",
            "statement": "어제와 오늘 읽은 책의 총쪽수는 각 날 읽은 쪽수를 더한 수입니다.",
            "symbolic": "총쪽수 = 어제 읽은 쪽수 + 오늘 읽은 쪽수",
            "uses": [
                "quantity.pages_read_yesterday",
                "quantity.pages_read_today",
            ],
            "result": "quantity.total_pages_read",
        },
        "diagnostic_questions": [
            {
                "id": "understand.target",
                "type": "multiple_choice",
                "prompt": "이 문제에서 구해야 하는 것은 무엇인가요?",
                "choices": [
                    "어제 읽은 책의 쪽수",
                    "오늘 읽은 책의 쪽수",
                    "어제와 오늘 읽은 책의 총쪽수",
                ],
                "answer_index": 2,
            },
            {
                "id": "understand.relation",
                "type": "multiple_choice",
                "prompt": "어제와 오늘 읽은 책의 쪽수를 모두 구하려면 어떻게 해야 하나요?",
                "choices": [
                    "415와 432를 더합니다.",
                    "432에서 415를 뺍니다.",
                    "415와 432를 비교합니다.",
                ],
                "answer_index": 0,
            },
        ],
        "student_restatement": {
            "prompt": "문제의 요지를 말해 볼까요?",
            "template": "{pages_read_yesterday}쪽과 {pages_read_today}쪽을 더해 {target_label}를 구합니다.",
            "answer": "415쪽과 432쪽을 더해 어제와 오늘 읽은 책의 총쪽수를 구합니다.",
        },
    },
    "method": "어제와 오늘 읽은 책의 쪽수를 덧셈으로 합하여 총쪽수를 구합니다.",
    "plan": [
        "어제 읽은 책의 쪽수 415쪽을 확인합니다.",
        "오늘 읽은 책의 쪽수 432쪽을 확인합니다.",
        "두 쪽수를 더하여 이틀 동안 읽은 총쪽수를 구합니다.",
    ],
    "steps": [
        {
            "id": "step.add_pages_read",
            "goal": "동수가 어제와 오늘 읽은 책의 총쪽수를 구합니다.",
            "uses": [
                "quantity.pages_read_yesterday",
                "quantity.pages_read_today",
            ],
            "relation_expr": "총쪽수 = 어제 읽은 쪽수 + 오늘 읽은 쪽수",
            "expr": "415 + 432",
            "value": {
                "count": 847,
                "unit": "쪽",
                "ref": "quantity.total_pages_read",
            },
            "explanation": "어제와 오늘 읽은 책의 쪽수를 모두 구해야 하므로 415와 432를 더합니다.",
        },
    ],
    "checks": [
        {
            "id": "check.subtract_yesterday_pages",
            "expr": "847 - 415",
            "expected": 432,
            "actual": 432,
            "pass": True,
        },
        {
            "id": "check.subtract_today_pages",
            "expr": "847 - 432",
            "expected": 415,
            "actual": 415,
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
            width = 600, height = 250, coordinate_mode="logical",
        ),
        regions=(
            Region(
                id="region.stem",
                role="stem",
                flow="vertical",
                slot_ids=("slot.question",'konva_1786962334798_text_49867', 'konva_1786962334798_rect_65307'),
            ),
        ),
        slots=(TextBoxSlot(
                id="slot.question",
                x = 14.098, y = 14.984, width = 458.689, height = 191.049, text=(
                    "동수는 책읽기를 좋아합니다. 어제는 415쪽을 읽었고, 오늘은 432쪽을 읽었습니다. "
                    "동수가 어제와 오늘 읽은 책의 쪽수는 모두 몇 쪽입니까?"
                ),
                font_size = 30, font_family='"Poor Story", "Noto Sans KR", sans-serif',
                fill="#202124",
                line_height=1.4,
                align="left",
                valign="top",
            ),
            BlankSlot(
                id="slot.expression",
                prompt="식",
                answer_key="415 + 432 = 847",
                placeholder="",
            ),
            BlankSlot(
                id="slot.answer",
                prompt="답",
                answer_key="847",
                placeholder="쪽",
            ),TextBoxSlot(id = 'konva_1786962334798_text_49867', prompt = '', text = '쪽', x = 521.984, y = 189.049, font_size = 30, fill = '#111827', width = 30.131, height = 46, align = 'left', line_height = 1.25), RectSlot(id = 'konva_1786962334798_rect_65307', prompt = '', x = 378.852, y = 186.393, width = 131.8, height = 51.25, fill = '#ffffff', stroke = '#111827', stroke_width = 1.2, interaction = {'type': 'input', 'role': 'answer', 'value_type': 'digit', 'max_length': 1, 'include_in_submission': True, 'order': 0, 'group_id': 'final_answer', 'answer_key_index': 0, 'answer_ref': 'answer.value', 'auto_advance': True, 'keyboard': 'number'}, input_style = {'font_size_mode': 'auto', 'font_size_adjust': 0, 'min_font_size': 14, 'max_font_size': 52, 'font_weight': 700, 'horizontal_align': 'center', 'vertical_align': 'middle', 'padding': 6, 'text_color': '#222222'})),
    )


PROBLEM_TEMPLATE = build_problem_template()
