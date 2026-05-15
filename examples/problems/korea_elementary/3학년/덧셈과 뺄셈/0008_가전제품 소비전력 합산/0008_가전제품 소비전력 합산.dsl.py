from __future__ import annotations

from modu_math.dsl import Arrow, BlankSlot, Canvas, ChoiceSlot, Circle, CircleSlot, Constraint, Cube, DiagramTemplate, FractionAreaModel, Grid, Group, LabelSlot, LineSlot, PolygonSlot, ProblemTemplate, RectSlot, Region, ShapeObject, TextSlot, Triangle

def build_problem_template() -> ProblemTemplate:
    canvas = Canvas(
        width=1000,
        height=600,
        coordinate_mode='logical',
    )
    regions = (
        Region(
            id='region.stem',
            role='stem',
            flow='vertical',
            slot_ids=('slot.t1',
             'slot.t2',
             'slot.name_0',
             'slot.name_1',
             'slot.name_2',
             'slot.val_0',
             'slot.val_1',
             'slot.val_2'),
        ),
    )
    slots = (
        TextSlot(
            id='slot.t1',
            prompt='',
            text='다음 가전제품 중에서 2개를 골라 소비전력의 합이 1000 W가 넘는',
            style_role='body',
        ),
        TextSlot(
            id='slot.t2',
            prompt='',
            text='경우를 찾아 그 합을 구하시오.',
            style_role='body',
        ),
        TextSlot(
            id='slot.name_0',
            prompt='',
            text='전기밥솥',
            style_role='body',
        ),
        TextSlot(
            id='slot.name_1',
            prompt='',
            text='정수기',
            style_role='body',
        ),
        TextSlot(
            id='slot.name_2',
            prompt='',
            text='모니터',
            style_role='body',
        ),
        TextSlot(
            id='slot.val_0',
            prompt='',
            text='500 W',
            style_role='body',
        ),
        TextSlot(
            id='slot.val_1',
            prompt='',
            text='770 W',
            style_role='body',
        ),
        TextSlot(
            id='slot.val_2',
            prompt='',
            text='150 W',
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
        id='0008_가전제품 소비전력 합산',
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
    'problem_id': '0008_가전제품 소비전력 합산',
    'problem_type': 'arithmetic_combination_sum_threshold',
    'metadata': {
        'language': 'ko',
        'question': '가전제품(전기밥솥:500W, 정수기:770W, 모니터:150W) 중 2개의 합이 1000W를 넘는 경우를 찾는 문제',
        'instruction': '합이 1000 W가 넘는 경우를 찾아 그 합을 구하시오.',
    },
    'domain': {
        'objects': [
            {'id': 'obj.rice_cooker', 'name': '전기밥솥', 'value': 500, 'unit': 'W'},
            {'id': 'obj.purifier', 'name': '정수기', 'value': 770, 'unit': 'W'},
            {'id': 'obj.monitor', 'name': '모니터', 'value': 150, 'unit': 'W'},
        ],
        'problem_solving': {
            'plan': {
                'method': 'exhaustive_search',
                'description': '가능한 모든 2개 조합의 합을 구하여 1000W 초과 여부를 확인한다.',
            }
        },
    },
    'answer': {
        'value': 1270,
        'unit': 'W',
    },
}

SOLVABLE = {
    'schema': 'modu.solvable.v1',
    'problem_id': '0008_가전제품 소비전력 합산',
    'problem_type': 'arithmetic_combination_sum_threshold',
    'given': [
        {'ref': 'obj.rice_cooker', 'value': 500},
        {'ref': 'obj.purifier', 'value': 770},
        {'ref': 'obj.monitor', 'value': 150}
    ],
    'target': {'type': 'number', 'description': '1000W를 넘는 합'},
    'method': 'exhaustive_search',
    'steps': [
        {
            'id': 'step.s1',
            'operation': 'addition',
            'expr': '500 + 770 = 1270',
            'description': '전기밥솥과 정수기의 합은 1270W입니다.',
            'value': 1270
        },
        {
            'id': 'step.s2',
            'operation': 'check',
            'expr': '1270 > 1000',
            'value': True
        }
    ],
    'checks': [
        {
            'id': 'check.c1',
            'type': 'arithmetic_consistency_check',
            'pass': True,
            'expected': 1270,
            'actual': 1270,
            'expr': '500 + 770'
        }
    ],
    'answer': {'value': 1270, 'unit': 'W', 'derived_from': 'step.s1'},
    'inputs': {
        'total_ticks': 1,
        'target_label': '답',
        'target_ticks': 1,
        'target_count': 1,
        'unit': 'W'
    },
    'plan': ['각 조합의 합을 구하여 1000이 넘는 1270(500+770)을 찾습니다.']
}
