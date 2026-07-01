from __future__ import annotations
from modu_math.dsl import (
    Canvas,
    ProblemTemplate,
    Region,
    RectSlot,
    TextSlot,
    CircleSlot,
    LineSlot,
    ImageSlot,
)


def build_problem_template() -> ProblemTemplate:
    return ProblemTemplate(
        id="S3_초등_3_008754",
        title="들이가 더 적은 것 고르기",
        canvas=Canvas(width=960, height=540, coordinate_mode="logical"),
        regions=(
            Region(
                id="region.stem",
                role="stem",
                flow="absolute",
                slot_ids=("slot.q2", "slot.q3", "slot.q4", "slot.inserted.image.1"),
            ),
            Region(
                id="region.diagram",
                role="diagram",
                flow="absolute",
                slot_ids=("slot.choice",),
            ),
            Region(id="region.answer", role="answer", flow="absolute", slot_ids=()),
        ),
        slots=(
            TextSlot(
                id="slot.q2",
                prompt="",
                text="지아 어머니께서 리필용 샴푸를 사서 비닐봉투에 모두 부었더니 다음",
                style_role="question",
                x=19,
                y=47,
                font_size=28,
            ),
            TextSlot(
                id="slot.q3",
                prompt="",
                text="그림과 같았습니다. 리필용 샴푸 용기와 샴푸통 중 들이가 더 적은 것을 선",
                style_role="question",
                x=18,
                y=98,
                font_size=28,
            ),
            TextSlot(
                id="slot.q4",
                prompt="",
                text="택하세요. (단, 리필용 샴푸 용기에는 샴푸가 가득 차 있었습니다.)",
                style_role="question",
                x=18,
                y=148,
                font_size=28,
            ),
            TextSlot(
                id="slot.choice",
                prompt="",
                text="( 리필용 샴푸 용기 , 샴푸통 )",
                style_role="choice",
                x=251,
                y=470,
                font_size=28,
                fill="#111111",
            ),
            ImageSlot(
                id="slot.inserted.image.1",
                prompt="",
                href="data:image/png;base64,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",
                x=205,
                y=190,
                width=400,
                height=215,
                preserve_aspect_ratio="xMidYMid meet",
            ),
        ),
        diagrams=(),
        groups=(),
        constraints=(),
        tags=(),
    )


PROBLEM_TEMPLATE = build_problem_template()

SEMANTIC_OVERRIDE = {
    "problem_id": "S3_초등_3_008754",
    "problem_type": "비교 판단",
    "metadata": {
        "language": "ko",
        "question": "리필용 샴푸 용기와 샴푸통 중 들이가 더 적은 것을 선택하는 문제",
        "instruction": "보이는 그림과 문장을 바탕으로 들이가 더 적은 대상을 고른다.",
        "points": 5,
    },
    "domain": {
        "objects": [
            {
                "id": "obj.refill_container",
                "type": "container",
                "name": "리필용 샴푸 용기",
            },
            {"id": "obj.shampoo_bottle", "type": "container", "name": "샴푸통"},
        ],
        "relations": [],
        "problem_solving": {
            "understand": {
                "given_refs": [
                    "obj.refill_container",
                    "obj.shampoo_bottle",
                    "rel.compare_capacity",
                ],
                "target_ref": "answer.target",
                "condition_refs": [],
            },
            "plan": {
                "method": "비교 판단",
                "description": "두 용기 중 들이가 더 적은 대상을 고른다.",
            },
            "execute": {
                "expected_operations": [
                    "그림과 해설 문장에서 비교 대상 확인",
                    "들이가 더 적은 대상 선택",
                ]
            },
            "review": {"check_methods": ["선택한 대상이 비교 조건과 일치하는지 확인"]},
        },
    },
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {"type": "selected_object", "description": "들이가 더 적은 것"},
        "value": "리필용 샴푸 용기",
        "unit": "",
    },
}

SOLVABLE = {
    "schema": "modu.solvable.v1.1",
    "problem_id": "S3_초등_3_008754",
    "problem_type": "비교 판단",
    "inputs": {
        "total_ticks": 0,
        "target_label": "들이가 더 적은 것",
        "target_ticks": 0,
        "target_count": 2,
        "unit": "",
    },
    "given": [
        {"ref": "obj.refill_container", "value": {"name": "리필용 샴푸 용기"}},
        {"ref": "obj.shampoo_bottle", "value": {"name": "샴푸통"}},
    ],
    "target": {"ref": "answer.target", "type": "selected_object"},
    "method": "비교 판단",
    "plan": [
        "그림과 해설에 보이는 두 대상을 확인한다.",
        "들이가 더 적은 대상을 선택한다.",
    ],
    "steps": [
        {"id": "step.1", "expr": "비교 대상 확인", "value": "리필용 샴푸 용기, 샴푸통"},
        {
            "id": "step.2",
            "expr": "들이가 더 적은 대상 선택",
            "value": "리필용 샴푸 용기",
        },
    ],
    "checks": [
        {
            "id": "check.1",
            "expr": "선택한 대상이 두 비교 대상 중 하나인가",
            "expected": True,
            "actual": True,
            "pass": True,
        }
    ],
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {"type": "selected_object", "description": "들이가 더 적은 것"},
        "value": "리필용 샴푸 용기",
        "unit": "",
    },
}
