from __future__ import annotations
from modu_math.dsl import Canvas, ProblemTemplate, Region, TextSlot, CircleSlot


def build_problem_template() -> ProblemTemplate:
    return ProblemTemplate(
        id="S3_초등_3_008877",
        title="무게가 무거운 것부터 순서대로 나열하기",
        canvas=Canvas(width=920, height=430, coordinate_mode="logical"),
        regions=(
            Region(
                id="region.stem",
                role="stem",
                flow="absolute",
                slot_ids=("slot.q1", "slot.q2", "slot.q3"),
            ),
            Region(
                id="region.figures",
                role="diagram",
                flow="absolute",
                slot_ids=(
                    "slot.fruit.watermelon",
                    "slot.fruit.balloon",
                    "slot.fruit.melon",
                    "slot.lb.watermelon",
                    "slot.lb.balloon",
                    "slot.lb.melon",
                ),
            ),
            Region(
                id="region.options",
                role="choice",
                flow="absolute",
                slot_ids=(
                    "slot.opt1.num",
                    "slot.opt1.text",
                    "slot.opt2.num",
                    "slot.opt2.text",
                    "slot.opt3.num",
                    "slot.opt3.text",
                    "slot.opt4.num",
                    "slot.opt4.text",
                    "slot.opt5.num",
                    "slot.opt5.text",
                ),
            ),
            Region(id="region.answer", role="answer", flow="absolute", slot_ids=()),
        ),
        slots=(
            TextSlot(
                id="slot.q1",
                prompt="",
                text="□",
                style_role="question",
                x=16.0,
                y=30.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.q2",
                prompt="",
                text="32.",
                style_role="question",
                x=34.0,
                y=30.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.q3",
                prompt="",
                text="무게가 무거운 것부터 순서대로 바르게 나열한 것을 고르세요.",
                style_role="question",
                x=78.0,
                y=30.0,
                font_size=28,
            ),
            CircleSlot(
                id="slot.fruit.watermelon", prompt="", cx=300.0, cy=96.0, r=34.0, fill="#6DAA3A"
            ),
            CircleSlot(
                id="slot.fruit.balloon", prompt="", cx=452.0, cy=95.0, r=25.0, fill="#F46C43"
            ),
            CircleSlot(id="slot.fruit.melon", prompt="", cx=614.0, cy=94.0, r=24.0, fill="#F3C44E"),
            TextSlot(
                id="slot.lb.watermelon",
                prompt="",
                text="수박",
                style_role="label",
                x=283.0,
                y=152.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.lb.balloon",
                prompt="",
                text="풍선",
                style_role="label",
                x=436.0,
                y=152.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.lb.melon",
                prompt="",
                text="참외",
                style_role="label",
                x=600.0,
                y=152.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.opt1.num",
                prompt="",
                text="①",
                style_role="choice_number",
                x=24.0,
                y=214.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.opt1.text",
                prompt="",
                text="풍선, 수박, 참외",
                style_role="choice",
                x=54.0,
                y=214.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.opt2.num",
                prompt="",
                text="②",
                style_role="choice_number",
                x=494.0,
                y=214.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.opt2.text",
                prompt="",
                text="수박, 풍선, 참외",
                style_role="choice",
                x=524.0,
                y=214.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.opt3.num",
                prompt="",
                text="③",
                style_role="choice_number",
                x=24.0,
                y=264.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.opt3.text",
                prompt="",
                text="수박, 참외, 풍선",
                style_role="choice",
                x=54.0,
                y=264.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.opt4.num",
                prompt="",
                text="④",
                style_role="choice_number",
                x=494.0,
                y=264.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.opt4.text",
                prompt="",
                text="참외, 풍선, 수박",
                style_role="choice",
                x=524.0,
                y=264.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.opt5.num",
                prompt="",
                text="⑤",
                style_role="choice_number",
                x=24.0,
                y=314.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.opt5.text",
                prompt="",
                text="참외, 수박, 풍선",
                style_role="choice",
                x=54.0,
                y=314.0,
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
    "problem_id": "S3_초등_3_008877",
    "problem_type": "ordering_by_weight",
    "metadata": {
        "language": "ko",
        "question": "무게가 무거운 것부터 순서대로 바르게 나열한 것을 고르는 문제",
        "instruction": "보기 중 무거운 것부터 가벼운 것 순으로 된 순서를 찾는다.",
    },
    "domain": {
        "objects": [
            {"id": "obj.watermelon", "type": "object", "name": "수박"},
            {"id": "obj.balloon", "type": "object", "name": "풍선"},
            {"id": "obj.melon", "type": "object", "name": "참외"},
            {"id": "obj.options", "type": "choices", "count": 5},
        ],
        "relations": [],
        "problem_solving": {
            "understand": {
                "given_refs": ["obj.watermelon", "obj.balloon", "obj.melon", "rel.weight_order"],
                "target_ref": "answer.target",
                "condition_refs": ["rel.correct_choice"],
            },
            "plan": {
                "method": "ordering",
                "description": "무거운 것부터 가벼운 것 순서로 나열된 보기를 찾는다.",
            },
            "execute": {"expected_operations": ["compare_weight_order", "match_to_choice"]},
            "review": {"check_methods": ["order_consistency_check"]},
        },
    },
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {"type": "correct_choice", "description": "무거운 것부터 순서대로 나열한 보기"},
        "value": 3,
        "unit": "",
    },
}

SOLVABLE = {
    "schema": "modu.solvable.v1.1",
    "problem_id": "S3_초등_3_008877",
    "problem_type": "ordering_by_weight",
    "inputs": {
        "total_ticks": 3,
        "target_label": "무거운 것부터 순서",
        "target_ticks": 3,
        "target_count": 3,
        "unit": "",
    },
    "given": [
        {"ref": "obj.watermelon", "value": {"name": "수박"}},
        {"ref": "obj.balloon", "value": {"name": "풍선"}},
        {"ref": "obj.melon", "value": {"name": "참외"}},
    ],
    "target": {"ref": "answer.target", "type": "correct_choice"},
    "method": "ordering",
    "plan": [
        "무게가 더 무거운 것부터 보기의 순서를 확인한다.",
        "주어진 보기 중 무거운 것→가벼운 것 순서와 일치하는 것을 찾는다.",
    ],
    "steps": [
        {"id": "step.1", "expr": "수박, 참외, 풍선", "value": "무거운 것부터 가벼운 것 순서"},
        {"id": "step.2", "expr": "보기 ③", "value": 3},
    ],
    "checks": [
        {
            "id": "check.1",
            "expr": "보기 ③이 수박, 참외, 풍선과 일치하는가",
            "expected": True,
            "actual": True,
            "pass": True,
        }
    ],
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {"type": "correct_choice", "description": "무거운 것부터 순서대로 나열한 보기"},
        "value": 3,
        "unit": "",
    },
}
