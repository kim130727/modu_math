from __future__ import annotations

from modu_math.dsl import Canvas, ProblemTemplate, Region, TextSlot, fraction_slots

def build_problem_template() -> ProblemTemplate:
    canvas = Canvas(
        width=300,
        height=150,
        coordinate_mode='logical',
    )
    regions = (
        Region(
            id='region.stem',
            role='stem',
            flow='absolute',
            slot_ids=(
                'slot.text.1',
                'slot.frac1.num', 'slot.frac1.bar', 'slot.frac1.den',
                'slot.text.div',
                'slot.frac2.num', 'slot.frac2.bar', 'slot.frac2.den'
            ),
        ),
    )
    slots = (
        TextSlot(
            id='slot.text.1',
            prompt='',
            text='1',
            style_role='body',
            x=20.0,
            y=85.0,
            font_size=35,
            fill='#000000',
        ),
        *fraction_slots(
            id_prefix='slot.frac1',
            numerator='1',
            denominator='4',
            x=60.0,
            numerator_y=63.0,
            denominator_y=107.0,
            bar_y=75.0,
            bar_width=40.0,
            font_size=35,
            fill='#000000',
            stroke='#000000',
            stroke_width=2.0,
        ),
        TextSlot(
            id='slot.text.div',
            prompt='',
            text='÷',
            style_role='body',
            x=105.0,
            y=85.0,
            font_size=35,
            fill='#000000',
        ),
        *fraction_slots(
            id_prefix='slot.frac2',
            numerator='1',
            denominator='3',
            x=175.0,
            numerator_y=63.0,
            denominator_y=107.0,
            bar_y=75.0,
            bar_width=40.0,
            font_size=35,
            fill='#000000',
            stroke='#000000',
            stroke_width=2.0,
        ),
    )
    return ProblemTemplate(
        id='msedge_x2oCeterFn',
        title='',
        canvas=canvas,
        regions=regions,
        slots=slots,
        diagrams=(),
        groups=(),
        constraints=(),
    )

PROBLEM_TEMPLATE = build_problem_template()


SEMANTIC_OVERRIDE = {   'problem_id': 'p260422_021',
    'problem_type': 'arithmetic',
    'metadata': {'language': 'ko', 'question': '1 1/4 ÷ 1/3', 'instruction': ''},
    'domain': {   'objects': [   {'id': 'obj1', 'type': 'number', 'value': 1, 'text': '1'},
                                 {'id': 'obj2', 'type': 'fraction', 'value': '1/4', 'text': '1/4'},
                                 {   'id': 'obj3',
                                     'type': 'expression',
                                     'value': '1 1/4',
                                     'text': '1 1/4'},
                                 {'id': 'obj4', 'type': 'operator', 'value': '÷', 'text': '÷'},
                                 {'id': 'obj5', 'type': 'fraction', 'value': '1/3', 'text': '1/3'}],
                  'relations': [   {   'id': 'rel1',
                                       'type': 'precedes',
                                       'from_id': 'obj3',
                                       'to_id': 'obj4'},
                                   {   'id': 'rel2',
                                       'type': 'precedes',
                                       'from_id': 'obj4',
                                       'to_id': 'obj5'},
                                   {   'id': 'rel3',
                                       'type': 'contains',
                                       'from_id': 'obj3',
                                       'to_id': 'obj1'},
                                   {   'id': 'rel4',
                                       'type': 'contains',
                                       'from_id': 'obj3',
                                       'to_id': 'obj2'}],
                  'problem_solving': {'understand': {}, 'plan': {}, 'execute': {}, 'review': {}}},
    'answer': {'target': {'type': 'number', 'description': '정답'}, 'value': 3.75, 'unit': ''}}

SOLVABLE = {   'schema': 'modu.solvable.v1',
    'problem_id': 'p260422_021',
    'problem_type': 'arithmetic',
    'inputs': {   'total_ticks': 3.75,
                  'target_label': '정답',
                  'target_ticks': 3.75,
                  'target_count': 3.75,
                  'unit': ''},
    'plan': [],
    'steps': [{'id': 'step.1', 'expr': '계산', 'value': 3.75}],
    'checks': [],
    'answer': {'value': 3.75, 'unit': ''}}
