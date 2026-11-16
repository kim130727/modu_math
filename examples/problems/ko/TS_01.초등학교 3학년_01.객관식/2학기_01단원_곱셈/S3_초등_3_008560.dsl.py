from __future__ import annotations

from modu_math.dsl import (
    Canvas,
    LineSlot,
    ProblemTemplate,
    RectSlot,
    Region,
    TextSlot,
)


def build_problem_template() -> ProblemTemplate:
    return ProblemTemplate(
        id="S3_초등_3_008560",
        title="4를 써야 할 곳을 찾기",
        canvas=Canvas(width=920, height=300, coordinate_mode="logical"),
        regions=(
            Region(
                id="region.stem",
                role="stem",
                flow="absolute",
                slot_ids=("slot.qtext",),
            ),
            Region(
                id="region.box",
                role="diagram",
                flow="absolute",
                slot_ids=(
                    "slot.box.frame",
                    "slot.box.line1",
                    "slot.box.line2",
                    "slot.box.line3",
                    "slot.box.line4",
                    "slot.box.line5",
                    "slot.box.answer1",
                    "slot.box.answer2",
                    "slot.box.answer3",
                    "slot.box.answer4",
                ),
            ),
            Region(
                id="region.answer",
                role="answer",
                flow="absolute",
                slot_ids=(),
            ),
            Region(
                id="region.explain",
                role="explanation",
                flow="absolute",
                slot_ids=(),
            ),
        ),
        slots=(
            TextSlot(
                id="slot.qtext",
                prompt="",
                text="다음 계산에서 3 × 8 = 24의 4를 써야 할 곳을 찾아 기호를 선택하세요.",
                style_role="question",
                x=45,
                y=55,
                font_size=30,
                fill="#111111",
            ),
            RectSlot(
                id="slot.box.frame",
                prompt="",
                x=360,
                y=105,
                width=210,
                height=160,
                fill="#ffffff",
                stroke="#111111",
                stroke_width=1.5,
            ),
            TextSlot(
                id="slot.box.line1",
                prompt="",
                text="3",
                style_role="body",
                x=470,
                y=145,
                font_size=30,
                fill="#111111",
            ),
            TextSlot(
                id="slot.box.line2",
                prompt="",
                text="0",
                style_role="body",
                x=505,
                y=145,
                font_size=30,
                fill="#111111",
            ),
            TextSlot(
                id="slot.box.line3",
                prompt="",
                text="×   8",
                style_role="body",
                x=430,
                y=190,
                font_size=30,
                fill="#111111",
            ),
            TextSlot(
                id="slot.box.line4",
                prompt="",
                text="0",
                style_role="body",
                x=505,
                y=190,
                font_size=30,
                fill="#111111",
            ),
            LineSlot(
                id="slot.box.line5",
                prompt="",
                x1=375,
                y1=205,
                x2=545,
                y2=205,
                stroke="#111111",
                stroke_width=2,
            ),
            TextSlot(
                id="slot.box.answer1",
                prompt="",
                text="㉠",
                style_role="body",
                x=390,
                y=245,
                font_size=30,
                fill="#111111",
            ),
            TextSlot(
                id="slot.box.answer2",
                prompt="",
                text="㉡",
                style_role="body",
                x=425,
                y=245,
                font_size=30,
                fill="#111111",
            ),
            TextSlot(
                id="slot.box.answer3",
                prompt="",
                text="㉢",
                style_role="body",
                x=460,
                y=245,
                font_size=30,
                fill="#111111",
            ),
            TextSlot(
                id="slot.box.answer4",
                prompt="",
                text="㉣",
                style_role="body",
                x=500,
                y=245,
                font_size=30,
                fill="#111111",
            ),
        ),
        diagrams=(),
        groups=(),
        constraints=(),
        tags=(),
    )


PROBLEM_TEMPLATE = build_problem_template()

SEMANTIC_OVERRIDE = {
    "problem_id": "S3_초등_3_008560",
    "problem_type": "선택형_자리값_도식",
    "metadata": {
        "language": "ko",
        "question": "다음 계산에서 3 × 8 = 24의 4를 써야 할 곳을 찾아 기호를 선택하세요.",
        "instruction": "기호를 선택하는 문제",
    },
    "domain": {
        "objects": [
            {
                "id": "obj.expression",
                "type": "multiplication_expression",
                "text": "3 × 8 = 24",
            },
            {
                "id": "obj.choice_symbols",
                "type": "choice_symbols",
                "symbols": ["ㄱ", "ㄴ", "ㄷ", "ㄹ"],
            },
            {"id": "obj.vertical_form", "type": "place_value_diagram"},
        ],
        "relations": [],
        "problem_solving": {
            "understand": {
                "given_refs": [
                    "obj.expression",
                    "obj.choice_symbols",
                    "obj.vertical_form",
                ],
                "target_ref": "answer.target",
                "condition_refs": ["rel.choice_to_position"],
            },
            "plan": {
                "method": "choice_selection",
                "description": "보이는 자리값 도식에서 4를 써야 하는 위치를 고른다.",
            },
            "execute": {"expected_operations": ["identify_position", "match_symbol"]},
            "review": {"check_methods": ["symbol_match_check"]},
        },
    },
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {
            "type": "selected_symbol",
            "description": "4를 써야 할 곳에 해당하는 기호",
        },
        "value": "ㄴ",
        "unit": "",
    },
}

SOLVABLE = {
    "schema": "modu.solvable.v1.1",
    "problem_id": "S3_초등_3_008560",
    "problem_type": "선택형_자리값_도식",
    "inputs": {
        "total_ticks": 4,
        "target_label": "4를 써야 할 곳",
        "target_ticks": 1,
        "target_count": 1,
        "unit": "",
    },
    "given": [
        {"ref": "obj.expression", "value": "3 × 8 = 24"},
        {"ref": "obj.choice_symbols", "value": ["ㄱ", "ㄴ", "ㄷ", "ㄹ"]},
    ],
    "target": {"ref": "answer.target", "type": "selected_symbol"},
    "method": "choice_selection",
    "plan": [
        "보이는 도식에서 4가 들어갈 위치를 확인한다.",
        "보기 기호와 위치를 대응시킨다.",
    ],
    "steps": [
        {"id": "step.1", "expr": "선택지 확인", "value": ["ㄱ", "ㄴ", "ㄷ", "ㄹ"]},
        {"id": "step.2", "expr": "자리 대응 확인", "value": "TODO"},
        {"id": "step.3", "expr": "정답 기호 선택", "value": "ㄴ"},
    ],
    "checks": [
        {
            "id": "check.1",
            "expr": "선택된 기호가 보기 안에 있는가",
            "expected": True,
            "actual": True,
            "pass": True,
        },
        {
            "id": "check.2",
            "expr": "해설 영역의 기호 배치와 일치하는가",
            "expected": True,
            "actual": True,
            "pass": True,
        },
    ],
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {
            "type": "selected_symbol",
            "description": "4를 써야 할 곳에 해당하는 기호",
        },
        "value": "ㄴ",
        "unit": "",
    },
}
