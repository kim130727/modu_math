from __future__ import annotations

from modu_math.dsl import Canvas, LineSlot, ProblemTemplate, RectSlot, Region, TextSlot


def build_problem_template() -> ProblemTemplate:
    return ProblemTemplate(
        id="S3_초등_3_008547",
        title="색칠된 부분은 실제 어떤 수의 곱인지 찾아 선택하세요.",
        canvas=Canvas(width=900, height=420, coordinate_mode="logical"),
        regions=(
            Region(id="region.stem", role="stem", flow="absolute", slot_ids=("slot.q.no", "slot.q.text")),
            Region(id="region.work", role="diagram", flow="absolute", slot_ids=()),
            Region(id="region.choices", role="choices", flow="absolute", slot_ids=()),
            Region(id="region.footer", role="footer", flow="absolute", slot_ids=()),
        ),
        slots=(
            TextSlot(
                id="slot.q.text",
                prompt="",
                text="색칠된 부분은 실제 어떤 수의 곱인지 찾아 선택하세요.",
                style_role="question",
                x=20.0,
                y=40.0,
                font_size=38,
            ),
            TextSlot(id="slot.top.d0", prompt="", text="3 2 4", style_role="diagram", x=305.0, y=104.0, font_size=44),
            TextSlot(id="slot.mul.sign", prompt="", text="×", style_role="diagram", x=274.0, y=146.0, font_size=44),
            TextSlot(id="slot.mul.d0", prompt="", text="6", style_role="diagram", x=374.0, y=146.0, font_size=44),
            LineSlot(id="slot.bar.1", prompt="", x1=270.0, y1=162.0, x2=392.0, y2=162.0),
            TextSlot(id="slot.part0.d0", prompt="", text="2 4", style_role="diagram", x=340.0, y=200.0, font_size=44),
            RectSlot(id="slot.highlight", prompt="", x = 300, y = 205, width = 110, height = 50, fill="#d9ddb7"),
            TextSlot(id="slot.part1.d0", prompt="", text = '1 2 0', style_role="diagram", x = 305, y = 242, font_size = 44, max_width = 772, fill = '#111111'),
            TextSlot(id="slot.part2.d0", prompt="", text="1 8 0 0", style_role="diagram", x=270.0, y=290.0, font_size=44),
            LineSlot(id="slot.bar.2", prompt="", x1=270.0, y1=300.0, x2=392.0, y2=300.0),
            TextSlot(id="slot.final.d0", prompt="", text="1 9 4 4", style_role="diagram", x=270.0, y=340.0, font_size=44),
            RectSlot(id="slot.choice.box", prompt="", x=510.0, y=77.0, width=214.0, height=252.0, fill="none"),
            TextSlot(id="slot.choice.1", prompt="", text="㉠ 2 × 6", style_role="choice", x=520.0, y=142.0, font_size=40),
            TextSlot(id="slot.choice.2", prompt="", text="㉡ 2 × 60", style_role="choice", x=520.0, y=186.0, font_size=40),
            TextSlot(id="slot.choice.3", prompt="", text="㉢ 20 × 6", style_role="choice", x=520.0, y=230.0, font_size=40),
            TextSlot(id="slot.choice.4", prompt="", text="㉣ 200 × 6", style_role="choice", x=520.0, y=274.0, font_size=40),
        ),
        diagrams=(),
        groups=(),
        constraints=(),
        tags=("초등", "수학", "곱셈", "세로셈", "자리값"),
    )


PROBLEM_TEMPLATE = build_problem_template()

SEMANTIC_OVERRIDE = {
    "problem_id": "S3_초등_3_008547",
    "problem_type": "multiplication_place_value_choice",
    "metadata": {
        "language": "ko",
        "question": "색칠된 부분은 실제 어떤 수의 곱인지 찾아 선택하세요.",
        "instruction": "보기에서 알맞은 식을 고르세요.",
    },
    "domain": {"objects": [{"id": "obj.target", "type": "expression", "text": "20 × 6"}], "relations": []},
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {"type": "selected_expression", "description": "색칠된 부분에 해당하는 식"},
        "value": "㉢ 20 × 6",
        "unit": "",
    },
}

SOLVABLE = {
    "schema": "modu.solvable.v1.1",
    "problem_id": "S3_초등_3_008547",
    "problem_type": "multiplication_place_value_choice",
    "inputs": {"total_ticks": 0, "target_label": "색칠된 부분에 해당하는 식", "target_ticks": 0, "target_count": 1, "unit": ""},
    "given": [
        {"ref": "obj.target", "value": "20 × 6"},
        {"ref": "obj.highlighted_value", "value": 120},
        {"ref": "obj.choice_set", "value": ["2 × 6", "2 × 60", "20 × 6", "200 × 6"]},
    ],
    "target": {"ref": "answer.target", "type": "selected_expression"},
    "method": "place_value_matching",
    "plan": ["세로셈에서 색칠된 120이 어떤 자리값 곱인지 확인한다.", "보기 중 같은 식을 고른다."],
    "steps": [
        {"id": "step.1", "expr": "324에서 십의 자리 2는 20을 나타낸다", "value": 20},
        {"id": "step.2", "expr": "20 × 6", "value": 120},
        {"id": "step.3", "expr": "색칠된 부분 120에 해당하는 보기 찾기", "value": "20 × 6"},
    ],
    "checks": [{"id": "check.1", "expr": "선택한 식 검산", "expected": "일치", "actual": "일치", "pass": True}],
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {"type": "selected_expression", "description": "색칠된 부분에 해당하는 식"},
        "value": "㉢ 20 × 6",
        "unit": "",
    },
}
