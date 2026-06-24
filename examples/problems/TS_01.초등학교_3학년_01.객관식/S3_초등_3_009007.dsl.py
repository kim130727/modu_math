from __future__ import annotations
from modu_math.dsl import Canvas, ProblemTemplate, Region, RectSlot, TextSlot, LineSlot, CircleSlot


def build_problem_template() -> ProblemTemplate:
    return ProblemTemplate(
        id="S3_초등_3_009007",
        title="알맞은 말을 선택하세요",
        canvas=Canvas(width=410, height=312, coordinate_mode="logical"),
        regions=(
            Region(
                id="region.header",
                role="header",
                flow="absolute",
                slot_ids=("slot.chk", "slot.qnum", "slot.title"),
            ),
            Region(
                id="region.main_box",
                role="body",
                flow="absolute",
                slot_ids=(
                    "slot.box",
                    "slot.line",
                    "slot.pt.l",
                    "slot.pt.r",
                    "slot.body_text",
                    "slot.choice",
                ),
            ),
            Region(id="region.explanation", role="supporting", flow="absolute", slot_ids=()),
        ),
        slots=(
            TextSlot(
                id="slot.chk",
                prompt="",
                text="□",
                style_role="question",
                x=4.0,
                y=24.0,
                font_size=24,
            ),
            TextSlot(
                id="slot.qnum",
                prompt="",
                text="46.",
                style_role="question",
                x=34.0,
                y=24.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.title",
                prompt="",
                text="알맞은 말을 선택하세요.",
                style_role="question",
                x=70.0,
                y=24.0,
                font_size=28,
            ),
            RectSlot(
                id="slot.box",
                prompt="",
                x=8.0,
                y=48.0,
                width=388.0,
                height=144.0,
                stroke="#FFA24A",
                fill="none",
            ),
            LineSlot(
                id="slot.line",
                prompt="",
                x1=146.0,
                y1=118.0,
                x2=259.0,
                y2=80.0,
                stroke="#444444",
                stroke_width=2.0,
            ),
            CircleSlot(id="slot.pt.l", prompt="", cx=146.0, cy=118.0, r=3.6, fill="#333333"),
            CircleSlot(id="slot.pt.r", prompt="", cx=259.0, cy=80.0, r=3.6, fill="#333333"),
            TextSlot(
                id="slot.body_text",
                prompt="",
                text="두 점을 곧게 이은 선은",
                style_role="question",
                x=100.0,
                y=154.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.choice",
                prompt="",
                text="( 선분입니다, 선분이 아닙니다.)",
                style_role="question",
                x=24.0,
                y=186.0,
                font_size=28,
            ),
        ),
        diagrams=(),
        groups=(),
        constraints=(),
        tags=("초등수학", "선분", "용어판별"),
    )


PROBLEM_TEMPLATE = build_problem_template()

SEMANTIC_OVERRIDE = {
    "problem_id": "S3_초등_3_009007",
    "problem_type": "concept_choice",
    "metadata": {
        "language": "ko",
        "question": "두 점을 곧게 이은 선이 무엇인지 알맞은 말을 고르는 문제",
        "instruction": "알맞은 말을 선택하세요.",
    },
    "domain": {
        "objects": [
            {
                "id": "obj.figure",
                "type": "geometry_figure",
                "description": "두 점이 양 끝에 표시된 선 모양",
            },
            {"id": "obj.choice.segment", "type": "term", "text": "선분입니다"},
            {"id": "obj.choice.not_segment", "type": "term", "text": "선분이 아닙니다"},
        ],
        "relations": [],
        "problem_solving": {
            "understand": {
                "given_refs": ["obj.figure"],
                "target_ref": "answer.target",
                "condition_refs": ["rel.definition"],
            },
            "plan": {
                "method": "definition_matching",
                "description": "그림이 선분의 정의와 맞는지 보고 알맞은 말을 고른다.",
            },
            "execute": {
                "expected_operations": [
                    "figure_identification",
                    "definition_comparison",
                    "choice_selection",
                ]
            },
            "review": {"check_methods": ["definition_consistency_check"]},
        },
    },
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {"type": "choice_text", "description": "두 점을 곧게 이은 선에 대한 알맞은 말"},
        "value": 0,
        "unit": "",
    },
}

SOLVABLE = {
    "schema": "modu.solvable.v1.1",
    "problem_id": "S3_초등_3_009007",
    "problem_type": "concept_choice",
    "inputs": {
        "total_ticks": 1,
        "target_label": "두 점을 곧게 이은 선",
        "target_ticks": 1,
        "target_count": 1,
        "unit": "",
    },
    "given": [{"ref": "obj.figure", "value": {"description": "두 점이 양 끝에 표시된 선 모양"}}],
    "target": {"ref": "answer.target", "type": "choice_text"},
    "method": "definition_matching",
    "plan": [
        "그림의 의미를 확인하고 선분의 정의와 비교합니다.",
        "보기에서 알맞은 말을 선택합니다.",
    ],
    "steps": [
        {"id": "step.1", "expr": "그림이 두 점을 곧게 이은 선인지 확인한다.", "value": "확인됨"},
        {"id": "step.2", "expr": "선분의 정의와 비교한다.", "value": "일치"},
        {"id": "step.3", "expr": "알맞은 말을 선택한다.", "value": "선분입니다"},
    ],
    "checks": [
        {
            "id": "check.1",
            "expr": "definition_match(그림, 선분)",
            "expected": True,
            "actual": True,
            "pass": True,
        }
    ],
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {"type": "choice_text", "description": "두 점을 곧게 이은 선에 대한 알맞은 말"},
        "value": 0,
        "unit": "",
    },
}
