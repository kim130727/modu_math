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
        title="그림을 보고 알맞은 말을 선택하세요",
        canvas=Canvas(width=900, height=450, coordinate_mode="logical"),
        regions=(
            Region(
                id="region.stem",
                role="stem",
                flow="absolute",
                slot_ids=(
                    "slot.q1",
                    "slot.q2",
                    "slot.q3",
                ),
            ),
            Region(
                id="region.diagram",
                role="diagram",
                flow="absolute",
                slot_ids=(
                    "slot.circle",
                    "slot.center",
                    "slot.lb.g",
                    "slot.lb.n",
                    "slot.lb.d",
                    "slot.lb.r",
                    "slot.line.gr",
                    "slot.line.nr",
                    "slot.line.cd",
                    "slot.lb.d.copy2",
                ),
            ),
            Region(id="region.explain", role="explanation", flow="absolute", slot_ids=()),
        ),
        slots=(
            TextSlot(
                id="slot.q1",
                prompt="",
                text="그림을 보고 알맞은 말을 선택하세요.",
                style_role="question",
                x=40,
                y=35,
                font_size=30,
            ),
            TextSlot(
                id="slot.q2",
                prompt="",
                text="원의 (지름, 반지름)은 원을 둘로 똑같이 나눕니다.",
                style_role="question",
                x=45,
                y=395,
                font_size=30,
            ),
            CircleSlot(id="slot.circle", prompt="", cx=425, cy=220, r=115, fill="none"),
            CircleSlot(id="slot.center", prompt="", cx=425, cy=220, r=5, fill="#d81b60"),
            TextSlot(
                id="slot.lb.g", prompt="", text="ㄱ", style_role="label", x=380, y=105, font_size=30
            ),
            TextSlot(
                id="slot.lb.n", prompt="", text="ㄴ", style_role="label", x=290, y=280, font_size=30
            ),
            TextSlot(
                id="slot.lb.d", prompt="", text="ㄷ", style_role="label", x=490, y=340, font_size=30
            ),
            TextSlot(
                id="slot.lb.r", prompt="", text="ㄹ", style_role="label", x=540, y=185, font_size=30
            ),
            LineSlot(id="slot.line.gr", prompt="", x1=410, y1=105, x2=535, y2=180),
            LineSlot(id="slot.line.nr", prompt="", x1=318, y1=263, x2=533, y2=178),
            LineSlot(id="slot.line.cd", prompt="", x1=425, y1=220, x2=490, y2=315),
            TextSlot(
                id="slot.lb.d.copy2",
                prompt="",
                text="ㅇ",
                x=410,
                y=215,
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
    "steps": [{"id": "step.1", "expr": "문장 속 빈칸에 들어갈 개념 확인", "value": "지름"}],
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
