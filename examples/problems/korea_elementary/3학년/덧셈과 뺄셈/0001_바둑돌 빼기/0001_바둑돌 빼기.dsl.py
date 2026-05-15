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
            slot_ids=('slot.p1', 'slot.p2', 'slot.p3'),
        ),
    )
    slots = (
        TextSlot(
            id='slot.p1',
            prompt='',
            text='바둑돌 통에 검은색 바둑돌 374개와 흰색 바둑돌 558개가 있었습니다.',
            style_role='body',
            x=50.0,
            y=80.0,
            font_size=24,
            font_family='sans-serif',
            anchor='start',
            fill='#000000',
        ),
        TextSlot(
            id='slot.p2',
            prompt='',
            text='그중에서 몇 개를 뺐더니 463개가 남았습니다.',
            style_role='body',
            x=50.0,
            y=180.0,
            font_size=24,
            font_family='sans-serif',
            anchor='start',
            fill='#000000',
        ),
        TextSlot(
            id='slot.p3',
            prompt='',
            text='뺀 바둑돌은 몇 개입니까?',
            style_role='body',
            x=50.0,
            y=260.0,
            font_size=24,
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
        id='0001_바둑돌 빼기',
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
    'problem_id': '0001_바둑돌 빼기',
    'problem_type': 'arithmetic_word_problem_subtraction',
    'metadata': {
        'language': 'ko',
        'question': '검은색 바둑돌 374개와 흰색 바둑돌 558개 중 일부를 뺀 후 463개가 남았을 때, 뺀 바둑돌의 수를 구하는 문제',
        'instruction': '뺀 바둑돌은 몇 개입니까?',
    },
    'domain': {
        'objects': [
            {'id': 'obj.black', 'type': 'count', 'value': 374, 'description': '검은색 바둑돌'},
            {'id': 'obj.white', 'type': 'count', 'value': 558, 'description': '흰색 바둑돌'},
            {'id': 'obj.remaining', 'type': 'count', 'value': 463, 'description': '남은 바둑돌'},
        ],
        'problem_solving': {
            'plan': {
                'method': 'total_then_subtract',
                'description': '먼저 검은색과 흰색 바둑돌을 합해 전체 바둑돌 수를 구하고, 거기서 남은 바둑돌 수를 빼서 뺀 바둑돌 수를 구한다.',
            }
        },
    },
    'answer': {
        'value': 469,
        'unit': '개',
    },
}

SOLVABLE = {
    'schema': 'modu.solvable.v1',
    'problem_id': '0001_바둑돌 빼기',
    'problem_type': 'arithmetic_word_problem_subtraction',
    'given': [
        {'ref': 'obj.black', 'value': 374},
        {'ref': 'obj.white', 'value': 558},
        {'ref': 'obj.remaining', 'value': 463}
    ],
    'target': {'type': 'count', 'description': '뺀 바둑돌의 수'},
    'method': 'total_then_subtract',
    'steps': [
        {
            'id': 'step.s1',
            'operation': 'addition',
            'expr': '374 + 558 = 932',
            'value': 932
        },
        {
            'id': 'step.s2',
            'operation': 'subtraction',
            'expr': '932 - 463 = 469',
            'value': 469
        }
    ],
    'checks': [
        {
            'id': 'check.c1',
            'type': 'arithmetic_consistency_check',
            'pass': True,
            'expected': 469,
            'actual': 469,
            'expr': '932 - 469 = 463'
        }
    ],
    'answer': {'value': 469, 'unit': '개', 'derived_from': 'step.s2'},
    'inputs': {
        'total_ticks': 1,
        'target_label': '답',
        'target_ticks': 1,
        'target_count': 1,
        'unit': '개'
    },
    'plan': ['전체 바둑돌 932개에서 남은 463개를 빼서 469개를 구합니다.']
}
