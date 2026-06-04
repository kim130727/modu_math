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
        id="S3_초등_3_008660",
        title="원의 반지름 찾기",
        canvas=Canvas(width=952, height=406, coordinate_mode="logical"),
        regions=(
            Region(
                id="region.stem",
                role="stem",
                flow="absolute",
                slot_ids=("slot.q_num", "slot.q_text_1", "slot.q_text_2"),
            ),
            Region(
                id="region.diagram",
                role="diagram",
                flow="absolute",
                slot_ids=(
                    "slot.circle",
                    "slot.center",
                    "slot.pt.a",
                    "slot.pt.b",
                    "slot.pt.c",
                    "slot.pt.d",
                    "slot.pt.e",
                    "slot.lb.o",
                    "slot.lb.ga",
                    "slot.lb.na",
                    "slot.lb.da",
                    "slot.lb.ra",
                    "slot.seg.1",
                    "slot.seg.2",
                    "slot.seg.3",
                    "slot.seg.4",
                ),
            ),
            Region(
                id="region.choices",
                role="choices",
                flow="absolute",
                slot_ids=(
                    "slot.choice.ga",
                    "slot.choice.na",
                    "slot.choice.da",
                    "slot.choice.ra",
                ),
            ),
            Region(id="region.answer", role="answer", flow="absolute", slot_ids=()),
        ),
        slots=(
            TextSlot(
                id="slot.q_num",
                prompt="",
                text="35.",
                style_role="question",
                x=10.0,
                y=34.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.q_text_1",
                prompt="",
                text="그림에서 원의 반지름을 나타내는 선분을 찾아 기호를 모두 선택해 보세",
                style_role="question",
                x=52.0,
                y=35.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.q_text_2",
                prompt="",
                text="요.",
                style_role="question",
                x=25.0,
                y=68.0,
                font_size=28,
            ),
            CircleSlot(
                id="slot.circle", prompt="", cx=497.0, cy=160.0, r=77.0, fill="none"
            ),
            CircleSlot(
                id="slot.center", prompt="", cx=486.0, cy=155.0, r=3.5, fill="#ff4fa3"
            ),
            CircleSlot(
                id="slot.pt.a", prompt="", cx=418.0, cy=110.0, r=2.8, fill="#222222"
            ),
            CircleSlot(
                id="slot.pt.b", prompt="", cx=435.0, cy=241.0, r=2.8, fill="#222222"
            ),
            CircleSlot(
                id="slot.pt.c", prompt="", cx=548.0, cy=217.0, r=2.8, fill="#222222"
            ),
            CircleSlot(
                id="slot.pt.d", prompt="", cx=501.0, cy=233.0, r=2.8, fill="#222222"
            ),
            CircleSlot(
                id="slot.pt.e", prompt="", cx=501.0, cy=86.0, r=2.8, fill="#222222"
            ),
            LineSlot(
                id="slot.seg.1",
                prompt="",
                x1=418.0,
                y1=110.0,
                x2=486.0,
                y2=155.0,
                stroke="#222222",
                stroke_width=1.5,
            ),
            LineSlot(
                id="slot.seg.2",
                prompt="",
                x1=418.0,
                y1=110.0,
                x2=501.0,
                y2=233.0,
                stroke="#222222",
                stroke_width=1.5,
            ),
            LineSlot(
                id="slot.seg.3",
                prompt="",
                x1=435.0,
                y1=241.0,
                x2=486.0,
                y2=155.0,
                stroke="#222222",
                stroke_width=1.5,
            ),
            LineSlot(
                id="slot.seg.4",
                prompt="",
                x1=435.0,
                y1=241.0,
                x2=548.0,
                y2=217.0,
                stroke="#222222",
                stroke_width=1.5,
            ),
            TextSlot(
                id="slot.lb.o",
                prompt="",
                text="ㅇ",
                style_role="label",
                x=482.0,
                y=141.0,
                font_size=24,
            ),
            TextSlot(
                id="slot.lb.ga",
                prompt="",
                text="ㄱ",
                style_role="label",
                x=407.0,
                y=101.0,
                font_size=24,
            ),
            TextSlot(
                id="slot.lb.na",
                prompt="",
                text="ㄴ",
                style_role="label",
                x=414.0,
                y=253.0,
                font_size=24,
            ),
            TextSlot(
                id="slot.lb.da",
                prompt="",
                text="ㄷ",
                style_role="label",
                x=502.0,
                y=248.0,
                font_size=24,
            ),
            TextSlot(
                id="slot.lb.ra",
                prompt="",
                text="ㄹ",
                style_role="label",
                x=559.0,
                y=212.0,
                font_size=24,
            ),
            TextSlot(
                id="slot.choice.ga",
                prompt="",
                text="⑴  가  선분  ㅇㄱ",
                style_role="choice",
                x=115.0,
                y=270.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.choice.na",
                prompt="",
                text="⑵  나  선분  ㅇㄴ",
                style_role="choice",
                x=300.0,
                y=270.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.choice.da",
                prompt="",
                text="⑶  다  선분  ㄱㄷ",
                style_role="choice",
                x=545.0,
                y=270.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.choice.ra",
                prompt="",
                text="⑷  라  선분  ㄴㄹ",
                style_role="choice",
                x=735.0,
                y=270.0,
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
    "problem_id": "S3_초등_3_008660",
    "problem_type": "geometry_radius_selection",
    "metadata": {
        "language": "ko",
        "question": "그림에서 원의 반지름을 나타내는 선분을 찾아 기호를 모두 선택해 보세요.",
        "instruction": "기호를 모두 선택하시오.",
    },
    "domain": {
        "objects": [
            {"id": "obj.circle", "type": "circle"},
            {"id": "obj.center", "type": "center", "label": "ㅇ"},
            {"id": "obj.radius_candidate_1", "type": "segment", "label": "ㅇㄱ"},
            {"id": "obj.radius_candidate_2", "type": "segment", "label": "ㅇㄴ"},
        ],
        "relations": [],
        "problem_solving": {
            "understand": {
                "given_refs": ["obj.circle", "obj.center"],
                "target_ref": "answer.target",
                "condition_refs": ["rel.radius_from_center_to_point"],
            },
            "plan": {
                "method": "identify_radius_by_center_and_point",
                "description": "원의 중심과 원 위의 점을 잇는 선분을 반지름으로 찾는다.",
            },
            "execute": {
                "expected_operations": [
                    "compare_center_to_boundary_segments",
                    "select_radius_labels",
                ]
            },
            "review": {"check_methods": ["center_to_circle_boundary_check"]},
        },
    },
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {
            "type": "multiple_choice_labels",
            "description": "원의 반지름을 나타내는 선분의 보기 기호",
        },
        "value": 2,
        "unit": "",
    },
}

