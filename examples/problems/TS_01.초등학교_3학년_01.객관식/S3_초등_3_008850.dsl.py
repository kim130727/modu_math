from __future__ import annotations
from modu_math.dsl import (
    Canvas,
    ProblemTemplate,
    Region,
    TextSlot,
    RectSlot,
    CircleSlot,
    LineSlot,
    PathSlot,
)


def build_problem_template() -> ProblemTemplate:
    return ProblemTemplate(
        id="S3_초등_3_008850",
        title="주스병과 물병 비교",
        canvas=Canvas(width=960, height=400, coordinate_mode="logical"),
        regions=(
            Region(
                id="region.stem",
                role="stem",
                flow="absolute",
                slot_ids=("slot.q1", "slot.q2"),
            ),
            Region(
                id="region.diagram",
                role="diagram",
                flow="absolute",
                slot_ids=(
                    "slot.lb.juice_bottle",
                    "slot.lb.water_bottle",
                ),
            ),
            Region(
                id="region.choice_and_answer",
                role="note",
                flow="absolute",
                slot_ids=("slot.choice",),
            ),
        ),
        slots=(
            TextSlot(
                id="slot.q1",
                prompt="",
                text="주스병에 물을 가득 채운 후 물병에 옮겨 담았습니다. 그림과 같이 물을",
                style_role="question",
                x=36.184,
                y=41.974,
                font_size=28,
                fill="#111111",
            ),
            TextSlot(
                id="slot.q2",
                prompt="",
                text="채웠을 때에 주스병과 물병 중 들어가 더 많은 것을 선택해 보세요.",
                style_role="question",
                x=37.956,
                y=78.632,
                font_size=28,
                fill="#111111",
            ),
            TextSlot(
                id="slot.lb.juice_bottle",
                prompt="",
                text="주스병",
                style_role="label",
                x=246.35,
                y=238.676,
                font_size=28,
                fill="#111111",
            ),
            TextSlot(
                id="slot.lb.water_bottle",
                prompt="",
                text="물병",
                style_role="label",
                x=600.649,
                y=226.763,
                font_size=28,
                fill="#111111",
            ),
            TextSlot(
                id="slot.choice",
                prompt="",
                text="( 주스병 , 물병 )",
                style_role="question",
                x=341.049,
                y=360.281,
                font_size=28,
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
    "problem_id": "S3_초등_3_008850",
    "problem_type": "comparison_choice",
    "metadata": {
        "language": "ko",
        "question": "주스병과 물병 중 들어가 더 많은 것을 선택하는 문제",
        "instruction": "그림과 같이 물을 채웠을 때에 주스병과 물병 중 들어가 더 많은 것을 선택해 보세요.",
    },
    "domain": {
        "objects": [
            {"id": "obj.juice_bottle", "type": "container", "name": "주스병"},
            {"id": "obj.water_bottle", "type": "container", "name": "물병"},
        ],
        "relations": [],
        "problem_solving": {
            "understand": {
                "given_refs": ["obj.juice_bottle", "obj.water_bottle"],
                "target_ref": "answer.target",
                "condition_refs": ["rel.more_capacity"],
            },
            "plan": {
                "method": "compare_capacity",
                "description": "그림과 설명을 바탕으로 더 많이 들어가는 용기를 고른다.",
            },
            "execute": {
                "expected_operations": [
                    "identify_objects",
                    "compare_capacity",
                    "select_larger_container",
                ]
            },
            "review": {"check_methods": ["text_consistency_check"]},
        },
    },
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {"type": "selection", "description": "주스병과 물병 중 더 많이 들어가는 것"},
        "value": "물병",
        "unit": "",
    },
}

SOLVABLE = {
    "schema": "modu.solvable.v1.1",
    "problem_id": "S3_초등_3_008850",
    "problem_type": "comparison_choice",
    "inputs": {
        "total_ticks": 0,
        "target_label": "더 많이 들어가는 것",
        "target_ticks": 1,
        "target_count": 2,
        "unit": "",
    },
    "given": [
        {"ref": "obj.juice_bottle", "value": "주스병"},
        {"ref": "obj.water_bottle", "value": "물병"},
    ],
    "target": {"ref": "answer.target", "type": "selection"},
    "method": "compare_capacity",
    "plan": ["두 용기 중 더 많이 들어가는 용기를 고른다."],
    "steps": [{"id": "step.1", "expr": "주스병과 물병을 비교한다", "value": "물병"}],
    "checks": [
        {
            "id": "check.1",
            "expr": "선택된 답이 물병인지 확인한다",
            "expected": "물병",
            "actual": "물병",
            "pass": True,
        }
    ],
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {"type": "selection", "description": "주스병과 물병 중 더 많이 들어가는 것"},
        "value": "물병",
        "unit": "",
    },
}
