from __future__ import annotations

from modu_math.dsl import Canvas, LineSlot, ProblemTemplate, RectSlot, Region, TextSlot


QUESTION = "색칠된 부분은 실제 어떤 수의 곱인지 찾아 선택하세요."
TARGET_EXPRESSION = "60 × 4"
TARGET_DESCRIPTION = "색칠된 부분이 나타내는 곱"


def build_problem_template() -> ProblemTemplate:
    return ProblemTemplate(
        id="S3_초등_3_008559",
        title=QUESTION,
        canvas=Canvas(width=800, height=420, coordinate_mode="logical"),
        regions=(
            Region(id="region.stem", role="stem", flow="absolute", slot_ids=("slot.q.no", "slot.q.text")),
        ),
        slots=(
            TextSlot(id="slot.q.no", prompt="", text="23.", style_role="question", x=12, y=30, font_size=38),
            TextSlot(id="slot.q.text", prompt="", text=QUESTION, style_role="question", x=48, y=30, font_size=44),
            RectSlot(id="slot.choice.box", prompt="", x=513, y=63, width=150, height=219, fill="none"),
            TextSlot(id="t2", prompt="", text="7", style_role="diagram", x=344, y=74, font_size=44),
            TextSlot(id="t1", prompt="", text="6", style_role="diagram", x=384, y=74, font_size=44),
            TextSlot(id="t0", prompt="", text="2", style_role="diagram", x=424, y=74, font_size=44),
            TextSlot(id="mx", prompt="", text="×", style_role="diagram", x=300, y=114, font_size=44),
            TextSlot(id="m0", prompt="", text="4", style_role="diagram", x=424, y=114, font_size=44),
            LineSlot(id="l1", prompt="", x1=298, y1=122, x2=438, y2=122),
            TextSlot(id="p0", prompt="", text="8", style_role="diagram", x=424, y=156, font_size=44),
            RectSlot(id="hl", prompt="", x=368, y=168, width=88, height=38, fill="#e9c8dc"),
            TextSlot(id="h2", prompt="", text="2", style_role="diagram", x=374, y=200, font_size=44),
            TextSlot(id="h1", prompt="", text="4", style_role="diagram", x=408, y=200, font_size=44),
            TextSlot(id="h0", prompt="", text="0", style_role="diagram", x=442, y=200, font_size=44),
            TextSlot(id="p23", prompt="", text="2", style_role="diagram", x=304, y=240, font_size=44),
            TextSlot(id="p22", prompt="", text="8", style_role="diagram", x=344, y=240, font_size=44),
            TextSlot(id="p21", prompt="", text="0", style_role="diagram", x=384, y=240, font_size=44),
            TextSlot(id="p20", prompt="", text="0", style_role="diagram", x=424, y=240, font_size=44),
            LineSlot(id="l2", prompt="", x1=298, y1=242, x2=458, y2=242),
            TextSlot(id="f3", prompt="", text="3", style_role="diagram", x=304, y=280, font_size=44),
            TextSlot(id="f2", prompt="", text="0", style_role="diagram", x=344, y=280, font_size=44),
            TextSlot(id="f1", prompt="", text="4", style_role="diagram", x=384, y=280, font_size=44),
            TextSlot(id="f0", prompt="", text="8", style_role="diagram", x=424, y=280, font_size=44),
            TextSlot(id="c1", prompt="", text="6 × 4", style_role="choice", x=536, y=112, font_size=40),
            TextSlot(id="c2", prompt="", text=TARGET_EXPRESSION, style_role="choice", x=536, y=154, font_size=40),
            TextSlot(id="c3", prompt="", text="62 × 4", style_role="choice", x=536, y=196, font_size=40),
            TextSlot(id="c4", prompt="", text="600 × 4", style_role="choice", x=536, y=238, font_size=40),
            TextSlot(id="a", prompt="", text="(답) 60 × 4", style_role="body", x=8, y=334, font_size=36),
            TextSlot(id="e", prompt="", text="(풀이) 762에서 6은 십의 자리이므로 60 × 4 = 240입니다.", style_role="body", x=8, y=382, font_size=40),
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
