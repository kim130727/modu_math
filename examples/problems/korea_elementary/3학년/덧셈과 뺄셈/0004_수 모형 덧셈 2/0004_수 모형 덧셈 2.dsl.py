from __future__ import annotations

from modu_math.dsl import Arrow, BlankSlot, Canvas, ChoiceSlot, Circle, CircleSlot, Constraint, Cube, DiagramTemplate, FractionAreaModel, Grid, Group, LabelSlot, LineSlot, PathSlot, PolygonSlot, ProblemTemplate, RectSlot, Region, ShapeObject, TextSlot, Triangle


def _hundred_grid_path(x: float, y: float) -> str:
    vertical = [f"M {x + 14 * i:g} {y:g} V {y + 140:g}" for i in range(1, 10)]
    horizontal = [f"M {x:g} {y + 14 * i:g} H {x + 140:g}" for i in range(1, 10)]
    return " ".join([*vertical, *horizontal])


def _ten_grid_path(x: float, y: float) -> str:
    vertical = [f"M {x + 14 * i:g} {y:g} V {y + 20:g}" for i in range(1, 10)]
    return " ".join(vertical)


def build_problem_template() -> ProblemTemplate:
    canvas = Canvas(
        width=1280,
        height=720,
        coordinate_mode='logical',
    )

    slots_list = [
        TextSlot(
            id='slot.instruction',
            prompt='',
            text='수 모형으로 137+286을 구해 보세요.',
            style_role='body',
            x=42.0,
            y=72.0,
            font_size=50,
            font_family='Malgun Gothic',
            anchor='start',
            fill='#222222',
            semantic_role='instruction',
        ),
        RectSlot(
            id='slot.model_box',
            prompt='',
            x=170.0,
            y=196.0,
            width=675.0,
            height=453.0,
            stroke='#9C9CA1',
            stroke_width=3.0,
            fill='none',
            semantic_role='container',
        ),
        LineSlot(
            id='slot.model_divider',
            prompt='',
            x1=170.0,
            y1=398.0,
            x2=845.0,
            y2=398.0,
            stroke='#9C9CA1',
            stroke_width=3.0,
            semantic_role='row_divider',
        ),
    ]

    # Top addend: 137 = 1 hundred, 3 tens, 7 ones
    slots_list.extend([
        RectSlot(
            id='slot.top_0_hundred',
            prompt='',
            x=200.0,
            y=218.0,
            width=140.0,
            height=140.0,
            stroke='#D3AE1D',
            stroke_width=2.0,
            fill='#F2CF43',
            semantic_role='hundred_block',
        ),
        PathSlot(
            id='slot.top_0_hundred_grid',
            prompt='',
            d=_hundred_grid_path(200.0, 218.0),
            stroke='#D3AE1D',
            stroke_width=1.0,
            fill='none',
            semantic_role='grid_lines',
        ),
    ])

    for i, y in enumerate((254.0, 278.0, 302.0)):
        slots_list.extend([
            RectSlot(
                id=f'slot.top_ten_{i}_ten',
                prompt='',
                x=420.0,
                y=y,
                width=140.0,
                height=20.0,
                stroke='#4B8FAF',
                stroke_width=2.0,
                fill='#6CB5D9',
                semantic_role='ten_block',
            ),
            PathSlot(
                id=f'slot.top_ten_{i}_ten_grid',
                prompt='',
                d=_ten_grid_path(420.0, y),
                stroke='#4B8FAF',
                stroke_width=1.0,
                fill='none',
                semantic_role='grid_lines',
            ),
        ])

    for i in range(7):
        slots_list.append(
            RectSlot(
                id=f'slot.top_one_{i}_one',
                prompt='',
                x=615.0 + 30.0 * i,
                y=278.0,
                width=20.0,
                height=20.0,
                stroke='#C95E5E',
                stroke_width=2.0,
                fill='#E87979',
                semantic_role='one_block',
            )
        )

    # Bottom addend: 286 = 2 hundreds, 8 tens, 6 ones
    slots_list.extend([
        RectSlot(
            id='slot.bottom_0_hundred',
            prompt='',
            x=200.0,
            y=446.0,
            width=140.0,
            height=140.0,
            stroke='#D3AE1D',
            stroke_width=2.0,
            fill='#F2CF43',
            semantic_role='hundred_block',
        ),
        PathSlot(
            id='slot.bottom_0_hundred_grid',
            prompt='',
            d=_hundred_grid_path(200.0, 446.0),
            stroke='#D3AE1D',
            stroke_width=1.0,
            fill='none',
            semantic_role='grid_lines',
        ),
        RectSlot(
            id='slot.bottom_1_hundred',
            prompt='',
            x=218.0,
            y=481.0,
            width=140.0,
            height=140.0,
            stroke='#D3AE1D',
            stroke_width=2.0,
            fill='#F2CF43',
            semantic_role='hundred_block',
        ),
        PathSlot(
            id='slot.bottom_1_hundred_grid',
            prompt='',
            d=_hundred_grid_path(218.0, 481.0),
            stroke='#D3AE1D',
            stroke_width=1.0,
            fill='none',
            semantic_role='grid_lines',
        ),
    ])

    for i in range(8):
        y = 439.0 + 24.0 * i
        slots_list.extend([
            RectSlot(
                id=f'slot.bottom_ten_{i}_ten',
                prompt='',
                x=420.0,
                y=y,
                width=140.0,
                height=20.0,
                stroke='#4B8FAF',
                stroke_width=2.0,
                fill='#6CB5D9',
                semantic_role='ten_block',
            ),
            PathSlot(
                id=f'slot.bottom_ten_{i}_ten_grid',
                prompt='',
                d=_ten_grid_path(420.0, y),
                stroke='#4B8FAF',
                stroke_width=1.0,
                fill='none',
                semantic_role='grid_lines',
            ),
        ])

    for i in range(6):
        slots_list.append(
            RectSlot(
                id=f'slot.bottom_one_{i}_one',
                prompt='',
                x=615.0 + 30.0 * i,
                y=523.0,
                width=20.0,
                height=20.0,
                stroke='#C95E5E',
                stroke_width=2.0,
                fill='#E87979',
                semantic_role='one_block',
            )
        )

    slots_list.extend([
        RectSlot(
            id='slot.answer_blank',
            prompt='',
            x=1120.0,
            y=576.0,
            width=135.0,
            height=78.0,
            stroke='#69BEEA',
            stroke_width=4.0,
            rx=10.0,
            fill='none',
            semantic_role='answer_blank',
        ),
        TextSlot(
            id='slot.equation_text',
            prompt='',
            text='137+286=',
            style_role='body',
            x=980.0,
            y=615.0,
            font_size=56,
            font_family='Malgun Gothic',
            anchor='middle',
            fill='#222222',
            semantic_role='equation',
        ),
    ])

    regions = (
        Region(
            id='region.stem',
            role='stem',
            flow='vertical',
            slot_ids=('slot.instruction', 'slot.equation_text'),
        ),
    )

    return ProblemTemplate(
        id='0004_수 모형 덧셈 2',
        title='',
        canvas=canvas,
        regions=regions,
        slots=tuple(slots_list),
        diagrams=(),
        groups=(),
        constraints=(),
    )


