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
        id="S3_초등_3_008652",
        title="그림의 규칙을 바르게 말한 사람 선택하기",
        canvas=Canvas(width=960, height=620, coordinate_mode="logical"),
        regions=(
            Region(
                id="region.header",
                role="stem",
                flow="absolute",
                slot_ids=("slot.qnum", "slot.qtext"),
            ),
            Region(
                id="region.diagram",
                role="diagram",
                flow="absolute",
                slot_ids=(
                    "slot.grid.frame",
                    "slot.grid.v1",
                    "slot.grid.v2",
                    "slot.grid.v3",
                    "slot.grid.v4",
                    "slot.grid.v5",
                    "slot.grid.v6",
                    "slot.grid.v7",
                    "slot.grid.v8",
                    "slot.grid.v9",
                    "slot.grid.v10",
                    "slot.grid.v11",
                    "slot.grid.v12",
                    "slot.grid.h1",
                    "slot.grid.h2",
                    "slot.grid.h3",
                    "slot.grid.h4",
                    "slot.grid.h5",
                    "slot.grid.h6",
                    "slot.grid.h7",
                    "slot.grid.h8",
                    "slot.grid.h9",
                    "slot.grid.h10",
                    "slot.grid.h11",
                    "slot.grid.h12",
                    "slot.circle.outer",
                    "slot.circle.middle",
                    "slot.circle.inner",
                    "slot.center",
                ),
            ),
            Region(
                id="region.characters",
                role="diagram",
                flow="absolute",
                slot_ids=(
                    "slot.sunga.face",
                    "slot.sunga.body",
                    "slot.sunga.namebox",
                    "slot.sunga.name",
                    "slot.sunga.bubble",
                    "slot.sunga.b1",
                    "slot.sunga.b2",
                    "slot.sunga.b3",
                    "slot.sunga.b4",
                    "slot.jaewon.face",
                    "slot.jaewon.body",
                    "slot.jaewon.namebox",
                    "slot.jaewon.name",
                    "slot.jaewon.bubble",
                    "slot.jaewon.b1",
                    "slot.jaewon.b2",
                    "slot.jaewon.b3",
                    "slot.jaewon.b4",
                ),
            ),
            Region(id="region.footer", role="stem", flow="absolute", slot_ids=()),
        ),
        slots=(
            TextSlot(
                id="slot.qnum",
                prompt="",
                text="27.",
                style_role="question",
                x=20.0,
                y=42.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.qtext",
                prompt="",
                text="규칙에 따라 원을 그린 것입니다. 그린 규칙을 바르게 말한 사람을 선택해 보세요.",
                style_role="question",
                x=64.0,
                y=42.0,
                font_size=28,
            ),
            RectSlot(
                id="slot.grid.frame",
                prompt="",
                x=110.0,
                y=150.0,
                width=280.0,
                height=280.0,
            ),
            LineSlot(
                id="slot.grid.v1", prompt="", x1=110.0, y1=150.0, x2=110.0, y2=430.0
            ),
            LineSlot(
                id="slot.grid.v2", prompt="", x1=133.3, y1=150.0, x2=133.3, y2=430.0
            ),
            LineSlot(
                id="slot.grid.v3", prompt="", x1=156.7, y1=150.0, x2=156.7, y2=430.0
            ),
            LineSlot(
                id="slot.grid.v4", prompt="", x1=180.0, y1=150.0, x2=180.0, y2=430.0
            ),
            LineSlot(
                id="slot.grid.v5", prompt="", x1=203.3, y1=150.0, x2=203.3, y2=430.0
            ),
            LineSlot(
                id="slot.grid.v6", prompt="", x1=226.7, y1=150.0, x2=226.7, y2=430.0
            ),
            LineSlot(
                id="slot.grid.v7", prompt="", x1=250.0, y1=150.0, x2=250.0, y2=430.0
            ),
            LineSlot(
                id="slot.grid.v8", prompt="", x1=273.3, y1=150.0, x2=273.3, y2=430.0
            ),
            LineSlot(
                id="slot.grid.v9", prompt="", x1=296.7, y1=150.0, x2=296.7, y2=430.0
            ),
            LineSlot(
                id="slot.grid.v10", prompt="", x1=320.0, y1=150.0, x2=320.0, y2=430.0
            ),
            LineSlot(
                id="slot.grid.v11", prompt="", x1=343.3, y1=150.0, x2=343.3, y2=430.0
            ),
            LineSlot(
                id="slot.grid.v12", prompt="", x1=366.7, y1=150.0, x2=366.7, y2=430.0
            ),
            LineSlot(
                id="slot.grid.h1", prompt="", x1=110.0, y1=150.0, x2=390.0, y2=150.0
            ),
            LineSlot(
                id="slot.grid.h2", prompt="", x1=110.0, y1=173.3, x2=390.0, y2=173.3
            ),
            LineSlot(
                id="slot.grid.h3", prompt="", x1=110.0, y1=196.7, x2=390.0, y2=196.7
            ),
            LineSlot(
                id="slot.grid.h4", prompt="", x1=110.0, y1=220.0, x2=390.0, y2=220.0
            ),
            LineSlot(
                id="slot.grid.h5", prompt="", x1=110.0, y1=243.3, x2=390.0, y2=243.3
            ),
            LineSlot(
                id="slot.grid.h6", prompt="", x1=110.0, y1=266.7, x2=390.0, y2=266.7
            ),
            LineSlot(
                id="slot.grid.h7", prompt="", x1=110.0, y1=290.0, x2=390.0, y2=290.0
            ),
            LineSlot(
                id="slot.grid.h8", prompt="", x1=110.0, y1=313.3, x2=390.0, y2=313.3
            ),
            LineSlot(
                id="slot.grid.h9", prompt="", x1=110.0, y1=336.7, x2=390.0, y2=336.7
            ),
            LineSlot(
                id="slot.grid.h10", prompt="", x1=110.0, y1=360.0, x2=390.0, y2=360.0
            ),
            LineSlot(
                id="slot.grid.h11", prompt="", x1=110.0, y1=383.3, x2=390.0, y2=383.3
            ),
            LineSlot(
                id="slot.grid.h12", prompt="", x1=110.0, y1=406.7, x2=390.0, y2=406.7
            ),
            CircleSlot(
                id="slot.circle.outer",
                prompt="",
                cx=250.0,
                cy=290.0,
                r=116.0,
                fill="none",
            ),
            CircleSlot(
                id="slot.circle.middle",
                prompt="",
                cx=250.0,
                cy=290.0,
                r=71.0,
                fill="none",
            ),
            CircleSlot(
                id="slot.circle.inner",
                prompt="",
                cx=250.0,
                cy=290.0,
                r=23.0,
                fill="none",
            ),
            CircleSlot(
                id="slot.center", prompt="", cx=250.0, cy=290.0, r=4.0, fill="#ff4da6"
            ),
            CircleSlot(
                id="slot.sunga.face",
                prompt="",
                cx=565.0,
                cy=145.0,
                r=28.0,
                fill="#f6d3b0",
            ),
            RectSlot(
                id="slot.sunga.body",
                prompt="",
                x=538.0,
                y=168.0,
                width=54.0,
                height=50.0,
            ),
            RectSlot(
                id="slot.sunga.namebox",
                prompt="",
                x=535.0,
                y=236.0,
                width=60.0,
                height=36.0,
            ),
            TextSlot(
                id="slot.sunga.name",
                prompt="",
                text="승아",
                style_role="label",
                x=553.0,
                y=262.0,
                font_size=28,
            ),
            RectSlot(
                id="slot.sunga.bubble",
                prompt="",
                x=610.0,
                y=74.0,
                width=250.0,
                height=175.0,
            ),
            TextSlot(
                id="slot.sunga.b1",
                prompt="",
                text="원의 중심이 모두",
                style_role="speech",
                x=667.0,
                y=114.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.sunga.b2",
                prompt="",
                text="다르고 원의 반지름이",
                style_role="speech",
                x=640.0,
                y=148.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.sunga.b3",
                prompt="",
                text="모눈 1칸씩 늘어나게",
                style_role="speech",
                x=633.0,
                y=182.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.sunga.b4",
                prompt="",
                text="그렸어요.",
                style_role="speech",
                x=695.0,
                y=216.0,
                font_size=28,
            ),
            CircleSlot(
                id="slot.jaewon.face",
                prompt="",
                cx=565.0,
                cy=360.0,
                r=28.0,
                fill="#f6d3b0",
            ),
            RectSlot(
                id="slot.jaewon.body",
                prompt="",
                x=538.0,
                y=383.0,
                width=54.0,
                height=50.0,
            ),
            RectSlot(
                id="slot.jaewon.namebox",
                prompt="",
                x=535.0,
                y=451.0,
                width=60.0,
                height=36.0,
            ),
            TextSlot(
                id="slot.jaewon.name",
                prompt="",
                text="재원",
                style_role="label",
                x=553.0,
                y=477.0,
                font_size=28,
            ),
            RectSlot(
                id="slot.jaewon.bubble",
                prompt="",
                x=610.0,
                y=289.0,
                width=250.0,
                height=175.0,
            ),
            TextSlot(
                id="slot.jaewon.b1",
                prompt="",
                text="원의 중심이 모두",
                style_role="speech",
                x=667.0,
                y=329.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.jaewon.b2",
                prompt="",
                text="같고 원의 반지름이",
                style_role="speech",
                x=640.0,
                y=363.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.jaewon.b3",
                prompt="",
                text="모눈 2칸씩 늘어나게",
                style_role="speech",
                x=633.0,
                y=397.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.jaewon.b4",
                prompt="",
                text="그렸어요.",
                style_role="speech",
                x=695.0,
                y=431.0,
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
    "problem_id": "S3_초등_3_008652",
    "problem_type": "rule_selection",
    "metadata": {
        "language": "ko",
        "question": "그림의 규칙을 바르게 말한 사람을 고르는 문제",
        "instruction": "그린 규칙을 바르게 말한 사람을 선택해 보세요.",
    },
    "domain": {
        "objects": [
            {"id": "obj.circles", "type": "circle_set", "count": 3},
            {"id": "obj.center", "type": "center_point"},
            {"id": "obj.grid", "type": "grid"},
            {"id": "obj.student.sunga", "type": "student", "name": "승아"},
            {"id": "obj.student.jaewon", "type": "student", "name": "재원"},
        ],
        "relations": [],
        "problem_solving": {
            "understand": {
                "given_refs": [
                    "obj.circles",
                    "obj.center",
                    "obj.student.sunga",
                    "obj.student.jaewon",
                ],
                "target_ref": "answer.target",
                "condition_refs": ["rel.same_center", "rel.radius_increase"],
            },
            "plan": {
                "method": "rule_matching",
                "description": "그림의 원이 어떤 규칙으로 그려졌는지 보고, 말풍선 설명과 맞는 사람을 고른다.",
            },
            "execute": {
                "expected_operations": [
                    "identify_same_center",
                    "recognize_increasing_radius_pattern",
                    "match_student_statement",
                ]
            },
            "review": {
                "check_methods": [
                    "compare_with_visible_answer_tag",
                    "confirm_rule_consistency",
                ]
            },
        },
    },
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {
            "type": "correct_student",
            "description": "그린 규칙을 바르게 말한 사람",
        },
        "value": "재원",
        "unit": "",
    },
}

