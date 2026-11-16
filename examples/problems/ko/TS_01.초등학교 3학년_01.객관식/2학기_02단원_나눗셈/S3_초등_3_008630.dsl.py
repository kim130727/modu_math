from __future__ import annotations
from modu_math.dsl import Canvas, ProblemTemplate, RectSlot, Region, TextSlot


def build_problem_template() -> ProblemTemplate:
    return ProblemTemplate(
        id="S3_초등_3_008630",
        title="나머지가 큰 것부터 차례대로 기호를 쓰기",
        canvas=Canvas(width=860, height=400, coordinate_mode="logical"),
        regions=(
            Region(
                id="region.stem",
                role="stem",
                flow="absolute",
                slot_ids=("slot.q_text",),
            ),
            Region(
                id="region.box",
                role="diagram",
                flow="absolute",
                slot_ids=(
                    "slot.box.outer",
                    "slot.box.l1",
                    "slot.box.l2",
                    "slot.box.a1",
                    "slot.box.a2",
                    "slot.box.a3",
                    "slot.box.a4",
                ),
            ),
            Region(
                id="region.options",
                role="choices",
                flow="absolute",
                slot_ids=(
                    "slot.opt1.no",
                    "slot.opt1.text",
                    "slot.opt2.no",
                    "slot.opt2.text",
                    "slot.opt3.no",
                    "slot.opt3.text",
                    "slot.opt4.no",
                    "slot.opt4.text",
                    "slot.opt5.no",
                    "slot.opt5.text",
                ),
            ),
            Region(id="region.answer", role="answer", flow="absolute", slot_ids=()),
            Region(
                id="region.solution",
                role="solution",
                flow="absolute",
                slot_ids=(),
            ),
        ),
        slots=(
            TextSlot(
                id="slot.q_text",
                prompt="",
                text = '나머지가 큰 것부터 차례대로 기호를 쓰세요.', style_role="question",
                x = 25, y = 40, font_size = 30),
            RectSlot(
                id="slot.box.outer",
                prompt="",
                x = 20, y = 60, width = 770, height = 85),
            TextSlot(
                id="slot.box.a1",
                prompt="",
                text = '㉠ 70 ÷ 4', style_role="diagram",
                x = 75, y = 110, font_size = 30),
            TextSlot(
                id="slot.box.a2",
                prompt="",
                text = '㉡ 83 ÷ 5', style_role="diagram",
                x = 265, y = 110, font_size = 30),
            TextSlot(
                id="slot.box.a3",
                prompt="",
                text = '㉢ 89 ÷ 6', style_role="diagram",
                x = 440, y = 110, font_size = 30),
            TextSlot(
                id="slot.box.a4",
                prompt="",
                text = '㉣ 92 ÷ 7', style_role="diagram",
                x = 615, y = 110, font_size = 30),
            TextSlot(
                id="slot.box.l1",
                prompt="",
                text="",
                style_role="diagram",
                x=476.0,
                y=49.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.box.l2",
                prompt="",
                text="",
                style_role="diagram",
                x=476.0,
                y=131.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.opt1.no",
                prompt="",
                text="①",
                style_role="choice",
                x=20.0,
                y=198.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.opt1.text",
                prompt="",
                text="ㄱ, ㄴ, ㄷ, ㄹ",
                style_role="choice",
                x=61.0,
                y=198.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.opt2.no",
                prompt="",
                text="②",
                style_role="choice",
                x=319.0,
                y=198.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.opt2.text",
                prompt="",
                text="ㄴ, ㄱ, ㄷ, ㄹ",
                style_role="choice",
                x=360.0,
                y=198.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.opt3.no",
                prompt="",
                text="③",
                style_role="choice",
                x=622.0,
                y=198.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.opt3.text",
                prompt="",
                text="ㄴ, ㄷ, ㄱ, ㄹ",
                style_role="choice",
                x=663.0,
                y=198.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.opt4.no",
                prompt="",
                text="④",
                style_role="choice",
                x=20.0,
                y=243.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.opt4.text",
                prompt="",
                text="ㄷ, ㄱ, ㄴ, ㄹ",
                style_role="choice",
                x=61.0,
                y=243.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.opt5.no",
                prompt="",
                text="⑤",
                style_role="choice",
                x=319.0,
                y=243.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.opt5.text",
                prompt="",
                text="ㄷ, ㄴ, ㄱ, ㄹ",
                style_role="choice",
                x=360.0,
                y=243.0,
                font_size=28,
            ),
            
        ),
        diagrams=(),
        groups=(),
        constraints=(),
        tags=("초등수학", "나눗셈", "나머지비교", "객관식"),
    )


