from __future__ import annotations
from modu_math.dsl import Canvas, ProblemTemplate, Region, TextSlot, RectSlot, CircleSlot, LineSlot


def build_problem_template() -> ProblemTemplate:
    return ProblemTemplate(
        id="S3_초등_3_008688",
        title="원의 성질 선택",
        canvas=Canvas(width=886.0, height=563.0, coordinate_mode="logical"),
        regions=(
            Region(
                id="region.stem",
                role="stem",
                flow="absolute",
                slot_ids=(
                    "slot.q2",
                    "slot.circle",
                    "slot.circle.center",
                    "slot.circle.line1",
                    "slot.circle.line2",
                    "slot.circle.mark1",
                    "slot.choice_box",
                    "slot.choice.line1",
                    "slot.choice.line2",
                ),
            ),
        ),
        slots=(
            TextSlot(
                id="slot.q2",
                prompt="",
                text="알맞은 말을 선택하세요.",
                style_role="question",
                x=75,
                y=60,
                font_size=30,
            ),
            CircleSlot(id="slot.circle", prompt="", cx=485, cy=240, r=145, fill="none"),
            CircleSlot(id="slot.circle.center", prompt="", cx=485, cy=240, r=5, fill="#ff2a8a"),
            LineSlot(id="slot.circle.line1", prompt="", x1=340, y1=240, x2=630, y2=240),
            LineSlot(id="slot.circle.line2", prompt="", x1=405, y1=120, x2=565, y2=360),
            CircleSlot(id="slot.circle.mark1", prompt="", cx=505, cy=220, r=5, fill="none"),
            RectSlot(
                id="slot.choice_box", prompt="", x=70, y=405, width=765, height=120, fill="none"
            ),
            TextSlot(
                id="slot.choice.line1",
                prompt="",
                text="한 원에는 지름을 ( 2개만, 무수히 많이 ) 그을 수 있고",
                style_role="question",
                x=135,
                y=460,
                font_size=30,
            ),
            TextSlot(
                id="slot.choice.line2",
                prompt="",
                text="그 길이는 모두 ( 같습니다, 다릅니다 ).",
                style_role="question",
                x=185,
                y=495,
                font_size=30,
            ),
        ),
        diagrams=(),
        groups=(),
        constraints=(),
        tags=(),
    )


PROBLEM_TEMPLATE = build_problem_template()

SEMANTIC_OVERRIDE = {
    "problem_id": "S3_초등_3_008688",
    "problem_type": "multiple_choice_circle_property",
    "metadata": {
        "language": "ko",
        "question": "알맞은 말을 선택하세요.",
        "instruction": "원의 성질에 대한 문장 완성",
    },
    "domain": {
        "objects": [
            {"id": "obj.circle", "type": "circle"},
            {"id": "obj.diameter", "type": "diameter", "countability": "many"},
            {"id": "obj.diameter_length", "type": "length_property", "relation": "same"},
        ],
        "relations": [],
        "problem_solving": {
            "understand": {
                "given_refs": ["obj.circle"],
                "target_ref": "answer.target",
                "condition_refs": ["rel.diameter_count", "rel.diameter_length"],
            },
            "plan": {
                "method": "circle_property_selection",
                "description": "원의 성질을 보고 알맞은 선택지를 고른다.",
            },
            "execute": {
                "expected_operations": ["identify_circle_property", "choose_correct_words"]
            },
            "review": {"check_methods": ["property_consistency_check"]},
        },
    },
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {"type": "selected_words", "description": "문장 괄호 안에서 알맞은 말"},
        "value": "무수히 많이, 같습니다",
        "unit": "",
    },
}

SOLVABLE = {
    "schema": "modu.solvable.v1.1",
    "problem_id": "S3_초등_3_008688",
    "problem_type": "multiple_choice_circle_property",
    "inputs": {
        "total_ticks": 0,
        "target_label": "selected_words",
        "target_ticks": 0,
        "target_count": 2,
        "unit": "",
    },
    "given": [{"ref": "obj.circle", "value": {"type": "circle"}}],
    "target": {"ref": "answer.target", "type": "selected_words"},
    "method": "circle_property_selection",
    "plan": ["원의 성질을 확인한다.", "두 문장에 들어갈 알맞은 말을 고른다."],
    "steps": [
        {"id": "step.1", "expr": "원의 지름은 여러 개 그을 수 있는가", "value": "무수히 많이"},
        {"id": "step.2", "expr": "지름의 길이는 모두 같은가", "value": "같습니다"},
    ],
    "checks": [
        {
            "id": "check.1",
            "expr": "원의 지름 개수와 길이 성질이 문장과 일치하는가",
            "expected": True,
            "actual": True,
            "pass": True,
        }
    ],
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {"type": "selected_words", "description": "문장 괄호 안에서 알맞은 말"},
        "value": "무수히 많이, 같습니다",
        "unit": "",
    },
}
