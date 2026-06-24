from __future__ import annotations
from modu_math.dsl import (
    Canvas,
    ProblemTemplate,
    Region,
    TextSlot,
    RectSlot,
    CircleSlot,
    PolygonSlot,
)


def build_problem_template() -> ProblemTemplate:
    return ProblemTemplate(
        id="S3_초등_3_008791",
        title="들이가 더 많은 컵 고르기",
        canvas=Canvas(width=960, height=520, coordinate_mode="logical"),
        regions=(
            Region(
                id="region.header",
                role="stem",
                flow="absolute",
                slot_ids=("slot.q_num", "slot.q_text"),
            ),
            Region(
                id="region.diagram.main",
                role="diagram",
                flow="absolute",
                slot_ids=(
                    "slot.bowl.body",
                    "slot.bowl.rim",
                    "slot.cup.a.top",
                    "slot.cup.a.body",
                    "slot.cup.a.label",
                    "slot.count.a",
                    "slot.cup.b.top",
                    "slot.cup.b.body",
                    "slot.cup.b.label",
                    "slot.count.b",
                ),
            ),
            Region(
                id="region.answer",
                role="answer",
                flow="absolute",
                slot_ids=("slot.answer.cup.top", "slot.answer.cup.body", "slot.answer.count"),
            ),
            Region(id="region.explain", role="explain", flow="absolute", slot_ids=()),
        ),
        slots=(
            TextSlot(
                id="slot.q_num",
                prompt="",
                text="16.",
                style_role="question",
                x=12.0,
                y=34.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.q_text",
                prompt="",
                text="왼쪽 그릇에 물을 가득 채우려면 ㉠ 컵과 ㉡ 컵에 물을 가득 채워 각각 다음과 같이 부어야 합니다. 들이가 더 많은 컵의 기호를 선택하세요.",
                style_role="question",
                x=58.0,
                y=34.0,
                font_size=28,
            ),
            PolygonSlot(
                id="slot.bowl.body",
                prompt="",
                points=((160.0, 100.0), (240.0, 100.0), (260.0, 150.0), (140.0, 150.0)),
            ),
            PolygonSlot(
                id="slot.bowl.rim",
                prompt="",
                points=((148.0, 100.0), (252.0, 100.0), (240.0, 104.0), (160.0, 104.0)),
            ),
            PolygonSlot(
                id="slot.cup.a.top",
                prompt="",
                points=((480.0, 90.0), (528.0, 90.0), (522.0, 98.0), (486.0, 98.0)),
            ),
            PolygonSlot(
                id="slot.cup.a.body",
                prompt="",
                points=((486.0, 98.0), (522.0, 98.0), (516.0, 140.0), (492.0, 140.0)),
            ),
            TextSlot(
                id="slot.cup.a.label",
                prompt="",
                text="가",
                style_role="label",
                x=500.0,
                y=121.0,
                font_size=28,
            ),
            RectSlot(id="slot.count.a", prompt="", x=463.0, y=158.0, width=92.0, height=52.0),
            TextSlot(
                id="slot.count.a.text",
                prompt="",
                text="6번",
                style_role="label",
                x=498.0,
                y=193.0,
                font_size=28,
            ),
            PolygonSlot(
                id="slot.cup.b.top",
                prompt="",
                points=((730.0, 110.0), (768.0, 110.0), (764.0, 116.0), (734.0, 116.0)),
            ),
            PolygonSlot(
                id="slot.cup.b.body",
                prompt="",
                points=((734.0, 116.0), (764.0, 116.0), (760.0, 150.0), (738.0, 150.0)),
            ),
            TextSlot(
                id="slot.cup.b.label",
                prompt="",
                text="나",
                style_role="label",
                x=749.0,
                y=136.0,
                font_size=28,
            ),
            RectSlot(id="slot.count.b", prompt="", x=718.0, y=160.0, width=92.0, height=52.0),
            TextSlot(
                id="slot.count.b.text",
                prompt="",
                text="9번",
                style_role="label",
                x=753.0,
                y=195.0,
                font_size=28,
            ),
            PolygonSlot(
                id="slot.answer.cup.top",
                prompt="",
                points=((70.0, 260.0), (118.0, 260.0), (112.0, 268.0), (76.0, 268.0)),
            ),
            PolygonSlot(
                id="slot.answer.cup.body",
                prompt="",
                points=((76.0, 268.0), (112.0, 268.0), (106.0, 310.0), (82.0, 310.0)),
            ),
            RectSlot(id="slot.answer.count", prompt="", x=58.0, y=320.0, width=92.0, height=52.0),
        ),
        diagrams=(),
        groups=(),
        constraints=(),
        tags=(),
    )


PROBLEM_TEMPLATE = build_problem_template()

SEMANTIC_OVERRIDE = {
    "problem_id": "S3_초등_3_008791",
    "problem_type": "comparison_capacity",
    "metadata": {
        "language": "ko",
        "question": "들이가 더 많은 컵의 기호를 선택하는 문제",
        "instruction": "들이가 더 많은 컵의 기호를 선택하세요.",
    },
    "domain": {
        "objects": [
            {"id": "obj.cup.a", "type": "cup", "symbol": "가"},
            {"id": "obj.cup.b", "type": "cup", "symbol": "나"},
            {"id": "obj.count.a", "type": "pour_count", "value": 6},
            {"id": "obj.count.b", "type": "pour_count", "value": 9},
        ],
        "relations": [],
        "problem_solving": {
            "understand": {
                "given_refs": ["obj.cup.a", "obj.cup.b", "obj.count.a", "obj.count.b"],
                "target_ref": "answer.target",
                "condition_refs": ["rel.more_capacity_from_fewer_pours"],
            },
            "plan": {
                "method": "compare_pour_counts",
                "description": "같은 양을 채우는 데 필요한 횟수를 비교하여 들이가 더 큰 컵을 고른다.",
            },
            "execute": {"expected_operations": ["compare_pour_counts", "select_smaller_count_cup"]},
            "review": {"check_methods": ["count_order_check"]},
        },
    },
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {"type": "cup_symbol", "description": "들이가 더 많은 컵의 기호"},
        "value": "가",
        "unit": "",
    },
}

SOLVABLE = {
    "schema": "modu.solvable.v1.1",
    "problem_id": "S3_초등_3_008791",
    "problem_type": "comparison_capacity",
    "inputs": {
        "total_ticks": 0,
        "target_label": "들이가 더 많은 컵의 기호",
        "target_ticks": 0,
        "target_count": 2,
        "unit": "",
    },
    "given": [{"ref": "obj.count.a", "value": 6}, {"ref": "obj.count.b", "value": 9}],
    "target": {"ref": "answer.target", "type": "cup_symbol"},
    "method": "compare_pour_counts",
    "plan": [
        "같은 양을 채우는 데 필요한 횟수를 비교한다.",
        "더 적은 횟수로 채워지는 컵을 선택한다.",
    ],
    "steps": [
        {"id": "step.1", "expr": "6 < 9", "value": True},
        {"id": "step.2", "expr": "더 적은 횟수에 해당하는 컵 선택", "value": "가"},
    ],
    "checks": [
        {
            "id": "check.1",
            "expr": "선택한 컵의 횟수가 더 적은지 확인",
            "expected": True,
            "actual": True,
            "pass": True,
        }
    ],
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {"type": "cup_symbol", "description": "들이가 더 많은 컵의 기호"},
        "value": "가",
        "unit": "",
    },
}
