from __future__ import annotations
from modu_math.dsl import Canvas, ProblemTemplate, Region, RectSlot, TextSlot


def build_problem_template() -> ProblemTemplate:
    return ProblemTemplate(
        id="S3_초등_3_008769",
        title="무게를 알맞게 어림한 것을 찾아 선택하세요.",
        canvas=Canvas(width=730, height=360, coordinate_mode="logical"),
        regions=(
            Region(
                id="region.header",
                role="stem",
                flow="absolute",
                slot_ids=("slot.chk", "slot.qnum", "slot.qtext"),
            ),
            Region(
                id="region.choice_box",
                role="diagram",
                flow="absolute",
                slot_ids=("slot.box", "slot.car", "slot.choice"),
            ),
            Region(id="region.answer", role="answer", flow="absolute", slot_ids=()),
        ),
        slots=(
            TextSlot(
                id="slot.chk",
                prompt="",
                text="□",
                style_role="question",
                x=8.0,
                y=28.0,
                font_size=24,
            ),
            TextSlot(
                id="slot.qnum",
                prompt="",
                text="71.",
                style_role="question",
                x=34.0,
                y=30.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.qtext",
                prompt="",
                text="무게를 알맞게 어림한 것을 찾아 선택하세요.",
                style_role="question",
                x=78.0,
                y=30.0,
                font_size=28,
            ),
            RectSlot(id="slot.box", prompt="", x=290.0, y=80.0, width=370.0, height=182.0),
            TextSlot(
                id="slot.car",
                prompt="",
                text="TODO: 경찰차 그림",
                style_role="diagram",
                x=395.0,
                y=124.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.choice",
                prompt="",
                text="약 ( 1 g , 1 kg , 1 t )",
                style_role="diagram",
                x=365.0,
                y=224.0,
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
    "problem_id": "S3_초등_3_008769",
    "problem_type": "weight_estimation_choice",
    "metadata": {
        "language": "ko",
        "question": "무게를 알맞게 어림한 것을 찾아 선택하세요.",
        "instruction": "그림을 보고 알맞은 무게 단위를 고른다.",
    },
    "domain": {
        "objects": [
            {"id": "obj.vehicle", "type": "vehicle", "name": "경찰차"},
            {"id": "obj.choices", "type": "weight_choices", "values": ["1 g", "1 kg", "1 t"]},
        ],
        "relations": [],
        "problem_solving": {
            "understand": {
                "given_refs": ["obj.vehicle", "obj.choices"],
                "target_ref": "answer.target",
                "condition_refs": ["rel.compare_weight"],
            },
            "plan": {
                "method": "relative_weight_choice",
                "description": "그림의 물체가 사람보다 매우 무거운 물체인지 보고, 제시된 단위 중 알맞은 것을 고른다.",
            },
            "execute": {
                "expected_operations": [
                    "compare_with_gram",
                    "compare_with_kilogram",
                    "compare_with_ton",
                ]
            },
            "review": {"check_methods": ["choice_reasonableness_check"]},
        },
    },
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {"type": "weight_choice", "description": "그림에 알맞은 무게 어림값"},
        "value": 1,
        "unit": "",
    },
}

SOLVABLE = {
    "schema": "modu.solvable.v1.1",
    "problem_id": "S3_초등_3_008769",
    "problem_type": "weight_estimation_choice",
    "inputs": {
        "total_ticks": 3,
        "target_label": "그림에 알맞은 무게",
        "target_ticks": 1,
        "target_count": 1,
        "unit": "",
    },
    "given": [
        {"ref": "obj.vehicle", "value": "경찰차"},
        {"ref": "obj.choices", "value": ["1 g", "1 kg", "1 t"]},
    ],
    "target": {"ref": "answer.target", "type": "weight_choice"},
    "method": "relative_weight_choice",
    "plan": [
        "그림 속 물체의 무게를 보기 좋게 비교한다.",
        "제시된 단위 중 가장 알맞은 것을 고른다.",
    ],
    "steps": [
        {"id": "step.1", "expr": "선택지 = [1 g, 1 kg, 1 t]", "value": ["1 g", "1 kg", "1 t"]},
        {"id": "step.2", "expr": "경찰차는 1 kg보다 더 무거운 물체로 판단", "value": "1 kg 초과"},
        {"id": "step.3", "expr": "알맞은 단위 선택", "value": "1 t"},
    ],
    "checks": [
        {
            "id": "check.1",
            "expr": "선택한 단위가 1 kg보다 큰 무게를 나타내는지 확인",
            "expected": True,
            "actual": True,
            "pass": True,
        }
    ],
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {"type": "weight_choice", "description": "그림에 알맞은 무게 어림값"},
        "value": 1,
        "unit": "",
    },
}
