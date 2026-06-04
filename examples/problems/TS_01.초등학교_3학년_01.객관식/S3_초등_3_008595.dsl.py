from __future__ import annotations
from modu_math.dsl import Canvas, ProblemTemplate, RectSlot, Region, TextSlot


def build_problem_template() -> ProblemTemplate:
    return ProblemTemplate(
        id="S3_초등_3_008595",
        title="나누어떨어지는 나눗셈식을 찾아 기호를 선택해 보세요.",
        canvas=Canvas(width=752.0, height=321.0, coordinate_mode="logical"),
        regions=(
            Region(id="region.stem", role="stem", flow="absolute", slot_ids=("slot.q.no", "slot.q.text")),
            Region(
                id="region.choice_box",
                role="choices",
                flow="absolute",
                slot_ids=("slot.choice.box", "slot.choice.a.mark", "slot.choice.a.text", "slot.choice.b.mark", "slot.choice.b.text"),
            ),
        ),
        slots=(
            TextSlot(id="slot.q.no", prompt="", text="63.", style_role="question", x=12.0, y=31.0, font_size=28),
            TextSlot(id="slot.q.text", prompt="", text="나누어떨어지는 나눗셈식을 찾아 기호를 선택해 보세요.", style_role="question", x=98.0, y=31.0, font_size=28),
            RectSlot(id="slot.choice.box", prompt="", x=280.0, y=54.0, width=372.0, height=50.0, fill="none", stroke="#F4A259"),
            TextSlot(id="slot.choice.a.mark", prompt="", text="㉠", style_role="choice", x=300.0, y=86.0, font_size=28),
            TextSlot(id="slot.choice.a.text", prompt="", text="59 ÷ 5", style_role="choice", x=330.0, y=86.0, font_size=28),
            TextSlot(id="slot.choice.b.mark", prompt="", text="㉡", style_role="choice", x=500.0, y=86.0, font_size=28),
            TextSlot(id="slot.choice.b.text", prompt="", text="88 ÷ 4", style_role="choice", x=530.0, y=86.0, font_size=28),
        ),
        diagrams=(), groups=(), constraints=(), tags=("초등", "수학", "나눗셈", "나누어떨어짐", "선택형"),
    )


PROBLEM_TEMPLATE = build_problem_template()

SEMANTIC_OVERRIDE = {
    "problem_id": "S3_초등_3_008595",
    "problem_type": "multiple_choice_divisibility",
    "metadata": {"language": "ko", "question": "나누어떨어지는 나눗셈식을 찾아 기호를 선택해 보세요.", "instruction": "보기 중 나누어떨어지는 식의 기호를 고르세요."},
    "domain": {
        "objects": [
            {"id": "obj.choice.a", "type": "division_expression", "label": "㉠", "dividend": 59, "divisor": 5},
            {"id": "obj.choice.b", "type": "division_expression", "label": "㉡", "dividend": 88, "divisor": 4},
        ],
        "relations": [],
        "problem_solving": {
            "understand": {"given_refs": ["obj.choice.a", "obj.choice.b"], "target_ref": "answer.target", "condition_refs": ["rel.divisible"]},
            "plan": {"method": "compare_remainders", "description": "각 나눗셈식의 나머지를 확인해 나누어떨어지는 식을 고른다."},
            "execute": {"expected_operations": ["evaluate_division_expressions", "check_for_remainder", "select_divisible_choice"]},
            "review": {"check_methods": ["divisibility_check", "choice_consistency_check"]},
        },
    },
    "answer": {"blanks": [], "choices": [], "answer_key": [], "target": {"type": "selected_choice", "description": "나누어떨어지는 나눗셈식의 기호"}, "value": "㉡", "unit": ""},
}

SOLVABLE = {
    "schema": "modu.solvable.v1.1",
    "problem_id": "S3_초등_3_008595",
    "problem_type": "multiple_choice_divisibility",
    "inputs": {"target_label": "선택한 기호", "unit": "", "total_ticks": 0, "target_ticks": 0, "target_count": 1},
    "given": [
        {"ref": "obj.choice.a", "value": {"label": "㉠", "dividend": 59, "divisor": 5}},
        {"ref": "obj.choice.b", "value": {"label": "㉡", "dividend": 88, "divisor": 4}},
    ],
    "target": {"ref": "answer.target", "type": "selected_choice"},
    "method": "compare_remainders",
    "plan": ["각 보기의 나머지를 확인한다.", "나머지가 0인 보기의 기호를 고른다."],
    "steps": [
        {"id": "step.1", "expr": "59 ÷ 5", "value": {"quotient": 11, "remainder": 4}},
        {"id": "step.2", "expr": "88 ÷ 4", "value": {"quotient": 22, "remainder": 0}},
        {"id": "step.3", "expr": "선택한 기호", "value": "㉡"},
    ],
    "checks": [{"id": "check.1", "expr": "88 ÷ 4 remainder == 0", "expected": True, "actual": True, "pass": True}],
    "answer": {"blanks": [], "choices": [], "answer_key": [], "target": {"type": "selected_choice", "description": "나누어떨어지는 나눗셈식의 기호"}, "value": "㉡", "unit": ""},
}
