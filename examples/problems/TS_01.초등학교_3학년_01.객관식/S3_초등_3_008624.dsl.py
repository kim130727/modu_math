from __future__ import annotations
from modu_math.dsl import Canvas, ProblemTemplate, Region, RectSlot, TextSlot


def build_problem_template() -> ProblemTemplate:
    return ProblemTemplate(
        id="S3_초등_3_008624",
        title="나머지가 큰 것부터 차례로 기호를 나열한 것을 고르기",
        canvas=Canvas(width=780, height=540, coordinate_mode="logical"),
        regions=(
            Region(
                id="region.stem",
                role="stem",
                flow="absolute",
                slot_ids=(
                    "slot.qnum",
                    "slot.qtext",
                    "slot.box",
                    "slot.div.a",
                    "slot.div.b",
                    "slot.div.c",
                ),
            ),
            Region(
                id="region.choices",
                role="choices",
                flow="absolute",
                slot_ids=("slot.ch1", "slot.ch2", "slot.ch3", "slot.ch4"),
            ),
            Region(id="region.answer", role="answer", flow="absolute", slot_ids=()),
            Region(
                id="region.explanation",
                role="explanation",
                flow="absolute",
                slot_ids=(),
            ),
        ),
        slots=(
            TextSlot(
                id="slot.qnum",
                prompt="",
                text="□ 94.",
                style_role="question",
                x=12.0,
                y=28.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.qtext",
                prompt="",
                text="나머지가 큰 것부터 차례로 기호를 나열한 것을 고르세요.",
                style_role="question",
                x=86.0,
                y=28.0,
                font_size=28,
            ),
            RectSlot(
                id="slot.box",
                x=382.0,
                y=52.0,
                width=208.0,
                height=160.0,
                fill="#E3DDF2",
                stroke="#A79BD5",
                stroke_width=1.5,
                prompt="",
            ),
            TextSlot(
                id="slot.div.a",
                prompt="",
                text="ㄱ 29 ÷ 6",
                style_role="body",
                x=430.0,
                y=96.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.div.b",
                prompt="",
                text="ㄴ 92 ÷ 4",
                style_role="body",
                x=430.0,
                y=136.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.div.c",
                prompt="",
                text="ㄷ 84 ÷ 8",
                style_role="body",
                x=430.0,
                y=176.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.ch1",
                prompt="",
                text="① ㄱ ㄴ ㄷ",
                style_role="body",
                x=18.0,
                y=250.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.ch2",
                prompt="",
                text="② ㄴ ㄷ ㄱ",
                style_role="body",
                x=486.0,
                y=250.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.ch3",
                prompt="",
                text="③ ㄷ ㄱ ㄴ",
                style_role="body",
                x=18.0,
                y=292.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.ch4",
                prompt="",
                text="④ ㄱ ㄷ ㄴ",
                style_role="body",
                x=486.0,
                y=292.0,
                font_size=28,
            ),
        ),
        diagrams=(),
        groups=(),
        constraints=(),
        tags=(),
    )


PROBLEM_TEMPLATE = build_problem_template()

SEMANTIC_OVERRIDE = {
    "problem_id": "S3_초등_3_008624",
    "problem_type": "order_by_remainder",
    "metadata": {
        "language": "ko",
        "question": "나머지가 큰 것부터 차례로 기호를 나열한 것을 고르는 문제",
        "instruction": "나머지가 큰 것부터 차례로 기호를 나열한 것을 고르세요.",
    },
    "domain": {
        "objects": [
            {
                "id": "obj.a",
                "type": "division_expression",
                "symbol": "ㄱ",
                "dividend": 29,
                "divisor": 6,
            },
            {
                "id": "obj.b",
                "type": "division_expression",
                "symbol": "ㄴ",
                "dividend": 92,
                "divisor": 4,
            },
            {
                "id": "obj.c",
                "type": "division_expression",
                "symbol": "ㄷ",
                "dividend": 84,
                "divisor": 8,
            },
        ],
        "relations": [],
        "problem_solving": {
            "understand": {
                "given_refs": ["obj.a", "obj.b", "obj.c"],
                "target_ref": "answer.target",
                "condition_refs": ["rel.compare_remainder"],
            },
            "plan": {
                "method": "compare_remainders",
                "description": "각 나눗셈의 나머지를 비교하여 큰 것부터 순서를 정한다.",
            },
            "execute": {"expected_operations": ["division", "remainder_comparison"]},
            "review": {"check_methods": ["order_consistency_check"]},
        },
    },
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {
            "type": "ordered_symbols",
            "description": "나머지가 큰 것부터 차례로 기호",
        },
        "value": ["ㄱ", "ㄷ", "ㄴ"],
        "unit": "",
    },
}

SOLVABLE = {
    "schema": "modu.solvable.v1.1",
    "problem_id": "S3_초등_3_008624",
    "problem_type": "order_by_remainder",
    "inputs": {
        "total_ticks": 3,
        "target_label": "ordered_symbols",
        "target_ticks": 3,
        "target_count": 3,
        "unit": "",
    },
    "given": [
        {"ref": "obj.a", "value": {"symbol": "ㄱ", "dividend": 29, "divisor": 6}},
        {"ref": "obj.b", "value": {"symbol": "ㄴ", "dividend": 92, "divisor": 4}},
        {"ref": "obj.c", "value": {"symbol": "ㄷ", "dividend": 84, "divisor": 8}},
    ],
    "target": {"ref": "answer.target", "type": "ordered_symbols"},
    "method": "compare_remainders",
    "plan": [
        "각 나눗셈의 나머지를 확인한다.",
        "나머지가 큰 것부터 기호를 순서대로 정한다.",
    ],
    "steps": [
        {"id": "step.1", "expr": "29 ÷ 6", "value": {"quotient": 4, "remainder": 5}},
        {"id": "step.2", "expr": "92 ÷ 4", "value": {"quotient": 23, "remainder": 0}},
        {"id": "step.3", "expr": "84 ÷ 8", "value": {"quotient": 10, "remainder": 4}},
        {"id": "step.4", "expr": "나머지 비교 결과", "value": ["ㄱ", "ㄷ", "ㄴ"]},
    ],
    "checks": [
        {
            "id": "check.1",
            "expr": "5 > 4 > 0",
            "expected": True,
            "actual": True,
            "pass": True,
        },
        {
            "id": "check.2",
            "expr": "순서가 ㄱ, ㄷ, ㄴ인지 확인",
            "expected": ["ㄱ", "ㄷ", "ㄴ"],
            "actual": ["ㄱ", "ㄷ", "ㄴ"],
            "pass": True,
        },
    ],
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {
            "type": "ordered_symbols",
            "description": "나머지가 큰 것부터 차례로 기호",
        },
        "value": ["ㄱ", "ㄷ", "ㄴ"],
        "unit": "",
    },
}
