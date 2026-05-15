from __future__ import annotations

from modu_math.dsl import Canvas, ProblemTemplate, Region, TextSlot


def build_problem_template() -> ProblemTemplate:
    return ProblemTemplate(
        id="Hpdf_67IWfsGbkY",
        title="구슬 나눔",
        canvas=Canvas(width=800, height=294, coordinate_mode="logical"),
        regions=(
            Region(
                id="region.stem",
                role="stem",
                flow="absolute",
                slot_ids=(
                    "slot.q1",
                    "slot.q2",
                    "slot.q3",
                    "slot.q4",
                    "slot.q5",
                    "slot.q6",
                ),
            ),
        ),
        slots=(
            TextSlot(
                id="slot.q1",
                prompt="",
                text="(가), (나), (다) 세 사람은 구슬 게임을 합니다.",
                style_role="question",
                x=18.0,
                y=34.0,
                font_size=24,
                anchor="start",
                fill="#111111",
            ),
            TextSlot(
                id="slot.q2",
                prompt="",
                text="게임에서 진 사람은 이긴 사람이 갖고 있는 수만큼 구슬을 주기로 하였습니다.",
                style_role="question",
                x=18.0,
                y=70.0,
                font_size=24,
                anchor="start",
                fill="#111111",
            ),
            TextSlot(
                id="slot.q3",
                prompt="",
                text="첫 번째 게임에서 (나)는 (가)와 (다)에게 졌습니다.",
                style_role="question",
                x=18.0,
                y=106.0,
                font_size=24,
                anchor="start",
                fill="#111111",
            ),
            TextSlot(
                id="slot.q4",
                prompt="",
                text="두 번째 게임에서 (가)는 (나)와 (다)에게 졌습니다.",
                style_role="question",
                x=18.0,
                y=142.0,
                font_size=24,
                anchor="start",
                fill="#111111",
            ),
            TextSlot(
                id="slot.q5",
                prompt="",
                text="두 번의 게임이 끝난 후 세 사람이 가지고 있는 구슬은 각각 240개로 같았습니다.",
                style_role="question",
                x=18.0,
                y=178.0,
                font_size=24,
                anchor="start",
                fill="#111111",
            ),
            TextSlot(
                id="slot.q6",
                prompt="",
                text="게임을 시작하기 전 (나)가 가지고 있던 구슬은 몇 개입니까?",
                style_role="question",
                x=18.0,
                y=214.0,
                font_size=24,
                anchor="start",
                fill="#111111",
            ),
        ),
        diagrams=(),
        groups=(),
        constraints=(),
        tags=(),
    )


PROBLEM_TEMPLATE = build_problem_template()

SEMANTIC_OVERRIDE = {
    "problem_id": "Hpdf_67IWfsGbkY",
    "problem_type": "equation_word_problem",
    "metadata": {
        "language": "ko",
        "question": "두 번의 게임 후 세 사람이 각각 240개일 때 시작 전 (나)의 구슬 수를 구하는 문제",
        "instruction": "게임 규칙과 최종 상태를 이용해 시작 전 (나)의 구슬 개수를 구하시오.",
    },
    "domain": {
        "objects": [
            {"id": "obj.A", "type": "person", "name": "(가)"},
            {"id": "obj.B", "type": "person", "name": "(나)"},
            {"id": "obj.C", "type": "person", "name": "(다)"},
            {
                "id": "obj.final_each",
                "type": "quantity",
                "name": "게임 후 각 사람의 구슬 수",
            },
            {
                "id": "obj.initial_B",
                "type": "quantity",
                "name": "시작 전 (나)의 구슬 수",
            },
        ],
        "relations": [
            {
                "id": "rel.game1",
                "type": "loses_to",
                "from_id": "obj.B",
                "to_id": "obj.A",
            },
            {
                "id": "rel.game1_2",
                "type": "loses_to",
                "from_id": "obj.B",
                "to_id": "obj.C",
            },
            {
                "id": "rel.game2",
                "type": "loses_to",
                "from_id": "obj.A",
                "to_id": "obj.B",
            },
            {
                "id": "rel.game2_2",
                "type": "loses_to",
                "from_id": "obj.A",
                "to_id": "obj.C",
            },
            {
                "id": "rel.final_equal",
                "type": "equal_amount",
                "from_id": "obj.A",
                "to_id": "obj.B",
            },
            {
                "id": "rel.final_equal_2",
                "type": "equal_amount",
                "from_id": "obj.B",
                "to_id": "obj.C",
            },
        ],
        "problem_solving": {
            "understand": {
                "given_refs": [
                    "obj.final_each",
                    "rel.game1",
                    "rel.game1_2",
                    "rel.game2",
                    "rel.game2_2",
                ],
                "target_ref": "answer.target",
                "condition_refs": ["rel.final_equal", "rel.final_equal_2"],
            },
            "plan": {
                "method": "equation_modeling",
                "description": "게임별 구슬 이동을 식으로 세우고 최종 A=B=C=240 조건으로 초기 (나)를 구한다.",
            },
            "execute": {
                "expected_operations": [
                    "각 게임 후 A, B, C 변화를 식으로 표현한다",
                    "최종 상태 A=B=C=240을 반영한다",
                    "초기 (나)의 값을 계산한다",
                ]
            },
            "review": {
                "check_methods": [
                    "계산한 초기값을 게임 규칙에 대입해 최종 240 검산",
                    "구슬 개수 단위 일치 확인",
                ]
            },
        },
    },
    "answer": {
        "target": {
            "type": "initial_amount",
            "description": "게임 시작 전 (나)가 가지고 있던 구슬 수",
        },
        "value": 420,
        "unit": "개",
    },
}

SOLVABLE = {   'schema': 'modu.solvable.v1',
    'problem_id': 'Hpdf_67IWfsGbkY',
    'problem_type': 'equation_word_problem',
    'inputs': {   'total_ticks': 3,
                  'target_label': '시작 전 (나)의 구슬 수',
                  'target_ticks': 1,
                  'target_count': 240,
                  'unit': '개'},
    'plan': [   '첫째/둘째 게임에서의 구슬 이동을 식으로 정리한다.',
                '최종 상태가 A=B=C=240이라는 조건을 적용한다.',
                '초기 (나)의 구슬 수를 계산하고 검산한다.'],
    'steps': [   {   'id': 'step.s1',
                     'expr': '초기값을 A=a, B=b, C=c로 두고 규칙대로 게임 후 식을 만든다.',
                     'value': None},
                 {   'id': 'step.s2',
                     'expr': '최종식에서 C=240 -> c=60, B=240 -> b-a=180, A=240 -> 3a-b=300을 얻는다.',
                     'value': None},
                 {   'id': 'step.s3',
                     'expr': '연립하면 a=240, b=420, c=60이므로 시작 전 (나)는 420개이다.',
                     'value': 420}],
    'checks': [   {   'id': 'check.c1',
                      'expr': 'a=240, b=420, c=60을 두 게임 규칙에 대입하면 최종 A=B=C=240인지 확인',
                      'expected': {'A': 240, 'B': 240, 'C': 240, 'unit': '개'},
                      'actual': {'A': 240, 'B': 240, 'C': 240, 'unit': '개'},
                      'pass': True}],
    'answer': {'value': 420, 'unit': '개'}}
