from __future__ import annotations

from modu_math.dsl import (
    Canvas,
    ProblemTemplate,
    Region,
    TextBoxSlot,
RectSlot)


PROBLEM_ID = "P3_1_01_00040_00472"
PROBLEM_TITLE = "도서관에서 책을 읽고 있는 사람 수"


def build_problem_template() -> ProblemTemplate:
    return ProblemTemplate(
        id=PROBLEM_ID,
        title=PROBLEM_TITLE,
        canvas=Canvas(
            width = 600, height = 220, coordinate_mode="logical",
        ),
        regions=(
            Region(
                id="region.stem",
                role="stem",
                flow="absolute",
                slot_ids=("slot.question",
                    'konva_1785110879232_paste_690676_0', 'konva_1785110879232_paste_716370_0', 'konva_1785110879232_paste_740217_0'),
            ),
        ),
        slots=(TextBoxSlot(
                id="slot.question",
                x=38,
                y=22,
                width = 583.928, height = 68, text = '도서관에서 어른 648명, 어린이 476명이 책을 읽고 있습니다.', font_size=24,
                font_family="Noto Sans KR",
                fill="#202124",
                align="left",
                valign="middle",
            ),
            TextBoxSlot(id = 'konva_1785110879232_paste_690676_0', prompt = '', text = '책 읽는 사람은 모두 몇 명입니까?', x = 39.392, y = 61.063, font_size = 24, fill = '#202124', width = 348.163, height = 50.785, align = 'left', line_height = 1.25), TextBoxSlot(id = 'konva_1785110879232_paste_716370_0', prompt = '', text = '명', x = 500.474, y = 150.847, font_size = 24, fill = '#202124', width = 61.799, height = 38, align = 'left', line_height = 1.25), RectSlot(id = 'konva_1785110879232_paste_740217_0', prompt = '', x = 408.307, y = 145.841, width = 78.73, height = 41.989, fill = '#ffffff', stroke = '#111827', stroke_width = 1.2, interaction = {'type': 'input', 'role': 'answer', 'value_type': 'digit', 'max_length': 1, 'include_in_submission': True, 'order': 0, 'group_id': 'final_answer', 'auto_advance': True, 'keyboard': 'number'}, input_style = {'font_size_mode': 'auto', 'font_size_adjust': 0, 'min_font_size': 14, 'max_font_size': 52, 'font_weight': 700, 'horizontal_align': 'center', 'vertical_align': 'middle', 'padding': 6, 'text_color': '#222222'})),
    )


PROBLEM_TEMPLATE = build_problem_template()


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
                "id": "place.library",
                "type": "place",
                "label": "도서관",
            },
            {
                "id": "group.adults",
                "type": "person_group",
                "label": "책을 읽고 있는 어른",
                "count": 648,
                "unit": "명",
            },
            {
                "id": "group.children",
                "type": "person_group",
                "label": "책을 읽고 있는 어린이",
                "count": 476,
                "unit": "명",
            },
            {
                "id": "group.all_readers",
                "type": "person_group",
                "label": "책을 읽고 있는 모든 사람",
                "count": 1124,
                "unit": "명",
            },
        ],
        "relations": [
            {
                "id": "relation.adults_in_library",
                "type": "located_in",
                "subject": "group.adults",
                "object": "place.library",
            },
            {
                "id": "relation.children_in_library",
                "type": "located_in",
                "subject": "group.children",
                "object": "place.library",
            },
            {
                "id": "relation.all_readers_composed_of_groups",
                "type": "sum_of",
                "subject": "group.all_readers",
                "objects": [
                    "group.adults",
                    "group.children",
                ],
            },
        ],
    },
    "answer": {
        "value": 1124,
        "unit": "명",
        "expression": "648 + 476 = 1124",
    },
}

SEMANTIC_OVERRIDE = SEMANTIC


