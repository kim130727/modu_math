from __future__ import annotations
from modu_math.dsl import (
    Canvas,
    ProblemTemplate,
    Region,
    TextSlot,
    RectSlot,
    LineSlot,
    CircleSlot,
    PathSlot,
)


def build_problem_template() -> ProblemTemplate:
    return ProblemTemplate(
        id="S3_초등_3_009034",
        title="OX 판단 문제",
        canvas=Canvas(width=960, height=420, coordinate_mode="logical"),
        regions=(
            Region(
                id="region.header",
                role="stem",
                flow="absolute",
                slot_ids=("slot.qnum", "slot.qstem"),
            ),
            Region(
                id="region.diagram",
                role="diagram",
                flow="absolute",
                slot_ids=(
                    "slot.step1.rect",
                    "slot.step1.diag",
                    "slot.step1.note",
                    "slot.arrow1",
                    "slot.step2.rect",
                    "slot.step2.fold",
                    "slot.step2.note",
                    "slot.arrow2",
                    "slot.step3.rect",
                    "slot.step3.fold",
                    "slot.step3.scissors",
                    "slot.step3.note",
                    "slot.arrow3",
                    "slot.step4.rect",
                    "slot.step4.diag",
                    "slot.step4.curve",
                    "slot.step4.note",
                ),
            ),
            Region(id="region.center", role="stem", flow="absolute", slot_ids=("slot.claim",)),
            Region(
                id="region.answer",
                role="answer",
                flow="absolute",
                slot_ids=("slot.choice.o", "slot.choice.x"),
            ),
        ),
        slots=(
            TextSlot(
                id="slot.qnum",
                prompt="",
                text="72.",
                style_role="question",
                x=20.0,
                y=28.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.qstem",
                prompt="",
                text="직사각형 모양의 종이로 그림과 같은 모양을 만들었습니다. 다음을 읽고 O, X를 고르세요.",
                style_role="question",
                x=58.0,
                y=28.0,
                font_size=28,
            ),
            RectSlot(id="slot.step1.rect", prompt="", x=38.0, y=84.0, width=120.0, height=84.0),
            LineSlot(id="slot.step1.diag", prompt="", x1=44.0, y1=90.0, x2=128.0, y2=166.0),
            TextSlot(
                id="slot.step1.note",
                prompt="",
                text="접선을 따라 접어요.",
                style_role="annotation",
                x=114.0,
                y=190.0,
                font_size=24,
            ),
            TextSlot(
                id="slot.arrow1",
                prompt="",
                text="→",
                style_role="annotation",
                x=178.0,
                y=132.0,
                font_size=34,
            ),
            RectSlot(id="slot.step2.rect", prompt="", x=274.0, y=84.0, width=120.0, height=84.0),
            LineSlot(id="slot.step2.fold", prompt="", x1=274.0, y1=84.0, x2=350.0, y2=168.0),
            TextSlot(
                id="slot.step2.note",
                prompt="",
                text="",
                style_role="annotation",
                x=0.0,
                y=0.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.arrow2",
                prompt="",
                text="→",
                style_role="annotation",
                x=414.0,
                y=132.0,
                font_size=34,
            ),
            RectSlot(id="slot.step3.rect", prompt="", x=510.0, y=84.0, width=120.0, height=84.0),
            LineSlot(id="slot.step3.fold", prompt="", x1=510.0, y1=84.0, x2=586.0, y2=168.0),
            PathSlot(
                id="slot.step3.scissors",
                prompt="",
                d="M 578.0 164.0 C 582.0 174.0, 582.0 182.0, 578.0 190.0",
            ),
            TextSlot(
                id="slot.step3.note",
                prompt="",
                text="",
                style_role="annotation",
                x=0.0,
                y=0.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.arrow3",
                prompt="",
                text="→",
                style_role="annotation",
                x=650.0,
                y=132.0,
                font_size=34,
            ),
            RectSlot(id="slot.step4.rect", prompt="", x=726.0, y=84.0, width=120.0, height=84.0),
            LineSlot(id="slot.step4.diag", prompt="", x1=738.0, y1=90.0, x2=820.0, y2=166.0),
            PathSlot(
                id="slot.step4.curve",
                prompt="",
                d="M 790.0 110.0 C 812.0 112.0, 813.0 136.0, 790.0 142.0",
            ),
            TextSlot(
                id="slot.step4.note",
                prompt="",
                text="잘라낸 모양을 펼쳐요.",
                style_role="annotation",
                x=790.0,
                y=190.0,
                font_size=24,
            ),
            TextSlot(
                id="slot.claim",
                prompt="",
                text="만든 모양의 네 변의 길이는 모두 같습니다.",
                style_role="question",
                x=230.0,
                y=252.0,
                font_size=30,
            ),
            CircleSlot(id="slot.choice.o", prompt="", cx=22.0, cy=338.0, r=8.0, fill="#ffffff"),
            CircleSlot(id="slot.choice.x", prompt="", cx=476.0, cy=338.0, r=8.0, fill="#ffffff"),
        ),
        diagrams=(),
        groups=(),
        constraints=(),
        tags=(),
    )


