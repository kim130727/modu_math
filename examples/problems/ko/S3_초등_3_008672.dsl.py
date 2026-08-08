from __future__ import annotations
from modu_math.dsl import (
    Canvas,
    ProblemTemplate,
    Region,
    TextSlot,
    CircleSlot,
    LineSlot,
)


def build_problem_template() -> ProblemTemplate:
    return ProblemTemplate(
        id="S3_초등_3_008672",
        title="원의 반지름",
        canvas=Canvas(width=700, height=450, coordinate_mode="logical"),
        regions=(
            Region(
                id="region.header",
                role="stem",
                flow="absolute",
                slot_ids=("slot.header.text",),
            ),
            Region(
                id="region.diagram",
                role="diagram",
                flow="absolute",
                slot_ids=(
                    "slot.circle.outer",
                    "slot.line.g1",
                    "slot.line.g2",
                    "slot.line.g3",
                    "slot.lb.ga",
                    "slot.lb.na",
                    "slot.lb.da",
                    "slot.pt.center",
                    "slot.lb.ga.copy1",
                ),
            ),
            Region(
                id="region.question",
                role="stem",
                flow="absolute",
                slot_ids=("slot.q1", "slot.q1.copy2"),
            ),
            Region(id="region.answer", role="answer", flow="absolute", slot_ids=()),
        ),
        slots=(
            TextSlot(
                id="slot.header.text",
                prompt="",
                text="알맞은 말을 선택해 보시오.",
                style_role="question",
                x=34.0,
                y=32.0,
                font_size=28,
            ),
            CircleSlot(
                id="slot.circle.outer",
                prompt="",
                cx=376,
                cy=180,
                r=125,
                fill="none",
            ),
            LineSlot(id="slot.line.g1", prompt="", x1=375, y1=180, x2=265, y2=125),
            LineSlot(id="slot.line.g2", prompt="", x1=375, y1=180, x2=445, y2=285),
            LineSlot(id="slot.line.g3", prompt="", x1=375, y1=180, x2=465, y2=95),
            CircleSlot(
                id="slot.pt.center",
                prompt="",
                cx=375,
                cy=180,
                r=5,
                fill="#d4006a",
            ),
            TextSlot(
                id="slot.lb.ga",
                prompt="",
                text="ㄱ",
                style_role="label",
                x=235,
                y=120,
                font_size=20,
            ),
            TextSlot(
                id="slot.lb.na",
                prompt="",
                text="ㄴ",
                style_role="label",
                x=450,
                y=300,
                font_size=20,
            ),
            TextSlot(
                id="slot.lb.da", prompt="", text="ㄷ", style_role="label", x=475, y=95, font_size=20
            ),
            TextSlot(
                id="slot.q1",
                prompt="",
                text="모두 원의 (지름, 반지름, 중심)입니다.    ",
                style_role="question",
                x=55,
                y=395,
                font_size=30,
            ),
            TextSlot(
                id="slot.lb.ga.copy1",
                prompt="",
                text="ㅇ",
                x=350,
                y=205,
                font_size=20,
                fill="#111111",
            ),
            TextSlot(
                id="slot.q1.copy2",
                prompt="",
                text="        선분 ㄱㅇ, 선분 ㄴㅇ, 선분 ㄷㅇ은",
                x=55,
                y=355,
                font_size=30,
                fill="#111111",
            ),
        ),
        diagrams=(),
        groups=(),
        constraints=(),
        tags=("원의용어", "반지름", "초등수학"),
    )


PROBLEM_TEMPLATE = build_problem_template()

SEMANTIC_OVERRIDE = {
    "problem_id": "S3_초등_3_008672",
    "problem_type": "circle_terms_choice",
    "metadata": {
        "language": "ko",
        "question": "원의 중심과 원 위의 점을 잇는 선분의 이름을 고르는 문제",
        "instruction": "알맞은 말을 선택해 보시오.",
    },
    "domain": {
        "objects": [
            {"id": "obj.circle", "type": "circle"},
            {"id": "obj.center", "type": "point", "label": "O", "role": "center"},
            {"id": "obj.segment.ga", "type": "segment", "label": "ㄱO"},
            {"id": "obj.segment.na", "type": "segment", "label": "ㄴO"},
            {"id": "obj.segment.da", "type": "segment", "label": "ㄷO"},
        ],
        "relations": [],
        "problem_solving": {
            "understand": {
                "given_refs": [
                    "obj.circle",
                    "obj.center",
                    "obj.segment.ga",
                    "obj.segment.na",
                    "obj.segment.da",
                ],
                "target_ref": "answer.target",
                "condition_refs": ["rel.segment_to_radius"],
            },
            "plan": {
                "method": "concept_identification",
                "description": "중심과 원 위의 한 점을 잇는 선분의 이름을 찾는다.",
            },
            "execute": {"expected_operations": ["identify_radius"]},
            "review": {"check_methods": ["definition_match_check"]},
        },
    },
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {
            "type": "circle_term",
            "description": "선분 ㄱㅇ, 선분 ㄴㅇ, 선분 ㄷㅇ에 알맞은 말",
        },
        "value": "반지름",
        "unit": "",
    },
}

SOLVABLE = {
    "schema": "modu.solvable.v1.1",
    "problem_id": "S3_초등_3_008672",
    "problem_type": "circle_terms_choice",
    "inputs": {
        "total_ticks": 3,
        "target_label": "반지름",
        "target_ticks": 1,
        "target_count": 3,
        "unit": "",
    },
    "given": [
        {"ref": "obj.center", "value": {"label": "O"}},
        {"ref": "obj.segment.ga", "value": {"label": "ㄱㅇ"}},
        {"ref": "obj.segment.na", "value": {"label": "ㄴㅇ"}},
        {"ref": "obj.segment.da", "value": {"label": "ㄷㅇ"}},
    ],
    "target": {"ref": "answer.target", "type": "circle_term"},
    "method": "concept_identification",
    "plan": [
        "중심과 원 위의 점을 잇는 선분의 이름을 찾는다.",
        "보기 중 해당하는 말을 고른다.",
    ],
    "steps": [
        {
            "id": "step.1",
            "expr": "ㄱㅇ, ㄴㅇ, ㄷㅇ는 모두 원의 중심 O에서 원 위의 점으로 이어진 선분이다.",
            "value": "center_to_circle_point_segments",
        },
        {
            "id": "step.2",
            "expr": "원의 중심과 원 위의 한 점을 잇는 선분의 이름은 반지름이다.",
            "value": "반지름",
        },
    ],
    "checks": [
        {
            "id": "check.1",
            "expr": "정의와 일치하는가",
            "expected": "반지름",
            "actual": "반지름",
            "pass": True,
        }
    ],
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {
            "type": "circle_term",
            "description": "선분 ㄱㅇ, 선분 ㄴㅇ, 선분 ㄷㅇ에 알맞은 말",
        },
        "value": "반지름",
        "unit": "",
    },
}