SOLVABLE = {'schema': 'modu.solvable.v1.2',
 'problem_id': 'P3_1_01_00040_00472',
 'problem_type': 'numeric_answer_addition_word_problem',
 'inputs': {'target_label': '도서관에서 책을 읽고 있는 사람의 전체 수',
            'unit': '명',
            'answer_type': 'integer',
            'quantities': {'adult_count': 648, 'child_count': 476},
            'conditions': ['도서관에서 책을 읽고 있는 어른은 648명입니다.',
                           '도서관에서 책을 읽고 있는 어린이는 476명입니다.',
                           '어른과 어린이의 수를 모두 더합니다.']},
 'given': [{'ref': 'group.adults', 'value': {'count': 648, 'unit': '명', 'label': '어른'}},
           {'ref': 'group.children', 'value': {'count': 476, 'unit': '명', 'label': '어린이'}}],
 'target': {'ref': 'group.all_readers', 'type': 'count'},
 'method': '어른의 수와 어린이의 수를 더한다.',
 'plan': ['책을 읽고 있는 어른의 수를 확인한다.',
          '책을 읽고 있는 어린이의 수를 확인한다.',
          '두 수를 덧셈식으로 나타낸다.',
          '648과 476을 더하여 전체 사람 수를 구한다.'],
 'steps': [{'id': 'step.identify_adult_count',
            'expr': 'adult_count = 648',
            'value': 648,
            'explanation': '책을 읽고 있는 어른은 648명입니다.'},
           {'id': 'step.identify_child_count',
            'expr': 'child_count = 476',
            'value': 476,
            'explanation': '책을 읽고 있는 어린이는 476명입니다.'},
           {'id': 'step.add_reader_counts',
            'expr': '648 + 476',
            'value': 1124,
            'explanation': '어른과 어린이의 수를 더하면 1124명입니다.'}],
 'checks': [{'id': 'check.ones_place', 'expr': '8 + 6', 'expected': 14, 'actual': 14, 'pass': True},
            {'id': 'check.tens_place',
             'expr': '4 + 7 + 1',
             'expected': 12,
             'actual': 12,
             'pass': True},
            {'id': 'check.hundreds_place',
             'expr': '6 + 4 + 1',
             'expected': 11,
             'actual': 11,
             'pass': True},
            {'id': 'check.total',
             'expr': '648 + 476',
             'expected': 1124,
             'actual': 1124,
             'pass': True},
            {'id': 'check.inverse_operation',
             'expr': '1124 - 476',
             'expected': 648,
             'actual': 648,
             'pass': True}],
 'answer': {'value': 1124, 'unit': '명', 'expression': '648 + 476 = 1124'},
 'understanding': {'summary': 'Find 도서관에서 책을 읽고 있는 사람의 전체 수 using the given information.',
                   'facts': [{'ref': 'group.adults',
                              'label': 'adults',
                              'value': 648,
                              'unit': '명',
                              'source': 'explicit'},
                             {'ref': 'group.children',
                              'label': 'children',
                              'value': 476,
                              'unit': '명',
                              'source': 'explicit'}],
                   'unknowns': [{'ref': 'group.all_readers',
                                 'label': '도서관에서 책을 읽고 있는 사람의 전체 수',
                                 'unit': '명',
                                 'source': 'unknown'}],
                   'relation': {'type': '어른의 수와 어린이의 수를 더한다.',
                                'statement': '책을 읽고 있는 어른의 수를 확인한다.',
                                'symbolic': 'adult_count = 648',
                                'uses': ['group.adults', 'group.children'],
                                'result': 'group.all_readers'},
                   'diagnostic_questions': [{'id': 'understand.target',
                                             'type': 'multiple_choice',
                                             'prompt': 'What should we find?',
                                             'choices': ['adults',
                                                         'children',
                                                         '도서관에서 책을 읽고 있는 사람의 전체 수'],
                                             'answer_index': 2}]}}

SEMANTIC_ANSWER = SOLVABLE["answer"]
