from __future__ import annotations

from modu_math.dsl import Arrow, BlankSlot, Canvas, ChoiceSlot, Circle, CircleSlot, Constraint, Cube, DiagramTemplate, FractionAreaModel, Grid, Group, LabelSlot, LineSlot, PathSlot, PolygonSlot, ProblemTemplate, RectSlot, Region, ShapeObject, TextSlot, Triangle

def build_problem_template() -> ProblemTemplate:
    canvas = Canvas(
        width=1280,
        height=720,
        coordinate_mode='logical',
    )
    regions = (
        Region(
            id='region.stem',
            role='stem',
            flow='vertical',
            slot_ids=('slot.instruction', 'slot.equation'),
        ),
    )
    slots = (
        TextSlot(
            id='slot.instruction',
            prompt='',
            text='□안에 알맞은 수를 구하시오.',
            style_role='body',
            x=72.0,
            y=92.0,
            font_size=42,
            font_family='Malgun Gothic',
            anchor='start',
            fill='#000000',
            semantic_role='instruction',
        ),
        RectSlot(
            id='slot.question_box',
            prompt='',
            x=280.0,
            y=240.0,
            width=720.0,
            height=180.0,
            stroke='#000000',
            stroke_width=3.0,
            rx=24.0,
            fill='none',
            semantic_role='question_container',
        ),
        TextSlot(
            id='slot.equation',
            prompt='',
            text='410초=6분 □초',
            style_role='body',
            x=640.0,
            y=345.0,
            font_size=54,
            font_family='Malgun Gothic',
            anchor='middle',
            fill='#000000',
            semantic_role='equation',
        ),
    )
    diagrams = (
    )
    groups = (
    )
    constraints = (
    )
    return ProblemTemplate(
        id='0001_직각의 개수',
        title='',
        canvas=canvas,
        regions=regions,
        slots=slots,
        diagrams=diagrams,
        groups=groups,
        constraints=constraints,
    )

PROBLEM_TEMPLATE = build_problem_template()
