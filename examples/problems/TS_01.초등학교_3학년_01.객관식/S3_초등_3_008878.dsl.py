from __future__ import annotations
from modu_math.dsl import Canvas, ProblemTemplate, Region, TextSlot


def build_problem_template() -> ProblemTemplate:
    return ProblemTemplate(
        id="S3_초등_3_008878",
        title="바나나와 오이의 무게 비교 방법",
        canvas=Canvas(width=940, height=478, coordinate_mode="logical"),
        regions=(
            Region(
                id="region.stem",
                role="stem",
                flow="absolute",
                slot_ids=("slot.q_no", "slot.q1", "slot.q2", "slot.opt1", "slot.opt2"),
            ),
            Region(
                id="region.diagram",
                role="diagram",
                flow="absolute",
                slot_ids=("slot.banana", "slot.cucumber"),
            ),
        ),
        slots=(
            TextSlot(
                id="slot.q_no",
                prompt="",
                text="□ 33.",
                style_role="question",
                x=12.0,
                y=28.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.q1",
                prompt="",
                text="바나나와 오이를 양손에 들어 보니 무게가 비슷하여 어느 것이 더 무거운지 알 수 없습니다. 바나나와 오이의 무게를 비교할 수 있는 방법을 바로",
                style_role="question",
                x=56.0,
                y=30.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.q2",
                prompt="",
                text="게 말한 것을 선택해 보세요.",
                style_role="question",
                x=46.0,
                y=74.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.banana",
                prompt="",
                text="바나나",
                style_role="diagram",
                x=372.0,
                y=132.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.cucumber",
                prompt="",
                text="오이",
                style_role="diagram",
                x=512.0,
                y=132.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.opt1",
                prompt="",
                text="① 바나나와 오이의 길이를 각각 재어 비교해. 길이가 더 긴 쪽이 더 무거워.",
                style_role="answer_choice",
                x=26.0,
                y=230.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.opt2",
                prompt="",
                text="② 저울의 양쪽 접시에 바나나와 오이를 각각 올려놓고 무게를 비교해. 아래\n   로 내려간 쪽이 더 무거워.",
                style_role="answer_choice",
                x=26.0,
                y=276.0,
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
    "problem_id": "S3_초등_3_008878",
    "problem_type": "multiple_choice_science_math",
    "metadata": {
        "language": "ko",
        "question": "바나나와 오이의 무게를 비교할 수 있는 방법을 고르는 문제",
        "instruction": "가장 알맞은 방법을 선택한다.",
    },
    "domain": {
        "objects": [
            {"id": "obj.banana", "type": "fruit", "name": "바나나"},
            {"id": "obj.cucumber", "type": "vegetable", "name": "오이"},
            {"id": "obj.scale", "type": "tool", "name": "저울"},
        ],
        "relations": [],
        "problem_solving": {
            "understand": {
                "given_refs": ["obj.banana", "obj.cucumber"],
                "target_ref": "answer.target",
                "condition_refs": ["rel.compare_weight", "rel.use_scale"],
            },
            "plan": {
                "method": "concept_selection",
                "description": "무게를 비교하는 올바른 도구와 방법을 고른다.",
            },
            "execute": {
                "expected_operations": ["보기의 의미를 비교한다", "무게 비교에 맞는 방법을 찾는다"]
            },
            "review": {
                "check_methods": [
                    "도구가 무게 측정에 적절한지 확인한다",
                    "길이와 무게를 혼동하지 않는지 확인한다",
                ]
            },
        },
    },
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {
            "type": "correct_choice",
            "description": "바나나와 오이의 무게를 비교할 수 있는 방법",
        },
        "value": 2,
        "unit": "",
    },
}

SOLVABLE = {
    "schema": "modu.solvable.v1.1",
    "problem_id": "S3_초등_3_008878",
    "problem_type": "multiple_choice_science_math",
    "inputs": {
        "total_ticks": 2,
        "target_label": "정답",
        "target_ticks": 1,
        "target_count": 1,
        "unit": "",
    },
    "given": [
        {"ref": "obj.banana", "value": {"name": "바나나"}},
        {"ref": "obj.cucumber", "value": {"name": "오이"}},
        {"ref": "obj.scale", "value": {"name": "저울"}},
    ],
    "target": {"ref": "answer.target", "type": "correct_choice"},
    "method": "concept_selection",
    "plan": [
        "무게를 비교하는 데 알맞은 방법인지 보기의 의미를 확인한다.",
        "길이를 재는 방법이 아니라 저울을 사용하는 방법을 고른다.",
    ],
    "steps": [
        {
            "id": "step.1",
            "expr": "보기 ①: 길이를 재어 무게를 비교하는 방법인지 확인",
            "value": "무게 비교에 부적절",
        },
        {
            "id": "step.2",
            "expr": "보기 ②: 저울로 양쪽의 무게를 비교하는 방법인지 확인",
            "value": "무게 비교에 적절",
        },
        {"id": "step.3", "expr": "정답 선택", "value": 2},
    ],
    "checks": [
        {
            "id": "check.1",
            "expr": "무게 비교에 저울을 사용하는가",
            "expected": True,
            "actual": True,
            "pass": True,
        }
    ],
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {
            "type": "correct_choice",
            "description": "바나나와 오이의 무게를 비교할 수 있는 방법",
        },
        "value": 2,
        "unit": "",
    },
}
