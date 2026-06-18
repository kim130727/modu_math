from __future__ import annotations

from dataclasses import replace

from modu_math.dsl import (
    Canvas,
    LineSlot,
    PolygonSlot,
    ProblemTemplate,
    Region,
    TextSlot,
    folded_half_circle_slots,
    opened_circle_with_fold_slots,
)


PAPER_FILL = "#FDE8EF"
PAPER_STROKE = "#FF9AB2"
ARROW = "#9AA0A6"


def _folded_half_slots() -> tuple:
    slots = folded_half_circle_slots(
        "slot.folded",
        cx = 775.0, cy = 165.0, r = 60.0, fill=PAPER_FILL,
        stroke=PAPER_STROKE,
        stroke_width=1.7,
    )
    return tuple(replace(slot, transform="rotate(180 345 153)") for slot in slots)


def _opened_circle_slots() -> tuple:
    return opened_circle_with_fold_slots(
        "slot.opened",
        cx=612.0,
        cy=153.0,
        r=59.0,
        angle=0.0,
        fill=PAPER_FILL,
        stroke=PAPER_STROKE,
        stroke_width=1.7,
        dash="5 4",
    )


def build_problem_template() -> ProblemTemplate:
    folded_slots = _folded_half_slots()
    opened_slots = _opened_circle_slots()

    return ProblemTemplate(
        id="S3_초등_3_008678",
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
                x1=462.0,
                y1=153.0,
                x2=484.0,
                y2=153.0,
                stroke=ARROW,
                stroke_width=8.0,
            ),
            PolygonSlot(
                id="slot.arrow.head",
                prompt="",
                points=((496.0, 153.0), (481.0, 139.0), (481.0, 167.0)),
                fill=ARROW,
                stroke=ARROW,
                stroke_width=0.0,
            ),
            *opened_slots,
            TextSlot(
                id="slot.choice.1",
                prompt="",
                text="(1) 반을 접어 생긴 선분은 원의 ( 지름 , 반지름 )입니다.",
                style_role="choice",
                x=30.0,
                y=263.0,
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
        "instruction": "보이는 선택 문장만 렌더링하고 정답/해설성 하단 문장은 생략한다.",
    },
    "domain": {
        "objects": [
            {"id": "obj.circle_paper", "type": "circle_paper", "description": "원 모양 종이"},
            {"id": "obj.fold_line", "type": "line_segment", "description": "반을 접었다가 펴서 생긴 선분"},
            {"id": "obj.choice_diameter", "type": "term", "text": "지름"},
            {"id": "obj.choice_radius", "type": "term", "text": "반지름"},
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
            "plan": {"method": "concept_matching", "description": "원을 둘로 똑같이 나누는 선분의 이름을 보기에서 고른다."},
            "execute": {"expected_operations": ["observe_fold_line", "match_circle_term"]},
            "review": {"check_methods": ["visible_choice_only_check"]},
        },
    },
    "answer": {
        "blanks": [],
        "choices": [{"id": "choice.diameter", "value": "지름"}, {"id": "choice.radius", "value": "반지름"}],
        "answer_key": [],
        "target": {"type": "choice_word", "description": "괄호 안에 들어갈 알맞은 말"},
        "value": "",
        "unit": "",
    },
}

SOLVABLE = {
    "schema": "modu.solvable.v1.1",
    "problem_id": "S3_초등_3_008678",
    "problem_type": "circle_paper_folding_choice",
    "inputs": {
        "total_ticks": 0,
        "target_label": "괄호 안에 들어갈 알맞은 말",
        "target_ticks": 0,
        "target_count": 1,
        "unit": "",
    },
    "given": [
        {"ref": "obj.circle_paper", "value": {"shape": "circle"}},
        {"ref": "obj.fold_line", "value": {"type": "line_segment", "created_by": "fold_and_open"}},
    ],
    "target": {"ref": "answer.target", "type": "choice_word"},
    "method": "concept_matching",
    "plan": ["반으로 접었다가 폈을 때 생긴 선분을 관찰한다.", "보기의 두 용어 중 알맞은 말을 고른다."],
    "steps": [{"id": "step.1", "expr": "접힌 선분이 원을 둘로 똑같이 나누는지 확인한다.", "value": ""}],
    "checks": [{"id": "check.1", "expr": "정답과 해설 문장이 렌더링되지 않는다.", "expected": True, "actual": True, "pass": True}],
    "answer": {
        "blanks": [],
        "choices": [{"id": "choice.diameter", "value": "지름"}, {"id": "choice.radius", "value": "반지름"}],
        "answer_key": [],
        "target": {"type": "choice_word", "description": "괄호 안에 들어갈 알맞은 말"},
        "value": "",
        "unit": "",
    },
}
