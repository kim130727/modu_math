from __future__ import annotations

from modu_math.dsl import Arrow, BlankSlot, Canvas, ChoiceSlot, Circle, CircleSlot, Constraint, Cube, DiagramTemplate, FractionAreaModel, Grid, Group, LabelSlot, LineSlot, PathSlot, PolygonSlot, ProblemTemplate, RectSlot, Region, ShapeObject, TextSlot, Triangle

def build_problem_template() -> ProblemTemplate:
    canvas = Canvas(
        width=440,
        height=361,
        coordinate_mode='logical',
    )
    regions = (
        Region(
            id='region.stem',
            role='stem',
            flow='vertical',
            slot_ids=('slot.instruction_1',
             'slot.instruction_2',
             'slot.choice_key_㉠',
             'slot.choice_key_㉡',
             'slot.choice_key_㉢',
             'slot.choice_key_㉣',
             'slot.answer_left_paren',
             'slot.answer_right_paren'),
        ),
    )
    slots = (
        RectSlot(
            id='slot.bg',
            prompt='',
            x=0.0,
            y=0.0,
            width=440.0,
            height=361.0,
            stroke='none',
            stroke_width=0.0,
            fill='#F4F4F4',
            semantic_role='background',
        ),
        TextSlot(
            id='slot.instruction_1',
            prompt='',
            text='도형의 이름으로 알맞은 것을 모두 찾아 기호를',
            style_role='body',
            x=4.0,
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
            text='쓰시오.',
            style_role='body',
            x=4.0,
            y=65.0,
            font_size=17,
            font_family='Malgun Gothic',
            anchor='start',
            fill='#222222',
            semantic_role='instruction',
        ),
        RectSlot(
            id='slot.grid_box',
            prompt='',
            x=149.0,
            y=78.0,
            width=110.0,
            height=110.0,
            stroke='#767676',
            stroke_width=1.2,
            fill='none',
            semantic_role='guide',
        ),
        LineSlot(
            id='slot.grid_h_0',
            prompt='',
            x1=149.0,
            y1=78.0,
            x2=259.0,
            y2=78.0,
            stroke='#767676',
            stroke_width=1.2,
            semantic_role='guide',
        ),
        LineSlot(
            id='slot.grid_v_0',
            prompt='',
            x1=149.0,
            y1=78.0,
            x2=149.0,
            y2=188.0,
            stroke='#767676',
            stroke_width=1.2,
            semantic_role='guide',
        ),
        LineSlot(
            id='slot.grid_v_1',
            prompt='',
            x1=171.0,
            y1=78.0,
            x2=171.0,
            y2=188.0,
            stroke='#767676',
            stroke_width=1.2,
            semantic_role='guide',
        ),
        LineSlot(
            id='slot.grid_v_2',
            prompt='',
            x1=193.0,
            y1=78.0,
            x2=193.0,
            y2=188.0,
            stroke='#767676',
            stroke_width=1.2,
            semantic_role='guide',
        ),
        LineSlot(
            id='slot.grid_v_3',
            prompt='',
            x1=215.0,
            y1=78.0,
            x2=215.0,
            y2=188.0,
            stroke='#767676',
            stroke_width=1.2,
            semantic_role='guide',
        ),
        LineSlot(
            id='slot.grid_v_4',
            prompt='',
            x1=237.0,
            y1=78.0,
            x2=237.0,
            y2=188.0,
            stroke='#767676',
            stroke_width=1.2,
            semantic_role='guide',
        ),
        LineSlot(
            id='slot.grid_v_5',
            prompt='',
            x1=259.0,
            y1=78.0,
            x2=259.0,
            y2=188.0,
            stroke='#767676',
            stroke_width=1.2,
            semantic_role='guide',
        ),
        LineSlot(
            id='slot.grid_h_1',
            prompt='',
            x1=149.0,
            y1=100.0,
            x2=259.0,
            y2=100.0,
            stroke='#767676',
            stroke_width=1.2,
            semantic_role='guide',
        ),
        RectSlot(
            id='slot.target_shape',
            prompt='',
            x=171.0,
            y=100.0,
            width=66.0,
            height=66.0,
            stroke='#2D2D2D',
            stroke_width=3.0,
            fill='none',
            semantic_role='shape',
        ),
        LineSlot(
            id='slot.grid_h_2',
            prompt='',
            x1=149.0,
            y1=122.0,
            x2=259.0,
            y2=122.0,
            stroke='#767676',
            stroke_width=1.2,
            semantic_role='guide',
        ),
        LineSlot(
            id='slot.grid_h_3',
            prompt='',
            x1=149.0,
            y1=144.0,
            x2=259.0,
            y2=144.0,
            stroke='#767676',
            stroke_width=1.2,
            semantic_role='guide',
        ),
        LineSlot(
            id='slot.grid_h_4',
            prompt='',
            x1=149.0,
            y1=166.0,
            x2=259.0,
            y2=166.0,
            stroke='#767676',
            stroke_width=1.2,
            semantic_role='guide',
        ),
        LineSlot(
            id='slot.grid_h_5',
            prompt='',
            x1=149.0,
            y1=188.0,
            x2=259.0,
            y2=188.0,
            stroke='#767676',
            stroke_width=1.2,
            semantic_role='guide',
        ),
        RectSlot(
            id='slot.choice_box',
            prompt='',
            x=4.0,
            y=213.0,
            width=399.0,
            height=88.0,
            stroke='#6D6D6D',
            stroke_width=1.8,
            rx=12.0,
            ry=12.0,
            fill='none',
            semantic_role='guide',
        ),
        TextSlot(
            id='slot.choice_key_㉠',
            prompt='',
            text='㉠ 직사각형',
            style_role='body',
            x=20.0,
            y=248.0,
            font_size=17,
            font_family='Malgun Gothic',
            anchor='start',
            fill='#222222',
            semantic_role='choice',
        ),
        TextSlot(
            id='slot.choice_key_㉡',
            prompt='',
            text='㉡ 사각형',
            style_role='body',
            x=206.0,
            y=248.0,
            font_size=17,
            font_family='Malgun Gothic',
            anchor='start',
            fill='#222222',
            semantic_role='choice',
        ),
        TextSlot(
            id='slot.choice_key_㉢',
            prompt='',
            text='㉢ 직각삼각형',
            style_role='body',
            x=20.0,
            y=280.0,
            font_size=17,
            font_family='Malgun Gothic',
            anchor='start',
            fill='#222222',
            semantic_role='choice',
        ),
        TextSlot(
            id='slot.choice_key_㉣',
            prompt='',
            text='㉣ 정사각형',
            style_role='body',
            x=206.0,
            y=280.0,
            font_size=17,
            font_family='Malgun Gothic',
            anchor='start',
            fill='#222222',
            semantic_role='choice',
        ),
        RectSlot(
            id='slot.answer_blank',
            prompt='',
            x=188.0,
            y=318.0,
            width=188.0,
            height=34.0,
            stroke='none',
            stroke_width=0.0,
            fill='none',
            semantic_role='answer_anchor',
        ),
        TextSlot(
            id='slot.answer_left_paren',
            prompt='',
            text='(',
            style_role='body',
            x=170.0,
            y=345.0,
            font_size=44,
            font_family='Malgun Gothic',
            anchor='start',
            fill='#222222',
            semantic_role='guide',
        ),
        TextSlot(
            id='slot.answer_right_paren',
            prompt='',
            text=')',
            style_role='body',
            x=394.0,
            y=345.0,
            font_size=44,
            font_family='Malgun Gothic',
            anchor='start',
            fill='#222222',
            semantic_role='guide',
        ),
    )
    diagrams = (
    )
    groups = (
    )
    constraints = (
    )
    return ProblemTemplate(
        id='0003_각 이름 쓰기',
        title='',
        canvas=canvas,
        regions=regions,
        slots=slots,
        diagrams=diagrams,
        groups=groups,
        constraints=constraints,
    )

PROBLEM_TEMPLATE = build_problem_template()
