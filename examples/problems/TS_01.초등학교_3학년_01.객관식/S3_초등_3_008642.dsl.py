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
        id="S3_초등_3_008642",
        title="지름의 개수",
        canvas=Canvas(width=945.0, height=650.0, coordinate_mode="logical"),
        regions=(
            Region(
                id="region.stem",
                role="stem",
                flow="absolute",
                slot_ids=(
                    "slot.q1",
                    "slot.title_marker",
                    "slot.diagram.circle",
                    "slot.diagram.diameter1",
                    "slot.diagram.diameter2",
                    "slot.diagram.diameter3",
                    "slot.diagram.center",
                    "slot.diagram.label.eunji",
                    "slot.diagram.label.jina",
                    "slot.diagram.label.hyeonjun",
                    "slot.diagram.note",
                    "slot.diagram.arrow",
                    "slot.choice.box",
                    "slot.choice.text",
                ),
            ),
        ),
        slots=(
            TextSlot(
                id="slot.title_marker",
                prompt="",
                text="□ 14.",
                style_role="question",
                x=10.0,
                y=32.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.q1",
                prompt="",
                text="은지, 진아, 현준이가 한 원에 지름을 그은 것입니다. 한 원에 지름을 몇 개 그을 수 있는지 알맞은 것을 선택하세요.",
                style_role="question",
                x=48.0,
                y=32.0,
                font_size=28,
            ),
            CircleSlot(
                id="slot.diagram.circle",
                prompt="",
                cx=456.0,
                cy=230.0,
                r=117.0,
                fill="none",
            ),
            LineSlot(
                id="slot.diagram.diameter1",
                prompt="",
                x1=456.0,
                y1=113.0,
                x2=456.0,
                y2=347.0,
            ),
            LineSlot(
                id="slot.diagram.diameter2",
                prompt="",
                x1=365.0,
                y1=173.0,
                x2=547.0,
                y2=287.0,
            ),
            LineSlot(
                id="slot.diagram.diameter3",
                prompt="",
                x1=352.0,
                y1=263.0,
                x2=560.0,
                y2=198.0,
            ),
            CircleSlot(
                id="slot.diagram.center",
                prompt="",
                cx=456.0,
                cy=230.0,
                r=3.8,
                fill="#cc2aa5",
            ),
            TextSlot(
                id="slot.diagram.label.eunji",
                prompt="",
                text="은지",
                style_role="label",
                x=462.0,
                y=100.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.diagram.label.jina",
                prompt="",
                text="진아",
                style_role="label",
                x=592.0,
                y=197.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.diagram.label.hyeonjun",
                prompt="",
                text="현준",
                style_role="label",
                x=578.0,
                y=301.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.diagram.note",
                prompt="",
                text="지름은 모두\n원의 중심을\n지나요.",
                style_role="annotation",
                x=512.0,
                y=386.0,
                font_size=28,
            ),
            LineSlot(
                id="slot.diagram.arrow",
                prompt="",
                x1=507.0,
                y1=373.0,
                x2=457.0,
                y2=232.0,
            ),
            RectSlot(
                id="slot.choice.box",
                prompt="",
                x=102.0,
                y=413.0,
                width=749.0,
                height=79.0,
                fill="none",
            ),
            TextSlot(
                id="slot.choice.text",
                prompt="",
                text="( 무수히 많이 그을 수 있습니다. , 3개 )",
                style_role="choice",
                x=239.0,
                y=463.0,
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
    "problem_id": "S3_초등_3_008642",
    "problem_type": "conceptual_choice",
    "metadata": {
        "language": "ko",
        "question": "한 원에 지름을 몇 개 그을 수 있는지 알맞은 것을 선택하는 문제",
        "instruction": "알맞은 것을 선택하세요.",
    },
    "domain": {
        "objects": [
            {"id": "obj.circle", "type": "circle"},
            {"id": "obj.diameter", "type": "diameter", "count": "multiple"},
            {"id": "obj.center", "type": "center"},
        ],
        "relations": [],
        "problem_solving": {
            "understand": {
                "given_refs": ["obj.circle", "obj.center", "obj.diameter"],
                "target_ref": "answer.target",
                "condition_refs": ["rel.diameter_through_center"],
            },
            "plan": {
                "method": "definition_check",
                "description": "지름의 정의를 확인해 한 원에 가능한 지름의 개수를 판단한다.",
            },
            "execute": {
                "expected_operations": ["identify_definition", "compare_choices"]
            },
            "review": {"check_methods": ["definition_consistency_check"]},
        },
    },
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {
            "type": "choice",
            "description": "한 원에 지름을 몇 개 그을 수 있는지에 대한 알맞은 선택지",
        },
        "value": 0,
        "unit": "",
    },
}

SOLVABLE = {
    "schema": "modu.solvable.v1.1",
    "problem_id": "S3_초등_3_008642",
    "problem_type": "conceptual_choice",
    "inputs": {
        "total_ticks": 0,
        "target_label": "한 원에 지름을 몇 개 그을 수 있는지",
        "target_ticks": 0,
        "target_count": 0,
        "unit": "",
    },
    "given": [
        {"ref": "obj.circle", "value": {"type": "circle"}},
        {"ref": "obj.center", "value": {"type": "center"}},
        {"ref": "obj.diameter", "value": {"count": "multiple"}},
    ],
    "target": {"ref": "answer.target", "type": "choice"},
    "method": "definition_check",
    "plan": [
        "지름의 정의를 확인한다.",
        "한 원에 그을 수 있는 지름의 개수를 판단한다.",
        "보기와 일치하는 선택지를 고른다.",
    ],
    "steps": [
        {
            "id": "step.1",
            "expr": "지름은 원의 중심을 지나고 원 위의 두 점을 잇는 선분이다.",
            "value": "definition",
        },
        {
            "id": "step.2",
            "expr": "원의 중심을 지나는 방향은 여러 가지가 가능하다.",
            "value": "multiple",
        },
        {
            "id": "step.3",
            "expr": "따라서 한 원에 지름은 무수히 많이 그을 수 있다.",
            "value": "무수히 많이",
        },
    ],
    "checks": [
        {
            "id": "check.1",
            "expr": "지름이 중심을 지나는가",
            "expected": True,
            "actual": True,
            "pass": True,
        },
        {
            "id": "check.2",
            "expr": "선택지가 정의와 일치하는가",
            "expected": "무수히 많이 그을 수 있습니다.",
            "actual": "무수히 많이 그을 수 있습니다.",
            "pass": True,
        },
    ],
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {
            "type": "choice",
            "description": "한 원에 지름을 몇 개 그을 수 있는지에 대한 알맞은 선택지",
        },
        "value": 0,
        "unit": "",
    },
}
