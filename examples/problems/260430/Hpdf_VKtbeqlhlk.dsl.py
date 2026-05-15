from __future__ import annotations
from modu_math.dsl import Canvas, ProblemTemplate, Region, TextSlot


def build_problem_template() -> ProblemTemplate:
    return ProblemTemplate(
        id="Hpdf_VKtbeqlhlk",
        title="테이프 길이 합",
        canvas=Canvas(width=566, height=201, coordinate_mode="logical"),
        regions=(
            Region(
                id="region.stem",
                role="stem",
                flow="absolute",
                slot_ids=("slot.q1", "slot.q2", "slot.q3", "slot.q4"),
            ),
        ),
        slots=(
            TextSlot(
                id="slot.q1",
                prompt="",
                text="초록색 테이프 294 cm와 노란색 테이프",
                style_role="question",
                x=14.0,
                y=36.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.q2",
                prompt="",
                text="215 cm를 겹치게 한 줄로 이어 붙였더니",
                style_role="question",
                x=14.0,
                y=75.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.q3",
                prompt="",
                text="374 cm가 되었습니다. 겹친 부분은 몇 cm입",
                style_role="question",
                x=14.0,
                y=114.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.q4",
                prompt="",
                text="니까?",
                style_role="question",
                x=14.0,
                y=153.0,
                font_size=28,
            ),
        ),
        diagrams=(),
        groups=(),
        constraints=(),
        tags=(),
    )


PROBLEM_TEMPLATE = build_problem_template()
SEMANTIC_OVERRIDE = {
    "problem_id": "Hpdf_VKtbeqlhlk",
    "problem_type": "overlap_length",
    "metadata": {
        "language": "ko",
        "question": "초록색 테이프 294 cm와 노란색 테이프 215 cm를 겹치게 한 줄로 이어 붙였더니 374 cm가 되었습니다. 겹친 부분은 몇 cm입니까?",
        "instruction": "겹친 부분의 길이를 구하시오.",
    },
    "domain": {
        "objects": [
            {
                "id": "obj.tape.green",
                "type": "tape",
                "color": "green",
                "length_cm": 294,
            },
            {
                "id": "obj.tape.yellow",
                "type": "tape",
                "color": "yellow",
                "length_cm": 215,
            },
            {"id": "obj.result.length", "type": "length", "value_cm": 374},
            {"id": "obj.overlap", "type": "overlap"},
        ],
        "relations": [
            {
                "id": "rel.combine_with_overlap",
                "type": "combined_length_with_overlap",
                "from_id": "obj.tape.green",
                "to_id": "obj.tape.yellow",
                "result": "obj.result.length",
                "shared_part": "obj.overlap",
            }
        ],
        "problem_solving": {
            "understand": {
                "given_refs": [
                    "obj.tape.green",
                    "obj.tape.yellow",
                    "obj.result.length",
                ],
                "target_ref": "answer.target",
                "condition_refs": ["rel.combine_with_overlap"],
            },
            "plan": {
                "method": "subtract_overlap_from_sum",
                "description": "두 테이프의 전체 길이의 합에서 이어 붙인 길이를 빼서 겹친 부분의 길이를 구한다.",
            },
            "execute": {
                "expected_operations": ["add_two_lengths", "subtract_combined_length"]
            },
            "review": {
                "check_methods": ["inverse_relation_check", "unit_consistency_check"]
            },
        },
    },
    "answer": {
        "target": {"type": "overlap_length", "description": "겹친 부분의 길이"},
        "value": 135,
        "unit": "cm",
    },
}
SOLVABLE = {   'schema': 'modu.solvable.v1',
    'problem_id': 'Hpdf_VKtbeqlhlk',
    'problem_type': 'overlap_length',
    'given': [   {'ref': 'obj.tape.green', 'value': {'length_cm': 294}},
                 {'ref': 'obj.tape.yellow', 'value': {'length_cm': 215}},
                 {'ref': 'obj.result.length', 'value': {'value_cm': 374}}],
    'target': {'ref': 'answer.target', 'type': 'overlap_length'},
    'method': 'subtract_overlap_from_sum',
    'steps': [   {   'id': 'step.s1',
                     'operation': 'add_two_lengths',
                     'expr': '294 + 215',
                     'value': 509},
                 {   'id': 'step.s2',
                     'operation': 'subtract_combined_length',
                     'expr': '509 - 374',
                     'value': 135}],
    'checks': [   {   'id': 'check.c1',
                      'type': 'inverse_relation_check',
                      'pass': True,
                      'expr': '294 + 215 - 135 = 374',
                      'expected': 1,
                      'actual': 1},
                  {   'id': 'check.c2',
                      'type': 'unit_consistency_check',
                      'pass': True,
                      'expected': 1,
                      'actual': 1,
                      'expr': 'check'}],
    'answer': {'value': 135, 'unit': 'cm', 'derived_from': 'step.s2'},
    'inputs': {   'total_ticks': 1,
                  'target_label': '답',
                  'target_ticks': 1,
                  'target_count': 1,
                  'unit': ''},
    'plan': ['풀이 과정 없음']}
