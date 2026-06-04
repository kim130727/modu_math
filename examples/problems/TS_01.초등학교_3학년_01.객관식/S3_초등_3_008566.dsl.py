from __future__ import annotations

from modu_math.dsl import Canvas, ProblemTemplate, RectSlot, Region, TextSlot


def build_problem_template() -> ProblemTemplate:
    return ProblemTemplate(
        id="S3_초등_3_008566",
        title="계산 결과가 가장 큰 것을 찾아 기호를 선택해 보세요.",
        canvas=Canvas(width=786, height=360, coordinate_mode="logical"),
        regions=(
            Region(id="region.top", role="stem", flow="absolute", slot_ids=("slot.qnum", "slot.qtext")),
            Region(id="region.main", role="diagram", flow="absolute", slot_ids=("slot.box", "slot.choice1", "slot.choice2")),
            Region(id="region.note", role="supporting", flow="absolute", slot_ids=("slot.note1", "slot.note2")),
        ),
        slots=(
            TextSlot(id="slot.qtext", prompt="", text="계산 결과가 가장 큰 것을 찾아 기호를 선택해 보세요.", style_role="question", x=84.0, y=24.0, font_size=24),
            RectSlot(id="slot.box", prompt="", x = 85, y = 55, width=520.0, height=110.0),
            TextSlot(id="slot.choice1", prompt="", text="ㄱ 23 × 59, ㄴ 61 × 34", style_role="diagram", x = 120, y = 120, font_size=24),
            TextSlot(id="slot.choice2", prompt="", text="ㄷ 82 × 18", style_role="diagram", x = 445, y = 120, font_size=24),
        ),
        diagrams=(),
        groups=(),
        constraints=(),
        tags=(),
    )


PROBLEM_TEMPLATE = build_problem_template()

SEMANTIC_OVERRIDE = {
    "problem_id": "S3_초등_3_008566",
    "problem_type": "선택형 비교",
    "metadata": {"grade": 3, "subject": "수학", "topic": "곱셈 결과 비교"},
    "domain": {
        "objects": [
            {"id": "expr_1", "type": "expression", "text": "ㄱ 23 × 59, ㄴ 61 × 34"},
            {"id": "expr_2", "type": "expression", "text": "ㄷ 82 × 18"},
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
    "problem_id": "S3_초등_3_008566",
    "problem_type": "선택형 비교",
    "inputs": {
        "target_label": "조건에 맞는 항목",
        "unit": "",
        "quantities": {
            "expr_1": "ㄱ 23 × 59, ㄴ 61 × 34",
            "expr_2": "ㄷ 82 × 18",
        },
    },
    "given": [
        {"ref": "expr_1", "value": "ㄱ 23 × 59, ㄴ 61 × 34"},
        {"ref": "expr_2", "value": "ㄷ 82 × 18"},
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

