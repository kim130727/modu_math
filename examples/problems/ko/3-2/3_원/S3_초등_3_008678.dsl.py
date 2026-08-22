from __future__ import annotations

from modu_math.dsl import (
    Canvas,
    CircleSlot,
    LineSlot,
    PathSlot,
    PolygonSlot,
    ProblemTemplate,
    Region,
    TextSlot,
)

PAPER_FILL = "#FDE8EF"
PAPER_STROKE = "#FF9AB2"
ARROW = "#9AA0A6"


def build_problem_template() -> ProblemTemplate:
    return ProblemTemplate(
        id="S3_초등_3_008678",
        title="반을 접어 생긴 선분",
        canvas=Canvas(width=940, height=330, coordinate_mode="logical"),
        regions=(
            Region(
                id="region.stem",
                role="stem",
                flow="absolute",
                slot_ids=("slot.stem",),
            ),
            Region(
                id="region.diagram",
                role="diagram",
                flow="absolute",
                slot_ids=(
                    "slot.folded.paper",
                    "slot.folded.edge",
                    "slot.arrow.body",
                    "slot.arrow.head",
                    "slot.opened.paper",
                    "slot.opened.fold_line",
                ),
            ),
            Region(
                id="region.choice",
                role="choices",
                flow="absolute",
                slot_ids=("slot.choice.1",),
            ),
        ),
        slots=(
            TextSlot(
                id="slot.stem",
                prompt="",
                text="원 모양 종이를 똑같이 둘로 나누어지도록 반을 접었다가 폈더니\n선이 생겼습니다. 알맞은 말을 선택하세요.",
                style_role="question",
                x=35,
                y=35,
                font_size=25,
            ),
            PathSlot(
                id="slot.folded.paper",
                prompt="",
                d="M 193.0 153.0 A 59.0 59.0 0 0 1 311.0 153.0 Z",
                fill=PAPER_FILL,
                stroke=PAPER_STROKE,
                stroke_width=2.0,
            ),
            LineSlot(
                id="slot.folded.edge",
                prompt="",
                x1=193.0,
                y1=153.0,
                x2=311.0,
                y2=153.0,
                stroke=PAPER_STROKE,
                stroke_width=2.0,
            ),
            LineSlot(
                id="slot.arrow.body",
                prompt="",
                x1=355.0,
                y1=153.0,
                x2=395.0,
                y2=153.0,
                stroke=ARROW,
                stroke_width=6.0,
            ),
            PolygonSlot(
                id="slot.arrow.head",
                prompt="",
                points=[
                    [410.0, 153.0],
                    [395.0, 143.0],
                    [395.0, 163.0],
                ],
                fill=ARROW,
                stroke=ARROW,
                stroke_width=0,
            ),
            CircleSlot(
                id="slot.opened.paper",
                prompt="",
                cx=509.0,
                cy=153.0,
                r=59.0,
                fill=PAPER_FILL,
                stroke=PAPER_STROKE,
                stroke_width=2.0,
            ),
            LineSlot(
                id="slot.opened.fold_line",
                prompt="",
                x1=450.0,
                y1=153.0,
                x2=568.0,
                y2=153.0,
                stroke=PAPER_STROKE,
                stroke_width=2.0,
                stroke_dasharray="5 4",
            ),
            TextSlot(
                id="slot.choice.1",
                prompt="",
                text="반을 접어 생긴 선분은 원의 ( 지름 , 반지름 )입니다.",
                style_role="choice",
                x=35,
                y=265,
                font_size=26,
            ),
        ),
        diagrams=(),
        groups=(),
        constraints=(),
        tags=("geometry", "circle", "paper_folding"),
    )


PROBLEM_TEMPLATE = build_problem_template()

SEMANTIC_OVERRIDE = {
    "problem_id": "S3_초등_3_008678",
    "problem_type": "circle_paper_folding_choice",
    "metadata": {
        "language": "ko",
        "question": "원 모양 종이를 똑같이 둘로 나누어지도록 반을 접었다가 폈더니 선이 생겼습니다. 알맞은 말을 선택하세요.",
        "instruction": "반을 접어 생긴 선분에 알맞은 말을 고른다.",
    },
    "domain": {
        "objects": [
            {"id": "obj.circle_paper", "type": "circle_paper", "description": "원 모양 종이"},
            {
                "id": "obj.fold_line",
                "type": "line_segment",
                "description": "반을 접었다가 펴서 생긴 선분",
            },
        ],
        "relations": [
            {
                "id": "rel.equal_halves",
                "type": "equal_partition",
                "from_id": "obj.fold_line",
                "to_id": "obj.circle_paper",
                "description": "접힌 선이 원을 둘로 똑같이 나눈다.",
            }
        ],
        "problem_solving": {
            "understand": {
                "given_refs": ["obj.circle_paper", "obj.fold_line"],
                "target_ref": "answer.target",
                "condition_refs": ["rel.equal_halves"],
            },
            "plan": {
                "method": "concept_matching",
                "description": "원을 둘로 똑같이 나누는 선분의 이름을 보기에서 고른다.",
            },
            "execute": {"expected_operations": ["observe_fold_line", "match_circle_term"]},
            "review": {"check_methods": ["definition_check"]},
        },
    },
    "answer": {
        "blanks": [],
        "choices": ["지름", "반지름"],
        "answer_key": ["지름"],
        "target": {"type": "choice_word", "description": "괄호 안에 들어갈 알맞은 말"},
        "value": "지름",
        "unit": "",
    },
}

SOLVABLE = {
    "schema": "modu.solvable.v1.1",
    "problem_id": "S3_초등_3_008678",
    "problem_type": "circle_paper_folding_choice",
    "inputs": {
        "total_ticks": 2,
        "target_label": "지름",
        "target_ticks": 1,
        "target_count": 1,
        "unit": "",
    },
    "given": [
        {"ref": "obj.circle_paper", "value": {"shape": "circle"}},
        {"ref": "obj.fold_line", "value": {"type": "line_segment", "created_by": "fold_and_open"}},
    ],
    "target": {"ref": "answer.target", "type": "choice_word"},
    "method": "concept_matching",
    "plan": [
        "반으로 접었다가 폈을 때 생긴 선분을 관찰한다.",
        "보기의 두 용어 중 알맞은 말(지름)을 고른다.",
    ],
    "steps": [
        {
            "id": "step.1",
            "expr": "접힌 선분이 원을 둘로 똑같이 나누는 지름인지 확인한다.",
            "value": "지름",
        }
    ],
    "checks": [
        {
            "id": "check.1",
            "expr": "지름의 정의와 일치하는가",
            "expected": "지름",
            "actual": "지름",
            "pass": True,
        }
    ],
    "answer": {
        "blanks": [],
        "choices": ["지름", "반지름"],
        "answer_key": ["지름"],
        "target": {"type": "choice_word", "description": "괄호 안에 들어갈 알맞은 말"},
        "value": "지름",
        "unit": "",
    },
}
