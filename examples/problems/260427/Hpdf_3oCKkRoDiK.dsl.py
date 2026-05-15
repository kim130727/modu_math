from __future__ import annotations

from modu_math.dsl import (
    Canvas,
    CircleSlot,
    ProblemTemplate,
    RectSlot,
    Region,
    TextSlot,
)


def build_problem_template() -> ProblemTemplate:
    canvas = Canvas(
        width=566,
        height=370,
        coordinate_mode="logical",
    )

    regions = (
        Region(
            id="region.stem",
            role="stem",
            flow="absolute",
            slot_ids=(
                "slot.title.l1",
                "slot.title.l2",
                "slot.title.l3",
                "slot.box",
                "slot.pt.g",
                "slot.lbl.g",
                "slot.pt.d",
                "slot.lbl.d",
                "slot.pt.n",
                "slot.lbl.n",
                "slot.pt.r",
                "slot.lbl.r",
                "slot.pt.m",
                "slot.lbl.m",
            ),
        ),
    )

    slots = (
        TextSlot(
            id="slot.title.l1",
            prompt="",
            text="다음 5개의 점 중에서 3개의 점을 이용하여 각",
            style_role="body",
            x=10.0,
            y=45.0,
            font_size=28,
            fill="#222222",
        ),
        TextSlot(
            id="slot.title.l2",
            prompt="",
            text="을 그릴 때 점 ㄹ을 꼭짓점으로 하는 각은 모두",
            style_role="body",
            x=10.0,
            y=95.0,
            font_size=28,
            fill="#222222",
        ),
        TextSlot(
            id="slot.title.l3",
            prompt="",
            text="몇 개입니까?",
            style_role="body",
            x=10.0,
            y=145.0,
            font_size=28,
            fill="#222222",
        ),
        RectSlot(
            id="slot.box",
            prompt="",
            x=155.0,
            y=179.0,
            width=248.0,
            height=179.0,
            rx=15.0,
            ry=15.0,
            stroke="#777777",
            stroke_width=2.0,
            fill="none",
        ),
        CircleSlot(
            id="slot.pt.g",
            prompt="",
            cx=211.0,
            cy=217.0,
            r=4.0,
            stroke="#222222",
            stroke_width=1.0,
            fill="#222222",
            semantic_role="vertex",
        ),
        TextSlot(
            id="slot.lbl.g",
            prompt="",
            text="ㄱ",
            style_role="body",
            x=176.0,
            y=232.0,
            font_size=28,
            fill="#222222",
        ),
        CircleSlot(
            id="slot.pt.d",
            prompt="",
            cx=313.0,
            cy=200.0,
            r=4.0,
            stroke="#222222",
            stroke_width=1.0,
            fill="#222222",
            semantic_role="vertex",
        ),
        TextSlot(
            id="slot.lbl.d",
            prompt="",
            text="ㄷ",
            style_role="body",
            x=324.0,
            y=206.0,
            font_size=28,
            fill="#222222",
        ),
        CircleSlot(
            id="slot.pt.n",
            prompt="",
            cx=223.0,
            cy=295.0,
            r=4.0,
            stroke="#222222",
            stroke_width=1.0,
            fill="#222222",
            semantic_role="vertex",
        ),
        TextSlot(
            id="slot.lbl.n",
            prompt="",
            text="ㄴ",
            style_role="body",
            x=188.0,
            y=316.0,
            font_size=28,
            fill="#222222",
        ),
        CircleSlot(
            id="slot.pt.r",
            prompt="",
            cx=305.0,
            cy=320.0,
            r=4.0,
            stroke="#222222",
            stroke_width=1.0,
            fill="#222222",
            semantic_role="vertex",
        ),
        TextSlot(
            id="slot.lbl.r",
            prompt="",
            text="ㄹ",
            style_role="body",
            x=289.0,
            y=352.0,
            font_size=28,
            fill="#222222",
        ),
        CircleSlot(
            id="slot.pt.m",
            prompt="",
            cx=363.0,
            cy=267.0,
            r=4.0,
            stroke="#222222",
            stroke_width=1.0,
            fill="#222222",
            semantic_role="vertex",
        ),
        TextSlot(
            id="slot.lbl.m",
            prompt="",
            text="ㅁ",
            style_role="body",
            x=348.0,
            y=299.0,
            font_size=28,
            fill="#222222",
        ),
    )

    diagrams = ()
    groups = ()
    constraints = ()

    return ProblemTemplate(
        id="Hpdf_3oCKkRoDiK",
        title="",
        canvas=canvas,
        regions=regions,
        slots=slots,
        diagrams=diagrams,
        groups=groups,
        constraints=constraints,
    )


