from __future__ import annotations
from modu_math.dsl import (
    Canvas,
    CircleSlot,
    LineSlot,
    ProblemTemplate,
    Region,
    TextSlot,
)


def build_problem_template() -> ProblemTemplate:
    return ProblemTemplate(
        id="S3_초등_3_008649",
        title="원의 지름",
        canvas=Canvas(width=660, height=360, coordinate_mode="logical"),
        regions=(
            Region(
                id="region.header",
                role="stem",
                flow="absolute",
                slot_ids=("slot.instruction",),
            ),
            Region(
                id="region.diagram",
                role="diagram",
                flow="absolute",
                slot_ids=(
                    "slot.circle_outline",
                    "slot.center_point",
                    "slot.line_top_right",
                    "slot.line_left_right",
                    "slot.line_center_down",
                    "slot.lb.ㄱ",
                    "slot.lb.ㄴ",
                    "slot.lb.ㄷ",
                    "slot.lb.ㄹ",
                ),
            ),
            Region(
                id="region.body",
                role="stem",
                flow="absolute",
                slot_ids=("slot.sentence1", "slot.sentence2", "slot.choice"),
            ),
        ),
        slots=(
            TextSlot(
                id="slot.instruction",
                prompt="",
                text = '그림을 보고 알맞은 말을 선택하세요.', style_role="question",
                x = 10, y = 30, font_size = 30),
            CircleSlot(
                id="slot.circle_outline",
                prompt="",
                cx = 265, cy = 140, r = 65, fill="none",
            ),
            CircleSlot(
                id="slot.center_point",
                prompt="",
                cx = 250, cy = 150, r = 5, fill="#d81b60",
            ),
            LineSlot(
                id="slot.line_top_right",
                prompt="",
                x1 = 245, y1 = 75, x2 = 330, y2 = 125),
            LineSlot(
                id="slot.line_left_right",
                prompt="",
                x1 = 180, y1 = 175, x2 = 330, y2 = 125),
            LineSlot(
                id="slot.line_center_down",
                prompt="",
                x1 = 250, y1 = 150, x2 = 280, y2 = 215),
            TextSlot(
                id="slot.lb.ㄱ",
                prompt="",
                text = 'ㄱ', style_role="label",
                x = 235, y = 65, font_size = 30),
            TextSlot(
                id="slot.lb.ㄴ",
                prompt="",
                text = 'ㄴ', style_role="label",
                x = 160, y = 185, font_size = 30),
            TextSlot(
                id="slot.lb.ㄷ",
                prompt="",
                text = 'ㄷ', style_role="label",
                x = 285, y = 230, font_size = 30),
            TextSlot(
                id="slot.lb.ㄹ",
                prompt="",
                text = 'ㄹ', style_role="label",
                x = 340, y = 135, font_size = 30),
            TextSlot(
                id="slot.sentence1",
                prompt="",
                text="원의 ( 지름, 반지름 )은 원을 둘로 똑같이 나눕니다.",
                style_role="question",
                x=12.0,
                y=268.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.sentence2",
                prompt="",
                text="원의 지름은 원을 둘로 똑같이 나눕니다.",
                style_role="question",
                x=12.0,
                y=308.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.choice",
                prompt="",
                text="지름",
                style_role="question",
                x=12.0,
                y=348.0,
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
    "problem_id": "S3_초등_3_008649",
    "problem_type": "circle_concept_choice",
    "metadata": {
        "language": "ko",
        "question": "그림을 보고 알맞은 말을 선택하세요.",
        "instruction": "원의 구성 요소 이름을 고르는 문제",
    },
    "domain": {
        "objects": [
            {"id": "obj.circle", "type": "circle"},
            {"id": "obj.center", "type": "point", "role": "center"},
            {"id": "obj.diameter", "type": "segment", "role": "diameter"},
            {"id": "obj.radius", "type": "segment", "role": "radius"},
        ],
        "relations": [],
        "problem_solving": {
            "understand": {
                "given_refs": [
                    "obj.circle",
                    "obj.center",
                    "obj.diameter",
                    "obj.radius",
                ],
                "target_ref": "answer.target",
                "condition_refs": ["rel.diameter_divides_circle"],
            },
            "plan": {
                "method": "concept_choice",
                "description": "그림과 문장을 보고 원을 둘로 똑같이 나누는 이름을 찾는다.",
            },
            "execute": {
                "expected_operations": [
                    "identify_circle_part_name",
                    "match_sentence_to_concept",
                ]
            },
            "review": {"check_methods": ["concept_consistency_check"]},
        },
    },
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {"type": "concept_name", "description": "원을 둘로 똑같이 나누는 말"},
        "value": "지름",
        "unit": "",
    },
}

SOLVABLE = {
    "schema": "modu.solvable.v1.1",
    "problem_id": "S3_초등_3_008649",
    "problem_type": "circle_concept_choice",
    "inputs": {
        "total_ticks": 0,
        "target_label": "원을 둘로 똑같이 나누는 말",
        "target_ticks": 0,
        "target_count": 0,
        "unit": "",
    },
    "given": [
        {"ref": "obj.circle", "value": "circle"},
        {"ref": "obj.diameter", "value": "segment"},
        {"ref": "obj.radius", "value": "segment"},
    ],
    "target": {"ref": "answer.target", "type": "concept_name"},
    "method": "concept_choice",
    "plan": ["그림과 문장을 보고 원을 둘로 똑같이 나누는 말을 찾는다."],
    "steps": [
        {"id": "step.1", "expr": "문장 속 빈칸에 들어갈 개념 확인", "value": "지름"}
    ],
    "checks": [
        {
            "id": "check.1",
            "expr": "원의 지름은 원을 둘로 똑같이 나누는가",
            "expected": True,
            "actual": True,
            "pass": True,
        }
    ],
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {"type": "concept_name", "description": "원을 둘로 똑같이 나누는 말"},
        "value": "지름",
        "unit": "",
    },
}
