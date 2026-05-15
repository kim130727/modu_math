from __future__ import annotations

from modu_math.dsl import Arrow, BlankSlot, Canvas, ChoiceSlot, Circle, CircleSlot, Constraint, Cube, DiagramTemplate, FractionAreaModel, Grid, Group, LabelSlot, LineSlot, PolygonSlot, ProblemTemplate, RectSlot, Region, ShapeObject, TextSlot, Triangle


def build_problem_template() -> ProblemTemplate:
    canvas = Canvas(
        width=1000,
        height=600,
        coordinate_mode='logical',
    )
    regions = (
        Region(
            id='region.stem',
            role='stem',
            flow='vertical',
            slot_ids=(
                'slot.t1',
                'slot.t2',
                'slot.t3',
                'slot.card_0',
                'slot.card_1',
                'slot.card_2',
                'slot.card_3',
                'slot.card_4',
                'slot.card_text_0',
                'slot.card_text_1',
                'slot.card_text_2',
                'slot.card_text_3',
                'slot.card_text_4',
            ),
        ),
    )
    slots = (
        TextSlot(
            id='slot.t1',
            prompt='',
            text='5장의 수 카드 중에서 3장을 골라 한 번씩만 사용하여 세 자리 수를 만들었습니다.',
            style_role='body',
            x=64.0,
            y=72.0,
            font_size=26,
            font_family='Noto Sans KR, sans-serif',
            fill='#111111',
            anchor='start',
        ),
        TextSlot(
            id='slot.t2',
            prompt='',
            text='세 자리 수 중에서 십의 자리 숫자가 8인 두 번째로 큰 수와 일의 자리 숫자가',
            style_role='body',
            x=64.0,
            y=128.0,
            font_size=26,
            font_family='Noto Sans KR, sans-serif',
            fill='#111111',
            anchor='start',
        ),
        TextSlot(
            id='slot.t3',
            prompt='',
            text='8인 두 번째로 작은 수의 차는 얼마입니까?',
            style_role='body',
            x=64.0,
            y=184.0,
            font_size=26,
            font_family='Noto Sans KR, sans-serif',
            fill='#111111',
            anchor='start',
        ),
        RectSlot(
            id='slot.card_0',
            prompt='',
            x=100.0,
            y=250.0,
            width=120.0,
            height=160.0,
            fill='#FFF6D8',
            stroke='#C7B173',
            stroke_width=2.0,
            rx=12.0,
            semantic_role='card',
        ),
        RectSlot(
            id='slot.card_1',
            prompt='',
            x=260.0,
            y=250.0,
            width=120.0,
            height=160.0,
            fill='#FFF6D8',
            stroke='#C7B173',
            stroke_width=2.0,
            rx=12.0,
            semantic_role='card',
        ),
        RectSlot(
            id='slot.card_2',
            prompt='',
            x=420.0,
            y=250.0,
            width=120.0,
            height=160.0,
            fill='#FFF6D8',
            stroke='#C7B173',
            stroke_width=2.0,
            rx=12.0,
            semantic_role='card',
        ),
        RectSlot(
            id='slot.card_3',
            prompt='',
            x=580.0,
            y=250.0,
            width=120.0,
            height=160.0,
            fill='#FFF6D8',
            stroke='#C7B173',
            stroke_width=2.0,
            rx=12.0,
            semantic_role='card',
        ),
        RectSlot(
            id='slot.card_4',
            prompt='',
            x=740.0,
            y=250.0,
            width=120.0,
            height=160.0,
            fill='#FFF6D8',
            stroke='#C7B173',
            stroke_width=2.0,
            rx=12.0,
            semantic_role='card',
        ),
        TextSlot(
            id='slot.card_text_0',
            prompt='',
            text='2',
            style_role='body',
            x=160.0,
            y=350.0,
            font_size=68,
            font_family='Cambria',
            fill='#1F1F1F',
            anchor='middle',
        ),
        TextSlot(
            id='slot.card_text_1',
            prompt='',
            text='0',
            style_role='body',
            x=320.0,
            y=350.0,
            font_size=68,
            font_family='Cambria',
            fill='#1F1F1F',
            anchor='middle',
        ),
        TextSlot(
            id='slot.card_text_2',
            prompt='',
            text='4',
            style_role='body',
            x=480.0,
            y=350.0,
            font_size=68,
            font_family='Cambria',
            fill='#1F1F1F',
            anchor='middle',
        ),
        TextSlot(
            id='slot.card_text_3',
            prompt='',
            text='6',
            style_role='body',
            x=640.0,
            y=350.0,
            font_size=68,
            font_family='Cambria',
            fill='#1F1F1F',
            anchor='middle',
        ),
        TextSlot(
            id='slot.card_text_4',
            prompt='',
            text='8',
            style_role='body',
            x=800.0,
            y=350.0,
            font_size=68,
            font_family='Cambria',
            fill='#1F1F1F',
            anchor='middle',
        ),
    )
    diagrams = (
    )
    groups = (
    )
    constraints = (
    )
    return ProblemTemplate(
        id='0006_수 카드로 만든 수의 차',
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
    'problem_id': '0006_수 카드로 만든 수의 차',
    'problem_type': 'arithmetic_number_combination_optimization',
    'metadata': {
        'language': 'ko',
        'question': '수 카드(2, 0, 4, 6, 8)로 조건(십의 자리 8, 일의 자리 8)을 만족하는 특정 수들의 차를 구하는 문제',
        'instruction': '세 자리 수 중에서 십의 자리 숫자가 8인 두 번째로 큰 수와 일의 자리 숫자가 8인 두 번째로 작은 수의 차는 얼마입니까?',
    },
    'domain': {
        'objects': [
            {'id': 'obj.cards', 'type': 'list', 'value': [2, 0, 4, 6, 8]},
        ],
        'problem_solving': {
            'plan': {
                'method': 'conditional_enumeration',
                'description': '각 조건을 만족하는 수들을 나열하여 해당되는 두 수(682, 248)를 찾고 차를 구한다.',
            }
        },
    },
    'answer': {
        'value': 434,
        'unit': '',
    },
}

