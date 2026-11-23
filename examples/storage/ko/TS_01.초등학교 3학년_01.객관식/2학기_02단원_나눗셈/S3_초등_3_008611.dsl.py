from __future__ import annotations
from modu_math.dsl import Canvas, ProblemTemplate, Region, RectSlot, TextSlot


def build_problem_template() -> ProblemTemplate:
    return ProblemTemplate(
        id="S3_초등_3_008611",
        title="묶이 다른 하나를 찾아 선택하세요",
        canvas=Canvas(width=840.0, height=225.0, coordinate_mode="logical"),
        regions=(
            Region(
                id="region.stem",
                role="stem",
                flow="absolute",
                slot_ids=("slot.q.text",),
            ),
            Region(
                id="region.options",
                role="diagram",
                flow="absolute",
                slot_ids=(
                    "slot.opt1.box",
                    "slot.opt1.text",
                    "slot.opt2.box",
                    "slot.opt2.text",
                    "slot.opt3.box",
                    "slot.opt3.text",
                ),
            ),
            Region(
                id="region.answer_explanation",
                role="supporting",
                flow="absolute",
                slot_ids=(),
            ),
        ),
        slots=(
            TextSlot(
                id="slot.q.text",
                prompt="",
                text = '몫이 다른 하나를 찾아 선택하세요.', style_role="question",
                x=68.0,
                y=28.0,
                font_size=28,
            ),
            RectSlot(
                id="slot.opt1.box",
                prompt="",
                x = 75, y = 70, width = 185, height = 80, fill="#F9DDE0",
                stroke="#F59AA6",
            ),
            TextSlot(
                id="slot.opt1.text",
                prompt="",
                text = '36 ÷ 3', style_role="choice",
                x = 120, y = 120, font_size = 30),
            RectSlot(
                id="slot.opt2.box",
                prompt="",
                x = 295, y = 70, width = 185, height = 80, fill="#FBE6C8",
                stroke="#F5A623",
            ),
            TextSlot(
                id="slot.opt2.text",
                prompt="",
                text = '55 ÷ 5', style_role="choice",
                x = 345, y = 120, font_size = 30),
            RectSlot(
                id="slot.opt3.box",
                prompt="",
                x = 515, y = 70, width = 185, height = 80, fill="#ECF3D8",
                stroke="#A7CF57",
            ),
            TextSlot(
                id="slot.opt3.text",
                prompt="",
                text = '77 ÷ 7', style_role="choice",
                x = 560, y = 120, font_size = 30),
        ),
        diagrams=(),
        groups=(),
        constraints=(),
        tags=(),
    )


PROBLEM_TEMPLATE = build_problem_template()

SEMANTIC_OVERRIDE = {
    "problem_id": "S3_초등_3_008611",
    "problem_type": "multiple_choice_division",
    "metadata": {
        "language": "ko",
        "question": "묶이 다른 하나를 찾아 선택하세요.",
        "instruction": "보기 중 묶이 다른 하나를 고르는 문제",
    },
    "domain": {
        "objects": [
            {"id": "obj.opt1", "type": "division_expression", "expression": "36 ÷ 3"},
            {"id": "obj.opt2", "type": "division_expression", "expression": "55 ÷ 5"},
            {"id": "obj.opt3", "type": "division_expression", "expression": "77 ÷ 7"},
        ],
        "relations": [],
        "problem_solving": {
            "understand": {
                "given_refs": ["obj.opt1", "obj.opt2", "obj.opt3"],
                "target_ref": "answer.target",
                "condition_refs": ["rel.compare_options"],
            },
            "plan": {
                "method": "compare_division_expressions",
                "description": "각 보기의 나눗셈 표현을 비교한다.",
            },
            "execute": {
                "expected_operations": ["evaluate_each_expression", "compare_results"]
            },
            "review": {
                "check_methods": ["compare_with_marked_answer", "result_consistency"]
            },
        },
    },
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {"type": "selected_option", "description": "묶이 다른 하나"},
        "value": 1,
        "unit": "",
    },
}

SOLVABLE = {
    "schema": "modu.solvable.v1.1",
    "problem_id": "S3_초등_3_008611",
    "problem_type": "multiple_choice_division",
    "inputs": {
        "total_ticks": 0,
        "target_label": "묶이 다른 하나",
        "target_ticks": 0,
        "target_count": 1,
        "unit": "",
    },
    "given": [
        {"ref": "obj.opt1", "value": {"expression": "36 ÷ 3"}},
        {"ref": "obj.opt2", "value": {"expression": "55 ÷ 5"}},
        {"ref": "obj.opt3", "value": {"expression": "77 ÷ 7"}},
    ],
    "target": {"ref": "answer.target", "type": "selected_option"},
    "method": "compare_division_expressions",
    "plan": [
        "각 보기의 나눗셈 식을 확인한다.",
        "해설에 적힌 계산 결과를 참고하여 보기들의 묶음 차이를 확인한다.",
    ],
    "steps": [
        {"id": "step.1", "expr": "36 ÷ 3", "value": 12},
        {"id": "step.2", "expr": "55 ÷ 5", "value": 11},
        {"id": "step.3", "expr": "77 ÷ 7", "value": 11},
        {"id": "step.4", "expr": "비교 결과", "value": "36 ÷ 3이 다른 묶이로 표시됨"},
    ],
    "checks": [
        {
            "id": "check.1",
            "expr": "해설에 적힌 결과와 일치하는지 확인",
            "expected": "36 ÷ 3 = 12, 55 ÷ 5 = 11, 77 ÷ 7 = 11",
            "actual": "36 ÷ 3 = 12, 55 ÷ 5 = 11, 77 ÷ 7 = 11",
            "pass": True,
        }
    ],
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {"type": "selected_option", "description": "묶이 다른 하나"},
        "value": 1,
        "unit": "",
    },
}
