from __future__ import annotations

from modu_math.dsl import (
    Canvas,
    CircleSlot,
    LineSlot,
    PathSlot,
    PolygonSlot,
    ProblemTemplate,
    RectSlot,
    Region,
    TextSlot,
    opened_circle_with_fold_slots,
)


PAPER_FILL = "#FDE8EF"
PAPER_STROKE = "#FF9AB2"
ARROW = "#9AA0A6"


def _folded_half_slots() -> tuple:
    cx, cy, r = 345.0, 153.0, 59.0
    return (
        PathSlot(
            id="slot.folded.paper",
            prompt="",
            d = 'M 193.6666259765625 156.55560302734375 C 196.0266259765625 119.97560302734377 224.3466259765625 97.55560302734375 252.6666259765625 97.55560302734375 C 280.9866259765625 97.55560302734375 309.3066259765625 119.97560302734377 311.6666259765625 156.55560302734375 L 193.6666259765625 156.55560302734375 Z', fill = '#FDE8EF', stroke="none",
        stroke_width = 2),
        CircleSlot(
            id="slot.folded.back_circle",
            prompt="",
            cx = 252, cy = 155, r = 60, fill="none",
            stroke=PAPER_STROKE,
            stroke_width=1.7,
        ),
        CircleSlot(
            id="slot.folded.front_circle",
            prompt="",
            cx = 252, cy = 160, r = 60, fill="none",
            stroke=PAPER_STROKE,
            stroke_width=1.7,
        ),
        RectSlot(
            id="slot.folded.lower_mask",
            prompt="",
            x = 171, y = 153, width=r * 2.0 + 24.0,
            height=r + 12.0,
            fill="#FFFFFF",
            stroke="none",
            stroke_width=0.0,
        ),
        LineSlot(
            id="slot.folded.edge",
            prompt="",
            x1 = 193, y1 = 153, x2 = 311, y2 = 153, stroke=PAPER_STROKE,
            stroke_width=1.7,
        ),
    )


def _opened_circle_slots() -> tuple:
    return opened_circle_with_fold_slots(
        "slot.opened",
        cx = 509.0, cy = 153.0, r = 59.0, angle = 0.0, fill=PAPER_FILL,
        stroke=PAPER_STROKE,
        stroke_width=1.7,
        dash="5 4",
    )


def build_problem_template() -> ProblemTemplate:
    folded_slots = _folded_half_slots()
    opened_slots = _opened_circle_slots()

    return ProblemTemplate(
        id="S3_초등_3_008679",
        title="반을 접어 생긴 선분",
        canvas=Canvas(width=940, height=325, coordinate_mode="logical"),
        regions=(
            Region(
                id="region.stem",
                role="stem",
                flow="absolute",
                slot_ids=("slot.stem.1", "slot.stem.2"),
            ),
            Region(
                id="region.diagram",
                role="diagram",
                flow="absolute",
                slot_ids=(
                    "slot.folded.paper",
                    "slot.folded.back_circle",
                    "slot.folded.front_circle",
                    "slot.folded.lower_mask",
                    "slot.folded.edge",
                    "slot.arrow.body",
                    "slot.arrow.head",
                    "slot.opened.paper",
                    "slot.opened.fold_line",
                ),
            ),
            Region(id="region.choice", role="choices", flow="absolute", slot_ids=("slot.choice.1",)),
        ),
        slots=(
            TextSlot(
                id="slot.stem.1",
                prompt="",
                text = '원 모양 종이를 똑같이 둘로 나누어지도록 반을 접었다가 폈더니 선이', style_role="question",
                x = 35, y = 35, font_size = 25),
            TextSlot(
                id="slot.stem.2",
                prompt="",
                text="생겼습니다. 알맞은 말을 선택하세요.",
                style_role="question",
                x=34.0,
                y=70.0,
                font_size=25,
            ),
            *folded_slots,
            LineSlot(
                id="slot.arrow.body",
                prompt="",
                x1 = 375, y1 = 155, x2 = 395, y2 = 155, stroke=ARROW,
                stroke_width=8.0,
            ),
            PolygonSlot(
                id="slot.arrow.head",
                prompt="",
                points = [[408, 157.4444580078125], [393, 143.4444580078125], [393, 171.4444580078125]], fill = '#9AA0A6', stroke = '#9AA0A6', stroke_width = 0),
            *opened_slots,
            TextSlot(
                id="slot.choice.1",
                prompt="",
                text="(2) 원의 지름은 원을 똑같이 (둘, 넷)(으)로 나눕니다.",
                style_role="choice",
                x = 36, y = 263, font_size=26,
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
        "choices": [],
        "answer_key": [],
        "target": {
            "type": "choice",
            "description": "원의 지름이 원을 똑같이 나누는 수",
        },
        "value": 2,
        "unit": "",
    },
}

SOLVABLE = {
    "schema": "modu.solvable.v1.1",
    "problem_id": "S3_초등_3_008679",
    "problem_type": "concept_selection",
    "inputs": {
        "total_ticks": 0,
        "target_label": "원의 지름이 원을 똑같이 나누는 수",
        "target_ticks": 0,
        "target_count": 2,
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
        "해설 문장에서 지름의 성질을 읽는다.",
        "지름이 원을 똑같이 몇 부분으로 나누는지 확인한다.",
        "선택지 중 알맞은 말을 고른다.",
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
        "choices": [],
        "answer_key": [],
        "target": {
            "type": "choice",
            "description": "원의 지름이 원을 똑같이 나누는 수",
        },
        "value": 2,
        "unit": "",
    },
}
