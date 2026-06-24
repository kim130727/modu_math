from __future__ import annotations
from modu_math.dsl import Canvas, ProblemTemplate, Region, TextSlot, RectSlot, CircleSlot, LineSlot


def build_problem_template() -> ProblemTemplate:
    return ProblemTemplate(
        id="S3_초등_3_008868",
        title="오이와 토마토의 무게 비교",
        canvas=Canvas(width=960, height=454, coordinate_mode="logical"),
        regions=(
            Region(id="region.stem", role="stem", flow="absolute", slot_ids=("slot.q1", "slot.q2")),
            Region(
                id="region.diagram.left",
                role="diagram",
                flow="absolute",
                slot_ids=(
                    "slot.left.label",
                    "slot.left.scale.base",
                    "slot.left.scale.arm",
                    "slot.left.scale.pillar",
                    "slot.left.scale.pan.left",
                    "slot.left.scale.pan.right",
                    "slot.left.scale.cucumber",
                    "slot.left.scale.coins",
                    "slot.left.scale.count",
                ),
            ),
            Region(
                id="region.diagram.right",
                role="diagram",
                flow="absolute",
                slot_ids=(
                    "slot.right.label",
                    "slot.right.scale.base",
                    "slot.right.scale.arm",
                    "slot.right.scale.pillar",
                    "slot.right.scale.pan.left",
                    "slot.right.scale.pan.right",
                    "slot.right.scale.tomato",
                    "slot.right.scale.coins",
                    "slot.right.scale.count",
                ),
            ),
            Region(id="region.bottom", role="answer", flow="absolute", slot_ids=()),
        ),
        slots=(
            TextSlot(
                id="slot.q1",
                prompt="",
                text="19. 양팔 저울을 사용하여 오이와 토마토의 무게를 알아본 것입니다. 오이와",
                style_role="question",
                x=14.0,
                y=30.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.q2",
                prompt="",
                text="토마토 중에서 어느 것이 더 무거울까요?",
                style_role="question",
                x=14.0,
                y=66.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.left.label",
                prompt="",
                text="45개",
                style_role="caption",
                x=386.0,
                y=112.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.right.label",
                prompt="",
                text="39개",
                style_role="caption",
                x=616.0,
                y=112.0,
                font_size=28,
            ),
            RectSlot(
                id="slot.left.scale.base", prompt="", x=240.0, y=232.0, width=190.0, height=62.0
            ),
            LineSlot(id="slot.left.scale.arm", prompt="", x1=272.0, y1=203.0, x2=404.0, y2=203.0),
            LineSlot(
                id="slot.left.scale.pillar", prompt="", x1=337.0, y1=203.0, x2=337.0, y2=255.0
            ),
            CircleSlot(
                id="slot.left.scale.pan.left", prompt="", cx=286.0, cy=178.0, r=27.0, fill="#D9DEE8"
            ),
            CircleSlot(
                id="slot.left.scale.pan.right",
                prompt="",
                cx=388.0,
                cy=178.0,
                r=27.0,
                fill="#D9DEE8",
            ),
            RectSlot(
                id="slot.left.scale.cucumber", prompt="", x=270.0, y=145.0, width=48.0, height=16.0
            ),
            RectSlot(
                id="slot.left.scale.coins", prompt="", x=369.0, y=140.0, width=38.0, height=26.0
            ),
            TextSlot(
                id="slot.left.scale.count",
                prompt="",
                text="TODO: 동전 더미 세부 형태",
                style_role="caption",
                x=250.0,
                y=140.0,
                font_size=18,
            ),
            RectSlot(
                id="slot.right.scale.base", prompt="", x=547.0, y=232.0, width=190.0, height=62.0
            ),
            LineSlot(id="slot.right.scale.arm", prompt="", x1=579.0, y1=203.0, x2=711.0, y2=203.0),
            LineSlot(
                id="slot.right.scale.pillar", prompt="", x1=644.0, y1=203.0, x2=644.0, y2=255.0
            ),
            CircleSlot(
                id="slot.right.scale.pan.left",
                prompt="",
                cx=593.0,
                cy=178.0,
                r=27.0,
                fill="#D9DEE8",
            ),
            CircleSlot(
                id="slot.right.scale.pan.right",
                prompt="",
                cx=695.0,
                cy=178.0,
                r=27.0,
                fill="#D9DEE8",
            ),
            RectSlot(
                id="slot.right.scale.tomato", prompt="", x=577.0, y=145.0, width=50.0, height=28.0
            ),
            RectSlot(
                id="slot.right.scale.coins", prompt="", x=676.0, y=140.0, width=38.0, height=26.0
            ),
            TextSlot(
                id="slot.right.scale.count",
                prompt="",
                text="TODO: 동전 더미 세부 형태",
                style_role="caption",
                x=548.0,
                y=140.0,
                font_size=18,
            ),
        ),
        diagrams=(),
        groups=(),
        constraints=(),
        tags=(),
    )


