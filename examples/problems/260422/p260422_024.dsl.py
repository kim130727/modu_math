from __future__ import annotations

from modu_math.dsl import Arrow, BlankSlot, Canvas, ChoiceSlot, Circle, CircleSlot, Constraint, Cube, DiagramTemplate, FractionAreaModel, Grid, Group, LabelSlot, LineSlot, PathSlot, PolygonSlot, ProblemTemplate, RectSlot, Region, ShapeObject, TextSlot, Triangle

def build_problem_template() -> ProblemTemplate:
    canvas = Canvas(
        width=400,
        height=150,
        coordinate_mode='logical',
    )
    regions = (
        Region(
            id='region.stem',
            role='stem',
            flow='absolute',
            slot_ids=('slot.frac1.num',
             'slot.frac1.bar',
             'slot.frac1.den',
             'slot.text.div',
             'slot.frac2.num',
             'slot.frac2.bar',
             'slot.frac2.den'),
        ),
    )
    slots = (
        TextSlot(
            id='slot.frac1.num',
            prompt='',
            text='5',
            style_role='body',
            x=60.0,
            y=63.0,
            font_size=35,
            anchor='middle',
            fill='#000000',
        ),
        LineSlot(
            id='slot.frac1.bar',
            prompt='',
            x1=37.5,
            y1=75.0,
            x2=82.5,
            y2=75.0,
            stroke='#000000',
            stroke_width=2.0,
        ),
        TextSlot(
            id='slot.frac1.den',
            prompt='',
            text='8',
            style_role='body',
            x=60.0,
            y=112.0,
            font_size=35,
            anchor='middle',
            fill='#000000',
        ),
        TextSlot(
            id='slot.text.div',
            prompt='',
            text='÷',
            style_role='body',
            x=114.18103046331466,
            y=87.96615957523379,
            font_size=35,
            fill='#000000',
        ),
        TextSlot(
            id='slot.frac2.num',
            prompt='',
            text='2',
            style_role='body',
            x=190.0,
            y=63.0,
            font_size=35,
            anchor='middle',
            fill='#000000',
        ),
        LineSlot(
            id='slot.frac2.bar',
            prompt='',
            x1=167.5,
            y1=75.0,
            x2=212.5,
            y2=75.0,
            stroke='#000000',
            stroke_width=2.0,
        ),
        TextSlot(
            id='slot.frac2.den',
            prompt='',
            text='8',
            style_role='body',
            x=190.0,
            y=112.0,
            font_size=35,
            anchor='middle',
            fill='#000000',
        ),
    )
    diagrams = (
    )
    groups = (
    )
    constraints = (
    )
    return ProblemTemplate(
        id='msedge_ZcKjwaG2Kd',
        title='',
        canvas=canvas,
        regions=regions,
        slots=slots,
        diagrams=diagrams,
        groups=groups,
        constraints=constraints,
    )

PROBLEM_TEMPLATE = build_problem_template()


SEMANTIC_OVERRIDE = {   'problem_id': 'p260422_024',
    'problem_type': 'arithmetic',
    'metadata': {'language': 'ko', 'question': '5/8 ÷ 2/8', 'instruction': ''},
    'domain': {   'objects': [   {'id': 'n1', 'type': 'number', 'value': 5, 'text': '5'},
                                 {'id': 'n2', 'type': 'number', 'value': 8, 'text': '8'},
                                 {'id': 'f1', 'type': 'fraction', 'text': '5/8'},
                                 {'id': 'n3', 'type': 'number', 'value': 2, 'text': '2'},
                                 {'id': 'n4', 'type': 'number', 'value': 8, 'text': '8'},
                                 {'id': 'f2', 'type': 'fraction', 'text': '2/8'},
                                 {'id': 'op1', 'type': 'operator', 'value': '÷', 'text': '÷'},
                                 {'id': 'q1', 'type': 'question', 'text': '5/8 ÷ 2/8'}],
                  'relations': [   {'id': 'r1', 'type': 'contains', 'from_id': 'q1', 'to_id': 'f1'},
                                   {'id': 'r2', 'type': 'contains', 'from_id': 'q1', 'to_id': 'f2'},
                                   {   'id': 'r3',
                                       'type': 'contains',
                                       'from_id': 'q1',
                                       'to_id': 'op1'},
                                   {'id': 'r4', 'type': 'defines', 'from_id': 'f1', 'to_id': 'n1'},
                                   {'id': 'r5', 'type': 'defines', 'from_id': 'f1', 'to_id': 'n2'},
                                   {'id': 'r6', 'type': 'defines', 'from_id': 'f2', 'to_id': 'n3'},
                                   {'id': 'r7', 'type': 'defines', 'from_id': 'f2', 'to_id': 'n4'},
                                   {   'id': 'r8',
                                       'type': 'references',
                                       'from_id': 'op1',
                                       'to_id': 'f1'},
                                   {   'id': 'r9',
                                       'type': 'references',
                                       'from_id': 'op1',
                                       'to_id': 'f2'}],
                  'problem_solving': {'understand': {}, 'plan': {}, 'execute': {}, 'review': {}}},
    'answer': {'target': {'type': 'number', 'description': '정답'}, 'value': 2.5, 'unit': ''}}

SOLVABLE = {   'schema': 'modu.solvable.v1',
    'problem_id': 'p260422_024',
    'problem_type': 'arithmetic',
    'inputs': {   'total_ticks': 2.5,
                  'target_label': '정답',
                  'target_ticks': 2.5,
                  'target_count': 2.5,
                  'unit': ''},
    'plan': [],
    'steps': [{'id': 'step.1', 'expr': '계산', 'value': 2.5}],
    'checks': [],
    'answer': {'value': 2.5, 'unit': ''}}
