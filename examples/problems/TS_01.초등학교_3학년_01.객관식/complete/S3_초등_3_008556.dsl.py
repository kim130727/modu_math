from __future__ import annotations

from modu_math.dsl import Canvas, LineSlot, ProblemTemplate, RectSlot, Region, TextSlot

def build_problem_template() -> ProblemTemplate:
    return ProblemTemplate(
        id="S3_초등_3_008556",
        title="색칠한 부분이 실제 어떤 수의 곱인지 찾아 선택하세요.",
        canvas=Canvas(width=886, height=396, coordinate_mode="logical"),
        regions=(
            Region(id="region.stem", role="stem", flow="absolute", slot_ids=("slot.q1",)),
            Region(
                id="region.left",
                role="diagram",
                flow="absolute",
                slot_ids=(
                    "slot.mul.vline1",
                    "slot.mul.vline2",
                    "slot.mul.vline3",
                    "slot.mul.vline4",
                    "slot.mul.vline5",
                    "slot.mul.hline1",
                    "slot.mul.hline2",
                    "slot.mul.hline3",
                    "slot.mul.hline4",
                    "slot.mul.869",
                    "slot.mul.x",
                    "slot.mul.4",
                    "slot.mul.36",
                    "slot.mul.240",
                    "slot.mul.3200",
                    "slot.mul.3476",
                    "slot.mul.highlight",
                ),
            ),
            Region(
                id="region.choice",
                role="diagram",
                flow="absolute",
                slot_ids=("slot.choice.box", "slot.choice.1", "slot.choice.2", "slot.choice.3"),
            ),
        ),
        slots=(
            TextSlot(
                id="slot.q1",
                prompt="",
                text="색칠한 부분이 실제 어떤 수의 곱인지 찾아 선택하세요.",
                style_role="question",
                x = 10, y = 30, font_size=28,
            ),
            LineSlot(
                id="slot.mul.vline1",
                prompt="",
                x1 = 275, y1 = 40, x2 = 275, y2 = 285, stroke="#9AA0A6",
                stroke_width=1.2,
                stroke_dasharray="5 3",
            ),
            LineSlot(
                id="slot.mul.vline2",
                prompt="",
                x1 = 300, y1 = 40, x2 = 300, y2 = 285, stroke="#9AA0A6",
                stroke_width=1.2,
                stroke_dasharray="5 3",
            ),
            LineSlot(
                id="slot.mul.vline3",
                prompt="",
                x1 = 322, y1 = 40, x2 = 322, y2 = 285, stroke="#9AA0A6",
                stroke_width=1.2,
                stroke_dasharray="5 3",
            ),
            LineSlot(
                id="slot.mul.vline4",
                prompt="",
                x1 = 342, y1 = 40, x2 = 342, y2 = 285, stroke="#9AA0A6",
                stroke_width=1.2,
                stroke_dasharray="5 3",
            ),
            LineSlot(
                id="slot.mul.vline5",
                prompt="",
                x1 = 366, y1 = 40, x2 = 366, y2 = 290, stroke="#9AA0A6",
                stroke_width=1.2,
                stroke_dasharray="5 3",
            ),
            LineSlot(id="slot.mul.hline1", prompt="", x1 = 245, y1 = 125, x2 = 365, y2 = 125, stroke="#222222", stroke_width=1.2),
            LineSlot(id="slot.mul.hline3", prompt="", x1 = 245, y1 = 240, x2 = 365, y2 = 240, stroke="#222222", stroke_width=1.2),
            TextSlot(id="slot.mul.869", prompt="", text="5 1 2", style_role="diagram", x = 304, y = 75, font_size=28),
            TextSlot(id="slot.mul.x", prompt="", text="×", style_role="diagram", x=240.0, y=112.0, font_size=28),
            TextSlot(id="slot.mul.4", prompt="", text="3", style_role="diagram", x = 350, y = 110, font_size=28),
            TextSlot(id="slot.mul.36", prompt="", text="6", style_role="diagram", x = 350, y = 160, font_size=28),
            RectSlot(id="slot.mul.highlight", prompt="", x = 290, y = 168, width=80.0, height=38.0, fill="#F4C6D8"),
            TextSlot(id="slot.mul.240", prompt="", text="3 0", style_role="diagram", x = 328, y = 195, font_size=28),
            TextSlot(id="slot.mul.3200", prompt="", text="1 5 0 0", style_role="diagram", x = 281, y = 230, font_size=28),
            TextSlot(id="slot.mul.3476", prompt="", text="1 5 3 6", style_role="diagram", x = 281, y = 265, font_size=28),
            RectSlot(id="slot.choice.box", prompt="", x=452.0, y=84.0, width=292.0, height=168.0, stroke="#F39C12", stroke_width=2.0, fill="none"),
            TextSlot(id="slot.choice.1", prompt="", text="1 × 3", style_role="diagram", x = 495, y = 145, font_size=28),
            TextSlot(id="slot.choice.2", prompt="", text="10 × 3", style_role="diagram", x = 610, y = 145, font_size=28),
            TextSlot(id="slot.choice.3", prompt="", text="100 × 3", style_role="diagram", x = 485, y = 205, font_size=28),
        ),
        diagrams=(),
        groups=(),
        constraints=(),
        tags=(),
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
