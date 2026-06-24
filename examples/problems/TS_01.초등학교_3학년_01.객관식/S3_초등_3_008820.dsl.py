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
        id="S3_초등_3_008820",
        title="들이가 가장 적은 그릇 고르기",
        canvas=Canvas(width=944.0, height=408.0, coordinate_mode="logical"),
        regions=(
            Region(
                id="region.stem",
                role="stem",
                flow="absolute",
                slot_ids=("slot.q.no", "slot.q1", "slot.q2"),
            ),
            Region(
                id="region.diagram",
                role="diagram",
                flow="absolute",
                slot_ids=(
                    "slot.label.ga",
                    "slot.label.na",
                    "slot.label.da",
                    "slot.bowl.ga.left",
                    "slot.bowl.ga.right",
                    "slot.arrow.ga",
                    "slot.bowl.na.left",
                    "slot.bowl.na.right",
                    "slot.arrow.na",
                    "slot.bowl.da.left",
                    "slot.bowl.da.right",
                    "slot.arrow.da",
                    "slot.option.text",
                ),
            ),
            Region(id="region.answer", role="answer", flow="absolute", slot_ids=()),
        ),
        slots=(
            TextSlot(
                id="slot.q.no",
                prompt="",
                text="□ 54.",
                style_role="question",
                x=16.0,
                y=30.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.q1",
                prompt="",
                text="가 그릇, 나 그릇, 다 그릇에 물을 가득 채운 후 모양과 같은 그릇",
                style_role="question",
                x=100.0,
                y=30.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.q2",
                prompt="",
                text="에 옮겨 담았습니다. 그림과 같이 물을 채웠을 때 가 그릇, 나 그릇, 다 그",
                style_role="question",
                x=36.0,
                y=66.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.q3",
                prompt="",
                text="릇 중 들이가 가장 적은 것은 어느 것인지 선택하세요.",
                style_role="question",
                x=36.0,
                y=102.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.label.ga",
                prompt="",
                text="가",
                style_role="label",
                x=104.0,
                y=140.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.label.na",
                prompt="",
                text="나",
                style_role="label",
                x=348.0,
                y=140.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.label.da",
                prompt="",
                text="다",
                style_role="label",
                x=596.0,
                y=140.0,
                font_size=28,
            ),
            RectSlot(id="slot.bowl.ga.left", prompt="", x=124.0, y=172.0, width=62.0, height=62.0),
            RectSlot(id="slot.bowl.ga.right", prompt="", x=246.0, y=164.0, width=62.0, height=70.0),
            LineSlot(id="slot.arrow.ga", prompt="", x1=196.0, y1=206.0, x2=236.0, y2=206.0),
            RectSlot(id="slot.bowl.na.left", prompt="", x=360.0, y=180.0, width=62.0, height=54.0),
            RectSlot(id="slot.bowl.na.right", prompt="", x=482.0, y=164.0, width=62.0, height=70.0),
            LineSlot(id="slot.arrow.na", prompt="", x1=432.0, y1=206.0, x2=472.0, y2=206.0),
            RectSlot(id="slot.bowl.da.left", prompt="", x=606.0, y=176.0, width=58.0, height=58.0),
            RectSlot(id="slot.bowl.da.right", prompt="", x=728.0, y=164.0, width=62.0, height=70.0),
            LineSlot(id="slot.arrow.da", prompt="", x1=678.0, y1=206.0, x2=718.0, y2=206.0),
            TextSlot(
                id="slot.option.text",
                prompt="",
                text="(가 그릇, 나 그릇, 다 그릇)",
                style_role="body",
                x=642.0,
                y=250.0,
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
    "problem_id": "S3_초등_3_008820",
    "problem_type": "comparison_choice",
    "metadata": {
        "language": "ko",
        "question": "그림을 보고 들이가 가장 적은 그릇을 고르는 문제",
        "instruction": "들이가 가장 적은 것을 선택하세요.",
        "points": 5,
    },
    "domain": {
        "objects": [
            {"id": "obj.ga_bowl", "type": "container", "label": "가 그릇"},
            {"id": "obj.na_bowl", "type": "container", "label": "나 그릇"},
            {"id": "obj.da_bowl", "type": "container", "label": "다 그릇"},
        ],
        "relations": [],
        "problem_solving": {
            "understand": {
                "given_refs": [
                    "obj.ga_bowl",
                    "obj.na_bowl",
                    "obj.da_bowl",
                    "rel.compare_water_level",
                ],
                "target_ref": "answer.target",
                "condition_refs": ["rel.choose_min_capacity"],
            },
            "plan": {
                "method": "visual_comparison",
                "description": "그릇에 담긴 물의 높이를 비교하여 들이를 판단한다.",
            },
            "execute": {
                "expected_operations": [
                    "compare_water_levels",
                    "identify_lowest_level",
                    "select_min_capacity_bowl",
                ]
            },
            "review": {
                "check_methods": [
                    "water_level_consistency_check",
                    "choice_matches_printed_explanation",
                ]
            },
        },
    },
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {"type": "selected_container", "description": "들이가 가장 적은 그릇"},
        "value": 2,
        "unit": "",
    },
}

SOLVABLE = {
    "schema": "modu.solvable.v1.1",
    "problem_id": "S3_초등_3_008820",
    "problem_type": "comparison_choice",
    "inputs": {
        "total_ticks": 3,
        "target_label": "가, 나, 다",
        "target_ticks": 1,
        "target_count": 3,
        "unit": "",
    },
    "given": [
        {"ref": "obj.ga_bowl", "value": {"label": "가 그릇"}},
        {"ref": "obj.na_bowl", "value": {"label": "나 그릇"}},
        {"ref": "obj.da_bowl", "value": {"label": "다 그릇"}},
    ],
    "target": {"ref": "answer.target", "type": "selected_container"},
    "method": "visual_comparison",
    "plan": ["세 그릇의 물 높이를 비교한다.", "가장 낮은 물 높이의 그릇을 고른다."],
    "steps": [
        {"id": "step.1", "expr": "물의 높이 비교", "value": "나 그릇이 가장 낮음"},
        {"id": "step.2", "expr": "들이가 가장 적은 그릇 선택", "value": "나 그릇"},
    ],
    "checks": [
        {
            "id": "check.1",
            "expr": "해설 문장과 선택 결과가 일치하는가",
            "expected": "나 그릇",
            "actual": "나 그릇",
            "pass": True,
        }
    ],
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {"type": "selected_container", "description": "들이가 가장 적은 그릇"},
        "value": 2,
        "unit": "",
    },
}
