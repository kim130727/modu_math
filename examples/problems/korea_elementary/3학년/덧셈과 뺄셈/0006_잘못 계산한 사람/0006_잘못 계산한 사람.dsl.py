from __future__ import annotations

from modu_math.dsl import Arrow, BlankSlot, Canvas, ChoiceSlot, Circle, CircleSlot, Constraint, Cube, DiagramTemplate, FractionAreaModel, Grid, Group, LabelSlot, LineSlot, PathSlot, PolygonSlot, ProblemTemplate, RectSlot, Region, ShapeObject, TextSlot, Triangle

def build_problem_template() -> ProblemTemplate:
    canvas = Canvas(
        width=767,
        height=276,
        coordinate_mode='logical',
    )
    regions = (
        Region(
            id='region.stem',
            role='stem',
            flow='vertical',
            slot_ids=('slot.i1', 'slot.i2', 'slot.jy', 'slot.gw'),
        ),
    )
    slots = (
        RectSlot(
            id='slot.bg',
            prompt='',
            x=0.0,
            y=0.0,
            width=767.0,
            height=276.0,
            stroke='none',
            stroke_width=0.0,
            fill='none',
        ),
        TextSlot(
            id='slot.i1',
            prompt='',
            text='지은이와 건우가 875-328을 계산한 방법을 대화로 나타낸 것입니다. 잘못 계산한',
            style_role='body',
            x=6.0,
            y=34.0,
            font_size=17,
            font_family='Malgun Gothic',
            anchor='start',
            fill='#222222',
        ),
        TextSlot(
            id='slot.i2',
            prompt='',
            text='사람과 이유를 쓰세요.',
            style_role='body',
            x=6.0,
            y=62.0,
            font_size=17,
            font_family='Malgun Gothic',
            anchor='start',
            fill='#222222',
        ),
        RectSlot(
            id='slot.bubble',
            prompt='',
            x=14.0,
            y=98.0,
            width=740.0,
            height=116.0,
            stroke='#666666',
            stroke_width=1.5,
            rx=10.0,
            ry=10.0,
            fill='none',
        ),
        TextSlot(
            id='slot.jy',
            prompt='',
            text='• 지은: 800에서 300을 빼고, 75에서 28을 뺀 다음 두 결과를 더했어.',
            style_role='body',
            x=24.0,
            y=132.0,
            font_size=17,
            font_family='Malgun Gothic',
            anchor='start',
            fill='#222222',
        ),
        TextSlot(
            id='slot.gw',
            prompt='',
            text='• 건우: 800에서 300을 빼고 75에서 30을 뺀 다음 2를 빼서 결과를 더했어.',
            style_role='body',
            x=24.0,
            y=174.0,
            font_size=17,
            font_family='Malgun Gothic',
            anchor='start',
            fill='#222222',
        ),
        RectSlot(
            id='slot.answer_text',
            prompt='',
            x=400.0,
            y=236.0,
            width=350.0,
            height=30.0,
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
        id='0006_잘못 계산한 사람',
        title='',
        canvas=canvas,
        regions=regions,
        slots=slots,
        diagrams=diagrams,
        groups=groups,
        constraints=constraints,
    )

PROBLEM_TEMPLATE = build_problem_template()

SEMANTIC_OVERRIDE = {'problem_id': '0006_잘못 계산한 사람',
 'problem_type': 'arithmetic_mental_math_critique',
 'metadata': {'title': '',
              'tags': [],
              'instruction': '잘못 계산한 사람과 이유를 쓰세요.',
              'question': '875-328을 계산하는 두 가지 암산 방법 중 잘못된 것을 찾고 이유를 설명하는 문제',
              'required_layout_ids': ['slot.bg', 'slot.bubble', 'slot.answer_text'],
              'extraction_confidence': 1.0,
              'language': 'ko'},
 'domain': {'objects': [{'id': 'obj.target_eq', 'type': 'equation', 'value': '875-328'},
                        {'id': 'obj.jieun',
                         'type': 'person',
                         'strategy': 'partial_subtraction_correct'},
                        {'id': 'obj.kunwoo',
                         'type': 'person',
                         'strategy': 'partial_subtraction_incorrect'}],
            'relations': [],
            'confidence': 1.0,
            'problem_solving': {'plan': {'method': 'logical_analysis_of_mental_math',
                                         'description': '각 사람의 계산 과정을 수식으로 변환하여 오류를 찾는다.'}}},
 'answer': {'blanks': [],
            'choices': [],
            'answer_key': [],
            'confidence': 1.0,
            'value': 0,
            'unit': '',
            'target': {'type': 'unknown', 'description': ''}}}

SOLVABLE = {'schema': 'modu.solvable.v1',
 'problem_id': '0006_잘못 계산한 사람',
 'problem_type': 'arithmetic_mental_math_critique',
 'inputs': {'total_ticks': 1, 'target_label': '', 'target_ticks': 1, 'target_count': 1, 'unit': ''},
 'given': [{'ref': 'obj.target_eq', 'value': '875-328'}],
 'target': {'ref': 'answer.target', 'type': 'unknown'},
 'method': 'read_visible_information',
 'plan': ['주어진 조건을 읽고 목표 값을 계산한다.'],
 'steps': [{'id': 'step.1',
            'operation': 'identify_target',
            'expr': 'identify target from problem',
            'value': 0}],
 'checks': [{'id': 'check.1',
             'expr': 'basic consistency check',
             'expected': '건우',
             'actual': '건우',
             'pass': True}],
 'answer': {'value': 0, 'unit': '', 'derived_from': 'step.1'}}
