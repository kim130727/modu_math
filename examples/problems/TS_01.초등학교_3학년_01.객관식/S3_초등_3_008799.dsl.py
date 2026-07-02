from __future__ import annotations
from modu_math.dsl import Canvas, ProblemTemplate, Region, TextSlot, ImageSlot


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
                slot_ids=(
                    "slot.instruction",
                    "slot.inserted.image.1",
                    "slot.inserted.image.2",
                    "slot.instruction.copy1",
                    "slot.instruction.copy1.copy2",
                ),
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
                id="slot.instruction",
                prompt="",
                text="무게가 더 무거운 것을 선택하세요.",
                style_role="question",
                x=17,
                y=50,
                font_size=28,
                fill="#111111",
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
            ImageSlot(
                id="slot.inserted.image.1",
                prompt="",
                href="data:image/png;base64,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",
                x=110,
                y=200,
                width=124,
                height=109,
                preserve_aspect_ratio="xMidYMid meet",
            ),
            ImageSlot(
                id="slot.inserted.image.2",
                prompt="",
                href="data:image/png;base64,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",
                x=360,
                y=115,
                width=230,
                height=205,
                preserve_aspect_ratio="xMidYMid meet",
            ),
            TextSlot(
                id="slot.instruction.copy1",
                prompt="",
                text="①",
                x=152,
                y=105,
                font_size=28,
                fill="#111111",
            ),
            TextSlot(
                id="slot.instruction.copy1.copy2",
                prompt="",
                text="②",
                x=462,
                y=105,
                font_size=28,
                fill="#111111",
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
        "value": "2번 책가방",
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
        "value": "2번 책가방",
        "unit": "",
    },
}
