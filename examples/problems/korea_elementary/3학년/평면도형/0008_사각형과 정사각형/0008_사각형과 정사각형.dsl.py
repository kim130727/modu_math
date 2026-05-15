from __future__ import annotations

from modu_math.dsl import Arrow, BlankSlot, Canvas, ChoiceSlot, Circle, CircleSlot, Constraint, Cube, DiagramTemplate, FractionAreaModel, Grid, Group, LabelSlot, LineSlot, PathSlot, PolygonSlot, ProblemTemplate, RectSlot, Region, ShapeObject, TextSlot, Triangle

def build_problem_template() -> ProblemTemplate:
    canvas = Canvas(
        width=400,
        height=260,
        coordinate_mode='logical',
    )
    regions = (
        Region(
            id='region.stem',
            role='stem',
            flow='vertical',
            slot_ids=('slot.i1',
             'slot.ga_t',
             'slot.na_t',
             'slot.da_t',
             'slot.ra_t',
             'slot.ma_t',
             'slot.ba_t'),
        ),
    )
    slots = (
        RectSlot(
            id='slot.bg',
            prompt='',
            x=0.0,
            y=0.0,
            width=400.0,
            height=260.0,
            stroke='none',
            stroke_width=0.0,
            fill='#F4F4F4',
        ),
        TextSlot(
            id='slot.i1',
            prompt='',
            text='직사각형은 정사각형보다 몇 개 더 많은지 구하세요.',
            style_role='body',
            x=4.0,
            y=34.0,
            font_size=17,
            font_family='Malgun Gothic',
            anchor='middle',
            fill='#222222',
        ),
        RectSlot(
            id='slot.frame',
            prompt='',
            x=6.0,
            y=52.0,
            width=384.0,
            height=194.0,
            stroke='#8A8A8A',
            stroke_width=1.4,
            rx=10.0,
            ry=10.0,
            fill='none',
        ),
        RectSlot(
            id='slot.na',
            prompt='',
            x=162.0,
            y=66.0,
            width=64.0,
            height=64.0,
            stroke='#4A4A4A',
            stroke_width=2.0,
            fill='none',
        ),
        PolygonSlot(
            id='slot.ga',
            prompt='',
            points=((26.0, 69.0), (106.0, 67.0), (84.0, 108.0), (36.0, 120.0)),
            stroke='#4A4A4A',
            stroke_width=2.0,
            fill='none',
        ),
        RectSlot(
            id='slot.da',
            prompt='',
            x=284.0,
            y=77.0,
            width=80.0,
            height=52.0,
            stroke='#4A4A4A',
            stroke_width=2.0,
            fill='none',
        ),
        TextSlot(
            id='slot.ga_t',
            prompt='',
            text='가',
            style_role='body',
            x=58.0,
            y=96.0,
            font_size=32,
            font_family='Malgun Gothic',
            anchor='middle',
            fill='#222222',
        ),
        TextSlot(
            id='slot.na_t',
            prompt='',
            text='나',
            style_role='body',
            x=194.0,
            y=106.0,
            font_size=32,
            font_family='Malgun Gothic',
            anchor='middle',
            fill='#222222',
        ),
        TextSlot(
            id='slot.da_t',
            prompt='',
            text='다',
            style_role='body',
            x=324.0,
            y=106.0,
            font_size=32,
            font_family='Malgun Gothic',
            anchor='middle',
            fill='#222222',
        ),
        PolygonSlot(
            id='slot.ra',
            prompt='',
            points=((56.0, 134.0), (100.0, 170.0), (56.0, 206.0), (12.0, 170.0)),
            stroke='#4A4A4A',
            stroke_width=2.0,
            fill='none',
        ),
        PolygonSlot(
            id='slot.ba',
            prompt='',
            points=((328.0, 150.0), (371.0, 174.0), (328.0, 198.0), (285.0, 174.0)),
            stroke='#4A4A4A',
            stroke_width=2.0,
            fill='none',
        ),
        RectSlot(
            id='slot.ma',
            prompt='',
            x=136.0,
            y=154.0,
            width=116.0,
            height=42.0,
            stroke='#4A4A4A',
            stroke_width=2.0,
            fill='none',
        ),
        TextSlot(
            id='slot.ra_t',
            prompt='',
            text='라',
            style_role='body',
            x=56.0,
            y=184.0,
            font_size=32,
            font_family='Malgun Gothic',
            anchor='middle',
            fill='#222222',
        ),
        TextSlot(
            id='slot.ma_t',
            prompt='',
            text='마',
            style_role='body',
            x=194.0,
            y=184.0,
            font_size=32,
            font_family='Malgun Gothic',
            anchor='middle',
            fill='#222222',
        ),
        TextSlot(
            id='slot.ba_t',
            prompt='',
            text='바',
            style_role='body',
            x=328.0,
            y=186.0,
            font_size=32,
            font_family='Malgun Gothic',
            anchor='middle',
            fill='#222222',
        ),
        RectSlot(
            id='slot.answer_value',
            prompt='',
            x=304.0,
            y=212.0,
            width=48.0,
            height=28.0,
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
        id='0008_사각형과 정사각형',
        title='',
        canvas=canvas,
        regions=regions,
        slots=slots,
        diagrams=diagrams,
        groups=groups,
        constraints=constraints,
    )

PROBLEM_TEMPLATE = build_problem_template()
