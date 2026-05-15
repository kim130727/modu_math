from __future__ import annotations
from modu_math.dsl import (
    Canvas,
    CircleSlot,
    LineSlot,
    ProblemTemplate,
    RectSlot,
    Region,
    TextSlot,
)


def build_problem_template() -> ProblemTemplate:
    return ProblemTemplate(
        id="Hpdf_RJJOU7cmRm",
        title="도형에서 직사각형 개수 세기",
        canvas=Canvas(width=568, height=347, coordinate_mode="logical"),
        regions=(
            Region(
                id="region.stem",
                role="stem",
                flow="absolute",
                slot_ids=("slot.q1", "slot.diagram.border", "slot.diagram.lines"),
            ),
        ),
        slots=(
            TextSlot(
                id="slot.q1",
                prompt="",
                text="도형에서 찾을 수 있는 크고 작은 직사각형은 모두 몇 개입니까?",
                style_role="question",
                x=10.0,
                y=28.0,
                font_size=28,
                anchor="start",
            ),
            RectSlot(
                id="slot.diagram.border",
                prompt="",
                x=102.0,
                y=124.0,
                width=355.0,
                height=215.0,
                stroke="#222222",
                stroke_width=2.0,
                fill="none",
            ),
            LineSlot(
                id="slot.diagram.lines.v1",
                prompt="",
                x1=170.0,
                y1=124.0,
                x2=170.0,
                y2=194.0,
                stroke="#222222",
                stroke_width=2.0,
            ),
            LineSlot(
                id="slot.diagram.lines.v2",
                prompt="",
                x1=240.0,
                y1=124.0,
                x2=240.0,
                y2=339.0,
                stroke="#222222",
                stroke_width=2.0,
            ),
            LineSlot(
                id="slot.diagram.lines.v3",
                prompt="",
                x1=350.0,
                y1=124.0,
                x2=350.0,
                y2=339.0,
                stroke="#222222",
                stroke_width=2.0,
            ),
            LineSlot(
                id="slot.diagram.lines.h1",
                prompt="",
                x1=102.0,
                y1=194.0,
                x2=240.0,
                y2=194.0,
                stroke="#222222",
                stroke_width=2.0,
            ),
            LineSlot(
                id="slot.diagram.lines.h2",
                prompt="",
                x1=240.0,
                y1=231.0,
                x2=457.0,
                y2=231.0,
                stroke="#222222",
                stroke_width=2.0,
            ),
        ),
        diagrams=(),
        groups=(),
        constraints=(),
        tags=(),
    )


PROBLEM_TEMPLATE = build_problem_template()
SEMANTIC_OVERRIDE = {
    "problem_id": "Hpdf_RJJOU7cmRm",
    "problem_type": "count_rectangles",
    "metadata": {
        "language": "ko",
        "question": "도형에서 찾을 수 있는 크고 작은 직사각형은 모두 몇 개입니까?",
        "instruction": "",
    },
    "domain": {
        "objects": [
            {"id": "obj.figure", "type": "composite_rectangle_figure"},
            {"id": "obj.subrectangles", "type": "rectangles"},
        ],
        "relations": [
            {
                "id": "rel.count_rectangles",
                "type": "contains_rectangles",
                "from_id": "obj.figure",
                "to_id": "obj.subrectangles",
            }
        ],
        "problem_solving": {
            "understand": {
                "given_refs": ["obj.figure"],
                "target_ref": "answer.target",
                "condition_refs": ["rel.count_rectangles"],
            },
            "plan": {
                "method": "case_counting",
                "description": "도형 안에서 만들어지는 작은 직사각형과 여러 칸을 합친 큰 직사각형을 빠짐없이 분류해 센다.",
            },
            "execute": {
                "expected_operations": [
                    "identify_all_axis_aligned_rectangles",
                    "count_by_size_or_span",
                    "sum_all_cases",
                ]
            },
            "review": {"check_methods": ["no_double_counting", "edge_alignment_check"]},
        },
    },
    "answer": {
        "target": {
            "type": "count",
            "description": "도형에서 찾을 수 있는 크고 작은 직사각형의 개수",
        },
        "value": 15,
        "unit": "개",
    },
}
SOLVABLE = {   'schema': 'modu.solvable.v1',
    'problem_id': 'Hpdf_RJJOU7cmRm',
    'problem_type': 'count_rectangles',
    'given': [{'ref': 'obj.figure', 'value': {'type': 'composite_rectangle_figure'}}],
    'target': {'ref': 'answer.target', 'type': 'count'},
    'method': 'case_counting',
    'steps': [   {   'id': 'step.s1',
                     'operation': 'identify_all_axis_aligned_rectangles',
                     'expr': '도형을 이루는 기본 칸들(7개)과 이들을 조합해 만들 수 있는 직사각형을 모두 찾는다.',
                     'value': 15},
                 {   'id': 'step.s2',
                     'operation': 'sum_all_cases',
                     'expr': '왼쪽(5개) + 오른쪽(9개) + 전체(1개) = 15개',
                     'value': 15}],
    'checks': [   {   'id': 'check.c1',
                      'type': 'no_double_counting',
                      'pass': True,
                      'expected': 15,
                      'actual': 15,
                      'expr': 'check'}],
    'answer': {'value': 15, 'unit': '개', 'derived_from': 'step.s2'},
    'inputs': {   'total_ticks': 1,
                  'target_label': '답',
                  'target_ticks': 1,
                  'target_count': 1,
                  'unit': ''},
    'plan': ['풀이 과정 없음']}
