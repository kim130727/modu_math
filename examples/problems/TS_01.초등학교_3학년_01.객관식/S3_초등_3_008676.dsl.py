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
        id="S3_초등_3_008676",
        title="원의 지름",
        canvas=Canvas(width=928, height=426, coordinate_mode="logical"),
        regions=(
            Region(
                id="region.stem", role="stem", flow="absolute", slot_ids=("slot.q1",)
            ),
            Region(
                id="region.diagram",
                role="diagram",
                flow="absolute",
                slot_ids=(
                    "slot.circle",
                    "slot.center",
                    "slot.line.diameter",
                    "slot.line.vertical",
                    "slot.line.right",
                    "slot.pt.g",
                    "slot.pt.n",
                    "slot.pt.d",
                    "slot.pt.r",
                    "slot.lb.g",
                    "slot.lb.n",
                    "slot.lb.d",
                    "slot.lb.r",
                    "slot.lb.o",
                ),
            ),
            Region(
                id="region.choices",
                role="choices",
                flow="absolute",
                slot_ids=(
                    "slot.choice_box",
                    "slot.choice.1",
                    "slot.choice.2",
                    "slot.choice.3",
                    "slot.choice.4",
                ),
            ),
            Region(id="region.answer", role="answer", flow="absolute", slot_ids=()),
        ),
        slots=(
            TextSlot(
                id="slot.q1",
                prompt="",
                text="59. 원의 지름을 나타내는 선분을 찾아 선택하세요.",
                style_role="question",
                x=14.0,
                y=25.0,
                font_size=28,
            ),
            CircleSlot(
                id="slot.circle", prompt="", cx=507.0, cy=97.0, r=51.0, fill="none"
            ),
            CircleSlot(
                id="slot.center", prompt="", cx=500.0, cy=97.0, r=3.5, fill="#ff4da6"
            ),
            LineSlot(
                id="slot.line.diameter",
                prompt="",
                x1=458.0,
                y1=148.0,
                x2=552.0,
                y2=54.0,
            ),
            LineSlot(
                id="slot.line.vertical",
                prompt="",
                x1=500.0,
                y1=97.0,
                x2=500.0,
                y2=149.0,
            ),
            LineSlot(
                id="slot.line.right", prompt="", x1=551.0, y1=55.0, x2=551.0, y2=149.0
            ),
            CircleSlot(
                id="slot.pt.g", prompt="", cx=458.0, cy=148.0, r=2.0, fill="#222222"
            ),
            CircleSlot(
                id="slot.pt.n", prompt="", cx=500.0, cy=149.0, r=2.0, fill="#222222"
            ),
            CircleSlot(
                id="slot.pt.d", prompt="", cx=551.0, cy=149.0, r=2.0, fill="#222222"
            ),
            CircleSlot(
                id="slot.pt.r", prompt="", cx=552.0, cy=54.0, r=2.0, fill="#222222"
            ),
            TextSlot(
                id="slot.lb.g",
                prompt="",
                text="ㄱ",
                style_role="label",
                x=441.0,
                y=150.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.lb.n",
                prompt="",
                text="ㄴ",
                style_role="label",
                x=492.0,
                y=171.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.lb.d",
                prompt="",
                text="ㄷ",
                style_role="label",
                x=553.0,
                y=151.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.lb.r",
                prompt="",
                text="ㄹ",
                style_role="label",
                x=551.0,
                y=44.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.lb.o",
                prompt="",
                text="ㅇ",
                style_role="label",
                x=511.0,
                y=110.0,
                font_size=28,
            ),
            RectSlot(
                id="slot.choice_box",
                prompt="",
                x=110.0,
                y=170.0,
                width=742.0,
                height=69.0,
                fill="none",
            ),
            TextSlot(
                id="slot.choice.1",
                prompt="",
                text="선분 ㄱㄹ",
                style_role="choice",
                x=150.0,
                y=210.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.choice.2",
                prompt="",
                text="선분 ㅇㄱ",
                style_role="choice",
                x=320.0,
                y=210.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.choice.3",
                prompt="",
                text="선분 ㅇㄴ",
                style_role="choice",
                x=518.0,
                y=210.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.choice.4",
                prompt="",
                text="선분 ㄷㄹ",
                style_role="choice",
                x=718.0,
                y=210.0,
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
    "problem_id": "S3_초등_3_008676",
    "problem_type": "geometry_circle_diameter",
    "metadata": {
        "language": "ko",
        "question": "원의 지름을 나타내는 선분을 찾는 문제",
        "instruction": "원 위의 두 점을 이은 선분 중 원의 중심을 지나는 선분을 고른다.",
    },
    "domain": {
        "objects": [
            {"id": "obj.circle", "type": "circle"},
            {"id": "obj.center", "type": "point", "role": "center"},
            {"id": "obj.segment.gh", "type": "segment", "label": "ㄱㄹ"},
            {"id": "obj.segment.og", "type": "segment", "label": "ㅇㄱ"},
            {"id": "obj.segment.on", "type": "segment", "label": "ㅇㄴ"},
            {"id": "obj.segment.dr", "type": "segment", "label": "ㄷㄹ"},
        ],
        "relations": [],
        "problem_solving": {
            "understand": {
                "given_refs": [
                    "obj.circle",
                    "obj.center",
                    "obj.segment.gh",
                    "obj.segment.og",
                    "obj.segment.on",
                    "obj.segment.dr",
                ],
                "target_ref": "answer.target",
                "condition_refs": ["rel.diameter"],
            },
            "plan": {
                "method": "center_intersection_check",
                "description": "원 위의 두 점을 잇는 선분인지와 중심을 지나는지 확인한다.",
            },
            "execute": {
                "expected_operations": [
                    "identify_candidate_segments",
                    "check_center_passing",
                ]
            },
            "review": {"check_methods": ["compare_with_center", "match_answer_label"]},
        },
    },
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {
            "type": "selected_segment",
            "description": "원의 지름을 나타내는 선분",
        },
        "value": 1,
        "unit": "",
    },
}

