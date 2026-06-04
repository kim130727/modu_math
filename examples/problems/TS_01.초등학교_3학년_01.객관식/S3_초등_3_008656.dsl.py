from __future__ import annotations
from modu_math.dsl import (
    Canvas,
    CircleSlot,
    LineSlot,
    ProblemTemplate,
    RectSlot,
    Region,
    TextSlot,
)


def build_problem_template() -> ProblemTemplate:
    return ProblemTemplate(
        id="S3_초등_3_008656",
        title="원의 지름이 아닌 것을 찾아 기호를 모두 선택하기",
        canvas=Canvas(width=720, height=400, coordinate_mode="logical"),
        regions=(
            Region(
                id="region.header",
                role="stem",
                flow="absolute",
                slot_ids=("slot.header.box", "slot.header.text"),
            ),
            Region(
                id="region.diagram",
                role="diagram",
                flow="absolute",
                slot_ids=(
                    "slot.circle.outer",
                    "slot.circle.center",
                    "slot.line.v",
                    "slot.line.h",
                    "slot.line.d1",
                    "slot.line.d2",
                    "slot.line.d3",
                    "slot.line.d4",
                    "slot.line.d5",
                    "slot.lb.ㄴ",
                    "slot.lb.ㄷ",
                    "slot.lb.ㄹ",
                    "slot.lb.ㅁ",
                    "slot.lb.ㅂ",
                    "slot.lb.ㅅ",
                    "slot.lb.ㄱ",
                ),
            ),
            Region(id="region.footer", role="answer", flow="absolute", slot_ids=()),
        ),
        slots=(
            RectSlot(
                id="slot.header.box", prompt="", x=6.0, y=14.0, width=12.0, height=12.0
            ),
            TextSlot(
                id="slot.header.text",
                prompt="",
                text="31. 원의 지름이 아닌 것을 찾아 기호를 모두 선택하세요.",
                style_role="question",
                x=22.0,
                y=24.0,
                font_size=28,
            ),
            CircleSlot(
                id="slot.circle.outer",
                prompt="",
                cx=524.0,
                cy=132.0,
                r=88.0,
                fill="none",
            ),
            CircleSlot(
                id="slot.circle.center",
                prompt="",
                cx=524.0,
                cy=132.0,
                r=2.5,
                fill="#d81b60",
            ),
            LineSlot(
                id="slot.line.v", prompt="", x1=524.0, y1=44.0, x2=524.0, y2=220.0
            ),
            LineSlot(
                id="slot.line.h", prompt="", x1=436.0, y1=132.0, x2=612.0, y2=132.0
            ),
            LineSlot(
                id="slot.line.d1", prompt="", x1=448.0, y1=74.0, x2=600.0, y2=170.0
            ),
            LineSlot(
                id="slot.line.d2", prompt="", x1=448.0, y1=186.0, x2=592.0, y2=92.0
            ),
            LineSlot(
                id="slot.line.d3", prompt="", x1=524.0, y1=220.0, x2=592.0, y2=68.0
            ),
            LineSlot(
                id="slot.line.d4", prompt="", x1=476.0, y1=208.0, x2=580.0, y2=52.0
            ),
            LineSlot(
                id="slot.line.d5", prompt="", x1=476.0, y1=208.0, x2=436.0, y2=132.0
            ),
            TextSlot(
                id="slot.lb.ㄴ",
                prompt="",
                text="ㄴ",
                style_role="label",
                x=448.0,
                y=66.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.lb.ㄷ",
                prompt="",
                text="ㄷ",
                style_role="label",
                x=518.0,
                y=30.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.lb.ㄹ",
                prompt="",
                text="ㄹ",
                style_role="label",
                x=586.0,
                y=54.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.lb.ㅁ",
                prompt="",
                text="ㅁ",
                style_role="label",
                x=608.0,
                y=96.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.lb.ㅂ",
                prompt="",
                text="ㅂ",
                style_role="label",
                x=610.0,
                y=186.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.lb.ㅅ",
                prompt="",
                text="ㅅ",
                style_role="label",
                x=432.0,
                y=148.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.lb.ㄱ",
                prompt="",
                text="ㄱ",
                style_role="label",
                x=436.0,
                y=116.0,
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
    "problem_id": "S3_초등_3_008656",
    "problem_type": "geometry_circle_diameter_selection",
    "metadata": {
        "language": "ko",
        "question": "원의 지름이 아닌 것을 찾아 기호를 모두 선택하세요.",
        "instruction": "도형에서 지름이 아닌 기호를 고른다.",
    },
    "domain": {
        "objects": [
            {"id": "obj.circle", "type": "circle"},
            {"id": "obj.center", "type": "point", "role": "center"},
            {
                "id": "obj.labels",
                "type": "label_set",
                "items": ["ㄴ", "ㄷ", "ㄹ", "ㅁ", "ㅂ", "ㅅ", "ㄱ"],
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
                "method": "center_membership_check",
                "description": "각 선이 중심을 지나는지 보고 지름인지 아닌지 구분한다.",
            },
            "execute": {
                "expected_operations": ["center_check", "select_non_diameter_labels"]
            },
            "review": {
                "check_methods": ["verify_center_crossing", "compare_with_answer_text"]
            },
        },
    },
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {"type": "selected_labels", "description": "원의 지름이 아닌 기호"},
        "value": 2,
        "unit": "",
    },
}

SOLVABLE = {
    "schema": "modu.solvable.v1.1",
    "problem_id": "S3_초등_3_008656",
    "problem_type": "geometry_circle_diameter_selection",
    "inputs": {
        "total_ticks": 1,
        "target_label": "원의 지름이 아닌 것",
        "target_ticks": 2,
        "target_count": 2,
        "unit": "",
    },
    "given": [
        {"ref": "obj.labels", "value": ["ㄴ", "ㄷ", "ㄹ", "ㅁ", "ㅂ", "ㅅ", "ㄱ"]}
    ],
    "target": {"ref": "answer.target", "type": "selected_labels"},
    "method": "center_membership_check",
    "plan": [
        "각 기호가 나타내는 선이 원의 중심을 지나는지 확인한다.",
        "중심을 지나지 않는 기호를 지름이 아닌 것으로 고른다.",
    ],
    "steps": [
        {"id": "step.1", "expr": "중심을 지나지 않는 선 확인", "value": ["ㄷ", "ㅁ"]}
    ],
    "checks": [
        {
            "id": "check.1",
            "expr": "선이 중심을 지나는지 여부",
            "expected": ["ㄷ", "ㅁ"],
            "actual": ["ㄷ", "ㅁ"],
            "pass": True,
        }
    ],
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {"type": "selected_labels", "description": "원의 지름이 아닌 기호"},
        "value": 2,
        "unit": "",
    },
}
