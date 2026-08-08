from __future__ import annotations
from modu_math.dsl import (
    Canvas,
    ProblemTemplate,
    Region,
    TextSlot,
    LineSlot,
    CircleSlot,
    table_slots,
)


def build_problem_template() -> ProblemTemplate:
    return ProblemTemplate(
        id="S3_초등_3_008645",
        title="원의 지름",
        canvas=Canvas(width=960, height=540, coordinate_mode="logical"),
        regions=(
            Region(
                id="region.stem",
                role="stem",
                flow="absolute",
                slot_ids=("slot.q2", "slot.q3"),
            ),
        ),
        slots=(
            TextSlot(
                id="slot.q2",
                prompt="",
                text="지름을 나타내는 선분을 찾아 길이를 잰 값을 보고, 맞는 말을 선택해 보세요.",
                style_role="question",
                x=76.0,
                y=30.0,
                font_size=28,
            ),
            CircleSlot(
                id="slot.circle.outer",
                prompt="",
                cx = 480, cy = 160, r = 80, fill="none",
            ),
            CircleSlot(
                id="slot.circle.center",
                prompt="",
                cx = 480, cy = 160, r = 5, fill="#d81b60",
            ),
            TextSlot(
                id="slot.lb.o",
                prompt="",
                text = 'ㅇ', style_role="label",
                x = 490, y = 155, font_size = 20),
            LineSlot(
                id="slot.line.gm", prompt="", x1 = 445, y1 = 90, x2 = 520, y2 = 230),
            LineSlot(
                id="slot.line.nb", prompt="", x1 = 400, y1 = 150, x2 = 560, y2 = 170),
            LineSlot(
                id="slot.line.ls", prompt="", x1 = 485, y1 = 80, x2 = 475, y2 = 240),
            LineSlot(
                id="slot.line.d", prompt="", x1 = 430, y1 = 220, x2 = 480, y2 = 160),
            TextSlot(
                id="slot.lb.ㄱ",
                prompt="",
                text = 'ㄱ', style_role="label",
                x = 430, y = 80, font_size = 20),
            TextSlot(
                id="slot.lb.ㄴ",
                prompt="",
                text = 'ㄴ', style_role="label",
                x = 375, y = 155, font_size = 20),
            TextSlot(
                id="slot.lb.ㄷ",
                prompt="",
                text = 'ㄷ', style_role="label",
                x = 410, y = 235, font_size = 20),
            TextSlot(
                id="slot.lb.ㄹ",
                prompt="",
                text = 'ㄹ', style_role="label",
                x = 455, y = 260, font_size = 20),
            TextSlot(
                id="slot.lb.ㅁ",
                prompt="",
                text = 'ㅁ', style_role="label",
                x = 520, y = 250, font_size = 20),
            TextSlot(
                id="slot.lb.ㅂ",
                prompt="",
                text = 'ㅂ', style_role="label",
                x = 565, y = 180, font_size = 20),
            TextSlot(
                id="slot.lb.ㅅ",
                prompt="",
                text = 'ㅅ', style_role="label",
                x = 485, y = 75, font_size = 20),
            *table_slots(
                "slot.table",
                x=175,
                y=290,
                col_widths=(220, 135, 135, 135),
                row_heights=(40, 40),
                cells=(
                    ("지름", "선분 ㄱㅁ", "선분 ㄴㅂ", "선분 ㄹㅅ"),
                    ("길이(cm)", "3", "3", "3"),
                ),
                font_size=26,
                align="center",
                text_dy=28,
                fill="none",
            ),
            TextSlot(
                id="slot.arrow",
                prompt="",
                text="➜",
                style_role="instruction",
                x=134.0,
                y=409.0,
                font_size=34,
            ),
            TextSlot(
                id="slot.q3",
                prompt="",
                text = '한 원에서 원의 지름은 모두 ( 같습니다 , 다릅니다 ).', style_role="question",
                x = 180, y = 410, font_size = 30),
        ),
        diagrams=(),
        groups=(),
        constraints=(),
        tags=(),
    )


PROBLEM_TEMPLATE = build_problem_template()

SEMANTIC_OVERRIDE = {
    "problem_id": "S3_초등_3_008645",
    "problem_type": "circle_diameter_comparison",
    "metadata": {
        "language": "ko",
        "question": "지름을 나타내는 선분을 찾아 길이를 잰 값을 보고, 맞는 말을 선택해 보세요.",
        "instruction": "한 원에서 원의 지름은 모두 (같습니다, 다릅니다).",
    },
    "domain": {
        "objects": [
            {"id": "obj.circle", "type": "circle"},
            {"id": "obj.segment.gm", "type": "segment", "label": "ㄱㅁ"},
            {"id": "obj.segment.nb", "type": "segment", "label": "ㄴㅂ"},
            {"id": "obj.segment.ls", "type": "segment", "label": "ㄹㅅ"},
        ],
        "relations": [],
        "problem_solving": {
            "understand": {
                "given_refs": [
                    "obj.circle",
                    "obj.segment.gm",
                    "obj.segment.nb",
                    "obj.segment.ls",
                ],
                "target_ref": "answer.target",
                "condition_refs": [
                    "rel.diameter_candidates",
                    "rel.diameter_candidates_2",
                    "rel.diameter_candidates_3",
                ],
            },
            "plan": {
                "method": "property_check",
                "description": "원의 중심을 지나며 원 위의 두 점을 잇는 선분이 지름인지 확인한다.",
            },
            "execute": {
                "expected_operations": [
                    "identify_diameter_candidates",
                    "compare_diameter_property",
                ]
            },
            "review": {"check_methods": ["property_consistency_check"]},
        },
    },
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {
            "type": "multiple_choice_completion",
            "description": "한 원에서 원의 지름은 모두 (같습니다, 다릅니다).",
        },
        "value": "같습니다",
        "unit": "",
    },
}

SOLVABLE = {
    "schema": "modu.solvable.v1.1",
    "problem_id": "S3_초등_3_008645",
    "problem_type": "circle_diameter_comparison",
    "inputs": {
        "total_ticks": 1,
        "target_label": "같습니다, 다릅니다",
        "target_ticks": 1,
        "target_count": 2,
        "unit": "",
    },
    "given": [
        {"ref": "obj.segment.gm", "value": {"label": "ㄱㅁ"}},
        {"ref": "obj.segment.nb", "value": {"label": "ㄴㅂ"}},
        {"ref": "obj.segment.ls", "value": {"label": "ㄹㅅ"}},
    ],
    "target": {"ref": "answer.target", "type": "multiple_choice_completion"},
    "method": "property_check",
    "plan": [
        "원의 중심을 지나고 원 위의 두 점을 잇는 선분이 지름인지 확인한다.",
        "지름의 성질을 이용해 한 원의 지름은 모두 같은지 판단한다.",
    ],
    "steps": [
        {
            "id": "step.1",
            "expr": "선분 ㄱㅁ, 선분 ㄴㅂ, 선분 ㄹㅅ은 지름 후보이다.",
            "value": "candidates",
        },
        {"id": "step.2", "expr": "한 원에서 지름은 모두 같다.", "value": "같습니다"},
    ],
    "checks": [
        {
            "id": "check.1",
            "expr": "지름의 성질 확인",
            "expected": "같습니다",
            "actual": "같습니다",
            "pass": True,
        }
    ],
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {
            "type": "multiple_choice_completion",
            "description": "한 원에서 원의 지름은 모두 (같습니다, 다릅니다).",
        },
        "value": "같습니다",
        "unit": "",
    },
}
