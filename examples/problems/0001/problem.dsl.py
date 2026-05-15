from __future__ import annotations

from modu_math.dsl import Canvas, ProblemTemplate, Region, TextSlot

def build_problem_template() -> ProblemTemplate:
    canvas = Canvas(
        width=1200,
        height=250,
        coordinate_mode='logical',
    )
    regions = (
        Region(
            id='region.stem',
            role='stem',
            flow='absolute',
            slot_ids=('slot.line_1', 'slot.line_2', 'slot.answer'),
        ),
    )
    slots = (
        TextSlot(
            id='slot.line_1',
            prompt='',
            text='예은이가 시계를 보았더니 7시 17분 25초였습니다.',
            style_role='body',
            x=30.0,
            y=60.0,
            font_size=35,
            fill='#111111',
        ),
        TextSlot(
            id='slot.line_2',
            prompt='',
            text='36분 47초 후의 시각이 ㉠시 ㉡분 ㉢초일 때 ㉠+㉡+㉢을 구하시오.',
            style_role='body',
            x=30.0,
            y=120.0,
            font_size=35,
            fill='#111111',
        ),
        TextSlot(
            id='slot.answer',
            prompt='',
            text='(            )',
            style_role='body',
            x=500.0,
            y=180.0,
            font_size=35,
            fill='#111111',
        ),
    )
    return ProblemTemplate(
        id='0001',
        title='',
        canvas=canvas,
        regions=regions,
        slots=slots,
        diagrams=(),
        groups=(),
        constraints=(),
    )

PROBLEM_TEMPLATE = build_problem_template()
