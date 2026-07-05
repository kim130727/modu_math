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
)


def build_problem_template() -> ProblemTemplate:
    return ProblemTemplate(
        id="S3_초등_3_008813",
        title="들이가 더 적은 것 고르기",
        canvas=Canvas(width=944, height=440, coordinate_mode="logical"),
        regions=(
            Region(
                id="region.stem",
                role="stem",
                flow="absolute",
                slot_ids=("slot.q1", "slot.q2", "slot.q1.copy6"),
            ),
            Region(
                id="region.diagram",
                role="diagram",
                flow="absolute",
                slot_ids=("slot.bottle.label",),
            ),
            Region(id="region.choice", role="choice", flow="absolute", slot_ids=("slot.choice",)),
            Region(id="region.answer", role="answer", flow="absolute", slot_ids=()),
        ),
        slots=(
            TextSlot(
                id="slot.q1",
                prompt="",
                text="우유병에 물을 가득 채운 후 컵에 옮겨 담았더니 우유병에 물이 남았습니다.",
                style_role="question",
                x=14,
                y=47,
                font_size=28,
                fill="#111111",
            ),
            TextSlot(
                id="slot.q2",
                prompt="",
                text="",
                style_role="question",
                x=14.0,
                y=22.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.bottle.label",
                prompt="",
                text="우유병",
                style_role="label",
                x=262.0,
                y=278.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.choice",
                prompt="",
                text="( 우유병, 컵 )",
                style_role="choice",
                x=758.0,
                y=317.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.q1.copy6",
                prompt="",
                text="우유병과 컵 중에서 들이가 더 적은 것을 선택해 보세요.",
                x=14,
                y=87,
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
    "problem_id": "S3_초등_3_008813",
    "problem_type": "capacity_comparison",
    "metadata": {
        "language": "ko",
        "question": "우유병과 컵 중에서 들이가 더 적은 것을 선택하는 문제",
        "instruction": "우유병과 컵 중에서 들이가 더 적은 것을 선택해 보세요.",
    },
    "domain": {
        "objects": [
            {"id": "obj.bottle", "type": "container", "name": "우유병"},
            {"id": "obj.cup", "type": "container", "name": "컵"},
        ],
        "relations": [],
        "problem_solving": {
            "understand": {
                "given_refs": ["obj.bottle", "obj.cup", "rel.transfer"],
                "target_ref": "answer.target",
                "condition_refs": ["rel.capacity_order"],
            },
            "plan": {
                "method": "compare_container_capacity",
                "description": "옮겨 담은 뒤에도 남는 상황을 바탕으로 들이가 더 적은 용기를 찾는다.",
            },
            "execute": {"expected_operations": ["compare_capacity_by_remaining_liquid"]},
            "review": {"check_methods": ["answer_matches_visible_result"]},
        },
    },
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {"type": "container_name", "description": "들이가 더 적은 것"},
        "value": "컵",
        "unit": "",
    },
}

SOLVABLE = {
    "schema": "modu.solvable.v1.1",
    "problem_id": "S3_초등_3_008813",
    "problem_type": "capacity_comparison",
    "inputs": {
        "total_ticks": 0,
        "target_label": "들이가 더 적은 것",
        "target_ticks": 0,
        "target_count": 2,
        "unit": "",
    },
    "given": [
        {"ref": "obj.bottle", "value": "우유병"},
        {"ref": "obj.cup", "value": "컵"},
        {"ref": "rel.transfer", "value": "우유병의 물을 컵에 옮겨 담았더니 우유병에 물이 남음"},
    ],
    "target": {"ref": "answer.target", "type": "container_name"},
    "method": "compare_container_capacity",
    "plan": [
        "옮겨 담은 뒤에도 남는 용기가 더 큰 들이를 가진다.",
        "남는 물이 있는 쪽과 비교하여 들이가 더 적은 용기를 고른다.",
    ],
    "steps": [
        {"id": "step.1", "expr": "우유병의 물을 컵에 옮겨 담는다.", "value": "옮겨 담기"},
        {"id": "step.2", "expr": "우유병에 물이 남는다.", "value": "남음"},
        {"id": "step.3", "expr": "따라서 들이가 더 적은 용기를 선택한다.", "value": "컵"},
    ],
    "checks": [
        {
            "id": "check.1",
            "expr": "정답이 화면의 (정답) 표기와 일치하는가",
            "expected": "컵",
            "actual": "컵",
            "pass": True,
        }
    ],
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {"type": "container_name", "description": "들이가 더 적은 것"},
        "value": "컵",
        "unit": "",
    },
}
