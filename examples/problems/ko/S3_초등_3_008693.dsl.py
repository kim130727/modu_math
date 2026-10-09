from __future__ import annotations
from modu_math.dsl import (
    Canvas,
    ProblemTemplate,
    Region,
    TextSlot,
    RectSlot,
    CircleSlot,
    LineSlot,
    PathSlot,
)


def build_problem_template() -> ProblemTemplate:
    return ProblemTemplate(
        id="S3_초등_3_008693",
        title="원의 중심을 고르기",
        canvas=Canvas(width=960.0, height=320.0, coordinate_mode="logical"),
        regions=(
            Region(
                id="region.stem",
                role="stem",
                flow="absolute",
                slot_ids=(
                    "slot.q1",
                    "slot.q2",
                    "slot.q2.copy1.copy2",
                    "slot.q2.copy1.copy3",
                    "slot.q2.copy1.copy4",
                    "slot.q2.copy1.copy5",
                    "slot.q2.copy1.copy4.copy7",
                ),
            ),
            Region(
                id="region.diagram",
                role="diagram",
                flow="absolute",
                slot_ids=(
                    "slot.band",
                    "slot.dot.1",
                    "slot.dot.2",
                    "slot.dot.3",
                    "slot.dot.4",
                    "slot.dot.5",
                    "slot.pin.body",
                    "slot.pin.head",
                    "slot.pencil.body",
                    "slot.pencil.tip",
                ),
            ),
            Region(id="region.answer", role="answer", flow="absolute", slot_ids=()),
        ),
        slots=(
            TextSlot(
                id="slot.q1",
                prompt="",
                text="그림과 같이 띠 종이를 누름 못으로 고정한 후 연필을 구멍에 넣어 원을",
                style_role="question",
                x=54.0,
                y=28.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.q2",
                prompt="",
                text="그리려고 합니다. 원의 중심이 되는 곳을 선택하세요.",
                style_role="question",
                x=54.0,
                y=60.0,
                font_size=28,
            ),
            RectSlot(
                id="slot.band",
                prompt="",
                x=235,
                y=185,
                width=360,
                height=65,
                fill="#F6F0D3",
                stroke="#D7CFA8",
                stroke_width=1,
            ),
            CircleSlot(id="slot.dot.1", prompt="", cx=265, cy=220, r=5, fill="#D8C89A"),
            CircleSlot(id="slot.dot.2", prompt="", cx=335, cy=220, r=5, fill="#D8C89A"),
            CircleSlot(id="slot.dot.3", prompt="", cx=405, cy=220, r=5, fill="#D8C89A"),
            CircleSlot(id="slot.dot.4", prompt="", cx=475, cy=220, r=5, fill="#D8C89A"),
            CircleSlot(id="slot.dot.5", prompt="", cx=545, cy=220, r=5, fill="#D8C89A"),
            LineSlot(
                id="slot.pin.body",
                prompt="",
                x1=335,
                y1=180,
                x2=335,
                y2=205,
                stroke="#8E8E8E",
                stroke_width=6.0,
            ),
            CircleSlot(id="slot.pin.head", prompt="", cx=335, cy=173, r=10, fill="#C8C8C8"),
            LineSlot(
                id="slot.pencil.body",
                prompt="",
                x1=545,
                y1=135,
                x2=545,
                y2=200,
                stroke="#F38B82",
                stroke_width=8,
            ),
            LineSlot(
                id="slot.pencil.tip",
                prompt="",
                x1=545,
                y1=200,
                x2=545,
                y2=205,
                stroke="#7A4A34",
                stroke_width=2,
            ),
            TextSlot(
                id="slot.q2.copy1.copy2",
                prompt="",
                text="1",
                x=255,
                y=285,
                font_size=30,
                fill="#111111",
            ),
            TextSlot(
                id="slot.q2.copy1.copy3",
                prompt="",
                text="2",
                x=330,
                y=285,
                font_size=30,
                fill="#111111",
            ),
            TextSlot(
                id="slot.q2.copy1.copy4",
                prompt="",
                text="3",
                x=400,
                y=285,
                font_size=30,
                fill="#111111",
            ),
            TextSlot(
                id="slot.q2.copy1.copy5",
                prompt="",
                text="4",
                x=470,
                y=285,
                font_size=30,
                fill="#111111",
            ),
            TextSlot(
                id="slot.q2.copy1.copy4.copy7",
                prompt="",
                text="5",
                x=535,
                y=285,
                font_size=30,
                fill="#111111",
            ),
        ),
        diagrams=(),
        groups=(),
        constraints=(),
        tags=("도형", "원의 중심", "객관식"),
    )


PROBLEM_TEMPLATE = build_problem_template()

SEMANTIC_OVERRIDE = {
    "problem_id": "S3_초등_3_008693",
    "problem_type": "geometry_center_choice",
    "metadata": {
        "language": "ko",
        "question": "그림에서 원의 중심이 되는 곳을 고르는 문제",
        "instruction": "원의 중심이 되는 곳을 선택하세요.",
    },
    "domain": {
        "objects": [
            {"id": "obj.band", "type": "strip"},
            {"id": "obj.points", "type": "ordered_points", "count": 5},
            {"id": "obj.pin", "type": "pushpin"},
            {"id": "obj.pencil", "type": "pencil"},
        ],
        "relations": [],
        "problem_solving": {
            "understand": {
                "given_refs": ["obj.points", "obj.pin", "obj.pencil"],
                "target_ref": "answer.target",
                "condition_refs": ["rel.pin_center"],
            },
            "plan": {
                "method": "identify_marked_center",
                "description": "누름 못이 꽂힌 위치가 중심인지 그림과 해설을 함께 보고 판단한다.",
            },
            "execute": {
                "expected_operations": [
                    "locate_pin_position",
                    "match_center_to_point",
                    "select_option",
                ]
            },
            "review": {"check_methods": ["compare_with_explanation", "verify_selected_option"]},
        },
    },
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {"type": "multiple_choice_option", "description": "원의 중심이 되는 곳"},
        "value": 2,
        "unit": "",
    },
}

SOLVABLE = {
    "schema": "modu.solvable.v1.1",
    "problem_id": "S3_초등_3_008693",
    "problem_type": "geometry_center_choice",
    "inputs": {
        "total_ticks": 5,
        "target_label": "원의 중심이 되는 곳",
        "target_ticks": 1,
        "target_count": 1,
        "unit": "",
    },
    "given": [
        {"ref": "obj.points", "value": {"count": 5}},
        {"ref": "obj.pin", "value": {"marked_point": 2}},
    ],
    "target": {"ref": "answer.target", "type": "multiple_choice_option"},
    "method": "identify_marked_center",
    "plan": [
        "그림에서 누름 못이 꽂힌 위치를 찾는다.",
        "그 위치가 원의 중심인지 확인하고 선택지를 고른다.",
    ],
    "steps": [
        {"id": "step.1", "expr": "누름 못이 꽂힌 위치 확인", "value": 2},
        {"id": "step.2", "expr": "원의 중심에 해당하는 선택지", "value": 2},
    ],
    "checks": [
        {
            "id": "check.1",
            "expr": "해설의 선택지와 일치하는가",
            "expected": 2,
            "actual": 2,
            "pass": True,
        }
    ],
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {"type": "multiple_choice_option", "description": "원의 중심이 되는 곳"},
        "value": 2,
        "unit": "",
    },
}
