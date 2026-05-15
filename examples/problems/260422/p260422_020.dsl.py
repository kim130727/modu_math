from __future__ import annotations

from modu_math.dsl import Canvas, ProblemTemplate, Region, TextSlot

def build_problem_template() -> ProblemTemplate:
    canvas = Canvas(
        width=1390,
        height=216,
        coordinate_mode='logical',
    )
    regions = (
        Region(
            id='region.stem',
            role='stem',
            flow='absolute',
            slot_ids=('slot.text.1', 'slot.text.2', 'slot.text.3'),
        ),
    )
    slots = (
        TextSlot(
            id='slot.text.1',
            prompt='',
            text='용희네 농장에서 닭과 오리를 키우고 있습니다. 닭이 498마리, 오',
            style_role='body',
            x=28.0,
            y=60.0,
            font_size=45,
            fill='#000000',
        ),
        TextSlot(
            id='slot.text.2',
            prompt='',
            text='리는 닭보다 117마리 더 많다고 합니다. 용희네 농장에서 키우고',
            style_role='body',
            x=28.0,
            y=140.0,
            font_size=45,
            fill='#000000',
        ),
        TextSlot(
            id='slot.text.3',
            prompt='',
            text='있는 닭과 오리는 모두 몇 마리입니까?',
            style_role='body',
            x=28.0,
            y=210.0,
            font_size=45,
            fill='#000000',
        ),
    )
    return ProblemTemplate(
        id='msedge_wtZFXPa9h9',
        title='',
        canvas=canvas,
        regions=regions,
        slots=slots,
        diagrams=(),
        groups=(),
        constraints=(),
    )

PROBLEM_TEMPLATE = build_problem_template()


SEMANTIC_OVERRIDE = {   'problem_id': 'p260422_020',
    'problem_type': 'word_problem',
    'metadata': {   'language': 'ko',
                    'question': '용희네 농장에서 닭과 오리를 키우고 있습니다. 닭이 498마리, 오리는 닭보다 117마리 더 많다고 합니다. 용희네 '
                                '농장에서 키우고 있는 닭과 오리는 모두 몇 마리입니까?',
                    'instruction': ''},
    'domain': {   'objects': [   {   'id': 'obj1',
                                     'type': 'question',
                                     'text': '용희네 농장에서 키우고 있는 닭과 오리는 모두 몇 마리입니까?'},
                                 {'id': 'obj2', 'type': 'number', 'value': 498, 'text': '498'},
                                 {'id': 'obj3', 'type': 'number', 'value': 117, 'text': '117'},
                                 {   'id': 'obj4',
                                     'type': 'constant',
                                     'value': 'chicken',
                                     'text': '닭'},
                                 {'id': 'obj5', 'type': 'constant', 'value': 'duck', 'text': '오리'},
                                 {'id': 'obj6', 'type': 'expression', 'text': '498 + (498 + 117)'}],
                  'relations': [   {   'id': 'rel1',
                                       'type': 'references',
                                       'from_id': 'obj1',
                                       'to_id': 'obj2'},
                                   {   'id': 'rel2',
                                       'type': 'references',
                                       'from_id': 'obj1',
                                       'to_id': 'obj3'},
                                   {   'id': 'rel3',
                                       'type': 'references',
                                       'from_id': 'obj1',
                                       'to_id': 'obj4'},
                                   {   'id': 'rel4',
                                       'type': 'references',
                                       'from_id': 'obj1',
                                       'to_id': 'obj5'},
                                   {   'id': 'rel5',
                                       'type': 'asks_for',
                                       'from_id': 'obj1',
                                       'to_id': 'obj6'},
                                   {   'id': 'rel6',
                                       'type': 'evaluates_to',
                                       'from_id': 'obj6',
                                       'to_id': None}],
                  'problem_solving': {'understand': {}, 'plan': {}, 'execute': {}, 'review': {}}},
    'answer': {'target': {'type': 'number', 'description': '정답'}, 'value': 1113, 'unit': '마리'}}

SOLVABLE = {   'schema': 'modu.solvable.v1',
    'problem_id': 'p260422_020',
    'problem_type': 'word_problem',
    'inputs': {   'total_ticks': 1113,
                  'target_label': '정답',
                  'target_ticks': 1113,
                  'target_count': 1113,
                  'unit': '마리'},
    'plan': ['오리 수는 498 + 117 = 615마리이고, 닭과 오리의 합은 498 + 615 = 1113마리입니다.'],
    'steps': [   {   'id': 'step.1',
                     'expr': '오리 수는 498 + 117 = 615마리이고, 닭과 오리의 합은 498 + 615 = 1113마리입니다.',
                     'value': 1113}],
    'checks': [],
    'answer': {'value': 1113, 'unit': '마리'}}
