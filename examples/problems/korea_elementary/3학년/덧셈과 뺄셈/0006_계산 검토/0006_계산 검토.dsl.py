from __future__ import annotations

from modu_math.dsl import Arrow, BlankSlot, Canvas, ChoiceSlot, Circle, CircleSlot, Constraint, Cube, DiagramTemplate, FractionAreaModel, Grid, Group, LabelSlot, LineSlot, PathSlot, PolygonSlot, ProblemTemplate, RectSlot, Region, ShapeObject, TextSlot, Triangle

def build_problem_template() -> ProblemTemplate:
    canvas = Canvas(
        width=1744,
        height=725,
        coordinate_mode='logical',
    )
    regions = (
        Region(
            id='region.stem',
            role='stem',
            flow='vertical',
            slot_ids=('slot.instruction',
             'slot.right_tab_text',
             'slot.left_top',
             'slot.left_mid',
             'slot.left_result'),
        ),
    )
    slots = (
        TextSlot(
            id='slot.instruction',
            prompt='',
            text='잘못 계산한 곳에 ○표 하고, 바르게 계산해 보세요.',
            style_role='body',
            x=115.52105,
            y=95.168732,
            font_size=66,
            font_family='Malgun Gothic',
            anchor='start',
            fill='#222222',
            semantic_role='instruction',
        ),
        RectSlot(
            id='slot.right_tab',
            prompt='',
            x=1089.9678,
            y=169.6675,
            width=400.0,
            height=100.0,
            stroke='none',
            stroke_width=0.0,
            rx=38.0,
            fill='#CE8D61',
            semantic_role='tab',
        ),
        RectSlot(
            id='slot.right_panel',
            prompt='',
            x=966.96783,
            y=205.6675,
            width=615.0,
            height=455.0,
            stroke='#CFC8BA',
            stroke_width=9.0,
            rx=70.0,
            fill='none',
            semantic_role='panel',
        ),
        RectSlot(
            id='slot.left_panel',
            prompt='',
            x=203.9678,
            y=215.6675,
            width=585.0,
            height=435.0,
            stroke='#CFC8BA',
            stroke_width=9.0,
            rx=70.0,
            fill='none',
            semantic_role='panel',
        ),
        TextSlot(
            id='slot.right_tab_text',
            prompt='',
            text='바르게 계산하기',
            style_role='body',
            x=1289.9678,
            y=231.6675,
            font_size=42,
            font_family='Malgun Gothic',
            anchor='middle',
            fill='#FFFFFF',
            semantic_role='tab_label',
        ),
        TextSlot(
            id='slot.left_top',
            prompt='',
            text='323',
            style_role='body',
            x=622.57715,
            y=360.0,
            font_size=88,
            font_family='Cambria',
            anchor='end',
            fill='#222222',
            semantic_role='equation',
        ),
        PolygonSlot(
            id='slot.arrow_head',
            prompt='',
            points=((892.96783, 408.66748), (914.96783, 435.66748), (892.96783, 462.66748)),
            stroke='none',
            stroke_width=0.0,
            fill='#9AAAB2',
            semantic_role='arrow',
        ),
        LineSlot(
            id='slot.arrow_body',
            prompt='',
            x1=852.96783,
            y1=435.66748,
            x2=892.96783,
            y2=435.66748,
            stroke='#9AAAB2',
            stroke_width=14.0,
            semantic_role='arrow',
        ),
        TextSlot(
            id='slot.left_mid',
            prompt='',
            text='+998',
            style_role='body',
            x=622.57715,
            y=460.0,
            font_size=88,
            font_family='Cambria',
            anchor='end',
            fill='#222222',
            semantic_role='equation',
        ),
        LineSlot(
            id='slot.left_line',
            prompt='',
            x1=296.30759,
            y1=486.0,
            x2=636.30762,
            y2=486.0,
            stroke='#333333',
            stroke_width=3.0,
            semantic_role='equation_line',
        ),
        TextSlot(
            id='slot.left_result',
            prompt='',
            text='1221',
            style_role='body',
            x=622.57715,
            y=560.0,
            font_size=87,
            font_family='Cambria',
            anchor='end',
            fill='#222222',
            semantic_role='wrong_result',
        ),
    )
    diagrams = (
    )
    groups = (
    )
    constraints = (
    )
    return ProblemTemplate(
        id='0006_계산 검토',
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
    'problem_id': '0006_계산 검토',
    'problem_type': 'arithmetic_error_correction',
    'metadata': {
        'language': 'ko',
        'question': '잘못 계산된 세로 덧셈식(323+998=1221)을 찾아 바르게 고치는 문제',
        'instruction': '잘못 계산한 곳에 ○표 하고, 바르게 계산해 보세요.',
    },
    'domain': {
        'objects': [
            {'id': 'obj.wrong_eq', 'type': 'equation', 'value': '323+998=1221', 'description': '잘못된 식'},
        ],
        'problem_solving': {
            'plan': {
                'method': 'recalculation_and_correction',
                'description': '받아올림을 주의하며 덧셈을 다시 수행하여 올바른 결과를 구한다.',
            }
        },
    },
    'answer': {
        'value': 1321,
        'unit': '',
    },
}

SOLVABLE = {
    'schema': 'modu.solvable.v1',
    'problem_id': '0006_계산 검토',
    'problem_type': 'arithmetic_error_correction',
    'given': [
        {'ref': 'obj.wrong_eq', 'value': '323+998=1221'}
    ],
    'target': {'type': 'number', 'description': '올바른 계산 결과'},
    'method': 'recalculation_and_correction',
    'steps': [
        {
            'id': 'step.s1',
            'operation': 'addition',
            'expr': '323 + 998 = 1321',
            'value': 1321
        }
    ],
    'checks': [
        {
            'id': 'check.c1',
            'type': 'arithmetic_consistency_check',
            'pass': True,
            'expected': 1321,
            'actual': 1321,
            'expr': '323 + 998'
        }
    ],
    'answer': {'value': 1321, 'unit': '', 'derived_from': 'step.s1'},
    'inputs': {
        'total_ticks': 1,
        'target_label': '답',
        'target_ticks': 1,
        'target_count': 1,
        'unit': ''
    },
    'plan': ['세로셈에서 십의 자리와 백의 자리의 받아올림을 정확히 계산하여 1321을 구합니다.']
}
