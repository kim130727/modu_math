from __future__ import annotations

from modu_math.dsl import Arrow, BlankSlot, Canvas, ChoiceSlot, Circle, CircleSlot, Constraint, Cube, DiagramTemplate, FractionAreaModel, Grid, Group, LabelSlot, LineSlot, PathSlot, PolygonSlot, ProblemTemplate, RectSlot, Region, ShapeObject, TextSlot, Triangle

def build_problem_template() -> ProblemTemplate:
    canvas = Canvas(
        width=400,
        height=230,
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
            height=230.0,
            stroke='none',
            stroke_width=0.0,
            fill='#F6F6F6',
        ),
        TextSlot(
            id='slot.i1',
            prompt='',
            text='색종이를 점선을 따라 자르면 직각삼각형은 모두',
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
            text='몇 개 만들어지는지 구하세요.',
            style_role='body',
            x=4.0,
            y=64.0,
            font_size=17,
            font_family='Malgun Gothic',
            anchor='middle',
            fill='#222222',
        ),
        RectSlot(
            id='slot.paper',
            prompt='',
            x=110.0,
            y=82.0,
            width=175.0,
            height=120.0,
            stroke='#6A6A6A',
            stroke_width=1.8,
            fill='#EEF4C8',
        ),
        RectSlot(
            id='slot.answer_value',
            prompt='',
            x=343.0,
            y=196.0,
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
        id='0007_삼각형 개수',
        title='',
        canvas=canvas,
        regions=regions,
        slots=slots,
        diagrams=diagrams,
        groups=groups,
        constraints=constraints,
    )

PROBLEM_TEMPLATE = build_problem_template()
