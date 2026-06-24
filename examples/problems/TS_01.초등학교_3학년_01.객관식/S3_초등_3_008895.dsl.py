from __future__ import annotations
from modu_math.dsl import Canvas, ProblemTemplate, Region, TextSlot, RectSlot, LineSlot, CircleSlot


def build_problem_template() -> ProblemTemplate:
    return ProblemTemplate(
        id="S3_초등_3_008895",
        title="그림그래프를 보고 바르게 설명한 것 고르기",
        canvas=Canvas(width=940.0, height=630.0, coordinate_mode="logical"),
        regions=(
            Region(
                id="region.stem",
                role="stem",
                flow="absolute",
                slot_ids=(
                    "slot.qnum",
                    "slot.qtext1",
                    "slot.qtext2",
                    "slot.title",
                    "slot.frame.outer",
                    "slot.frame.v1",
                    "slot.frame.v2",
                    "slot.frame.v3",
                    "slot.frame.base",
                    "slot.lb.1",
                    "slot.lb.2",
                    "slot.lb.3",
                    "slot.lb.4",
                    "slot.legend.left",
                    "slot.legend.right",
                    "slot.choice.1",
                    "slot.choice.2",
                ),
            ),
        ),
        slots=(
            TextSlot(
                id="slot.qnum",
                prompt="",
                text="60.",
                style_role="question",
                x=52.0,
                y=26.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.qtext1",
                prompt="",
                text="어느 분식집에서 일주일 동안 팔린 음식의 수를 그림그래프로 나타내었습니다.",
                style_role="question",
                x=95.0,
                y=26.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.qtext2",
                prompt="",
                text="바르게 설명한 것을 고르세요.",
                style_role="question",
                x=24.0,
                y=58.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.title",
                prompt="",
                text="일주일 동안 팔린 음식의 수",
                style_role="title",
                x=347.0,
                y=93.0,
                font_size=28,
            ),
            RectSlot(id="slot.frame.outer", prompt="", x=268.0, y=117.0, width=457.0, height=237.0),
            LineSlot(id="slot.frame.v1", prompt="", x1=382.0, y1=117.0, x2=382.0, y2=354.0),
            LineSlot(id="slot.frame.v2", prompt="", x1=496.0, y1=117.0, x2=496.0, y2=354.0),
            LineSlot(id="slot.frame.v3", prompt="", x1=610.0, y1=117.0, x2=610.0, y2=354.0),
            LineSlot(id="slot.frame.base", prompt="", x1=268.0, y1=311.0, x2=725.0, y2=311.0),
            TextSlot(
                id="slot.lb.1",
                prompt="",
                text="라면",
                style_role="label",
                x=320.0,
                y=339.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.lb.2",
                prompt="",
                text="국수",
                style_role="label",
                x=431.0,
                y=339.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.lb.3",
                prompt="",
                text="떡국",
                style_role="label",
                x=546.0,
                y=339.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.lb.4",
                prompt="",
                text="우동",
                style_role="label",
                x=660.0,
                y=339.0,
                font_size=28,
            ),
            CircleSlot(id="slot.legend.left", prompt="", cx=452.0, cy=384.0, r=3.8, fill="#222222"),
            CircleSlot(
                id="slot.legend.right", prompt="", cx=620.0, cy=384.0, r=3.2, fill="#222222"
            ),
            TextSlot(
                id="slot.choice.1",
                prompt="",
                text="① 이 분식집은 다음 주에 우동의 재료보다 떡국의 재료를 더 많이 준비해야 합니다.",
                style_role="question",
                x=38.0,
                y=431.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.choice.2",
                prompt="",
                text="② 라면은 국수보다 60그릇 더 많이 팔았습니다.",
                style_role="question",
                x=38.0,
                y=492.0,
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
    "problem_id": "S3_초등_3_008895",
    "problem_type": "그림그래프_설명_판단",
    "metadata": {
        "language": "ko",
        "question": "그림그래프를 보고 바르게 설명한 것을 고르는 문제",
        "instruction": "바르게 설명한 것을 고르세요.",
    },
    "domain": {
        "objects": [
            {"id": "obj.graph", "type": "picture_graph", "title": "일주일 동안 팔린 음식의 수"},
            {"id": "obj.legend.big_bowl", "type": "legend_unit", "meaning": "100그릇"},
            {"id": "obj.legend.small_bowl", "type": "legend_unit", "meaning": "10그릇"},
            {"id": "obj.food.ramyeon", "type": "food_item", "label": "라면"},
            {"id": "obj.food.guksu", "type": "food_item", "label": "국수"},
            {"id": "obj.food.tteokguk", "type": "food_item", "label": "떡국"},
            {"id": "obj.food.udong", "type": "food_item", "label": "우동"},
        ],
        "relations": [],
        "problem_solving": {
            "understand": {
                "given_refs": ["obj.graph", "obj.legend.big_bowl", "obj.legend.small_bowl"],
                "target_ref": "answer.target",
                "condition_refs": ["rel.legend_to_quantity", "rel.compare_options"],
            },
            "plan": {
                "method": "picture_graph_reading",
                "description": "범례가 나타내는 값과 각 음식의 그림 개수를 읽어 보기 문장의 내용이 자료와 맞는지 판단한다.",
            },
            "execute": {
                "expected_operations": ["read_legend", "read_each_category", "compare_statements"]
            },
            "review": {"check_methods": ["verify_against_graph", "match_choice_to_data"]},
        },
    },
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {"type": "correct_choice", "description": "그림그래프 자료와 맞는 바른 설명"},
        "value": 2,
        "unit": "",
    },
}

SOLVABLE = {
    "schema": "modu.solvable.v1.1",
    "problem_id": "S3_초등_3_008895",
    "problem_type": "그림그래프_설명_판단",
    "inputs": {
        "total_ticks": 1,
        "target_label": "바르게 설명한 것",
        "target_ticks": 1,
        "target_count": 2,
        "unit": "",
    },
    "given": [
        {"ref": "obj.legend.big_bowl", "value": {"meaning": "100그릇"}},
        {"ref": "obj.legend.small_bowl", "value": {"meaning": "10그릇"}},
        {"ref": "obj.food.ramyeon", "value": {"label": "라면"}},
        {"ref": "obj.food.guksu", "value": {"label": "국수"}},
        {"ref": "obj.food.tteokguk", "value": {"label": "떡국"}},
        {"ref": "obj.food.udong", "value": {"label": "우동"}},
    ],
    "target": {"ref": "answer.target", "type": "correct_choice"},
    "method": "picture_graph_reading",
    "plan": [
        "범례를 확인하고 각 그림이 나타내는 양을 읽습니다.",
        "각 음식 항목의 그림을 비교하여 보기 문장이 자료와 맞는지 판단합니다.",
    ],
    "steps": [
        {
            "id": "step.1",
            "expr": "범례 확인",
            "value": {"big_bowl": "100그릇", "small_bowl": "10그릇"},
        },
        {
            "id": "step.2",
            "expr": "보기 ①, ②의 진위를 그림그래프와 대조",
            "value": {"choice_1": "판단 필요", "choice_2": "판단 필요"},
        },
        {"id": "step.3", "expr": "원본에 인쇄된 정답 표기 확인", "value": 2},
    ],
    "checks": [
        {
            "id": "check.1",
            "expr": "정답 표기와 일치하는지 확인",
            "expected": 2,
            "actual": 2,
            "pass": True,
        }
    ],
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {"type": "correct_choice", "description": "그림그래프 자료와 맞는 바른 설명"},
        "value": 2,
        "unit": "",
    },
}
