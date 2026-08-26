from __future__ import annotations
from modu_math.dsl import Canvas, ProblemTemplate, RectSlot, Region, TextSlot


def build_problem_template() -> ProblemTemplate:
    return ProblemTemplate(
        id="S3_초등_3_008610",
        title="바르게 계산한 것을 찾아 기호를 선택해 보세요.",
        canvas=Canvas(width=880, height=340, coordinate_mode="logical"),
        regions=(
            Region(
                id="region.stem",
                role="stem",
                flow="absolute",
                slot_ids=("slot.q.text",),
            ),
            Region(
                id="region.choices",
                role="choices",
                flow="absolute",
                slot_ids=(
                    "slot.choice.box",
                    "slot.choice.1.symbol",
                    "slot.choice.1.expr",
                    "slot.choice.2.symbol",
                    "slot.choice.2.expr",
                ),
            ),
            Region(
                id="region.explanation",
                role="explanation",
                flow="absolute",
                slot_ids=(),
            ),
        ),
        slots=(
            TextSlot(
                id="slot.q.text",
                prompt="",
                text="바르게 계산한 것을 찾아 기호를 선택해 보세요.",
                style_role="question",
                x=66.0,
                y=30.0,
                font_size=28,
            ),
            RectSlot(
                id="slot.choice.box",
                prompt="",
                x = 65, y = 75, width = 675, height = 80),
            TextSlot(
                id="slot.choice.1.symbol",
                prompt="",
                text = '㉠', style_role="choice",
                x = 127, y = 125, font_size = 30, max_width = 750),
            TextSlot(
                id="slot.choice.1.expr",
                prompt="",
                text = '54 ÷ 3 = 17', style_role="choice",
                x = 167, y = 125, font_size = 30, max_width = 750),
            TextSlot(
                id="slot.choice.2.symbol",
                prompt="",
                text = '㉡', style_role="choice",
                x = 470, y = 125, font_size = 30, max_width = 750),
            TextSlot(
                id="slot.choice.2.expr",
                prompt="",
                text = '96 ÷ 8 = 12', style_role="choice",
                x = 515, y = 125, font_size = 30, max_width = 750),
            
        ),
        diagrams=(),
        groups=(),
        constraints=(),
        tags=("초등", "수학", "나눗셈", "계산", "선택형"),
    )


PROBLEM_TEMPLATE = build_problem_template()

SEMANTIC_OVERRIDE = {
    "problem_id": "S3_초등_3_008610",
    "problem_type": "multiple_choice_calculation_check",
    "metadata": {
        "language": "ko",
        "question": "바르게 계산한 것을 찾아 기호를 선택해 보세요.",
        "instruction": "보기 중 바르게 계산한 식의 기호를 고르세요.",
    },
    "domain": {
        "objects": [
            {"id": "obj.choice.1", "type": "expression", "symbol": "㉠", "text": "54 ÷ 3 = 17"},
            {"id": "obj.choice.2", "type": "expression", "symbol": "㉡", "text": "96 ÷ 8 = 12"},
            {"id": "obj.ref.correct", "type": "expression", "text": "54 ÷ 3 = 18"},
        ],
        "relations": [],
        "problem_solving": {
            "understand": {
                "given_refs": ["obj.choice.1", "obj.choice.2", "obj.ref.correct"],
                "target_ref": "answer.target",
                "condition_refs": ["rel.pick_correct_calculation"],
            },
            "plan": {
                "method": "compare_calculation_results",
                "description": "각 보기의 계산 결과를 실제 계산과 비교해 바른 식의 기호를 고른다.",
            },
            "execute": {
                "expected_operations": ["check_choice_1", "check_choice_2", "select_correct_symbol"]
            },
            "review": {"check_methods": ["recalculation_check", "answer_symbol_check"]},
        },
    },
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {"type": "symbol", "description": "바르게 계산한 식의 기호"},
        "value": "㉡",
        "unit": "",
    },
}

SOLVABLE = {
    "schema": "modu.solvable.v1.1",
    "problem_id": "S3_초등_3_008610",
    "problem_type": "multiple_choice_calculation_check",
    "inputs": {"target_label": "바르게 계산한 식의 기호", "unit": "", "target_ticks": 0, "target_count": 1, "total_ticks": 0},
    "given": [
        {"ref": "obj.choice.1", "value": {"symbol": "㉠", "text": "54 ÷ 3 = 17"}},
        {"ref": "obj.choice.2", "value": {"symbol": "㉡", "text": "96 ÷ 8 = 12"}},
        {"ref": "obj.ref.correct", "value": {"text": "54 ÷ 3 = 18"}},
    ],
    "target": {"ref": "answer.target", "type": "symbol"},
    "method": "compare_calculation_results",
    "plan": ["각 보기의 계산이 맞는지 확인하고 바른 식의 기호를 선택한다."],
    "steps": [
        {"id": "step.1", "expr": "54 ÷ 3 = 18", "value": False},
        {"id": "step.2", "expr": "96 ÷ 8 = 12", "value": True},
        {"id": "step.3", "expr": "선택한 기호", "value": "㉡"},
    ],
    "checks": [
        {"id": "check.1", "expr": "selected_symbol_check", "expected": "㉡", "actual": "㉡", "pass": True}
    ],
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {"type": "symbol", "description": "바르게 계산한 식의 기호"},
        "value": "㉡",
        "unit": "",
    },
}
