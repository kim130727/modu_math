from __future__ import annotations
from modu_math.dsl import Canvas, ProblemTemplate, Region, TextSlot, CircleSlot, LineSlot, PathSlot


def build_problem_template() -> ProblemTemplate:
    return ProblemTemplate(
        id="S3_초등_3_008689",
        title="원의 반지름과 지름",
        canvas=Canvas(width=960, height=392, coordinate_mode="logical"),
        regions=(
            Region(
                id="region.stem",
                role="stem",
                flow="absolute",
                slot_ids=(
                    "slot.q1",
                    "slot.q1.copy6",
                    "slot.inserted.arc.1",
                    "slot.inserted.arc.1.copy5",
                    "slot.inserted.arc.1.copy6",
                ),
            ),
            Region(
                id="region.diagram",
                role="diagram",
                flow="absolute",
                slot_ids=(
                    "slot.circle.outer",
                    "slot.line.a",
                    "slot.line.c",
                    "slot.pt.center",
                    "slot.lb.o",
                    "slot.lb.ga",
                    "slot.lb.na",
                    "slot.lb.da",
                ),
            ),
            Region(id="region.choice", role="choice", flow="absolute", slot_ids=("slot.choice",)),
            Region(id="region.answer", role="answer", flow="absolute", slot_ids=()),
        ),
        slots=(
            TextSlot(
                id="slot.q1",
                prompt="",
                text="        원의 반지름과 지름을 나타내는 선분을 각각 찾아      ",
                style_role="question",
                x=65,
                y=40,
                font_size=30,
            ),
            CircleSlot(id="slot.circle.outer", prompt="", cx=390, cy=235, r=105, fill="none"),
            LineSlot(id="slot.line.a", prompt="", x1=315, y1=160, x2=310, y2=305),
            LineSlot(id="slot.line.c", prompt="", x1=470, y1=165, x2=310, y2=305),
            CircleSlot(id="slot.pt.center", prompt="", cx=390, cy=235, r=5, fill="#d81b60"),
            TextSlot(
                id="slot.lb.o",
                prompt="",
                text="ㅇ",
                style_role="label",
                x=400,
                y=245,
                font_size=20,
                fill="#111111",
            ),
            TextSlot(
                id="slot.lb.ga",
                prompt="",
                text="ㄱ",
                style_role="label",
                x=330,
                y=235,
                font_size=25,
                fill="#111111",
            ),
            TextSlot(
                id="slot.lb.na",
                prompt="",
                text="ㄴ",
                style_role="label",
                x=400,
                y=280,
                font_size=25,
                fill="#111111",
            ),
            TextSlot(
                id="slot.lb.da",
                prompt="",
                text="ㄷ",
                style_role="label",
                x=390,
                y=180,
                font_size=25,
                fill="#111111",
            ),
            TextSlot(
                id="slot.choice",
                prompt="",
                text="원의 반지름 ( ㄱ , ㄴ , ㄷ ), 원의 지름 ( ㄱ , ㄴ , ㄷ )",
                style_role="question",
                x=60,
                y=380,
                font_size=30,
            ),
            TextSlot(
                id="slot.q1.copy6",
                prompt="",
                text="기호를 선택해       보세요      ",
                x=65,
                y=85,
                font_size=30,
                fill="#111111",
            ),
            PathSlot(
                id="slot.inserted.arc.1",
                prompt="",
                d="M 250 235 A 70 20 0 0 1 385 235",
                fill="#ffffff",
                stroke="#111827",
                stroke_width=1.5,
                stroke_dasharray="10 6",
                transform="rotate(90 317.5 231.32)",
            ),
            PathSlot(
                id="slot.inserted.arc.1.copy5",
                prompt="",
                d="M 375 207 A 45 20 0 0 1 475 207",
                fill="#ffffff",
                stroke="#111827",
                stroke_width=1.5,
                stroke_dasharray="10 6",
                transform="rotate(-40 418 199)",
            ),
            PathSlot(
                id="slot.inserted.arc.1.copy6",
                prompt="",
                d="M 290 250 A 105 30 0 0 1 495 250",
                fill="#ffffff",
                stroke="#111827",
                stroke_width=1.5,
                stroke_dasharray="10 6",
                transform="rotate(-220 392.5 242.17)",
            ),
        ),
        diagrams=(),
        groups=(),
        constraints=(),
        tags=(),
    )


