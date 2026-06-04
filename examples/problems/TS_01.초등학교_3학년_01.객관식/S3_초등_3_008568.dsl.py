from __future__ import annotations

from modu_math.dsl import Canvas, ProblemTemplate, RectSlot, Region, TextSlot,LineSlot

def build_problem_template() -> ProblemTemplate:
    return ProblemTemplate(
        id="S3_초등_3_008568",
        title="6의 자리를 찾기",
        canvas=Canvas(width=920, height=470, coordinate_mode="logical"),
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
                text="곱셈을 계산할 때 4 × 9 = 36의 6은 어느 자리에 써야 하는지\n 기호를 선택하세요.",
                style_role="question",
                x=45,
                y=55,
                font_size=30,
            ),
            RectSlot(
                id="slot.box.frame",
                prompt="",
                x = 285, y = 145, width = 210, height = 160),
            TextSlot(
                id="slot.box.line1",
                prompt="",
                text = '4', style_role="body",
                x = 395, y = 185, font_size = 30),
            TextSlot(
                id="slot.box.line2",
                prompt="",
                text = '0', style_role="body",
                x = 430, y = 185, font_size = 30),
            TextSlot(
                id="slot.box.line3",
                prompt="",
                text = '×   9', style_role="body",
                x = 355, y = 230, font_size = 30),
            TextSlot(
                id="slot.box.line4",
                prompt="",
                text = '0', style_role="body",
                x = 430, y = 230, font_size = 30),
            LineSlot(
                id="slot.box.line5",
                prompt="",
                x1 = 300, y1 = 245, x2 = 470, y2 = 245),
            TextSlot(
                id="slot.box.answer1",
                prompt="",
                text = '㉠', style_role="body",
                x = 315, y = 285, font_size = 30),
            TextSlot(
                id="slot.box.answer2",
                prompt="",
                text = '㉡', style_role="body",
                x = 350, y = 285, font_size = 30),
            TextSlot(
                id="slot.box.answer3",
                prompt="",
                text = '㉢', style_role="body",
                x = 385, y = 285, font_size = 30),
            TextSlot(
                id="slot.box.answer4",
                prompt="",
                text = '㉣', style_role="body",
                x = 425, y = 285, font_size = 30),
        ),
        diagrams=(),
        groups=(),
        constraints=(),
        tags=(),
    )

PROBLEM_TEMPLATE = build_problem_template()

SEMANTIC_OVERRIDE = {
    "problem_id": "S3_초등_3_008568",
    "problem_type": "선택형 비교",
    "metadata": {"grade": 3, "subject": "수학", "topic": "곱셈 결과 비교"},
    "domain": {
        "objects": [
            {"id": "expr_1", "type": "expression", "text": "세로셈: 40 × 90"},
            {"id": "expr_2", "type": "expression", "text": "선택지: ㄱ, ㄴ, ㄷ, ㄹ"},
        ],
        "relations": [],
        "problem_solving": {
            "understand": "비교 대상을 읽고 조건에 맞는 항목을 고르는 문제이다.",
            "plan": "각 대상을 비교 가능한 값으로 확인한 뒤 크기를 판단한다.",
            "execute": "조건에 맞는 항목을 선택한다.",
            "review": "선택한 답이 조건과 일치하는지 확인한다.",
        },
    },
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {"type": "selected_option", "description": "조건에 맞는 항목"},
        "value": "ㄴ",
        "unit": "",
    },
}

SOLVABLE = {
    "schema": "modu.solvable.v1.1",
    "problem_id": "S3_초등_3_008568",
    "problem_type": "선택형 비교",
    "inputs": {
        "target_label": "조건에 맞는 항목",
        "unit": "",
        "quantities": {
            "expr_1": "세로셈: 40 × 90",
            "expr_2": "선택지: ㄱ, ㄴ, ㄷ, ㄹ",
        },
    },
    "given": [
        {"ref": "expr_1", "value": "세로셈: 40 × 90"},
        {"ref": "expr_2", "value": "선택지: ㄱ, ㄴ, ㄷ, ㄹ"},
    ],
    "target": {"ref": "answer.target", "type": "selected_option"},
    "method": "compare_and_select",
    "plan": ["조건을 확인한다.", "대상을 비교한다.", "알맞은 답을 선택한다."],
    "steps": [
        {"id": "step.1", "expr": "비교 조건 확인", "value": "완료"},
        {"id": "step.2", "expr": "정답 선택", "value": "ㄴ"},
    ],
    "checks": [
        {"id": "check.1", "expr": "선택값 존재 여부", "expected": True, "actual": True, "pass": True},
        {"id": "check.2", "expr": "정답 일치", "expected": "ㄴ", "actual": "ㄴ", "pass": True},
    ],
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {"type": "selected_option", "description": "조건에 맞는 항목"},
        "value": "ㄴ",
        "unit": "",
    },
}


