from __future__ import annotations
from modu_math.dsl import Canvas, ProblemTemplate, Region, RectSlot, TextSlot


def build_problem_template() -> ProblemTemplate:
    return ProblemTemplate(
        id="S3_초등_3_008875",
        title="가 그릇과 나 그릇의 들이 비교",
        canvas=Canvas(width=960, height=540, coordinate_mode="logical"),
        regions=(
            Region(
                id="region.stem",
                role="stem",
                flow="absolute",
                slot_ids=(
                    "slot.q.no",
                    "slot.q.text1",
                    "slot.q.text2",
                    "slot.table.head.left",
                    "slot.table.head.right",
                    "slot.table.value.left",
                    "slot.table.value.right",
                    "slot.bubble.text",
                    "slot.name",
                    "slot.choice.o",
                    "slot.choice.x",
                ),
            ),
        ),
        slots=(
            TextSlot(
                id="slot.q.no",
                prompt="",
                text="30.",
                style_role="question",
                x=18.0,
                y=38.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.q.text1",
                prompt="",
                text="가 그릇과 나 그릇의 들이를 나타낸 것입니다. 주혁이 가 그릇과 나 그릇을",
                style_role="question",
                x=60.0,
                y=38.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.q.text2",
                prompt="",
                text="사용하여 양동이에 물 3 L를 담는 방법을 바르게 이야기했으면 ○, 그렇지 않으면 ×를 선택하세요.",
                style_role="question",
                x=60.0,
                y=74.0,
                font_size=28,
            ),
            RectSlot(
                id="slot.table.head.left", prompt="", x=270.0, y=132.0, width=214.0, height=44.0
            ),
            RectSlot(
                id="slot.table.head.right", prompt="", x=484.0, y=132.0, width=214.0, height=44.0
            ),
            RectSlot(
                id="slot.table.value.left", prompt="", x=270.0, y=176.0, width=214.0, height=44.0
            ),
            RectSlot(
                id="slot.table.value.right", prompt="", x=484.0, y=176.0, width=214.0, height=44.0
            ),
            TextSlot(
                id="slot.table.head.left.text",
                prompt="",
                text="가 그릇",
                style_role="label",
                x=351.0,
                y=162.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.table.head.right.text",
                prompt="",
                text="나 그릇",
                style_role="label",
                x=565.0,
                y=162.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.table.value.left.text",
                prompt="",
                text="4 L 200 mL",
                style_role="label",
                x=326.0,
                y=206.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.table.value.right.text",
                prompt="",
                text="1 L 200 mL",
                style_role="label",
                x=540.0,
                y=206.0,
                font_size=28,
            ),
            RectSlot(id="slot.bubble.box", prompt="", x=300.0, y=235.0, width=525.0, height=105.0),
            TextSlot(
                id="slot.bubble.text",
                prompt="",
                text="가 그릇에 물을 가득 담은 후 그 물을 나 그릇\n이 가득 찰 때까지 붓고 남는 물을 양동이에\n부으면 돼.",
                style_role="dialogue",
                x=318.0,
                y=264.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.name",
                prompt="",
                text="준혁",
                style_role="label",
                x=186.0,
                y=344.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.choice.o",
                prompt="",
                text="○",
                style_role="label",
                x=30.0,
                y=402.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.choice.x",
                prompt="",
                text="×",
                style_role="label",
                x=30.0,
                y=434.0,
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
    "problem_id": "S3_초등_3_008875",
    "problem_type": "ox_judgment",
    "metadata": {
        "language": "ko",
        "question": "가 그릇과 나 그릇의 들이를 비교하여 말풍선의 설명이 맞는지 ○/×로 고르는 문제",
        "instruction": "주어진 들이 관계를 보고 설명이 맞으면 ○, 아니면 ×를 선택한다.",
    },
    "domain": {
        "objects": [
            {
                "id": "obj.container_a",
                "type": "container",
                "label": "가 그릇",
                "capacity": "4 L 200 mL",
            },
            {
                "id": "obj.container_b",
                "type": "container",
                "label": "나 그릇",
                "capacity": "1 L 200 mL",
            },
            {"id": "obj.water_amount", "type": "quantity", "label": "3 L"},
            {"id": "obj.speaker", "type": "person", "label": "준혁"},
        ],
        "relations": [],
        "problem_solving": {
            "understand": {
                "given_refs": ["obj.container_a", "obj.container_b", "obj.water_amount"],
                "target_ref": "answer.target",
                "condition_refs": ["rel.compare_capacity"],
            },
            "plan": {
                "method": "compare_and_judge",
                "description": "두 그릇의 들이 관계를 비교하여 말풍선의 설명이 맞는지 판단한다.",
            },
            "execute": {"expected_operations": ["compare_capacities", "judge_statement"]},
            "review": {"check_methods": ["capacity_difference_consistency"]},
        },
    },
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {"type": "ox_choice", "description": "말풍선 속 설명의 옳고 그름"},
        "value": "○",
        "unit": "",
    },
}

SOLVABLE = {
    "schema": "modu.solvable.v1.1",
    "problem_id": "S3_초등_3_008875",
    "problem_type": "ox_judgment",
    "inputs": {
        "total_ticks": 0,
        "target_label": "말풍선 설명의 옳고 그름",
        "target_ticks": 0,
        "target_count": 1,
        "unit": "",
    },
    "given": [
        {"ref": "obj.container_a", "value": {"label": "가 그릇", "capacity": "4 L 200 mL"}},
        {"ref": "obj.container_b", "value": {"label": "나 그릇", "capacity": "1 L 200 mL"}},
    ],
    "target": {"ref": "answer.target", "type": "ox_choice"},
    "method": "compare_and_judge",
    "plan": ["두 그릇의 들이를 비교한다.", "말풍선 속 설명이 두 들이 관계와 맞는지 판단한다."],
    "steps": [
        {"id": "step.1", "expr": "4 L 200 mL - 1 L 200 mL", "value": "3 L"},
        {"id": "step.2", "expr": "말풍선 설명의 판단", "value": "○"},
    ],
    "checks": [
        {
            "id": "check.1",
            "expr": "4 L 200 mL - 1 L 200 mL = 3 L",
            "expected": "3 L",
            "actual": "3 L",
            "pass": True,
        }
    ],
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {"type": "ox_choice", "description": "말풍선 속 설명의 옳고 그름"},
        "value": "○",
        "unit": "",
    },
}
