from __future__ import annotations
from modu_math.dsl import (
    Canvas,
    ProblemTemplate,
    Region,
    TextSlot,
    CircleSlot,
    LineSlot,
    RectSlot,
)


def build_problem_template() -> ProblemTemplate:
    return ProblemTemplate(
        id="S3_초등_3_008679",
        title="원의 지름",
        canvas=Canvas(width=940, height=406, coordinate_mode="logical"),
        regions=(
            Region(
                id="region.stem",
                role="stem",
                flow="absolute",
                slot_ids=("slot.q2", "slot.q3"),
            ),
            Region(
                id="region.diagram",
                role="diagram",
                flow="absolute",
                slot_ids=(
                    "slot.fig.left",
                    "slot.fig.arrow",
                    "slot.fig.right",
                    "slot.fig.right.dash",
                ),
            ),
            Region(
                id="region.choice",
                role="choice",
                flow="absolute",
                slot_ids=("slot.choice.line", ),
            ),
            Region(
                id="region.explanation",
                role="explanation",
                flow="absolute",
                slot_ids=(),
            ),
            Region(id="region.footer", role="footer", flow="absolute", slot_ids=()),
        ),
        slots=(
            TextSlot(
                id="slot.q2",
                prompt="",
                text = '    원 모양 종이를 똑같이 둘로 나누어지도록 반을 접었다가 펴더니  ', style_role="question",
                x = 25, y = 60, font_size = 30),
            TextSlot(
                id="slot.q3",
                prompt="",
                text = '선이 생겼습니다. 알맞은 말을 선택하세요.', style_role="question",
                x = 25, y = 105, font_size = 30),
            RectSlot(
                id="slot.fig.left",
                prompt="",
                x = 200, y = 145, width = 125, height = 30, fill="#F9DCE3",
                stroke="#FF9CB4",
                stroke_width=2.0,
            ),
            CircleSlot(
                id="slot.fig.right",
                prompt="",
                cx = 605, cy = 165, r = 60, fill="#F9DCE3",
                stroke="#FF9CB4",
                stroke_width=2.0,
            ),
            LineSlot(
                id="slot.fig.right.dash",
                prompt="",
                x1 = 550, y1 = 165, x2 = 660, y2 = 165, stroke="#FF9CB4",
                stroke_width=2.0,
                stroke_dasharray="5 4",
            ),
            TextSlot(
                id="slot.fig.arrow",
                prompt="",
                text = '→', style_role="diagram",
                x = 415, y = 185, font_size = 55, max_width = 810),
            TextSlot(
                id="slot.choice.line",
                prompt="",
                text = '(2) 원의 지름은 원을 똑같이 ( 둘, 넷 )(○)로 나눕니다.', style_role="question",
                x = 45, y = 295, font_size = 30, max_width = 810),
            
        ),
        diagrams=(),
        groups=(),
        constraints=(),
        tags=(),
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
