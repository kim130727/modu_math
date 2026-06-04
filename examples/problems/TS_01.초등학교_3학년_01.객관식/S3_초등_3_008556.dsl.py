from __future__ import annotations

from modu_math.dsl import Canvas, LineSlot, ProblemTemplate, RectSlot, Region, TextSlot


def build_problem_template() -> ProblemTemplate:
    return ProblemTemplate(
        id="S3_초등_3_008556",
        title="색칠된 부분은 실제 어떤 수의 곱인지를 찾아 선택하세요.",
        canvas=Canvas(width=900, height=420, coordinate_mode="logical"),
        regions=(
            Region(id="region.stem", role="stem", flow="absolute", slot_ids=("slot.q.text")),
            Region(id="region.work", role="diagram", flow="absolute", slot_ids=()),
            Region(id="region.choice", role="choices", flow="absolute", slot_ids=()),
            Region(id="region.footer", role="footer", flow="absolute", slot_ids=()),
        ),
        slots=(
            TextSlot(id="slot.q.text", prompt="", text="색칠된 부분은 실제 어떤 수의 곱인지를 찾아 선택하세요.", style_role="question", x = 40, y = 40, font_size=36),

            LineSlot(id="slot.v1", prompt="", x1 = 425, y1 = 60, x2 = 425, y2 = 315, stroke="#9AA0A6", stroke_width=1.2, stroke_dasharray="5 3"),
            LineSlot(id="slot.v2", prompt="", x1 = 465, y1 = 60, x2 = 465, y2 = 315, stroke="#9AA0A6", stroke_width=1.2, stroke_dasharray="5 3"),
            LineSlot(id="slot.v3", prompt="", x1 = 505, y1 = 60, x2 = 505, y2 = 315, stroke="#9AA0A6", stroke_width=1.2, stroke_dasharray="5 3"),
            LineSlot(id="slot.v4", prompt="", x1 = 545, y1 = 60, x2 = 545, y2 = 315, stroke="#9AA0A6", stroke_width=1.2, stroke_dasharray="5 3"),
            LineSlot(id="slot.v5", prompt="", x1 = 585, y1 = 60, x2 = 585, y2 = 315, stroke="#9AA0A6", stroke_width=1.2, stroke_dasharray="5 3"),

            TextSlot(id="slot.top2", prompt="", text="5 1 2", style_role="diagram", x = 480, y = 95, font_size=44),
            TextSlot(id="slot.mulx", prompt="", text="×", style_role="diagram", x = 425, y = 135, font_size=44),
            TextSlot(id="slot.mul0", prompt="", text="3", style_role="diagram", x = 552, y = 135, font_size=44),
            LineSlot(id="slot.bar1", prompt="", x1 = 415, y1 = 140, x2 = 585, y2 = 140),

            TextSlot(id="slot.p0", prompt="", text="6", style_role="diagram", x = 550, y = 185, font_size=44),
            RectSlot(id="slot.hl", prompt="", x = 505, y = 190, width=78.0, height=40.0, fill="#efc8b9"),
            TextSlot(id="slot.p11", prompt="", text="3 0", style_role="diagram", x = 515, y = 225, font_size=44),

            TextSlot(id="slot.p23", prompt="", text="1 5 0 0", style_role="diagram", x = 442, y = 265, font_size=44),
            LineSlot(id="slot.bar2", prompt="", x1 = 415, y1 = 270, x2 = 585, y2 = 270),

            TextSlot(id="slot.f3", prompt="", text="1 5 3 6", style_role="diagram", x = 442, y = 310, font_size=44),

            RectSlot(id="slot.choice.box", prompt="", x = 190, y = 335, width=514.0, height=76.0, stroke="#D8A100", stroke_width=2.0, fill="none"),
            TextSlot(id="slot.c1", prompt="", text="1 × 3", style_role="choice", x = 260, y = 385, font_size=40),
            TextSlot(id="slot.c2", prompt="", text="10 × 3", style_role="choice", x = 395, y = 385, font_size=40),
            TextSlot(id="slot.c3", prompt="", text="100 × 3", style_role="choice", x = 540, y = 385, font_size=40),
        ),
        diagrams=(),
        groups=(),
        constraints=(),
        tags=("초등", "수학", "곱셈", "세로셈", "자리값"),
    )


PROBLEM_TEMPLATE = build_problem_template()

SEMANTIC_OVERRIDE = {
    "problem_id": "S3_초등_3_008556",
    "problem_type": "multiplication_place_value_choice",
    "metadata": {
        "language": "ko",
        "question": "색칠된 부분은 실제 어떤 수의 곱인지를 찾아 선택하세요.",
        "instruction": "보기에서 알맞은 식을 고르세요.",
    },
    "domain": {"objects": [{"id": "obj.target", "type": "expression", "text": "10 × 3"}], "relations": []},
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {"type": "selected_expression", "description": "색칠된 부분에 해당하는 식"},
        "value": "10 × 3",
        "unit": "",
    },
}

SOLVABLE = {
    "schema": "modu.solvable.v1.1",
    "problem_id": "S3_초등_3_008556",
    "problem_type": "multiplication_place_value_choice",
    "inputs": {"total_ticks": 0, "target_label": "색칠된 부분에 해당하는 식", "target_ticks": 0, "target_count": 1, "unit": ""},
    "given": [{"ref": "obj.target", "value": "10 × 3"}],
    "target": {"ref": "answer.target", "type": "selected_expression"},
    "method": "place_value_matching",
    "plan": ["색칠된 부분과 자리값을 확인한다.", "같은 식을 고른다."],
    "steps": [{"id": "step.1", "expr": "색칠된 부분과 보기 비교", "value": "10 × 3"}],
    "checks": [{"id": "check.1", "expr": "검산", "expected": "일치", "actual": "일치", "pass": True}],
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {"type": "selected_expression", "description": "색칠된 부분에 해당하는 식"},
        "value": "10 × 3",
        "unit": "",
    },
}
