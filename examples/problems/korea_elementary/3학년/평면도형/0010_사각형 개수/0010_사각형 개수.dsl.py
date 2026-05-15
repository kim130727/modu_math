from __future__ import annotations

from modu_math.dsl import Arrow, BlankSlot, Canvas, ChoiceSlot, Circle, CircleSlot, Constraint, Cube, DiagramTemplate, FractionAreaModel, Grid, Group, LabelSlot, LineSlot, PathSlot, PolygonSlot, ProblemTemplate, RectSlot, Region, ShapeObject, TextSlot, Triangle

def build_problem_template() -> ProblemTemplate:
    canvas = Canvas(
        width=400,
        height=210,
        coordinate_mode='logical',
    )
    regions = (
        Region(
            id='region.stem',
            role='stem',
            flow='vertical',
            slot_ids=('slot.i1', 'slot.i2'),
        ),
    )
    slots = (
        RectSlot(
            id='slot.bg',
            prompt='',
            x=0.0,
            y=0.0,
            width=400.0,
            height=210.0,
            stroke='none',
            stroke_width=0.0,
            fill='#F4F4F4',
        ),
        TextSlot(
            id='slot.i1',
            prompt='',
            text='다음 도형에서 찾을 수 있는 크고 작은',
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
            text='직사각형은 모두 몇 개인지 구하세요.',
            style_role='body',
            x=4.0,
            y=64.0,
            font_size=17,
            font_family='Malgun Gothic',
            anchor='middle',
            fill='#222222',
        ),
        RectSlot(
            id='slot.outer',
            prompt='',
            x=148.0,
            y=104.0,
            width=126.0,
            height=96.0,
            stroke='#4A4A4A',
            stroke_width=2.0,
            fill='none',
        ),
        LineSlot(
            id='slot.v1',
            prompt='',
            x1=190.0,
            y1=104.0,
            x2=190.0,
            y2=200.0,
            stroke='#4A4A4A',
            stroke_width=2.0,
        ),
        LineSlot(
            id='slot.v2',
            prompt='',
            x1=224.0,
            y1=104.0,
            x2=224.0,
            y2=200.0,
            stroke='#4A4A4A',
            stroke_width=2.0,
        ),
        LineSlot(
            id='slot.h1',
            prompt='',
            x1=148.0,
            y1=152.0,
            x2=224.0,
            y2=152.0,
            stroke='#4A4A4A',
            stroke_width=2.0,
        ),
        RectSlot(
            id='slot.answer_value',
            prompt='',
            x=336.0,
            y=176.0,
            width=56.0,
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
        id='0010_사각형 개수',
        title='',
        canvas=canvas,
        regions=regions,
        slots=slots,
        diagrams=diagrams,
        groups=groups,
        constraints=constraints,
    )

PROBLEM_TEMPLATE = build_problem_template()
