from __future__ import annotations
from modu_math.dsl import Canvas, CircleSlot, LineSlot, ProblemTemplate, RectSlot, Region, TextSlot


def build_problem_template() -> ProblemTemplate:
    return ProblemTemplate(
        id="S3_초등_3_008700",
        title="원의 지름 찾기",
        canvas=Canvas(width=960, height=608, coordinate_mode="logical"),
        regions=(
            Region(id="region.stem", role="stem", flow="absolute", slot_ids=("slot.q1",)),
            Region(
                id="region.diagram",
                role="diagram",
                flow="absolute",
                slot_ids=(
                    "slot.diagram.circle",
                    "slot.diagram.line1",
                    "slot.diagram.line2",
                    "slot.diagram.line3",
                    "slot.diagram.line4",
                    "slot.diagram.line5",
                    "slot.diagram.center",
                ),
            ),
            Region(
                id="region.explanation",
                role="explanation",
                flow="absolute",
                slot_ids=("slot.box", "slot.box_line1", "slot.box_arrow", "slot.box_line2"),
            ),
            Region(id="region.answer", role="answer", flow="absolute", slot_ids=()),
        ),
        slots=(
            TextSlot(
                id="slot.q1",
                prompt="",
                text="그림을 보고 □ 안에 공통으로 들어갈 선분을 찾아 기호를 선택하세요.  ",
                style_role="question",
                x=10.0,
                y=28.0,
                font_size=28,
            ),
            CircleSlot(id="slot.diagram.circle", prompt="", cx=430, cy=210, r=125, fill="none"),
            LineSlot(id="slot.diagram.line1", prompt="", x1=345, y1=120, x2=350, y2=305),
            LineSlot(id="slot.diagram.line2", prompt="", x1=390, y1=90, x2=395, y2=330),
            LineSlot(id="slot.diagram.line3", prompt="", x1=431, y1=85, x2=431, y2=335),
            LineSlot(
                id="slot.diagram.line4",
                prompt="",
                x1=473.86163330078125,
                y1=93.3836669921875,
                x2=475,
                y2=325,
            ),
            LineSlot(id="slot.diagram.line5", prompt="", x1=510, y1=115, x2=510, y2=305),
            CircleSlot(id="slot.diagram.center", prompt="", cx=430, cy=210, r=5, fill="#e84aa6"),
            TextSlot(
                id="slot.diagram.label1_text",
                prompt="",
                text="ㄱ",
                style_role="label",
                x=324.7295455932617,
                y=114.8124771118164,
                font_size=20,
                fill="#111111",
            ),
            TextSlot(
                id="slot.diagram.label2_text",
                prompt="",
                text="ㄴ",
                style_role="label",
                x=367.61014556884766,
                y=79.46142578125,
                font_size=20,
                fill="#111111",
            ),
            TextSlot(
                id="slot.diagram.label3_text",
                prompt="",
                text="ㄷ",
                style_role="label",
                x=421.5088348388672,
                y=69.68378067016602,
                font_size=20,
                fill="#111111",
            ),
            TextSlot(
                id="slot.diagram.label4_text",
                prompt="",
                text="ㄹ",
                style_role="label",
                x=464.4242248535156,
                y=85,
                font_size=20,
                fill="#111111",
            ),
            TextSlot(
                id="slot.diagram.label5_text",
                prompt="",
                text="ㅁ",
                style_role="label",
                x=515.337890625,
                y=106.29962158203125,
                font_size=20,
                fill="#111111",
            ),
            RectSlot(id="slot.box", prompt="", x=70, y=355, width=650, height=125, fill="#dcd7f2"),
            TextSlot(
                id="slot.box_line1",
                prompt="",
                text="길이가 가장 긴 선분은 □입니다.",
                style_role="body",
                x=210,
                y=405,
                font_size=30,
            ),
            TextSlot(
                id="slot.box_arrow",
                prompt="",
                text="→",
                style_role="body",
                x=250,
                y=455,
                font_size=30,
            ),
            TextSlot(
                id="slot.box_line2",
                prompt="",
                text="원의 지름은 □입니다.",
                style_role="body",
                x=285,
                y=460,
                font_size=30,
            ),
        ),
        diagrams=(),
        groups=(),
        constraints=(),
        tags=(),
    )


PROBLEM_TEMPLATE = build_problem_template()

SEMANTIC_OVERRIDE = {
    "problem_id": "S3_초등_3_008700",
    "problem_type": "circle_segment_identification",
    "metadata": {
        "language": "ko",
        "question": "그림을 보고 공통으로 들어갈 선분을 찾는 문제",
        "instruction": "그림을 보고 □ 안에 공통으로 들어갈 선분을 찾아 기호를 선택하세요.",
    },
    "domain": {
        "objects": [
            {"id": "obj.circle", "type": "circle"},
            {"id": "obj.segments", "type": "segment_collection"},
            {
                "id": "obj.diameter",
                "type": "segment_property",
                "property": "longest_segment_in_circle",
            },
        ],
        "relations": [],
        "problem_solving": {
            "understand": {
                "given_refs": ["obj.circle", "obj.segments"],
                "target_ref": "answer.target",
                "condition_refs": ["rel.longest_is_diameter"],
            },
            "plan": {
                "method": "diagram_comparison",
                "description": "원 안의 여러 선분을 비교하여 가장 긴 선분이 무엇인지 찾는다.",
            },
            "execute": {
                "expected_operations": [
                    "compare_segments",
                    "identify_longest_segment",
                    "match_with_diameter_property",
                ]
            },
            "review": {"check_methods": ["property_consistency_check"]},
        },
    },
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {"type": "segment_symbol", "description": "길이가 가장 긴 선분과 같은 기호"},
        "value": "㉡",
        "unit": "",
    },
}

SOLVABLE = {
    "schema": "modu.solvable.v1.1",
    "problem_id": "S3_초등_3_008700",
    "problem_type": "circle_segment_identification",
    "inputs": {
        "total_ticks": 0,
        "target_label": "길이가 가장 긴 선분",
        "target_ticks": 0,
        "target_count": 1,
        "unit": "",
    },
    "given": [
        {"ref": "obj.circle", "value": "circle"},
        {"ref": "obj.segments", "value": "multiple segments in a circle"},
    ],
    "target": {"ref": "answer.target", "type": "segment_symbol"},
    "method": "diagram_comparison",
    "plan": [
        "원 안의 선분들을 비교한다.",
        "가장 긴 선분을 찾는다.",
        "그 선분이 원의 지름인지 확인한다.",
    ],
    "steps": [
        {"id": "step.1", "expr": "원 안의 여러 선분을 비교한다.", "value": "comparison"},
        {
            "id": "step.2",
            "expr": "가장 긴 선분은 원의 중심을 지나는 선분이다.",
            "value": "diameter",
        },
        {"id": "step.3", "expr": "문항의 선택 기호를 해당 선분과 연결한다.", "value": "㉡"},
    ],
    "checks": [
        {
            "id": "check.1",
            "expr": "가장 긴 선분 = 원의 지름",
            "expected": True,
            "actual": True,
            "pass": True,
        }
    ],
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {"type": "segment_symbol", "description": "길이가 가장 긴 선분과 같은 기호"},
        "value": "㉡",
        "unit": "",
    },
}