PROBLEM_TEMPLATE = build_problem_template()

SEMANTIC_OVERRIDE = {
    "problem_id": "S3_초등_3_008868",
    "problem_type": "비교",
    "metadata": {
        "language": "ko",
        "question": "오이와 토마토 중에서 어느 것이 더 무거운지를 묻는 문제",
        "instruction": "그림과 해설에 보이는 비교 관계를 읽는다.",
    },
    "domain": {
        "objects": [
            {"id": "obj.cucumber", "type": "vegetable", "name": "오이"},
            {"id": "obj.tomato", "type": "vegetable", "name": "토마토"},
            {"id": "obj.coin_45", "type": "coin_count", "count": 45},
            {"id": "obj.coin_39", "type": "coin_count", "count": 39},
        ],
        "relations": [],
        "problem_solving": {
            "understand": {
                "given_refs": ["obj.cucumber", "obj.tomato", "obj.coin_45", "obj.coin_39"],
                "target_ref": "answer.target",
                "condition_refs": [
                    "rel.cucumber_equals_45coins",
                    "rel.tomato_equals_39coins",
                    "rel.compare_weight",
                ],
            },
            "plan": {
                "method": "비교하기",
                "description": "두 대상이 각각 대응하는 동전 개수를 비교하여 더 무거운 쪽을 찾는다.",
            },
            "execute": {"expected_operations": ["compare_coin_counts", "identify_heavier_object"]},
            "review": {"check_methods": ["larger_count_means_heavier"]},
        },
    },
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {"type": "heavier_object", "description": "오이와 토마토 중 더 무거운 것"},
        "value": "오이",
        "unit": "",
    },
}

SOLVABLE = {
    "schema": "modu.solvable.v1.1",
    "problem_id": "S3_초등_3_008868",
    "problem_type": "비교",
    "inputs": {
        "total_ticks": 45,
        "target_label": "더 무거운 것",
        "target_ticks": 39,
        "target_count": 1,
        "unit": "개",
    },
    "given": [
        {"ref": "obj.cucumber", "value": {"name": "오이", "coin_count": 45}},
        {"ref": "obj.tomato", "value": {"name": "토마토", "coin_count": 39}},
    ],
    "target": {"ref": "answer.target", "type": "heavier_object"},
    "method": "비교하기",
    "plan": [
        "오이와 토마토가 각각 몇 개의 동전 무게와 같은지 확인한다.",
        "동전 개수가 더 많은 쪽이 더 무겁다고 비교한다.",
    ],
    "steps": [
        {"id": "step.1", "expr": "45와 39를 비교한다.", "value": {"left": 45, "right": 39}},
        {"id": "step.2", "expr": "45 > 39", "value": True},
        {"id": "step.3", "expr": "더 무거운 것은 오이이다.", "value": "오이"},
    ],
    "checks": [
        {
            "id": "check.1",
            "expr": "동전 개수가 더 많은 쪽이 더 무거운가?",
            "expected": True,
            "actual": True,
            "pass": True,
        }
    ],
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {"type": "heavier_object", "description": "오이와 토마토 중 더 무거운 것"},
        "value": "오이",
        "unit": "",
    },
}
