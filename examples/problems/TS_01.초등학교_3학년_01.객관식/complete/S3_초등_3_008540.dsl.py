from __future__ import annotations

from modu_math.dsl import Canvas, LineSlot, ProblemTemplate, RectSlot, Region, TextSlot


def build_problem_template() -> ProblemTemplate:
    return ProblemTemplate(
        id="S3_초등_3_008540",
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
                slot_ids=("slot.choice.box", "slot.choice.1", "slot.choice.2", "slot.choice.3", "slot.choice.4"),
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
                x1 = 275, y1 = 40, x2 = 275, y2 = 295, stroke="#9AA0A6",
                stroke_width=1.2,
                stroke_dasharray="5 3",
            ),
            LineSlot(
                id="slot.mul.vline2",
                prompt="",
                x1 = 300, y1 = 40, x2 = 300, y2 = 295, stroke="#9AA0A6",
                stroke_width=1.2,
                stroke_dasharray="5 3",
            ),
            LineSlot(
                id="slot.mul.vline3",
                prompt="",
                x1 = 322, y1 = 40, x2 = 322, y2 = 295, stroke="#9AA0A6",
                stroke_width=1.2,
                stroke_dasharray="5 3",
            ),
            LineSlot(
                id="slot.mul.vline4",
                prompt="",
                x1 = 342, y1 = 40, x2 = 342, y2 = 295, stroke="#9AA0A6",
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
            LineSlot(id="slot.mul.hline2", prompt="", x1 = 245, y1 = 170, x2 = 365, y2 = 170, stroke="#222222", stroke_width=1.2),
            LineSlot(id="slot.mul.hline3", prompt="", x1 = 245, y1 = 250, x2 = 365, y2 = 250, stroke="#222222", stroke_width=1.2),
            LineSlot(id="slot.mul.hline4", prompt="", x1 = 245, y1 = 295, x2 = 365, y2 = 295, stroke="#222222", stroke_width=1.2),
            TextSlot(id="slot.mul.869", prompt="", text="8 6 9", style_role="diagram", x = 304, y = 75, font_size=28),
            TextSlot(id="slot.mul.x", prompt="", text="×", style_role="diagram", x=240.0, y=112.0, font_size=28),
            TextSlot(id="slot.mul.4", prompt="", text="4", style_role="diagram", x = 347, y = 110, font_size=28),
            TextSlot(id="slot.mul.36", prompt="", text="3 6", style_role="diagram", x = 325, y = 157, font_size=28),
            RectSlot(id="slot.mul.highlight", prompt="", x = 285, y = 180, width=80.0, height=38.0, fill="#F4C6D8"),
            TextSlot(id="slot.mul.240", prompt="", text="2 4 0", style_role="diagram", x = 303, y = 210, font_size=28),
            TextSlot(id="slot.mul.3200", prompt="", text="3 2 0 0", style_role="diagram", x = 281, y = 245, font_size=28),
            TextSlot(id="slot.mul.3476", prompt="", text="3 4 7 6", style_role="diagram", x = 281, y = 285, font_size=28),
            RectSlot(id="slot.choice.box", prompt="", x=452.0, y=84.0, width=292.0, height=168.0, stroke="#F39C12", stroke_width=2.0, fill="none"),
            TextSlot(id="slot.choice.1", prompt="", text="6 × 4", style_role="diagram", x = 495, y = 145, font_size=28),
            TextSlot(id="slot.choice.2", prompt="", text="69 × 4", style_role="diagram", x = 610, y = 145, font_size=28),
            TextSlot(id="slot.choice.3", prompt="", text="60 × 4", style_role="diagram", x = 485, y = 205, font_size=28),
            TextSlot(id="slot.choice.4", prompt="", text="600 × 4", style_role="diagram", x = 600, y = 205, font_size=28),
        ),
        diagrams=(),
        groups=(),
        constraints=(),
        tags=(),
    )


PROBLEM_TEMPLATE = build_problem_template()

SEMANTIC_OVERRIDE = {
    "problem_id": "S3_초등_3_008540",
    "problem_type": "multiple_choice_multiplication_place_value",
    "metadata": {
        "language": "ko",
        "question": "색칠한 부분이 실제 어떤 수의 곱인지 찾아 선택하세요.",
        "instruction": "보기에서 알맞은 식을 고른다.",
    },
    "domain": {
        "objects": [
            {"id": "obj.multiple", "type": "multiplication_expression", "text": "869 × 4"},
            {"id": "obj.highlighted_value", "type": "value", "text": "240"},
            {"id": "obj.choice_set", "type": "multiple_choice_options", "text": ["6 × 4", "69 × 4", "60 × 4", "600 × 4"]},
        ],
        "relations": [
            {"id": "rel.highlighted_part", "type": "corresponds_to_place_value", "from_id": "obj.highlighted_value", "to_id": "obj.multiple"}
        ],
    },
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {"type": "matching_expression", "description": "색칠한 부분 240에 해당하는 실제 곱"},
        "value": "60 × 4",
        "unit": "",
    },
}

SOLVABLE = {
    "schema": "modu.solvable.v1.1",
    "problem_id": "S3_초등_3_008540",
    "problem_type": "multiple_choice_multiplication_place_value",
    "inputs": {"total_ticks": 1, "target_label": "색칠한 부분", "target_ticks": 1, "target_count": 1, "unit": ""},
    "given": [
        {"ref": "obj.multiple", "value": "869 × 4"},
        {"ref": "obj.highlighted_value", "value": "240"},
        {"ref": "obj.choice_set", "value": ["6 × 4", "69 × 4", "60 × 4", "600 × 4"]},
    ],
    "target": {"ref": "answer.target", "type": "matching_expression"},
    "method": "place_value_matching",
    "plan": ["색칠한 부분이 나타내는 자리값을 해설 문장과 함께 확인한다.", "보기 중 같은 수식을 찾는다."],
    "steps": [
        {"id": "step.1", "expr": "869에서 6은 60을 나타낸다", "value": "60"},
        {"id": "step.2", "expr": "60 × 4", "value": 240},
        {"id": "step.3", "expr": "색칠한 부분 240에 대응하는 보기 찾기", "value": "60 × 4"},
    ],
    "checks": [{"id": "check.1", "expr": "60 × 4 = 240", "expected": 240, "actual": 240, "pass": True}],
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {"type": "matching_expression", "description": "색칠한 부분 240에 해당하는 실제 곱"},
        "value": "60 × 4",
        "unit": "",
    },
}
