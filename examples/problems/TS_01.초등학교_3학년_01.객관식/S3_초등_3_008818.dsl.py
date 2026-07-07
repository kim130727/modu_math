from __future__ import annotations
from modu_math.dsl import (
    Canvas,
    CircleSlot,
    LineSlot,
    PathSlot,
    PolygonSlot,
    ProblemTemplate,
    RectSlot,
    Region,
    TextSlot,
    ImageSlot,
)


def build_problem_template() -> ProblemTemplate:
    return ProblemTemplate(
        id="S3_초등_3_008818",
        title="들이다 비교",
        canvas=Canvas(width=940, height=516, coordinate_mode="logical"),
        regions=(
            Region(
                id="region.stem",
                role="stem",
                flow="absolute",
                slot_ids=("slot.q2", "slot.q3", "slot.inserted.image.1"),
            ),
            Region(
                id="region.diagram",
                role="diagram",
                flow="absolute",
                slot_ids=("slot.lb.choice",),
            ),
            Region(id="region.footer", role="note", flow="absolute", slot_ids=()),
        ),
        slots=(
            TextSlot(
                id="slot.q2",
                prompt="",
                text="물병에 물을 가득 채운 후 페트병에 옮겨 담았습니다. 그림과 같이 물을",
                style_role="question",
                x=20,
                y=45,
                font_size=28,
                fill="#111111",
            ),
            TextSlot(
                id="slot.q3",
                prompt="",
                text="채웠을 때에 물병과 페트병 중 들이가 더 많은 것은 어느 것인지 선택해 보",
                style_role="question",
                x=20,
                y=84,
                font_size=28,
                fill="#111111",
            ),
            TextSlot(
                id="slot.q4",
                prompt="",
                text="세요.",
                style_role="question",
                x=20,
                y=120,
                font_size=28,
                fill="#111111",
            ),
            TextSlot(
                id="slot.lb.choice",
                prompt="",
                text="( 물병 , 페트병 )",
                style_role="label",
                x=326,
                y=466,
                font_size=28,
                fill="#111111",
            ),
            ImageSlot(
                id="slot.inserted.image.1",
                prompt="",
                href="data:image/png;base64,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",
                x=275,
                y=135,
                width=295,
                height=280,
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
    "problem_id": "S3_초등_3_008818",
    "problem_type": "comparison_capacity",
    "metadata": {
        "language": "ko",
        "question": "그림을 보고 물병과 페트병 중 들이가 더 많은 것을 고르는 문제",
        "instruction": "물병과 페트병 중 들이가 더 많은 것을 선택하시오.",
    },
    "domain": {
        "objects": [
            {"id": "obj.water_bottle", "type": "container", "name": "물병"},
            {"id": "obj.pet_bottle", "type": "container", "name": "페트병"},
        ],
        "relations": [],
        "problem_solving": {
            "understand": {
                "given_refs": ["obj.water_bottle", "obj.pet_bottle", "rel.pour_water"],
                "target_ref": "answer.target",
                "condition_refs": ["rel.compare_capacity"],
            },
            "plan": {
                "method": "visual_comparison",
                "description": "그림의 물이 옮겨진 상황과 가득 차지 않은 상태를 보고 더 큰 들이를 고른다.",
            },
            "execute": {
                "expected_operations": ["identify_containers", "compare_capacity_by_scene"]
            },
            "review": {
                "check_methods": ["compare_only_two_choices", "confirm_printed_answer_note"]
            },
        },
    },
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {"type": "choice", "description": "물병과 페트병 중 들이가 더 많은 것"},
        "value": 0,
        "unit": "",
    },
}

SOLVABLE = {
    "schema": "modu.solvable.v1.1",
    "problem_id": "S3_초등_3_008818",
    "problem_type": "comparison_capacity",
    "inputs": {
        "total_ticks": 0,
        "target_label": "들이가 더 많은 것",
        "target_ticks": 0,
        "target_count": 2,
        "unit": "",
    },
    "given": [
        {"ref": "obj.water_bottle", "value": {"name": "물병"}},
        {"ref": "obj.pet_bottle", "value": {"name": "페트병"}},
        {"ref": "rel.pour_water", "value": {"from": "물병", "to": "페트병"}},
    ],
    "target": {"ref": "answer.target", "type": "choice"},
    "method": "visual_comparison",
    "plan": [
        "그림에서 비교 대상인 물병과 페트병을 찾는다.",
        "물이 옮겨진 뒤의 상태를 보고 어느 용기가 더 큰 들이를 가지는지 판단한다.",
    ],
    "steps": [
        {"id": "step.1", "expr": "비교 대상 확인", "value": ["물병", "페트병"]},
        {"id": "step.2", "expr": "그림의 상황 해석", "value": "물병의 물이 페트병으로 옮겨진 상태"},
        {"id": "step.3", "expr": "선택", "value": "페트병"},
    ],
    "checks": [
        {
            "id": "check.1",
            "expr": "보기는 두 개의 용기 중 하나를 고르는 형태인가",
            "expected": 2,
            "actual": 2,
            "pass": True,
        },
        {
            "id": "check.2",
            "expr": "인쇄된 정답 표시와 선택값이 일치하는가",
            "expected": "페트병",
            "actual": "페트병",
            "pass": True,
        },
    ],
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {"type": "choice", "description": "물병과 페트병 중 들이가 더 많은 것"},
        "value": 0,
        "unit": "",
    },
}
