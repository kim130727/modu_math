from __future__ import annotations

from modu_math.dsl import Arrow, BlankSlot, Canvas, ChoiceSlot, Circle, CircleSlot, Constraint, Cube, DiagramTemplate, FractionAreaModel, Grid, Group, LabelSlot, LineSlot, PathSlot, PolygonSlot, ProblemTemplate, RectSlot, Region, ShapeObject, TextSlot, Triangle

def build_problem_template() -> ProblemTemplate:
    canvas = Canvas(
        width=400,
        height=220,
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
            height=220.0,
            stroke='none',
            stroke_width=0.0,
            fill='#F4F4F4',
        ),
        TextSlot(
            id='slot.i1',
            prompt='',
            text='다음 도형에서 찾을 수 있는 직각은 모두 몇',
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
            text='개인지 구하세요.',
            style_role='body',
            x=4.0,
            y=64.0,
            font_size=17,
            font_family='Malgun Gothic',
            anchor='middle',
            fill='#222222',
        ),
        RectSlot(
            id='slot.answer_value',
            prompt='',
            x=344.0,
            y=186.0,
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
        id='0006_직각의 개수',
        title='',
        canvas=canvas,
        regions=regions,
        slots=slots,
        diagrams=diagrams,
        groups=groups,
        constraints=constraints,
    )

PROBLEM_TEMPLATE = build_problem_template()
