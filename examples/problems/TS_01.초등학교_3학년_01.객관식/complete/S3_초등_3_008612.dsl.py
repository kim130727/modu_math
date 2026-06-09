from __future__ import annotations
from modu_math.dsl import Canvas, ProblemTemplate, RectSlot, Region, TextSlot


def build_problem_template() -> ProblemTemplate:
    return ProblemTemplate(
        id="S3_초등_3_008612",
        title="다음 나눗셈이 나누어떨어지는지 판단하기",
        canvas=Canvas(width=940.0, height=364.0, coordinate_mode="logical"),
        regions=(
            Region(
                id="region.stem",
                role="stem",
                flow="absolute",
                slot_ids=("slot.q.text", "slot.expr.box", "slot.expr.text",'slot.q.text.copy2'),
            ),
            Region(
                id="region.choice",
                role="choices",
                flow="absolute",
                slot_ids=(),
            ),
            Region(
                id="region.explanation",
                role="explanation",
                flow="absolute",
                slot_ids=( ),
            ),
        ),
        slots=(TextSlot(
                id="slot.q.text",
                prompt="",
                text = '다음 나눗셈이 나누어떨어지면 O표,', style_role="question",
                x = 100, y = 55, font_size = 30),
            RectSlot(
                id="slot.expr.box",
                prompt="",
                x = 230, y = 140, width = 190, height = 80),
            TextSlot(
                id="slot.expr.text",
                prompt="",
                text = '28 ÷ 3', style_role="choice",
                x = 280, y = 190, font_size = 30),TextSlot(id = 'slot.q.text.copy2', prompt = '', text = '나누어떨어지지 않으면 X표를 선택하세요.', x = 70, y = 110, font_size = 30, fill = '#111111')),
        diagrams=(),
        groups=(),
        constraints=(),
        tags=("초등", "수학", "나눗셈", "나누어떨어짐", "판단"),
    )


PROBLEM_TEMPLATE = build_problem_template()

SEMANTIC_OVERRIDE = {
    "problem_id": "S3_초등_3_008612",
    "problem_type": "divisibility_judgment",
    "metadata": {
        "language": "ko",
        "question": "28 ÷ 3이 나누어떨어지는지 판단하는 문제",
        "instruction": "나누어떨어지면 O, 나누어떨어지지 않으면 X를 선택한다.",
    },
    "domain": {
        "objects": [
            {"id": "obj.dividend", "type": "number", "value": 28},
            {"id": "obj.divisor", "type": "number", "value": 3},
            {"id": "obj.selected_symbol", "type": "symbol", "value": "X"},
        ],
        "relations": [],
        "problem_solving": {
            "understand": {
                "given_refs": ["obj.dividend", "obj.divisor"],
                "target_ref": "answer.target",
                "condition_refs": ["rel.divisibility"],
            },
            "plan": {
                "method": "division_remainder_check",
                "description": "나눗셈의 나머지가 0인지 확인해 O/X를 판단한다.",
            },
            "execute": {
                "expected_operations": ["divide", "check_remainder", "select_symbol"]
            },
            "review": {"check_methods": ["remainder_zero_check", "symbol_match_check"]},
        },
    },
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {"type": "selection_symbol", "description": "정답 기호"},
        "value": "X",
        "unit": "",
    },
}

SOLVABLE = {
    "schema": "modu.solvable.v1.1",
    "problem_id": "S3_초등_3_008612",
    "problem_type": "divisibility_judgment",
    "inputs": {"target_label": "정답 기호", "unit": "", "target_ticks": 1, "target_count": 1, "total_ticks": 0},
    "given": [
        {"ref": "obj.dividend", "value": 28},
        {"ref": "obj.divisor", "value": 3},
    ],
    "target": {"ref": "answer.target", "type": "selection_symbol"},
    "method": "division_remainder_check",
    "plan": ["28 ÷ 3의 나머지를 확인해 나누어떨어짐 여부를 판단한다."],
    "steps": [
        {"id": "step.1", "expr": "28 ÷ 3", "value": {"quotient": 9, "remainder": 1}},
        {"id": "step.2", "expr": "remainder == 0", "value": False},
        {"id": "step.3", "expr": "선택 기호", "value": "X"},
    ],
    "checks": [
        {"id": "check.1", "expr": "symbol_check", "expected": "X", "actual": "X", "pass": True}
    ],
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {"type": "selection_symbol", "description": "정답 기호"},
        "value": "X",
        "unit": "",
    },
}
