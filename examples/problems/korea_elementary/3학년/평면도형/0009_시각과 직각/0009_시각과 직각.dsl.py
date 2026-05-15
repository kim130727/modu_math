from __future__ import annotations

from modu_math.dsl import Arrow, BlankSlot, Canvas, ChoiceSlot, Circle, CircleSlot, Constraint, Cube, DiagramTemplate, FractionAreaModel, Grid, Group, LabelSlot, LineSlot, PathSlot, PolygonSlot, ProblemTemplate, RectSlot, Region, ShapeObject, TextSlot, Triangle

def build_problem_template() -> ProblemTemplate:
    canvas = Canvas(
        width=400,
        height=180,
        coordinate_mode='logical',
    )
    regions = (
        Region(
            id='region.stem',
            role='stem',
            flow='vertical',
            slot_ids=('slot.i1', 'slot.i2', 'slot.c1', 'slot.c2', 'slot.c3', 'slot.c4', 'slot.c5'),
        ),
    )
    slots = (
        RectSlot(
            id='slot.bg',
            prompt='',
            x=0.0,
            y=0.0,
            width=400.0,
            height=180.0,
            stroke='none',
            stroke_width=0.0,
            fill='#F4F4F4',
        ),
        TextSlot(
            id='slot.i1',
            prompt='',
            text='시계의 긴바늘과 짧은바늘이 이루는 각이',
            style_role='body',
            x=4.0,
            y=34.0,
            font_size=17,
            font_family='Malgun Gothic',
            anchor='middle',
            fill='#222222',
        ),
        TextSlot(
            id='slot.i2',
            prompt='',
            text='직각인 시각은 언제인가요?',
            style_role='body',
            x=4.0,
            y=64.0,
            font_size=17,
            font_family='Malgun Gothic',
            anchor='middle',
            fill='#222222',
        ),
        TextSlot(
            id='slot.c1',
            prompt='',
            text='① 2시',
            style_role='body',
            x=4.0,
            y=106.0,
            font_size=17,
            font_family='Malgun Gothic',
            anchor='middle',
            fill='#222222',
        ),
        TextSlot(
            id='slot.c2',
            prompt='',
            text='② 6시',
            style_role='body',
            x=112.0,
            y=106.0,
            font_size=17,
            font_family='Malgun Gothic',
            anchor='middle',
            fill='#222222',
        ),
        TextSlot(
            id='slot.c3',
            prompt='',
            text='③ 9시',
            style_role='body',
            x=224.0,
            y=106.0,
            font_size=17,
            font_family='Malgun Gothic',
            anchor='middle',
            fill='#222222',
        ),
        RectSlot(
            id='slot.answer_text',
            prompt='',
            x=348.0,
            y=146.0,
            width=44.0,
            height=28.0,
            stroke='none',
            stroke_width=0.0,
            fill='none',
            semantic_role='answer_anchor',
        ),
        TextSlot(
            id='slot.c4',
            prompt='',
            text='④ 10시',
            style_role='body',
            x=4.0,
            y=148.0,
            font_size=17,
            font_family='Malgun Gothic',
            anchor='middle',
            fill='#222222',
        ),
        TextSlot(
            id='slot.c5',
            prompt='',
            text='⑤ 11시',
            style_role='body',
            x=112.0,
            y=148.0,
            font_size=17,
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
        id='0009_시각과 직각',
        title='',
        canvas=canvas,
        regions=regions,
        slots=slots,
        diagrams=diagrams,
        groups=groups,
        constraints=constraints,
    )

PROBLEM_TEMPLATE = build_problem_template()
