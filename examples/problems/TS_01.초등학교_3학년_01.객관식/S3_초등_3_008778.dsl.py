from __future__ import annotations
from modu_math.dsl import (
    Canvas,
    CircleSlot,
    LineSlot,
    PathSlot,
    ProblemTemplate,
    RectSlot,
    Region,
    TextSlot,
)


def build_problem_template() -> ProblemTemplate:
    return ProblemTemplate(
        id="S3_초등_3_008778",
        title="들이가 더 많은 것 선택하기",
        canvas=Canvas(width=952, height=438, coordinate_mode="logical"),
        regions=(
            Region(
                id="region.stem",
                role="stem",
                flow="absolute",
                slot_ids=("slot.q1", "slot.q2", "slot.q3"),
            ),
            Region(
                id="region.diagram",
                role="diagram",
                flow="absolute",
                slot_ids=(
                    "slot.obj.bottle",
                    "slot.obj.cup_left",
                    "slot.obj.cup_right",
                    "slot.obj.kettle",
                    "slot.arrow.left",
                    "slot.arrow.right",
                    "slot.water.left",
                    "slot.water.right",
                ),
            ),
            Region(id="region.answer", role="answer", flow="absolute", slot_ids=("slot.choice",)),
        ),
        slots=(
            TextSlot(
                id="slot.q1",
                prompt="",
                text="□ 93. 물병과 주전자에 물을 가득 채웠다가 모양과 크기가 같은 그릇에 각각",
                style_role="question",
                x=10.0,
                y=34.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.q2",
                prompt="",
                text="옮겨 담았습니다. 물병과 주전자 중에서 들이가 더 많은 것을 선택해 보세",
                style_role="question",
                x=10.0,
                y=68.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.q3",
                prompt="",
                text="요.",
                style_role="question",
                x=10.0,
                y=102.0,
                font_size=28,
            ),
            RectSlot(
                id="slot.obj.bottle",
                prompt="",
                x=297.0,
                y=119.0,
                width=45.0,
                height=117.0,
                fill="#D7F0FF",
                stroke="#58B7E6",
                stroke_width=2.0,
            ),
            RectSlot(
                id="slot.obj.cup_left",
                prompt="",
                x=370.0,
                y=110.0,
                width=46.0,
                height=131.0,
                fill="#FFFFFF",
                stroke="#BFC8D4",
                stroke_width=2.0,
            ),
            RectSlot(
                id="slot.obj.cup_right",
                prompt="",
                x=430.0,
                y=110.0,
                width=46.0,
                height=131.0,
                fill="#FFFFFF",
                stroke="#BFC8D4",
                stroke_width=2.0,
            ),
            RectSlot(
                id="slot.obj.kettle",
                prompt="",
                x=616.0,
                y=118.0,
                width=92.0,
                height=100.0,
                fill="#ECEAF8",
                stroke="#B5B0D8",
                stroke_width=2.0,
            ),
            PathSlot(
                id="slot.arrow.left",
                prompt="",
                d="M 339.0 132.0 C 356.0 120.0, 362.0 112.0, 376.0 109.0",
                stroke="#FF4FA3",
                stroke_width=3.0,
                fill="none",
            ),
            PathSlot(
                id="slot.arrow.right",
                prompt="",
                d="M 612.0 130.0 C 595.0 118.0, 588.0 111.0, 573.0 109.0",
                stroke="#FF4FA3",
                stroke_width=3.0,
                fill="none",
            ),
            RectSlot(
                id="slot.water.left",
                prompt="",
                x=372.5,
                y=174.0,
                width=41.0,
                height=67.0,
                fill="#4FA9E6",
                stroke="none",
            ),
            RectSlot(
                id="slot.water.right",
                prompt="",
                x=432.5,
                y=149.0,
                width=41.0,
                height=92.0,
                fill="#4FA9E6",
                stroke="none",
            ),
            TextSlot(
                id="slot.choice",
                prompt="",
                text="( 물병 , 주전자 )",
                style_role="choice",
                x=740.0,
                y=316.0,
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
    "problem_id": "S3_초등_3_008778",
    "problem_type": "비교_들이",
    "metadata": {
        "language": "ko",
        "question": "물병과 주전자 중에서 들이가 더 많은 것을 선택하는 문제",
        "instruction": "옮겨 담은 물의 높이를 비교하여 더 많은 들이를 고른다.",
    },
    "domain": {
        "objects": [
            {"id": "obj.bottle", "type": "container", "name": "물병"},
            {"id": "obj.kettle", "type": "container", "name": "주전자"},
            {
                "id": "obj.comparison_cups",
                "type": "container_pair",
                "name": "같은 모양과 크기의 그릇",
            },
        ],
        "relations": [],
        "problem_solving": {
            "understand": {
                "given_refs": ["obj.bottle", "obj.kettle", "obj.comparison_cups"],
                "target_ref": "answer.target",
                "condition_refs": ["rel.compare_capacity"],
            },
            "plan": {
                "method": "compare_water_level",
                "description": "같은 그릇에 옮겨 담았을 때 더 높이 차는 쪽을 더 많은 들이로 본다.",
            },
            "execute": {
                "expected_operations": [
                    "observe_levels",
                    "compare_relative_height",
                    "select_larger_container",
                ]
            },
            "review": {"check_methods": ["compare_by_height", "match_with_given_choice"]},
        },
    },
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {"type": "selected_container", "description": "들이가 더 많은 것"},
        "value": "주전자",
        "unit": "",
    },
}

SOLVABLE = {
    "schema": "modu.solvable.v1.1",
    "problem_id": "S3_초등_3_008778",
    "problem_type": "비교_들이",
    "inputs": {
        "total_ticks": 2,
        "target_label": "들이가 더 많은 것",
        "target_ticks": 1,
        "target_count": 2,
        "unit": "",
    },
    "given": [
        {"ref": "obj.bottle", "value": "물병"},
        {"ref": "obj.kettle", "value": "주전자"},
        {"ref": "obj.comparison_cups", "value": "같은 모양과 크기의 그릇"},
    ],
    "target": {"ref": "answer.target", "type": "selected_container"},
    "plan": "같은 그릇에 옮겨 담은 물의 높이를 비교하여 더 높은 쪽을 고른다.",
    "steps": [
        {
            "id": "step.1",
            "expr": "같은 그릇에 옮겨 담은 물의 높이 비교",
            "value": "주전자 쪽이 더 높음",
        },
        {"id": "step.2", "expr": "더 높은 물높이 = 더 많은 들이", "value": "주전자"},
    ],
    "checks": [
        {
            "id": "check.1",
            "expr": "그림의 해설과 선택이 일치하는가",
            "expected": "주전자",
            "actual": "주전자",
            "pass": True,
        }
    ],
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {"type": "selected_container", "description": "들이가 더 많은 것"},
        "value": "주전자",
        "unit": "",
    },
}
