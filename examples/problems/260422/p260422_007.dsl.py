from __future__ import annotations

from modu_math.dsl import Arrow, BlankSlot, Canvas, ChoiceSlot, Circle, CircleSlot, Constraint, Cube, DiagramTemplate, FractionAreaModel, Grid, Group, LabelSlot, LineSlot, PathSlot, PolygonSlot, ProblemTemplate, RectSlot, Region, ShapeObject, TextSlot, Triangle

def build_problem_template() -> ProblemTemplate:
    canvas = Canvas(
        width=1179,
        height=244,
        coordinate_mode='logical',
    )
    regions = (
        Region(
            id='region.stem',
            role='stem',
            flow='vertical',
            slot_ids=('slot.b1',),
        ),
    )
    slots = (
        TextSlot(
            id='slot.b1',
            prompt='',
            text='오늘 동물원에 입장한 어른은 824명, 어린이는 647명입니다.',
            style_role='body',
            x=15.0,
            y=80.0,
            font_size=45,
            fill='#111111',
        ),
        TextSlot(
            id='slot.b2',
            prompt='',
            text='오늘 동물원에 입장한 어른은 어린이보다 몇 명 더 많습니까?',
            style_role='body',
            x=15.0,
            y=150.0,
            font_size=45,
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
        id='msedge_ib0uSJwhd1',
        title='',
        canvas=canvas,
        regions=regions,
        slots=slots,
        diagrams=diagrams,
        groups=groups,
        constraints=constraints,
    )

PROBLEM_TEMPLATE = build_problem_template()


SEMANTIC_OVERRIDE = {   'problem_id': 'p260422_007',
    'problem_type': 'word_problem',
    'metadata': {   'language': 'ko',
                    'question': '오늘 동물원에 입장한 어른은 824명, 어린이는 647명입니다. 오늘 동물원에 입장한 어른은 어린이보다 몇 명 더 '
                                '많습니까?',
                    'instruction': ''},
    'domain': {   'objects': [   {'id': 'o1', 'type': 'question', 'text': '어른은 어린이보다 몇 명 더 많습니까?'},
                                 {'id': 'o2', 'type': 'number', 'value': 824, 'text': '824'},
                                 {'id': 'o3', 'type': 'number', 'value': 647, 'text': '647'},
                                 {'id': 'o4', 'type': 'unit', 'value': '명', 'text': '명'},
                                 {   'id': 'o5',
                                     'type': 'expression',
                                     'value': '824 - 647',
                                     'text': '824 - 647'}],
                  'relations': [   {'id': 'r1', 'type': 'asks_for', 'from_id': 'o1', 'to_id': 'o5'},
                                   {   'id': 'r2',
                                       'type': 'references',
                                       'from_id': 'o1',
                                       'to_id': 'o2'},
                                   {   'id': 'r3',
                                       'type': 'references',
                                       'from_id': 'o1',
                                       'to_id': 'o3'},
                                   {   'id': 'r4',
                                       'type': 'evaluates_to',
                                       'from_id': 'o5',
                                       'to_id': None}],
                  'problem_solving': {'understand': {}, 'plan': {}, 'execute': {}, 'review': {}}},
    'answer': {'target': {'type': 'number', 'description': '정답'}, 'value': 177, 'unit': '명'}}

SOLVABLE = {   'schema': 'modu.solvable.v1',
    'problem_id': 'p260422_007',
    'problem_type': 'word_problem',
    'inputs': {   'total_ticks': 177,
                  'target_label': '정답',
                  'target_ticks': 177,
                  'target_count': 177,
                  'unit': '명'},
    'plan': ['824명에서 647명을 빼면 177명입니다.'],
    'steps': [{'id': 'step.1', 'expr': '824명에서 647명을 빼면 177명입니다.', 'value': 177}],
    'checks': [],
    'answer': {'value': 177, 'unit': '명'}}
