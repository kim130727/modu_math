from __future__ import annotations
from modu_math.dsl import (
    Canvas,
    CircleSlot,
    LineSlot,
    ProblemTemplate,
    Region,
    TextSlot,
)


def build_problem_template() -> ProblemTemplate:
    return ProblemTemplate(
        id="S3_초등_3_008637",
        title="원의 중심 찾기",
        canvas=Canvas(width=600, height=360, coordinate_mode="logical"),
        regions=(
            Region(
                id="region.stem", role="stem", flow="absolute", slot_ids=("slot.q1",)
            ),
            Region(
                id="region.diagram.top",
                role="diagram",
                flow="absolute",
                slot_ids=(
                    "slot.top.grid.v1",
                    "slot.top.grid.v2",
                    "slot.top.grid.v3",
                    "slot.top.grid.v4",
                    "slot.top.grid.v5",
                    "slot.top.grid.v6",
                    "slot.top.grid.v7",
                    "slot.top.grid.v8",
                    "slot.top.grid.v9",
                    "slot.top.grid.h1",
                    "slot.top.grid.h2",
                    "slot.top.grid.h3",
                    "slot.top.grid.h4",
                    "slot.top.grid.h5",
                    "slot.top.grid.h6",
                    "slot.top.grid.h7",
                    "slot.top.grid.h8",
                    "slot.top.circle",
                    "slot.top.pt.giyeok",
                    "slot.top.pt.nieun",
                    "slot.top.pt.digeut",
                    "slot.top.lb.giyeok",
                    "slot.top.lb.nieun",
                    "slot.top.lb.digeut",
                ),
            ),
            Region(
                id="region.diagram.bottom",
                role="diagram",
                flow="absolute",
                slot_ids=(
                    "slot.bottom.grid.h1",
                    
                    
                ),
            ),
            Region(
                id="region.explanation",
                role="explanation",
                flow="absolute",
                slot_ids=(),
            ),
        ),
        slots=(
            TextSlot(
                id="slot.q1",
                prompt="",
                text = '원의 중심을 찾아 선택해 보세요.', style_role="question",
                x=10.0,
                y=32.0,
                font_size=28,
            ),
            LineSlot(
                id="slot.top.grid.v1",
                prompt="",
                x1 = 235, y1 = 95, x2 = 235, y2 = 310, stroke="#9AA0A6",
                stroke_width=1.2,
                stroke_dasharray="5 3",
            ),
            LineSlot(
                id="slot.top.grid.v2",
                prompt="",
                x1 = 265, y1 = 95, x2 = 265, y2 = 310, stroke="#9AA0A6",
                stroke_width=1.2,
                stroke_dasharray="5 3",
            ),
            LineSlot(
                id="slot.top.grid.v3",
                prompt="",
                x1 = 290, y1 = 95, x2 = 290, y2 = 310, stroke="#9AA0A6",
                stroke_width=1.2,
                stroke_dasharray="5 3",
            ),
            LineSlot(
                id="slot.top.grid.v4",
                prompt="",
                x1 = 315, y1 = 95, x2 = 315, y2 = 310, stroke="#9AA0A6",
                stroke_width=1.2,
                stroke_dasharray="5 3",
            ),
            LineSlot(
                id="slot.top.grid.v5",
                prompt="",
                x1 = 340, y1 = 95, x2 = 340, y2 = 310, stroke="#9AA0A6",
                stroke_width=1.2,
                stroke_dasharray="5 3",
            ),
            LineSlot(
                id="slot.top.grid.v6",
                prompt="",
                x1 = 365, y1 = 95, x2 = 365, y2 = 310, stroke="#9AA0A6",
                stroke_width=1.2,
                stroke_dasharray="5 3",
            ),
            LineSlot(
                id="slot.top.grid.v7",
                prompt="",
                x1 = 395, y1 = 95, x2 = 395, y2 = 310, stroke="#9AA0A6",
                stroke_width=1.2,
                stroke_dasharray="5 3",
            ),
            LineSlot(
                id="slot.top.grid.v8",
                prompt="",
                x1 = 420, y1 = 95, x2 = 420, y2 = 310, stroke="#9AA0A6",
                stroke_width=1.2,
                stroke_dasharray="5 3",
            ),
            LineSlot(
                id="slot.top.grid.v9",
                prompt="",
                x1 = 445, y1 = 95, x2 = 445, y2 = 310, stroke="#9AA0A6",
                stroke_width=1.2,
                stroke_dasharray="5 3",
            ),
            LineSlot(
                id="slot.top.grid.h1",
                prompt="",
                x1 = 235, y1 = 95, x2 = 445, y2 = 95, stroke="#9AA0A6",
                stroke_width=1.2,
                stroke_dasharray="5 3",
            ),
            LineSlot(
                id="slot.top.grid.h2",
                prompt="",
                x1 = 235, y1 = 120, x2 = 445, y2 = 120, stroke="#9AA0A6",
                stroke_width=1.2,
                stroke_dasharray="5 3",
            ),
            LineSlot(
                id="slot.top.grid.h3",
                prompt="",
                x1 = 235, y1 = 150, x2 = 445, y2 = 150, stroke="#9AA0A6",
                stroke_width=1.2,
                stroke_dasharray="5 3",
            ),
            LineSlot(
                id="slot.top.grid.h4",
                prompt="",
                x1 = 235, y1 = 175, x2 = 445, y2 = 175, stroke="#9AA0A6",
                stroke_width=1.2,
                stroke_dasharray="5 3",
            ),
            LineSlot(
                id="slot.top.grid.h5",
                prompt="",
                x1 = 235, y1 = 200, x2 = 445, y2 = 200, stroke="#9AA0A6",
                stroke_width=1.2,
                stroke_dasharray="5 3",
            ),
            LineSlot(
                id="slot.top.grid.h6",
                prompt="",
                x1 = 235, y1 = 225, x2 = 445, y2 = 225, stroke="#9AA0A6",
                stroke_width=1.2,
                stroke_dasharray="5 3",
            ),
            LineSlot(
                id="slot.top.grid.h7",
                prompt="",
                x1 = 235, y1 = 250, x2 = 445, y2 = 250, stroke="#9AA0A6",
                stroke_width=1.2,
                stroke_dasharray="5 3",
            ),
            LineSlot(
                id="slot.top.grid.h8",
                prompt="",
                x1 = 235, y1 = 280, x2 = 445, y2 = 280, stroke="#9AA0A6",
                stroke_width=1.2,
                stroke_dasharray="5 3",
            ),
            CircleSlot(
                id="slot.top.circle", prompt="", cx = 342, cy = 201, r = 50, fill="none"
            ),
            CircleSlot(
                id="slot.top.pt.giyeok",
                prompt="",
                cx = 290, cy = 200, r = 5, fill="#ff4da6",
            ),
            CircleSlot(
                id="slot.top.pt.nieun",
                prompt="",
                cx = 340, cy = 200, r = 5, fill="#ff4da6",
            ),
            CircleSlot(
                id="slot.top.pt.digeut",
                prompt="",
                cx = 395, cy = 200, r = 5, fill="#ff4da6",
            ),
            TextSlot(
                id="slot.top.lb.giyeok",
                prompt="",
                text = 'ㄱ', style_role="label",
                x = 265, y = 195, font_size = 30),
            TextSlot(
                id="slot.top.lb.nieun",
                prompt="",
                text = 'ㄴ', style_role="label",
                x = 330, y = 195, font_size = 30),
            TextSlot(
                id="slot.top.lb.digeut",
                prompt="",
                text = 'ㄷ', style_role="label",
                x = 405, y = 195, font_size = 30),
            LineSlot(
                id="slot.bottom.grid.h1",
                prompt="",
                x1 = 235, y1 = 305, x2 = 445, y2 = 305, stroke="#9AA0A6",
                stroke_width=1.2,
                stroke_dasharray="5 3",
            ),
            
        ),
        diagrams=(),
        groups=(),
        constraints=(),
        tags=(),
    )


