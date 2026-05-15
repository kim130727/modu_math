from __future__ import annotations

from modu_math.dsl import Arrow, BlankSlot, Canvas, ChoiceSlot, Circle, CircleSlot, Constraint, Cube, DiagramTemplate, FractionAreaModel, Grid, Group, LabelSlot, LineSlot, PathSlot, PolygonSlot, ProblemTemplate, RectSlot, Region, ShapeObject, TextSlot, Triangle

def build_problem_template() -> ProblemTemplate:
    canvas = Canvas(
        width=768,
        height=341,
        coordinate_mode='logical',
    )
    regions = (
        Region(
            id='region.stem',
            role='stem',
            # flow='vertical' removed to allow absolute positioning of TextSlots
            slot_ids=('slot.line1_prefix.text',
             'slot.expr_mul.text',
             'slot.line2.text',
             'slot.num_4.text',
             'slot.num_9.text',
             'slot.num_2.text',
             'slot.answer_left_paren.text',
             'slot.answer_right_paren.text'),
        ),
    )
    slots = (
        RectSlot(
            id='slot.expr_box_1.rect',
            prompt='',
            x=458.19281005859375,
            y=22.95867919921875,
            width=33.0,
            height=31.0,
            stroke='#1f1f1f',
            stroke_width=1.0,
            fill='none',
        ),
        RectSlot(
            id='slot.expr_box_2.rect',
            prompt='',
            x=525.1928100585938,
            y=22.95867919921875,
            width=33.0,
            height=31.0,
            stroke='#1f1f1f',
            stroke_width=1.0,
            fill='none',
        ),
        RectSlot(
            id='slot.expr_box_3.rect',
            prompt='',
            x=566.1928100585938,
            y=22.95867919921875,
            width=33.0,
            height=31.0,
            stroke='#1f1f1f',
            stroke_width=1.0,
            fill='none',
        ),
        TextSlot(
            id='slot.line1_prefix.text',
            prompt='',
            text='3장의 수 카드를 모두 한 번씩만 사용하여',
            style_role='body',
            x=18.0,
            y=46.0,
            font_size=22,
            font_family='Malgun Gothic',
            anchor='start',
            fill='#000000',
        ),
        TextSlot(
            id='slot.expr_mul.text',
            prompt='',
            text='×',
            style_role='body',
            x=509.1101989746094,
            y=50.95867919921875,
            font_size=45,
            font_family='Malgun Gothic',
            anchor='middle',
            fill='#000000',
        ),
        TextSlot(
            id='slot.line2.text',
            prompt='',
            text='을 만들려고 합니다. 곱이 가장 큰 곱셈식을 만들어 곱을 구하시오',
            style_role='body',
            x=18.0,
            y=102.0,
            font_size=22,
            font_family='Malgun Gothic',
            anchor='start',
            fill='#000000',
        ),
        RectSlot(
            id='slot.card_9.rect',
            prompt='',
            x=182.0,
            y=172.0,
            width=73.0,
            height=85.0,
            stroke='#1f1f1f',
            stroke_width=1.0,
            fill='#b4b4b4',
        ),
        RectSlot(
            id='slot.card_2.rect',
            prompt='',
            x=327.0,
            y=172.0,
            width=73.0,
            height=85.0,
            stroke='#1f1f1f',
            stroke_width=1.0,
            fill='#b4b4b4',
        ),
        RectSlot(
            id='slot.card_4.rect',
            prompt='',
            x=472.0,
            y=172.0,
            width=73.0,
            height=85.0,
            stroke='#1f1f1f',
            stroke_width=1.0,
            fill='#b4b4b4',
        ),
        TextSlot(
            id='slot.num_4.text',
            prompt='',
            text='4',
            style_role='body',
            x=505.9311218261719,
            y=229.0068817138672,
            font_size=53,
            font_family='Malgun Gothic',
            anchor='middle',
            fill='#000000',
        ),
        TextSlot(
            id='slot.num_9.text',
            prompt='',
            text='9',
            style_role='body',
            x=214.93801879882812,
            y=232.97933959960938,
            font_size=53,
            font_family='Malgun Gothic',
            anchor='middle',
            fill='#000000',
        ),
        TextSlot(
            id='slot.num_2.text',
            prompt='',
            text='2',
            style_role='body',
            x=360.93115234375,
            y=232.97933959960938,
            font_size=53,
            font_family='Malgun Gothic',
            anchor='middle',
            fill='#000000',
        ),
        RectSlot(
            id='slot.answer_blank.rect',
            prompt='',
            x=430.0,
            y=272.0,
            width=235.0,
            height=44.0,
            stroke='none',
            stroke_width=1.0,
            fill='none',
        ),
        TextSlot(
            id='slot.answer_left_paren.text',
            prompt='',
            text='(',
            style_role='body',
            x=396.0,
            y=304.0,
            font_size=40,
            font_family='Malgun Gothic',
            anchor='middle',
            fill='#000000',
        ),
        TextSlot(
            id='slot.answer_right_paren.text',
            prompt='',
            text=')',
            style_role='body',
            x=697.0,
            y=304.0,
            font_size=40,
            font_family='Malgun Gothic',
            anchor='middle',
            fill='#000000',
        ),
    )
    diagrams = (
    )
    groups = (
    )
    constraints = (
    )
    return ProblemTemplate(
        id='0016_카드 곱셈',
        title='',
        canvas=canvas,
        regions=regions,
        slots=slots,
        diagrams=diagrams,
        groups=groups,
        constraints=constraints,
    )

