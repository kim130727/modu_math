from __future__ import annotations

from modu_math.dsl import Arrow, BlankSlot, Canvas, ChoiceSlot, Circle, CircleSlot, Constraint, Cube, DiagramTemplate, FractionAreaModel, Grid, Group, LabelSlot, LineSlot, PathSlot, PolygonSlot, ProblemTemplate, RectSlot, Region, ShapeObject, TextSlot, Triangle

def build_problem_template() -> ProblemTemplate:
    canvas = Canvas(
        width=767,
        height=162,
        coordinate_mode='logical',
    )
    regions = (
        Region(
            id='region.stem',
            role='stem',
            flow='vertical',
            slot_ids=('slot.t1', 'slot.t2'),
        ),
    )
    slots = (
        RectSlot(
            id='slot.bg',
            prompt='',
            x=0.0,
            y=0.0,
            width=767.0,
            height=162.0,
            stroke='none',
            stroke_width=0.0,
            fill='none',
        ),
        TextSlot(
            id='slot.t1',
            prompt='',
            text='소희는 종이별을 399개 접었고, 은별이는 소희보다 115개만큼 더 많이 접었습니다.',
            style_role='body',
            x=8.0,
            y=32.0,
            font_size=17,
            font_family='Malgun Gothic',
            anchor='start',
            fill='#222222',
        ),
        TextSlot(
            id='slot.t2',
            prompt='',
            text='두 사람이 접은 종이별은 모두 몇 개인지 식과 답을 구하시오.',
            style_role='body',
            x=8.0,
            y=60.0,
            font_size=17,
            font_family='Malgun Gothic',
            anchor='start',
            fill='#222222',
        ),
        RectSlot(
            id='slot.answer_total',
            prompt='',
            x=689.0,
            y=120.0,
            width=60.0,
            height=30.0,
            stroke='none',
            stroke_width=0.0,
            fill='none',
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
        id='0005_종이별 개수',
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
    'problem_id': '0005_종이별 개수',
    'problem_type': 'arithmetic_word_problem_addition_multi_step',
    'metadata': {
        'language': 'ko',
        'question': '소희와 은별이가 접은 종이별의 총 개수를 구하는 문제 (은별이는 소희보다 일정량 더 많이 접음)',
        'instruction': '두 사람이 접은 종이별은 모두 몇 개인지 식과 답을 구하시오.',
    },
    'domain': {
        'objects': [
            {'id': 'obj.sohee', 'type': 'count', 'value': 399, 'description': '소희가 접은 별'},
            {'id': 'obj.diff', 'type': 'count', 'value': 115, 'description': '은별이가 더 접은 양'},
        ],
        'problem_solving': {
            'plan': {
                'method': 'stepwise_addition',
                'description': '은별이가 접은 별의 수를 먼저 구하고, 소희와 은별이의 별의 수를 합산한다.',
            }
        },
    },
    'answer': {
        'value': 913,
        'unit': '개',
    },
}

SOLVABLE = {
    'schema': 'modu.solvable.v1',
    'problem_id': '0005_종이별 개수',
    'problem_type': 'arithmetic_word_problem_addition_multi_step',
    'given': [
        {'ref': 'obj.sohee', 'value': 399},
        {'ref': 'obj.diff', 'value': 115}
    ],
    'target': {'type': 'count', 'description': '전체 별의 수'},
    'method': 'stepwise_addition',
    'steps': [
        {
            'id': 'step.s1',
            'operation': 'addition',
            'expr': '399 + 115 = 514',
            'description': '은별이가 접은 별은 514개입니다.',
            'value': 514
        },
        {
            'id': 'step.s2',
            'operation': 'addition',
            'expr': '399 + 514 = 913',
            'description': '두 사람이 접은 별은 총 913개입니다.',
            'value': 913
        }
    ],
    'checks': [
        {
            'id': 'check.c1',
            'type': 'arithmetic_consistency_check',
            'pass': True,
            'expected': 913,
            'actual': 913,
            'expr': '399 + (399 + 115)'
        }
    ],
    'answer': {'value': 913, 'unit': '개', 'derived_from': 'step.s2'},
    'inputs': {
        'total_ticks': 1,
        'target_label': '답',
        'target_ticks': 1,
        'target_count': 1,
        'unit': '개'
    },
    'plan': ['은별이가 접은 514개와 소희의 399개를 더해 총 913개를 구합니다.']
}
