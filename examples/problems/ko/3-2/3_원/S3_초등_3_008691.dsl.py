from __future__ import annotations
from modu_math.dsl import (
    Canvas,
    CircleSlot,
    LineSlot,
    ProblemTemplate,
    RectSlot,
    Region,
    TextSlot,
    PathSlot,
)


def build_problem_template() -> ProblemTemplate:
    return ProblemTemplate(
        id="S3_초등_3_008691",
        title="원의 반지름과 지름",
        canvas=Canvas(width=950, height=410, coordinate_mode="logical"),
        regions=(
            Region(
                id="region.stem",
                role="stem",
                flow="absolute",
                slot_ids=(
                    "slot.qtext1",
                    "slot.lb.da_text.copy1",
                    "slot.inserted.arc.1.copy5.copy7.copy10",
                    "slot.inserted.arc.1.copy5.copy7.copy10.copy11",
                    "slot.inserted.arc.1.copy5.copy7.copy10.copy11.copy12",
                ),
            ),
            Region(
                id="region.diagram",
                role="diagram",
                flow="absolute",
                slot_ids=(
                    "slot.circle",
                    "slot.line.c",
                    "slot.line.j",
                    "slot.line.k",
                    "slot.pt.center",
                ),
            ),
            Region(id="region.choice", role="choice", flow="absolute", slot_ids=("slot.choice",)),
            Region(id="region.footer", role="footer", flow="absolute", slot_ids=()),
        ),
        slots=(
            TextSlot(
                id="slot.qtext1",
                prompt="",
                text="원의 반지름과 지름을 나타내는 선분을 각각 찾아 보세요.",
                style_role="question",
                x=40,
                y=35,
                font_size=28,
                fill="#111111",
            ),
            CircleSlot(
                id="slot.circle",
                prompt="",
                cx=385,
                cy=210,
                r=125,
                fill="none",
                stroke="#111111",
                stroke_width=2,
            ),
            LineSlot(id="slot.line.c", prompt="", x1=385, y1=210, x2=510, y2=210),
            LineSlot(id="slot.line.j", prompt="", x1=385, y1=85, x2=385, y2=335),
            LineSlot(id="slot.line.k", prompt="", x1=265, y1=170, x2=385, y2=85),
            CircleSlot(id="slot.pt.center", prompt="", cx=385, cy=210, r=5, fill="#ff4da6"),
            TextSlot(
                id="slot.lb.ga_text",
                prompt="",
                text="ㄱ",
                style_role="label",
                x=305,
                y=125,
                font_size=20,
                fill="#111111",
            ),
            TextSlot(
                id="slot.lb.na_text",
                prompt="",
                text="ㄴ",
                style_role="label",
                x=330,
                y=215,
                font_size=20,
                fill="#111111",
            ),
            TextSlot(
                id="slot.lb.da_text",
                prompt="",
                text="ㄷ",
                style_role="label",
                x=435,
                y=180,
                font_size=20,
                fill="#111111",
            ),
            TextSlot(
                id="slot.choice",
                prompt="",
                text="원의 반지름 (ㄱ, ㄴ, ㄷ), 원의 지름 (ㄱ, ㄴ, ㄷ)",
                style_role="question",
                x=70,
                y=390,
                font_size=30,
            ),
            TextSlot(
                id="slot.lb.da_text.copy1",
                prompt="",
                text="ㅇ",
                x=365,
                y=205,
                font_size=20,
                fill="#111111",
            ),
            PathSlot(
                id="slot.inserted.arc.1.copy5.copy7.copy10",
                prompt="",
                d="M 245 135 A 65 10 0 0 1 390 135",
                fill="#ffffff",
                stroke="#111827",
                stroke_width=1.5,
                stroke_dasharray="10 6",
                transform="rotate(-395 317.5 121.06)",
            ),
            PathSlot(
                id="slot.inserted.arc.1.copy5.copy7.copy10.copy11",
                prompt="",
                d="M 202 176 A 110 25 0 0 1 442 176",
                fill="#ffffff",
                stroke="#111827",
                stroke_width=1.5,
                stroke_dasharray="10 6",
                transform="rotate(-450 369.5 162.06)",
            ),
            PathSlot(
                id="slot.inserted.arc.1.copy5.copy7.copy10.copy11.copy12",
                prompt="",
                d="M 390 205 A 50 10 0 0 1 510 205",
                fill="#ffffff",
                stroke="#111827",
                stroke_width=1.5,
                stroke_dasharray="10 6",
                transform="rotate(-360 512 192.05)",
            ),
        ),
        diagrams=(),
        groups=(),
        constraints=(),
        tags=(),
    )