SOLVABLE = {
    "schema": "modu.solvable.v1.1",
    "problem_id": "S3_초등_3_008652",
    "problem_type": "rule_selection",
    "inputs": {
        "total_ticks": 0,
        "target_label": "그린 규칙을 바르게 말한 사람",
        "target_ticks": 0,
        "target_count": 1,
        "unit": "",
    },
    "given": [
        {"ref": "obj.circles", "value": {"count": 3}},
        {"ref": "obj.center", "value": {"type": "center_point"}},
    ],
    "plan": "그림에서 같은 중심을 공유하는 원들의 반지름 규칙을 확인하고, 말풍선 내용과 맞는 학생을 찾는다.",
    "steps": [
        {"id": "step.1", "expr": "원 3개를 확인한다", "value": 3},
        {"id": "step.2", "expr": "중심이 같은지 확인한다", "value": True},
        {
            "id": "step.3",
            "expr": "반지름이 2칸씩 늘어나는 규칙과 일치하는 학생을 선택한다",
            "value": "재원",
        },
    ],
    "checks": [
        {
            "id": "check.1",
            "expr": "그림의 규칙이 동심원인지 확인",
            "expected": True,
            "actual": True,
            "pass": True,
        },
        {
            "id": "check.2",
            "expr": "정답 표기와 선택 학생이 일치하는지 확인",
            "expected": "재원",
            "actual": "재원",
            "pass": True,
        },
    ],
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {
            "type": "correct_student",
            "description": "그린 규칙을 바르게 말한 사람",
        },
        "value": "재원",
        "unit": "",
    },
}
