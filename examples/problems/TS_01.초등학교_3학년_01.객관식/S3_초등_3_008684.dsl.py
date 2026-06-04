from __future__ import annotations
from modu_math.dsl import (
    Canvas,
    ProblemTemplate,
    Region,
    TextSlot,
    RectSlot,
    CircleSlot,
    LineSlot,
    PathSlot,
)


def build_problem_template() -> ProblemTemplate:
    return ProblemTemplate(
        id="S3_초등_3_008684",
        title="누름 못과 띠 종이",
        canvas=Canvas(width=940, height=594, coordinate_mode="logical"),
        regions=(
            Region(
                id="region.header",
                role="stem",
                flow="absolute",
                slot_ids=("slot.qnum", "slot.qtext1"),
            ),
            Region(
                id="region.left_figure",
                role="diagram",
                flow="absolute",
                slot_ids=(
                    "slot.left.frame",
                    "slot.left.circle",
                    "slot.left.ribbon",
                    "slot.left.pin",
                    "slot.left.hand",
                    "slot.left.pencil",
                    "slot.left.arrow1",
                    "slot.left.arrow2",
                    "slot.left.text1",
                    "slot.left.text2",
                ),
            ),
            Region(
                id="region.right_figure",
                role="diagram",
                flow="absolute",
                slot_ids=(
                    "slot.right.frame",
                    "slot.right.circle",
                    "slot.right.center",
                    "slot.right.cross_v",
                    "slot.right.cross_h",
                    "slot.right.p1",
                    "slot.right.p2",
                    "slot.right.p3",
                    "slot.right.p4",
                ),
            ),
            Region(
                id="region.choice",
                role="stem",
                flow="absolute",
                slot_ids=(
                    "slot.choice.frame",
                    "slot.choice.text1",
                    "slot.choice.text2",
                ),
            ),
            Region(id="region.answer", role="answer", flow="absolute", slot_ids=()),
        ),
        slots=(
            TextSlot(
                id="slot.qnum",
                prompt="",
                text="□ 72.  누름 못과 띠 종이를 이용하여 원을 그렸습니다. 그림을 보고 알맞은 말을",
                style_role="question",
                x=20.0,
                y=30.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.qtext1",
                prompt="",
                text="선택하세요.",
                style_role="question",
                x=20.0,
                y=66.0,
                font_size=28,
            ),
            RectSlot(
                id="slot.left.frame",
                prompt="",
                x=240.0,
                y=122.0,
                width=214.0,
                height=214.0,
                fill="none",
            ),
            CircleSlot(
                id="slot.left.circle",
                prompt="",
                cx=344.0,
                cy=226.0,
                r=103.0,
                fill="none",
            ),
            RectSlot(
                id="slot.left.ribbon",
                prompt="",
                x=308.0,
                y=142.0,
                width=122.0,
                height=34.0,
                fill="none",
            ),
            CircleSlot(
                id="slot.left.pin", prompt="", cx=310.0, cy=223.0, r=4.0, fill="#6AA84F"
            ),
            PathSlot(
                id="slot.left.hand",
                prompt="",
                d="M 313.0 290.0 L 333.0 267.0 L 347.0 268.0 L 361.0 286.0 L 360.0 322.0 L 336.0 332.0 L 316.0 312.0 Z",
                fill="none",
            ),
            PathSlot(
                id="slot.left.pencil",
                prompt="",
                d="M 356.0 148.0 L 410.0 185.0",
                fill="none",
            ),
            PathSlot(
                id="slot.left.arrow1",
                prompt="",
                d="M 303.0 210.0 C 250.0 195.0, 236.0 186.0, 214.0 188.0",
                fill="none",
            ),
            PathSlot(
                id="slot.left.arrow2",
                prompt="",
                d="M 410.0 206.0 C 434.0 208.0, 451.0 221.0, 452.0 237.0",
                fill="none",
            ),
            TextSlot(
                id="slot.left.text1",
                prompt="",
                text="① 한쪽 구멍에",
                style_role="diagram",
                x=108.0,
                y=205.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.left.text2",
                prompt="",
                text="누름 못을 꽂아",
                style_role="diagram",
                x=108.0,
                y=235.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.right.text1",
                prompt="",
                text="② 다른 구멍에",
                style_role="diagram",
                x=480.0,
                y=204.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.right.text2",
                prompt="",
                text="연필을 꽂고",
                style_role="diagram",
                x=480.0,
                y=234.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.right.text3",
                prompt="",
                text="한 바퀴 돌려",
                style_role="diagram",
                x=480.0,
                y=264.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.right.text4",
                prompt="",
                text="원을 그려요.",
                style_role="diagram",
                x=480.0,
                y=294.0,
                font_size=28,
            ),
            RectSlot(
                id="slot.right.frame",
                prompt="",
                x=670.0,
                y=122.0,
                width=190.0,
                height=214.0,
                fill="none",
            ),
            CircleSlot(
                id="slot.right.circle",
                prompt="",
                cx=765.0,
                cy=226.0,
                r=103.0,
                fill="none",
            ),
            CircleSlot(
                id="slot.right.center",
                prompt="",
                cx=765.0,
                cy=226.0,
                r=5.0,
                fill="none",
            ),
            LineSlot(
                id="slot.right.cross_v",
                prompt="",
                x1=765.0,
                y1=122.0,
                x2=765.0,
                y2=336.0,
            ),
            LineSlot(
                id="slot.right.cross_h",
                prompt="",
                x1=670.0,
                y1=226.0,
                x2=860.0,
                y2=226.0,
            ),
            CircleSlot(
                id="slot.right.p1", prompt="", cx=765.0, cy=122.0, r=3.5, fill="#222222"
            ),
            CircleSlot(
                id="slot.right.p2", prompt="", cx=860.0, cy=226.0, r=3.5, fill="#222222"
            ),
            CircleSlot(
                id="slot.right.p3", prompt="", cx=765.0, cy=336.0, r=3.5, fill="#222222"
            ),
            CircleSlot(
                id="slot.right.p4", prompt="", cx=670.0, cy=226.0, r=3.5, fill="#222222"
            ),
            RectSlot(
                id="slot.choice.frame",
                prompt="",
                x=98.0,
                y=368.0,
                width=734.0,
                height=118.0,
                fill="none",
            ),
            TextSlot(
                id="slot.choice.text1",
                prompt="",
                text="누름 못이 꽂힌 점에서 원 위에 찍은 4개의 점까지의 길이는",
                style_role="question",
                x=124.0,
                y=414.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.choice.text2",
                prompt="",
                text="모두 ( 같습니다, 다릅니다 ).",
                style_role="question",
                x=275.0,
                y=448.0,
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
    "problem_id": "S3_초등_3_008684",
    "problem_type": "choice_geometry_circle",
    "metadata": {
        "language": "ko",
        "question": "누름 못과 띠 종이를 이용하여 원을 그렸습니다. 그림을 보고 알맞은 말을 선택하세요.",
        "instruction": "같습니다, 다릅니다 중 알맞은 말을 고르는 문제",
    },
    "domain": {
        "objects": [
            {"id": "obj.pin_point", "type": "point", "label": "누름 못이 꽂힌 점"},
            {
                "id": "obj.circle_points",
                "type": "set_of_points",
                "label": "원 위에 찍은 4개의 점",
                "count": 4,
            },
            {"id": "obj.circle", "type": "circle"},
        ],
        "relations": [],
        "problem_solving": {
            "understand": {
                "given_refs": ["obj.pin_point", "obj.circle_points", "obj.circle"],
                "target_ref": "answer.target",
                "condition_refs": ["rel.equal_radii_like_distances"],
            },
            "plan": {
                "method": "circle_distance_property",
                "description": "원 위의 점들은 중심에서 같은 거리에 있다는 성질을 이용해 문장을 판단한다.",
            },
            "execute": {
                "expected_operations": [
                    "identify_center_like_point",
                    "compare_distances_to_points",
                    "select_matching_word",
                ]
            },
            "review": {
                "check_methods": ["circle_property_check", "choice_consistency_check"]
            },
        },
    },
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {"type": "choice_word", "description": "괄호 안에 들어갈 알맞은 말"},
        "value": 1,
        "unit": "",
    },
}

SOLVABLE = {
    "schema": "modu.solvable.v1.1",
    "problem_id": "S3_초등_3_008684",
    "problem_type": "choice_geometry_circle",
    "inputs": {
        "total_ticks": 4,
        "target_label": "괄호 안 선택",
        "target_ticks": 2,
        "target_count": 4,
        "unit": "",
    },
    "given": [
        {"ref": "obj.pin_point", "value": "누름 못이 꽂힌 점"},
        {"ref": "obj.circle_points", "value": "원 위에 찍은 4개의 점"},
        {"ref": "obj.circle", "value": "원"},
    ],
    "target": {"ref": "answer.target", "type": "choice_word"},
    "plan": [
        "원의 성질을 보고, 중심에서 원 위의 점까지의 길이가 서로 같은지 판단한다.",
        "문장의 괄호 안에서 알맞은 말을 고른다.",
    ],
    "method": "circle_property_check",
    "steps": [
        {
            "id": "step.1",
            "expr": "원 위의 점들은 중심에서 같은 거리에 있다",
            "value": True,
        },
        {
            "id": "step.2",
            "expr": "누름 못이 꽂힌 점에서 4개의 점까지의 길이를 비교한다",
            "value": "모두 같음",
        },
        {"id": "step.3", "expr": "괄호 안 선택", "value": "같습니다"},
    ],
    "checks": [
        {
            "id": "check.1",
            "expr": "원의 성질과 일치하는가",
            "expected": True,
            "actual": True,
            "pass": True,
        },
        {
            "id": "check.2",
            "expr": "선택한 말이 문장에 맞는가",
            "expected": "같습니다",
            "actual": "같습니다",
            "pass": True,
        },
    ],
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {"type": "choice_word", "description": "괄호 안에 들어갈 알맞은 말"},
        "value": 1,
        "unit": "",
    },
}
