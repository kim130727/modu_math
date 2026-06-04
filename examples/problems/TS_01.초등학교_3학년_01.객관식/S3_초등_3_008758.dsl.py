from __future__ import annotations
from modu_math.dsl import Canvas, ProblemTemplate, Region, TextSlot, RectSlot


def build_problem_template() -> ProblemTemplate:
    return ProblemTemplate(
        id="S3_초등_3_008758",
        title="주스병의 들이를 어림한 친구를 선택해 보세요",
        canvas=Canvas(width=840.0, height=380.0, coordinate_mode="logical"),
        regions=(
            Region(
                id="region.stem",
                role="stem",
                flow="absolute",
                slot_ids=(
                    "slot.q.square",
                    "slot.q.number",
                    "slot.q.text",
                    "slot.name.jinyoung",
                    "slot.name.chanho",
                    "slot.bubble.top",
                    "slot.bubble.bottom",
                    "slot.top.text",
                    "slot.bottom.text",
                ),
            ),
        ),
        slots=(
            TextSlot(
                id="slot.q.square",
                prompt="",
                text="□",
                style_role="question",
                x=12.0,
                y=26.0,
                font_size=26,
            ),
            TextSlot(
                id="slot.q.number",
                prompt="",
                text="57.",
                style_role="question",
                x=38.0,
                y=26.0,
                font_size=26,
            ),
            TextSlot(
                id="slot.q.text",
                prompt="",
                text="주스병의 들이를 적절히 어림한 친구를 선택해 보세요.",
                style_role="question",
                x=85.0,
                y=26.0,
                font_size=28,
            ),
            RectSlot(
                id="slot.name.jinyoung",
                prompt="",
                x=115.0,
                y=96.0,
                width=62.0,
                height=30.0,
            ),
            RectSlot(
                id="slot.name.chanho",
                prompt="",
                x=745.0,
                y=243.0,
                width=62.0,
                height=30.0,
            ),
            RectSlot(
                id="slot.bubble.top",
                prompt="",
                x=337.0,
                y=62.0,
                width=350.0,
                height=110.0,
            ),
            RectSlot(
                id="slot.bubble.bottom",
                prompt="",
                x=225.0,
                y=200.0,
                width=362.0,
                height=104.0,
            ),
            TextSlot(
                id="slot.top.text",
                prompt="",
                text="주스병에는 200 mL 유우컵으로 4번쯤\n들어갈 것 같아. 들이는 약 800 mL야.",
                style_role="question",
                x=352.0,
                y=96.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.bottom.text",
                prompt="",
                text="주스병은 1 L 유우컵과 들이가\n비슷할 것 같아. 들이는 약 100 mL야.",
                style_role="question",
                x=264.0,
                y=228.0,
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
    "problem_id": "S3_초등_3_008758",
    "problem_type": "choice_estimation_comparison",
    "metadata": {
        "language": "ko",
        "question": "주스병의 들이를 적절히 어림한 친구를 선택해 보세요.",
        "instruction": "보이는 말풍선과 하단 정답/해설 문장을 읽는다.",
    },
    "domain": {
        "objects": [
            {"id": "obj.jinyoung", "type": "student", "name": "진영"},
            {"id": "obj.chanho", "type": "student", "name": "찬호"},
            {"id": "obj.juice_bottle", "type": "container", "description": "주스병"},
            {
                "id": "obj.cup_200ml",
                "type": "cup",
                "capacity": {"value": 200, "unit": "mL"},
            },
            {"id": "obj.cup_1l", "type": "cup", "capacity": {"value": 1, "unit": "L"}},
        ],
        "relations": [],
        "problem_solving": {
            "understand": {
                "given_refs": ["obj.jinyoung", "obj.chanho", "obj.juice_bottle"],
                "target_ref": "answer.target",
                "condition_refs": ["rel.jinyoung_estimate", "rel.chanho_estimate"],
            },
            "plan": {
                "method": "compare_estimates",
                "description": "말풍선의 어림값이 주스병의 들이에 어울리는지 비교한다.",
            },
            "execute": {"expected_operations": ["compare_capacity_estimates"]},
            "review": {"check_methods": ["consistency_with_printed_answer"]},
        },
    },
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {
            "type": "selected_friend",
            "description": "주스병의 들이를 적절히 어림한 친구",
        },
        "value": 0,
        "unit": "",
    },
}

SOLVABLE = {
    "schema": "modu.solvable.v1.1",
    "problem_id": "S3_초등_3_008758",
    "problem_type": "choice_estimation_comparison",
    "inputs": {
        "total_ticks": 0,
        "target_label": "주스병의 들이를 적절히 어림한 친구",
        "target_ticks": 0,
        "target_count": 2,
        "unit": "",
    },
    "given": [
        {"ref": "obj.cup_200ml", "value": {"value": 200, "unit": "mL"}},
        {"ref": "obj.cup_1l", "value": {"value": 1, "unit": "L"}},
        {
            "ref": "rel.jinyoung_estimate",
            "value": {"count": 4, "approx_capacity": {"value": 800, "unit": "mL"}},
        },
        {
            "ref": "rel.chanho_estimate",
            "value": {"approx_capacity": {"value": 100, "unit": "mL"}},
        },
    ],
    "target": {"ref": "answer.target", "type": "selected_friend"},
    "method": "compare_estimates",
    "plan": [
        "두 친구가 말한 어림값이 주스병의 들이에 맞는지 비교한다.",
        "더 타당한 어림값을 말한 친구를 선택한다.",
    ],
    "steps": [
        {"id": "step.1", "expr": "200 mL × 4", "value": 800},
        {"id": "step.2", "expr": "1 L = 1000 mL", "value": 1000},
        {"id": "step.3", "expr": "주스병 들이와 가까운 어림값 비교", "value": "진영"},
    ],
    "checks": [
        {
            "id": "check.1",
            "expr": "800 mL는 200 mL를 4번쯤 더한 값이다",
            "expected": 800,
            "actual": 800,
            "pass": True,
        },
        {
            "id": "check.2",
            "expr": "1 L는 1000 mL이다",
            "expected": 1000,
            "actual": 1000,
            "pass": True,
        },
    ],
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {
            "type": "selected_friend",
            "description": "주스병의 들이를 적절히 어림한 친구",
        },
        "value": 0,
        "unit": "",
    },
}