SOLVABLE = {
    "schema": "modu.solvable.v1.1",
    "problem_id": "S3_초등_3_008660",
    "problem_type": "geometry_radius_selection",
    "inputs": {
        "total_ticks": 0,
        "target_label": "원의 반지름을 나타내는 선분",
        "target_ticks": 0,
        "target_count": 2,
        "unit": "",
    },
    "given": [
        {"ref": "obj.center", "value": {"label": "ㅇ"}},
        {"ref": "obj.radius_candidate_1", "value": {"label": "ㅇㄱ"}},
        {"ref": "obj.radius_candidate_2", "value": {"label": "ㅇㄴ"}},
    ],
    "target": {"ref": "answer.target", "type": "multiple_choice_labels"},
    "method": "identify_radius_by_center_and_point",
    "plan": [
        "원의 중심 ㅇ에서 원 위의 점으로 이어진 선분을 찾는다.",
        "반지름에 해당하는 보기 기호를 고른다.",
    ],
    "steps": [
        {
            "id": "step.1",
            "expr": "원의 중심 ㅇ과 원 위의 점을 잇는 선분 확인",
            "value": "ㅇㄱ, ㅇㄴ",
        },
        {"id": "step.2", "expr": "반지름에 해당하는 보기 기호 선택", "value": "가, 나"},
    ],
    "checks": [
        {
            "id": "check.1",
            "expr": "중심 ㅇ을 포함하고 원 위의 점까지 이어지는 선분인지 확인",
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
            "type": "multiple_choice_labels",
            "description": "원의 반지름을 나타내는 선분의 보기 기호",
        },
        "value": 2,
        "unit": "",
    },
}