PROBLEM_TEMPLATE = build_problem_template()

SEMANTIC_OVERRIDE = {
    'problem_id': '0004_수 모형 덧셈 2',
    'problem_type': 'arithmetic_visual_model_addition',
    'metadata': {
        'language': 'ko',
        'question': '수 모형(백, 십, 일 모형)을 시각적으로 확인하여 137 + 286의 합을 구하는 문제',
        'instruction': '수 모형으로 137+286을 구해 보세요.',
    },
    'domain': {
        'objects': [
            {'id': 'obj.num1', 'type': 'number_model', 'value': 137, 'description': '137을 나타내는 수 모형'},
            {'id': 'obj.num2', 'type': 'number_model', 'value': 286, 'description': '286을 나타내는 수 모형'},
        ],
        'problem_solving': {
            'plan': {
                'method': 'visual_addition_with_regrouping',
                'description': '각 자리 모형을 합산하되, 일의 자리와 십의 자리에서 올림(받아올림)을 고려하여 전체 합을 구한다.',
            }
        },
    },
    'answer': {
        'value': 423,
        'unit': '',
    },
}

SOLVABLE = {
    'schema': 'modu.solvable.v1',
    'problem_id': '0004_수 모형 덧셈 2',
    'problem_type': 'arithmetic_visual_model_addition',
    'given': [
        {'ref': 'obj.num1', 'value': 137},
        {'ref': 'obj.num2', 'value': 286}
    ],
    'target': {'type': 'number', 'description': '137+286의 합'},
    'method': 'visual_addition_with_regrouping',
    'steps': [
        {
            'id': 'step.s1',
            'operation': 'addition',
            'expr': '137 + 286 = 423',
            'value': 423
        }
    ],
    'checks': [
        {
            'id': 'check.c1',
            'type': 'arithmetic_consistency_check',
            'pass': True,
            'expected': 423,
            'actual': 423,
            'expr': '137 + 286'
        }
    ],
    'answer': {'value': 423, 'unit': '', 'derived_from': 'step.s1'},
    'inputs': {
        'total_ticks': 1,
        'target_label': '답',
        'target_ticks': 1,
        'target_count': 1,
        'unit': ''
    },
    'plan': ['일의 자리(7+6=13), 십의 자리(3+8=11), 백의 자리(1+2=3)를 합산하여 받아올림을 포함해 423을 구합니다.']
}
