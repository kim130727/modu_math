from __future__ import annotations

from modu_math.dsl import (
    Canvas,
    ProblemTemplate,
    Region,
    TextBoxSlot,
)


PROBLEM_ID = "P3_1_01_00040_00472"
PROBLEM_TITLE = "도서관에서 책을 읽고 있는 사람 수"


def build_problem_template() -> ProblemTemplate:
    return ProblemTemplate(
        id=PROBLEM_ID,
        title=PROBLEM_TITLE,
        canvas=Canvas(
            width=900,
            height=220,
            coordinate_mode="logical",
        ),
        regions=(
            Region(
                id="region.stem",
                role="stem",
                flow="absolute",
                slot_ids=(
                    "slot.question",
                    "slot.expression_label",
                    "slot.expression_blank",
                    "slot.answer_label",
                    "slot.answer_blank",
                ),
            ),
        ),
        slots=(
            TextBoxSlot(
                id="slot.question",
                x=38,
                y=22,
                width=824,
                height=58,
                text=(
                    "도서관에서 어른 648명, 어린이 476명이 책을 읽고 있습니다. "
                    "책 읽는 사람은 모두 몇 명입니까?"
                ),
                font_size=24,
                font_family="Noto Sans KR",
                fill="#202124",
                align="left",
                valign="middle",
            ),
            TextBoxSlot(
                id="slot.expression_label",
                x=38,
                y=88,
                width=42,
                height=38,
                text="식",
                font_size=24,
                font_family="Noto Sans KR",
                fill="#202124",
                align="left",
                valign="middle",
            ),
            TextBoxSlot(
                id="slot.expression_blank",
                x=82,
                y=88,
                width=170,
                height=38,
                text="____________",
                font_size=24,
                font_family="Noto Sans KR",
                fill="#202124",
                align="left",
                valign="middle",
            ),
            TextBoxSlot(
                id="slot.answer_label",
                x=38,
                y=134,
                width=42,
                height=38,
                text="답",
                font_size=24,
                font_family="Noto Sans KR",
                fill="#202124",
                align="left",
                valign="middle",
            ),
            TextBoxSlot(
                id="slot.answer_blank",
                x=82,
                y=134,
                width=130,
                height=38,
                text="_________",
                font_size=24,
                font_family="Noto Sans KR",
                fill="#202124",
                align="left",
                valign="middle",
            ),
        ),
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
