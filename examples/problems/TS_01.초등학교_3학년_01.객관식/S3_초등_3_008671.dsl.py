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
        id="S3_초등_3_008671",
        title="누름 못과 띠 종이",
        canvas=Canvas(width=947.0, height=312.0, coordinate_mode="logical"),
        regions=(
            Region(
                id="region.stem",
                role="stem",
                flow="absolute",
                slot_ids=("slot.q_num", "slot.q1", "slot.q2"),
            ),
            Region(
                id="region.diagram",
                role="diagram",
                flow="absolute",
                slot_ids=(
                    "slot.band",
                    "slot.pin",
                    "slot.hole.1",
                    "slot.hole.2",
                    "slot.hole.3",
                    "slot.hole.4",
                    "slot.arrow.1",
                    "slot.arrow.2",
                    "slot.arrow.3",
                    "slot.arrow.4",
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
                id="slot.q_num",
                prompt="",
                text="□ 50.",
                style_role="question",
                x=14.0,
                y=34.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.q1",
                prompt="",
                text="누름 못과 띠 종이를 사용하여 원을 그리려고 합니다. 원을 가장 크게 그",
                style_role="question",
                x=58.0,
                y=34.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.q2",
                prompt="",
                text="리려면 어느 구멍에 연필을 꽂아야 하는지 알맞은 기호를 선택하세요.",
                style_role="question",
                x=14.0,
                y=72.0,
                font_size=28,
            ),
            RectSlot(
                id="slot.band", prompt="", x=326.0, y=94.0, width=392.0, height=36.0
            ),
            CircleSlot(
                id="slot.pin", prompt="", cx=396.0, cy=110.0, r=8.0, fill="#8A97A3"
            ),
            CircleSlot(
                id="slot.hole.1", prompt="", cx=484.0, cy=105.0, r=3.5, fill="#FFFFFF"
            ),
            CircleSlot(
                id="slot.hole.2", prompt="", cx=545.0, cy=105.0, r=3.5, fill="#FFFFFF"
            ),
            CircleSlot(
                id="slot.hole.3", prompt="", cx=608.0, cy=105.0, r=3.5, fill="#FFFFFF"
            ),
            CircleSlot(
                id="slot.hole.4", prompt="", cx=671.0, cy=105.0, r=3.5, fill="#FFFFFF"
            ),
            LineSlot(
                id="slot.arrow.1", prompt="", x1=484.0, y1=116.0, x2=484.0, y2=154.0
            ),
            LineSlot(
                id="slot.arrow.2", prompt="", x1=545.0, y1=116.0, x2=545.0, y2=154.0
            ),
            LineSlot(
                id="slot.arrow.3", prompt="", x1=608.0, y1=116.0, x2=608.0, y2=154.0
            ),
            LineSlot(
                id="slot.arrow.4", prompt="", x1=671.0, y1=116.0, x2=671.0, y2=154.0
            ),
            CircleSlot(
                id="slot.choice.1",
                prompt="",
                cx=484.0,
                cy=170.0,
                r=11.0,
                fill="#FFFFFF",
            ),
            CircleSlot(
                id="slot.choice.2",
                prompt="",
                cx=545.0,
                cy=170.0,
                r=11.0,
                fill="#FFFFFF",
            ),
            CircleSlot(
                id="slot.choice.3",
                prompt="",
                cx=608.0,
                cy=170.0,
                r=11.0,
                fill="#FFFFFF",
            ),
            CircleSlot(
                id="slot.choice.4",
                prompt="",
                cx=671.0,
                cy=170.0,
                r=11.0,
                fill="#FFFFFF",
            ),
            TextSlot(
                id="slot.choice_label.1",
                prompt="",
                text="ㄱ",
                style_role="choice",
                x=477.0,
                y=178.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.choice_label.2",
                prompt="",
                text="ㄴ",
                style_role="choice",
                x=538.0,
                y=178.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.choice_label.3",
                prompt="",
                text="ㄷ",
                style_role="choice",
                x=601.0,
                y=178.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.choice_label.4",
                prompt="",
                text="ㄹ",
                style_role="choice",
                x=664.0,
                y=178.0,
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
    "problem_id": "S3_초등_3_008671",
    "problem_type": "multiple_choice",
    "metadata": {
        "language": "ko",
        "question": "누름 못과 띠 종이를 사용하여 원을 그리는 방법을 보고, 원을 가장 크게 그리기 위해 어느 구멍에 연필을 꽂아야 하는지 알맞은 기호를 고르는 문제",
        "instruction": "알맞은 기호를 선택하세요.",
    },
    "domain": {
        "objects": [
            {"id": "obj.pin", "type": "fixed_point", "name": "누름 못"},
            {"id": "obj.paper_strip", "type": "strip", "name": "띠 종이"},
            {"id": "obj.holes", "type": "ordered_positions", "count": 4},
            {
                "id": "obj.options",
                "type": "choice_labels",
                "labels": ["ㄱ", "ㄴ", "ㄷ", "ㄹ"],
            },
        ],
        "relations": [],
        "problem_solving": {
            "understand": {
                "given_refs": [
                    "obj.pin",
                    "obj.paper_strip",
                    "obj.holes",
                    "obj.options",
                ],
                "target_ref": "answer.target",
                "condition_refs": ["rel.distance_circle_size"],
            },
            "plan": {
                "method": "compare_distance_to_select",
                "description": "누름 못과 연필심 사이의 거리가 가장 멀어지도록 대응되는 구멍을 찾는다.",
            },
            "execute": {
                "expected_operations": [
                    "compare_hole_positions",
                    "select_farthest_hole",
                    "match_option_label",
                ]
            },
            "review": {"check_methods": ["distance_order_check", "answer_label_check"]},
        },
    },
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {
            "type": "choice_label",
            "description": "원을 가장 크게 그리기 위해 선택할 기호",
        },
        "value": "ㄹ",
        "unit": "",
    },
}

SOLVABLE = {
    "schema": "modu.solvable.v1.1",
    "problem_id": "S3_초등_3_008671",
    "problem_type": "multiple_choice",
    "inputs": {
        "total_ticks": 4,
        "target_label": "ㄹ",
        "target_ticks": 4,
        "target_count": 1,
        "unit": "",
    },
    "given": [
        {"ref": "obj.pin", "value": "고정점"},
        {"ref": "obj.holes", "value": ["ㄱ", "ㄴ", "ㄷ", "ㄹ"]},
    ],
    "target": {"ref": "answer.target", "type": "choice_label"},
    "method": "distance_compare",
    "plan": [
        "누름 못에서 더 멀리 있는 구멍을 찾는다.",
        "가장 멀리 있는 구멍에 해당하는 기호를 고른다.",
    ],
    "steps": [
        {
            "id": "step.1",
            "expr": "구멍 위치를 왼쪽에서 오른쪽으로 비교한다.",
            "value": "ㄱ < ㄴ < ㄷ < ㄹ",
        },
        {
            "id": "step.2",
            "expr": "가장 먼 구멍에 해당하는 선택지를 찾는다.",
            "value": "ㄹ",
        },
    ],
    "checks": [
        {
            "id": "check.1",
            "expr": "해설의 의미와 선택된 기호가 일치하는가",
            "expected": "ㄹ",
            "actual": "ㄹ",
            "pass": True,
        }
    ],
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {
            "type": "choice_label",
            "description": "원을 가장 크게 그리기 위해 선택할 기호",
        },
        "value": "ㄹ",
        "unit": "",
    },
}
