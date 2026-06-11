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
                slot_ids=("slot.header.text",),
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
                    "slot.line.d3",
                    "slot.line.d4",
                    "slot.lb.ㄴ",
                    "slot.lb.ㄷ",
                    "slot.lb.ㄹ",
                    "slot.lb.ㅁ",
                    "slot.lb.ㄱ",
                ),
            ),
            Region(id="region.footer", role="answer", flow="absolute", slot_ids=()),
        ),
        slots=(
            TextSlot(
                id="slot.header.text",
                prompt="",
                text = '\n    \n    원의 지름이 아닌 것을 찾아 기호를 모두\n    선택하세요.  \n  ', style_role="question",
                x = 50, y = 15, font_size = 30),
            CircleSlot(
                id="slot.circle.outer",
                prompt="",
                cx = 315, cy = 245, r = 115, fill="none",
            ),
            CircleSlot(
                id="slot.circle.center",
                prompt="",
                cx = 315, cy = 245, r = 5, fill="#d81b60",
            ),
            LineSlot(
                id="slot.line.v", prompt="", x1 = 315, y1 = 130, x2 = 315, y2 = 360, stroke = '#111111', stroke_width = 2),
            LineSlot(
                id="slot.line.h", prompt="", x1 = 200, y1 = 245, x2 = 430, y2 = 245),
            LineSlot(
                id="slot.line.d1", prompt="", x1 = 225, y1 = 175, x2 = 405, y2 = 315),
            LineSlot(
                id="slot.line.d3", prompt="", x1 = 355, y1 = 355, x2 = 410, y2 = 180),
            LineSlot(
                id="slot.line.d4", prompt="", x1 = 220, y1 = 310, x2 = 370, y2 = 145),
            TextSlot(
                id="slot.lb.ㄴ",
                prompt="",
                text = '㉡', style_role="label",
                x = 190, y = 165, font_size = 30, max_width = 590),
            TextSlot(
                id="slot.lb.ㄷ",
                prompt="",
                text = '㉢', style_role="label",
                x = 300, y = 110, font_size = 30),
            TextSlot(
                id="slot.lb.ㄹ",
                prompt="",
                text = '㉣', style_role="label",
                x = 380, y = 130, font_size = 30, max_width = 590),
            TextSlot(
                id="slot.lb.ㅁ",
                prompt="",
                text = '㉤', style_role="label",
                x = 420, y = 160, font_size = 30, max_width = 590),
            TextSlot(
                id="slot.lb.ㄱ",
                prompt="",
                text = '㉠', style_role="label",
                x = 150, y = 260, font_size = 30, max_width = 590),
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
        "value": "㉣, ㉤",
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
        "value": "㉣, ㉤",
        "unit": "",
    },
}
