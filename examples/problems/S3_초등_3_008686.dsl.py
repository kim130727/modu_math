from __future__ import annotations
from modu_math.dsl import Canvas, ProblemTemplate, Region, TextSlot, CircleSlot, LineSlot


def build_problem_template() -> ProblemTemplate:
    return ProblemTemplate(
        id="S3_초등_3_008686",
        title="원의 지름을 나타내는 선분 판단",
        canvas=Canvas(width=940, height=469, coordinate_mode="logical"),
        regions=(
            Region(
                id="region.stem",
                role="stem",
                flow="absolute",
                slot_ids=(
                    "slot.qnum",
                    "slot.diagram.circle",
                    "slot.diagram.diameter",
                    "slot.diagram.left_label",
                    "slot.diagram.right_label",
                    "slot.diagram.center_mark",
                    "slot.diagram.pink_dot",
                    "slot.statement",
                    "slot.pt.center",
                ),
            ),
        ),
        slots=(
            TextSlot(
                id="slot.qnum",
                prompt="",
                text="    다음을 읽고 바르게 설명하였으면 ○표, 그렇지 않으면 ×표를 선택하세요.    ",
                style_role="question",
                x=10,
                y=50,
                font_size=30,
            ),
            CircleSlot(
                id="slot.diagram.circle",
                prompt="",
                cx=444,
                cy=189,
                r=90,
                fill="none",
                stroke="#111111",
                stroke_width=2,
            ),
            CircleSlot(
                id="slot.pt.center",
                prompt="",
                cx=445,
                cy=190,
                r=5,
                fill="#ff2aa8",
                stroke="#111111",
                stroke_width=2,
            ),
            LineSlot(
                id="slot.diagram.diameter",
                prompt="",
                x1=355,
                y1=190,
                x2=535,
                y2=190,
                stroke="#111111",
                stroke_width=2,
            ),
            TextSlot(
                id="slot.diagram.left_label",
                prompt="",
                text="ㄱ",
                style_role="label",
                x=310,
                y=195,
                font_size=30,
                fill="#111111",
            ),
            TextSlot(
                id="slot.diagram.right_label",
                prompt="",
                text="ㄴ",
                style_role="label",
                x=560,
                y=190,
                font_size=30,
                fill="#111111",
            ),
            CircleSlot(
                id="slot.diagram.center_mark",
                prompt="",
                cx=450,
                cy=170,
                r=5,
                fill="none",
                stroke="#111111",
                stroke_width=2,
            ),
            CircleSlot(
                id="slot.diagram.pink_dot",
                prompt="",
                cx=445,
                cy=185,
                r=0,
                fill="none",
                stroke="#111111",
                stroke_width=2,
            ),
            TextSlot(
                id="slot.statement",
                prompt="",
                text="원의 지름을 나타내는 선분은 선분 ㄱㄴ입니다.",
                style_role="question",
                x=160,
                y=350,
                font_size=30,
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
    "problem_id": "S3_초등_3_008686",
    "problem_type": "ox_judgment",
    "metadata": {
        "language": "ko",
        "question": "원의 지름을 나타내는 선분이 무엇인지 판단하는 문제",
        "instruction": "다음을 읽고 바르게 설명하였으면 ○표, 그렇지 않으면 ×표를 하세요.",
    },
    "domain": {
        "objects": [
            {"id": "obj.circle", "type": "circle"},
            {"id": "obj.segment_gn", "type": "segment", "label": "ㄱㄴ"},
        ],
        "relations": [],
        "problem_solving": {
            "understand": {
                "given_refs": ["obj.circle", "obj.segment_gn"],
                "target_ref": "answer.target",
                "condition_refs": ["rel.diameter_claim"],
            },
            "plan": {
                "method": "ox_judgment",
                "description": "문장의 내용이 도형의 성질과 맞는지 판단한다.",
            },
            "execute": {
                "expected_operations": ["compare_statement_with_geometry", "judge_true_or_false"]
            },
            "review": {"check_methods": ["statement_consistency_check"]},
        },
    },
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {
            "type": "ox_judgment",
            "description": "선분 ㄱㄴ이 원의 지름을 나타낸다는 설명이 맞는지",
        },
        "value": "○",
        "unit": "",
    },
}

SOLVABLE = {
    "schema": "modu.solvable.v1.1",
    "problem_id": "S3_초등_3_008686",
    "problem_type": "ox_judgment",
    "inputs": {
        "total_ticks": 1,
        "target_label": "선분 ㄱㄴ이 원의 지름인지 판단",
        "target_ticks": 1,
        "target_count": 1,
        "unit": "",
    },
    "given": [
        {"ref": "obj.circle", "value": {"type": "circle"}},
        {"ref": "obj.segment_gn", "value": {"type": "segment", "label": "ㄱㄴ"}},
    ],
    "target": {"ref": "answer.target", "type": "ox_judgment"},
    "method": "ox_judgment",
    "plan": [
        "문장에서 선분 ㄱㄴ이 원의 지름이라고 말하는지 확인한다.",
        "도형의 성질과 문장의 내용이 같으면 ○, 다르면 ×로 판단한다.",
    ],
    "steps": [
        {
            "id": "step.1",
            "expr": "선분 ㄱㄴ의 위치와 원의 중심을 지난다는 관계를 확인한다.",
            "value": "중심을 지나는 선분",
        },
        {
            "id": "step.2",
            "expr": "문장 '선분 ㄱㄴ은 원의 지름을 나타냅니다.'의 진위 판단",
            "value": "○",
        },
    ],
    "checks": [
        {
            "id": "check.1",
            "expr": "문장 내용이 도형의 지름 성질과 일치하는가",
            "expected": "○",
            "actual": "○",
            "pass": True,
        }
    ],
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {
            "type": "ox_judgment",
            "description": "선분 ㄱㄴ이 원의 지름을 나타낸다는 설명이 맞는지",
        },
        "value": "○",
        "unit": "",
    },
}
