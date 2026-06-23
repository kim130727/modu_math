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
        id="S3_초등_3_008721",
        title="도형 판별 문제",
        canvas=Canvas(width=960, height=560, coordinate_mode="logical"),
        regions=(
            Region(
                id="region.stem",
                role="stem",
                flow="absolute",
                slot_ids=("slot.q1",
                    "slot.diagram.circle",
                    "slot.diagram.center",
                    "slot.diagram.line1",
                    "slot.diagram.line2",
                    "slot.diagram.line3",
                    "slot.diagram.label.ga",
                    "slot.diagram.label.na",
                    "slot.diagram.label.da",
                    "slot.diagram.label.ra",
                    "slot.diagram.label.ma",
                    "slot.diagram.label.sa",
                    "slot.diagram.label.ya",
                    "slot.q2",'slot.diagram.label.ya.copy3', 'slot.diagram.line1.copy7'),
            ),
        ),
        slots=(TextSlot(
                id="slot.q1",
                prompt="",
                text="바르게 설명하였으면 ○, 그렇지 않으면 ×를 선택하세요.",
                style_role="question",
                x=18.0,
                y=34.0,
                font_size=28,
            ),
            CircleSlot(
                id="slot.diagram.circle", prompt="", cx = 450, cy = 231, r=135, fill="none"
            ),
            CircleSlot(
                id="slot.diagram.center", prompt="", cx = 450, cy = 231, r=5, fill="#ff2a8a"
            ),
            LineSlot(
                id="slot.diagram.line1", prompt="", x1 = 480, y1 = 100, x2 = 490, y2 = 360),
            LineSlot(
                id="slot.diagram.line2", prompt="", x1 = 445, y1 = 95, x2 = 455, y2 = 365),
            LineSlot(id="slot.diagram.line3", prompt="", x1 = 350, y1 = 141, x2 = 450, y2 = 231),
            TextSlot(
                id="slot.diagram.label.ga",
                prompt="",
                text = 'ㄱ', style_role="label",
                x = 430, y = 90, font_size = 30),
            TextSlot(
                id="slot.diagram.label.na",
                prompt="",
                text = 'ㅅ', style_role="label",
                x = 470, y = 90, font_size = 30),
            TextSlot(
                id="slot.diagram.label.da",
                prompt="",
                text = 'ㄴ', style_role="label",
                x = 315, y = 140, font_size = 30),
            TextSlot(
                id="slot.diagram.label.ra",
                prompt="",
                text = 'ㅂ', style_role="label",
                x = 585, y = 175, font_size = 30),
            TextSlot(
                id="slot.diagram.label.ma",
                prompt="",
                text = 'ㄷ', style_role="label",
                x = 385, y = 385, font_size = 30),
            TextSlot(
                id="slot.diagram.label.sa",
                prompt="",
                text = 'ㄹ', style_role="label",
                x = 435, y = 395, font_size = 30),
            TextSlot(
                id="slot.diagram.label.ya",
                prompt="",
                text = 'ㅁ', style_role="label",
                x = 490, y = 380, font_size = 30),
            TextSlot(
                id="slot.q2",
                prompt="",
                text = '길이가 가장 긴 선분은 선분 ㅁㅅ이고, 원의 지름은 선분 ㄱㄷ입니다.', style_role="question",
                x = 25, y = 435, font_size = 30),TextSlot(id = 'slot.diagram.label.ya.copy3', prompt = '', text = 'ㅇ', x = 420, y = 255, font_size = 30, fill = '#111111'), LineSlot(id = 'slot.diagram.line1.copy7', prompt = '', x1 = 575, y1 = 180, x2 = 410, y2 = 360, stroke = '#111111', stroke_width = 2)),
        diagrams=(),
        groups=(),
        constraints=(),
        tags=(),
    )


PROBLEM_TEMPLATE = build_problem_template()

SEMANTIC_OVERRIDE = {
    "problem_id": "S3_초등_3_008721",
    "problem_type": "도형_참거짓판단",
    "metadata": {
        "language": "ko",
        "question": "바르게 설명하였으면 ○, 그렇지 않으면 ×를 선택하는 도형 판별 문제",
        "instruction": "그림을 보고 문장의 참/거짓을 판단한다.",
    },
    "domain": {
        "objects": [
            {"id": "obj.circle", "type": "circle"},
            {"id": "obj.center", "type": "point"},
            {"id": "obj.segment_candidate_1", "type": "segment"},
            {"id": "obj.segment_candidate_2", "type": "segment"},
        ],
        "relations": [],
        "problem_solving": {
            "understand": {
                "given_refs": [
                    "obj.circle",
                    "obj.center",
                    "obj.segment_candidate_1",
                    "obj.segment_candidate_2",
                ],
                "target_ref": "answer.target",
                "condition_refs": [
                    "rel.longest_segment",
                    "rel.diameter_through_center",
                ],
            },
            "plan": {
                "method": "도형관계판단",
                "description": "그림에서 가장 긴 선분과 중심을 지나는 선분을 비교해 문장이 맞는지 판단한다.",
            },
            "execute": {"expected_operations": ["선분 비교", "중심 통과 여부 확인", "참거짓 판단"]},
            "review": {"check_methods": ["그림의 선분 이름과 설명이 일치하는지 확인", "지름의 정의에 맞는지 확인"]},
        },
    },
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {"type": "truth_value", "description": "제시된 설명의 참/거짓"},
        "value": "×",
        "unit": "",
    },
}

SOLVABLE = {
    "schema": "modu.solvable.v1.1",
    "problem_id": "S3_초등_3_008721",
    "problem_type": "도형_참거짓판단",
    "inputs": {
        "total_ticks": 1,
        "target_label": "제시된 설명의 참/거짓",
        "target_ticks": 1,
        "target_count": 1,
        "unit": "",
    },
    "given": [
        {"ref": "obj.circle", "value": {"type": "circle"}},
        {"ref": "obj.center", "value": {"type": "point"}},
    ],
    "target": {"ref": "answer.target", "type": "truth_value"},
    "method": "도형관계판단",
    "plan": ["그림에서 선분의 길이와 중심 통과 여부를 보고 문장의 참/거짓을 판단한다."],
    "steps": [
        {"id": "step.1", "expr": "그림의 선분 관계를 비교한다.", "value": 0},
        {"id": "step.2", "expr": "중심을 지나는 선분이 지름인지 확인한다.", "value": 0},
        {"id": "step.3", "expr": "제시된 문장의 참/거짓을 판단한다.", "value": 0},
    ],
    "checks": [
        {
            "id": "check.1",
            "expr": "문장 판단 결과가 하단의 인쇄된 정답 표기와 일치하는지 확인",
            "expected": "×",
            "actual": "×",
            "pass": True,
        }
    ],
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {"type": "truth_value", "description": "제시된 설명의 참/거짓"},
        "value": "×",
        "unit": "",
    },
}
