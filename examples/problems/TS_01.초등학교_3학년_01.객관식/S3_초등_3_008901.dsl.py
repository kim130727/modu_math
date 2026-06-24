from __future__ import annotations
from modu_math.dsl import Canvas, ProblemTemplate, Region, RectSlot, TextSlot


def build_problem_template() -> ProblemTemplate:
    return ProblemTemplate(
        id="S3_초등_3_008901",
        title="팔린 아이스크림 수",
        canvas=Canvas(width=940.0, height=680.0, coordinate_mode="logical"),
        regions=(
            Region(
                id="region.stem",
                role="stem",
                flow="absolute",
                slot_ids=(
                    "slot.q_no",
                    "slot.q_text_1",
                    "slot.q_text_2",
                    "slot.title",
                    "slot.table.head1",
                    "slot.table.head2",
                    "slot.table.row1.label",
                    "slot.table.row2.label",
                    "slot.table.row3.label",
                    "slot.table.row4.label",
                    "slot.legend.big",
                    "slot.legend.small",
                    "slot.choice",
                ),
            ),
        ),
        slots=(
            TextSlot(
                id="slot.q_no",
                prompt="",
                text="□ 67.",
                style_role="question",
                x=12.0,
                y=22.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.q_text_1",
                prompt="",
                text="어느 가게에서 일주일 동안 팔린 아이스크림 수를 조사하여 그림그래프로 나타내었습니다.",
                style_role="question",
                x=92.0,
                y=22.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.q_text_2",
                prompt="",
                text="딸기 맛과 바닐라 맛 아이스크림 중 더 많이 팔린 아이스크림을 선택해 보세요.",
                style_role="question",
                x=12.0,
                y=56.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.title",
                prompt="",
                text="팔린 아이스크림 수",
                style_role="title",
                x=396.0,
                y=110.0,
                font_size=28,
            ),
            RectSlot(id="slot.table.outer", prompt="", x=244.0, y=122.0, width=480.0, height=284.0),
            RectSlot(
                id="slot.table.head_bg", prompt="", x=244.0, y=122.0, width=480.0, height=40.0
            ),
            RectSlot(
                id="slot.table.left_bg", prompt="", x=244.0, y=162.0, width=140.0, height=244.0
            ),
            TextSlot(
                id="slot.table.head1",
                prompt="",
                text="맛",
                style_role="table_header",
                x=298.0,
                y=149.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.table.head2",
                prompt="",
                text="아이스크림 수",
                style_role="table_header",
                x=470.0,
                y=149.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.table.row1.label",
                prompt="",
                text="멜론 맛",
                style_role="table_cell",
                x=294.0,
                y=200.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.table.row2.label",
                prompt="",
                text="딸기 맛",
                style_role="table_cell",
                x=294.0,
                y=248.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.table.row3.label",
                prompt="",
                text="초콜릿 맛",
                style_role="table_cell",
                x=286.0,
                y=296.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.table.row4.label",
                prompt="",
                text="바닐라 맛",
                style_role="table_cell",
                x=286.0,
                y=344.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.legend.big",
                prompt="",
                text="10개",
                style_role="caption",
                x=660.0,
                y=438.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.legend.small",
                prompt="",
                text="1개",
                style_role="caption",
                x=758.0,
                y=438.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.choice",
                prompt="",
                text="( 딸기 맛 , 바닐라 맛 )",
                style_role="caption",
                x=650.0,
                y=520.0,
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
    "problem_id": "S3_초등_3_008901",
    "problem_type": "picture_graph_compare",
    "metadata": {
        "language": "ko",
        "question": "딸기 맛과 바닐라 맛 아이스크림 중 더 많이 팔린 아이스크림을 선택하는 문제",
        "instruction": "더 많이 팔린 아이스크림을 고르기",
    },
    "domain": {
        "objects": [
            {"id": "obj.legend.big", "type": "picture_symbol", "meaning": 10},
            {"id": "obj.legend.small", "type": "picture_symbol", "meaning": 1},
            {"id": "obj.strawberry", "type": "category", "label": "딸기 맛"},
            {"id": "obj.vanilla", "type": "category", "label": "바닐라 맛"},
        ],
        "relations": [],
        "problem_solving": {
            "understand": {
                "given_refs": [
                    "obj.legend.big",
                    "obj.legend.small",
                    "obj.strawberry",
                    "obj.vanilla",
                ],
                "target_ref": "answer.target",
                "condition_refs": ["rel.compare"],
            },
            "plan": {
                "method": "count_and_compare",
                "description": "범례에 따라 그림 개수를 읽고 두 맛의 양을 비교한다.",
            },
            "execute": {"expected_operations": ["read_symbol_values", "compare_two_categories"]},
            "review": {"check_methods": ["compare_with_legend"]},
        },
    },
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {"type": "larger_quantity_category", "description": "더 많이 팔린 아이스크림"},
        "value": "딸기 맛",
        "unit": "",
    },
}

SOLVABLE = {
    "schema": "modu.solvable.v1.1",
    "problem_id": "S3_초등_3_008901",
    "problem_type": "picture_graph_compare",
    "inputs": {
        "total_ticks": 0,
        "target_label": "더 많이 팔린 아이스크림",
        "target_ticks": 0,
        "target_count": 0,
        "unit": "",
    },
    "given": [
        {"ref": "obj.legend.big", "value": 10},
        {"ref": "obj.legend.small", "value": 1},
        {"ref": "obj.strawberry", "value": {"big": 2, "small": 3}},
        {"ref": "obj.vanilla", "value": {"big": 1, "small": 6}},
    ],
    "target": {"ref": "answer.target", "type": "larger_quantity_category"},
    "method": "count_and_compare",
    "plan": [
        "범례를 읽어 큰 그림과 작은 그림의 값을 확인한다.",
        "딸기 맛과 바닐라 맛의 총 개수를 각각 구한다.",
        "두 값을 비교하여 더 큰 쪽을 찾는다.",
    ],
    "steps": [
        {"id": "step.1", "expr": "딸기 맛 = 2×10 + 3×1", "value": 23},
        {"id": "step.2", "expr": "바닐라 맛 = 1×10 + 6×1", "value": 16},
        {"id": "step.3", "expr": "23과 16을 비교", "value": "딸기 맛"},
    ],
    "checks": [
        {"id": "check.1", "expr": "23 > 16", "expected": True, "actual": True, "pass": True}
    ],
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {"type": "larger_quantity_category", "description": "더 많이 팔린 아이스크림"},
        "value": "딸기 맛",
        "unit": "",
    },
}
