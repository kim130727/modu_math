from __future__ import annotations

from modu_math.dsl import Canvas, ProblemTemplate, Region, TextSlot

def build_problem_template() -> ProblemTemplate:
    canvas = Canvas(width=600, height=250, coordinate_mode='logical')
    regions = (
        Region(
            id='region.stem',
            role='stem',
            flow='absolute',
            slot_ids=('slot.instr', 'slot.q1', 'slot.q2'),
        ),
    )
    slots = (
        TextSlot(
            id='slot.instr',
            prompt='',
            text='다음을 계산하시오.',
            style_role='body',
            x=20.0,
            y=50.0,
            font_size=35,
            fill='#111111',
        ),
        TextSlot(
            id='slot.q1',
            prompt='',
            text='(1) 196+198+202+204',
            style_role='body',
            x=20.0,
            y=120.0,
            font_size=35,
            fill='#111111',
        ),
        TextSlot(
            id='slot.q2',
            prompt='',
            text='(2) 127+346+873+654',
            style_role='body',
            x=20.0,
            y=190.0,
            font_size=35,
            fill='#111111',
        ),
    )
    return ProblemTemplate(
        id='msedge_ZhOurRI2aQ',
        title='',
        canvas=canvas,
        regions=regions,
        slots=slots,
        diagrams=(),
        groups=(),
        constraints=(),
    )

PROBLEM_TEMPLATE = build_problem_template()


SEMANTIC_OVERRIDE = {   'problem_id': 'p260422_025',
    'problem_type': 'arithmetic',
    'metadata': {   'language': 'ko',
                    'question': '(1) 196+198+202+204\n(2) 127+346+873+654',
                    'instruction': '다음을 계산하시오.'},
    'domain': {   'objects': [   {   'id': 'obj_instruction',
                                     'type': 'instruction',
                                     'text': '다음을 계산하시오.'},
                                 {'id': 'obj_q1', 'type': 'expression', 'text': '196+198+202+204'},
                                 {'id': 'obj_q2', 'type': 'expression', 'text': '127+346+873+654'}],
                  'relations': [   {   'id': 'rel_1',
                                       'type': 'asks_for',
                                       'from_id': 'obj_instruction',
                                       'to_id': 'obj_q1'},
                                   {   'id': 'rel_2',
                                       'type': 'asks_for',
                                       'from_id': 'obj_instruction',
                                       'to_id': 'obj_q2'}],
                  'problem_solving': {'understand': {}, 'plan': {}, 'execute': {}, 'review': {}}},
    'answer': {   'target': {'type': 'number', 'description': '정답'},
                  'value': [800, 2000],
                  'unit': ''}}

SOLVABLE = {   'schema': 'modu.solvable.v1',
    'problem_id': 'p260422_025',
    'problem_type': 'arithmetic',
    'inputs': {   'total_ticks': 0,
                  'target_label': '정답',
                  'target_ticks': 0,
                  'target_count': 0,
                  'unit': ''},
    'plan': ['(1) 196+198+202+204 = 800. (2) 127+346+873+654 = 2000.'],
    'steps': [   {   'id': 'step.1',
                     'expr': '(1) 196+198+202+204 = 800. (2) 127+346+873+654 = 2000.',
                     'value': [800, 2000]}],
    'checks': [],
    'answer': {'value': 2800, 'unit': ''}}
