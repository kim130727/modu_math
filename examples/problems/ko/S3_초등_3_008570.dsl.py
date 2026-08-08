from __future__ import annotations

from modu_math.dsl import Canvas, ProblemTemplate, RectSlot, Region, TextSlot


def build_problem_template() -> ProblemTemplate:
    return ProblemTemplate(
        id="S3_초등_3_008570",
        title="계산 결과가 가장 큰 것의 기호를 선택하세요.",
        canvas=Canvas(width=786, height=360, coordinate_mode="logical"),
        regions=(
            Region(id="region.top", role="stem", flow="absolute", slot_ids=("slot.qtext",)),
            Region(
                id="region.main",
                role="diagram",
                flow="absolute",
                slot_ids=("slot.box", "slot.choice1", "slot.choice2", "slot.choice3"),
            ),
            Region(id="region.note", role="supporting", flow="absolute", slot_ids=()),
        ),
        slots=(
            TextSlot(
                id="slot.qtext",
                prompt="",
                text="계산 결과가 가장 큰 것의 기호를 선택하세요.",
                style_role="question",
                x=155.018,
                y=93,
                font_size=28,
                fill="#111111",
            ),
            RectSlot(
                id="slot.box",
                prompt="",
                x=121.022,
                y=137,
                width=520,
                height=110,
                fill="#ffffff",
                stroke="#111111",
                stroke_width=1.5,
            ),
            TextSlot(
                id="slot.choice1",
                prompt="",
                text="㉠ 512 × 3",
                style_role="diagram",
                x=156.022,
                y=210,
                font_size=28,
                fill="#111111",
            ),
            TextSlot(
                id="slot.choice2",
                prompt="",
                text="㉡ 35 × 29",
                x=306.022,
                y=210,
                font_size=28,
                fill="#111111",
            ),
            TextSlot(
                id="slot.choice3",
                prompt="",
                text="㉢ 16 × 90",
                style_role="diagram",
                x=464.025,
                y=211,
                font_size=28,
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
    "problem_id": "S3_초등_3_008570",
    "problem_type": "선택형 비교",
    "metadata": {"grade": 3, "subject": "수학", "topic": "곱셈 결과 비교"},
    "domain": {
        "objects": [
            {"id": "expr_1", "type": "expression", "text": "ㄱ 512 × 3"},
            {"id": "expr_2", "type": "expression", "text": "ㄴ 35 × 29"},
            {"id": "expr_3", "type": "expression", "text": "ㄷ 16 × 90"},
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
        "value": "ㄱ",
        "unit": "",
    },
}

SOLVABLE = {
    "schema": "modu.solvable.v1.1",
    "problem_id": "S3_초등_3_008570",
    "problem_type": "선택형 비교",
    "inputs": {
        "target_label": "조건에 맞는 항목",
        "unit": "",
        "quantities": {
            "expr_1": "ㄱ 512 × 3",
            "expr_2": "ㄴ 35 × 29",
            "expr_3": "ㄷ 16 × 90",
        },
    },
    "given": [
        {"ref": "expr_1", "value": "ㄱ 512 × 3"},
        {"ref": "expr_2", "value": "ㄴ 35 × 29"},
        {"ref": "expr_3", "value": "ㄷ 16 × 90"},
    ],
    "target": {"ref": "answer.target", "type": "selected_option"},
    "method": "compare_and_select",
    "plan": ["조건을 확인한다.", "대상을 비교한다.", "알맞은 답을 선택한다."],
    "steps": [
        {"id": "step.1", "expr": "비교 조건 확인", "value": "완료"},
        {"id": "step.2", "expr": "정답 선택", "value": "ㄱ"},
    ],
    "checks": [
        {
            "id": "check.1",
            "expr": "선택값 존재 여부",
            "expected": True,
            "actual": True,
            "pass": True,
        },
        {"id": "check.2", "expr": "정답 일치", "expected": "ㄱ", "actual": "ㄱ", "pass": True},
    ],
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {"type": "selected_option", "description": "조건에 맞는 항목"},
        "value": "ㄱ",
        "unit": "",
    },
}
