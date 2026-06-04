from __future__ import annotations
from modu_math.dsl import (
    Canvas,
    ProblemTemplate,
    Region,
    RectSlot,
    TextSlot,
    CircleSlot,
    LineSlot,
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
                slot_ids=("slot.q1", "slot.q2", "slot.q3", "slot.q4"),
            ),
            Region(
                id="region.diagram",
                role="diagram",
                flow="absolute",
                slot_ids=(
                    "slot.left.bag",
                    "slot.left.label",
                    "slot.arrow",
                    "slot.right.bottle",
                    "slot.right.cap",
                    "slot.right.label",
                    "slot.choice",
                ),
            ),
            Region(id="region.answer", role="answer", flow="absolute", slot_ids=()),
        ),
        slots=(
            TextSlot(
                id="slot.q1",
                prompt="",
                text="51.",
                style_role="question",
                x=18.0,
                y=34.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.q2",
                prompt="",
                text="지아 어머니께서 리필용 샴푸를 사서 비닐봉투에 모두 부었더니 다음",
                style_role="question",
                x=58.0,
                y=34.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.q3",
                prompt="",
                text="그림과 같았습니다. 리필용 샴푸 용기와 샴푸통 중 들이가 더 적은 것을 선",
                style_role="question",
                x=18.0,
                y=66.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.q4",
                prompt="",
                text="택하세요. (단, 리필용 샴푸 용기에는 샴푸가 가득 차 있었습니다.)",
                style_role="question",
                x=18.0,
                y=98.0,
                font_size=28,
            ),
            RectSlot(
                id="slot.left.bag",
                prompt="",
                x=365.0,
                y=160.0,
                width=78.0,
                height=120.0,
                fill="#b8ecf7",
                stroke="#5bbfd6",
                stroke_width=2.0,
                rx=4.0,
                ry=4.0,
            ),
            TextSlot(
                id="slot.left.label",
                prompt="",
                text="리필용\n샴푸",
                style_role="label",
                x=384.0,
                y=210.0,
                font_size=26,
            ),
            LineSlot(
                id="slot.arrow",
                prompt="",
                x1=475.0,
                y1=218.0,
                x2=516.0,
                y2=218.0,
                stroke="#9a9a9a",
                stroke_width=6.0,
            ),
            RectSlot(
                id="slot.right.bottle",
                prompt="",
                x=550.0,
                y=165.0,
                width=72.0,
                height=116.0,
                fill="#ecf6a7",
                stroke="#9db64e",
                stroke_width=2.0,
                rx=18.0,
                ry=18.0,
            ),
            RectSlot(
                id="slot.right.cap",
                prompt="",
                x=570.0,
                y=135.0,
                width=32.0,
                height=30.0,
                fill="#eef6c0",
                stroke="#9db64e",
                stroke_width=2.0,
                rx=10.0,
                ry=10.0,
            ),
            CircleSlot(
                id="slot.right.cap.knob",
                prompt="",
                cx=586.0,
                cy=126.0,
                r=8.0,
                fill="#eef6c0",
                stroke="#9db64e",
                stroke_width=2.0,
            ),
            LineSlot(
                id="slot.right.cap.stem",
                prompt="",
                x1=586.0,
                y1=126.0,
                x2=586.0,
                y2=154.0,
                stroke="#9db64e",
                stroke_width=2.0,
            ),
            TextSlot(
                id="slot.right.label",
                prompt="",
                text="샴푸통",
                style_role="label",
                x=566.0,
                y=253.0,
                font_size=26,
            ),
            TextSlot(
                id="slot.choice",
                prompt="",
                text="( 리필용 샴푸 용기 , 샴푸통 )",
                style_role="choice",
                x=586.0,
                y=340.0,
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
