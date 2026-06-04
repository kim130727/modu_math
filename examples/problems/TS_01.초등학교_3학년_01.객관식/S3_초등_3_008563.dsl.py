from __future__ import annotations

from modu_math.dsl import Canvas, CircleSlot, LineSlot, ProblemTemplate, RectSlot, Region, TextSlot


def build_problem_template() -> ProblemTemplate:
    return ProblemTemplate(
        id="S3_초등_3_008563",
        title="계산 결과가 더 큰 사람을 선택해 보세요.",
        canvas=Canvas(width=786, height=301, coordinate_mode="logical"),
        regions=(
            Region(
                id="region.top",
                role="stem",
                flow="absolute",
                slot_ids=("slot.q_text"),
            ),
            Region(
                id="region.middle",
                role="diagram",
                flow="absolute",
                slot_ids=(
                    "slot.left_head",
                    "slot.left_body",
                    "slot.left_leg1",
                    "slot.left_leg2",
                    "slot.right_head",
                    "slot.right_body",
                    "slot.right_leg1",
                    "slot.right_leg2",
                    "slot.left_card",
                    "slot.right_card",
                    "slot.left_name_box",
                    "slot.right_name_box",
                    "slot.left_name",
                    "slot.right_name",
                    "slot.left_expr",
                    "slot.right_expr",
                ),
            ),
            Region(
                id="region.bottom",
                role="supporting",
                flow="absolute",
                slot_ids=("slot.note1", "slot.note2"),
            ),
        ),
        slots=(
            TextSlot(
                id="slot.q_text",
                prompt="",
                text="계산 결과가 더 큰 사람을 선택해 보세요.",
                style_role="question",
                x=74.0,
                y=20.0,
                font_size=24,
            ),
            RectSlot(id="slot.left_card", prompt="", x=302.0, y=70.0, width=122.0, height=61.0),
            RectSlot(id="slot.right_card", prompt="", x=562.0, y=70.0, width=121.0, height=61.0),
            CircleSlot(id="slot.left_head", prompt="", cx=340.0, cy=56.0, r=17.0, fill="#FFD9B3"),
            RectSlot(id="slot.left_body", prompt="", x=323.0, y=73.0, width=34.0, height=36.0, fill="#9ED3FF"),
            LineSlot(id="slot.left_leg1", prompt="", x1=332.0, y1=109.0, x2=326.0, y2=124.0),
            LineSlot(id="slot.left_leg2", prompt="", x1=348.0, y1=109.0, x2=354.0, y2=124.0),
            CircleSlot(id="slot.right_head", prompt="", cx=600.0, cy=56.0, r=17.0, fill="#FFD9B3"),
            RectSlot(id="slot.right_body", prompt="", x=583.0, y=73.0, width=34.0, height=36.0, fill="#B7E7A1"),
            LineSlot(id="slot.right_leg1", prompt="", x1=592.0, y1=109.0, x2=586.0, y2=124.0),
            LineSlot(id="slot.right_leg2", prompt="", x1=608.0, y1=109.0, x2=614.0, y2=124.0),
            RectSlot(id="slot.left_name_box", prompt="", x=201.0, y=48.0, width=58.0, height=27.0),
            RectSlot(id="slot.right_name_box", prompt="", x=724.0, y=48.0, width=52.0, height=27.0),
            TextSlot(id="slot.left_name", prompt="", text="은우", style_role="diagram", x=210.0, y=67.0, font_size=18),
            TextSlot(id="slot.right_name", prompt="", text="도윤", style_role="diagram", x=732.0, y=67.0, font_size=18),
            TextSlot(id="slot.left_expr", prompt="", text="24 × 42", style_role="diagram", x=330.0, y=104.0, font_size=24),
            TextSlot(id="slot.right_expr", prompt="", text="19 × 78", style_role="diagram", x=588.0, y=104.0, font_size=24),
        ),
        diagrams=(),
        groups=(),
        constraints=(),
        tags=(),
    )


PROBLEM_TEMPLATE = build_problem_template()

SEMANTIC_OVERRIDE = {
    "problem_id": "S3_초등_3_008563",
    "problem_type": "선택형 비교",
    "metadata": {"grade": 3, "subject": "수학", "topic": "곱셈 결과 비교"},
    "domain": {
        "objects": [
            {"id": "expr_1", "type": "multiplication", "text": "24 × 42"},
            {"id": "expr_2", "type": "multiplication", "text": "19 × 78"},
            {"id": "person_1", "type": "person", "text": "은우"},
            {"id": "person_2", "type": "person", "text": "도윤"},
        ],
        "relations": [],
        "problem_solving": {
            "understand": "두 사람의 곱셈식 결과를 비교해 더 큰 사람을 고르는 문제이다.",
            "plan": "각 식의 결과를 확인하고 크기를 비교한다.",
            "execute": "더 큰 결과에 해당하는 사람을 선택한다.",
            "review": "선택 결과가 조건과 일치하는지 확인한다.",
        },
    },
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {"type": "selected_person", "description": "계산 결과가 더 큰 사람"},
        "value": "도윤",
        "unit": "",
    },
}

SOLVABLE = {
    "schema": "modu.solvable.v1.1",
    "problem_id": "S3_초등_3_008563",
    "problem_type": "선택형 비교",
    "inputs": {
        "target_label": "계산 결과가 더 큰 사람",
        "unit": "",
        "quantities": {
            "expr_1": "24 × 42",
            "expr_2": "19 × 78",
            "person_1": "은우",
            "person_2": "도윤",
        },
    },
    "given": [
        {"ref": "expr_1", "value": "24 × 42"},
        {"ref": "expr_2", "value": "19 × 78"},
    ],
    "target": {"ref": "answer.target", "type": "selected_person"},
    "method": "compare_and_select",
    "plan": ["각 식의 값을 계산한다.", "두 값을 비교한다.", "더 큰 값의 사람을 고른다."],
    "steps": [
        {"id": "step.1", "expr": "24 × 42 와 19 × 78 비교", "value": "도윤이 더 큼"},
        {"id": "step.2", "expr": "정답 사람 선택", "value": "도윤"},
    ],
    "checks": [
        {"id": "check.1", "expr": "선택값 존재 여부", "expected": True, "actual": True, "pass": True},
        {"id": "check.2", "expr": "정답 일치", "expected": "도윤", "actual": "도윤", "pass": True},
    ],
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {"type": "selected_person", "description": "계산 결과가 더 큰 사람"},
        "value": "도윤",
        "unit": "",
    },
}
