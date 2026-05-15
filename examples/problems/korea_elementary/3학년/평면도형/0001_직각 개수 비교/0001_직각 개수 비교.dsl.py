from __future__ import annotations

from modu_math.dsl import Arrow, BlankSlot, Canvas, ChoiceSlot, Circle, CircleSlot, Constraint, Cube, DiagramTemplate, FractionAreaModel, Grid, Group, LabelSlot, LineSlot, PathSlot, PolygonSlot, ProblemTemplate, RectSlot, Region, ShapeObject, TextSlot, Triangle

def build_problem_template() -> ProblemTemplate:
    canvas = Canvas(
        width=411,
        height=279,
        coordinate_mode='logical',
    )
    regions = (
        Region(
            id='region.stem',
            role='stem',
            flow='vertical',
            slot_ids=('slot.instruction_1',
             'slot.instruction_2',
             'slot.label_text_ㄴ',
             'slot.label_text_ㄱ',
             'slot.label_text_ㄷ',
             'slot.label_text_ㄹ'),
        ),
    )
    slots = (
        RectSlot(
            id='slot.bg',
            prompt='',
            x=0.0,
            y=0.0,
            width=411.0,
            height=279.0,
            stroke='none',
            stroke_width=0.0,
            fill='#F4F4F4',
            semantic_role='background',
        ),
        RectSlot(
            id='slot.answer_most',
            prompt='',
            x=342.0,
            y=16.0,
            width=24.0,
            height=24.0,
            stroke='none',
            stroke_width=0.0,
            fill='none',
            semantic_role='answer_anchor',
        ),
        RectSlot(
            id='slot.answer_least',
            prompt='',
            x=374.0,
            y=16.0,
            width=24.0,
            height=24.0,
            stroke='none',
            stroke_width=0.0,
            fill='none',
            semantic_role='answer_anchor',
        ),
        TextSlot(
            id='slot.instruction_1',
            prompt='',
            text='직각이 가장 많은 도형과 가장 적은 도형을',
            style_role='body',
            x=10.0,
            y=33.0,
            font_size=17,
            font_family='Malgun Gothic',
            anchor='start',
            fill='#222222',
            semantic_role='instruction',
        ),
        TextSlot(
            id='slot.instruction_2',
            prompt='',
            text='찾아 차례로 기호를 쓰세요.',
            style_role='body',
            x=10.0,
            y=65.0,
            font_size=17,
            font_family='Malgun Gothic',
            anchor='start',
            fill='#222222',
            semantic_role='instruction',
        ),
        RectSlot(
            id='slot.problem_frame',
            prompt='',
            x=10.0,
            y=74.0,
            width=391.0,
            height=194.0,
            stroke='#7A7A7A',
            stroke_width=1.3,
            rx=10.0,
            ry=10.0,
            fill='none',
            semantic_role='guide',
        ),
        CircleSlot(
            id='slot.label_circle_ㄴ',
            prompt='',
            cx=214.0,
            cy=100.0,
            r=8.0,
            stroke='#666666',
            stroke_width=1.6,
            fill='none',
            semantic_role='label_marker',
        ),
        CircleSlot(
            id='slot.label_circle_ㄱ',
            prompt='',
            cx=35.0,
            cy=101.0,
            r=8.0,
            stroke='#666666',
            stroke_width=1.6,
            fill='none',
            semantic_role='label_marker',
        ),
        TextSlot(
            id='slot.label_text_ㄴ',
            prompt='',
            text='ㄴ',
            style_role='body',
            x=214.0,
            y=105.0,
            font_size=14,
            font_family='Malgun Gothic',
            anchor='middle',
            fill='#555555',
            semantic_role='label',
        ),
        TextSlot(
            id='slot.label_text_ㄱ',
            prompt='',
            text='ㄱ',
            style_role='body',
            x=35.0,
            y=106.0,
            font_size=14,
            font_family='Malgun Gothic',
            anchor='middle',
            fill='#555555',
            semantic_role='label',
        ),
        CircleSlot(
            id='slot.label_circle_ㄷ',
            prompt='',
            cx=35.0,
            cy=199.0,
            r=8.0,
            stroke='#666666',
            stroke_width=1.6,
            fill='none',
            semantic_role='label_marker',
        ),
        CircleSlot(
            id='slot.label_circle_ㄹ',
            prompt='',
            cx=214.0,
            cy=199.0,
            r=8.0,
            stroke='#666666',
            stroke_width=1.6,
            fill='none',
            semantic_role='label_marker',
        ),
        TextSlot(
            id='slot.label_text_ㄷ',
            prompt='',
            text='ㄷ',
            style_role='body',
            x=35.0,
            y=204.0,
            font_size=14,
            font_family='Malgun Gothic',
            anchor='middle',
            fill='#555555',
            semantic_role='label',
        ),
        TextSlot(
            id='slot.label_text_ㄹ',
            prompt='',
            text='ㄹ',
            style_role='body',
            x=214.0,
            y=204.0,
            font_size=14,
            font_family='Malgun Gothic',
            anchor='middle',
            fill='#555555',
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
        id='0001_직각 개수 비교',
        title='',
        canvas=canvas,
        regions=regions,
        slots=slots,
        diagrams=diagrams,
        groups=groups,
        constraints=constraints,
    )

PROBLEM_TEMPLATE = build_problem_template()