PROBLEM_TEMPLATE = build_problem_template()

SEMANTIC_OVERRIDE = {
    "problem_id": "S3_초등_3_009034",
    "problem_type": "ox_judgement",
    "metadata": {
        "language": "ko",
        "question": "직사각형 모양의 종이로 만든 모양에 대한 O, X 판단 문제",
        "instruction": "문장을 읽고 O, X를 고르기",
    },
    "domain": {
        "objects": [
            {"id": "obj.paper", "type": "paper_shape", "description": "직사각형 종이"},
            {
                "id": "obj.result_shape",
                "type": "shape",
                "description": "접고 자르고 펼친 뒤의 모양",
            },
            {
                "id": "obj.statement",
                "type": "claim",
                "description": "만든 모양의 네 변의 길이는 모두 같습니다.",
            },
        ],
        "relations": [],
        "problem_solving": {
            "understand": {
                "given_refs": ["obj.paper", "obj.statement"],
                "target_ref": "answer.target",
                "condition_refs": ["rel.transform", "rel.judgement"],
            },
            "plan": {
                "method": "ox_judgement",
                "description": "그림의 도형 변형 과정을 보고 문장의 참·거짓을 판단한다.",
            },
            "execute": {
                "expected_operations": [
                    "observe_sequence",
                    "match_statement_to_result_shape",
                    "choose_ox",
                ]
            },
            "review": {"check_methods": ["statement_consistency_check"]},
        },
    },
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {
            "type": "ox_choice",
            "description": "만든 모양의 네 변의 길이는 모두 같습니다.에 대한 O, X",
        },
        "value": 0,
        "unit": "",
    },
}

SOLVABLE = {
    "schema": "modu.solvable.v1.1",
    "problem_id": "S3_초등_3_009034",
    "problem_type": "ox_judgement",
    "inputs": {
        "total_ticks": 1,
        "target_label": "O, X",
        "target_ticks": 1,
        "target_count": 1,
        "unit": "",
    },
    "given": [
        {"ref": "obj.paper", "value": {"type": "rectangle_paper"}},
        {"ref": "obj.statement", "value": {"text": "만든 모양의 네 변의 길이는 모두 같습니다."}},
    ],
    "target": {"ref": "answer.target", "type": "ox_choice"},
    "method": "ox_judgement",
    "plan": [
        "그림의 종이 접기, 자르기, 펼치기 과정을 확인한다.",
        "판단 문장이 만들어진 모양의 성질과 맞는지 살핀다.",
    ],
    "steps": [
        {"id": "step.1", "expr": "그림의 변형 과정을 관찰한다.", "value": 0},
        {"id": "step.2", "expr": "판단 문장과 결과 모양의 성질을 대응한다.", "value": 0},
    ],
    "checks": [
        {
            "id": "check.1",
            "expr": "문장과 그림의 내용이 일치하는지 확인한다.",
            "expected": 0,
            "actual": 0,
            "pass": False,
        }
    ],
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {
            "type": "ox_choice",
            "description": "만든 모양의 네 변의 길이는 모두 같습니다.에 대한 O, X",
        },
        "value": 0,
        "unit": "",
    },
}
