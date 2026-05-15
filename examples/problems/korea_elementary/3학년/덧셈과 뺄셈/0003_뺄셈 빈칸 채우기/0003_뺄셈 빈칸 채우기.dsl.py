from __future__ import annotations

from modu_math.dsl import Arrow, BlankSlot, Canvas, ChoiceSlot, Circle, CircleSlot, Constraint, Cube, DiagramTemplate, FractionAreaModel, Grid, Group, LabelSlot, LineSlot, PathSlot, PolygonSlot, ProblemTemplate, RectSlot, Region, ShapeObject, TextSlot, Triangle

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
            slot_ids=('slot.t1',
             'slot.t2',
             'slot.text_11',
             'slot.text_8',
             'slot.text_9',
             'slot.v2',
             'slot.text_12',
             'slot.text_10',
             'slot.text_7',
             'slot.v4'),
        ),
    )
    slots = (
        TextSlot(
            id='slot.t1',
            prompt='',
            text='오른쪽 뺄셈식에서 같은 문자는 같은 숫자를 나타냅니다.',
            style_role='body',
            x=50.29764150834108,
            y=82.05971772177185,
            font_size=35,
            font_family='sans-serif',
            anchor='start',
            fill='#000000',
        ),
        TextSlot(
            id='slot.t2',
            prompt='',
            text='서로 다른 숫자 ㉠, ㉡, ㉢의 합을 구하시오.',
            style_role='body',
            x=48.02522586405705,
            y=146.4619347708566,
            font_size=35,
            font_family='sans-serif',
            anchor='start',
            fill='#000000',
        ),
        TextSlot(
            id='slot.text_11',
            prompt='',
            text='2',
            style_role='body',
            x=482.7040710449219,
            y=272.28443908691406,
            font_size=45,
            fill='#111',
        ),
        TextSlot(
            id='slot.text_8',
            prompt='',
            text='㉡',
            style_role='body',
            x=419.2308349609375,
            y=273.5798034667969,
            font_size=45,
            fill='#111',
        ),
        TextSlot(
            id='slot.text_9',
            prompt='',
            text='㉠',
            style_role='body',
            x=368.7113494873047,
            y=273.57981872558594,
            font_size=45,
            fill='#111',
        ),
        TextSlot(
            id='slot.v2',
            prompt='',
            text='-',
            style_role='body',
            x=346.55812971635197,
            y=333.8746022191541,
            font_size=41,
            font_family='sans-serif',
            anchor='start',
            fill='#000000',
        ),
        TextSlot(
            id='slot.text_12',
            prompt='',
            text='㉢',
            style_role='body',
            x=473.6365203857422,
            y=338.3484344482422,
            font_size=45,
            fill='#111',
        ),
        TextSlot(
            id='slot.text_10',
            prompt='',
            text='1',
            style_role='body',
            x=377.7789764404297,
            y=338.34844970703125,
            font_size=45,
            fill='#111',
        ),
        TextSlot(
            id='slot.text_7',
            prompt='',
            text='㉠',
            style_role='body',
            x=417.9355163574219,
            y=339.64376068115234,
            font_size=45,
            fill='#111',
        ),
        RectSlot(
            id='slot.v3_line',
            prompt='',
            x=328.235107421875,
            y=359.2491149902344,
            width=220.0,
            height=3.0,
            stroke='#000000',
            stroke_width=1.0,
            fill='black',
        ),
        TextSlot(
            id='slot.v4',
            prompt='',
            text='3 1 4',
            style_role='body',
            x=378.6347557596757,
            y=429.7482486748209,
            font_size=53,
            font_family='sans-serif',
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
        id='0003_뺄셈 빈칸 채우기',
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
    'problem_id': '0003_뺄셈 빈칸 채우기',
    'problem_type': 'arithmetic_vertical_subtraction_puzzle',
    'metadata': {
        'language': 'ko',
        'question': '세로 뺄셈식 [㉠㉡2] - [1㉠㉢] = [314]에서 각 기호가 나타내는 숫자를 찾아 합을 구하는 문제',
        'instruction': '서로 다른 숫자 ㉠, ㉡, ㉢의 합을 구하시오.',
    },
    'domain': {
        'objects': [
            {'id': 'obj.vertical_sub', 'type': 'vertical_arithmetic', 'description': '[㉠㉡2] - [1㉠㉢] = [314]'},
        ],
        'problem_solving': {
            'plan': {
                'method': 'digit_analysis',
                'description': '각 자릿수별로 뺄셈 원리를 적용하여 기호의 값을 찾는다. 일의 자리에서 받아내림을 고려하고 백의 자리부터 확정한다.',
            }
        },
    },
    'answer': {
        'value': 18,
        'unit': '',
    },
}

SOLVABLE = {
    'schema': 'modu.solvable.v1',
    'problem_id': '0003_뺄셈 빈칸 채우기',
    'problem_type': 'arithmetic_vertical_subtraction_puzzle',
    'given': [
        {'ref': 'obj.vertical_sub', 'value': '[㉠㉡2] - [1㉠㉢] = [314]'}
    ],
    'target': {'type': 'number', 'description': '㉠+㉡+㉢의 값'},
    'method': 'digit_analysis',
    'steps': [
        {
            'id': 'step.s1',
            'operation': 'deduction',
            'expr': '㉠ - 1 = 3',
            'description': '백의 자리에서 ㉠=4임을 알 수 있습니다.',
            'value': 4
        },
        {
            'id': 'step.s2',
            'operation': 'deduction',
            'expr': '12 - ㉢ = 4',
            'description': '일의 자리에서 ㉢=8임을 알 수 있습니다. (십의 자리에서 받아내림 발생)',
            'value': 8
        },
        {
            'id': 'step.s3',
            'operation': 'deduction',
            'expr': '(㉡ - 1) - 4 = 1',
            'description': '십의 자리에서 받아내림을 고려하여 ㉡=6임을 알 수 있습니다.',
            'value': 6
        },
        {
            'id': 'step.s4',
            'operation': 'addition',
            'expr': '4 + 6 + 8 = 18',
            'description': '세 숫자의 합을 구합니다.',
            'value': 18
        }
    ],
    'checks': [
        {
            'id': 'check.c1',
            'type': 'arithmetic_consistency_check',
            'pass': True,
            'expected': 314,
            'actual': 314,
            'expr': '462 - 148'
        }
    ],
    'answer': {'value': 18, 'unit': '', 'derived_from': 'step.s4'},
    'inputs': {
        'total_ticks': 1,
        'target_label': '답',
        'target_ticks': 1,
        'target_count': 1,
        'unit': ''
    },
    'plan': ['백의 자리에서 ㉠=4, 일의 자리에서 ㉢=8, 십의 자리에서 ㉡=6임을 찾아 모두 더합니다.']
}
