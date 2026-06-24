from __future__ import annotations
from modu_math.dsl import Canvas, ProblemTemplate, Region, TextSlot, PolygonSlot


def build_problem_template() -> ProblemTemplate:
    return ProblemTemplate(
        id="S3_초등_3_009027",
        title="삼각형을 보고 알맞은 기호를 모두 선택하세요.",
        canvas=Canvas(width=720, height=233, coordinate_mode="logical"),
        regions=(
            Region(
                id="region.header",
                role="stem",
                flow="absolute",
                slot_ids=("slot.num", "slot.title"),
            ),
            Region(
                id="region.diagram",
                role="diagram",
                flow="absolute",
                slot_ids=(
                    "slot.lb.ga",
                    "slot.lb.na",
                    "slot.lb.da",
                    "slot.lb.ra",
                    "slot.tri.ga",
                    "slot.tri.na",
                    "slot.tri.da",
                    "slot.tri.ra",
                ),
            ),
            Region(
                id="region.body",
                role="stem",
                flow="absolute",
                slot_ids=("slot.line1", "slot.line2", "slot.line3"),
            ),
        ),
        slots=(
            TextSlot(
                id="slot.num",
                prompt="",
                text="64.",
                style_role="question",
                x=18.0,
                y=24.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.title",
                prompt="",
                text="삼각형을 보고 알맞은 기호를 모두 선택하세요.",
                style_role="question",
                x=58.0,
                y=24.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.lb.ga",
                prompt="",
                text="가",
                style_role="label",
                x=96.0,
                y=56.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.lb.na",
                prompt="",
                text="나",
                style_role="label",
                x=254.0,
                y=56.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.lb.da",
                prompt="",
                text="다",
                style_role="label",
                x=430.0,
                y=56.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.lb.ra",
                prompt="",
                text="라",
                style_role="label",
                x=600.0,
                y=56.0,
                font_size=28,
            ),
            PolygonSlot(
                id="slot.tri.ga", prompt="", points=((110.0, 110.0), (165.0, 40.0), (205.0, 110.0))
            ),
            PolygonSlot(
                id="slot.tri.na", prompt="", points=((295.0, 110.0), (295.0, 42.0), (360.0, 110.0))
            ),
            PolygonSlot(
                id="slot.tri.da", prompt="", points=((450.0, 103.0), (565.0, 43.0), (520.0, 110.0))
            ),
            PolygonSlot(
                id="slot.tri.ra", prompt="", points=((615.0, 42.0), (675.0, 42.0), (675.0, 110.0))
            ),
            TextSlot(
                id="slot.line1",
                prompt="",
                text="(3) 직각삼각형은 ( 가, 나, 다, 라 )입니다.",
                style_role="question",
                x=10.0,
                y=150.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.line2",
                prompt="",
                text="(3) 직각삼각형은 나, 라입니다.",
                style_role="question",
                x=10.0,
                y=187.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.line3",
                prompt="",
                text="(3) 나, 라",
                style_role="question",
                x=10.0,
                y=224.0,
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
    "problem_id": "S3_초등_3_009027",
    "problem_type": "도형_분류",
    "metadata": {
        "language": "ko",
        "question": "삼각형을 보고 알맞은 기호를 모두 선택하세요.",
        "instruction": "직각삼각형에 해당하는 기호를 고르는 문제",
    },
    "domain": {
        "objects": [
            {"id": "obj.triangle.ga", "type": "triangle", "label": "가"},
            {"id": "obj.triangle.na", "type": "triangle", "label": "나"},
            {"id": "obj.triangle.da", "type": "triangle", "label": "다"},
            {"id": "obj.triangle.ra", "type": "triangle", "label": "라"},
        ],
        "relations": [],
        "problem_solving": {
            "understand": {
                "given_refs": [
                    "obj.triangle.ga",
                    "obj.triangle.na",
                    "obj.triangle.da",
                    "obj.triangle.ra",
                ],
                "target_ref": "answer.target",
                "condition_refs": ["rel.choose_right_triangles"],
            },
            "plan": {
                "method": "도형의 각을 보고 직각삼각형을 고른다",
                "description": "네 삼각형을 비교하여 직각이 있는 삼각형의 기호를 찾는다.",
            },
            "execute": {
                "expected_operations": [
                    "compare_angles",
                    "identify_right_angle",
                    "select_matching_labels",
                ]
            },
            "review": {"check_methods": ["visual_property_check", "label_selection_check"]},
        },
    },
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {"type": "selected_labels", "description": "직각삼각형에 해당하는 기호"},
        "value": 2,
        "unit": "",
    },
}

SOLVABLE = {
    "schema": "modu.solvable.v1.1",
    "problem_id": "S3_초등_3_009027",
    "problem_type": "도형_분류",
    "inputs": {
        "total_ticks": 4,
        "target_label": "직각삼각형",
        "target_ticks": 2,
        "target_count": 2,
        "unit": "",
    },
    "given": [
        {"ref": "obj.triangle.ga", "value": {"label": "가"}},
        {"ref": "obj.triangle.na", "value": {"label": "나"}},
        {"ref": "obj.triangle.da", "value": {"label": "다"}},
        {"ref": "obj.triangle.ra", "value": {"label": "라"}},
    ],
    "target": {"ref": "answer.target", "type": "selected_labels"},
    "method": "도형의 각을 보고 직각삼각형을 고른다",
    "plan": ["네 삼각형을 살펴보고 직각이 있는 삼각형을 찾는다.", "해당하는 기호를 선택한다."],
    "steps": [
        {"id": "step.1", "expr": "삼각형 4개를 비교한다.", "value": 4},
        {"id": "step.2", "expr": "직각삼각형으로 보이는 기호를 고른다.", "value": ["나", "라"]},
    ],
    "checks": [
        {
            "id": "check.1",
            "expr": "선택한 기호의 개수가 2개인가?",
            "expected": 2,
            "actual": 2,
            "pass": True,
        },
        {
            "id": "check.2",
            "expr": "선택 기호가 직각삼각형에 해당하는가?",
            "expected": True,
            "actual": True,
            "pass": True,
        },
    ],
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {"type": "selected_labels", "description": "직각삼각형에 해당하는 기호"},
        "value": 2,
        "unit": "",
    },
}
