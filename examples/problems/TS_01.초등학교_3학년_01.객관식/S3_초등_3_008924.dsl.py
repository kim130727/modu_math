from __future__ import annotations
from modu_math.dsl import Canvas, ProblemTemplate, Region, TextSlot, RectSlot, CircleSlot


def build_problem_template() -> ProblemTemplate:
    return ProblemTemplate(
        id="S3_초등_3_008924",
        title="모둠별 찬장 도장 수",
        canvas=Canvas(width=960, height=540, coordinate_mode="logical"),
        regions=(
            Region(
                id="region.stem",
                role="stem",
                flow="absolute",
                slot_ids=(
                    "slot.q.no",
                    "slot.q.s1",
                    "slot.q.s2",
                    "slot.title",
                    "slot.table.h1",
                    "slot.table.h2",
                    "slot.table.row1",
                    "slot.table.row2",
                    "slot.group.a",
                    "slot.group.b",
                    "slot.group.c",
                    "slot.legend.big_label",
                    "slot.legend.small_label",
                    "slot.choice",
                ),
            ),
        ),
        slots=(
            TextSlot(
                id="slot.q.no",
                prompt="",
                text="90.",
                style_role="question",
                x=18.0,
                y=28.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.q.s1",
                prompt="",
                text="대성이네 반의 모둠별 찬장 도장 수를 조사하여 그림그래프로 나타내었습니다.",
                style_role="question",
                x=64.0,
                y=28.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.q.s2",
                prompt="",
                text="가장 많은 찬장 도장을 받은 모둠을 선택하세요.",
                style_role="question",
                x=64.0,
                y=64.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.title",
                prompt="",
                text="모둠별 찬장 도장 수",
                style_role="title",
                x=382.0,
                y=118.0,
                font_size=28,
            ),
            RectSlot(
                id="slot.table.h1",
                prompt="",
                x=200.0,
                y=150.0,
                width=86.0,
                height=192.0,
                fill="#F7F1E8",
                stroke="#D8B08C",
                stroke_width=1.2,
            ),
            RectSlot(
                id="slot.table.h2",
                prompt="",
                x=286.0,
                y=150.0,
                width=470.0,
                height=192.0,
                fill="#FFFFFF",
                stroke="#D8B08C",
                stroke_width=1.2,
            ),
            TextSlot(
                id="slot.table.row1",
                prompt="",
                text="모둠",
                style_role="label",
                x=225.0,
                y=176.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.table.row2",
                prompt="",
                text="찬장 도장 수",
                style_role="label",
                x=462.0,
                y=176.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.group.a",
                prompt="",
                text="가",
                style_role="label",
                x=226.0,
                y=222.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.group.b",
                prompt="",
                text="나",
                style_role="label",
                x=226.0,
                y=274.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.group.c",
                prompt="",
                text="다",
                style_role="label",
                x=226.0,
                y=326.0,
                font_size=28,
            ),
            CircleSlot(
                id="slot.legend.big_stamp", prompt="", cx=590.0, cy=332.0, r=24.0, fill="#C93B34"
            ),
            CircleSlot(
                id="slot.legend.small_stamp", prompt="", cx=694.0, cy=332.0, r=15.0, fill="#C93B34"
            ),
            TextSlot(
                id="slot.legend.big_label",
                prompt="",
                text="10개",
                style_role="label",
                x=623.0,
                y=342.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.legend.small_label",
                prompt="",
                text="1개",
                style_role="label",
                x=729.0,
                y=342.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.choice",
                prompt="",
                text="( 가 모둠, 나 모둠, 다 모둠 )",
                style_role="label",
                x=575.0,
                y=392.0,
                font_size=28,
            ),
        ),
        diagrams=(),
        groups=(),
        constraints=(),
        tags=("그림그래프", "비교", "초등3"),
    )


PROBLEM_TEMPLATE = build_problem_template()

SEMANTIC_OVERRIDE = {
    "problem_id": "S3_초등_3_008924",
    "problem_type": "그림그래프에서 가장 많은 모둠 찾기",
    "metadata": {
        "language": "ko",
        "question": "대성이네 반의 모둠별 찬장 도장 수를 조사하여 그림그래프로 나타내었습니다. 가장 많은 찬장 도장을 받은 모둠을 선택하세요.",
        "instruction": "가장 많은 찬장 도장을 받은 모둠을 찾는다.",
    },
    "domain": {
        "objects": [
            {"id": "obj.chart", "type": "picture_graph", "title": "모둠별 찬장 도장 수"},
            {"id": "obj.group.ga", "type": "group", "label": "가"},
            {"id": "obj.group.na", "type": "group", "label": "나"},
            {"id": "obj.group.da", "type": "group", "label": "다"},
            {"id": "obj.legend.big_stamp", "type": "legend_item", "label": "10개"},
            {"id": "obj.legend.small_stamp", "type": "legend_item", "label": "1개"},
        ],
        "relations": [],
        "problem_solving": {
            "understand": {
                "given_refs": ["obj.chart", "obj.legend.big_stamp", "obj.legend.small_stamp"],
                "target_ref": "answer.target",
                "condition_refs": ["rel.compare_counts"],
            },
            "plan": {
                "method": "picture_graph_compare",
                "description": "그림그래프에서 각 모둠의 도장 수를 비교하여 가장 많은 모둠을 찾는다.",
            },
            "execute": {
                "expected_operations": [
                    "read_graph_values",
                    "compare_group_counts",
                    "select_max_group",
                ]
            },
            "review": {"check_methods": ["largest_value_check", "comparison_consistency_check"]},
        },
    },
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {"type": "selected_group", "description": "가장 많은 찬장 도장을 받은 모둠"},
        "value": 0,
        "unit": "",
    },
}

SOLVABLE = {
    "schema": "modu.solvable.v1.1",
    "problem_id": "S3_초등_3_008924",
    "problem_type": "그림그래프에서 가장 많은 모둠 찾기",
    "inputs": {
        "total_ticks": 0,
        "target_label": "가장 많은 찬장 도장을 받은 모둠",
        "target_ticks": 0,
        "target_count": 0,
        "unit": "",
    },
    "given": [
        {"ref": "obj.legend.big_stamp", "value": {"label": "10개"}},
        {"ref": "obj.legend.small_stamp", "value": {"label": "1개"}},
        {"ref": "obj.group.ga", "value": {"label": "가"}},
        {"ref": "obj.group.na", "value": {"label": "나"}},
        {"ref": "obj.group.da", "value": {"label": "다"}},
    ],
    "target": {"ref": "answer.target", "type": "selected_group"},
    "method": "picture_graph_compare",
    "plan": [
        "그림그래프의 범례를 확인한다.",
        "각 모둠의 도장 수를 비교한다.",
        "가장 많은 모둠을 선택한다.",
    ],
    "steps": [
        {"id": "step.1", "expr": "그림그래프에서 모둠별 도장 수를 읽는다.", "value": "TODO"},
        {"id": "step.2", "expr": "모둠별 수를 비교하여 최댓값을 찾는다.", "value": "TODO"},
    ],
    "checks": [
        {
            "id": "check.1",
            "expr": "가장 많은 모둠이 하나인지 확인한다.",
            "expected": "TODO",
            "actual": "TODO",
            "pass": False,
        }
    ],
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {"type": "selected_group", "description": "가장 많은 찬장 도장을 받은 모둠"},
        "value": 0,
        "unit": "",
    },
}
