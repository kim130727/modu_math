from __future__ import annotations

from modu_math.dsl import Arrow, BlankSlot, Canvas, ChoiceSlot, Circle, CircleSlot, Constraint, Cube, DiagramTemplate, FractionAreaModel, Grid, Group, LabelSlot, LineSlot, PathSlot, PolygonSlot, ProblemTemplate, RectSlot, Region, ShapeObject, TextSlot, Triangle

def build_problem_template() -> ProblemTemplate:
    canvas = Canvas(
        width=1000,
        height=500,
        coordinate_mode='logical',
    )
    regions = (
        Region(
            id='region.stem',
            role='stem',
            flow='vertical',
            slot_ids=('slot.t1', 'slot.eq1', 'slot.eq2'),
        ),
    )
    slots = (
        TextSlot(
            id='slot.t1',
            prompt='',
            text='같은 모양은 같은 수를 나타냅니다. ■와 ▲에 알맞은 수의 차를 구하시오.',
            style_role='body',
            x=50.0,
            y=80.0,
            font_size=24,
            font_family='sans-serif',
            anchor='start',
            fill='#000000',
        ),
        TextSlot(
            id='slot.eq1',
            prompt='',
            text='800 - 347 + ■ = 650',
            style_role='body',
            x=80.0,
            y=200.0,
            font_size=28,
            font_family='serif',
            anchor='start',
            fill='#000000',
        ),
        TextSlot(
            id='slot.eq2',
            prompt='',
            text='543 - ▲ = ■',
            style_role='body',
            x=80.0,
            y=300.0,
            font_size=28,
            font_family='serif',
            anchor='start',
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
        id='0002_모양에 알맞은 수 구하기',
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
    'problem_id': '0002_모양에 알맞은 수 구하기',
    'problem_type': 'arithmetic_shape_puzzle',
    'metadata': {
        'language': 'ko',
        'question': '기호 ■와 ▲가 포함된 두 식을 해결하여 두 수의 차를 구하는 문제',
        'instruction': '■와 ▲에 알맞은 수의 차를 구하시오.',
    },
    'domain': {
        'objects': [
            {'id': 'obj.eq1', 'type': 'equation', 'value': '800 - 347 + ■ = 650'},
            {'id': 'obj.eq2', 'type': 'equation', 'value': '543 - ▲ = ■'},
        ],
        'problem_solving': {
            'plan': {
                'method': 'sequential_equation_solving',
                'description': '첫 번째 식에서 ■를 구하고, 그 값을 두 번째 식에 대입하여 ▲를 구한 뒤 두 수의 차를 계산한다.',
            }
        },
    },
    'answer': {
        'value': 149,
        'unit': '',
    },
}

SOLVABLE = {
    'schema': 'modu.solvable.v1',
    'problem_id': '0002_모양에 알맞은 수 구하기',
    'problem_type': 'arithmetic_shape_puzzle',
    'given': [
        {'ref': 'obj.eq1', 'value': '800 - 347 + ■ = 650'},
        {'ref': 'obj.eq2', 'value': '543 - ▲ = ■'}
    ],
    'target': {'type': 'number', 'description': '■와 ▲의 차'},
    'method': 'sequential_equation_solving',
    'steps': [
        {
            'id': 'step.s1',
            'operation': 'subtraction',
            'expr': '800 - 347 = 453',
            'value': 453
        },
        {
            'id': 'step.s2',
            'operation': 'subtraction',
            'expr': '650 - 453 = 197',
            'description': '■의 값은 197입니다.',
            'value': 197
        },
        {
            'id': 'step.s3',
            'operation': 'subtraction',
            'expr': '543 - 197 = 346',
            'description': '▲의 값은 346입니다.',
            'value': 346
        },
        {
            'id': 'step.s4',
            'operation': 'subtraction',
            'expr': '346 - 197 = 149',
            'description': '두 수의 차를 구합니다.',
            'value': 149
        }
    ],
    'checks': [
        {
            'id': 'check.c1',
            'type': 'arithmetic_consistency_check',
            'pass': True,
            'expected': 149,
            'actual': 149,
            'expr': '346 - 197'
        }
    ],
    'answer': {'value': 149, 'unit': '', 'derived_from': 'step.s4'},
    'inputs': {
        'total_ticks': 1,
        'target_label': '답',
        'target_ticks': 1,
        'target_count': 1,
        'unit': ''
    },
    'plan': ['첫 번째 식에서 ■=197을 구하고, 두 번째 식에서 ▲=346을 구한 뒤 차이인 149를 계산합니다.']
}
