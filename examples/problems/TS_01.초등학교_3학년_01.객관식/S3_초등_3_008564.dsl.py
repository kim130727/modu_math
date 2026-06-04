from __future__ import annotations

from modu_math.dsl import Canvas, CircleSlot, LineSlot, ProblemTemplate, RectSlot, Region, TextSlot


def build_problem_template() -> ProblemTemplate:
    return ProblemTemplate(
        id="S3_초등_3_008564",
        title="계산 결과가 더 작은 사람을 선택해 보세요.",
        canvas=Canvas(width=786, height=360, coordinate_mode="logical"),
        regions=(
            Region(id="region.top", role="stem", flow="absolute", slot_ids=("slot.qnum", "slot.qtext")),
            Region(
                id="region.main",
                role="diagram",
                flow="absolute",
                slot_ids=(
                    "slot.box",
                    "slot.left_head",
                    "slot.left_body",
                    "slot.left_leg1",
                    "slot.left_leg2",
                    "slot.right_head",
                    "slot.right_body",
                    "slot.right_leg1",
                    "slot.right_leg2",
                    "slot.choice1",
                    "slot.choice2",
                ),
            ),
            Region(id="region.note", role="supporting", flow="absolute", slot_ids=("slot.note1", "slot.note2")),
        ),
        slots=(
            TextSlot(id="slot.qtext", prompt="", text="계산 결과가 더 작은 사람을 선택해 보세요.", style_role="question", x=84.0, y=24.0, font_size=24),
            RectSlot(id="slot.box", prompt="", x=210.0, y=84.0, width=520.0, height=110.0),
            CircleSlot(id="slot.left_head", prompt="", cx=340.0, cy=56.0, r=17.0, fill="#FFD9B3"),
            RectSlot(id="slot.left_body", prompt="", x=323.0, y=73.0, width=34.0, height=36.0, fill="#F2BE8B"),
            LineSlot(id="slot.left_leg1", prompt="", x1=332.0, y1=109.0, x2=326.0, y2=124.0),
            LineSlot(id="slot.left_leg2", prompt="", x1=348.0, y1=109.0, x2=354.0, y2=124.0),
            CircleSlot(id="slot.right_head", prompt="", cx=600.0, cy=56.0, r=17.0, fill="#FFD9B3"),
            RectSlot(id="slot.right_body", prompt="", x=583.0, y=73.0, width=34.0, height=36.0, fill="#9ED3FF"),
            LineSlot(id="slot.right_leg1", prompt="", x1=592.0, y1=109.0, x2=586.0, y2=124.0),
            LineSlot(id="slot.right_leg2", prompt="", x1=608.0, y1=109.0, x2=614.0, y2=124.0),
            TextSlot(id="slot.choice1", prompt="", text="민재 73 × 28", style_role="diagram", x=236.0, y=126.0, font_size=24),
            TextSlot(id="slot.choice2", prompt="", text="서윤 31 × 65", style_role="diagram", x=236.0, y=166.0, font_size=24),
        ),
        diagrams=(),
        groups=(),
        constraints=(),
        tags=(),
    )


PROBLEM_TEMPLATE = build_problem_template()

SEMANTIC_OVERRIDE = {
    "problem_id": "S3_초등_3_008564",
    "problem_type": "선택형 비교",
    "metadata": {"grade": 3, "subject": "수학", "topic": "곱셈 결과 비교"},
    "domain": {
        "objects": [
            {"id": "expr_1", "type": "expression", "text": "민재 73 × 28"},
            {"id": "expr_2", "type": "expression", "text": "서윤 31 × 65"},
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
        "value": "서윤",
        "unit": "",
    },
}

SOLVABLE = {
    "schema": "modu.solvable.v1.1",
    "problem_id": "S3_초등_3_008564",
    "problem_type": "선택형 비교",
    "inputs": {
        "target_label": "조건에 맞는 항목",
        "unit": "",
        "quantities": {
            "expr_1": "민재 73 × 28",
            "expr_2": "서윤 31 × 65",
        },
    },
    "given": [
        {"ref": "expr_1", "value": "민재 73 × 28"},
        {"ref": "expr_2", "value": "서윤 31 × 65"},
    ],
    "target": {"ref": "answer.target", "type": "selected_option"},
    "method": "compare_and_select",
    "plan": ["조건을 확인한다.", "대상을 비교한다.", "알맞은 답을 선택한다."],
    "steps": [
        {"id": "step.1", "expr": "비교 조건 확인", "value": "완료"},
        {"id": "step.2", "expr": "정답 선택", "value": "서윤"},
    ],
    "checks": [
        {"id": "check.1", "expr": "선택값 존재 여부", "expected": True, "actual": True, "pass": True},
        {"id": "check.2", "expr": "정답 일치", "expected": "서윤", "actual": "서윤", "pass": True},
    ],
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {"type": "selected_option", "description": "조건에 맞는 항목"},
        "value": "서윤",
        "unit": "",
    },
}