PROBLEM_TEMPLATE = build_problem_template()

SEMANTIC_OVERRIDE = {
    "problem_id": "S3_초등_3_008637",
    "problem_type": "concept_choice",
    "metadata": {
        "language": "ko",
        "question": "원의 중심을 찾아 선택하는 문제",
        "instruction": "그림에서 원의 중심에 해당하는 점을 고른다.",
    },
    "domain": {
        "objects": [
            {"id": "obj.circle", "type": "circle"},
            {
                "id": "obj.point_left",
                "type": "point",
                "label": "ㄱ",
                "role": "candidate",
            },
            {
                "id": "obj.point_center",
                "type": "point",
                "label": "ㄴ",
                "role": "center_candidate",
            },
            {
                "id": "obj.point_right",
                "type": "point",
                "label": "ㄷ",
                "role": "candidate",
            },
        ],
        "relations": [],
        "problem_solving": {
            "understand": {
                "given_refs": [
                    "obj.circle",
                    "obj.point_left",
                    "obj.point_center",
                    "obj.point_right",
                ],
                "target_ref": "answer.target",
                "condition_refs": ["rel.center_of_circle"],
            },
            "plan": {
                "method": "center_identification",
                "description": "원의 중심에 놓인 점을 찾는다.",
            },
            "execute": {
                "expected_operations": [
                    "compare_point_positions",
                    "select_center_candidate",
                ]
            },
            "review": {
                "check_methods": [
                    "center_is_single_point",
                    "matches_visible_answer_label",
                ]
            },
        },
    },
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {
            "type": "selected_label",
            "description": "원의 중심으로 선택한 점의 자모",
        },
        "value": 2,
        "unit": "",
    },
}

SOLVABLE = {
    "schema": "modu.solvable.v1.1",
    "problem_id": "S3_초등_3_008637",
    "problem_type": "concept_choice",
    "inputs": {
        "total_ticks": 1,
        "target_label": "ㄴ",
        "target_ticks": 1,
        "target_count": 1,
        "unit": "",
    },
    "given": [
        {"ref": "obj.circle", "value": "circle"},
        {"ref": "obj.point_left", "value": {"label": "ㄱ"}},
        {"ref": "obj.point_center", "value": {"label": "ㄴ"}},
        {"ref": "obj.point_right", "value": {"label": "ㄷ"}},
    ],
    "target": {"ref": "answer.target", "type": "selected_label"},
    "method": "center_identification",
    "plan": ["원의 중심에 해당하는 점을 찾는다.", "그 점의 자모 라벨을 선택한다."],
    "steps": [
        {
            "id": "step.1",
            "expr": "가운데 점이 원의 중심 후보인지 확인한다.",
            "value": "ㄴ",
        },
        {
            "id": "step.2",
            "expr": "정답 표기와 일치하는 라벨을 선택한다.",
            "value": "ㄴ",
        },
    ],
    "checks": [
        {
            "id": "check.1",
            "expr": "선택한 라벨이 원의 중심에 해당하는가",
            "expected": "ㄴ",
            "actual": "ㄴ",
            "pass": True,
        }
    ],
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {
            "type": "selected_label",
            "description": "원의 중심으로 선택한 점의 자모",
        },
        "value": 2,
        "unit": "",
    },
}
