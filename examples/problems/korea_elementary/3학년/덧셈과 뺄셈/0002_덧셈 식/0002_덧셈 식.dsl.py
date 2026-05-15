from __future__ import annotations

from modu_math.dsl import Arrow, BlankSlot, Canvas, ChoiceSlot, Circle, CircleSlot, Constraint, Cube, DiagramTemplate, FractionAreaModel, Grid, Group, LabelSlot, LineSlot, PathSlot, PolygonSlot, ProblemTemplate, RectSlot, Region, ShapeObject, TextSlot, Triangle

def build_problem_template() -> ProblemTemplate:
    canvas = Canvas(
        width=408,
        height=212,
        coordinate_mode='logical',
    )
    regions = (
        Region(
            id='region.stem',
            role='stem',
            flow='vertical',
            slot_ids=('slot.instruction_1',
             'slot.instruction_2',
             'slot.candidate_1',
             'slot.candidate_2',
             'slot.candidate_3',
             'slot.candidate_4',
             'slot.plus_sign',
             'slot.equal_expr'),
        ),
    )
    slots = (
        RectSlot(
            id='slot.bg',
            prompt='',
            x=0.0,
            y=0.0,
            width=408.0,
            height=212.0,
            stroke='none',
            stroke_width=0.0,
            fill='none',
            semantic_role='background',
        ),
        TextSlot(
            id='slot.instruction_1',
            prompt='',
            text='다음 수 중에서 2개를 골라 덧셈식을 만들려고',
            style_role='body',
            x=6.0,
            y=30.0,
            font_size=17,
            font_family='Malgun Gothic',
            anchor='start',
            fill='#222222',
            semantic_role='instruction',
        ),
        TextSlot(
            id='slot.instruction_2',
            prompt='',
            text='합니다. □ 안에 알맞은 수를 써넣으세요.',
            style_role='body',
            x=6.0,
            y=60.0,
            font_size=17,
            font_family='Malgun Gothic',
            anchor='start',
            fill='#222222',
            semantic_role='instruction',
        ),
        RectSlot(
            id='slot.candidate_box',
            prompt='',
            x=6.0,
            y=78.0,
            width=396.0,
            height=56.0,
            stroke='#666666',
            stroke_width=1.5,
            rx=10.0,
            ry=10.0,
            fill='none',
            semantic_role='guide',
        ),
        TextSlot(
            id='slot.candidate_1',
            prompt='',
            text='718',
            style_role='body',
            x=74.0,
            y=113.0,
            font_size=17,
            font_family='Malgun Gothic',
            anchor='middle',
            fill='#222222',
            semantic_role='label',
        ),
        TextSlot(
            id='slot.candidate_2',
            prompt='',
            text='295',
            style_role='body',
            x=160.0,
            y=113.0,
            font_size=17,
            font_family='Malgun Gothic',
            anchor='middle',
            fill='#222222',
            semantic_role='label',
        ),
        TextSlot(
            id='slot.candidate_3',
            prompt='',
            text='658',
            style_role='body',
            x=246.0,
            y=113.0,
            font_size=17,
            font_family='Malgun Gothic',
            anchor='middle',
            fill='#222222',
            semantic_role='label',
        ),
        TextSlot(
            id='slot.candidate_4',
            prompt='',
            text='245',
            style_role='body',
            x=332.0,
            y=113.0,
            font_size=17,
            font_family='Malgun Gothic',
            anchor='middle',
            fill='#222222',
            semantic_role='label',
        ),
        RectSlot(
            id='slot.blank_left',
            prompt='',
            x=94.0,
            y=150.0,
            width=69.0,
            height=36.0,
            stroke='#666666',
            stroke_width=1.5,
            fill='none',
            semantic_role='answer_anchor',
        ),
        RectSlot(
            id='slot.blank_right',
            prompt='',
            x=184.0,
            y=150.0,
            width=69.0,
            height=36.0,
            stroke='#666666',
            stroke_width=1.5,
            fill='none',
            semantic_role='answer_anchor',
        ),
        TextSlot(
            id='slot.plus_sign',
            prompt='',
            text='+',
            style_role='body',
            x=173.0,
            y=176.0,
            font_size=34,
            font_family='Malgun Gothic',
            anchor='middle',
            fill='#222222',
            semantic_role='label',
        ),
        TextSlot(
            id='slot.equal_expr',
            prompt='',
            text='=953',
            style_role='body',
            x=300.0,
            y=176.0,
            font_size=34,
            font_family='Malgun Gothic',
            anchor='middle',
            fill='#222222',
            semantic_role='label',
        ),
    )
    diagrams = (
    )
    groups = (
    )
    constraints = (
    )
    return ProblemTemplate(
        id='0002_덧셈 식',
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
    'problem_id': '0002_덧셈 식',
    'problem_type': 'arithmetic_combination_sum',
    'metadata': {
        'language': 'ko',
        'question': '주어진 네 수(718, 295, 658, 245) 중 두 수를 골라 합이 953이 되는 덧셈식을 완성하는 문제',
        'instruction': '□ 안에 알맞은 수를 써넣으세요.',
    },
    'domain': {
        'objects': [
            {'id': 'obj.candidates', 'type': 'list', 'value': [718, 295, 658, 245]},
            {'id': 'obj.target_sum', 'type': 'number', 'value': 953},
        ],
        'problem_solving': {
            'plan': {
                'method': 'exhaustive_search',
                'description': '주어진 수들을 조합하여 더했을 때 953이 나오는 쌍을 찾는다.',
            }
        },
    },
    'answer': {
        'value': [295, 658],
        'unit': '',
    },
}

SOLVABLE = {
    'schema': 'modu.solvable.v1',
    'problem_id': '0002_덧셈 식',
    'problem_type': 'arithmetic_combination_sum',
    'given': [
        {'ref': 'obj.candidates', 'value': [718, 295, 658, 245]},
        {'ref': 'obj.target_sum', 'value': 953}
    ],
    'target': {'type': 'list', 'description': '합이 953인 두 수'},
    'method': 'exhaustive_search',
    'steps': [
        {
            'id': 'step.s1',
            'operation': 'addition',
            'expr': '295 + 658 = 953',
            'value': 953
        }
    ],
    'checks': [
        {
            'id': 'check.c1',
            'type': 'arithmetic_consistency_check',
            'pass': True,
            'expected': 953,
            'actual': 953,
            'expr': '295 + 658'
        }
    ],
    'answer': {'value': 953, 'unit': '', 'derived_from': 'step.s1'},
    'inputs': {
        'total_ticks': 2,
        'target_label': '답',
        'target_ticks': 2,
        'target_count': 2,
        'unit': ''
    },
    'plan': ['295와 658을 더하면 953이 됨을 확인하여 빈칸을 채웁니다.']
}
