from __future__ import annotations
from modu_math.dsl import Canvas, ProblemTemplate, Region, TextSlot, RectSlot


def build_problem_template() -> ProblemTemplate:
    return ProblemTemplate(
        id="S3_초등_3_008839",
        title="키위와 복숭아의 무게 비교",
        canvas=Canvas(width=920, height=620, coordinate_mode="logical"),
        regions=(
            Region(id="region.stem", role="stem", flow="absolute", slot_ids=("slot.q1", "slot.q2")),
            Region(
                id="region.diagram",
                role="diagram",
                flow="absolute",
                slot_ids=(
                    "slot.lb.no",
                    "slot.stem.label1",
                    "slot.stem.label2",
                    "slot.lb.kiwi",
                    "slot.lb.orange",
                    "slot.lb.balloon_name",
                    "slot.balloon",
                    "slot.choice.1",
                    "slot.choice.2",
                    "slot.choice.3",
                ),
            ),
        ),
        slots=(
            TextSlot(
                id="slot.q1",
                prompt="",
                text="81. 영재는 키위와 복숭아의 무게를 다음과 같이 비교했습니다. 몸에 답하세요.",
                style_role="question",
                x=14.0,
                y=34.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.q2",
                prompt="",
                text="",
                style_role="question",
                x=14.0,
                y=70.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.lb.no",
                prompt="",
                text="81.",
                style_role="label",
                x=10.0,
                y=28.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.stem.label1",
                prompt="",
                text="키위",
                style_role="label",
                x=242.0,
                y=108.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.stem.label2",
                prompt="",
                text="100원짜리\n동전 15개",
                style_role="label",
                x=326.0,
                y=100.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.lb.kiwi",
                prompt="",
                text="복숭아",
                style_role="label",
                x=535.0,
                y=108.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.lb.orange",
                prompt="",
                text="500원짜리\n동전 15개",
                style_role="label",
                x=615.0,
                y=100.0,
                font_size=28,
            ),
            RectSlot(
                id="slot.balloon",
                prompt="",
                x=310.0,
                y=274.0,
                width=380.0,
                height=118.0,
                fill="#f7d59f",
            ),
            TextSlot(
                id="slot.lb.balloon_name",
                prompt="",
                text="영재",
                style_role="label",
                x=114.0,
                y=360.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.choice.1",
                prompt="",
                text="(2) 알맞은 말을 선택하여 이유를 완성해 보세요.\n동전의 ( 수 , 무게 )는 같지만 100원짜리 동전과 500원짜리 동전의 ( 수 ,\n무게 )가 서로 다르기 때문입니다.",
                style_role="question",
                x=10.0,
                y=432.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.choice.2",
                prompt="",
                text="(2) 키위와 복숭아의 무게를 나타낸 100원짜리 동전과 500원짜리 동전의 수\n는 같지만 100원짜리 동전과 500원짜리 동전의 무게가 서로 다르기 때\n문입니다.",
                style_role="question",
                x=10.0,
                y=496.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.choice.3",
                prompt="",
                text="(2) 수, 무게",
                style_role="question",
                x=10.0,
                y=588.0,
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
    "problem_id": "S3_초등_3_008839",
    "problem_type": "reason_selection",
    "metadata": {
        "language": "ko",
        "question": "키위와 복숭아의 무게 비교를 보고 알맞은 이유를 선택하는 문제",
        "instruction": "알맞은 말을 선택하여 이유를 완성해 보세요.",
    },
    "domain": {
        "objects": [
            {"id": "obj.kiwi", "type": "fruit", "name": "키위"},
            {"id": "obj.peach", "type": "fruit", "name": "복숭아"},
            {"id": "obj.coin_100", "type": "coin", "name": "100원짜리 동전"},
            {"id": "obj.coin_500", "type": "coin", "name": "500원짜리 동전"},
            {"id": "obj.count_15", "type": "count", "value": 15},
        ],
        "relations": [],
        "problem_solving": {
            "understand": {
                "given_refs": [
                    "obj.kiwi",
                    "obj.peach",
                    "obj.coin_100",
                    "obj.coin_500",
                    "obj.count_15",
                ],
                "target_ref": "answer.target",
                "condition_refs": [
                    "rel.kiwi_compares_to_100",
                    "rel.peach_compares_to_500",
                    "rel.compare_reason",
                ],
            },
            "plan": {
                "method": "reason_selection",
                "description": "그림에서 같은 수와 무게의 차이를 나타내는 말을 찾는다.",
            },
            "execute": {
                "expected_operations": ["compare_counts", "compare_weights", "select_reason"]
            },
            "review": {"check_methods": ["statement_matches_image", "meaning_consistency_check"]},
        },
    },
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {"type": "reason_selection", "description": "알맞은 이유 문장"},
        "value": 0,
        "unit": "",
    },
}

SOLVABLE = {
    "schema": "modu.solvable.v1.1",
    "problem_id": "S3_초등_3_008839",
    "problem_type": "reason_selection",
    "inputs": {
        "total_ticks": 15,
        "target_label": "이유",
        "target_ticks": 15,
        "target_count": 2,
        "unit": "개",
    },
    "given": [
        {"ref": "obj.kiwi", "value": {"name": "키위"}},
        {"ref": "obj.peach", "value": {"name": "복숭아"}},
        {"ref": "obj.coin_100", "value": {"name": "100원짜리 동전"}},
        {"ref": "obj.coin_500", "value": {"name": "500원짜리 동전"}},
        {"ref": "obj.count_15", "value": 15},
    ],
    "target": {"ref": "answer.target", "type": "reason_selection"},
    "method": "reason_selection",
    "plan": [
        "그림에서 두 비교가 각각 어떤 동전과 연결되는지 확인한다.",
        "같은 수와 다른 무게의 관계를 나타내는 문장을 고른다.",
    ],
    "steps": [
        {
            "id": "step.1",
            "expr": "키위 ↔ 100원짜리 동전 15개, 복숭아 ↔ 500원짜리 동전 15개",
            "value": "관계 확인",
        },
        {"id": "step.2", "expr": "이유 문장 선택", "value": "수와 무게를 구분하는 이유"},
    ],
    "checks": [
        {
            "id": "check.1",
            "expr": "그림의 비교 관계와 문장의 의미가 일치하는가",
            "expected": True,
            "actual": True,
            "pass": True,
        }
    ],
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {"type": "reason_selection", "description": "알맞은 이유 문장"},
        "value": 0,
        "unit": "",
    },
}
