from __future__ import annotations

from modu_math.dsl import Arrow, BlankSlot, Canvas, ChoiceSlot, Circle, CircleSlot, Constraint, Cube, DiagramTemplate, FractionAreaModel, Grid, Group, LabelSlot, LineSlot, PathSlot, PolygonSlot, ProblemTemplate, RectSlot, Region, ShapeObject, TextSlot, Triangle

def build_problem_template() -> ProblemTemplate:
    canvas = Canvas(
        width=768,
        height=667,
        coordinate_mode='logical',
    )
    regions = (
        Region(
            id='region.stem',
            role='stem',
            flow='vertical',
            slot_ids=('slot.instruction_1',
             'slot.instruction_2',
             'slot.instruction_3',
             'slot.label_choice_2',
             'slot.label_choice_3',
             'slot.label_choice_4',
             'slot.label_choice_1',
             'slot.label_choice_5',
             'slot.label_base_start',
             'slot.label_base_end'),
        ),
    )
    slots = (
        RectSlot(
            id='slot.bg',
            prompt='',
            x=0.0,
            y=0.0,
            width=768.0,
            height=667.0,
            stroke='none',
            stroke_width=0.0,
            fill='#F4F4F4',
            semantic_role='background',
        ),
        TextSlot(
            id='slot.instruction_1',
            prompt='',
            text='선분 ㄱㄴ을 변으로 하는 직각삼각형을',
            style_role='body',
            x=24.0,
            y=58.0,
            font_size=34,
            font_family='Malgun Gothic',
            anchor='start',
            fill='#222222',
            semantic_role='instruction',
        ),
        TextSlot(
            id='slot.instruction_2',
            prompt='',
            text='그리고 싶습니다. 이을 점을 찾아 선을',
            style_role='body',
            x=24.0,
            y=100.0,
            font_size=34,
            font_family='Malgun Gothic',
            anchor='start',
            fill='#222222',
            semantic_role='instruction',
        ),
        TextSlot(
            id='slot.instruction_3',
            prompt='',
            text='긋고, 직각삼각형을 완성해 보세요.',
            style_role='body',
            x=24.0,
            y=142.0,
            font_size=34,
            font_family='Malgun Gothic',
            anchor='start',
            fill='#222222',
            semantic_role='instruction',
        ),
        RectSlot(
            id='slot.grid_box',
            prompt='',
            x=58.0,
            y=180.0,
            width=640.0,
            height=320.0,
            stroke='#9CA3AF',
            stroke_width=2.0,
            fill='none',
            semantic_role='guide',
        ),
        LineSlot(
            id='slot.grid_h_00',
            prompt='',
            x1=58.0,
            y1=180.0,
            x2=698.0,
            y2=180.0,
            stroke='#9CA3AF',
            stroke_width=1.0,
            semantic_role='guide',
        ),
        LineSlot(
            id='slot.grid_v_00',
            prompt='',
            x1=58.0,
            y1=180.0,
            x2=58.0,
            y2=500.0,
            stroke='#9CA3AF',
            stroke_width=1.0,
            semantic_role='guide',
        ),
        LineSlot(
            id='slot.grid_v_01',
            prompt='',
            x1=98.0,
            y1=180.0,
            x2=98.0,
            y2=500.0,
            stroke='#9CA3AF',
            stroke_width=1.0,
            semantic_role='guide',
        ),
        LineSlot(
            id='slot.grid_v_02',
            prompt='',
            x1=138.0,
            y1=180.0,
            x2=138.0,
            y2=500.0,
            stroke='#9CA3AF',
            stroke_width=1.0,
            semantic_role='guide',
        ),
        LineSlot(
            id='slot.grid_v_03',
            prompt='',
            x1=178.0,
            y1=180.0,
            x2=178.0,
            y2=500.0,
            stroke='#9CA3AF',
            stroke_width=1.0,
            semantic_role='guide',
        ),
        LineSlot(
            id='slot.grid_v_04',
            prompt='',
            x1=218.0,
            y1=180.0,
            x2=218.0,
            y2=500.0,
            stroke='#9CA3AF',
            stroke_width=1.0,
            semantic_role='guide',
        ),
        LineSlot(
            id='slot.grid_v_05',
            prompt='',
            x1=258.0,
            y1=180.0,
            x2=258.0,
            y2=500.0,
            stroke='#9CA3AF',
            stroke_width=1.0,
            semantic_role='guide',
        ),
        LineSlot(
            id='slot.grid_v_06',
            prompt='',
            x1=298.0,
            y1=180.0,
            x2=298.0,
            y2=500.0,
            stroke='#9CA3AF',
            stroke_width=1.0,
            semantic_role='guide',
        ),
        LineSlot(
            id='slot.grid_v_07',
            prompt='',
            x1=338.0,
            y1=180.0,
            x2=338.0,
            y2=500.0,
            stroke='#9CA3AF',
            stroke_width=1.0,
            semantic_role='guide',
        ),
        LineSlot(
            id='slot.grid_v_08',
            prompt='',
            x1=378.0,
            y1=180.0,
            x2=378.0,
            y2=500.0,
            stroke='#9CA3AF',
            stroke_width=1.0,
            semantic_role='guide',
        ),
        LineSlot(
            id='slot.grid_v_09',
            prompt='',
            x1=418.0,
            y1=180.0,
            x2=418.0,
            y2=500.0,
            stroke='#9CA3AF',
            stroke_width=1.0,
            semantic_role='guide',
        ),
        LineSlot(
            id='slot.grid_v_10',
            prompt='',
            x1=458.0,
            y1=180.0,
            x2=458.0,
            y2=500.0,
            stroke='#9CA3AF',
            stroke_width=1.0,
            semantic_role='guide',
        ),
        LineSlot(
            id='slot.grid_v_11',
            prompt='',
            x1=498.0,
            y1=180.0,
            x2=498.0,
            y2=500.0,
            stroke='#9CA3AF',
            stroke_width=1.0,
            semantic_role='guide',
        ),
        LineSlot(
            id='slot.grid_v_12',
            prompt='',
            x1=538.0,
            y1=180.0,
            x2=538.0,
            y2=500.0,
            stroke='#9CA3AF',
            stroke_width=1.0,
            semantic_role='guide',
        ),
        LineSlot(
            id='slot.grid_v_13',
            prompt='',
            x1=578.0,
            y1=180.0,
            x2=578.0,
            y2=500.0,
            stroke='#9CA3AF',
            stroke_width=1.0,
            semantic_role='guide',
        ),
        LineSlot(
            id='slot.grid_v_14',
            prompt='',
            x1=618.0,
            y1=180.0,
            x2=618.0,
            y2=500.0,
            stroke='#9CA3AF',
            stroke_width=1.0,
            semantic_role='guide',
        ),
        LineSlot(
            id='slot.grid_v_15',
            prompt='',
            x1=658.0,
            y1=180.0,
            x2=658.0,
            y2=500.0,
            stroke='#9CA3AF',
            stroke_width=1.0,
            semantic_role='guide',
        ),
        LineSlot(
            id='slot.grid_v_16',
            prompt='',
            x1=698.0,
            y1=180.0,
            x2=698.0,
            y2=500.0,
            stroke='#9CA3AF',
            stroke_width=1.0,
            semantic_role='guide',
        ),
        LineSlot(
            id='slot.grid_h_01',
            prompt='',
            x1=58.0,
            y1=220.0,
            x2=698.0,
            y2=220.0,
            stroke='#9CA3AF',
            stroke_width=1.0,
            semantic_role='guide',
        ),
        TextSlot(
            id='slot.label_choice_2',
            prompt='',
            text='ㄹ',
            style_role='body',
            x=306.0,
            y=251.0,
            font_size=34,
            font_family='Malgun Gothic',
            anchor='start',
            fill='#222222',
            semantic_role='label',
        ),
        TextSlot(
            id='slot.label_choice_3',
            prompt='',
            text='ㅁ',
            style_role='body',
            x=385.0,
            y=251.0,
            font_size=34,
            font_family='Malgun Gothic',
            anchor='start',
            fill='#222222',
            semantic_role='label',
        ),
        TextSlot(
            id='slot.label_choice_4',
            prompt='',
            text='ㅂ',
            style_role='body',
            x=587.0,
            y=251.0,
            font_size=34,
            font_family='Malgun Gothic',
            anchor='start',
            fill='#222222',
            semantic_role='label',
        ),
        CircleSlot(
            id='slot.dot_choice_2',
            prompt='',
            cx=298.0,
            cy=259.0,
            r=5.0,
            stroke='none',
            stroke_width=0.0,
            fill='#222222',
            semantic_role='point',
        ),
        CircleSlot(
            id='slot.dot_choice_3',
            prompt='',
            cx=377.0,
            cy=259.0,
            r=5.0,
            stroke='none',
            stroke_width=0.0,
            fill='#222222',
            semantic_role='point',
        ),
        CircleSlot(
            id='slot.dot_choice_4',
            prompt='',
            cx=579.0,
            cy=259.0,
            r=5.0,
            stroke='none',
            stroke_width=0.0,
            fill='#222222',
            semantic_role='point',
        ),
        LineSlot(
            id='slot.grid_h_02',
            prompt='',
            x1=58.0,
            y1=260.0,
            x2=698.0,
            y2=260.0,
            stroke='#9CA3AF',
            stroke_width=1.0,
            semantic_role='guide',
        ),
        TextSlot(
            id='slot.label_choice_1',
            prompt='',
            text='ㄷ',
            style_role='body',
            x=186.0,
            y=292.0,
            font_size=34,
            font_family='Malgun Gothic',
            anchor='start',
            fill='#222222',
            semantic_role='label',
        ),
        LineSlot(
            id='slot.grid_h_03',
            prompt='',
            x1=58.0,
            y1=300.0,
            x2=698.0,
            y2=300.0,
            stroke='#9CA3AF',
            stroke_width=1.0,
            semantic_role='guide',
        ),
        CircleSlot(
            id='slot.dot_choice_1',
            prompt='',
            cx=178.0,
            cy=300.0,
            r=5.0,
            stroke='none',
            stroke_width=0.0,
            fill='#222222',
            semantic_role='point',
        ),
        TextSlot(
            id='slot.label_choice_5',
            prompt='',
            text='ㅅ',
            style_role='body',
            x=627.0,
            y=331.0,
            font_size=34,
            font_family='Malgun Gothic',
            anchor='start',
            fill='#222222',
            semantic_role='label',
        ),
        CircleSlot(
            id='slot.dot_choice_5',
            prompt='',
            cx=619.0,
            cy=339.0,
            r=5.0,
            stroke='none',
            stroke_width=0.0,
            fill='#222222',
            semantic_role='point',
        ),
        LineSlot(
            id='slot.grid_h_04',
            prompt='',
            x1=58.0,
            y1=340.0,
            x2=698.0,
            y2=340.0,
            stroke='#9CA3AF',
            stroke_width=1.0,
            semantic_role='guide',
        ),
        LineSlot(
            id='slot.grid_h_05',
            prompt='',
            x1=58.0,
            y1=380.0,
            x2=698.0,
            y2=380.0,
            stroke='#9CA3AF',
            stroke_width=1.0,
            semantic_role='guide',
        ),
        LineSlot(
            id='slot.grid_h_06',
            prompt='',
            x1=58.0,
            y1=420.0,
            x2=698.0,
            y2=420.0,
            stroke='#9CA3AF',
            stroke_width=1.0,
            semantic_role='guide',
        ),
        TextSlot(
            id='slot.label_base_start',
            prompt='',
            text='ㄱ',
            style_role='body',
            x=265.0,
            y=451.0,
            font_size=34,
            font_family='Malgun Gothic',
            anchor='start',
            fill='#222222',
            semantic_role='label',
        ),
        TextSlot(
            id='slot.label_base_end',
            prompt='',
            text='ㄴ',
            style_role='body',
            x=587.0,
            y=451.0,
            font_size=34,
            font_family='Malgun Gothic',
            anchor='start',
            fill='#222222',
            semantic_role='label',
        ),
        LineSlot(
            id='slot.base_segment',
            prompt='',
            x1=257.0,
            y1=459.0,
            x2=579.0,
            y2=459.0,
            stroke='#222222',
            stroke_width=4.0,
            semantic_role='given_segment',
        ),
        CircleSlot(
            id='slot.dot_base_start',
            prompt='',
            cx=257.0,
            cy=459.0,
            r=5.0,
            stroke='none',
            stroke_width=0.0,
            fill='#222222',
            semantic_role='point',
        ),
        CircleSlot(
            id='slot.dot_base_end',
            prompt='',
            cx=579.0,
            cy=459.0,
            r=5.0,
            stroke='none',
            stroke_width=0.0,
            fill='#222222',
            semantic_role='point',
        ),
        LineSlot(
            id='slot.grid_h_07',
            prompt='',
            x1=58.0,
            y1=460.0,
            x2=698.0,
            y2=460.0,
            stroke='#9CA3AF',
            stroke_width=1.0,
            semantic_role='guide',
        ),
        LineSlot(
            id='slot.grid_h_08',
            prompt='',
            x1=58.0,
            y1=500.0,
            x2=698.0,
            y2=500.0,
            stroke='#9CA3AF',
            stroke_width=1.0,
            semantic_role='guide',
        ),
        RectSlot(
            id='slot.answer_point',
            prompt='',
            x=640.0,
            y=611.0,
            width=60.0,
            height=42.0,
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
        id='0002_직각 삼각형 개수',
        title='',
        canvas=canvas,
        regions=regions,
        slots=slots,
        diagrams=diagrams,
        groups=groups,
        constraints=constraints,
    )

PROBLEM_TEMPLATE = build_problem_template()
