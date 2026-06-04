from __future__ import annotations
from modu_math.dsl import Canvas, ProblemTemplate, Region, TextSlot, RectSlot


def build_problem_template() -> ProblemTemplate:
    return ProblemTemplate(
        id="S3_초등_3_008545",
        title="보기와 계산 결과가 같은 것을 선택하세요",
        canvas=Canvas(width=700, height=350, coordinate_mode="logical"),
        regions=(
            Region(
                id="region.stem", role="stem", flow="absolute", slot_ids=("slot.q1",)
            ),
            Region(
                id="region.view_box",
                role="diagram",
                flow="absolute",
                slot_ids=("slot.view_box", "slot.view_label", "slot.view_expr"),
            ),
            Region(
                id="region.choice_box",
                role="diagram",
                flow="absolute",
                slot_ids=("slot.choice_box", "slot.choice_left", "slot.choice_right"),
            ),
            Region(
                id="region.answer_explain",
                role="explanation",
                flow="absolute",
                slot_ids=(
                    
                ),
            ),
        ),
        slots=(
            RectSlot(
                id="slot.view_box",
                prompt="",
                x = 145, y = 50, width=379.0,
                height=117.0,
                fill="#FFFFFF",
                stroke="#9A9A9A",
            ),
            RectSlot(
                id="slot.choice_box",
                prompt="",
                x = 145, y = 180, width=377.0,
                height=79.0,
                fill="#D7DBF2",
                stroke="#D7DBF2",
            ),
            TextSlot(
                id="slot.q1",
                prompt="",
                text="<보기>와 계산 결과가 같은 것을 선택하세요.",
                style_role="question",
                x=13.0,
                y=28.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.view_label",
                prompt="",
                text="<보기>",
                style_role="label",
                x = 220, y = 110, font_size=28,
            ),
            TextSlot(
                id="slot.view_expr",
                prompt="",
                text="789 × 2",
                style_role="equation",
                x = 315, y = 110, font_size=28,
            ),
            TextSlot(
                id="slot.choice_left",
                prompt="",
                text="412 × 4",
                style_role="equation",
                x = 200, y = 230, font_size=28,
            ),
            TextSlot(
                id="slot.choice_right",
                prompt="",
                text="526 × 3",
                style_role="equation",
                x = 365, y = 230, font_size=28,
            ),
            
        ),
        diagrams=(),
        groups=(),
        constraints=(),
        tags=(),
    )


PROBLEM_TEMPLATE = build_problem_template()

SEMANTIC_OVERRIDE = {
    "problem_id": "S3_초등_3_008545",
    "problem_type": "비교_곱셈_선택",
    "metadata": {
        "language": "ko",
        "question": "보기와 계산 결과가 같은 것을 선택하는 문제",
        "instruction": "보기와 계산 결과가 같은 것을 선택하세요.",
    },
    "domain": {
        "objects": [
            {"id": "obj.view_expr", "type": "multiplication", "expression": "789 × 2"},
            {"id": "obj.choice_1", "type": "multiplication", "expression": "412 × 4"},
            {"id": "obj.choice_2", "type": "multiplication", "expression": "526 × 3"},
        ],
        "relations": [],
        "problem_solving": {
            "understand": {
                "given_refs": ["obj.view_expr", "obj.choice_1", "obj.choice_2"],
                "target_ref": "answer.target",
                "condition_refs": ["rel.compare_result"],
            },
            "plan": {
                "method": "compare_calculated_results",
                "description": "보기의 계산 결과와 각 선택지의 계산 결과를 비교한다.",
            },
            "execute": {
                "expected_operations": ["compute_multiplication", "compare_results"]
            },
            "review": {"check_methods": ["match_against_view_result"]},
        },
    },
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {
            "type": "selected_expression",
            "description": "보기와 계산 결과가 같은 식",
        },
        "value": "526 × 3",
        "unit": "",
    },
}

SOLVABLE = {
    "schema": "modu.solvable.v1.1",
    "problem_id": "S3_초등_3_008545",
    "problem_type": "비교_곱셈_선택",
    "inputs": {
        "total_ticks": 0,
        "target_label": "같은 계산 결과를 갖는 식",
        "target_ticks": 0,
        "target_count": 1,
        "unit": "",
    },
    "given": [
        {"ref": "obj.view_expr", "value": {"expression": "789 × 2"}},
        {"ref": "obj.choice_1", "value": {"expression": "412 × 4"}},
        {"ref": "obj.choice_2", "value": {"expression": "526 × 3"}},
    ],
    "target": {"ref": "answer.target", "type": "selected_expression"},
    "method": "compare_calculated_results",
    "plan": [
        "보기의 곱셈 결과를 구한다.",
        "각 선택지의 곱셈 결과를 구한다.",
        "보기와 같은 결과를 가진 식을 찾는다.",
    ],
    "steps": [
        {"id": "step.1", "expr": "789 × 2", "value": 1578},
        {"id": "step.2", "expr": "412 × 4", "value": 1648},
        {"id": "step.3", "expr": "526 × 3", "value": 1578},
        {
            "id": "step.4",
            "expr": "보기와 같은 계산 결과를 가진 식 확인",
            "value": "526 × 3",
        },
    ],
    "checks": [
        {
            "id": "check.1",
            "expr": "789 × 2 == 526 × 3",
            "expected": 1578,
            "actual": 1578,
            "pass": True,
        }
    ],
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {
            "type": "selected_expression",
            "description": "보기와 계산 결과가 같은 식",
        },
        "value": "526 × 3",
        "unit": "",
    },
}
