from __future__ import annotations

from modu_math.dsl import Canvas, ProblemTemplate, RectSlot, Region, TextSlot


def build_problem_template() -> ProblemTemplate:
    return ProblemTemplate(
        id="S3_초등_3_008568",
        title="4 × 9 = 36에서 6은 어느 자리에 써야 하는지 기호를 선택하세요.",
        canvas=Canvas(width=786, height=360, coordinate_mode="logical"),
        regions=(
            Region(id="region.top", role="stem", flow="absolute", slot_ids=("slot.qnum", "slot.qtext")),
            Region(id="region.main", role="diagram", flow="absolute", slot_ids=("slot.box", "slot.choice1", "slot.choice2")),
            Region(id="region.note", role="supporting", flow="absolute", slot_ids=("slot.note1", "slot.note2")),
        ),
        slots=(
            TextSlot(id="slot.qnum", prompt="", text="33.", style_role="question", x=24.0, y=24.0, font_size=28),
            TextSlot(id="slot.qtext", prompt="", text="4 × 9 = 36에서 6은 어느 자리에 써야 하는지 기호를 선택하세요.", style_role="question", x=84.0, y=24.0, font_size=24),
            RectSlot(id="slot.box", prompt="", x=210.0, y=84.0, width=520.0, height=110.0),
            TextSlot(id="slot.choice1", prompt="", text="세로셈: 40 × 90", style_role="diagram", x=236.0, y=126.0, font_size=24),
            TextSlot(id="slot.choice2", prompt="", text="선택지: ㄱ, ㄴ, ㄷ, ㄹ", style_role="diagram", x=236.0, y=166.0, font_size=24),
            TextSlot(id="slot.note1", prompt="", text="비교 대상의 계산 결과를 확인합니다.", style_role="supporting", x=24.0, y=266.0, font_size=20),
            TextSlot(id="slot.note2", prompt="", text="조건에 맞는 기호(또는 식)를 선택합니다.", style_role="supporting", x=24.0, y=300.0, font_size=20),
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


