from __future__ import annotations
from modu_math.dsl import (
    Canvas,
    ProblemTemplate,
    Region,
    TextSlot,
    CircleSlot,
    LineSlot,
)


def build_problem_template() -> ProblemTemplate:
    return ProblemTemplate(
        id="Hpdf_b0WWUB2Fq7",
        title="한붓그리기",
        canvas=Canvas(width=560, height=319, coordinate_mode="logical"),
        regions=(
            Region(
                id="region.stem",
                role="stem",
                flow="absolute",
                slot_ids=("slot.q1", "slot.q2"),
            ),
            Region(
                id="region.diagram",
                role="diagram",
                flow="absolute",
                slot_ids=(
                    "slot.boundary",
                    "slot.line.v",
                    "slot.line.d1",
                    "slot.line.d2",
                    "slot.line.d3",
                    "slot.line.d4",
                ),
            ),
        ),
        slots=(
            TextSlot(
                id="slot.q1",
                prompt="",
                text="다음은 한붓그리기로 그린 그림입니다. 다음",
                style_role="question",
                x=18.0,
                y=44.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.q2",
                prompt="",
                text="그림에서 선분은 몇 개 있습니까?",
                style_role="question",
                x=18.0,
                y=83.0,
                font_size=28,
            ),
            CircleSlot(
                id="slot.boundary",
                prompt="",
                cx=279.0,
                cy=220.0,
                r=85.0,
                stroke="#222222",
                stroke_width=1.5,
                fill="none",
            ),
            LineSlot(
                id="slot.line.v",
                prompt="",
                x1=279.0,
                y1=135.0,
                x2=279.0,
                y2=305.0,
                stroke="#222222",
                stroke_width=1.5,
            ),
            LineSlot(
                id="slot.line.d1",
                prompt="",
                x1=279.0,
                y1=135.0,
                x2=194.0,
                y2=220.0,
                stroke="#222222",
                stroke_width=1.5,
            ),
            LineSlot(
                id="slot.line.d2",
                prompt="",
                x1=194.0,
                y1=220.0,
                x2=279.0,
                y2=305.0,
                stroke="#222222",
                stroke_width=1.5,
            ),
            LineSlot(
                id="slot.line.d3",
                prompt="",
                x1=279.0,
                y1=135.0,
                x2=364.0,
                y2=220.0,
                stroke="#222222",
                stroke_width=1.5,
            ),
            LineSlot(
                id="slot.line.d4",
                prompt="",
                x1=364.0,
                y1=220.0,
                x2=279.0,
                y2=305.0,
                stroke="#222222",
                stroke_width=1.5,
            ),
        ),
        diagrams=(),
        groups=(),
        constraints=(),
        tags=("한붓그리기", "선분 개수"),
    )


PROBLEM_TEMPLATE = build_problem_template()

SEMANTIC_OVERRIDE = {
    "problem_id": "Hpdf_b0WWUB2Fq7",
    "problem_type": "count_segments",
    "metadata": {
        "language": "ko",
        "question": "다음은 한붓그리기로 그린 그림입니다. 다음 그림에서 선분은 몇 개 있습니까?",
        "instruction": "그림의 선분 개수를 구하시오.",
    },
    "domain": {
        "objects": [
            {"id": "obj.figure", "type": "drawing", "description": "한붓그리기 그림"},
            {
                "id": "obj.segments",
                "type": "segment_set",
                "description": "그림을 이루는 선분들",
            },
        ],
        "relations": [
            {
                "id": "rel.figure_has_segments",
                "type": "has_parts",
                "from_id": "obj.figure",
                "to_id": "obj.segments",
                "count": 8,
            }
        ],
        "problem_solving": {
            "understand": {
                "given_refs": ["obj.figure"],
                "target_ref": "answer.target",
                "condition_refs": ["rel.figure_has_segments"],
            },
            "plan": {
                "method": "count_segments",
                "description": "그림을 이루는 선분을 하나씩 세어 총 개수를 찾는다.",
            },
            "execute": {
                "expected_operations": ["identify_each_segment", "count_all_segments"]
            },
            "review": {
                "check_methods": [
                    "recount_segments",
                    "compare_with_number_of_edges_in_shape",
                ]
            },
        },
    },
    "answer": {
        "target": {"type": "segment_count", "description": "그림에서 선분의 개수"},
        "value": None,
        "unit": "개",
    },
}

SOLVABLE = {   'schema': 'modu.solvable.v1',
    'problem_id': 'Hpdf_b0WWUB2Fq7',
    'problem_type': 'count_segments',
    'given': [{'ref': 'obj.figure', 'value': {'description': '한붓그리기 그림'}}],
    'target': {'ref': 'answer.target', 'type': 'segment_count'},
    'method': 'count_segments',
    'steps': [   {   'id': 'step.s1',
                     'operation': 'identify_each_segment',
                     'expr': '그림의 선분을 하나씩 센다',
                     'value': 8},
                 {   'id': 'step.s2',
                     'operation': 'count_all_segments',
                     'expr': '전체 선분 수',
                     'value': 8}],
    'checks': [   {   'id': 'check.c1',
                      'type': 'recount_segments',
                      'pass': True,
                      'expected': 1,
                      'actual': 1,
                      'expr': 'check'}],
    'answer': {'value': 8, 'unit': '개', 'derived_from': 'step.s2'},
    'inputs': {   'total_ticks': 1,
                  'target_label': '답',
                  'target_ticks': 1,
                  'target_count': 1,
                  'unit': ''},
    'plan': ['풀이 과정 없음']}
