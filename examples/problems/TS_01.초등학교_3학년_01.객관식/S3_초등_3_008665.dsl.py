from __future__ import annotations
from modu_math.dsl import (
    Canvas,
    ProblemTemplate,
    Region,
    RectSlot,
    TextSlot,
    CircleSlot,
    LineSlot,
)


def build_problem_template() -> ProblemTemplate:
    return ProblemTemplate(
        id="S3_초등_3_008665",
        title="원의 지름",
        canvas=Canvas(width=960, height=420, coordinate_mode="logical"),
        regions=(
            Region(
                id="region.stem",
                role="stem",
                flow="absolute",
                slot_ids=("slot.box", "slot.qnum", "slot.question"),
            ),
            Region(
                id="region.diagram",
                role="diagram",
                flow="absolute",
                slot_ids=(
                    "slot.circle",
                    "slot.center_mark",
                    "slot.center_dot",
                    "slot.line.1",
                    "slot.line.2",
                    "slot.line.3",
                    "slot.line.4",
                    "slot.line.5",
                    "slot.line.6",
                    "slot.lb.ga",
                    "slot.lb.na",
                    "slot.lb.da",
                    "slot.lb.ra",
                    "slot.lb.ma",
                ),
            ),
            Region(id="region.answer", role="answer", flow="absolute", slot_ids=()),
        ),
        slots=(
            RectSlot(id="slot.box", prompt="", x=10.0, y=15.0, width=16.0, height=16.0),
            TextSlot(
                id="slot.qnum",
                prompt="",
                text="40.",
                style_role="question",
                x=35.0,
                y=31.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.question",
                prompt="",
                text="원의 지름이 아닌 것을 모두 찾아 선택해 보세요.",
                style_role="question",
                x=80.0,
                y=31.0,
                font_size=28,
            ),
            CircleSlot(
                id="slot.circle", prompt="", cx=520.0, cy=150.0, r=85.0, fill="none"
            ),
            CircleSlot(
                id="slot.center_dot",
                prompt="",
                cx=482.0,
                cy=150.0,
                r=3.5,
                fill="#ff3b8d",
            ),
            TextSlot(
                id="slot.center_mark",
                prompt="",
                text="ㅇ",
                style_role="label",
                x=466.0,
                y=168.0,
                font_size=22,
            ),
            LineSlot(
                id="slot.line.1", prompt="", x1=520.0, y1=65.0, x2=586.0, y2=240.0
            ),
            LineSlot(
                id="slot.line.2", prompt="", x1=600.0, y1=88.0, x2=431.0, y2=229.0
            ),
            LineSlot(
                id="slot.line.3", prompt="", x1=443.0, y1=82.0, x2=585.0, y2=193.0
            ),
            LineSlot(
                id="slot.line.4", prompt="", x1=486.0, y1=235.0, x2=598.0, y2=83.0
            ),
            LineSlot(
                id="slot.line.5", prompt="", x1=457.0, y1=105.0, x2=607.0, y2=160.0
            ),
            LineSlot(
                id="slot.line.6", prompt="", x1=434.0, y1=150.0, x2=607.0, y2=150.0
            ),
            TextSlot(
                id="slot.lb.ga",
                prompt="",
                text="ㄱ",
                style_role="label",
                x=397.0,
                y=88.0,
                font_size=22,
            ),
            TextSlot(
                id="slot.lb.na",
                prompt="",
                text="ㄴ",
                style_role="label",
                x=391.0,
                y=156.0,
                font_size=22,
            ),
            TextSlot(
                id="slot.lb.da",
                prompt="",
                text="ㄷ",
                style_role="label",
                x=401.0,
                y=237.0,
                font_size=22,
            ),
            TextSlot(
                id="slot.lb.ra",
                prompt="",
                text="ㄹ",
                style_role="label",
                x=502.0,
                y=263.0,
                font_size=22,
            ),
            TextSlot(
                id="slot.lb.ma",
                prompt="",
                text="ㅁ",
                style_role="label",
                x=617.0,
                y=195.0,
                font_size=22,
            ),
        ),
        diagrams=(),
        groups=(),
        constraints=(),
        tags=(),
    )


PROBLEM_TEMPLATE = build_problem_template()

SEMANTIC_OVERRIDE = {
    "problem_id": "S3_초등_3_008665",
    "problem_type": "geometry_circle_diameter_selection",
    "metadata": {
        "language": "ko",
        "question": "원의 지름이 아닌 것을 모두 찾아 선택해 보세요.",
        "instruction": "원의 지름이 아닌 것을 모두 찾아 선택해 보세요.",
    },
    "domain": {
        "objects": [
            {"id": "obj.circle", "type": "circle"},
            {"id": "obj.center", "type": "center"},
            {
                "id": "obj.labels",
                "type": "point_labels",
                "labels": ["ㄱ", "ㄴ", "ㄷ", "ㄹ", "ㅁ"],
            },
        ],
        "relations": [],
        "problem_solving": {
            "understand": {
                "given_refs": ["obj.circle", "obj.center", "obj.labels"],
                "target_ref": "answer.target",
                "condition_refs": ["rel.diameter_test"],
            },
            "plan": {
                "method": "diameter_classification",
                "description": "각 선분이 원의 중심을 지나는지 확인하여 지름인지 아닌지 분류한다.",
            },
            "execute": {
                "expected_operations": [
                    "identify_center_passing_segments",
                    "compare_segments_with_diameter_definition",
                ]
            },
            "review": {"check_methods": ["definition_consistency_check"]},
        },
    },
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {
            "type": "non_diameter_selection",
            "description": "원의 지름이 아닌 것 모두",
        },
        "value": 2,
        "unit": "",
    },
}

SOLVABLE = {
    "schema": "modu.solvable.v1.1",
    "problem_id": "S3_초등_3_008665",
    "problem_type": "geometry_circle_diameter_selection",
    "inputs": {
        "total_ticks": 1,
        "target_label": "원의 지름이 아닌 것",
        "target_ticks": 2,
        "target_count": 2,
        "unit": "",
    },
    "given": [
        {"ref": "obj.circle", "value": "circle"},
        {"ref": "obj.center", "value": "center"},
        {"ref": "obj.labels", "value": ["ㄱ", "ㄴ", "ㄷ", "ㄹ", "ㅁ"]},
    ],
    "target": {"ref": "answer.target", "type": "non_diameter_selection"},
    "method": "diameter_classification",
    "plan": [
        "각 표시가 가리키는 선분이 원의 중심을 지나는지 확인한다.",
        "중심을 지나지 않으면 지름이 아니다.",
    ],
    "steps": [
        {
            "id": "step.1",
            "expr": "표시된 선분들을 원의 중심 통과 여부로 분류",
            "value": "classification",
        },
        {"id": "step.2", "expr": "지름이 아닌 표시 선택", "value": ["ㄹ", "ㅁ"]},
    ],
    "checks": [
        {
            "id": "check.1",
            "expr": "선택 개수 확인",
            "expected": 2,
            "actual": 2,
            "pass": True,
        },
        {
            "id": "check.2",
            "expr": "선택된 항목이 지름이 아님",
            "expected": True,
            "actual": True,
            "pass": True,
        },
    ],
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {
            "type": "non_diameter_selection",
            "description": "원의 지름이 아닌 것 모두",
        },
        "value": 2,
        "unit": "",
    },
}