PROBLEM_TEMPLATE = build_problem_template()

SEMANTIC_OVERRIDE = {
    "problem_id": "Hpdf_3oCKkRoDiK",
    "problem_type": "geometry_counting",
    "metadata": {
        "language": "ko",
        "question": "다음 5개의 점 중에서 3개의 점을 이용하여 각을 그릴 때 점 ㄹ을 꼭짓점으로 하는 각은 모두 몇 개입니까?",
        "instruction": "5개의 점 중 ㄹ을 꼭짓점으로 하는 각의 개수를 구한다.",
    },
    "domain": {
        "objects": [
            {"id": "pt.ㄱ", "type": "point", "label": "ㄱ"},
            {"id": "pt.ㄴ", "type": "point", "label": "ㄴ"},
            {"id": "pt.ㄷ", "type": "point", "label": "ㄷ"},
            {"id": "pt.ㄹ", "type": "point", "label": "ㄹ"},
            {"id": "pt.ㅁ", "type": "point", "label": "ㅁ"},
            {"id": "set.other_pts", "type": "set", "members": ["pt.ㄱ", "pt.ㄴ", "pt.ㄷ", "pt.ㅁ"]},
            {"id": "angle.target", "type": "angle", "vertex": "pt.ㄹ", "side_points": {"type": "combination", "from": "set.other_pts", "count": 2}},
        ],
        "relations": [
            {"id": "rel.count", "type": "count_set", "target": "angle.target"}
        ],
        "problem_solving": {
            "understand": {
                "given_refs": ["set.other_pts", "pt.ㄹ"],
                "target_ref": "answer.target",
                "condition_refs": [],
            },
            "plan": {
                "method": "combination_counting",
                "description": "점 ㄹ을 꼭짓점으로 하므로, 나머지 4개의 점(ㄱ, ㄴ, ㄷ, ㅁ) 중 순서에 상관없이 2개를 고르는 경우의 수를 구한다.",
            },
            "execute": {
                "expected_operations": ["compute_combination"]
            },
            "review": {"check_methods": []},
        },
    },
    "answer": {
        "target": {
            "type": "count",
            "ref": "rel.count",
            "description": "점 ㄹ을 꼭짓점으로 하는 각의 개수",
        },
        "value": 6,
        "unit": "개",
    },
}

SOLVABLE = {   'schema': 'modu.solvable.v1',
    'problem_id': 'Hpdf_3oCKkRoDiK',
    'problem_type': 'geometry_counting',
    'inputs': {   'total_ticks': 6,
                  'target_label': '각의 개수',
                  'target_ticks': 6,
                  'target_count': 6,
                  'unit': '개'},
    'plan': [   '각을 만들기 위해서는 꼭짓점 1개와 변을 이룰 다른 점 2개가 필요하다.',
                '꼭짓점은 점 ㄹ로 고정되어 있다.',
                '남은 4개의 점(ㄱ, ㄴ, ㄷ, ㅁ) 중에서 2개를 고르는 방법의 수를 구한다.',
                '4개 중 2개를 고르는 조합은 (4 × 3) ÷ 2 = 6가지이다.'],
    'steps': [   {'id': 'step.s1', 'expr': '남은 점의 개수', 'value': 4},
                 {'id': 'step.s2', 'expr': '4C2 = (4 * 3) / 2', 'value': 6}],
    'checks': [   {   'id': 'check.c1',
                      'expr': '직접 나열 (ㄱ-ㄹ-ㄴ, ㄱ-ㄹ-ㄷ, ㄱ-ㄹ-ㅁ, ㄴ-ㄹ-ㄷ, ㄴ-ㄹ-ㅁ, ㄷ-ㄹ-ㅁ)',
                      'expected': 6,
                      'actual': 6,
                      'pass': True}],
    'answer': {'value': 6, 'unit': '개'}}