PROBLEM_TEMPLATE = build_problem_template()

SEMANTIC_OVERRIDE = {
    "problem_id": "S3_초등_3_008689",
    "problem_type": "geometry_circle_classification",
    "metadata": {
        "language": "ko",
        "question": "원의 반지름과 지름을 나타내는 선분을 각각 찾아 기호를 선택하는 문제",
        "instruction": "원의 반지름과 지름을 나타내는 선분을 각각 찾아 기호를 선택해 보세요.",
    },
    "domain": {
        "objects": [
            {"id": "obj.circle", "type": "circle"},
            {"id": "obj.center", "type": "center"},
            {"id": "obj.segment.ga", "type": "segment", "label": "ㄱ"},
            {"id": "obj.segment.na", "type": "segment", "label": "ㄴ"},
            {"id": "obj.segment.da", "type": "segment", "label": "ㄷ"},
        ],
        "relations": [],
        "problem_solving": {
            "understand": {
                "given_refs": [
                    "obj.circle",
                    "obj.center",
                    "obj.segment.ga",
                    "obj.segment.na",
                    "obj.segment.da",
                ],
                "target_ref": "answer.target",
                "condition_refs": ["rel.radius", "rel.diameter"],
            },
            "plan": {
                "method": "visual_classification",
                "description": "각 선분이 중심에서 시작하는지, 원을 가로지르는지, 원 둘레까지 이어지는지를 보고 분류한다.",
            },
            "execute": {
                "expected_operations": [
                    "identify_radius_candidate",
                    "identify_diameter_candidate",
                    "match_symbols_to_categories",
                ]
            },
            "review": {"check_methods": ["center_relation_check", "endpoint_on_circle_check"]},
        },
    },
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {
            "type": "symbol_selection",
            "description": "원의 반지름과 원의 지름에 해당하는 기호를 고르기",
        },
        "value": "ㄷ, ㄴ",
        "unit": "",
    },
}

SOLVABLE = {
    "schema": "modu.solvable.v1.1",
    "problem_id": "S3_초등_3_008689",
    "problem_type": "geometry_circle_classification",
    "inputs": {
        "total_ticks": 3,
        "target_label": "원의 반지름과 지름을 나타내는 선분의 기호",
        "target_ticks": 2,
        "target_count": 2,
        "unit": "",
    },
    "given": [
        {"ref": "obj.segment.ga", "value": {"label": "ㄱ"}},
        {"ref": "obj.segment.na", "value": {"label": "ㄴ"}},
        {"ref": "obj.segment.da", "value": {"label": "ㄷ"}},
    ],
    "target": {"ref": "answer.target", "type": "symbol_selection"},
    "method": "visual_classification",
    "plan": [
        "중심을 지나는지 확인한다.",
        "원 둘레까지 이어지는지 확인한다.",
        "반지름과 지름에 해당하는 기호를 고른다.",
    ],
    "steps": [
        {
            "id": "step.1",
            "expr": "기호 ㄷ은 중심에서 원 둘레까지 이어지는 선분으로 본다.",
            "value": "반지름",
        },
        {
            "id": "step.2",
            "expr": "기호 ㄴ은 원을 가로지르며 중심을 지나는 선분으로 본다.",
            "value": "지름",
        },
    ],
    "checks": [
        {
            "id": "check.1",
            "expr": "반지름 후보가 중심과 원 둘레를 연결하는가",
            "expected": True,
            "actual": True,
            "pass": True,
        },
        {
            "id": "check.2",
            "expr": "지름 후보가 원의 두 점을 잇고 중심을 지나는가",
            "expected": True,
            "actual": True,
            "pass": True,
        },
    ],
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {
            "type": "symbol_selection",
            "description": "원의 반지름과 원의 지름에 해당하는 기호를 고르기",
        },
        "value": "ㄷ, ㄴ",
        "unit": "",
    },
}
