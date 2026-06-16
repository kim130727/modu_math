from __future__ import annotations
from modu_math.dsl import (
    Canvas,
    ProblemTemplate,
    Region,
    TextSlot,
    RectSlot,
    LineSlot,
    CircleSlot,
)


def build_problem_template() -> ProblemTemplate:
    return ProblemTemplate(
        id="S3_초등_3_008678",
        title="반을 접어 생긴 선",
        canvas=Canvas(width=940, height=360, coordinate_mode="logical"),
        regions=(
            Region(
                id="region.stem",
                role="stem",
                flow="absolute",
                slot_ids=("slot.q1", "slot.q2"),
            ),
            Region(
                id="region.diagram",
                role="diagram",
                flow="absolute",
                slot_ids=(
                    "slot.paper.left",
                    "slot.arrow",
                    "slot.paper.right",
                    "slot.foldline",
                ),
            ),
            Region(
                id="region.choice",
                role="choice",
                flow="absolute",
                slot_ids=("slot.c1",  ),
            ),
        ),
        slots=(
            TextSlot(
                id="slot.q1",
                prompt="",
                text = '원 모양 종이를 똑같이 둘로 나누어지도록 반을 접었다가 펴더니 선이  ', style_role="question",
                x=18.0,
                y=32.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.q2",
                prompt="",
                text = '생겼습니다. 알맞은 말을 선택하세요.', style_role="question",
                x = 20, y = 80, font_size = 30),
            RectSlot(
                id="slot.paper.left",
                prompt="",
                x = 160, y = 140, width = 120, height = 60, fill="#FDE8EF",
                stroke="#FF9AB2",
                stroke_width=2.0,
            ),
            LineSlot(
                id="slot.arrow",
                prompt="",
                x1 = 375, y1 = 170, x2 = 415, y2 = 170, stroke="#9AA0A6",
                stroke_width=3.0,
            ),
            CircleSlot(
                id="slot.paper.right",
                prompt="",
                cx = 575, cy = 180, r = 60, fill="#FDE8EF",
                stroke="#FF9AB2",
                stroke_width=2.0,
            ),
            LineSlot(
                id="slot.foldline",
                prompt="",
                x1 = 520, y1 = 180, x2 = 630, y2 = 180, stroke="#FF9AB2",
                stroke_width=1.6,
                stroke_dasharray="5 3",
            ),
            TextSlot(
                id="slot.c1",
                prompt="",
                text = '(1) 반을 접어 생긴 선분은 원의 ( 지름 , 반지름 )입니다.', style_role="question",
                x = 25, y = 285, font_size = 30),
            
            
        ),
        diagrams=(),
        groups=(),
        constraints=(),
        tags=(),
    )


PROBLEM_TEMPLATE = build_problem_template()

SEMANTIC_OVERRIDE = {
    "problem_id": "S3_초등_3_008678",
    "problem_type": "도형의 성질_선택형",
    "metadata": {
        "language": "ko",
        "question": "원 모양 종이를 똑같이 둘로 나누어지도록 반을 접었다가 펴니 선이 생겼습니다. 알맞은 말을 선택하세요.",
        "instruction": "알맞은 말을 선택하세요.",
    },
    "domain": {
        "objects": [
            {"id": "obj.paper", "type": "paper_shape", "shape": "circle"},
            {"id": "obj.folded_shape", "type": "paper_shape", "shape": "semicircle"},
            {"id": "obj.fold_line", "type": "line"},
            {"id": "obj.choice_diameter", "type": "term", "text": "지름"},
            {"id": "obj.choice_radius", "type": "term", "text": "반지름"},
        ],
        "relations": [],
        "problem_solving": {
            "understand": {
                "given_refs": ["obj.paper", "obj.folded_shape"],
                "target_ref": "answer.target",
                "condition_refs": ["rel.fold_creates_line", "rel.line_divides_circle"],
            },
            "plan": {
                "method": "도형의 성질 확인",
                "description": "접어서 생긴 선이 원을 똑같이 둘로 나누는 선인지 살펴본다.",
            },
            "execute": {
                "expected_operations": [
                    "folding_relation_check",
                    "circle_line_property_check",
                ]
            },
            "review": {"check_methods": ["choice_match_check"]},
        },
    },
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {"type": "choice_word", "description": "빈칸에 들어갈 알맞은 말"},
        "value": 0,
        "unit": "",
    },
}

SOLVABLE = {
    "schema": "modu.solvable.v1.1",
    "problem_id": "S3_초등_3_008678",
    "problem_type": "도형의 성질_선택형",
    "inputs": {
        "total_ticks": 0,
        "target_label": "빈칸에 들어갈 알맞은 말",
        "target_ticks": 0,
        "target_count": 1,
        "unit": "",
    },
    "given": [
        {"ref": "obj.paper", "value": {"shape": "circle"}},
        {"ref": "obj.folded_shape", "value": {"shape": "semicircle"}},
        {"ref": "obj.choice_diameter", "value": {"text": "지름"}},
        {"ref": "obj.choice_radius", "value": {"text": "반지름"}},
    ],
    "target": {"ref": "answer.target", "type": "choice_word"},
    "method": "도형의 성질 확인",
    "plan": [
        "원 모양 종이를 반으로 접었을 때 생기는 선의 성질을 확인한다.",
        "보기의 단어 중 원의 중심을 지나는 선과 맞는 말을 찾는다.",
    ],
    "steps": [
        {
            "id": "step.1",
            "expr": "원 모양 종이를 반으로 접음",
            "value": "접힌 선이 생김",
        },
        {
            "id": "step.2",
            "expr": "접힌 선의 성질 확인",
            "value": "원을 똑같이 둘로 나누는 선",
        },
    ],
    "checks": [
        {
            "id": "check.1",
            "expr": "접힌 선이 원의 중심을 지나는지 확인",
            "expected": True,
            "actual": True,
            "pass": True,
        }
    ],
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {"type": "choice_word", "description": "빈칸에 들어갈 알맞은 말"},
        "value": 0,
        "unit": "",
    },
}
