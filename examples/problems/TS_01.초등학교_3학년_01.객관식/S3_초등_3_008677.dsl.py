from __future__ import annotations
from modu_math.dsl import (
    Canvas,
    ProblemTemplate,
    Region,
    TextSlot,
    RectSlot,
    CircleSlot,
    LineSlot,
)


def build_problem_template() -> ProblemTemplate:
    return ProblemTemplate(
        id="S3_초등_3_008677",
        title="원의 반지름",
        canvas=Canvas(width=800.0, height=390.0, coordinate_mode="logical"),
        regions=(
            Region(
                id="region.stem",
                role="stem",
                flow="absolute",
                slot_ids=("slot.qnum", "slot.qtext"),
            ),
            Region(
                id="region.diagram",
                role="diagram",
                flow="absolute",
                slot_ids=(
                    "slot.circle",
                    "slot.seg1",
                    "slot.seg2",
                    "slot.seg3",
                    "slot.pt.center",
                    "slot.lb.g1",
                    "slot.lb.g2",
                    "slot.lb.g3",
                    "slot.lb.g4",
                    "slot.lb.o",
                ),
            ),
            Region(
                id="region.choices",
                role="choices",
                flow="absolute",
                slot_ids=(
                    "slot.choice_box",
                    "slot.choice1",
                    "slot.choice2",
                    "slot.choice3",
                ),
            ),
            Region(id="region.answer", role="answer", flow="absolute", slot_ids=()),
        ),
        slots=(
            TextSlot(
                id="slot.qnum",
                prompt="",
                text="□ 60.",
                style_role="question",
                x=8.0,
                y=24.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.qtext",
                prompt="",
                text="원의 반지름을 나타내는 선분을 찾아 선택하세요.",
                style_role="question",
                x=90.0,
                y=24.0,
                font_size=28,
            ),
            CircleSlot(
                id="slot.circle", prompt="", cx=510.0, cy=106.0, r=71.0, fill="none"
            ),
            LineSlot(id="slot.seg1", prompt="", x1=446.0, y1=175.0, x2=551.0, y2=70.0),
            LineSlot(id="slot.seg2", prompt="", x1=510.0, y1=106.0, x2=510.0, y2=177.0),
            LineSlot(id="slot.seg3", prompt="", x1=548.0, y1=73.0, x2=548.0, y2=173.0),
            CircleSlot(
                id="slot.pt.center",
                prompt="",
                cx=482.0,
                cy=106.0,
                r=3.5,
                fill="#ff4aa5",
            ),
            TextSlot(
                id="slot.lb.g1",
                prompt="",
                text="ㄱ",
                style_role="label",
                x=430.0,
                y=184.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.lb.g2",
                prompt="",
                text="ㄴ",
                style_role="label",
                x=560.0,
                y=63.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.lb.g3",
                prompt="",
                text="ㄷ",
                style_role="label",
                x=555.0,
                y=187.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.lb.g4",
                prompt="",
                text="ㄹ",
                style_role="label",
                x=507.0,
                y=193.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.lb.o",
                prompt="",
                text="O",
                style_role="label",
                x=491.0,
                y=120.0,
                font_size=28,
            ),
            RectSlot(
                id="slot.choice_box",
                prompt="",
                x=194.0,
                y=204.0,
                width=579.0,
                height=63.0,
                fill="none",
            ),
            TextSlot(
                id="slot.choice1",
                prompt="",
                text="선분 ㄱㄹ",
                style_role="choice",
                x=236.0,
                y=242.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.choice2",
                prompt="",
                text="선분 Oㄴ",
                style_role="choice",
                x=411.0,
                y=242.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.choice3",
                prompt="",
                text="선분 ㄷㄹ",
                style_role="choice",
                x=589.0,
                y=242.0,
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
    "problem_id": "S3_초등_3_008677",
    "problem_type": "geometry_circle_radius_selection",
    "metadata": {
        "language": "ko",
        "question": "원의 반지름을 나타내는 선분을 찾는 선택형 문제",
        "instruction": "원의 반지름을 나타내는 선분을 찾아 선택하세요.",
    },
    "domain": {
        "objects": [
            {"id": "obj.circle", "type": "circle"},
            {"id": "obj.center", "type": "point", "label": "O", "role": "center_like"},
            {"id": "obj.segment.on", "type": "segment", "label": "Oㄴ"},
        ],
        "relations": [],
        "problem_solving": {
            "understand": {
                "given_refs": ["obj.circle", "obj.center"],
                "target_ref": "answer.target",
                "condition_refs": ["rel.radius_definition"],
            },
            "plan": {
                "method": "definition_matching",
                "description": "원의 중심과 원 위의 한 점을 이은 선분을 찾는다.",
            },
            "execute": {
                "expected_operations": [
                    "identify_center",
                    "identify_point_on_circle",
                    "match_segment_to_radius_definition",
                ]
            },
            "review": {"check_methods": ["definition_check"]},
        },
    },
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {"type": "segment", "description": "원의 반지름을 나타내는 선분"},
        "value": "선분 Oㄴ",
        "unit": "",
    },
}

SOLVABLE = {
    "schema": "modu.solvable.v1.1",
    "problem_id": "S3_초등_3_008677",
    "problem_type": "geometry_circle_radius_selection",
    "inputs": {
        "total_ticks": 1,
        "target_label": "반지름",
        "target_ticks": 1,
        "target_count": 1,
        "unit": "",
    },
    "given": [
        {"ref": "obj.circle", "value": {"type": "circle"}},
        {"ref": "obj.center", "value": {"label": "O"}},
        {"ref": "obj.segment.on", "value": {"label": "Oㄴ"}},
    ],
    "target": {"ref": "answer.target", "type": "segment"},
    "method": "definition_matching",
    "plan": [
        "원의 중심과 원 위의 한 점을 이은 선분이 반지름인지 확인한다.",
        "보기 중 해당하는 선분을 고른다.",
    ],
    "steps": [
        {
            "id": "step.1",
            "expr": "원의 중심 O와 원 위의 한 점 ㄴ을 이은 선분 확인",
            "value": "Oㄴ",
        },
        {
            "id": "step.2",
            "expr": "반지름의 정의와 일치하는 보기 선택",
            "value": "선분 Oㄴ",
        },
    ],
    "checks": [
        {
            "id": "check.1",
            "expr": "중심 O에서 원 위의 점 ㄴ으로 이어지는가",
            "expected": True,
            "actual": True,
            "pass": True,
        }
    ],
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {"type": "segment", "description": "원의 반지름을 나타내는 선분"},
        "value": "선분 Oㄴ",
        "unit": "",
    },
}
