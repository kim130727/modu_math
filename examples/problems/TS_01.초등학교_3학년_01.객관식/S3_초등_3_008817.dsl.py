from __future__ import annotations
from modu_math.dsl import Canvas, CircleSlot, LineSlot, ProblemTemplate, RectSlot, Region, TextSlot


def build_problem_template() -> ProblemTemplate:
    return ProblemTemplate(
        id="S3_초등_3_008817",
        title="들이가 더 많은 그릇 고르기",
        canvas=Canvas(width=940, height=408, coordinate_mode="logical"),
        regions=(
            Region(
                id="region.stem",
                role="stem",
                flow="absolute",
                slot_ids=("slot.q1", "slot.q2", "slot.q3", "slot.q4"),
            ),
            Region(
                id="region.diagram",
                role="diagram",
                flow="absolute",
                slot_ids=(
                    "slot.bowl.left.outer",
                    "slot.bowl.left.water",
                    "slot.bowl.left.line1",
                    "slot.bowl.left.line2",
                    "slot.bowl.left.line3",
                    "slot.bowl.left.line4",
                    "slot.bowl.left.line5",
                    "slot.bowl.right.outer",
                    "slot.bowl.right.water",
                    "slot.bowl.right.line1",
                    "slot.bowl.right.line2",
                    "slot.bowl.right.line3",
                    "slot.bowl.right.line4",
                    "slot.bowl.right.line5",
                    "slot.label.ga.circle",
                    "slot.label.na.circle",
                    "slot.label.ga.text",
                    "slot.label.na.text",
                    "slot.choice.text",
                ),
            ),
            Region(id="region.answer", role="answer", flow="absolute", slot_ids=()),
        ),
        slots=(
            TextSlot(
                id="slot.q1",
                prompt="",
                text="50.",
                style_role="question",
                x=44.0,
                y=34.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.q2",
                prompt="",
                text="가 그릇과 나 그릇에 물을 가득 채운 후 모양과 크기가 같은 그릇에 옮겨 담았더니 그림과 같이 물이 채워졌습니다. 들이가 더 많은 그릇을 선택해 보세요.",
                style_role="question",
                x=86.0,
                y=34.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.q3",
                prompt="",
                text="( 가, 나 ) 그릇",
                style_role="question",
                x=734.0,
                y=300.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.q4", prompt="", text="", style_role="question", x=0.0, y=0.0, font_size=28
            ),
            RectSlot(
                id="slot.bowl.left.outer", prompt="", x=294.0, y=120.0, width=134.0, height=122.0
            ),
            RectSlot(
                id="slot.bowl.left.water", prompt="", x=296.0, y=178.0, width=130.0, height=62.0
            ),
            LineSlot(id="slot.bowl.left.line1", prompt="", x1=294.0, y1=120.0, x2=321.0, y2=98.0),
            LineSlot(id="slot.bowl.left.line2", prompt="", x1=428.0, y1=120.0, x2=455.0, y2=98.0),
            LineSlot(id="slot.bowl.left.line3", prompt="", x1=428.0, y1=242.0, x2=455.0, y2=220.0),
            LineSlot(id="slot.bowl.left.line4", prompt="", x1=294.0, y1=120.0, x2=428.0, y2=120.0),
            LineSlot(id="slot.bowl.left.line5", prompt="", x1=294.0, y1=242.0, x2=428.0, y2=242.0),
            RectSlot(
                id="slot.bowl.right.outer", prompt="", x=556.0, y=120.0, width=134.0, height=122.0
            ),
            RectSlot(
                id="slot.bowl.right.water", prompt="", x=558.0, y=162.0, width=130.0, height=78.0
            ),
            LineSlot(id="slot.bowl.right.line1", prompt="", x1=556.0, y1=120.0, x2=583.0, y2=98.0),
            LineSlot(id="slot.bowl.right.line2", prompt="", x1=690.0, y1=120.0, x2=717.0, y2=98.0),
            LineSlot(id="slot.bowl.right.line3", prompt="", x1=690.0, y1=242.0, x2=717.0, y2=220.0),
            LineSlot(id="slot.bowl.right.line4", prompt="", x1=556.0, y1=120.0, x2=690.0, y2=120.0),
            LineSlot(id="slot.bowl.right.line5", prompt="", x1=556.0, y1=242.0, x2=690.0, y2=242.0),
            CircleSlot(
                id="slot.label.ga.circle", prompt="", cx=262.0, cy=122.0, r=12.0, fill="#ffffff"
            ),
            CircleSlot(
                id="slot.label.na.circle", prompt="", cx=523.0, cy=122.0, r=12.0, fill="#ffffff"
            ),
            TextSlot(
                id="slot.label.ga.text",
                prompt="",
                text="가",
                style_role="label",
                x=258.0,
                y=127.0,
                font_size=20,
            ),
            TextSlot(
                id="slot.label.na.text",
                prompt="",
                text="나",
                style_role="label",
                x=519.0,
                y=127.0,
                font_size=20,
            ),
            TextSlot(
                id="slot.choice.text",
                prompt="",
                text="",
                style_role="question",
                x=0.0,
                y=0.0,
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
    "problem_id": "S3_초등_3_008817",
    "problem_type": "비교_들이",
    "metadata": {
        "language": "ko",
        "question": "들이가 더 많은 그릇을 고르는 문제",
        "instruction": "그림을 보고 들이가 더 많은 그릇을 선택한다.",
    },
    "domain": {
        "objects": [
            {"id": "obj.bowl.ga", "type": "container", "name": "가 그릇"},
            {"id": "obj.bowl.na", "type": "container", "name": "나 그릇"},
        ],
        "relations": [],
        "problem_solving": {
            "understand": {
                "given_refs": [
                    "obj.bowl.ga",
                    "obj.bowl.na",
                    "rel.same_shape_size",
                    "rel.compare_water_height",
                ],
                "target_ref": "answer.target",
                "condition_refs": ["rel.same_shape_size", "rel.compare_water_height"],
            },
            "plan": {
                "method": "그림 비교",
                "description": "같은 모양과 크기의 그릇에서 물의 높이가 더 높은 쪽을 들이가 더 많은 그릇으로 본다.",
            },
            "execute": {"expected_operations": ["비교", "선택"]},
            "review": {"check_methods": ["그림의 물 높이 비교"]},
        },
    },
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {"type": "container_name", "description": "들이가 더 많은 그릇"},
        "value": 0,
        "unit": "",
    },
}

SOLVABLE = {
    "schema": "modu.solvable.v1.1",
    "problem_id": "S3_초등_3_008817",
    "problem_type": "비교_들이",
    "inputs": {
        "total_ticks": 2,
        "target_label": "들이가 더 많은 그릇",
        "target_ticks": 1,
        "target_count": 1,
        "unit": "",
    },
    "given": [
        {"ref": "obj.bowl.ga", "value": {"name": "가 그릇"}},
        {"ref": "obj.bowl.na", "value": {"name": "나 그릇"}},
    ],
    "target": {"ref": "answer.target", "type": "container_name"},
    "method": "그림 비교",
    "plan": [
        "두 그릇의 모양과 크기가 같은지 확인한다.",
        "물의 높이를 비교한다.",
        "물의 높이가 더 높은 그릇을 고른다.",
    ],
    "steps": [
        {
            "id": "step.1",
            "expr": "같은 모양과 크기의 그릇에서 물의 높이를 비교한다.",
            "value": "나 쪽이 더 높게 보임",
        },
        {"id": "step.2", "expr": "들이가 더 많은 그릇 선택", "value": "나 그릇"},
    ],
    "checks": [
        {
            "id": "check.1",
            "expr": "물의 높이가 더 높은 그릇을 선택했는가",
            "expected": "나 그릇",
            "actual": "나 그릇",
            "pass": True,
        }
    ],
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {"type": "container_name", "description": "들이가 더 많은 그릇"},
        "value": 0,
        "unit": "",
    },
}
