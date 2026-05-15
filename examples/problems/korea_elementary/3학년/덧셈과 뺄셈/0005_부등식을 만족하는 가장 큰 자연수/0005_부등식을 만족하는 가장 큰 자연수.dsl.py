from __future__ import annotations

from modu_math.dsl import Arrow, BlankSlot, Canvas, ChoiceSlot, Circle, CircleSlot, Constraint, Cube, DiagramTemplate, FractionAreaModel, Grid, Group, LabelSlot, LineSlot, PolygonSlot, ProblemTemplate, RectSlot, Region, ShapeObject, TextSlot, Triangle

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
            slot_ids=('slot.t1', 'slot.f1'),
        ),
    )
    slots = (
        TextSlot(
            id='slot.t1',
            prompt='',
            text='□ 안에 들어갈 수 있는 수 중에서 가장 큰 자연수를 구하시오.',
            style_role='body',
        ),
        TextSlot(
            id='slot.f1',
            prompt='',
            text='179 + 265 < 933 - □',
            style_role='body',
        ),
    )
    diagrams = (
    )
    groups = (
    )
    constraints = (
    )
    return ProblemTemplate(
        id='0005_부등식을 만족하는 가장 큰 자연수',
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
    'problem_id': '0005_부등식을 만족하는 가장 큰 자연수',
    'problem_type': 'arithmetic_inequality_optimization',
    'metadata': {
        'language': 'ko',
        'question': '부등식 179 + 265 < 933 - □를 만족하는 가장 큰 자연수를 구하는 문제',
        'instruction': '□ 안에 들어갈 수 있는 수 중에서 가장 큰 자연수를 구하시오.',
    },
    'domain': {
        'objects': [
            {'id': 'obj.inequality', 'type': 'inequality', 'value': '179 + 265 < 933 - □'},
        ],
        'problem_solving': {
            'plan': {
                'method': 'algebraic_isolation',
                'description': '좌변을 계산하여 부등식을 단순화한 뒤, □의 범위를 구하고 그 중 가장 큰 자연수를 찾는다.',
            }
        },
    },
    'answer': {
        'value': 488,
        'unit': '',
    },
}

SOLVABLE = {
    'schema': 'modu.solvable.v1',
    'problem_id': '0005_부등식을 만족하는 가장 큰 자연수',
    'problem_type': 'arithmetic_inequality_optimization',
    'given': [
        {'ref': 'obj.inequality', 'value': '179 + 265 < 933 - □'}
    ],
    'target': {'type': 'number', 'description': '가장 큰 자연수 □'},
    'method': 'algebraic_isolation',
    'steps': [
        {
            'id': 'step.s1',
            'operation': 'addition',
            'expr': '179 + 265 = 444',
            'value': 444
        },
        {
            'id': 'step.s2',
            'operation': 'subtraction',
            'expr': '933 - 444 = 489',
            'description': '444 < 933 - □ 이므로 □ < 489 입니다.',
            'value': 489
        },
        {
            'id': 'step.s3',
            'operation': 'subtraction',
            'expr': '489 - 1 = 488',
            'description': '489보다 작은 자연수 중 가장 큰 수는 488입니다.',
            'value': 488
        }
    ],
    'checks': [
        {
            'id': 'check.c1',
            'type': 'arithmetic_consistency_check',
            'pass': True,
            'expected': True,
            'actual': True,
            'expr': '179 + 265 < 933 - 488'
        }
    ],
    'answer': {'value': 488, 'unit': '', 'derived_from': 'step.s3'},
    'inputs': {
        'total_ticks': 1,
        'target_label': '답',
        'target_ticks': 1,
        'target_count': 1,
        'unit': ''
    },
    'plan': ['부등식을 정리하여 □ < 489임을 구한 뒤, 조건에 맞는 최대 자연수 488을 찾습니다.']
}
