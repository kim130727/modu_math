from __future__ import annotations
from modu_math.dsl import Canvas, ProblemTemplate, RectSlot, Region, TextSlot


def build_problem_template() -> ProblemTemplate:
    return ProblemTemplate(
        id="S3_초등_3_008615",
        title="나머지가 가장 큰 것",
        canvas=Canvas(width=896.0, height=252.0, coordinate_mode="logical"),
        regions=(
            Region(
                id="region.stem",
                role="stem",
                flow="absolute",
                slot_ids=("slot.q_num", "slot.q_text"),
            ),
            Region(
                id="region.options",
                role="content",
                flow="absolute",
                slot_ids=(
                    "slot.opt.1.box",
                    "slot.opt.1.text",
                    "slot.opt.2.box",
                    "slot.opt.2.text",
                    "slot.opt.3.box",
                    "slot.opt.3.text",
                ),
            ),
            Region(id="region.answer", role="answer", flow="absolute", slot_ids=()),
        ),
        slots=(
            TextSlot(
                id="slot.q_num",
                prompt="",
                text="85.",
                style_role="question",
                x=28.0,
                y=28.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.q_text",
                prompt="",
                text="나머지가 가장 큰 것을 찾아 선택하세요.",
                style_role="question",
                x=74.0,
                y=28.0,
                font_size=28,
            ),
            RectSlot(
                id="slot.opt.1.box",
                prompt="",
                x=118.0,
                y=52.0,
                width=188.0,
                height=46.0,
                fill="#FFF7F7",
                stroke="#FFB6B6",
            ),
            TextSlot(
                id="slot.opt.1.text",
                prompt="",
                text="35 ÷ 4",
                style_role="content",
                x=179.0,
                y=83.0,
                font_size=28,
            ),
            RectSlot(
                id="slot.opt.2.box",
                prompt="",
                x=383.0,
                y=52.0,
                width=188.0,
                height=46.0,
                fill="#FFF7F7",
                stroke="#FFB6B6",
            ),
            TextSlot(
                id="slot.opt.2.text",
                prompt="",
                text="20 ÷ 7",
                style_role="content",
                x=445.0,
                y=83.0,
                font_size=28,
            ),
            RectSlot(
                id="slot.opt.3.box",
                prompt="",
                x=652.0,
                y=52.0,
                width=188.0,
                height=46.0,
                fill="#FFF7F7",
                stroke="#FFB6B6",
            ),
            TextSlot(
                id="slot.opt.3.text",
                prompt="",
                text="65 ÷ 9",
                style_role="content",
                x=713.0,
                y=83.0,
                font_size=28,
            ),
        ),
        diagrams=(),
        groups=(),
        constraints=(),
        tags=("나눗셈", "나머지", "비교", "객관식"),
    )


PROBLEM_TEMPLATE = build_problem_template()

SEMANTIC_OVERRIDE = {
    "problem_id": "S3_초등_3_008615",
    "problem_type": "selection_comparison",
    "metadata": {
        "language": "ko",
        "question": "나머지가 가장 큰 것을 찾아 선택하세요.",
        "instruction": "보기 중 나머지가 가장 큰 나눗셈식을 고른다.",
    },
    "domain": {
        "objects": [
            {
                "id": "obj.opt1",
                "type": "division_expression",
                "dividend": 35,
                "divisor": 4,
            },
            {
                "id": "obj.opt2",
                "type": "division_expression",
                "dividend": 20,
                "divisor": 7,
            },
            {
                "id": "obj.opt3",
                "type": "division_expression",
                "dividend": 65,
                "divisor": 9,
            },
        ],
        "relations": [],
    },
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {
            "type": "division_expression",
            "description": "나머지가 가장 큰 보기",
        },
        "value": "20 ÷ 7",
        "unit": "",
    },
}

SOLVABLE = {
    "schema": "modu.solvable.v1.1",
    "problem_id": "S3_초등_3_008615",
    "problem_type": "selection_comparison",
    "inputs": {
        "total_ticks": 3,
        "target_label": "나머지가 가장 큰 것",
        "target_ticks": 1,
        "target_count": 1,
        "unit": "",
    },
    "given": [
        {"ref": "obj.opt1", "value": {"dividend": 35, "divisor": 4}},
        {"ref": "obj.opt2", "value": {"dividend": 20, "divisor": 7}},
        {"ref": "obj.opt3", "value": {"dividend": 65, "divisor": 9}},
    ],
    "target": {"ref": "answer.target", "type": "division_expression"},
    "method": "compare_remainders",
    "plan": ["각 나눗셈식의 나머지를 확인한 뒤, 나머지가 가장 큰 보기를 고른다."],
    "steps": [
        {"id": "step.1", "expr": "35 ÷ 4의 나머지", "value": 3},
        {"id": "step.2", "expr": "20 ÷ 7의 나머지", "value": 6},
        {"id": "step.3", "expr": "65 ÷ 9의 나머지", "value": 2},
        {"id": "step.4", "expr": "6 > 3 > 2", "value": "20 ÷ 7"},
    ],
    "checks": [
        {
            "id": "check.1",
            "expr": "최대 나머지 확인",
            "expected": 6,
            "actual": 6,
            "pass": True,
        },
        {
            "id": "check.2",
            "expr": "선택 보기 일치 확인",
            "expected": "20 ÷ 7",
            "actual": "20 ÷ 7",
            "pass": True,
        },
    ],
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {
            "type": "division_expression",
            "description": "나머지가 가장 큰 보기",
        },
        "value": "20 ÷ 7",
        "unit": "",
    },
}
