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
        id="S3_초등_3_008679",
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
                text="원의 지름은 원을 똑같이 ( 둘 , 넷 )(으)로 나눕니다.",
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
    "problem_id": "S3_초등_3_008679",
    "problem_type": "concept_selection",
    "metadata": {
        "language": "ko",
        "question": "원의 지름이 원을 어떻게 나누는지에 대한 알맞은 말을 고르는 문제",
        "instruction": "알맞은 말을 선택하세요.",
    },
    "domain": {
        "objects": [
            {"id": "obj.circle", "type": "circle"},
            {"id": "obj.diameter", "type": "segment", "role": "diameter"},
            {"id": "obj.fold_line", "type": "segment", "role": "crease_line"},
        ],
        "relations": [],
        "problem_solving": {
            "understand": {
                "given_refs": ["obj.circle", "obj.diameter", "obj.fold_line"],
                "target_ref": "answer.target",
                "condition_refs": [
                    "rel.diameter_through_center",
                    "rel.diameter_splits_circle",
                ],
            },
            "plan": {
                "method": "concept_match",
                "description": "해설의 개념 설명을 바탕으로 지름이 원을 몇 개로 나누는지 확인한다.",
            },
            "execute": {
                "expected_operations": [
                    "read_explanation",
                    "match_diameter_property",
                    "select_correct_choice",
                ]
            },
            "review": {
                "check_methods": [
                    "meaning_consistency_check",
                    "explanation_choice_match",
                ]
            },
        },
    },
    "answer": {
        "blanks": [],
        "choices": ["둘", "넷"],
        "answer_key": ["둘"],
        "target": {
            "type": "choice",
            "description": "원의 지름이 원을 똑같이 나누는 수",
        },
        "value": "둘",
        "unit": "",
    },
}

SOLVABLE = {
    "schema": "modu.solvable.v1.1",
    "problem_id": "S3_초등_3_008679",
    "problem_type": "concept_selection",
    "inputs": {
        "total_ticks": 2,
        "target_label": "원의 지름이 원을 똑같이 나누는 수",
        "target_ticks": 1,
        "target_count": 1,
        "unit": "",
    },
    "given": [
        {"ref": "obj.circle", "value": {"type": "circle"}},
        {"ref": "obj.diameter", "value": {"role": "diameter"}},
        {"ref": "obj.fold_line", "value": {"role": "crease_line"}},
    ],
    "target": {"ref": "answer.target", "type": "choice"},
    "method": "concept_match",
    "plan": [
        "지름의 성질을 확인한다.",
        "지름이 원을 똑같이 몇 부분으로 나누는지 확인한다.",
        "선택지 중 알맞은 말(둘)을 고른다.",
    ],
    "steps": [
        {
            "id": "step.1",
            "expr": "원의 지름의 성질을 확인한다.",
            "value": "원을 똑같이 둘로 나눈다",
        },
        {
            "id": "step.2",
            "expr": "선택지 (둘, 넷) 중 알맞은 말을 고른다.",
            "value": "둘",
        },
    ],
    "checks": [
        {
            "id": "check.1",
            "expr": "원의 지름은 원을 똑같이 둘로 나누는가",
            "expected": "둘",
            "actual": "둘",
            "pass": True,
        }
    ],
    "answer": {
        "blanks": [],
        "choices": ["둘", "넷"],
        "answer_key": ["둘"],
        "target": {
            "type": "choice",
            "description": "원의 지름이 원을 똑같이 나누는 수",
        },
        "value": "둘",
        "unit": "",
    },
}