PROBLEM_TEMPLATE = build_problem_template()

SEMANTIC_OVERRIDE = {
    "problem_id": "S3_초등_3_008630",
    "problem_type": "compare_remainders_ordering",
    "metadata": {
        "language": "ko",
        "question": "나머지가 큰 것부터 차례대로 기호를 쓰는 문제",
        "instruction": "나머지가 큰 것부터 차례대로 기호를 고른다.",
    },
    "domain": {
        "objects": [
            {
                "id": "obj.a",
                "type": "division_expression",
                "symbol": "ㄱ",
                "dividend": 70,
                "divisor": 4,
            },
            {
                "id": "obj.b",
                "type": "division_expression",
                "symbol": "ㄴ",
                "dividend": 83,
                "divisor": 5,
            },
            {
                "id": "obj.c",
                "type": "division_expression",
                "symbol": "ㄷ",
                "dividend": 89,
                "divisor": 6,
            },
            {
                "id": "obj.d",
                "type": "division_expression",
                "symbol": "ㄹ",
                "dividend": 92,
                "divisor": 7,
            },
        ],
        "relations": [],
        "problem_solving": {
            "understand": {
                "given_refs": ["obj.a", "obj.b", "obj.c", "obj.d"],
                "target_ref": "answer.target",
                "condition_refs": ["rel.compare_remainders"],
            },
            "plan": {
                "method": "compare_remainders",
                "description": "각 나눗셈의 나머지를 비교하여 큰 것부터 기호를 나열한다.",
            },
            "execute": {
                "expected_operations": [
                    "compute_remainder_each",
                    "sort_descending_by_remainder",
                    "match_symbol_sequence",
                ]
            },
            "review": {
                "check_methods": [
                    "order_matches_remainders",
                    "choice_consistency_check",
                ]
            },
        },
    },
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {
            "type": "symbol_sequence",
            "description": "나머지가 큰 것부터 차례대로 쓰는 기호의 순서",
        },
        "value": 5,
        "unit": "",
    },
}

SOLVABLE = {
    "schema": "modu.solvable.v1.1",
    "problem_id": "S3_초등_3_008630",
    "problem_type": "compare_remainders_ordering",
    "inputs": {
        "total_ticks": 4,
        "target_label": "기호 순서",
        "target_ticks": 4,
        "target_count": 4,
        "unit": "",
    },
    "given": [
        {"ref": "obj.a", "value": {"symbol": "ㄱ", "dividend": 70, "divisor": 4}},
        {"ref": "obj.b", "value": {"symbol": "ㄴ", "dividend": 83, "divisor": 5}},
        {"ref": "obj.c", "value": {"symbol": "ㄷ", "dividend": 89, "divisor": 6}},
        {"ref": "obj.d", "value": {"symbol": "ㄹ", "dividend": 92, "divisor": 7}},
    ],
    "target": {"ref": "answer.target", "type": "symbol_sequence"},
    "method": "compare_remainders",
    "plan": ["각 나눗셈의 나머지를 구한 뒤 큰 순서대로 기호를 배열한다."],
    "steps": [
        {
            "id": "step.1",
            "expr": "70 ÷ 4 = 17 ... 2",
            "value": {"symbol": "ㄱ", "quotient": 17, "remainder": 2},
        },
        {
            "id": "step.2",
            "expr": "83 ÷ 5 = 16 ... 3",
            "value": {"symbol": "ㄴ", "quotient": 16, "remainder": 3},
        },
        {
            "id": "step.3",
            "expr": "89 ÷ 6 = 14 ... 5",
            "value": {"symbol": "ㄷ", "quotient": 14, "remainder": 5},
        },
        {
            "id": "step.4",
            "expr": "92 ÷ 7 = 13 ... 1",
            "value": {"symbol": "ㄹ", "quotient": 13, "remainder": 1},
        },
        {
            "id": "step.5",
            "expr": "remainder_order_desc",
            "value": ["ㄷ", "ㄴ", "ㄱ", "ㄹ"],
        },
    ],
    "checks": [
        {
            "id": "check.1",
            "expr": "5 > 3 > 2 > 1",
            "expected": True,
            "actual": True,
            "pass": True,
        },
        {
            "id": "check.2",
            "expr": "choice_⑤_matches_sequence",
            "expected": ["ㄷ", "ㄴ", "ㄱ", "ㄹ"],
            "actual": ["ㄷ", "ㄴ", "ㄱ", "ㄹ"],
            "pass": True,
        },
    ],
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {
            "type": "symbol_sequence",
            "description": "나머지가 큰 것부터 차례대로 쓰는 기호의 순서",
        },
        "value": 5,
        "unit": "",
    },
}
