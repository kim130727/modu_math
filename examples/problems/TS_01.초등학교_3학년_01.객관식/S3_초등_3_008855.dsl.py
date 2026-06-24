from __future__ import annotations
from modu_math.dsl import Canvas, ProblemTemplate, Region, TextSlot


def build_problem_template() -> ProblemTemplate:
    return ProblemTemplate(
        id="S3_초등_3_008855",
        title="가장 적은 용량 고르기",
        canvas=Canvas(width=840, height=320, coordinate_mode="logical"),
        regions=(
            Region(
                id="region.stem", role="stem", flow="absolute", slot_ids=("slot.q1", "slot.choice")
            ),
        ),
        slots=(
            TextSlot(
                id="slot.q1",
                prompt="",
                text="□ 1. 민정이네 냉장고에 사과주스가 3 L 50 mL, 오렌지주스가 3500 mL, 포도주스가 5 L와 30 mL 있습니다. 사과주스, 오렌지주스, 포도주스 중 가장 적은 것은 어느 것인가요?",
                style_role="question",
                x=10.0,
                y=18.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.choice",
                prompt="",
                text="（사과주스, 오렌지주스, 포도주스）",
                style_role="body",
                x=480.0,
                y=112.0,
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
    "problem_id": "S3_초등_3_008855",
    "problem_type": "비교하여 가장 적은 것 고르기",
    "metadata": {
        "language": "ko",
        "question": "세 음료의 용량을 비교하여 가장 적은 것을 고르는 문제",
        "instruction": "가장 적은 것을 고르시오.",
    },
    "domain": {
        "objects": [
            {
                "id": "obj.apple_juice",
                "type": "beverage",
                "name": "사과주스",
                "quantity": {"text": "3 L 50 mL"},
            },
            {
                "id": "obj.orange_juice",
                "type": "beverage",
                "name": "오렌지주스",
                "quantity": {"text": "3500 mL"},
            },
            {
                "id": "obj.grape_juice",
                "type": "beverage",
                "name": "포도주스",
                "quantity": {"text": "5 L와 30 mL"},
            },
        ],
        "relations": [],
        "problem_solving": {
            "understand": {
                "given_refs": ["obj.apple_juice", "obj.orange_juice", "obj.grape_juice"],
                "target_ref": "answer.target",
                "condition_refs": ["rel.compare_quantities"],
            },
            "plan": {
                "method": "표기 변환 후 비교",
                "description": "서로 다른 단위 표기를 같은 기준으로 바꾸어 크기를 비교한다.",
            },
            "execute": {
                "expected_operations": ["단위 표기 변환", "크기 비교", "가장 적은 것 선택"]
            },
            "review": {"check_methods": ["비교 순서 확인", "정답 선택 확인"]},
        },
    },
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {
            "type": "least_quantity_beverage",
            "description": "사과주스, 오렌지주스, 포도주스 중 가장 적은 것",
        },
        "value": 1,
        "unit": "",
    },
}

SOLVABLE = {
    "schema": "modu.solvable.v1.1",
    "problem_id": "S3_초등_3_008855",
    "problem_type": "비교하여 가장 적은 것 고르기",
    "inputs": {
        "total_ticks": 3,
        "target_label": "가장 적은 것",
        "target_ticks": 1,
        "target_count": 1,
        "unit": "용량",
    },
    "given": [
        {"ref": "obj.apple_juice", "value": {"text": "3 L 50 mL"}},
        {"ref": "obj.orange_juice", "value": {"text": "3500 mL"}},
        {"ref": "obj.grape_juice", "value": {"text": "5 L와 30 mL"}},
    ],
    "target": {"ref": "answer.target", "type": "least_quantity_beverage"},
    "method": "표기 변환 후 비교",
    "plan": [
        "각 음료의 용량 표기를 같은 기준으로 바꾼다.",
        "세 용량을 비교하여 가장 작은 것을 고른다.",
    ],
    "steps": [
        {"id": "step.1", "expr": "3500 mL의 표기 확인", "value": "3500 mL"},
        {"id": "step.2", "expr": "5 L와 30 mL의 표기 확인", "value": "5 L 30 mL"},
        {
            "id": "step.3",
            "expr": "세 음료의 크기 비교 결과 확인",
            "value": "5 L 30 mL > 3 L 500 mL > 3 L 50 mL",
        },
        {"id": "step.4", "expr": "가장 적은 것 선택", "value": "사과주스"},
    ],
    "checks": [
        {
            "id": "check.1",
            "expr": "정답이 가장 작은 용량과 일치하는가",
            "expected": "사과주스",
            "actual": "사과주스",
            "pass": True,
        }
    ],
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {
            "type": "least_quantity_beverage",
            "description": "사과주스, 오렌지주스, 포도주스 중 가장 적은 것",
        },
        "value": 1,
        "unit": "",
    },
}
