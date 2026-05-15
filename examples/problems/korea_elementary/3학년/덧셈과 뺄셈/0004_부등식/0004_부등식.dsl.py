from __future__ import annotations

from modu_math.dsl import Arrow, BlankSlot, Canvas, ChoiceSlot, Circle, CircleSlot, Constraint, Cube, DiagramTemplate, FractionAreaModel, Grid, Group, LabelSlot, LineSlot, PathSlot, PolygonSlot, ProblemTemplate, RectSlot, Region, ShapeObject, TextSlot, Triangle

def build_problem_template() -> ProblemTemplate:
    canvas = Canvas(
        width=406,
        height=181,
        coordinate_mode='logical',
    )
    regions = (
        Region(
            id='region.stem',
            role='stem',
            flow='vertical',
            slot_ids=('slot.i1', 'slot.i2', 'slot.eq', 'slot.gaesu', 'slot.lp', 'slot.rp'),
        ),
    )
    slots = (
        TextSlot(
            id='slot.i1',
            prompt='',
            text='0부터 9까지의 수 중에서 □에 들어갈 수를',
            style_role='body',
            x=12.0,
            y=30.0,
            font_size=17,
            font_family='Malgun Gothic',
            anchor='start',
            fill='#222222',
        ),
        TextSlot(
            id='slot.i2',
            prompt='',
            text='모두 구하고 개수를 쓰시오.',
            style_role='body',
            x=12.0,
            y=60.0,
            font_size=17,
            font_family='Malgun Gothic',
            anchor='start',
            fill='#222222',
        ),
        RectSlot(
            id='slot.eq_box',
            prompt='',
            x=2.0,
            y=78.0,
            width=402.0,
            height=56.0,
            stroke='#666666',
            stroke_width=1.5,
            rx=10.0,
            ry=10.0,
            fill='none',
        ),
        TextSlot(
            id='slot.eq',
            prompt='',
            text='4□5+298>763',
            style_role='body',
            x=201.0,
            y=112.0,
            font_size=17,
            font_family='Malgun Gothic',
            anchor='middle',
            fill='#222222',
        ),
        RectSlot(
            id='slot.answer_count',
            prompt='',
            x=246.0,
            y=146.0,
            width=110.0,
            height=28.0,
            stroke='none',
            stroke_width=0.0,
            fill='none',
            semantic_role='answer_anchor',
        ),
        TextSlot(
            id='slot.gaesu',
            prompt='',
            text='개',
            style_role='body',
            x=378.0,
            y=166.0,
            font_size=17,
            font_family='Malgun Gothic',
            anchor='middle',
            fill='#222222',
        ),
        TextSlot(
            id='slot.lp',
            prompt='',
            text='(',
            style_role='body',
            x=230.0,
            y=168.0,
            font_size=24,
            font_family='Malgun Gothic',
            anchor='middle',
            fill='#222222',
        ),
        TextSlot(
            id='slot.rp',
            prompt='',
            text=')',
            style_role='body',
            x=364.0,
            y=168.0,
            font_size=24,
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
        id='0004_부등식',
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
    'problem_id': '0004_부등식',
    'problem_type': 'arithmetic_inequality_puzzle',
    'metadata': {
        'language': 'ko',
        'question': '부등식 4□5 + 298 > 763을 만족하는 □ 안의 숫자(0-9)를 모두 찾고 개수를 구하는 문제',
        'instruction': '□ 안에 알맞은 수를 모두 구하고 개수를 쓰시오.',
    },
    'domain': {
        'objects': [
            {'id': 'obj.inequality', 'type': 'inequality', 'value': '4□5 + 298 > 763'},
        ],
        'problem_solving': {
            'plan': {
                'method': 'algebraic_simplification_and_trial',
                'description': '부등식을 단순화하여 4□5 > 465를 도출한 뒤, □에 들어갈 수 있는 숫자를 판별한다.',
            }
        },
    },
    'answer': {
        'value': {'numbers': [7, 8, 9], 'count': 3},
        'unit': '개',
    },
}

SOLVABLE = {
    'schema': 'modu.solvable.v1',
    'problem_id': '0004_부등식',
    'problem_type': 'arithmetic_inequality_puzzle',
    'given': [
        {'ref': 'obj.inequality', 'value': '4□5 + 298 > 763'}
    ],
    'target': {'type': 'object', 'description': '□ 안의 수와 개수'},
    'method': 'algebraic_simplification_and_trial',
    'steps': [
        {
            'id': 'step.s1',
            'operation': 'subtraction',
            'expr': '763 - 298 = 465',
            'description': '4□5 > 465가 되어야 함을 알 수 있습니다.',
            'value': 465
        },
        {
            'id': 'step.s2',
            'operation': 'deduction',
            'expr': '□ > 6',
            'description': '4□5가 465보다 크려면 십의 자리 □는 6보다 커야 합니다.',
            'value': [7, 8, 9]
        },
        {
            'id': 'step.s3',
            'operation': 'counting',
            'expr': 'len([7, 8, 9]) = 3',
            'value': 3
        }
    ],
    'checks': [
        {
            'id': 'check.c1',
            'type': 'arithmetic_consistency_check',
            'pass': True,
            'expected': True,
            'actual': True,
            'expr': '475 + 298 > 763'
        }
    ],
    'answer': {'value': 3, 'unit': '개', 'derived_from': 'step.s3'},
    'inputs': {
        'total_ticks': 2,
        'target_label': '답',
        'target_ticks': 2,
        'target_count': 2,
        'unit': '개'
    },
    'plan': ['부등식을 풀어 4□5 > 465임을 구한 뒤, □가 7, 8, 9가 될 수 있음을 확인하여 총 3개임을 구합니다.']
}
