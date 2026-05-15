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
                'slot.card_0',
                'slot.card_1',
                'slot.card_2',
                'slot.card_3',
                'slot.n0',
                'slot.n1',
                'slot.n2',
                'slot.n3',
                'slot.box1',
                'slot.op1',
                'slot.box2',
                'slot.op2',
                'slot.box3',
                'slot.eq',
                'slot.box_res',
            ),
        ),
    )
    slots = (
        TextSlot(
            id='slot.t1',
            prompt='',
            text='주어진 수 중에서 세 수를 골라 다음과 같은 식을 만들려고 합니다.',
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
            text='계산 결과가 가장 크게 되도록 □ 안에 알맞은 수를 써넣고, 계산한 값을 구하시오.',
            style_role='body',
            x=64.0,
            y=116.0,
            font_size=26,
            font_family='Noto Sans KR, sans-serif',
            fill='#111111',
            anchor='start',
        ),
        RectSlot(
            id='slot.card_0',
            prompt='',
            x=140.0,
            y=220.0,
            width=120.0,
            height=90.0,
            fill='#EAF4FF',
            stroke='#8FB3D9',
            stroke_width=2.0,
            rx=12.0,
            semantic_role='card',
        ),
        RectSlot(
            id='slot.card_1',
            prompt='',
            x=300.0,
            y=220.0,
            width=120.0,
            height=90.0,
            fill='#EAF4FF',
            stroke='#8FB3D9',
            stroke_width=2.0,
            rx=12.0,
            semantic_role='card',
        ),
        RectSlot(
            id='slot.card_2',
            prompt='',
            x=460.0,
            y=220.0,
            width=120.0,
            height=90.0,
            fill='#EAF4FF',
            stroke='#8FB3D9',
            stroke_width=2.0,
            rx=12.0,
            semantic_role='card',
        ),
        RectSlot(
            id='slot.card_3',
            prompt='',
            x=620.0,
            y=220.0,
            width=120.0,
            height=90.0,
            fill='#EAF4FF',
            stroke='#8FB3D9',
            stroke_width=2.0,
            rx=12.0,
            semantic_role='card',
        ),
        TextSlot(
            id='slot.n0',
            prompt='',
            text='365',
            style_role='body',
            x=200.0,
            y=280.0,
            font_size=38,
            font_family='Cambria',
            fill='#1F1F1F',
            anchor='middle',
        ),
        TextSlot(
            id='slot.n1',
            prompt='',
            text='567',
            style_role='body',
            x=360.0,
            y=280.0,
            font_size=38,
            font_family='Cambria',
            fill='#1F1F1F',
            anchor='middle',
        ),
        TextSlot(
            id='slot.n2',
            prompt='',
            text='827',
            style_role='body',
            x=520.0,
            y=280.0,
            font_size=38,
            font_family='Cambria',
            fill='#1F1F1F',
            anchor='middle',
        ),
        TextSlot(
            id='slot.n3',
            prompt='',
            text='910',
            style_role='body',
            x=680.0,
            y=280.0,
            font_size=38,
            font_family='Cambria',
            fill='#1F1F1F',
            anchor='middle',
        ),
        RectSlot(
            id='slot.box1',
            prompt='',
            x=210.0,
            y=390.0,
            width=120.0,
            height=70.0,
            fill='none',
            stroke='#666666',
            stroke_width=2.0,
            rx=10.0,
            semantic_role='blank',
        ),
        TextSlot(
            id='slot.op1',
            prompt='',
            text='-',
            style_role='body',
            x=360.0,
            y=438.0,
            font_size=50,
            font_family='Cambria',
            fill='#111111',
            anchor='middle',
        ),
        RectSlot(
            id='slot.box2',
            prompt='',
            x=390.0,
            y=390.0,
            width=120.0,
            height=70.0,
            fill='none',
            stroke='#666666',
            stroke_width=2.0,
            rx=10.0,
            semantic_role='blank',
        ),
        TextSlot(
            id='slot.op2',
            prompt='',
            text='+',
            style_role='body',
            x=540.0,
            y=438.0,
            font_size=50,
            font_family='Cambria',
            fill='#111111',
            anchor='middle',
        ),
        RectSlot(
            id='slot.box3',
            prompt='',
            x=570.0,
            y=390.0,
            width=120.0,
            height=70.0,
            fill='none',
            stroke='#666666',
            stroke_width=2.0,
            rx=10.0,
            semantic_role='blank',
        ),
        TextSlot(
            id='slot.eq',
            prompt='',
            text='=',
            style_role='body',
            x=730.0,
            y=438.0,
            font_size=50,
            font_family='Cambria',
            fill='#111111',
            anchor='middle',
        ),
        RectSlot(
            id='slot.box_res',
            prompt='',
            x=760.0,
            y=390.0,
            width=140.0,
            height=70.0,
            fill='none',
            stroke='#69BEEA',
            stroke_width=3.0,
            rx=10.0,
            semantic_role='answer_anchor',
        ),
    )
    diagrams = (
    )
    groups = (
    )
    constraints = (
    )
    return ProblemTemplate(
        id='0007_계산 결과가 가장 큰 식 만들기',
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
    'problem_id': '0007_계산 결과가 가장 큰 식 만들기',
    'problem_type': 'arithmetic_expression_optimization',
    'metadata': {
        'language': 'ko',
        'question': '네 개의 수(365, 567, 827, 910) 중 세 개를 골라 [A - B + C] 꼴의 식을 만들 때, 결과가 최대가 되는 값을 구하는 문제',
        'instruction': '계산 결과가 가장 크게 되도록 □ 안에 알맞은 수를 써넣고, 계산한 값을 구하시오.',
    },
    'domain': {
        'objects': [
            {'id': 'obj.nums', 'type': 'list', 'value': [365, 567, 827, 910]},
        ],
        'problem_solving': {
            'plan': {
                'method': 'optimization_strategy',
                'description': '결과를 최대화하기 위해 가장 큰 두 수를 더하고 가장 작은 수를 뺀다.',
            }
        },
    },
    'answer': {
        'value': 1372,
        'unit': '',
    },
}

SOLVABLE = {
    'schema': 'modu.solvable.v1',
    'problem_id': '0007_계산 결과가 가장 큰 식 만들기',
    'problem_type': 'arithmetic_expression_optimization',
    'given': [
        {'ref': 'obj.nums', 'value': [365, 567, 827, 910]}
    ],
    'target': {'type': 'number', 'description': '최대 계산 결과'},
    'method': 'optimization_strategy',
    'steps': [
        {
            'id': 'step.s1',
            'operation': 'selection',
            'expr': 'A=910, B=365, C=827',
            'description': '가장 큰 910과 827을 더하고, 가장 작은 365를 뺍니다.',
            'value': [910, 365, 827]
        },
        {
            'id': 'step.s2',
            'operation': 'calculation',
            'expr': '910 - 365 + 827 = 1372',
            'value': 1372
        }
    ],
    'checks': [
        {
            'id': 'check.c1',
            'type': 'arithmetic_consistency_check',
            'pass': True,
            'expected': 1372,
            'actual': 1372,
            'expr': '910 - 365 + 827'
        }
    ],
    'answer': {'value': 1372, 'unit': '', 'derived_from': 'step.s2'},
    'inputs': {
        'total_ticks': 4,
        'target_label': '답',
        'target_ticks': 4,
        'target_count': 4,
        'unit': ''
    },
    'plan': ['가장 큰 두 수(910, 827)를 양의 항에, 가장 작은 수(365)를 음의 항에 배치하여 1372를 구합니다.']
}
