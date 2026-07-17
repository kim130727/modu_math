from __future__ import annotations
from modu_math.dsl import (
    Canvas,
    ProblemTemplate,
    Region,
    TextSlot,
    RectSlot,
    LineSlot,
    CircleSlot,
    PathSlot,
    ImageSlot,
)


def build_problem_template() -> ProblemTemplate:
    return ProblemTemplate(
        id="S3_초등_3_008784",
        title="들이 비교",
        canvas=Canvas(width=940, height=367, coordinate_mode="logical"),
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
                slot_ids=(
                    "slot.bottle.label",
                    "slot.glass.caption",
                    "slot.choice",
                ),
            ),
        ),
        slots=(
            TextSlot(
                id="slot.q2",
                prompt="",
                text="물병과 유리컵에 물을 가득 채웠다가 모양과 크기가 같은 그릇에 각각 옮",
                style_role="question",
                x=72.0,
                y=28.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.q3",
                prompt="",
                text="겨 담았습니다. 물병과 유리컵 중에서 들이가 더 많은 것을 선택해 보세요.",
                style_role="question",
                x=72,
                y=74,
                font_size=28,
                fill="#111111",
            ),
            TextSlot(
                id="slot.bottle.label",
                prompt="",
                text="물병",
                style_role="label",
                x=287,
                y=286,
                font_size=28,
                fill="#111111",
            ),
            TextSlot(
                id="slot.glass.caption",
                prompt="",
                text="유리컵",
                style_role="label",
                x=599,
                y=286,
                font_size=28,
                fill="#111111",
            ),
            TextSlot(
                id="slot.choice",
                prompt="",
                text="( 물병 , 유리컵 )",
                style_role="choice",
                x=363,
                y=345,
                font_size=28,
                fill="#111111",
            ),
            ImageSlot(
                id="slot.inserted.image.1",
                prompt="",
                href="data:image/png;base64,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",
                x=250,
                y=95,
                width=445,
                height=160,
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
    "problem_id": "S3_초등_3_008784",
    "problem_type": "comparison_capacity",
    "metadata": {
        "language": "ko",
        "question": "물병과 유리컵 중에서 들이가 더 많은 것을 선택하는 문제",
        "instruction": "물병과 유리컵 중에서 들이가 더 많은 것을 선택해 보세요.",
    },
    "domain": {
        "objects": [
            {"id": "obj.bottle", "type": "container", "name": "물병"},
            {"id": "obj.glass", "type": "container", "name": "유리컵"},
            {"id": "obj.transfer_container_1", "type": "same_shape_container"},
            {"id": "obj.transfer_container_2", "type": "same_shape_container"},
        ],
        "relations": [],
        "problem_solving": {
            "understand": {
                "given_refs": [
                    "obj.bottle",
                    "obj.glass",
                    "obj.transfer_container_1",
                    "obj.transfer_container_2",
                ],
                "target_ref": "answer.target",
                "condition_refs": ["rel.compare_capacity"],
            },
            "plan": {
                "method": "visual_comparison",
                "description": "같은 모양과 크기의 그릇에 옮겨 담은 물의 높이를 비교한다.",
            },
            "execute": {
                "expected_operations": ["compare_transfer_heights", "choose_larger_capacity"]
            },
            "review": {"check_methods": ["compare_heights_consistency"]},
        },
    },
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {"type": "selection", "description": "들이가 더 많은 것"},
        "value": "물병",
        "unit": "",
    },
}

SOLVABLE = {
    "schema": "modu.solvable.v1.1",
    "problem_id": "S3_초등_3_008784",
    "problem_type": "comparison_capacity",
    "inputs": {
        "total_ticks": 0,
        "target_label": "들이가 더 많은 것",
        "target_ticks": 0,
        "target_count": 2,
        "unit": "",
    },
    "given": [
        {"ref": "obj.bottle", "value": {"name": "물병"}},
        {"ref": "obj.glass", "value": {"name": "유리컵"}},
    ],
    "target": {"ref": "answer.target", "type": "selection"},
    "method": "visual_comparison",
    "plan": [
        "같은 모양과 크기의 그릇에 옮겨 담은 물의 높이를 비교한다.",
        "물 높이가 더 높게 보이는 쪽의 들이가 더 많다고 판단한다.",
    ],
    "steps": [{"id": "step.1", "expr": "물병과 유리컵의 옮겨 담은 물 높이 비교", "value": "물병"}],
    "checks": [
        {
            "id": "check.1",
            "expr": "해설 문장과 일치하는 선택인지 확인",
            "expected": "물병",
            "actual": "물병",
            "pass": True,
        }
    ],
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {"type": "selection", "description": "들이가 더 많은 것"},
        "value": "물병",
        "unit": "",
    },
}
