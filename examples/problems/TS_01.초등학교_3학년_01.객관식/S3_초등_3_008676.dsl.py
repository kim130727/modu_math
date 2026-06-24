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
            Region(id="region.stem", role="stem", flow="absolute", slot_ids=("slot.q1",)),
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
                text="원의 지름을 나타내는 선분을 찾아 선택하세요.",
                style_role="question",
                x=30,
                y=40,
                font_size=30,
            ),
            CircleSlot(id="slot.circle", prompt="", cx=399, cy=170, r=105, fill="none"),
            CircleSlot(id="slot.center", prompt="", cx=400, cy=170, r=5, fill="#ff4da6"),
            LineSlot(id="slot.line.diameter", prompt="", x1=310, y1=225, x2=490, y2=115),
            LineSlot(id="slot.line.vertical", prompt="", x1=490, y1=115, x2=490, y2=220),
            LineSlot(id="slot.line.right", prompt="", x1=400, y1=170, x2=400, y2=275),
            TextSlot(
                id="slot.lb.g", prompt="", text="ㄱ", style_role="label", x=270, y=235, font_size=30
            ),
            TextSlot(
                id="slot.lb.n",
                prompt="",
                text="ㄴ",
                style_role="label",
                x=400,
                y=304,
                font_size=30,
                max_width=800,
            ),
            TextSlot(
                id="slot.lb.d", prompt="", text="ㄷ", style_role="label", x=505, y=250, font_size=30
            ),
            TextSlot(
                id="slot.lb.r", prompt="", text="ㄹ", style_role="label", x=495, y=110, font_size=30
            ),
            TextSlot(
                id="slot.lb.o", prompt="", text="ㅇ", style_role="label", x=375, y=160, font_size=30
            ),
            RectSlot(
                id="slot.choice_box",
                prompt="",
                x=40,
                y=309,
                width=740,
                height=70,
                fill="none",
            ),
            TextSlot(
                id="slot.choice.1",
                prompt="",
                text="1. 선분 ㄱㄹ",
                style_role="choice",
                x=80,
                y=355,
                font_size=30,
                max_width=800,
            ),
            TextSlot(
                id="slot.choice.2",
                prompt="",
                text="2. 선분 ㅇㄱ",
                style_role="choice",
                x=255,
                y=355,
                font_size=30,
                max_width=800,
            ),
            TextSlot(
                id="slot.choice.3",
                prompt="",
                text="3. 선분 ㅇㄴ",
                style_role="choice",
                x=430,
                y=355,
                font_size=30,
                max_width=800,
            ),
            TextSlot(
                id="slot.choice.4",
                prompt="",
                text="4. 선분 ㄷㄹ",
                style_role="choice",
                x=595,
                y=355,
                font_size=30,
                max_width=800,
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
