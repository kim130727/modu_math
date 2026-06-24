from __future__ import annotations
from modu_math.dsl import Canvas, ProblemTemplate, Region, RectSlot, TextSlot


def build_problem_template() -> ProblemTemplate:
    return ProblemTemplate(
        id="S3_초등_3_009065",
        title="알맞은 말을 선택하세요",
        canvas=Canvas(width=766, height=243, coordinate_mode="logical"),
        regions=(
            Region(
                id="region.header",
                role="stem",
                flow="absolute",
                slot_ids=("slot.header.mark", "slot.header.text"),
            ),
            Region(
                id="region.body",
                role="stem",
                flow="absolute",
                slot_ids=(
                    "slot.body.box",
                    "slot.body.text1",
                    "slot.body.text2",
                    "slot.body.diagram",
                ),
            ),
            Region(id="region.footer", role="note", flow="absolute", slot_ids=()),
        ),
        slots=(
            TextSlot(
                id="slot.header.mark",
                prompt="",
                text="□",
                style_role="question",
                x=18.0,
                y=18.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.header.text",
                prompt="",
                text="6. 알맞은 말을 선택하세요.",
                style_role="question",
                x=40.0,
                y=18.0,
                font_size=28,
            ),
            RectSlot(id="slot.body.box", prompt="", x=18.0, y=40.0, width=739.0, height=78.0),
            TextSlot(
                id="slot.body.text1",
                prompt="",
                text="( 한, 두, 네 ) 각이 모두 직각이고 ( 한, 두, 네 ) 변의",
                style_role="question",
                x=47.0,
                y=79.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.body.text2",
                prompt="",
                text="길이가 모두 같은 사각형을 정사각형이라고 합니다.",
                style_role="question",
                x=47.0,
                y=108.0,
                font_size=28,
            ),
            RectSlot(id="slot.body.diagram", prompt="", x=624.0, y=54.0, width=103.0, height=63.0),
        ),
        diagrams=(),
        groups=(),
        constraints=(),
        tags=(),
    )


PROBLEM_TEMPLATE = build_problem_template()

SEMANTIC_OVERRIDE = {
    "problem_id": "S3_초등_3_009065",
    "problem_type": "선택형_도형_정의",
    "metadata": {
        "language": "ko",
        "question": "정사각형의 정의를 묻는 선택형 문제",
        "instruction": "알맞은 말을 선택하세요.",
    },
    "domain": {
        "objects": [
            {"id": "obj.shape", "type": "quadrilateral", "name": "사각형"},
            {"id": "obj.definition.property1", "type": "property", "name": "모든 각이 직각"},
            {"id": "obj.definition.property2", "type": "property", "name": "모든 변의 길이가 같음"},
        ],
        "relations": [],
        "problem_solving": {
            "understand": {
                "given_refs": ["obj.shape", "obj.definition.property1", "obj.definition.property2"],
                "target_ref": "answer.target",
                "condition_refs": ["rel.define.square"],
            },
            "plan": {
                "method": "definition_matching",
                "description": "문장 속 빈칸에 들어갈 말을 정의에 맞게 고른다.",
            },
            "execute": {"expected_operations": ["definition_reading", "choice_matching"]},
            "review": {"check_methods": ["definition_consistency_check"]},
        },
    },
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {"type": "choice_fill", "description": "두 개의 빈칸에 들어갈 알맞은 말"},
        "value": 0,
        "unit": "",
    },
}

SOLVABLE = {
    "schema": "modu.solvable.v1.1",
    "problem_id": "S3_초등_3_009065",
    "problem_type": "선택형_도형_정의",
    "inputs": {
        "total_ticks": 2,
        "target_label": "빈칸",
        "target_ticks": 2,
        "target_count": 2,
        "unit": "",
    },
    "given": [
        {"ref": "obj.shape", "value": {"name": "사각형"}},
        {"ref": "obj.definition.property1", "value": {"name": "모든 각이 직각"}},
        {"ref": "obj.definition.property2", "value": {"name": "모든 변의 길이가 같음"}},
    ],
    "target": {"ref": "answer.target", "type": "choice_fill"},
    "method": "definition_matching",
    "plan": [
        "정사각형의 정의를 읽고 빈칸 두 곳에 들어갈 표현을 찾는다.",
        "각에 해당하는 말과 변에 해당하는 말을 구분한다.",
    ],
    "steps": [
        {"id": "step.1", "expr": "정의에서 각의 조건 확인", "value": "네"},
        {"id": "step.2", "expr": "정의에서 변의 조건 확인", "value": "네"},
    ],
    "checks": [
        {
            "id": "check.1",
            "expr": "각 조건과 변 조건이 정의와 일치하는가",
            "expected": True,
            "actual": True,
            "pass": True,
        }
    ],
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {"type": "choice_fill", "description": "두 개의 빈칸에 들어갈 알맞은 말"},
        "value": 0,
        "unit": "",
    },
}
