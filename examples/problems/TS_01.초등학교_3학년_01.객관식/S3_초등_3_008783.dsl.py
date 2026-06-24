from __future__ import annotations
from modu_math.dsl import Canvas, ProblemTemplate, Region, RectSlot, TextSlot


def build_problem_template() -> ProblemTemplate:
    return ProblemTemplate(
        id="S3_초등_3_008783",
        title="멜론의 무게를 가장 가깝게 어림한 것",
        canvas=Canvas(width=944, height=555, coordinate_mode="logical"),
        regions=(
            Region(id="region.stem", role="stem", flow="absolute", slot_ids=("slot.q1", "slot.q2")),
            Region(
                id="region.diagram",
                role="diagram",
                flow="absolute",
                slot_ids=(
                    "slot.scale.melon",
                    "slot.scale.label",
                    "slot.choice.box",
                    "slot.choice.g1",
                    "slot.choice.g2",
                    "slot.choice.g3",
                ),
            ),
            Region(id="region.answer", role="answer", flow="absolute", slot_ids=()),
        ),
        slots=(
            TextSlot(
                id="slot.q1",
                prompt="",
                text="5. 멜론의 무게를 재었더니 다음과 같습니다. 멜론의 무게를 가장 가깝게 어림한 것을 찾아 기호를 선택하세요.",
                style_role="question",
                x=16.0,
                y=28.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.q2",
                prompt="",
                text="",
                style_role="question",
                x=16.0,
                y=63.0,
                font_size=28,
            ),
            RectSlot(id="slot.choice.box", prompt="", x=465.0, y=101.0, width=322.0, height=212.0),
            TextSlot(
                id="slot.choice.g1",
                prompt="",
                text="ㄱ 약 3 kg 300 g",
                style_role="choice",
                x=498.0,
                y=150.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.choice.g2",
                prompt="",
                text="ㄴ 약 2 kg 700 g",
                style_role="choice",
                x=498.0,
                y=203.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.choice.g3",
                prompt="",
                text="ㄷ 약 3100 g",
                style_role="choice",
                x=498.0,
                y=257.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.scale.melon",
                prompt="",
                text="멜론과 저울 그림",
                style_role="diagram",
                x=210.0,
                y=125.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.scale.label",
                prompt="",
                text="3kg",
                style_role="diagram",
                x=205.0,
                y=341.0,
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
    "problem_id": "S3_초등_3_008783",
    "problem_type": "어림하기",
    "metadata": {
        "language": "ko",
        "question": "멜론의 무게를 가장 가깝게 어림한 것을 찾는 문제",
        "instruction": "가장 가깝게 어림한 것을 찾아 기호를 선택하세요.",
    },
    "domain": {
        "objects": [
            {"id": "obj.melon_weight", "type": "weight", "value": 3, "unit": "kg"},
            {"id": "obj.choice.g1", "type": "choice", "label": "ㄱ", "value": 3300, "unit": "g"},
            {"id": "obj.choice.g2", "type": "choice", "label": "ㄴ", "value": 2700, "unit": "g"},
            {"id": "obj.choice.g3", "type": "choice", "label": "ㄷ", "value": 3100, "unit": "g"},
        ],
        "relations": [],
        "problem_solving": {
            "understand": {
                "given_refs": [
                    "obj.melon_weight",
                    "obj.choice.g1",
                    "obj.choice.g2",
                    "obj.choice.g3",
                ],
                "target_ref": "answer.target",
                "condition_refs": ["rel.compare_to_weight"],
            },
            "plan": {
                "method": "difference_comparison",
                "description": "실제 무게와 각 보기의 차이를 비교하여 가장 가까운 보기를 찾는다.",
            },
            "execute": {
                "expected_operations": ["compare_weight_differences", "select_minimum_difference"]
            },
            "review": {"check_methods": ["difference_consistency_check"]},
        },
    },
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {"type": "choice_label", "description": "가장 가깝게 어림한 기호"},
        "value": "ㄷ",
        "unit": "",
    },
}

SOLVABLE = {
    "schema": "modu.solvable.v1.1",
    "problem_id": "S3_초등_3_008783",
    "problem_type": "어림하기",
    "inputs": {
        "total_ticks": 0,
        "target_label": "ㄱ ㄴ ㄷ",
        "target_ticks": 3,
        "target_count": 3,
        "unit": "g",
    },
    "given": [
        {"ref": "obj.melon_weight", "value": {"value": 3, "unit": "kg"}},
        {"ref": "obj.choice.g1", "value": {"value": 3300, "unit": "g"}},
        {"ref": "obj.choice.g2", "value": {"value": 2700, "unit": "g"}},
        {"ref": "obj.choice.g3", "value": {"value": 3100, "unit": "g"}},
    ],
    "target": {"ref": "answer.target", "type": "choice_label"},
    "method": "difference_comparison",
    "plan": ["실제 무게와 각 보기를 비교하여 차이가 가장 작은 것을 찾는다."],
    "steps": [
        {"id": "step.1", "expr": "보기 ㄱ과 3 kg의 차이를 비교한다", "value": "300 g"},
        {"id": "step.2", "expr": "보기 ㄴ과 3 kg의 차이를 비교한다", "value": "300 g"},
        {"id": "step.3", "expr": "보기 ㄷ과 3 kg의 차이를 비교한다", "value": "100 g"},
    ],
    "checks": [
        {
            "id": "check.1",
            "expr": "세 보기 중 차이가 가장 작은 값을 확인한다",
            "expected": "100 g",
            "actual": "100 g",
            "pass": True,
        }
    ],
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {"type": "choice_label", "description": "가장 가깝게 어림한 기호"},
        "value": "ㄷ",
        "unit": "",
    },
}
