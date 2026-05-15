from __future__ import annotations
from modu_math.dsl import (
    Canvas,
    ProblemTemplate,
    Region,
    TextSlot,
    RectSlot,
    CircleSlot,
    LineSlot,
)


def build_problem_template() -> ProblemTemplate:
    return ProblemTemplate(
        id="Hpdf_e9nrDzZWUc",
        title="반직선 개수",
        canvas=Canvas(width=560, height=308, coordinate_mode="logical"),
        regions=(
            Region(
                id="region.stem",
                role="stem",
                flow="absolute",
                slot_ids=(
                    "slot.q1",
                    "slot.q2",
                    "slot.diagram.frame",
                    "slot.pt.ㄱ",
                    "slot.pt.ㄴ",
                    "slot.pt.ㄷ",
                    "slot.pt.ㄹ",
                    "slot.pt.ㅁ",
                ),
            ),
        ),
        slots=(
            TextSlot(
                id="slot.q1",
                prompt="",
                text="다음 5개의 점 중에서 2개의 점을 이어 그릴",
                style_role="question",
                x=8.0,
                y=34.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.q2",
                prompt="",
                text="수 있는 반직선은 모두 몇 개인가?",
                style_role="question",
                x=8.0,
                y=66.0,
                font_size=28,
            ),
            RectSlot(
                id="slot.diagram.frame",
                prompt="",
                x=165.0,
                y=126.0,
                width=220.0,
                height=176.0,
                stroke="#777777",
                stroke_width=1.2,
                rx=14.0,
                ry=14.0,
                fill="#FFFFFF",
            ),
            CircleSlot(
                id="slot.pt.ㄱ", prompt="", cx=250.0, cy=155.0, r=3.8, fill="#222222"
            ),
            TextSlot(
                id="slot.lb.ㄱ",
                prompt="",
                text="ㄱ",
                style_role="label",
                x=241.0,
                y=148.0,
                font_size=28,
            ),
            CircleSlot(
                id="slot.pt.ㄴ", prompt="", cx=210.0, cy=193.0, r=3.8, fill="#222222"
            ),
            TextSlot(
                id="slot.lb.ㄴ",
                prompt="",
                text="ㄴ",
                style_role="label",
                x=186.0,
                y=190.0,
                font_size=28,
            ),
            CircleSlot(
                id="slot.pt.ㄷ", prompt="", cx=220.0, cy=249.0, r=3.8, fill="#222222"
            ),
            TextSlot(
                id="slot.lb.ㄷ",
                prompt="",
                text="ㄷ",
                style_role="label",
                x=185.0,
                y=255.0,
                font_size=28,
            ),
            CircleSlot(
                id="slot.pt.ㄹ", prompt="", cx=324.0, cy=194.0, r=3.8, fill="#222222"
            ),
            TextSlot(
                id="slot.lb.ㄹ",
                prompt="",
                text="ㄹ",
                style_role="label",
                x=332.0,
                y=191.0,
                font_size=28,
            ),
            CircleSlot(
                id="slot.pt.ㅁ", prompt="", cx=302.0, cy=250.0, r=3.8, fill="#222222"
            ),
            TextSlot(
                id="slot.lb.ㅁ",
                prompt="",
                text="ㅁ",
                style_role="label",
                x=310.0,
                y=256.0,
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
    "problem_id": "Hpdf_e9nrDzZWUc",
    "problem_type": "counting_geometry",
    "metadata": {
        "language": "ko",
        "question": "다음 5개의 점 중에서 2개의 점을 이어 그릴 수 있는 반직선은 모두 몇 개인가?",
        "instruction": "반직선의 개수를 구하시오.",
    },
    "domain": {
        "objects": [
            {"id": "obj.pt.ㄱ", "type": "point", "label": "ㄱ"},
            {"id": "obj.pt.ㄴ", "type": "point", "label": "ㄴ"},
            {"id": "obj.pt.ㄷ", "type": "point", "label": "ㄷ"},
            {"id": "obj.pt.ㄹ", "type": "point", "label": "ㄹ"},
            {"id": "obj.pt.ㅁ", "type": "point", "label": "ㅁ"},
            {
                "id": "obj.point_set",
                "type": "point_set",
                "count": 5,
                "labels": ["ㄱ", "ㄴ", "ㄷ", "ㄹ", "ㅁ"],
            },
            {"id": "obj.ray_set", "type": "ray_set"},
        ],
        "relations": [
            {
                "id": "rel.select_two_points",
                "type": "choose_2_points",
                "from_id": "obj.point_set",
                "to_id": "obj.ray_set",
                "count": 20,
            }
        ],
        "problem_solving": {
            "understand": {
                "given_refs": ["obj.point_set"],
                "target_ref": "answer.target",
                "condition_refs": ["rel.select_two_points"],
            },
            "plan": {
                "method": "combination_counting",
                "description": "5개의 점에서 서로 다른 2개의 점을 고르면 반직선의 개수를 셀 수 있다.",
            },
            "execute": {
                "expected_operations": [
                    "count_pairs_from_5_points",
                    "interpret_each_pair_as_one_ray",
                ]
            },
            "review": {"check_methods": ["counting_consistency_check"]},
        },
    },
    "answer": {
        "target": {
            "type": "count_of_rays",
            "description": "2개의 점을 이어 그릴 수 있는 반직선의 개수",
        },
        "value": 20,
        "unit": "개",
        "explanation": "5개의 점에서 서로 다른 2점을 고르는 경우의 수는 5C2=10이고, 각 점쌍마다 방향이 다른 반직선 2개가 가능하므로 10×2=20개이다.",
    },
}
SOLVABLE = {   'schema': 'modu.solvable.v1',
    'problem_id': 'Hpdf_e9nrDzZWUc',
    'problem_type': 'counting_geometry',
    'inputs': {   'total_ticks': 5,
                  'target_label': '반직선',
                  'target_ticks': 2,
                  'target_count': 20,
                  'unit': '개'},
    'plan': [   '5개의 점 중에서 서로 다른 2개의 점을 고른다.',
                '고른 두 점의 쌍마다 방향이 다른 반직선 2개를 대응시킨다.',
                '조합 5C2를 계산한 뒤 2를 곱해 전체 개수를 구한다.'],
    'steps': [   {'id': 's1', 'expr': '5C2', 'value': 10},
                 {'expr': '각 점의 쌍은 반직선 2개(AB, BA)에 대응', 'id': 's2', 'value': 20},
                 {'expr': '5C2 × 2', 'id': 's3', 'value': 20}],
    'checks': [{'id': 'c1', 'expr': 'C(5,2)×2', 'expected': 20, 'actual': 20, 'pass': True}],
    'answer': {'value': 20, 'unit': '개'}}
