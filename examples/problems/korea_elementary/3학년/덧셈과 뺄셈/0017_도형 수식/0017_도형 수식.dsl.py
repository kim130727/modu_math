from __future__ import annotations

from modu_math.dsl import Arrow, BlankSlot, Canvas, ChoiceSlot, Circle, CircleSlot, Constraint, Cube, DiagramTemplate, FractionAreaModel, Grid, Group, LabelSlot, LineSlot, PathSlot, PolygonSlot, ProblemTemplate, RectSlot, Region, ShapeObject, TextSlot, Triangle

def build_problem_template() -> ProblemTemplate:
    canvas = Canvas(
        width=736,
        height=340,
        coordinate_mode='logical',
    )
    regions = (
        Region(
            id='region.stem',
            role='stem',
            flow='vertical',
            slot_ids=('slot.line1',
             'slot.eq1',
             'slot.eq2',
             'slot.answer_left_paren',
             'slot.answer_right_paren'),
        ),
    )
    slots = (
        TextSlot(
            id='slot.line1',
            prompt='',
            text='같은 모양은 같은 수를 나타낼 때 ■는 얼마를 나타냅니까?',
            style_role='body',
            x=20.0,
            y=42.0,
            font_size=22,
            font_family='Malgun Gothic',
            anchor='middle',
            fill='#000000',
        ),
        RectSlot(
            id='slot.equation_box',
            prompt='',
            x=165.0,
            y=112.0,
            width=402.0,
            height=140.0,
            stroke='#111111',
            stroke_width=1.0,
            rx=22.0,
            ry=22.0,
            fill='none',
        ),
        TextSlot(
            id='slot.eq1',
            prompt='',
            text='17×▲=■',
            style_role='body',
            x=290.0,
            y=164.0,
            font_size=44,
            font_family='Malgun Gothic',
            anchor='middle',
            fill='#000000',
        ),
        TextSlot(
            id='slot.eq2',
            prompt='',
            text='64÷▲=8',
            style_role='body',
            x=290.0,
            y=224.0,
            font_size=44,
            font_family='Malgun Gothic',
            anchor='middle',
            fill='#000000',
        ),
        RectSlot(
            id='slot.answer_blank',
            prompt='',
            x=430.0,
            y=272.0,
            width=235.0,
            height=44.0,
            stroke='none',
            stroke_width=1.0,
            fill='none',
            semantic_role='blank_answer',
        ),
        TextSlot(
            id='slot.answer_left_paren',
            prompt='',
            text='(',
            style_role='body',
            x=398.0,
            y=304.0,
            font_size=40,
            font_family='Malgun Gothic',
            anchor='middle',
            fill='#000000',
        ),
        TextSlot(
            id='slot.answer_right_paren',
            prompt='',
            text=')',
            style_role='body',
            x=700.0,
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
        id='0017_도형 수식',
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
    'problem_id': '0017_도형 수식',
    'problem_type': 'arithmetic_shape_equations',
    'metadata': {
        'language': 'ko',
        'question': '두 도형 수식(64 ÷ ▲ = 8, 17 × ▲ = ■)을 연계하여 ■의 값을 구하는 문제',
        'instruction': '■는 얼마를 나타냅니까?',
    },
    'domain': {
        'objects': [
            {'id': 'obj.triangle', 'type': 'variable', 'symbol': '▲'},
            {'id': 'obj.square', 'type': 'variable', 'symbol': '■'},
            {'id': 'obj.eq1', 'type': 'equation', 'value': '17 * Triangle = Square'},
            {'id': 'obj.eq2', 'type': 'equation', 'value': '64 / Triangle = 8'},
        ],
        'problem_solving': {
            'plan': {
                'method': 'substitution_solving',
                'description': '두 번째 식에서 ▲를 구한 뒤 첫 번째 식에 대입하여 ■를 구한다.',
            }
        },
    },
    'answer': {
        'value': 136,
        'unit': '',
    },
}

SOLVABLE = {
    'schema': 'modu.solvable.v1',
    'problem_id': '0017_도형 수식',
    'problem_type': 'arithmetic_shape_equations',
    'given': [
        {'ref': 'obj.eq1', 'value': '17 * ▲ = ■'},
        {'ref': 'obj.eq2', 'value': '64 / ▲ = 8'}
    ],
    'target': {'type': 'number', 'description': '■의 값'},
    'method': 'substitution_solving',
    'steps': [
        {
            'id': 'step.s1',
            'operation': 'division',
            'expr': '▲ = 64 / 8 = 8',
            'value': 8
        },
        {
            'id': 'step.s2',
            'operation': 'multiplication',
            'expr': '■ = 17 * 8 = 136',
            'value': 136
        }
    ],
    'checks': [
        {
            'id': 'check.c1',
            'type': 'arithmetic_consistency_check',
            'pass': True,
            'expected': 136,
            'actual': 136,
            'expr': '17 * 8'
        }
    ],
    'answer': {'value': 136, 'unit': '', 'derived_from': 'step.s2'},
    'inputs': {
        'total_ticks': 1,
        'target_label': '답',
        'target_ticks': 1,
        'target_count': 1,
        'unit': ''
    },
    'plan': ['두 번째 식에서 ▲=8임을 구하고, 이를 첫 번째 식에 대입하여 ■=136을 도출합니다.']
}
