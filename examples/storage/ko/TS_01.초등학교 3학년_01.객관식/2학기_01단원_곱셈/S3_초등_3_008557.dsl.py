from __future__ import annotations

from modu_math.dsl import Canvas, LineSlot, ProblemTemplate, RectSlot, Region, TextSlot

QUESTION = "색칠된 부분은 실제 어떤 수의 곱인지 찾아 선택하세요."
TARGET_EXPRESSION = "300 × 4"
TARGET_DESCRIPTION = "색칠된 부분이 나타내는 곱"


def build_problem_template() -> ProblemTemplate:
    return ProblemTemplate(
        id="S3_초등_3_008557",
        title=QUESTION,
        canvas=Canvas(width=900, height=420, coordinate_mode="logical"),
        regions=(
            Region(id="region.stem", role="stem", flow="absolute", slot_ids=("slot.q.text",)),
            Region(id="region.work", role="diagram", flow="absolute", slot_ids=()),
            Region(id="region.choice", role="choices", flow="absolute", slot_ids=()),
            Region(id="region.footer", role="footer", flow="absolute", slot_ids=()),
        ),
        slots=(
            TextSlot(
                id="slot.q.text",
                prompt="",
                text="색칠된 부분은 실제 어떤 수의 곱인지 찾아 선택하세요.",
                style_role="question",
                x=40,
                y=40,
                font_size=36,
                fill="#111111",
            ),
            TextSlot(
                id="slot.top2",
                prompt="",
                text="3 9 5",
                style_role="diagram",
                x=492,
                y=95,
                font_size=44,
                fill="#111111",
            ),
            TextSlot(
                id="slot.mulx",
                prompt="",
                text="×",
                style_role="diagram",
                x=425,
                y=135,
                font_size=44,
                fill="#111111",
            ),
            TextSlot(
                id="slot.mul0",
                prompt="",
                text="4",
                style_role="diagram",
                x=554.001,
                y=130,
                font_size=44,
                fill="#111111",
            ),
            LineSlot(
                id="slot.bar1",
                prompt="",
                x1=415,
                y1=140,
                x2=585,
                y2=140,
                stroke="#111111",
                stroke_width=2,
            ),
            TextSlot(
                id="slot.p0",
                prompt="",
                text="2 0",
                style_role="diagram",
                x=524.003,
                y=179,
                font_size=44,
                fill="#111111",
            ),
            RectSlot(
                id="slot.hl",
                prompt="",
                x=440,
                y=225,
                width=145,
                height=40,
                fill="#efc8b9",
                stroke="#111111",
                stroke_width=1.5,
            ),
            TextSlot(
                id="slot.p11",
                prompt="",
                text="3 6 0",
                style_role="diagram",
                x=492.006,
                y=218,
                font_size=44,
                fill="#111111",
            ),
            TextSlot(
                id="slot.p23",
                prompt="",
                text="1 2 0 0",
                style_role="diagram",
                x=466.008,
                y=264,
                font_size=44,
                fill="#111111",
            ),
            LineSlot(
                id="slot.bar2",
                prompt="",
                x1=415,
                y1=270,
                x2=585,
                y2=270,
                stroke="#111111",
                stroke_width=2,
            ),
            TextSlot(
                id="slot.f3",
                prompt="",
                text="1 5 8 0",
                style_role="diagram",
                x=465.008,
                y=314,
                font_size=44,
                fill="#111111",
            ),
            RectSlot(
                id="slot.choice.box",
                prompt="",
                x=40,
                y=335,
                width=805,
                height=75,
                stroke="#D8A100",
                stroke_width=2,
                fill="none",
            ),
            TextSlot(
                id="slot.c1",
                prompt="",
                text="3 × 4",
                style_role="choice",
                x=135,
                y=385,
                font_size=40,
                fill="#111111",
            ),
            TextSlot(
                id="slot.c2",
                prompt="",
                text="30 × 4",
                style_role="choice",
                x=370,
                y=385,
                font_size=40,
                fill="#111111",
            ),
            TextSlot(
                id="slot.c3",
                prompt="",
                text="300 × 4",
                style_role="choice",
                x=630,
                y=385,
                font_size=40,
                fill="#111111",
            ),
        ),
        diagrams=(),
        groups=(),
        constraints=(),
        tags=("초등", "수학", "곱셈", "세로셈", "자리값"),
    )


PROBLEM_TEMPLATE = build_problem_template()

SEMANTIC_OVERRIDE = {
    "problem_id": "S3_초등_3_008557",
    "problem_type": "multiplication_place_value_choice",
    "metadata": {
        "language": "ko",
        "question": QUESTION,
        "instruction": "색칠된 부분이 나타내는 곱셈식을 고르세요.",
    },
    "domain": {
        "objects": [
            {"id": "obj.target", "type": "expression", "text": TARGET_EXPRESSION},
        ],
        "relations": [],
    },
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {"type": "selected_expression", "description": TARGET_DESCRIPTION},
        "value": TARGET_EXPRESSION,
        "unit": "",
    },
}

SOLVABLE = {
    "schema": "modu.solvable.v1.1",
    "problem_id": "S3_초등_3_008557",
    "problem_type": "multiplication_place_value_choice",
    "inputs": {
        "total_ticks": 0,
        "target_label": TARGET_DESCRIPTION,
        "target_ticks": 0,
        "target_count": 1,
        "unit": "",
    },
    "given": [
        {"ref": "obj.target", "value": TARGET_EXPRESSION},
    ],
    "target": {"ref": "answer.target", "type": "selected_expression"},
    "method": "place_value_matching",
    "plan": [
        "색칠된 부분의 자리값을 확인합니다.",
        "색칠된 부분은 300과 4의 곱을 나타냅니다.",
        "보기에서 300 × 4를 선택합니다.",
    ],
    "steps": [
        {"id": "step.1", "expr": "색칠된 부분 = 300 × 4", "value": TARGET_EXPRESSION},
    ],
    "checks": [
        {
            "id": "check.1",
            "expr": TARGET_DESCRIPTION,
            "expected": TARGET_EXPRESSION,
            "actual": TARGET_EXPRESSION,
            "pass": True,
        },
    ],
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {"type": "selected_expression", "description": TARGET_DESCRIPTION},
        "value": TARGET_EXPRESSION,
        "unit": "",
    },
}
