from __future__ import annotations

from modu_math.dsl import Arrow, BlankSlot, Canvas, ChoiceSlot, Circle, CircleSlot, Constraint, Cube, DiagramTemplate, FractionAreaModel, Grid, Group, LabelSlot, LineSlot, PathSlot, PolygonSlot, ProblemTemplate, RectSlot, Region, ShapeObject, TextSlot, Triangle

def build_problem_template() -> ProblemTemplate:
    canvas = Canvas(
        width=650,
        height=246,
        coordinate_mode='logical',
    )
    regions = (
        Region(
            id='region.stem',
            role='stem',
            flow='vertical',
            slot_ids=('slot.b1', 'slot.b4', 'slot.b2'),
        ),
    )
    slots = (
        TextSlot(
            id='slot.b1',
            prompt='',
            text='계산 결과의 크기를 비교하여 ○ 안에 >, =, <를\n알맞게 써넣으시오.',
            style_role='body',
            x=16.5518798828125,
            y=45.75864601135254,
            font_size=30,
            fill='#111111',
        ),
        CircleSlot(
            id='slot.circle_4',
            prompt='',
            cx=341,
            cy=171.04651260375977,
            r=21.24983717169655,
            stroke='#222',
            stroke_width=2.0,
            fill='none',
        ),
        TextSlot(
            id='slot.b4',
            prompt='',
            text='3/7 ÷ 1/7',
            style_role='body',
            x=377,
            y=178.12066650390625,
            font_size=30,
            fill='#111111',
        ),
        TextSlot(
            id='slot.b2',
            prompt='',
            text='8/9 ÷ 2/9',
            style_role='body',
            x=171.7586669921875,
            y=179.8793182373047,
            font_size=30,
            fill='#111111',
        ),
    )
    diagrams = (
    )
    groups = (
    )
    constraints = (
    )
    return ProblemTemplate(
        id='msedge_41Shi9FWDB',
        title='',
        canvas=canvas,
        regions=regions,
        slots=slots,
        diagrams=diagrams,
        groups=groups,
        constraints=constraints,
    )

PROBLEM_TEMPLATE = build_problem_template()


SEMANTIC_OVERRIDE = {   'problem_id': 'p260422_002',
    'problem_type': 'symbolic_operator_arithmetic',
    'metadata': {   'language': 'ko',
                    'question': '8/9 ÷ 2/9 ○ 3/7 ÷ 1/7',
                    'instruction': '계산 결과의 크기를 비교하여 ○ 안에 >, =, < 를 알맞게 써넣으시오.'},
    'domain': {   'objects': [   {   'id': 'obj1',
                                     'type': 'instruction',
                                     'text': '계산 결과의 크기를 비교하여 ○ 안에 >, =, < 를 알맞게 써넣으시오.'},
                                 {'id': 'obj2', 'type': 'fraction', 'text': '8/9'},
                                 {'id': 'obj3', 'type': 'fraction', 'text': '2/9'},
                                 {   'id': 'obj4',
                                     'type': 'custom_operator',
                                     'value': '÷',
                                     'text': '÷'},
                                 {'id': 'obj5', 'type': 'fraction', 'text': '3/7'},
                                 {'id': 'obj6', 'type': 'fraction', 'text': '1/7'},
                                 {'id': 'obj7', 'type': 'unknown', 'value': '○', 'text': '○'},
                                 {'id': 'obj8', 'type': 'question', 'text': '비교 결과를 ○ 안에 넣기'}],
                  'relations': [   {   'id': 'rel1',
                                       'type': 'asks_for',
                                       'from_id': 'obj1',
                                       'to_id': 'obj8'},
                                   {   'id': 'rel2',
                                       'type': 'compares',
                                       'from_id': 'obj2',
                                       'to_id': 'obj5'},
                                   {   'id': 'rel3',
                                       'type': 'applies_to',
                                       'from_id': 'obj7',
                                       'to_id': 'obj8'}],
                  'problem_solving': {'understand': {}, 'plan': {}, 'execute': {}, 'review': {}}},
    'answer': {'target': {'type': 'number', 'description': '정답'}, 'value': '>', 'unit': ''}}

SOLVABLE = {   'schema': 'modu.solvable.v1',
    'problem_id': 'p260422_002',
    'problem_type': 'symbolic_operator_arithmetic',
    'inputs': {   'total_ticks': 0,
                  'target_label': '정답',
                  'target_ticks': 0,
                  'target_count': 0,
                  'unit': ''},
    'plan': [   '8/9 ÷ 2/9 = 8/9 × 9/2 = 4, and 3/7 ÷ 1/7 = 3/7 × 7 = 3. Since 4 > 3, the correct '
                'symbol is >.'],
    'steps': [   {   'id': 'step.1',
                     'expr': '8/9 ÷ 2/9 = 8/9 × 9/2 = 4, and 3/7 ÷ 1/7 = 3/7 × 7 = 3. Since 4 > 3, '
                             'the correct symbol is >.',
                     'value': '>'}],
    'checks': [],
    'answer': {'value': 0, 'unit': ''}}
