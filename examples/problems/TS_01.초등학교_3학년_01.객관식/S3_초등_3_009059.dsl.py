from __future__ import annotations
from modu_math.dsl import Canvas, ProblemTemplate, Region, TextSlot, LineSlot, CircleSlot


def build_problem_template() -> ProblemTemplate:
    return ProblemTemplate(
        id="S3_초등_3_009059",
        title="도형을 보고 알맞은 말을 선택하세요",
        canvas=Canvas(width=792.0, height=300.0, coordinate_mode="logical"),
        regions=(
            Region(id="region.header", role="stem", flow="absolute", slot_ids=("slot.header",)),
            Region(
                id="region.diagram",
                role="diagram",
                flow="absolute",
                slot_ids=("slot.line", "slot.pt.s", "slot.pt.o", "slot.lb.s", "slot.lb.o"),
            ),
            Region(id="region.choices", role="choices", flow="absolute", slot_ids=("slot.choice",)),
            Region(id="region.answer", role="answer", flow="absolute", slot_ids=()),
        ),
        slots=(
            TextSlot(
                id="slot.header",
                prompt="",
                text="98. 도형을 보고 알맞은 말을 선택하세요.",
                style_role="question",
                x=26.0,
                y=30.0,
                font_size=28,
            ),
            LineSlot(
                id="slot.line",
                prompt="",
                x1=60.0,
                y1=65.0,
                x2=330.0,
                y2=124.0,
                stroke="#222222",
                stroke_width=2.0,
            ),
            CircleSlot(id="slot.pt.s", prompt="", cx=60.0, cy=64.0, r=3.8, fill="#222222"),
            CircleSlot(id="slot.pt.o", prompt="", cx=272.0, cy=111.0, r=3.8, fill="#222222"),
            TextSlot(
                id="slot.lb.s",
                prompt="",
                text="ㅅ",
                style_role="label",
                x=52.0,
                y=52.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.lb.o",
                prompt="",
                text="ㅇ",
                style_role="label",
                x=270.0,
                y=98.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.choice",
                prompt="",
                text="( 선분 ㅅㅇ , 반직선 ㅅㅇ , 직선 ㅅㅇ )",
                style_role="choice",
                x=401.0,
                y=86.0,
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
    "problem_id": "S3_초등_3_009059",
    "problem_type": "도형_분류",
    "metadata": {
        "language": "ko",
        "question": "도형을 보고 알맞은 말을 선택하세요.",
        "instruction": "선분, 반직선, 직선의 이름을 보고 알맞은 것을 고른다.",
        "points": 0,
    },
    "domain": {
        "objects": [
            {"id": "obj.point.s", "type": "point", "label": "ㅅ"},
            {"id": "obj.point.o", "type": "point", "label": "ㅇ"},
            {
                "id": "obj.figure",
                "type": "line_like_figure",
                "name_candidates": ["선분 ㅅㅇ", "반직선 ㅅㅇ", "직선 ㅅㅇ"],
            },
        ],
        "relations": [],
        "problem_solving": {
            "understand": {
                "given_refs": ["obj.point.s", "obj.point.o", "obj.figure"],
                "target_ref": "answer.target",
                "condition_refs": ["rel.start_from_s", "rel.passes_o"],
            },
            "plan": {
                "method": "도형의 정의와 표시된 점의 관계를 보고 이름을 고른다.",
                "description": "시작점과 지나는 점을 확인하고 보기 중 해당 도형 이름을 찾는다.",
            },
            "execute": {
                "expected_operations": [
                    "점 ㅅ이 시작점인지 확인",
                    "점 ㅇ이 지나는 점인지 확인",
                    "보기에서 알맞은 도형 이름 선택",
                ]
            },
            "review": {
                "check_methods": [
                    "정의와 그림이 일치하는지 확인",
                    "선택한 이름이 시작점 표시에 맞는지 확인",
                ]
            },
        },
    },
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {"type": "figure_name_choice", "description": "그림에 알맞은 도형의 이름"},
        "value": "반직선 ㅅㅇ",
        "unit": "",
    },
}

SOLVABLE = {
    "schema": "modu.solvable.v1.1",
    "problem_id": "S3_초등_3_009059",
    "problem_type": "도형_분류",
    "inputs": {
        "total_ticks": 0,
        "target_label": "도형 이름",
        "target_ticks": 0,
        "target_count": 1,
        "unit": "",
    },
    "given": [
        {"ref": "obj.point.s", "value": {"label": "ㅅ"}},
        {"ref": "obj.point.o", "value": {"label": "ㅇ"}},
        {
            "ref": "obj.figure",
            "value": {"name_candidates": ["선분 ㅅㅇ", "반직선 ㅅㅇ", "직선 ㅅㅇ"]},
        },
    ],
    "target": {"ref": "answer.target", "type": "figure_name_choice"},
    "method": "도형의 정의 비교",
    "plan": [
        "그림에서 시작점과 지나가는 점을 확인한다.",
        "보기의 세 도형 이름과 그림의 관계를 비교한다.",
        "알맞은 도형 이름을 고른다.",
    ],
    "steps": [
        {"id": "step.1", "expr": "점 ㅅ이 시작점인지 확인", "value": True},
        {"id": "step.2", "expr": "점 ㅇ을 지나는지 확인", "value": True},
        {"id": "step.3", "expr": "그림에 알맞은 도형 이름 선택", "value": "반직선 ㅅㅇ"},
    ],
    "checks": [
        {
            "id": "check.1",
            "expr": "시작점이 ㅅ이고 ㅇ을 지난다",
            "expected": True,
            "actual": True,
            "pass": True,
        },
        {
            "id": "check.2",
            "expr": "선택한 이름이 그림의 정의와 일치한다",
            "expected": "반직선 ㅅㅇ",
            "actual": "반직선 ㅅㅇ",
            "pass": True,
        },
    ],
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {"type": "figure_name_choice", "description": "그림에 알맞은 도형의 이름"},
        "value": "반직선 ㅅㅇ",
        "unit": "",
    },
}
