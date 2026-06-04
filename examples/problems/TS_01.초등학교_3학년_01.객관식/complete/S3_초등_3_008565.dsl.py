from __future__ import annotations

from modu_math.dsl import Canvas, CircleSlot, ProblemTemplate, RectSlot, Region, TextSlot


def build_problem_template() -> ProblemTemplate:
    return ProblemTemplate(
        id="S3_초등_3_008565",
        title="계산 결과가 2000보다 큰 곱셈식을 선택해 보세요.",
        canvas=Canvas(width=786, height=360, coordinate_mode="logical"),
        regions=(
            Region(id="region.top", role="stem", flow="absolute", slot_ids=("slot.qtext")),
            Region(
                id="region.main",
                role="diagram",
                flow="absolute",
                slot_ids=(
                    "slot.cloud1.core",
                    "slot.cloud1.bump1",
                    "slot.cloud1.bump2",
                    "slot.cloud1.text",
                    "slot.cloud2.core",
                    "slot.cloud2.bump1",
                    "slot.cloud2.bump2",
                    "slot.cloud2.text",
                    "slot.cloud3.core",
                    "slot.cloud3.bump1",
                    "slot.cloud3.bump2",
                    "slot.cloud3.text",
                    "slot.cloud4.core",
                    "slot.cloud4.bump1",
                    "slot.cloud4.bump2",
                    "slot.cloud4.text",
                ),
            ),
            Region(id="region.note", role="supporting", flow="absolute", slot_ids=("slot.note1", "slot.note2")),
        ),
        slots=(
            TextSlot(id="slot.qtext", prompt="", text = '계산 결과가 2000보다 큰 곱셈식을 선택해 보세요.', style_role="question", x = 100, y = 40, font_size = 25),
            RectSlot(id="slot.cloud1.core", prompt="", x = 235, y = 70, width = 120, height = 50, rx=20.0, ry=20.0),
            TextSlot(id="slot.cloud1.text", prompt="", text = '19 × 90', style_role="diagram", x = 255, y = 100, font_size = 20),
            RectSlot(id="slot.cloud2.core", prompt="", x = 370, y = 70, width = 120, height = 50, rx=20.0, ry=20.0),
            TextSlot(id="slot.cloud2.text", prompt="", text = '20 × 70', style_role="diagram", x = 390, y = 100, font_size = 20),
            RectSlot(id="slot.cloud3.core", prompt="", x = 240, y = 140, width = 120, height = 50, rx=20.0, ry=20.0),
            TextSlot(id="slot.cloud3.text", prompt="", text = '40 × 50', style_role="diagram", x = 260, y = 170, font_size = 20),
            RectSlot(id="slot.cloud4.core", prompt="", x = 370, y = 140, width = 120, height = 50, rx=20.0, ry=20.0),
            TextSlot(id="slot.cloud4.text", prompt="", text = '36 × 60', style_role="diagram", x = 390, y = 170, font_size = 20),
        ),
        diagrams=(),
        groups=(),
        constraints=(),
        tags=(),
    )


PROBLEM_TEMPLATE = build_problem_template()

SEMANTIC_OVERRIDE = {
    "problem_id": "S3_초등_3_008565",
    "problem_type": "선택형 비교",
    "metadata": {"grade": 3, "subject": "수학", "topic": "곱셈 결과 비교"},
    "domain": {
        "objects": [
            {"id": "expr_1", "type": "expression", "text": "19 × 90, 20 × 70"},
            {"id": "expr_2", "type": "expression", "text": "40 × 50, 36 × 60"},
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
        "value": "36 × 60",
        "unit": "",
    },
}

SOLVABLE = {
    "schema": "modu.solvable.v1.1",
    "problem_id": "S3_초등_3_008565",
    "problem_type": "선택형 비교",
    "inputs": {
        "target_label": "조건에 맞는 항목",
        "unit": "",
        "quantities": {
            "expr_1": "19 × 90, 20 × 70",
            "expr_2": "40 × 50, 36 × 60",
        },
    },
    "given": [
        {"ref": "expr_1", "value": "19 × 90, 20 × 70"},
        {"ref": "expr_2", "value": "40 × 50, 36 × 60"},
    ],
    "target": {"ref": "answer.target", "type": "selected_option"},
    "method": "compare_and_select",
    "plan": ["조건을 확인한다.", "대상을 비교한다.", "알맞은 답을 선택한다."],
    "steps": [
        {"id": "step.1", "expr": "비교 조건 확인", "value": "완료"},
        {"id": "step.2", "expr": "정답 선택", "value": "36 × 60"},
    ],
    "checks": [
        {"id": "check.1", "expr": "선택값 존재 여부", "expected": True, "actual": True, "pass": True},
        {"id": "check.2", "expr": "정답 일치", "expected": "36 × 60", "actual": "36 × 60", "pass": True},
    ],
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {"type": "selected_option", "description": "조건에 맞는 항목"},
        "value": "36 × 60",
        "unit": "",
    },
}

