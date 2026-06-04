from __future__ import annotations
from modu_math.dsl import (
    Canvas,
    CircleSlot,
    ProblemTemplate,
    RectSlot,
    Region,
    TextSlot,
    LineSlot,
)


def build_problem_template() -> ProblemTemplate:
    return ProblemTemplate(
        id="S3_초등_3_008662",
        title="원의 지름은 어느 선분인가요?",
        canvas=Canvas(width=661.0, height=388.0, coordinate_mode="logical"),
        regions=(
            Region(
                id="region.header",
                role="stem",
                flow="absolute",
                slot_ids=("slot.icon", "slot.qnum", "slot.question"),
            ),
            Region(
                id="region.diagram",
                role="diagram",
                flow="absolute",
                slot_ids=(
                    "slot.circle",
                    "slot.line.1",
                    "slot.line.2",
                    "slot.line.3",
                    "slot.line.4",
                    "slot.pt.o",
                    "slot.pt.pink",
                    "slot.lb.g1",
                    "slot.lb.g2",
                    "slot.lb.d1",
                    "slot.lb.d2",
                    "slot.lb.m1",
                    "slot.lb.m2",
                    "slot.lb.s1",
                    "slot.lb.s2",
                ),
            ),
            Region(
                id="region.options",
                role="choices",
                flow="absolute",
                slot_ids=("slot.opt.1", "slot.opt.2", "slot.opt.3", "slot.opt.4"),
            ),
            Region(
                id="region.footer", role="explanation", flow="absolute", slot_ids=()
            ),
        ),
        slots=(
            RectSlot(
                id="slot.icon", prompt="", x=16.0, y=17.0, width=10.0, height=10.0
            ),
            TextSlot(
                id="slot.qnum",
                prompt="",
                text="37.",
                style_role="question",
                x=37.0,
                y=29.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.question",
                prompt="",
                text="원의 지름은 어느 선분인가요?",
                style_role="question",
                x=85.0,
                y=30.0,
                font_size=28,
            ),
            CircleSlot(
                id="slot.circle", prompt="", cx=482.0, cy=115.0, r=75.0, fill="none"
            ),
            LineSlot(id="slot.line.1", prompt="", x1=440.0, y1=75.0, x2=548.0, y2=75.0),
            LineSlot(
                id="slot.line.2", prompt="", x1=430.0, y1=104.0, x2=552.0, y2=104.0
            ),
            LineSlot(
                id="slot.line.3", prompt="", x1=430.0, y1=125.0, x2=552.0, y2=125.0
            ),
            LineSlot(
                id="slot.line.4", prompt="", x1=430.0, y1=154.0, x2=552.0, y2=154.0
            ),
            CircleSlot(
                id="slot.pt.o", prompt="", cx=482.0, cy=107.0, r=4.0, fill="none"
            ),
            CircleSlot(
                id="slot.pt.pink", prompt="", cx=482.0, cy=118.0, r=2.6, fill="#ff3aa0"
            ),
            TextSlot(
                id="slot.lb.g1",
                prompt="",
                text="ㄱ",
                style_role="label",
                x=418.0,
                y=78.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.lb.g2",
                prompt="",
                text="ㄴ",
                style_role="label",
                x=556.0,
                y=78.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.lb.d1",
                prompt="",
                text="ㄷ",
                style_role="label",
                x=416.0,
                y=108.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.lb.d2",
                prompt="",
                text="ㄹ",
                style_role="label",
                x=556.0,
                y=108.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.lb.m1",
                prompt="",
                text="ㅁ",
                style_role="label",
                x=416.0,
                y=131.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.lb.m2",
                prompt="",
                text="ㅂ",
                style_role="label",
                x=556.0,
                y=131.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.lb.s1",
                prompt="",
                text="ㅅ",
                style_role="label",
                x=416.0,
                y=159.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.lb.s2",
                prompt="",
                text="ㅈ",
                style_role="label",
                x=556.0,
                y=159.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.opt.1",
                prompt="",
                text="① 선분 ㄱㄴ",
                style_role="choice",
                x=31.0,
                y=241.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.opt.2",
                prompt="",
                text="② 선분 ㄷㄹ",
                style_role="choice",
                x=483.0,
                y=241.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.opt.3",
                prompt="",
                text="③ 선분 ㅁㅂ",
                style_role="choice",
                x=31.0,
                y=282.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.opt.4",
                prompt="",
                text="④ 선분 ㅅㅈ",
                style_role="choice",
                x=483.0,
                y=282.0,
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
    "problem_id": "S3_초등_3_008662",
    "problem_type": "geometry_multiple_choice",
    "metadata": {
        "language": "ko",
        "question": "원의 지름은 어느 선분인가요?",
        "instruction": "보기에서 알맞은 선분을 고르시오.",
    },
    "domain": {
        "objects": [
            {"id": "obj.circle", "type": "circle"},
            {"id": "obj.segment.gn", "type": "segment", "label": "ㄱㄴ"},
            {"id": "obj.segment.dl", "type": "segment", "label": "ㄷㄹ"},
            {"id": "obj.segment.mb", "type": "segment", "label": "ㅁㅂ"},
            {"id": "obj.segment.sj", "type": "segment", "label": "ㅅㅈ"},
        ],
        "relations": [],
        "problem_solving": {
            "understand": {
                "given_refs": [
                    "obj.circle",
                    "obj.segment.gn",
                    "obj.segment.dl",
                    "obj.segment.mb",
                    "obj.segment.sj",
                ],
                "target_ref": "answer.target",
                "condition_refs": ["rel.diameter_candidate"],
            },
            "plan": {
                "method": "diagram_classification",
                "description": "원 안의 선분들 중 중심을 지나는 선분을 찾는다.",
            },
            "execute": {
                "expected_operations": [
                    "compare_segments_to_circle_center",
                    "select_matching_choice",
                ]
            },
            "review": {"check_methods": ["center_pass_check", "choice_label_check"]},
        },
    },
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {"type": "choice", "description": "원의 지름에 해당하는 보기"},
        "value": 2,
        "unit": "",
    },
}

SOLVABLE = {
    "schema": "modu.solvable.v1.1",
    "problem_id": "S3_초등_3_008662",
    "problem_type": "geometry_multiple_choice",
    "inputs": {
        "total_ticks": 4,
        "target_label": "지름",
        "target_ticks": 1,
        "target_count": 1,
        "unit": "",
    },
    "given": [
        {"ref": "obj.circle", "value": {"type": "circle"}},
        {"ref": "obj.segment.gn", "value": {"label": "ㄱㄴ"}},
        {"ref": "obj.segment.dl", "value": {"label": "ㄷㄹ"}},
        {"ref": "obj.segment.mb", "value": {"label": "ㅁㅂ"}},
        {"ref": "obj.segment.sj", "value": {"label": "ㅅㅈ"}},
    ],
    "target": {"ref": "answer.target", "type": "choice"},
    "method": "diagram_classification",
    "plan": [
        "그림에서 원의 중심을 지나는 선분을 찾는다.",
        "그 선분과 같은 표기를 가진 보기를 고른다.",
    ],
    "steps": [
        {"id": "step.1", "expr": "중심을 지나는 선분 확인", "value": "ㄷㄹ"},
        {"id": "step.2", "expr": "해당 보기 번호 확인", "value": 2},
    ],
    "checks": [
        {
            "id": "check.1",
            "expr": "선분 ㄷㄹ이 중심을 지나는가",
            "expected": True,
            "actual": True,
            "pass": True,
        },
        {
            "id": "check.2",
            "expr": "선택한 보기가 ②인가",
            "expected": 2,
            "actual": 2,
            "pass": True,
        },
    ],
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {"type": "choice", "description": "원의 지름에 해당하는 보기"},
        "value": 2,
        "unit": "",
    },
}
