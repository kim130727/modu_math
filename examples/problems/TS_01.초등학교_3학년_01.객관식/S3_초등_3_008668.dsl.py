from __future__ import annotations
from modu_math.dsl import (
    Canvas,
    ProblemTemplate,
    Region,
    TextSlot,
    RectSlot,
    LineSlot,
    CircleSlot,
)


def build_problem_template() -> ProblemTemplate:
    return ProblemTemplate(
        id="S3_초등_3_008668",
        title="바르게 설명하였으면 ○, 그렇지 않으면 ×를 선택하세요.",
        canvas=Canvas(width=944.0, height=470.0, coordinate_mode="logical"),
        regions=(
            Region(
                id="region.header",
                role="stem",
                flow="absolute",
                slot_ids=("slot.instruction",),
            ),
            Region(
                id="region.diagram",
                role="figure",
                flow="absolute",
                slot_ids=("slot.circle.outer",
                    "slot.line.vertical",
                    "slot.line.diagonal",
                    "slot.line.top",
                    "slot.pt.center",
                    "slot.lb.center",
                    "slot.lb.d",
                    "slot.lb.r",
                    "slot.lb.m",
                    "slot.lb.b",'slot.lb.d.copy13', 'slot.lb.d.copy13.copy14'),
            ),
            Region(
                id="region.statement",
                role="stem",
                flow="absolute",
                slot_ids=("slot.statement",),
            ),
            Region(
                id="region.choice",
                role="answer",
                flow="absolute",
                slot_ids=(),
            ),
            Region(
                id="region.footer", role="explanation", flow="absolute", slot_ids=()
            ),
        ),
        slots=(TextSlot(
                id="slot.instruction",
                prompt="",
                text = '바르게 설명하였으면 ○, 그렇지 않으면 ×를 선택하세요.', style_role="question",
                x = 45, y = 35, font_size = 30),
            CircleSlot(
                id="slot.circle.outer",
                prompt="",
                cx = 335, cy = 196, r = 110, fill="none",
            ),
            LineSlot(
                id="slot.line.vertical",
                prompt="",
                x1 = 390, y1 = 100, x2 = 390, y2 = 290),
            LineSlot(
                id="slot.line.diagonal",
                prompt="",
                x1 = 228, y1 = 174, x2 = 443, y2 = 219),
            LineSlot(
                id="slot.line.top", prompt="", x1 = 258, y1 = 115, x2 = 418, y2 = 120),
            CircleSlot(
                id="slot.pt.center", prompt="", cx = 335, cy = 195, r = 5, fill="#ff2aa1"
            ),
            TextSlot(
                id="slot.lb.center",
                prompt="",
                text = 'ㅇ', style_role="label",
                x = 305, y = 220, font_size = 30),
            TextSlot(
                id="slot.lb.d",
                prompt="",
                text = 'ㄷ', style_role="label",
                x = 185, y = 180, font_size = 30, fill = '#111111'),
            TextSlot(
                id="slot.lb.r",
                prompt="",
                text = 'ㄹ', style_role="label",
                x = 450, y = 235, font_size = 30),
            TextSlot(
                id="slot.lb.m",
                prompt="",
                text = 'ㅁ', style_role="label",
                x = 375, y = 85, font_size = 30),
            TextSlot(
                id="slot.lb.b",
                prompt="",
                text = 'ㅂ', style_role="label",
                x = 380, y = 320, font_size = 30),
            TextSlot(
                id="slot.statement",
                prompt="",
                text = '\n    \n    길이가 가장 긴 선분은 선분 ㅁㅂ이고, 원의 지름은 선분\n    ㄷㄹ입니다.\n  ', style_role="question",
                x = 60, y = 340, font_size = 30),TextSlot(id = 'slot.lb.d.copy13', prompt = '', text = 'ㄱ', x = 220, y = 125, font_size = 30, fill = '#111111'), TextSlot(id = 'slot.lb.d.copy13.copy14', prompt = '', text = 'ㄴ', x = 425, y = 130, font_size = 30, fill = '#111111')),
        diagrams=(),
        groups=(),
        constraints=(),
        tags=(),
    )


PROBLEM_TEMPLATE = build_problem_template()

SEMANTIC_OVERRIDE = {
    "problem_id": "S3_초등_3_008668",
    "problem_type": "true_false_geometry",
    "metadata": {
        "language": "ko",
        "question": "원에서 선분의 길이와 지름의 성질을 바르게 설명했는지 판단하는 문제",
        "instruction": "바르게 설명하였으면 ○, 그렇지 않으면 ×를 선택하세요.",
    },
    "domain": {
        "objects": [
            {"id": "obj.circle", "type": "circle"},
            {
                "id": "obj.segment.db",
                "type": "segment",
                "label": "ㄷㄹ",
                "role": "diameter_candidate",
            },
            {
                "id": "obj.segment.mb",
                "type": "segment",
                "label": "ㅁㅂ",
                "role": "longest_segment_claim",
            },
        ],
        "relations": [],
        "problem_solving": {
            "understand": {
                "given_refs": ["obj.circle", "obj.segment.db", "obj.segment.mb"],
                "target_ref": "answer.target",
                "condition_refs": ["rel.center_passage", "rel.truth_check"],
            },
            "plan": {
                "method": "truth_value_judgment",
                "description": "그림과 문장의 진술이 맞는지 확인한 뒤 ○/×를 판단한다.",
            },
            "execute": {
                "expected_operations": [
                    "compare_segments",
                    "identify_diameter",
                    "judge_statement_truth",
                ]
            },
            "review": {
                "check_methods": ["center_passage_check", "geometry_property_check"]
            },
        },
    },
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {"type": "truth_value", "description": "제시된 설명이 바른지 판단"},
        "value": "X",
        "unit": "",
    },
}

SOLVABLE = {
    "schema": "modu.solvable.v1.1",
    "problem_id": "S3_초등_3_008668",
    "problem_type": "true_false_geometry",
    "inputs": {
        "total_ticks": 1,
        "target_label": "×",
        "target_ticks": 1,
        "target_count": 1,
        "unit": "",
    },
    "given": [
        {"ref": "obj.circle", "value": {"type": "circle"}},
        {"ref": "obj.segment.db", "value": {"label": "ㄷㄹ"}},
        {"ref": "obj.segment.mb", "value": {"label": "ㅁㅂ"}},
    ],
    "target": {"ref": "answer.target", "type": "truth_value"},
    "method": "truth_value_judgment",
    "plan": [
        "그림에서 원의 중심을 지나가는 선분이 지름인지 확인한다.",
        "문장에 적힌 두 주장(가장 긴 선분, 지름)을 그림과 비교한다.",
        "진술이 맞으면 ○, 틀리면 ×로 판단한다.",
    ],
    "steps": [
        {"id": "step.1", "expr": "원의 중심을 지나는 선분 확인", "value": "ㄷㄹ"},
        {"id": "step.2", "expr": "가장 긴 선분에 대한 문장 판단", "value": "거짓"},
        {"id": "step.3", "expr": "전체 설명의 진위", "value": "거짓"},
    ],
    "checks": [
        {
            "id": "check.1",
            "expr": "지름은 중심을 지난다",
            "expected": True,
            "actual": True,
            "pass": True,
        },
        {
            "id": "check.2",
            "expr": "문장 전체가 바른가",
            "expected": False,
            "actual": False,
            "pass": True,
        },
    ],
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {"type": "truth_value", "description": "제시된 설명이 바른지 판단"},
        "value": "X",
        "unit": "",
    },
}
