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
        id="S3_초등_3_008789",
        title="들이가 더 많은 것 고르기",
        canvas=Canvas(width=960, height=436, coordinate_mode="logical"),
        regions=(
            Region(
                id="region.stem",
                role="stem",
                flow="absolute",
                slot_ids=(
                    "slot.q3",
                    "slot.q4",
                    "slot.q5",
                    "slot.inserted.image.1",
                    "slot.inserted.image.2",
                ),
            ),
            Region(
                id="region.diagram",
                role="diagram",
                flow="absolute",
                slot_ids=(
                    "slot.lb.tharmos",
                    "slot.lb.milk",
                    "slot.choice",
                ),
            ),
        ),
        slots=(
            TextSlot(
                id="slot.q3",
                prompt="",
                text="보온병과 우유갑에 물을 가득 채운 후 물을 같은 그릇에 옮겨 담았습니다.",
                style_role="question",
                x=64.0,
                y=24.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.q4",
                prompt="",
                text="그림과 같이 물이 채워졌을 때 보온병과 우유갑 중 들이가 더",
                style_role="question",
                x=64.0,
                y=60.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.q5",
                prompt="",
                text="많은 것을 선택하세요.",
                style_role="question",
                x=64.0,
                y=96.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.lb.tharmos",
                prompt="",
                text="보온병",
                style_role="label",
                x=180,
                y=335,
                font_size=28,
                fill="#111111",
            ),
            TextSlot(
                id="slot.lb.milk",
                prompt="",
                text="우유갑",
                style_role="label",
                x=560,
                y=335,
                font_size=28,
                fill="#111111",
            ),
            TextSlot(
                id="slot.choice",
                prompt="",
                text="( 보온병 , 우유갑 )",
                style_role="choice",
                x=368,
                y=402,
                font_size=28,
                fill="#111111",
            ),
            ImageSlot(
                id="slot.inserted.image.1",
                prompt="",
                href="data:image/png;base64,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",
                x=125,
                y=145,
                width=350,
                height=165,
                preserve_aspect_ratio="xMidYMid meet",
            ),
            ImageSlot(
                id="slot.inserted.image.2",
                prompt="",
                href="data:image/png;base64,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",
                x=540,
                y=145,
                width=305,
                height=165,
                preserve_aspect_ratio="xMidYMid meet",
            ),
        ),
    )


PROBLEM_TEMPLATE = build_problem_template()

SEMANTIC_OVERRIDE = {
    "problem_id": "S3_초등_3_008789",
    "problem_type": "visual_comparison_volume",
    "metadata": {
        "language": "ko",
        "question": "보온병과 우유갑 중 들이가 더 많은 것을 고르는 문제",
        "instruction": "그림을 보고 들이가 더 많은 대상을 선택한다.",
        "points": 5,
    },
    "domain": {
        "objects": [
            {"id": "obj.tharmos", "type": "container", "name": "보온병"},
            {"id": "obj.milk_carton", "type": "container", "name": "우유갑"},
            {"id": "obj.comparison_container", "type": "container", "name": "같은 그릇"},
        ],
        "relations": [],
        "problem_solving": {
            "understand": {
                "given_refs": ["obj.tharmos", "obj.milk_carton", "obj.comparison_container"],
                "target_ref": "answer.target",
                "condition_refs": ["rel.compare_volume"],
            },
            "plan": {
                "method": "visual_compare",
                "description": "같은 그릇에 옮겨 담은 뒤의 물 양을 비교하여 더 많은 대상을 고른다.",
            },
            "execute": {
                "expected_operations": [
                    "compare_poured_water_amounts",
                    "select_greater_capacity_container",
                ]
            },
            "review": {
                "check_methods": ["image_text_consistency_check", "choice_consistency_check"]
            },
        },
    },
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {
            "type": "greater_capacity_choice",
            "description": "보온병과 우유갑 중 들이가 더 많은 것",
        },
        "value": 1,
        "unit": "",
    },
}

SOLVABLE = {
    "schema": "modu.solvable.v1.1",
    "problem_id": "S3_초등_3_008789",
    "problem_type": "visual_comparison_volume",
    "inputs": {
        "total_ticks": 0,
        "target_label": "들이가 더 많은 것",
        "target_ticks": 0,
        "target_count": 2,
        "unit": "",
    },
    "given": [
        {"ref": "obj.tharmos", "value": {"name": "보온병"}},
        {"ref": "obj.milk_carton", "value": {"name": "우유갑"}},
        {"ref": "obj.comparison_container", "value": {"name": "같은 그릇"}},
    ],
    "target": {"ref": "answer.target", "type": "greater_capacity_choice"},
    "plan": [
        "같은 그릇에 옮겨 담은 뒤의 물 양을 비교한다.",
        "더 많은 물이 담기는 쪽을 들이가 더 큰 것으로 판단한다.",
    ],
    "method": "visual_compare",
    "steps": [
        {
            "id": "step.1",
            "expr": "보온병과 우유갑을 같은 그릇에 옮겨 담은 뒤 물의 양을 비교한다.",
            "value": "보온병 쪽이 더 많다고 제시됨",
        },
        {"id": "step.2", "expr": "더 많은 쪽을 선택한다.", "value": "보온병"},
    ],
    "checks": [
        {
            "id": "check.1",
            "expr": "문제의 해설 문구와 선택 결과가 일치하는가",
            "expected": "보온병",
            "actual": "보온병",
            "pass": True,
        }
    ],
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {
            "type": "greater_capacity_choice",
            "description": "보온병과 우유갑 중 들이가 더 많은 것",
        },
        "value": 1,
        "unit": "",
    },
}
