from __future__ import annotations
from modu_math.dsl import Canvas, ProblemTemplate, Region, TextSlot, RectSlot, PathSlot


def build_problem_template() -> ProblemTemplate:
    return ProblemTemplate(
        id="Hpdf_cvSkK84q3Z",
        title="대화를 보고 직사각형의 한 변의 길이 구하기",
        canvas=Canvas(width=600, height=440, coordinate_mode="logical"),
        regions=(
            Region(
                id="region.stem",
                role="stem",
                flow="absolute",
                slot_ids=(
                    "slot.q1",
                    "slot.msg1",
                    "slot.msg2",
                    "slot.msg3",
                    "slot.name1",
                    "slot.name2",
                    "slot.name3",
                    "slot.bubble1",
                    "slot.bubble2",
                    "slot.bubble3",
                    "slot.arrow1",
                    "slot.arrow2",
                    "slot.arrow3",
                ),
            ),
        ),
        slots=(
            TextSlot(
                id="slot.q1",
                prompt="",
                text="대화를 보고 건우가 가진 액자의 한 변은\n 몇 cm인지 구하시오.",
                style_role="question",
                x=8.0,
                y=30.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.name1",
                prompt="",
                text="〈다희〉",
                style_role="label",
                x=0.0,
                y=130.0,
                font_size=24,
            ),
            TextSlot(
                id="slot.name2",
                prompt="",
                text="〈건우〉",
                style_role="label",
                x=480.0,
                y=230.0,
                font_size=24,
            ),
            TextSlot(
                id="slot.name3",
                prompt="",
                text="〈다희〉",
                style_role="label",
                x=-2.0,
                y=350.0,
                font_size=24,
            ),
            RectSlot(
                id="slot.bubble1",
                prompt="",
                x=96.0,
                y=102.0,
                width=380.0,
                height=84.0,
                stroke="#333333",
                stroke_width=1.5,
                rx=10,
                ry=10,
                fill="none",
            ),
            RectSlot(
                id="slot.bubble2",
                prompt="",
                x=96.0,
                y=210.0,
                width=380.0,
                height=84.0,
                stroke="#333333",
                stroke_width=1.5,
                rx=10,
                ry=10,
                fill="none",
            ),
            RectSlot(
                id="slot.bubble3",
                prompt="",
                x=96.0,
                y=326.0,
                width=380.0,
                height=84.0,
                stroke="#333333",
                stroke_width=1.5,
                rx=10,
                ry=10,
                fill="none",
            ),
            PathSlot(
                id="slot.arrow1",
                prompt="",
                d="M 96 124 L 82 124 L 74 116",
                stroke="#333333",
                stroke_width=1.5,
                fill="none",
            ),
            PathSlot(
                id="slot.arrow2",
                prompt="",
                d="M 476 232 L 490 232 L 498 224",
                stroke="#333333",
                stroke_width=1.5,
                fill="none",
            ),
            PathSlot(
                id="slot.arrow3",
                prompt="",
                d="M 96 348 L 82 348 L 74 340",
                stroke="#333333",
                stroke_width=1.5,
                fill="none",
            ),
            TextSlot(
                id="slot.msg1",
                prompt="",
                text="나는 가로가 8 cm, 세로가 10 cm인\n직사각형 모양의 액자를 가지고 있어.",
                style_role="question",
                x=112.0,
                y=134.0,
                font_size=22,
            ),
            TextSlot(
                id="slot.msg2",
                prompt="",
                text="헉! 내가 가진 액자와 네 변의 길이의 합\n이 같네. 내 액자는 정사각형 모양이지.",
                style_role="question",
                x=112.0,
                y=242.0,
                font_size=22,
            ),
            TextSlot(
                id="slot.msg3",
                prompt="",
                text="그럼 네가 가진 액자의 한 변은 몇 cm\n야?",
                style_role="question",
                x=112.0,
                y=358.0,
                font_size=22,
            ),
        ),
        diagrams=(),
        groups=(),
        constraints=(),
        tags=(),
    )


PROBLEM_TEMPLATE = build_problem_template()
SEMANTIC_OVERRIDE = {
    "problem_id": "Hpdf_cvSkK84q3Z",
    "problem_type": "rectangle_perimeter_square_side",
    "metadata": {
        "language": "ko",
        "question": "대화를 보고 건우가 가진 액자의 한 변은 몇 cm인지 구하시오.",
        "instruction": "대화를 읽고 건우의 정사각형 액자의 한 변의 길이를 구한다.",
    },
    "domain": {
        "objects": [
            {
                "id": "obj.dahee_frame",
                "type": "rectangle",
                "sides": {"width_cm": 8, "height_cm": 10},
            },
            {"id": "obj.gunwoo_frame", "type": "square", "side_cm": None},
        ],
        "relations": [
            {
                "id": "rel.equal_perimeter",
                "type": "same_perimeter",
                "from_id": "obj.dahee_frame",
                "to_id": "obj.gunwoo_frame",
            }
        ],
        "problem_solving": {
            "understand": {
                "given_refs": ["obj.dahee_frame", "rel.equal_perimeter"],
                "target_ref": "answer.target",
                "condition_refs": ["rel.equal_perimeter"],
            },
            "plan": {
                "method": "perimeter_matching",
                "description": "다희의 직사각형 둘레를 구한 뒤, 건우의 정사각형 둘레와 같다고 보고 한 변의 길이를 찾는다.",
            },
            "execute": {
                "expected_operations": [
                    "compute_rectangle_perimeter",
                    "divide_by_4_for_square_side",
                ]
            },
            "review": {
                "check_methods": ["same_perimeter_check", "unit_consistency_check"]
            },
        },
    },
    "answer": {
        "target": {
            "type": "square_side_length",
            "description": "건우가 가진 액자의 한 변의 길이",
        },
        "value": None,
        "unit": "cm",
    },
}
SOLVABLE = {   'schema': 'modu.solvable.v1',
    'problem_id': 'Hpdf_cvSkK84q3Z',
    'problem_type': 'rectangle_perimeter_square_side',
    'inputs': {   'total_ticks': 36,
                  'target_label': '건우가 가진 액자의 한 변의 길이',
                  'target_ticks': 9,
                  'target_count': 9,
                  'unit': 'cm'},
    'plan': ['다희의 직사각형 액자의 둘레를 구한다.', '건우의 정사각형 액자 둘레와 다희의 액자 둘레가 같음을 이용해 한 변의 길이를 구한다.'],
    'steps': [   {'id': 'step.s1', 'expr': '2 × (8 + 10)', 'value': 36},
                 {'id': 'step.s2', 'expr': '36 ÷ 4', 'value': 9}],
    'checks': [   {   'id': 'check.c1',
                      'expr': '정사각형 둘레 확인 (4 × 9)',
                      'expected': 36,
                      'actual': 36,
                      'pass': True}],
    'answer': {'value': 9, 'unit': 'cm'}}
