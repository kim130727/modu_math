from __future__ import annotations
from modu_math.dsl import Canvas, ProblemTemplate, Region, RectSlot, TextSlot


def build_problem_template() -> ProblemTemplate:
    return ProblemTemplate(
        id="S3_초등_3_008618",
        title="묶이 가장 큰 나눗셈을 말한 사람을 선택해 보세요.",
        canvas=Canvas(width=886.0, height=430.0, coordinate_mode="logical"),
        regions=(
            Region(
                id="region.stem",
                role="stem",
                flow="absolute",
                slot_ids=("slot.qnum", "slot.qtext"),
            ),
            Region(
                id="region.diagram",
                role="diagram",
                flow="absolute",
                slot_ids=(
                    "slot.bubble.left",
                    "slot.bubble.mid",
                    "slot.bubble.right",
                    "slot.face.left",
                    "slot.face.mid",
                    "slot.face.right",
                    "slot.name.left",
                    "slot.name.mid",
                    "slot.name.right",
                ),
            ),
            Region(id="region.answer", role="answer", flow="absolute", slot_ids=()),
        ),
        slots=(
            RectSlot(
                id="slot.check", prompt="", x=17.0, y=18.0, width=12.0, height=12.0
            ),
            TextSlot(
                id="slot.qnum",
                prompt="",
                text="88.",
                style_role="question",
                x=40.0,
                y=30.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.qtext",
                prompt="",
                text="묶이 가장 큰 나눗셈을 말한 사람을 선택해 보세요.",
                style_role="question",
                x=84.0,
                y=30.0,
                font_size=28,
            ),
            RectSlot(
                id="slot.bubble.left",
                prompt="",
                x=113.0,
                y=52.0,
                width=196.0,
                height=52.0,
            ),
            RectSlot(
                id="slot.bubble.mid",
                prompt="",
                x=355.0,
                y=52.0,
                width=188.0,
                height=52.0,
            ),
            RectSlot(
                id="slot.bubble.right",
                prompt="",
                x=588.0,
                y=52.0,
                width=188.0,
                height=52.0,
            ),
            TextSlot(
                id="slot.face.left",
                prompt="",
                text="인물",
                style_role="body",
                x=167.0,
                y=175.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.face.mid",
                prompt="",
                text="인물",
                style_role="body",
                x=408.0,
                y=175.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.face.right",
                prompt="",
                text="인물",
                style_role="body",
                x=650.0,
                y=175.0,
                font_size=28,
            ),
            RectSlot(
                id="slot.name.left",
                prompt="",
                x=174.0,
                y=247.0,
                width=67.0,
                height=33.0,
            ),
            RectSlot(
                id="slot.name.mid", prompt="", x=416.0, y=247.0, width=67.0, height=33.0
            ),
            RectSlot(
                id="slot.name.right",
                prompt="",
                x=649.0,
                y=247.0,
                width=67.0,
                height=33.0,
            ),
            TextSlot(
                id="slot.name_text.left",
                prompt="",
                text="소진",
                style_role="label",
                x=191.0,
                y=269.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.name_text.mid",
                prompt="",
                text="경수",
                style_role="label",
                x=434.0,
                y=269.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.name_text.right",
                prompt="",
                text="태희",
                style_role="label",
                x=667.0,
                y=269.0,
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
    "problem_id": "S3_초등_3_008618",
    "problem_type": "compare_division_results",
    "metadata": {
        "language": "ko",
        "question": "묶이 가장 큰 나눗셈을 말한 사람을 선택해 보세요.",
        "instruction": "세 나눗셈의 결과를 비교하여 가장 큰 값을 말한 사람을 찾는다.",
    },
    "domain": {
        "objects": [
            {"id": "obj.sojin", "type": "person", "name": "소진"},
            {"id": "obj.gyeongsu", "type": "person", "name": "경수"},
            {"id": "obj.taehee", "type": "person", "name": "태희"},
            {"id": "obj.expr1", "type": "division_expression", "expression": "262 ÷ 2"},
            {"id": "obj.expr2", "type": "division_expression", "expression": "440 ÷ 5"},
            {"id": "obj.expr3", "type": "division_expression", "expression": "552 ÷ 6"},
        ],
        "relations": [],
    },
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {
            "type": "person_name",
            "description": "가장 큰 나눗셈 결과를 말한 사람",
        },
        "value": "소진",
        "unit": "",
    },
}

SOLVABLE = {
    "schema": "modu.solvable.v1.1",
    "problem_id": "S3_초등_3_008618",
    "problem_type": "compare_division_results",
    "inputs": {
        "total_ticks": 3,
        "target_label": "가장 큰 나눗셈을 말한 사람",
        "target_ticks": 1,
        "target_count": 1,
        "unit": "",
    },
    "given": [
        {
            "ref": "obj.expr1",
            "value": {"expression": "262 ÷ 2", "left": 262, "right": 2},
        },
        {
            "ref": "obj.expr2",
            "value": {"expression": "440 ÷ 5", "left": 440, "right": 5},
        },
        {
            "ref": "obj.expr3",
            "value": {"expression": "552 ÷ 6", "left": 552, "right": 6},
        },
    ],
    "target": {"ref": "answer.target", "type": "person_name"},
    "method": "compare_division_results",
    "plan": [
        "각 나눗셈의 결과를 계산한다.",
        "세 결과 중 가장 큰 값을 찾는다.",
        "그 값을 말한 사람을 고른다.",
    ],
    "steps": [
        {"id": "step.1", "expr": "262 ÷ 2", "value": 131},
        {"id": "step.2", "expr": "440 ÷ 5", "value": 88},
        {"id": "step.3", "expr": "552 ÷ 6", "value": 92},
        {"id": "step.4", "expr": "max(131, 88, 92)", "value": 131},
        {"id": "step.5", "expr": "가장 큰 결과를 말한 사람 찾기", "value": "소진"},
    ],
    "checks": [
        {
            "id": "check.1",
            "expr": "131 > 92 > 88",
            "expected": True,
            "actual": True,
            "pass": True,
        },
        {
            "id": "check.2",
            "expr": "max(131, 88, 92) == 131",
            "expected": 131,
            "actual": 131,
            "pass": True,
        },
    ],
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {
            "type": "person_name",
            "description": "가장 큰 나눗셈 결과를 말한 사람",
        },
        "value": "소진",
        "unit": "",
    },
}
