from __future__ import annotations
from modu_math.dsl import Canvas, ProblemTemplate, Region, RectSlot, TextSlot


def build_problem_template() -> ProblemTemplate:
    return ProblemTemplate(
        id="S3_초등_3_008856",
        title="가장 무거운 것",
        canvas=Canvas(width=846, height=482, coordinate_mode="logical"),
        regions=(
            Region(id="region.stem", role="stem", flow="absolute", slot_ids=("slot.q1", "slot.q2")),
            Region(
                id="region.diagram",
                role="diagram",
                flow="absolute",
                slot_ids=(
                    "slot.person",
                    "slot.person_name",
                    "slot.box",
                    "slot.box_text1",
                    "slot.box_text2",
                    "slot.box_text3",
                    "slot.box_text4",
                    "slot.choices",
                ),
            ),
            Region(id="region.answer", role="answer", flow="absolute", slot_ids=()),
        ),
        slots=(
            TextSlot(
                id="slot.q1",
                prompt="",
                text="□ 2. 은우가 가위, 풀, 지우개의 무게를 다음과 같이 비교하였습니다. 가위, 풀,",
                style_role="question",
                x=14.0,
                y=30.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.q2",
                prompt="",
                text="지우개 중 가장 무거운 것은 어느 것인가요?",
                style_role="question",
                x=35.0,
                y=63.0,
                font_size=28,
            ),
            RectSlot(id="slot.person", prompt="", x=70.0, y=96.0, width=110.0, height=110.0),
            TextSlot(
                id="slot.person_name",
                prompt="",
                text="은우",
                style_role="label",
                x=108.0,
                y=227.0,
                font_size=28,
            ),
            RectSlot(id="slot.box", prompt="", x=258.0, y=81.0, width=412.0, height=162.0),
            TextSlot(
                id="slot.box_text1",
                prompt="",
                text="가위와 풀을 양손에 각각 들면",
                style_role="body",
                x=323.0,
                y=106.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.box_text2",
                prompt="",
                text="가위를 든 손에 힘이 더 많이 들고,",
                style_role="body",
                x=294.0,
                y=140.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.box_text3",
                prompt="",
                text="풀과 지우개를 양손에 각각 들면",
                style_role="body",
                x=296.0,
                y=174.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.box_text4",
                prompt="",
                text="풀을 든 손에 힘이 더 많이 들어.",
                style_role="body",
                x=297.0,
                y=208.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.choices",
                prompt="",
                text="( 가위 , 풀 , 지우개 )",
                style_role="body",
                x=600.0,
                y=258.0,
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
    "problem_id": "S3_초등_3_008856",
    "problem_type": "비교_무게_순서",
    "metadata": {
        "language": "ko",
        "question": "가위, 풀, 지우개의 무게 비교를 바탕으로 가장 무거운 것을 찾는 문제",
        "instruction": "비교 문장을 읽고 가장 무거운 것을 고른다.",
    },
    "domain": {
        "objects": [
            {"id": "obj.scissors", "type": "item", "name": "가위"},
            {"id": "obj.glue", "type": "item", "name": "풀"},
            {"id": "obj.eraser", "type": "item", "name": "지우개"},
        ],
        "relations": [],
        "problem_solving": {
            "understand": {
                "given_refs": [
                    "obj.scissors",
                    "obj.glue",
                    "obj.eraser",
                    "rel.scissors_heavier_than_glue",
                    "rel.glue_heavier_than_eraser",
                ],
                "target_ref": "answer.target",
                "condition_refs": [
                    "rel.scissors_heavier_than_glue",
                    "rel.glue_heavier_than_eraser",
                ],
            },
            "plan": {
                "method": "compare_heaviness_order",
                "description": "비교 문장에서 더 무거운 대상을 찾아 순서를 정리한다.",
            },
            "execute": {
                "expected_operations": [
                    "identify_heavier_object_from_each_comparison",
                    "combine_order_relations",
                    "select_heaviest_object",
                ]
            },
            "review": {"check_methods": ["relation_consistency_check", "heaviest_selection_check"]},
        },
    },
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {"type": "heaviest_object", "description": "가장 무거운 것"},
        "value": "가위",
        "unit": "",
    },
}

SOLVABLE = {
    "schema": "modu.solvable.v1.1",
    "problem_id": "S3_초등_3_008856",
    "problem_type": "비교_무게_순서",
    "inputs": {
        "total_ticks": 1,
        "target_label": "가장 무거운 것",
        "target_ticks": 1,
        "target_count": 1,
        "unit": "",
    },
    "given": [
        {"ref": "obj.scissors", "value": {"name": "가위"}},
        {"ref": "obj.glue", "value": {"name": "풀"}},
        {"ref": "obj.eraser", "value": {"name": "지우개"}},
        {"ref": "rel.scissors_heavier_than_glue", "value": {"from": "가위", "to": "풀"}},
        {"ref": "rel.glue_heavier_than_eraser", "value": {"from": "풀", "to": "지우개"}},
    ],
    "target": {"ref": "answer.target", "type": "heaviest_object"},
    "method": "compare_heaviness_order",
    "plan": [
        "비교 문장에서 더 무거운 대상을 찾는다.",
        "두 비교 결과를 연결하여 무게 순서를 정리한다.",
        "가장 무거운 대상을 고른다.",
    ],
    "steps": [
        {"id": "step.1", "expr": "가위와 풀을 비교하면 가위가 더 무겁다.", "value": "가위 > 풀"},
        {"id": "step.2", "expr": "풀과 지우개를 비교하면 풀이 더 무겁다.", "value": "풀 > 지우개"},
        {
            "id": "step.3",
            "expr": "두 관계를 합치면 가위 > 풀 > 지우개 이다.",
            "value": "가위 > 풀 > 지우개",
        },
        {"id": "step.4", "expr": "가장 무거운 것을 선택한다.", "value": "가위"},
    ],
    "checks": [
        {
            "id": "check.1",
            "expr": "가위가 풀보다 무거운가?",
            "expected": "가위 > 풀",
            "actual": "가위 > 풀",
            "pass": True,
        },
        {
            "id": "check.2",
            "expr": "풀이 지우개보다 무거운가?",
            "expected": "풀 > 지우개",
            "actual": "풀 > 지우개",
            "pass": True,
        },
        {
            "id": "check.3",
            "expr": "가장 무거운 대상이 가위인가?",
            "expected": "가위",
            "actual": "가위",
            "pass": True,
        },
    ],
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {"type": "heaviest_object", "description": "가장 무거운 것"},
        "value": "가위",
        "unit": "",
    },
}
