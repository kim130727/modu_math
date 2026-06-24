from __future__ import annotations
from modu_math.dsl import Canvas, ProblemTemplate, Region, RectSlot, TextSlot


def build_problem_template() -> ProblemTemplate:
    return ProblemTemplate(
        id="S3_초등_3_008944",
        title="그림그래프와 비교",
        canvas=Canvas(width=944.0, height=570.0, coordinate_mode="logical"),
        regions=(
            Region(
                id="region.stem",
                role="stem",
                flow="absolute",
                slot_ids=(
                    "slot.q1",
                    "slot.title",
                    "slot.table.outer",
                    "slot.table.v1",
                    "slot.table.v2",
                    "slot.table.v3",
                    "slot.table.h1",
                    "slot.lb.kimchi",
                    "slot.lb.doenjang",
                    "slot.lb.bibim",
                    "slot.lb.naeng",
                    "slot.legend.big",
                    "slot.legend.small",
                    "slot.legend.big.label",
                    "slot.legend.small.label",
                    "slot.choice",
                ),
            ),
        ),
        slots=(
            TextSlot(
                id="slot.q1",
                prompt="",
                text="12. 어느 음식점에서 일주일 동안 팔린 음식의 수를 조사하여 그림그래프로 나타내었습니다. 된장찌개보다 더 많이 팔린 음식을 모두 선택해 보세요.",
                style_role="question",
                x=12.0,
                y=18.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.title",
                prompt="",
                text="일주일 동안 팔린 음식",
                style_role="title",
                x=372.0,
                y=74.0,
                font_size=28,
            ),
            RectSlot(
                id="slot.table.outer",
                prompt="",
                x=257.0,
                y=91.0,
                width=455.0,
                height=268.0,
                fill="none",
            ),
            RectSlot(
                id="slot.table.v1", prompt="", x=370.0, y=91.0, width=0.0, height=268.0, fill="none"
            ),
            RectSlot(
                id="slot.table.v2", prompt="", x=484.0, y=91.0, width=0.0, height=268.0, fill="none"
            ),
            RectSlot(
                id="slot.table.v3", prompt="", x=598.0, y=91.0, width=0.0, height=268.0, fill="none"
            ),
            RectSlot(
                id="slot.table.h1",
                prompt="",
                x=257.0,
                y=283.0,
                width=455.0,
                height=0.0,
                fill="none",
            ),
            TextSlot(
                id="slot.lb.kimchi",
                prompt="",
                text="김치찌개",
                style_role="label",
                x=280.0,
                y=338.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.lb.doenjang",
                prompt="",
                text="된장찌개",
                style_role="label",
                x=395.0,
                y=338.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.lb.bibim",
                prompt="",
                text="비빔\n밥",
                style_role="label",
                x=518.0,
                y=320.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.lb.naeng",
                prompt="",
                text="냉면",
                style_role="label",
                x=630.0,
                y=338.0,
                font_size=28,
            ),
            RectSlot(
                id="slot.legend.big",
                prompt="",
                x=396.0,
                y=382.0,
                width=40.0,
                height=30.0,
                fill="none",
            ),
            RectSlot(
                id="slot.legend.small",
                prompt="",
                x=587.0,
                y=386.0,
                width=30.0,
                height=20.0,
                fill="none",
            ),
            TextSlot(
                id="slot.legend.big.label",
                prompt="",
                text="100그릇",
                style_role="label",
                x=440.0,
                y=406.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.legend.small.label",
                prompt="",
                text="10그릇",
                style_role="label",
                x=628.0,
                y=406.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.choice",
                prompt="",
                text="( 김치찌개 , 비빔밥 , 냉면 )",
                style_role="body",
                x=588.0,
                y=452.0,
                font_size=28,
            ),
        ),
        diagrams=(),
        groups=(),
        constraints=(),
        tags=("그림그래프", "비교", "초등수학"),
    )


PROBLEM_TEMPLATE = build_problem_template()

SEMANTIC_OVERRIDE = {
    "problem_id": "S3_초등_3_008944",
    "problem_type": "picture_graph_comparison",
    "metadata": {
        "language": "ko",
        "question": "된장찌개보다 더 많이 팔린 음식을 모두 선택하는 문제",
        "instruction": "그림그래프를 보고 된장찌개보다 더 많이 팔린 음식을 고르기",
    },
    "domain": {
        "objects": [
            {"id": "obj.kimchi", "type": "food", "name": "김치찌개"},
            {"id": "obj.doenjang", "type": "food", "name": "된장찌개"},
            {"id": "obj.bibim", "type": "food", "name": "비빔밥"},
            {"id": "obj.naeng", "type": "food", "name": "냉면"},
            {"id": "obj.legend.big", "type": "legend_unit", "name": "100그릇"},
            {"id": "obj.legend.small", "type": "legend_unit", "name": "10그릇"},
        ],
        "relations": [],
    },
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {"type": "selected_food_names", "description": "된장찌개보다 더 많이 팔린 음식"},
        "value": ["김치찌개", "냉면"],
        "unit": "",
    },
}

SOLVABLE = {
    "schema": "modu.solvable.v1.1",
    "problem_id": "S3_초등_3_008944",
    "problem_type": "picture_graph_comparison",
    "inputs": {
        "total_ticks": 0,
        "target_label": "된장찌개보다 더 많이 팔린 음식",
        "target_ticks": 0,
        "target_count": 2,
        "unit": "",
    },
    "given": [
        {"ref": "obj.kimchi", "value": {"name": "김치찌개"}},
        {"ref": "obj.doenjang", "value": {"name": "된장찌개"}},
        {"ref": "obj.bibim", "value": {"name": "비빔밥"}},
        {"ref": "obj.naeng", "value": {"name": "냉면"}},
    ],
    "target": {"ref": "answer.target", "type": "selected_food_names"},
    "method": "compare_picture_counts",
    "plan": [
        "그림그래프에서 된장찌개의 그림 수를 기준으로 다른 음식들을 비교한다.",
        "된장찌개보다 그림 수가 더 많은 음식 이름을 고른다.",
    ],
    "steps": [
        {
            "id": "step.1",
            "expr": "그림그래프에서 된장찌개와 다른 음식의 그림 수를 비교한다",
            "value": "비교",
        },
        {
            "id": "step.2",
            "expr": "된장찌개보다 더 많은 음식은 김치찌개와 냉면이다",
            "value": ["김치찌개", "냉면"],
        },
    ],
    "checks": [
        {
            "id": "check.1",
            "expr": "선택한 음식이 된장찌개보다 더 많은지 확인",
            "expected": ["김치찌개", "냉면"],
            "actual": ["김치찌개", "냉면"],
            "pass": True,
        }
    ],
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {"type": "selected_food_names", "description": "된장찌개보다 더 많이 팔린 음식"},
        "value": ["김치찌개", "냉면"],
        "unit": "",
    },
}