SOLVABLE = {
    "schema": "modu.solvable.v1.1",
    "problem_id": "S3_초등_3_008676",
    "problem_type": "geometry_circle_diameter",
    "inputs": {
        "total_ticks": 0,
        "target_label": "선분 ㄱㄹ",
        "target_ticks": 0,
        "target_count": 1,
        "unit": "",
    },
    "given": [
        {"ref": "obj.circle", "value": "circle"},
        {"ref": "obj.center", "value": "center_point"},
        {"ref": "obj.segment.gh", "value": "candidate_segment"},
        {"ref": "obj.segment.og", "value": "candidate_segment"},
        {"ref": "obj.segment.on", "value": "candidate_segment"},
        {"ref": "obj.segment.dr", "value": "candidate_segment"},
    ],
    "target": {"ref": "answer.target", "type": "selected_segment"},
    "method": "center_intersection_check",
    "plan": [
        "원 위의 두 점을 이은 선분인지 확인한다.",
        "원의 중심을 지나는지 확인한다.",
        "조건을 만족하는 선분을 고른다.",
    ],
    "steps": [
        {"id": "step.1", "expr": "선분 ㄱㄹ은 원의 중심을 지난다.", "value": True},
        {
            "id": "step.2",
            "expr": "다른 보기들은 원의 지름 조건을 만족하지 않는다.",
            "value": True,
        },
        {"id": "step.3", "expr": "정답 선택", "value": "선분 ㄱㄹ"},
    ],
    "checks": [
        {
            "id": "check.1",
            "expr": "중심을 지나는가?",
            "expected": True,
            "actual": True,
            "pass": True,
        },
        {
            "id": "check.2",
            "expr": "답이 보기와 일치하는가?",
            "expected": "선분 ㄱㄹ",
            "actual": "선분 ㄱㄹ",
            "pass": True,
        },
    ],
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {
            "type": "selected_segment",
            "description": "원의 지름을 나타내는 선분",
        },
        "value": 1,
        "unit": "",
    },
}