SOLVABLE = {
    'schema': 'modu.solvable.v1',
    'problem_id': '0006_수 카드로 만든 수의 차',
    'problem_type': 'arithmetic_number_combination_optimization',
    'given': [
        {'ref': 'obj.cards', 'value': [2, 0, 4, 6, 8]}
    ],
    'target': {'type': 'number', 'description': '두 수의 차'},
    'method': 'conditional_enumeration',
    'steps': [
        {
            'id': 'step.s1',
            'operation': 'deduction',
            'expr': '십의 자리 8인 수: 684, 682, 486, ...',
            'description': '십의 자리가 8인 두 번째로 큰 수는 682입니다.',
            'value': 682
        },
        {
            'id': 'step.s2',
            'operation': 'deduction',
            'expr': '일의 자리 8인 수: 208, 248, 268, ...',
            'description': '일의 자리가 8인 두 번째로 작은 수는 248입니다.',
            'value': 248
        },
        {
            'id': 'step.s3',
            'operation': 'subtraction',
            'expr': '682 - 248 = 434',
            'value': 434
        }
    ],
    'checks': [
        {
            'id': 'check.c1',
            'type': 'arithmetic_consistency_check',
            'pass': True,
            'expected': 434,
            'actual': 434,
            'expr': '682 - 248'
        }
    ],
    'answer': {'value': 434, 'unit': '', 'derived_from': 'step.s3'},
    'inputs': {
        'total_ticks': 1,
        'target_label': '답',
        'target_ticks': 1,
        'target_count': 1,
        'unit': ''
    },
    'plan': ['십의 자리가 8인 수 중 682를 찾고, 일의 자리가 8인 수 중 248을 찾아 차이인 434를 구합니다.']
}