PROBLEM_TEMPLATE = build_problem_template()

SEMANTIC_OVERRIDE = {
    'problem_id': '0016_카드 곱셈',
    'problem_type': 'arithmetic_multiplication_maximization',
    'metadata': {
        'language': 'ko',
        'question': '3장의 수 카드(4, 9, 2)를 모두 한 번씩만 사용하여 곱이 가장 큰 (1자리 수) × (2자리 수)를 만들고 그 곱을 구하는 문제',
        'instruction': '곱이 가장 큰 곱셈식을 만들어 곱을 구하시오',
    },
    'domain': {
        'objects': [
            {'id': 'obj.cards', 'type': 'digit_cards', 'value': [4, 9, 2]},
            {'id': 'obj.template', 'type': 'expression_template', 'value': '[ ] × [ ][ ]'},
        ],
        'problem_solving': {
            'plan': {
                'method': 'maximization_strategy',
                'description': '가장 큰 숫자를 한 자리 수에 배치하고 그 다음 큰 숫자를 십의 자리에 배치한다.',
            }
        },
    },
    'answer': {
        'value': 378,
        'unit': '',
    },
}

SOLVABLE = {
    'schema': 'modu.solvable.v1',
    'problem_id': '0016_카드 곱셈',
    'problem_type': 'arithmetic_multiplication_maximization',
    'given': [
        {'ref': 'obj.cards', 'value': [4, 9, 2]},
        {'ref': 'obj.template', 'value': '[ ] × [ ][ ]'}
    ],
    'target': {'type': 'number', 'description': '최대 곱'},
    'method': 'maximization_strategy',
    'steps': [
        {
            'id': 'step.s1',
            'operation': 'multiplication',
            'expr': '9 * 42 = 378',
            'value': 378
        }
    ],
    'checks': [
        {
            'id': 'check.c1',
            'type': 'arithmetic_consistency_check',
            'pass': True,
            'expected': 378,
            'actual': 378,
            'expr': '9 * 42'
        }
    ],
    'answer': {'value': 378, 'unit': '', 'derived_from': 'step.s1'},
    'inputs': {
        'total_ticks': 1,
        'target_label': '답',
        'target_ticks': 1,
        'target_count': 1,
        'unit': ''
    },
    'plan': ['가장 큰 수인 9를 한 자리 수 자리에 놓고 42와 곱하여 378을 얻습니다.']
}
