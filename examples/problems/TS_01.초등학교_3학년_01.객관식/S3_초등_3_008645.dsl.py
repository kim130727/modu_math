from __future__ import annotations
from modu_math.dsl import (
    Canvas,
    ProblemTemplate,
    Region,
    TextSlot,
    RectSlot,
    LineSlot,
    CircleSlot,
)


def build_problem_template() -> ProblemTemplate:
    return ProblemTemplate(
        id="S3_초등_3_008645",
        title="원의 지름",
        canvas=Canvas(width=960, height=540, coordinate_mode="logical"),
        regions=(
            Region(
                id="region.stem",
                role="stem",
                flow="absolute",
                slot_ids=("slot.q0", "slot.q1", "slot.q2", "slot.q3"),
            ),
        ),
        slots=(
            TextSlot(
                id="slot.q0",
                prompt="",
                text="□",
                style_role="question",
                x=8.0,
                y=28.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.q1",
                prompt="",
                text="17.",
                style_role="question",
                x=44.0,
                y=30.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.q2",
                prompt="",
                text="지름을 나타내는 선분을 찾아 길이를 잰 값을 보고, 맞는 말을 선택해 보세요.",
                style_role="question",
                x=76.0,
                y=30.0,
                font_size=28,
            ),
            CircleSlot(
                id="slot.circle.outer",
                prompt="",
                cx=526.0,
                cy=170.0,
                r=79.0,
                fill="none",
            ),
            CircleSlot(
                id="slot.circle.center",
                prompt="",
                cx=526.0,
                cy=170.0,
                r=3.6,
                fill="#d81b60",
            ),
            TextSlot(
                id="slot.lb.o",
                prompt="",
                text="ㅇ",
                style_role="label",
                x=535.0,
                y=168.0,
                font_size=18,
            ),
            LineSlot(
                id="slot.line.gm", prompt="", x1=501.0, y1=103.0, x2=552.0, y2=237.0
            ),
            LineSlot(
                id="slot.line.nb", prompt="", x1=446.0, y1=162.0, x2=609.0, y2=179.0
            ),
            LineSlot(
                id="slot.line.ls", prompt="", x1=514.0, y1=91.0, x2=504.0, y2=248.0
            ),
            LineSlot(
                id="slot.line.d", prompt="", x1=480.0, y1=232.0, x2=531.0, y2=173.0
            ),
            TextSlot(
                id="slot.lb.ㄱ",
                prompt="",
                text="ㄱ",
                style_role="label",
                x=485.0,
                y=86.0,
                font_size=18,
            ),
            TextSlot(
                id="slot.lb.ㄴ",
                prompt="",
                text="ㄴ",
                style_role="label",
                x=421.0,
                y=171.0,
                font_size=18,
            ),
            TextSlot(
                id="slot.lb.ㄷ",
                prompt="",
                text="ㄷ",
                style_role="label",
                x=457.0,
                y=246.0,
                font_size=18,
            ),
            TextSlot(
                id="slot.lb.ㄹ",
                prompt="",
                text="ㄹ",
                style_role="label",
                x=495.0,
                y=255.0,
                font_size=18,
            ),
            TextSlot(
                id="slot.lb.ㅁ",
                prompt="",
                text="ㅁ",
                style_role="label",
                x=571.0,
                y=245.0,
                font_size=18,
            ),
            TextSlot(
                id="slot.lb.ㅂ",
                prompt="",
                text="ㅂ",
                style_role="label",
                x=613.0,
                y=184.0,
                font_size=18,
            ),
            TextSlot(
                id="slot.lb.ㅅ",
                prompt="",
                text="ㅅ",
                style_role="label",
                x=531.0,
                y=84.0,
                font_size=18,
            ),
            RectSlot(
                id="slot.table.outer",
                prompt="",
                x=238.0,
                y=286.0,
                width=515.0,
                height=76.0,
                fill="none",
            ),
            LineSlot(
                id="slot.table.v1", prompt="", x1=391.0, y1=286.0, x2=391.0, y2=362.0
            ),
            LineSlot(
                id="slot.table.v2", prompt="", x1=494.0, y1=286.0, x2=494.0, y2=362.0
            ),
            LineSlot(
                id="slot.table.v3", prompt="", x1=597.0, y1=286.0, x2=597.0, y2=362.0
            ),
            LineSlot(
                id="slot.table.h1", prompt="", x1=238.0, y1=323.0, x2=753.0, y2=323.0
            ),
            TextSlot(
                id="slot.t1",
                prompt="",
                text="지름",
                style_role="table",
                x=281.0,
                y=313.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.t2",
                prompt="",
                text="선분 ㄱㅁ",
                style_role="table",
                x=405.0,
                y=313.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.t3",
                prompt="",
                text="선분 ㄴㅂ",
                style_role="table",
                x=505.0,
                y=313.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.t4",
                prompt="",
                text="선분 ㄹㅅ",
                style_role="table",
                x=610.0,
                y=313.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.t5",
                prompt="",
                text="길이(cm)",
                style_role="table",
                x=263.0,
                y=351.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.t6",
                prompt="",
                text="3",
                style_role="table",
                x=431.0,
                y=351.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.t7",
                prompt="",
                text="3",
                style_role="table",
                x=535.0,
                y=351.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.t8",
                prompt="",
                text="3",
                style_role="table",
                x=638.0,
                y=351.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.arrow",
                prompt="",
                text="➜",
                style_role="instruction",
                x=134.0,
                y=409.0,
                font_size=34,
            ),
            TextSlot(
                id="slot.q3",
                prompt="",
                text="한 원에서 원의 지름은 모두 ( 같습니다 , 다릅니다 ).",
                style_role="question",
                x=188.0,
                y=411.0,
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
    "problem_id": "S3_초등_3_008645",
    "problem_type": "circle_diameter_comparison",
    "metadata": {
        "language": "ko",
        "question": "지름을 나타내는 선분을 찾아 길이를 잰 값을 보고, 맞는 말을 선택해 보세요.",
        "instruction": "한 원에서 원의 지름은 모두 (같습니다, 다릅니다).",
    },
    "domain": {
        "objects": [
            {"id": "obj.circle", "type": "circle"},
            {"id": "obj.segment.gm", "type": "segment", "label": "ㄱㅁ"},
            {"id": "obj.segment.nb", "type": "segment", "label": "ㄴㅂ"},
            {"id": "obj.segment.ls", "type": "segment", "label": "ㄹㅅ"},
        ],
        "relations": [],
        "problem_solving": {
            "understand": {
                "given_refs": [
                    "obj.circle",
                    "obj.segment.gm",
                    "obj.segment.nb",
                    "obj.segment.ls",
                ],
                "target_ref": "answer.target",
                "condition_refs": [
                    "rel.diameter_candidates",
                    "rel.diameter_candidates_2",
                    "rel.diameter_candidates_3",
                ],
            },
            "plan": {
                "method": "property_check",
                "description": "원의 중심을 지나며 원 위의 두 점을 잇는 선분이 지름인지 확인한다.",
            },
            "execute": {
                "expected_operations": [
                    "identify_diameter_candidates",
                    "compare_diameter_property",
                ]
            },
            "review": {"check_methods": ["property_consistency_check"]},
        },
    },
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {
            "type": "multiple_choice_completion",
            "description": "한 원에서 원의 지름은 모두 (같습니다, 다릅니다).",
        },
        "value": "같습니다",
        "unit": "",
    },
}

SOLVABLE = {
    "schema": "modu.solvable.v1.1",
    "problem_id": "S3_초등_3_008645",
    "problem_type": "circle_diameter_comparison",
    "inputs": {
        "total_ticks": 1,
        "target_label": "같습니다, 다릅니다",
        "target_ticks": 1,
        "target_count": 2,
        "unit": "",
    },
    "given": [
        {"ref": "obj.segment.gm", "value": {"label": "ㄱㅁ"}},
        {"ref": "obj.segment.nb", "value": {"label": "ㄴㅂ"}},
        {"ref": "obj.segment.ls", "value": {"label": "ㄹㅅ"}},
    ],
    "target": {"ref": "answer.target", "type": "multiple_choice_completion"},
    "method": "property_check",
    "plan": [
        "원의 중심을 지나고 원 위의 두 점을 잇는 선분이 지름인지 확인한다.",
        "지름의 성질을 이용해 한 원의 지름은 모두 같은지 판단한다.",
    ],
    "steps": [
        {
            "id": "step.1",
            "expr": "선분 ㄱㅁ, 선분 ㄴㅂ, 선분 ㄹㅅ은 지름 후보이다.",
            "value": "candidates",
        },
        {"id": "step.2", "expr": "한 원에서 지름은 모두 같다.", "value": "같습니다"},
    ],
    "checks": [
        {
            "id": "check.1",
            "expr": "지름의 성질 확인",
            "expected": "같습니다",
            "actual": "같습니다",
            "pass": True,
        }
    ],
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {
            "type": "multiple_choice_completion",
            "description": "한 원에서 원의 지름은 모두 (같습니다, 다릅니다).",
        },
        "value": "같습니다",
        "unit": "",
    },
}
