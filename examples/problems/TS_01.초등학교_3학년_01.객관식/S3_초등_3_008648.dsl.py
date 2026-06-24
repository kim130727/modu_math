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
        id="S3_초등_3_008648",
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
                text="길이가 가장 긴 선분은 선분 ( ㄱㄹ, ㄴㄹ, ㅇㄹ )이고,",
                style_role="question",
                x=40,
                y=345,
                font_size=30,
            ),
            TextSlot(
                id="slot.q3",
                prompt="",
                text=" 이 선분을 원의 (지름, 반지름 )이라고 합니다.",
                style_role="question",
                x=40,
                y=390,
                font_size=30,
            ),
            CircleSlot(id="slot.circle", prompt="", cx=430, cy=190, r=115, fill="none"),
            CircleSlot(id="slot.center", prompt="", cx=430, cy=190, r=5, fill="#d81b60"),
            TextSlot(
                id="slot.lb.g", prompt="", text="ㄱ", style_role="label", x=375, y=75, font_size=30
            ),
            TextSlot(
                id="slot.lb.n", prompt="", text="ㄴ", style_role="label", x=295, y=250, font_size=30
            ),
            TextSlot(
                id="slot.lb.d", prompt="", text="ㄷ", style_role="label", x=495, y=310, font_size=30
            ),
            TextSlot(
                id="slot.lb.r", prompt="", text="ㄹ", style_role="label", x=545, y=155, font_size=30
            ),
            LineSlot(id="slot.line.gr", prompt="", x1=415, y1=75, x2=540, y2=150),
            LineSlot(id="slot.line.nr", prompt="", x1=325, y1=235, x2=540, y2=150),
            LineSlot(id="slot.line.cd", prompt="", x1=430, y1=190, x2=495, y2=285),
            TextSlot(
                id="slot.lb.d.copy2",
                prompt="",
                text="ㅇ",
                x=415,
                y=185,
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
    "problem_id": "S3_초등_3_008648",
    "problem_type": "도형_개념_선택",
    "metadata": {
        "language": "ko",
        "question": "그림을 보고 알맞은 말을 선택하세요.",
        "instruction": "도형에서 가장 긴 선분과 원의 지름, 반지름을 구분하는 문제",
    },
    "domain": {
        "objects": [
            {"id": "obj.circle", "type": "circle"},
            {"id": "obj.segment.gr", "type": "segment", "endpoints": ["ㄱ", "ㄹ"]},
            {"id": "obj.segment.nr", "type": "segment", "endpoints": ["ㄴ", "ㄹ"]},
            {"id": "obj.segment.cd", "type": "segment", "endpoints": ["ㅇ", "ㄷ"]},
        ],
        "relations": [],
        "problem_solving": {
            "understand": {
                "given_refs": [
                    "obj.circle",
                    "obj.segment.gr",
                    "obj.segment.nr",
                    "obj.segment.cd",
                ],
                "target_ref": "answer.target",
                "condition_refs": ["rel.compare_length", "rel.diameter_concept"],
            },
            "plan": {
                "method": "도형_관찰",
                "description": "그림의 선분들을 비교하고 원에서 가장 긴 선분의 개념을 확인한다.",
            },
            "execute": {"expected_operations": ["선분_비교", "원의_지름_개념_확인"]},
            "review": {"check_methods": ["그림_표시와_문장_선택지_일치_확인"]},
        },
    },
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {
            "type": "선분과_원의_개념_선택",
            "description": "길이가 가장 긴 선분과 원의 지름을 고르는 선택",
        },
        "value": "가장 긴 선분 ㄴㄹ, 원의 지름",
        "unit": "",
    },
}

SOLVABLE = {
    "schema": "modu.solvable.v1.1",
    "problem_id": "S3_초등_3_008648",
    "problem_type": "도형_개념_선택",
    "inputs": {
        "total_ticks": 0,
        "target_label": "가장 긴 선분, 지름",
        "target_ticks": 0,
        "target_count": 1,
        "unit": "",
    },
    "given": [
        {"ref": "obj.circle", "value": {"type": "circle"}},
        {"ref": "obj.segment.gr", "value": {"endpoints": ["ㄱ", "ㄹ"]}},
        {"ref": "obj.segment.nr", "value": {"endpoints": ["ㄴ", "ㄹ"]}},
        {"ref": "obj.segment.cd", "value": {"endpoints": ["ㅇ", "ㄷ"]}},
    ],
    "target": {"ref": "answer.target", "type": "선분과_원의_개념_선택"},
    "method": "도형_관찰",
    "plan": [
        "그림에 나타난 선분들을 비교한다.",
        "원에서 가장 긴 선분이 무엇인지 확인한다.",
        "선택지와 아래 설명의 형태를 확인한다.",
    ],
    "steps": [
        {
            "id": "step.1",
            "expr": "선분 비교",
            "value": "길이 비교 대상: ㄱㄹ, ㄴㄹ, ㅇㄹ",
        },
        {
            "id": "step.2",
            "expr": "원의 지름 개념 확인",
            "value": "가장 긴 선분을 원의 지름으로 설명하는 문장 구조",
        },
        {
            "id": "step.3",
            "expr": "화면 하단 설명 문장 확인",
            "value": "길이가 가장 긴 선분은 선분 ㄴㄹ이고, 이 선분을 원의 지름이라고 합니다.",
        },
    ],
    "checks": [
        {
            "id": "check.1",
            "expr": "도형의 선분 선택지가 보이는가",
            "expected": True,
            "actual": True,
            "pass": True,
        },
        {
            "id": "check.2",
            "expr": "지름/반지름 선택 구조가 보이는가",
            "expected": True,
            "actual": True,
            "pass": True,
        },
    ],
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {
            "type": "선분과_원의_개념_선택",
            "description": "길이가 가장 긴 선분과 원의 지름을 고르는 선택",
        },
        "value": "가장 긴 선분 ㄴㄹ, 원의 지름",
        "unit": "",
    },
}
