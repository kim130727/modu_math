from __future__ import annotations
from modu_math.dsl import (
    Canvas,
    CircleSlot,
    LineSlot,
    PathSlot,
    PolygonSlot,
    ProblemTemplate,
    Region,
    RectSlot,
    TextSlot,
)


def build_problem_template() -> ProblemTemplate:
    return ProblemTemplate(
        id="S3_초등_3_008646",
        title="원을 두 번 접어 원의 성질 알아보기",
        canvas=Canvas(width=944.0, height=654.0, coordinate_mode="logical"),
        regions=(
            Region(
                id="region.stem",
                role="stem",
                flow="absolute",
                slot_ids=(
                    "slot.qnum",
                    "slot.stem",
                    "slot.bubble",
                    "slot.bubble.text1",
                    "slot.bubble.text2",
                    "slot.bubble.text3",
                ),
            ),
            Region(
                id="region.diagram",
                role="diagram",
                flow="absolute",
                slot_ids=(
                    "slot.circle1",
                    "slot.arrow1",
                    "slot.fold1",
                    "slot.arrow2",
                    "slot.circle2",
                    "slot.arrow3",
                    "slot.fold2",
                    "slot.arrow4",
                    "slot.circle3",
                    "slot.arrow5",
                    "slot.fold3",
                    "slot.arrow6",
                    "slot.circle4",
                    "slot.arrow7",
                    "slot.green1",
                    "slot.green2",
                    "slot.pinkdot",
                ),
            ),
            Region(
                id="region.answer",
                role="answer",
                flow="absolute",
                slot_ids=("slot.pinkbox",),
            ),
        ),
        slots=(
            TextSlot(
                id="slot.qnum",
                prompt="",
                text="18.",
                style_role="question",
                x=14.0,
                y=28.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.stem",
                prompt="",
                text="원 모양의 종이를 접어 위의 성질을 알아보고 알맞은 말을 선택하세요.",
                style_role="question",
                x=68.0,
                y=28.0,
                font_size=28,
            ),
            CircleSlot(
                id="slot.circle1", prompt="", cx=88.0, cy=304.0, r=58.0, fill="#DFF2F0"
            ),
            LineSlot(
                id="slot.arrow1",
                prompt="",
                x1=180.0,
                y1=304.0,
                x2=214.0,
                y2=304.0,
                stroke="#9A9A9A",
            ),
            PathSlot(
                id="slot.fold1",
                prompt="",
                d="M 262.0 306.0 C 224.0 306.0, 210.0 306.0, 208.0 306.0 C 210.0 338.0, 232.0 357.0, 262.0 357.0",
            ),
            LineSlot(
                id="slot.arrow2",
                prompt="",
                x1=392.0,
                y1=304.0,
                x2=426.0,
                y2=304.0,
                stroke="#9A9A9A",
            ),
            CircleSlot(
                id="slot.circle2", prompt="", cx=518.0, cy=304.0, r=58.0, fill="#DFF2F0"
            ),
            LineSlot(
                id="slot.arrow3",
                prompt="",
                x1=608.0,
                y1=304.0,
                x2=642.0,
                y2=304.0,
                stroke="#9A9A9A",
            ),
            PathSlot(
                id="slot.fold2",
                prompt="",
                d="M 681.0 302.0 C 662.0 269.0, 656.0 248.0, 662.0 244.0 C 683.0 256.0, 702.0 286.0, 725.0 340.0 C 706.0 344.0, 692.0 342.0, 681.0 302.0",
            ),
            LineSlot(
                id="slot.arrow4",
                prompt="",
                x1=790.0,
                y1=304.0,
                x2=824.0,
                y2=304.0,
                stroke="#9A9A9A",
            ),
            CircleSlot(
                id="slot.circle3", prompt="", cx=878.0, cy=304.0, r=58.0, fill="#DFF2F0"
            ),
            LineSlot(
                id="slot.arrow5",
                prompt="",
                x1=512.0,
                y1=230.0,
                x2=528.0,
                y2=210.0,
                stroke="#2AAE96",
            ),
            PathSlot(
                id="slot.fold3",
                prompt="",
                d="M 872.0 305.0 C 840.0 281.0, 828.0 258.0, 826.0 246.0 C 846.0 242.0, 866.0 247.0, 878.0 304.0",
            ),
            LineSlot(
                id="slot.arrow6",
                prompt="",
                x1=878.0,
                y1=304.0,
                x2=878.0,
                y2=248.0,
                stroke="#67C5E2",
            ),
            CircleSlot(
                id="slot.circle4", prompt="", cx=878.0, cy=304.0, r=58.0, fill="#DFF2F0"
            ),
            LineSlot(
                id="slot.arrow7",
                prompt="",
                x1=734.0,
                y1=304.0,
                x2=768.0,
                y2=304.0,
                stroke="#9A9A9A",
            ),
            LineSlot(
                id="slot.green1",
                prompt="",
                x1=835.0,
                y1=236.0,
                x2=900.0,
                y2=236.0,
                stroke="#1E9B53",
            ),
            TextSlot(
                id="slot.green2",
                prompt="",
                text="접힌 선의 윗부분과 아랫부분이 똑같아요.",
                style_role="annotation",
                x=540.0,
                y=241.0,
                font_size=24,
            ),
            CircleSlot(
                id="slot.pinkdot", prompt="", cx=866.0, cy=304.0, r=3.5, fill="#E11A86"
            ),
            RectSlot(
                id="slot.pinkbox",
                prompt="",
                x=98.0,
                y=426.0,
                width=734.0,
                height=116.0,
                fill="#F9E0DA",
            ),
            TextSlot(
                id="slot.bubble",
                prompt="",
                text="원 모양의 종이를 둘로 똑같이 나누어지도록\n접었다가 펼친 다음 다른 방향으로 둘로 똑같이\n나누어지도록 접었다가 펼쳤어.",
                style_role="speech",
                x=318.0,
                y=74.0,
                font_size=26,
            ),
            TextSlot(
                id="slot.bubble.text1",
                prompt="",
                text="",
                style_role="speech",
                x=0.0,
                y=0.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.bubble.text2",
                prompt="",
                text="",
                style_role="speech",
                x=0.0,
                y=0.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.bubble.text3",
                prompt="",
                text="",
                style_role="speech",
                x=0.0,
                y=0.0,
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
    "problem_id": "S3_초등_3_008646",
    "problem_type": "geometry_concept_selection",
    "metadata": {
        "language": "ko",
        "question": "원을 두 번 접어 생긴 선의 성질을 보고 알맞은 말을 고르는 문제",
        "instruction": "알맞은 말을 선택하세요.",
    },
    "domain": {
        "objects": [
            {
                "id": "obj.circle_paper",
                "type": "circle",
                "description": "원 모양의 종이",
            },
            {
                "id": "obj.fold_line",
                "type": "line_segment",
                "description": "원을 둘로 똑같이 나누는 접힌 선",
            },
            {"id": "obj.center", "type": "point", "description": "원의 중심"},
        ],
        "relations": [],
        "problem_solving": {
            "understand": {
                "given_refs": ["obj.circle_paper", "obj.fold_line"],
                "target_ref": "answer.target",
                "condition_refs": ["rel.divides_equally", "rel.passes_center"],
            },
            "plan": {
                "method": "concept_matching",
                "description": "원을 둘로 똑같이 나누는 선이 중심을 지나면 어떤 성질의 선인지 판단한다.",
            },
            "execute": {
                "expected_operations": [
                    "identify_center_passing_segment",
                    "match_to_diameter",
                ]
            },
            "review": {"check_methods": ["definition_consistency_check"]},
        },
    },
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {
            "type": "concept_name",
            "description": "원을 둘로 똑같이 나누는 선분의 이름",
        },
        "value": "지름",
        "unit": "",
    },
}

SOLVABLE = {
    "schema": "modu.solvable.v1.1",
    "problem_id": "S3_초등_3_008646",
    "problem_type": "geometry_concept_selection",
    "inputs": {
        "total_ticks": 0,
        "target_label": "지름",
        "target_ticks": 0,
        "target_count": 1,
        "unit": "",
    },
    "given": [
        {
            "ref": "obj.circle_paper",
            "value": {"type": "circle", "description": "원 모양의 종이"},
        },
        {
            "ref": "obj.fold_line",
            "value": {
                "type": "line_segment",
                "description": "원을 둘로 똑같이 나누는 접힌 선",
            },
        },
    ],
    "target": {"ref": "answer.target", "type": "concept_name"},
    "method": "concept_matching",
    "plan": [
        "접힌 선이 원을 둘로 똑같이 나누는지 확인한다.",
        "그 선이 원의 중심을 지나면 지름인지 판단한다.",
    ],
    "steps": [
        {
            "id": "step.1",
            "expr": "원을 둘로 똑같이 나누는 선분은 원의 중심을 지난다",
            "value": "center_passing_segment",
        },
        {"id": "step.2", "expr": "center_passing_segment → diameter", "value": "지름"},
    ],
    "checks": [
        {
            "id": "check.1",
            "expr": "정의 확인: 원의 중심을 지나면서 원을 둘로 똑같이 나누는가",
            "expected": True,
            "actual": True,
            "pass": True,
        }
    ],
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {
            "type": "concept_name",
            "description": "원을 둘로 똑같이 나누는 선분의 이름",
        },
        "value": "지름",
        "unit": "",
    },
}
