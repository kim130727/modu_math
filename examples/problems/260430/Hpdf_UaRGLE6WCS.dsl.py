from __future__ import annotations
from modu_math.dsl import Canvas, ProblemTemplate, Region, TextSlot


def build_problem_template() -> ProblemTemplate:
    return ProblemTemplate(
        id="Hpdf_UaRGLE6WCS",
        title="정사각형 모양의 종이",
        canvas=Canvas(width=558, height=154, coordinate_mode="logical"),
        regions=(
            Region(
                id="region.stem",
                role="stem",
                flow="absolute",
                slot_ids=("slot.q1", "slot.q2", "slot.q3"),
            ),
        ),
        slots=(
            TextSlot(
                id="slot.q1",
                prompt="",
                text="한 변이 40 cm인 정사각형 모양의 종이를 잘라",
                style_role="question",
                x=8.0,
                y=34.0,
                font_size=28,
                anchor="start",
            ),
            TextSlot(
                id="slot.q2",
                prompt="",
                text="한 변이 5 cm인 정사각형을 만들려고 합니다.",
                style_role="question",
                x=8.0,
                y=74.0,
                font_size=28,
                anchor="start",
            ),
            TextSlot(
                id="slot.q3",
                prompt="",
                text="모두 몇 개까지 만들 수 있습니까?",
                style_role="question",
                x=8.0,
                y=114.0,
                font_size=28,
                anchor="start",
            ),
        ),
        diagrams=(),
        groups=(),
        constraints=(),
        tags=(),
    )


PROBLEM_TEMPLATE = build_problem_template()
SEMANTIC_OVERRIDE = {
    "problem_id": "Hpdf_UaRGLE6WCS",
    "problem_type": "area_division",
    "metadata": {
        "language": "ko",
        "question": "한 변이 40 cm인 정사각형 모양의 종이를 잘라 한 변이 5 cm인 정사각형을 만들려고 합니다. 모두 몇 개까지 만들 수 있습니까?",
        "instruction": "",
    },
    "domain": {
        "objects": [
            {"id": "obj.large_square_paper", "type": "square", "side_length_cm": 40},
            {"id": "obj.small_square_piece", "type": "square", "side_length_cm": 5},
        ],
        "relations": [
            {
                "id": "rel.side_ratio",
                "type": "same_shape_scaling",
                "from_id": "obj.large_square_paper",
                "to_id": "obj.small_square_piece",
                "ratio": 8,
            },
            {
                "id": "rel.partition_count",
                "type": "count_by_side_division",
                "from_id": "obj.large_square_paper",
                "to_id": "obj.small_square_piece",
            },
        ],
        "problem_solving": {
            "understand": {
                "given_refs": ["obj.large_square_paper", "obj.small_square_piece"],
                "target_ref": "answer.target",
                "condition_refs": ["rel.side_ratio", "rel.partition_count"],
            },
            "plan": {
                "method": "side_division_and_area_count",
                "description": "큰 정사각형의 한 변에 작은 정사각형이 몇 개 들어가는지 보고, 전체 개수를 구한다.",
            },
            "execute": {
                "expected_operations": ["divide_side_length", "square_the_result"]
            },
            "review": {"check_methods": ["area_ratio_check", "unit_consistency_check"]},
        },
    },
    "answer": {
        "target": {
            "type": "count",
            "description": "만들 수 있는 5 cm 정사각형의 최대 개수",
        },
        "value": 64,
        "unit": "개",
    },
}
SOLVABLE = {   'schema': 'modu.solvable.v1',
    'problem_id': 'Hpdf_UaRGLE6WCS',
    'problem_type': 'area_division',
    'given': [   {'ref': 'obj.large_square_paper', 'value': {'side_length_cm': 40}},
                 {'ref': 'obj.small_square_piece', 'value': {'side_length_cm': 5}}],
    'target': {'ref': 'answer.target', 'type': 'count'},
    'method': 'side_division_and_area_count',
    'steps': [   {'id': 'step.s1', 'operation': 'divide_side_length', 'expr': '40 ÷ 5', 'value': 8},
                 {'id': 'step.s2', 'operation': 'square_the_result', 'expr': '8 × 8', 'value': 64}],
    'checks': [   {   'id': 'check.c1',
                      'type': 'area_ratio_check',
                      'pass': True,
                      'expected': 1,
                      'actual': 1,
                      'expr': 'check'},
                  {   'id': 'check.c2',
                      'type': 'unit_consistency_check',
                      'pass': True,
                      'expected': 1,
                      'actual': 1,
                      'expr': 'check'}],
    'answer': {'value': 64, 'unit': '개', 'derived_from': 'step.s2'},
    'inputs': {   'total_ticks': 1,
                  'target_label': '답',
                  'target_ticks': 1,
                  'target_count': 1,
                  'unit': ''},
    'plan': ['풀이 과정 없음']}
