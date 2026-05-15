from __future__ import annotations

from modu_math.dsl import Arrow, BlankSlot, Canvas, ChoiceSlot, Circle, CircleSlot, Constraint, Cube, DiagramTemplate, FractionAreaModel, Grid, Group, LabelSlot, LineSlot, PolygonSlot, ProblemTemplate, RectSlot, Region, ShapeObject, TextSlot, Triangle

def build_problem_template() -> ProblemTemplate:
    canvas = Canvas(
        width=1000,
        height=500,
        coordinate_mode='logical',
    )
    regions = (
        Region(
            id='region.stem',
            role='stem',
            flow='vertical',
            slot_ids=('slot.t1', 'slot.t2', 'slot.t3'),
        ),
    )
    slots = (
        TextSlot(
            id='slot.t1',
            prompt='',
            text='국어나 수학을 좋아하는 학생 780명 중에서 국어를 좋아하는 학생이 621명,',
            style_role='body',
        ),
        TextSlot(
            id='slot.t2',
            prompt='',
            text='수학을 좋아하는 학생이 348명입니다. 국어와 수학을 모두 좋아하는 학생은',
            style_role='body',
        ),
        TextSlot(
            id='slot.t3',
            prompt='',
            text='몇 명입니까?',
            style_role='body',
        ),
    )
    diagrams = (
    )
    groups = (
    )
    constraints = (
    )
    return ProblemTemplate(
        id='0004_국어와 수학을 모두 좋아하는 학생 수',
        title='',
        canvas=canvas,
        regions=regions,
        slots=slots,
        diagrams=diagrams,
        groups=groups,
        constraints=constraints,
    )

PROBLEM_TEMPLATE = build_problem_template()

SEMANTIC_OVERRIDE = {
    'problem_id': '0004_국어와 수학을 모두 좋아하는 학생 수',
    'problem_type': 'arithmetic_set_theory_word_problem',
    'metadata': {
        'language': 'ko',
        'question': '전체 학생 수(합집합)와 각 과목을 좋아하는 학생 수를 알 때, 두 과목을 모두 좋아하는 학생 수(교집합)를 구하는 문제',
        'instruction': '국어와 수학을 모두 좋아하는 학생은 몇 명입니까?',
    },
    'domain': {
        'objects': [
            {'id': 'obj.total_union', 'type': 'count', 'value': 780, 'description': '국어나 수학을 좋아하는 학생'},
            {'id': 'obj.korean', 'type': 'count', 'value': 621, 'description': '국어를 좋아하는 학생'},
            {'id': 'obj.math', 'type': 'count', 'value': 348, 'description': '수학을 좋아하는 학생'},
        ],
        'problem_solving': {
            'plan': {
                'method': 'inclusion_exclusion_principle',
                'description': '교집합의 원소의 수 = n(A) + n(B) - n(A∪B) 공식을 이용한다.',
            }
        },
    },
    'answer': {
        'value': 189,
        'unit': '명',
    },
}

SOLVABLE = {
    'schema': 'modu.solvable.v1',
    'problem_id': '0004_국어와 수학을 모두 좋아하는 학생 수',
    'problem_type': 'arithmetic_set_theory_word_problem',
    'given': [
        {'ref': 'obj.total_union', 'value': 780},
        {'ref': 'obj.korean', 'value': 621},
        {'ref': 'obj.math', 'value': 348}
    ],
    'target': {'type': 'count', 'description': '모두 좋아하는 학생 수'},
    'method': 'inclusion_exclusion_principle',
    'steps': [
        {
            'id': 'step.s1',
            'operation': 'addition',
            'expr': '621 + 348 = 969',
            'value': 969
        },
        {
            'id': 'step.s2',
            'operation': 'subtraction',
            'expr': '969 - 780 = 189',
            'value': 189
        }
    ],
    'checks': [
        {
            'id': 'check.c1',
            'type': 'arithmetic_consistency_check',
            'pass': True,
            'expected': 189,
            'actual': 189,
            'expr': '621 + 348 - 189 = 780'
        }
    ],
    'answer': {'value': 189, 'unit': '명', 'derived_from': 'step.s2'},
    'inputs': {
        'total_ticks': 1,
        'target_label': '답',
        'target_ticks': 1,
        'target_count': 1,
        'unit': '명'
    },
    'plan': ['국어와 수학을 좋아하는 학생 수의 합(969)에서 전체 학생 수(780)를 빼서 교집합인 189를 구합니다.']
}
