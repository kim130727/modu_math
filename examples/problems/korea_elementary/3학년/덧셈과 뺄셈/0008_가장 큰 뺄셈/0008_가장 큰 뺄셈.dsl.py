from __future__ import annotations

from modu_math.dsl import Arrow, BlankSlot, Canvas, ChoiceSlot, Circle, CircleSlot, Constraint, Cube, DiagramTemplate, FractionAreaModel, Grid, Group, LabelSlot, LineSlot, PathSlot, PolygonSlot, ProblemTemplate, RectSlot, Region, ShapeObject, TextSlot, Triangle

def build_problem_template() -> ProblemTemplate:
    canvas = Canvas(
        width=767,
        height=155,
        coordinate_mode='logical',
    )
    regions = (
        Region(
            id='region.stem',
            role='stem',
            flow='vertical',
            slot_ids=('slot.i1', 'slot.n1', 'slot.n2', 'slot.n3', 'slot.n4'),
        ),
    )
    slots = (
        RectSlot(
            id='slot.bg',
            prompt='',
            x=0.0,
            y=0.0,
            width=767.0,
            height=155.0,
            stroke='none',
            stroke_width=0.0,
            fill='#FFFFFF',
        ),
        TextSlot(
            id='slot.i1',
            prompt='',
            text='다음 수 중에서 2개를 골라 가장 큰 뺄셈식을 만들려고 합니다. 식과 답을 구하시오.',
            style_role='body',
            x=6.0,
            y=34.0,
            font_size=17,
            font_family='Malgun Gothic',
            anchor='middle',
            fill='#222222',
        ),
        RectSlot(
            id='slot.num_box',
            prompt='',
            x=168.0,
            y=86.0,
            width=389.0,
            height=56.0,
            stroke='#666666',
            stroke_width=1.5,
            rx=10.0,
            ry=10.0,
            fill='none',
        ),
        RectSlot(
            id='slot.answer_expr',
            prompt='',
            x=520.0,
            y=121.0,
            width=238.0,
            height=28.0,
            stroke='none',
            stroke_width=0.0,
            fill='none',
            semantic_role='answer_anchor',
        ),
        TextSlot(
            id='slot.n1',
            prompt='',
            text='326',
            style_role='body',
            x=259.0,
            y=123.0,
            font_size=17,
            font_family='Malgun Gothic',
            anchor='middle',
            fill='#222222',
        ),
        TextSlot(
            id='slot.n2',
            prompt='',
            text='412',
            style_role='body',
            x=334.0,
            y=123.0,
            font_size=17,
            font_family='Malgun Gothic',
            anchor='middle',
            fill='#222222',
        ),
        TextSlot(
            id='slot.n3',
            prompt='',
            text='481',
            style_role='body',
            x=409.0,
            y=123.0,
            font_size=17,
            font_family='Malgun Gothic',
            anchor='middle',
            fill='#222222',
        ),
        TextSlot(
            id='slot.n4',
            prompt='',
            text='112',
            style_role='body',
            x=484.0,
            y=123.0,
            font_size=17,
            font_family='Malgun Gothic',
            anchor='middle',
            fill='#222222',
        ),
    )
    diagrams = (
    )
    groups = (
    )
    constraints = (
    )
    return ProblemTemplate(
        id='0008_가장 큰 뺄셈',
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
    'problem_id': '0008_가장 큰 뺄셈',
    'problem_type': 'arithmetic_subtraction_optimization',
    'metadata': {
        'language': 'ko',
        'question': '네 개의 수(326, 412, 481, 112) 중 두 개를 골라 차가 최대가 되는 뺄셈식을 만드는 문제',
        'instruction': '다음 수 중에서 2개를 골라 가장 큰 뺄셈식을 만들려고 합니다. 식과 답을 구하시오.',
    },
    'domain': {
        'objects': [
            {'id': 'obj.nums', 'type': 'list', 'value': [326, 412, 481, 112]},
        ],
        'problem_solving': {
            'plan': {
                'method': 'extremes_difference',
                'description': '가장 큰 수에서 가장 작은 수를 뺀다.',
            }
        },
    },
    'answer': {
        'value': 369,
        'unit': '',
    },
}

SOLVABLE = {
    'schema': 'modu.solvable.v1',
    'problem_id': '0008_가장 큰 뺄셈',
    'problem_type': 'arithmetic_subtraction_optimization',
    'given': [
        {'ref': 'obj.nums', 'value': [326, 412, 481, 112]}
    ],
    'target': {'type': 'number', 'description': '최대 차'},
    'method': 'extremes_difference',
    'steps': [
        {
            'id': 'step.s1',
            'operation': 'selection',
            'expr': 'max=481, min=112',
            'value': [481, 112]
        },
        {
            'id': 'step.s2',
            'operation': 'subtraction',
            'expr': '481 - 112 = 369',
            'value': 369
        }
    ],
    'checks': [
        {
            'id': 'check.c1',
            'type': 'arithmetic_consistency_check',
            'pass': True,
            'expected': 369,
            'actual': 369,
            'expr': '481 - 112'
        }
    ],
    'answer': {'value': 369, 'unit': '', 'derived_from': 'step.s2'},
    'inputs': {
        'total_ticks': 1,
        'target_label': '답',
        'target_ticks': 1,
        'target_count': 1,
        'unit': ''
    },
    'plan': ['가장 큰 481에서 가장 작은 112를 빼서 최대 차인 369를 구합니다.']
}
