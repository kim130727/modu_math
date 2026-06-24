from __future__ import annotations
from modu_math.dsl import Canvas, CircleSlot, ProblemTemplate, RectSlot, Region, TextSlot


def build_problem_template() -> ProblemTemplate:
    return ProblemTemplate(
        id="S3_초등_3_008766",
        title="가지와 당근의 무게를 비교하는 바른 방법",
        canvas=Canvas(width=940, height=560, coordinate_mode="logical"),
        regions=(
            Region(
                id="region.stem",
                role="stem",
                flow="absolute",
                slot_ids=("slot.qnum", "slot.q1", "slot.q2", "slot.q3"),
            ),
            Region(
                id="region.diagram",
                role="diagram",
                flow="absolute",
                slot_ids=("slot.bg.ellipse", "slot.obj.eggplant", "slot.obj.carrot"),
            ),
            Region(
                id="region.options",
                role="options",
                flow="absolute",
                slot_ids=("slot.opt1", "slot.opt2"),
            ),
            Region(
                id="region.answer_explanation",
                role="answer_explanation",
                flow="absolute",
                slot_ids=(),
            ),
        ),
        slots=(
            TextSlot(
                id="slot.qnum",
                prompt="",
                text="□ 68.",
                style_role="question",
                x=16.0,
                y=30.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.q1",
                prompt="",
                text="가지와 당근을 양손에 들어 보니 무게가 비슷하여 어느 것이 더 무거운",
                style_role="question",
                x=62.0,
                y=30.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.q2",
                prompt="",
                text="지 알 수 없습니다. 가지와 당근의 무게를 비교할 수 있는 방법을 바르게 말",
                style_role="question",
                x=40.0,
                y=64.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.q3",
                prompt="",
                text="한 것을 선택해 보세요.",
                style_role="question",
                x=40.0,
                y=98.0,
                font_size=28,
            ),
            RectSlot(
                id="slot.bg.ellipse",
                prompt="",
                x=412.0,
                y=122.0,
                width=150.0,
                height=184.0,
                fill="#F8EFB7",
                stroke="none",
                rx=75.0,
                ry=92.0,
            ),
            TextSlot(
                id="slot.obj.eggplant",
                prompt="",
                text="",
                style_role="annotation",
                x=0.0,
                y=0.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.obj.carrot",
                prompt="",
                text="",
                style_role="annotation",
                x=0.0,
                y=0.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.opt1",
                prompt="",
                text="① 가지와 당근의 길이를 각각 재어 비교해. 길이가 더 긴 쪽이 더 무거워.",
                style_role="question",
                x=22.0,
                y=326.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.opt2",
                prompt="",
                text="② 저울의 양쪽 접시에 가지와 당근을 각각 올려 무게를 비교해. 아래로 내려간 쪽이 더 무거워.",
                style_role="question",
                x=22.0,
                y=366.0,
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
    "problem_id": "S3_초등_3_008766",
    "problem_type": "multiple_choice_concept",
    "metadata": {
        "language": "ko",
        "question": "가지와 당근의 무게를 비교할 수 있는 방법을 바르게 고르는 문제",
        "instruction": "바르게 말한 것을 선택하시오.",
    },
    "domain": {
        "objects": [
            {"id": "obj.eggplant", "type": "vegetable", "name": "가지"},
            {"id": "obj.carrot", "type": "vegetable", "name": "당근"},
            {"id": "obj.scale", "type": "instrument", "name": "저울"},
        ],
        "relations": [],
        "problem_solving": {
            "understand": {
                "given_refs": ["obj.eggplant", "obj.carrot"],
                "target_ref": "answer.target",
                "condition_refs": ["rel.compare_weight"],
            },
            "plan": {
                "method": "concept_choice",
                "description": "무게 비교에 알맞은 방법을 고른다.",
            },
            "execute": {
                "expected_operations": [
                    "compare_candidate_methods",
                    "select_weight_measurement_method",
                ]
            },
            "review": {"check_methods": ["method_suitability_check"]},
        },
    },
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {
            "type": "choice",
            "description": "가지와 당근의 무게를 비교할 수 있는 바른 방법",
        },
        "value": 2,
        "unit": "",
    },
}

SOLVABLE = {
    "schema": "modu.solvable.v1.1",
    "problem_id": "S3_초등_3_008766",
    "problem_type": "multiple_choice_concept",
    "inputs": {
        "total_ticks": 2,
        "target_label": "정답",
        "target_ticks": 2,
        "target_count": 2,
        "unit": "",
    },
    "given": [
        {"ref": "obj.eggplant", "value": {"name": "가지"}},
        {"ref": "obj.carrot", "value": {"name": "당근"}},
        {"ref": "obj.scale", "value": {"name": "저울"}},
    ],
    "target": {"ref": "answer.target", "type": "choice"},
    "method": "concept_choice",
    "plan": [
        "무게를 비교하는 데 알맞은 방법인지 판단한다.",
        "보기 중 저울을 사용하는 방법을 고른다.",
    ],
    "steps": [
        {"id": "step.1", "expr": "길이를 재어 무게를 비교하는 방법", "value": 1},
        {"id": "step.2", "expr": "저울의 양쪽 접시에 올려 무게를 비교하는 방법", "value": 2},
    ],
    "checks": [
        {
            "id": "check.1",
            "expr": "무게 비교에 사용할 수 있는 방법인가",
            "expected": 2,
            "actual": 2,
            "pass": True,
        }
    ],
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {
            "type": "choice",
            "description": "가지와 당근의 무게를 비교할 수 있는 바른 방법",
        },
        "value": 2,
        "unit": "",
    },
}
