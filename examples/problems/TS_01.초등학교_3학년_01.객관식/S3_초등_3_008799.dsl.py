from __future__ import annotations
from modu_math.dsl import Canvas, ProblemTemplate, Region, TextSlot


def build_problem_template() -> ProblemTemplate:
    return ProblemTemplate(
        id="S3_초등_3_008799",
        title="무게가 더 무거운 것을 선택하세요",
        canvas=Canvas(width=720, height=360, coordinate_mode="logical"),
        regions=(
            Region(
                id="region.header",
                role="stem",
                flow="absolute",
                slot_ids=("slot.box", "slot.qnum", "slot.instruction"),
            ),
            Region(
                id="region.diagram",
                role="content",
                flow="absolute",
                slot_ids=("slot.scissor", "slot.bag_right", "slot.bag_left"),
            ),
            Region(id="region.footer", role="explanation", flow="absolute", slot_ids=()),
        ),
        slots=(
            TextSlot(
                id="slot.box",
                prompt="",
                text="□",
                style_role="question",
                x=15.0,
                y=30.0,
                font_size=22,
            ),
            TextSlot(
                id="slot.qnum",
                prompt="",
                text="28.",
                style_role="question",
                x=42.0,
                y=30.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.instruction",
                prompt="",
                text="무게가 더 무거운 것을 선택하세요.",
                style_role="question",
                x=77.0,
                y=30.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.scissor",
                prompt="",
                text="",
                style_role="content",
                x=322.0,
                y=92.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.bag_right",
                prompt="",
                text="",
                style_role="content",
                x=575.0,
                y=92.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.bag_left",
                prompt="",
                text="",
                style_role="content",
                x=62.0,
                y=213.0,
                font_size=28,
            ),
        ),
        diagrams=(),
        groups=(),
        constraints=(),
        tags=("비교", "무게", "그림선택"),
    )


PROBLEM_TEMPLATE = build_problem_template()

SEMANTIC_OVERRIDE = {
    "problem_id": "S3_초등_3_008799",
    "problem_type": "comparison_selection",
    "metadata": {
        "language": "ko",
        "question": "무게가 더 무거운 것을 선택하세요.",
        "instruction": "그림들 중 더 무거운 대상을 고르는 문제",
    },
    "domain": {
        "objects": [
            {"id": "obj.scissors", "type": "object", "name": "가위"},
            {"id": "obj.bag.left", "type": "object", "name": "책가방"},
            {"id": "obj.bag.right", "type": "object", "name": "책가방"},
        ],
        "relations": [],
        "problem_solving": {
            "understand": {
                "given_refs": ["obj.scissors", "obj.bag.left", "obj.bag.right"],
                "target_ref": "answer.target",
                "condition_refs": ["rel.compare_weight"],
            },
            "plan": {
                "method": "visual_weight_comparison",
                "description": "그림을 보고 더 무거운 대상을 고른다.",
            },
            "execute": {
                "expected_operations": ["compare_objects_by_weight", "select_heavier_object"]
            },
            "review": {"check_methods": ["answer_mark_consistency"]},
        },
    },
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {"type": "heavier_object", "description": "무게가 더 무거운 것"},
        "value": 0,
        "unit": "",
    },
}

SOLVABLE = {
    "schema": "modu.solvable.v1.1",
    "problem_id": "S3_초등_3_008799",
    "problem_type": "comparison_selection",
    "inputs": {
        "total_ticks": 0,
        "target_label": "무게가 더 무거운 것",
        "target_ticks": 0,
        "target_count": 1,
        "unit": "",
    },
    "given": [
        {"ref": "obj.scissors", "value": {"name": "가위"}},
        {"ref": "obj.bag.left", "value": {"name": "책가방"}},
        {"ref": "obj.bag.right", "value": {"name": "책가방"}},
    ],
    "target": {"ref": "answer.target", "type": "heavier_object"},
    "method": "visual_weight_comparison",
    "plan": ["그림에 있는 물체들을 확인한다.", "더 무거운 대상을 선택한다."],
    "steps": [
        {"id": "step.1", "expr": "그림의 대상 확인", "value": ["가위", "책가방", "책가방"]},
        {"id": "step.2", "expr": "더 무거운 대상 선택", "value": "TODO"},
    ],
    "checks": [
        {
            "id": "check.1",
            "expr": "정답 표시와 선택 대상 일치 여부 확인",
            "expected": "TODO",
            "actual": "TODO",
            "pass": False,
        }
    ],
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {"type": "heavier_object", "description": "무게가 더 무거운 것"},
        "value": 0,
        "unit": "",
    },
}
