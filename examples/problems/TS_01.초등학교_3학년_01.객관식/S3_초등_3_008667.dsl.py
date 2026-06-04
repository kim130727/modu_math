from __future__ import annotations
from modu_math.dsl import Canvas, ProblemTemplate, Region, TextSlot, CircleSlot


def build_problem_template() -> ProblemTemplate:
    return ProblemTemplate(
        id="S3_초등_3_008667",
        title="원의 중심 찾기",
        canvas=Canvas(width=700, height=300, coordinate_mode="logical"),
        regions=(
            Region(
                id="region.stem",
                role="stem",
                flow="absolute",
                slot_ids=(
                    "slot.q1",
                    "slot.diagram.circle",
                    "slot.diagram.pt.g",
                    "slot.diagram.pt.n",
                    "slot.diagram.pt.d",
                    "slot.diagram.pt.r",
                    "slot.diagram.lb.g",
                    "slot.diagram.lb.n",
                    "slot.diagram.lb.d",
                    "slot.diagram.lb.r",
                ),
            ),
        ),
        slots=(
            TextSlot(
                id="slot.q1",
                prompt="",
                text="□ 44. 그림에서 원의 중심을 찾아 선택해 보세요.",
                style_role="question",
                x=18.0,
                y=32.0,
                font_size=28,
            ),
            CircleSlot(
                id="slot.diagram.circle",
                prompt="",
                cx=514.0,
                cy=107.0,
                r=72.0,
                fill="none",
            ),
            CircleSlot(
                id="slot.diagram.pt.g",
                prompt="",
                cx=478.0,
                cy=57.0,
                r=3.8,
                fill="#ff2a9a",
            ),
            CircleSlot(
                id="slot.diagram.pt.n",
                prompt="",
                cx=519.0,
                cy=100.0,
                r=3.8,
                fill="#ff2a9a",
            ),
            CircleSlot(
                id="slot.diagram.pt.d",
                prompt="",
                cx=492.0,
                cy=153.0,
                r=3.8,
                fill="#ff2a9a",
            ),
            CircleSlot(
                id="slot.diagram.pt.r",
                prompt="",
                cx=527.0,
                cy=153.0,
                r=3.8,
                fill="#ff2a9a",
            ),
            TextSlot(
                id="slot.diagram.lb.g",
                prompt="",
                text="ㄱ",
                style_role="label",
                x=461.0,
                y=64.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.diagram.lb.n",
                prompt="",
                text="ㄴ",
                style_role="label",
                x=498.0,
                y=104.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.diagram.lb.d",
                prompt="",
                text="ㄷ",
                style_role="label",
                x=486.0,
                y=169.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.diagram.lb.r",
                prompt="",
                text="ㄹ",
                style_role="label",
                x=521.0,
                y=169.0,
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
    "problem_id": "S3_초등_3_008667",
    "problem_type": "geometry_point_selection",
    "metadata": {
        "language": "ko",
        "question": "그림에서 원의 중심을 찾아 선택해 보세요.",
        "instruction": "그림에서 원의 중심을 찾아 선택하기",
    },
    "domain": {
        "objects": [
            {"id": "obj.circle", "type": "circle"},
            {"id": "obj.point_g", "type": "point", "label": "ㄱ", "role": "candidate"},
            {
                "id": "obj.point_n",
                "type": "point",
                "label": "ㄴ",
                "role": "candidate_center",
            },
            {"id": "obj.point_d", "type": "point", "label": "ㄷ", "role": "candidate"},
            {"id": "obj.point_r", "type": "point", "label": "ㄹ", "role": "candidate"},
        ],
        "relations": [],
        "problem_solving": {
            "understand": {
                "given_refs": [
                    "obj.circle",
                    "obj.point_g",
                    "obj.point_n",
                    "obj.point_d",
                    "obj.point_r",
                ],
                "target_ref": "answer.target",
                "condition_refs": ["rel.center_of"],
            },
            "plan": {
                "method": "center_identification",
                "description": "원 안의 후보 점들 중 원의 중심에 해당하는 점을 찾는다.",
            },
            "execute": {
                "expected_operations": [
                    "compare_candidate_positions",
                    "identify_central_point",
                ]
            },
            "review": {"check_methods": ["center_position_check"]},
        },
    },
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {"type": "selected_label", "description": "원의 중심으로 선택할 점"},
        "value": "ㄴ",
        "unit": "",
    },
}

SOLVABLE = {
    "schema": "modu.solvable.v1.1",
    "problem_id": "S3_초등_3_008667",
    "problem_type": "geometry_point_selection",
    "inputs": {
        "total_ticks": 0,
        "target_label": "ㄴ",
        "target_ticks": 0,
        "target_count": 1,
        "unit": "",
    },
    "given": [
        {"ref": "obj.circle", "value": {"type": "circle"}},
        {"ref": "obj.point_g", "value": {"label": "ㄱ", "role": "candidate"}},
        {"ref": "obj.point_n", "value": {"label": "ㄴ", "role": "candidate_center"}},
        {"ref": "obj.point_d", "value": {"label": "ㄷ", "role": "candidate"}},
        {"ref": "obj.point_r", "value": {"label": "ㄹ", "role": "candidate"}},
    ],
    "target": {"ref": "answer.target", "type": "selected_label"},
    "method": "center_identification",
    "plan": ["원 안의 후보 점들 중 중심에 해당하는 점을 찾는다."],
    "steps": [
        {
            "id": "step.1",
            "expr": "원에서 가장 안쪽에 있는 후보 점을 확인한다.",
            "value": "ㄴ",
        }
    ],
    "checks": [
        {
            "id": "check.1",
            "expr": "선택한 점이 원의 중심인가?",
            "expected": "ㄴ",
            "actual": "ㄴ",
            "pass": True,
        }
    ],
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {"type": "selected_label", "description": "원의 중심으로 선택할 점"},
        "value": "ㄴ",
        "unit": "",
    },
}
