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
            slot_ids=('slot.t1', 'slot.t2', 'slot.v1', 'slot.v2', 'slot.v3'),
        ),
    )
    slots = (
        TextSlot(
            id='slot.t1',
            prompt='',
            text='다음 뺄셈식에서 같은 모양은 같은 숫자를 나타냅니다.',
            style_role='body',
        ),
        TextSlot(
            id='slot.t2',
            prompt='',
            text='■와 ★가 나타내는 숫자의 합을 구하시오.',
            style_role='body',
        ),
        TextSlot(
            id='slot.v1',
            prompt='',
            text='  ■ ★ ■',
            style_role='body',
        ),
        TextSlot(
            id='slot.v2',
            prompt='',
            text='- ★ ■ ★',
            style_role='body',
        ),
        TextSlot(
            id='slot.v3',
            prompt='',
            text='  ★ 7 3',
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
        id='0009_도형 복면산 뺄셈',
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
    'problem_id': '0009_도형 복면산 뺄셈',
    'problem_type': 'arithmetic_alphametic_subtraction',
    'metadata': {
        'language': 'ko',
        'question': '도형(■, ★)이 포함된 복면산 뺄셈식(■★■ - ★■★ = ★73)에서 두 도형이 나타내는 숫자의 합을 구하는 문제',
        'instruction': '■와 ★가 나타내는 숫자의 합을 구하시오.',
    },
    'domain': {
        'objects': [
            {'id': 'obj.square', 'type': 'variable', 'symbol': '■'},
            {'id': 'obj.star', 'type': 'variable', 'symbol': '★'},
            {'id': 'obj.equation', 'type': 'equation', 'value': 'SquareStarSquare - StarSquareStar = Star73'},
        ],
        'problem_solving': {
            'plan': {
                'method': 'digit_deduction',
                'description': '각 자릿수별로 받아내림을 고려하여 가능한 숫자를 추론한다.',
            }
        },
    },
    'answer': {
        'value': 7,
        'unit': '',
    },
}

SOLVABLE = {
    'schema': 'modu.solvable.v1',
    'problem_id': '0009_도형 복면산 뺄셈',
    'problem_type': 'arithmetic_alphametic_subtraction',
    'given': [
        {'ref': 'obj.equation', 'value': '■★■ - ★■★ = ★73'}
    ],
    'target': {'type': 'number', 'description': '두 숫자의 합'},
    'method': 'digit_deduction',
    'steps': [
        {
            'id': 'step.s1',
            'operation': 'deduction',
            'expr': '525 - 252 = 273',
            'description': '■=5, ★=2일 때 식이 성립합니다.',
            'value': {'■': 5, '★': 2}
        },
        {
            'id': 'step.s2',
            'operation': 'addition',
            'expr': '5 + 2 = 7',
            'value': 7
        }
    ],
    'checks': [
        {
            'id': 'check.c1',
            'type': 'arithmetic_consistency_check',
            'pass': True,
            'expected': 7,
            'actual': 7,
            'expr': '5 + 2'
        }
    ],
    'answer': {'value': 7, 'unit': '', 'derived_from': 'step.s2'},
    'inputs': {
        'total_ticks': 1,
        'target_label': '답',
        'target_ticks': 1,
        'target_count': 1,
        'unit': ''
    },
    'plan': ['각 자릿수를 비교하여 ■=5, ★=2임을 찾아내고, 두 수의 합인 7을 구합니다.']
}
