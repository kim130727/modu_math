from __future__ import annotations

from modu_math.dsl import Canvas, LineSlot, ProblemTemplate, RectSlot, Region, TextSlot


QUESTION = "색칠된 부분은 실제 어떤 수의 곱인지 찾아 선택하세요."
TARGET_EXPRESSION = "60 × 4"
TARGET_DESCRIPTION = "색칠된 부분이 나타내는 곱"

def build_problem_template() -> ProblemTemplate:
    return ProblemTemplate(
        id="S3_초등_3_008559",
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
                text=QUESTION,
                style_role="question",
                x=40,
                y=40,
                font_size=36,
            ),
            LineSlot(id="slot.v1", prompt="", x1=425, y1=60, x2=425, y2=315, stroke="#9AA0A6", stroke_width=1.2, stroke_dasharray="5 3"),
            LineSlot(id="slot.v2", prompt="", x1=465, y1=60, x2=465, y2=315, stroke="#9AA0A6", stroke_width=1.2, stroke_dasharray="5 3"),
            LineSlot(id="slot.v3", prompt="", x1=505, y1=60, x2=505, y2=315, stroke="#9AA0A6", stroke_width=1.2, stroke_dasharray="5 3"),
            LineSlot(id="slot.v4", prompt="", x1=545, y1=60, x2=545, y2=315, stroke="#9AA0A6", stroke_width=1.2, stroke_dasharray="5 3"),
            LineSlot(id="slot.v5", prompt="", x1=585, y1=60, x2=585, y2=315, stroke="#9AA0A6", stroke_width=1.2, stroke_dasharray="5 3"),
            TextSlot(id="slot.top2", prompt="", text = '7 6 2', style_role="diagram", x = 480, y = 95, font_size = 45),
            TextSlot(id="slot.mulx", prompt="", text="×", style_role="diagram", x=425, y=135, font_size=44),
            TextSlot(id="slot.mul0", prompt="", text="4", style_role="diagram", x = 555, y = 135, font_size=44),
            LineSlot(id="slot.bar1", prompt="", x1=415, y1=140, x2=585, y2=140),
            TextSlot(id="slot.p0", prompt="", text = '8', style_role="diagram", x = 555, y = 180, font_size = 45),
            RectSlot(id="slot.hl", prompt="", x=440, y=225, width=145, height=40, fill="#efc8b9"),
            TextSlot(id="slot.p11", prompt="", text = '2 4 0', style_role="diagram", x = 480, y = 220, font_size = 45),
            TextSlot(id="slot.p23", prompt="", text="2 8 0 0", style_role="diagram", x = 445, y = 260, font_size=44),
            LineSlot(id="slot.bar2", prompt="", x1=415, y1=270, x2=585, y2=270),
            TextSlot(id="slot.f3", prompt="", text="3 0 4 8", style_role="diagram", x = 445, y = 310, font_size=44),
            RectSlot(
                id="slot.choice.box",
                prompt="",
                x = 45, y = 335, width = 790, height = 75, stroke="#D8A100",
                stroke_width=2.0,
                fill="none",
            ),
            TextSlot(id="slot.c1", prompt="", text = '6 × 4', style_role="choice", x = 110, y = 390, font_size = 40),
            TextSlot(id="slot.c2", prompt="", text = '60 × 4', style_role="choice", x = 290, y = 390, font_size = 40),
            TextSlot(id="slot.c3", prompt="", text = '62 × 4', style_role="choice", x = 485, y = 390, font_size = 40),
            TextSlot(id="slot.c4", prompt="", text = '600 × 4', style_role="choice", x = 665, y = 385, font_size = 40),
        ),
        diagrams=(),
        groups=(),
        constraints=(),
        tags=("초등", "수학", "곱셈", "세로셈", "자리값"),
    )


PROBLEM_TEMPLATE = build_problem_template()

SEMANTIC_OVERRIDE = {
    "problem_id": "S3_초등_3_008559",
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
    "problem_id": "S3_초등_3_008559",
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
        "762에서 6은 십의 자리 숫자이므로 실제로는 60을 뜻합니다.",
        "색칠된 부분은 60 × 4를 나타냅니다.",
    ],
    "steps": [
        {"id": "step.1", "expr": "762의 6 = 60", "value": 60},
        {"id": "step.2", "expr": "색칠된 부분 = 60 × 4", "value": TARGET_EXPRESSION},
    ],
    "checks": [
        {"id": "check.1", "expr": TARGET_DESCRIPTION, "expected": TARGET_EXPRESSION, "actual": TARGET_EXPRESSION, "pass": True},
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