PROBLEM_TEMPLATE = build_problem_template()

SEMANTIC_OVERRIDE = {
    "problem_id": "S3_초등_3_008691",
    "problem_type": "도형_선분_분류",
    "metadata": {
        "language": "ko",
        "question": "원의 반지름과 지름을 나타내는 선분을 각각 찾아 보세요.",
        "instruction": "선분을 분류하여 반지름과 지름을 찾는다.",
        "points": 0,
    },
    "domain": {
        "objects": [
            {"id": "obj.circle", "type": "circle"},
            {"id": "obj.center", "type": "point", "role": "center"},
            {"id": "obj.segment.ga", "type": "segment_label", "label": "ㄱ"},
            {"id": "obj.segment.na", "type": "segment_label", "label": "ㄴ"},
            {"id": "obj.segment.da", "type": "segment_label", "label": "ㄷ"},
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
                "condition_refs": ["rel.radius_candidate", "rel.diameter_candidate"],
            },
            "plan": {
                "method": "definition_matching",
                "description": "원에서 중심과 둘레의 관계를 보고 반지름과 지름에 해당하는 선분을 고른다.",
            },
            "execute": {
                "expected_operations": [
                    "identify_center_to_circle_edge",
                    "identify_through_center_across_circle",
                ]
            },
            "review": {"check_methods": ["definition_check", "label_match_check"]},
        },
    },
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {
            "type": "selected_segments",
            "description": "원의 반지름과 지름에 해당하는 선분",
        },
        "value": "ㄷ, ㄴ",
        "unit": "",
    },
}

SOLVABLE = {
    "schema": "modu.solvable.v1.1",
    "problem_id": "S3_초등_3_008691",
    "problem_type": "도형_선분_분류",
    "inputs": {
        "total_ticks": 1,
        "target_label": "원의 반지름과 지름을 나타내는 선분",
        "target_ticks": 1,
        "target_count": 2,
        "unit": "",
    },
    "given": [
        {"ref": "obj.circle", "value": "circle"},
        {"ref": "obj.center", "value": "center_point"},
        {"ref": "obj.segment.ga", "value": "ㄱ"},
        {"ref": "obj.segment.na", "value": "ㄴ"},
        {"ref": "obj.segment.da", "value": "ㄷ"},
    ],
    "target": {"ref": "answer.target", "type": "selected_segments"},
    "method": "definition_matching",
    "plan": [
        "원에서 중심과 둘레를 잇는 선분이 반지름인지 확인한다.",
        "원에서 중심을 지나 양쪽 둘레를 잇는 선분이 지름인지 확인한다.",
    ],
    "steps": [
        {"id": "step.1", "expr": "반지름 후보를 선분 라벨에서 찾기", "value": "ㄷ"},
        {"id": "step.2", "expr": "지름 후보를 선분 라벨에서 찾기", "value": "ㄴ"},
    ],
    "checks": [
        {
            "id": "check.1",
            "expr": "반지름은 중심에서 원 둘레까지의 선분인가",
            "expected": "ㄷ",
            "actual": "ㄷ",
            "pass": True,
        },
        {
            "id": "check.2",
            "expr": "지름은 중심을 지나 원의 양쪽 둘레를 잇는 선분인가",
            "expected": "ㄴ",
            "actual": "ㄴ",
            "pass": True,
        },
    ],
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {
            "type": "selected_segments",
            "description": "원의 반지름과 지름에 해당하는 선분",
        },
        "value": "ㄷ, ㄴ",
        "unit": "",
    },
}
