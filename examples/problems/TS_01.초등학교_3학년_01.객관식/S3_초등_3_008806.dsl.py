from __future__ import annotations
from modu_math.dsl import Canvas, ProblemTemplate, Region, TextSlot, RectSlot


def build_problem_template() -> ProblemTemplate:
    return ProblemTemplate(
        id="S3_초등_3_008806",
        title="무게가 100 g보다 더 가벼운 것을 선택하세요",
        canvas=Canvas(width=760, height=460, coordinate_mode="logical"),
        regions=(
            Region(
                id="region.stem",
                role="stem",
                flow="absolute",
                slot_ids=("slot.q.symbol", "slot.q.text"),
            ),
            Region(
                id="region.example",
                role="diagram",
                flow="absolute",
                slot_ids=(
                    "slot.box",
                    "slot.box.label",
                    "slot.box.object",
                    "slot.box.weight",
                    "slot.choice.strawberry",
                    "slot.choice.pineapple",
                ),
            ),
            Region(id="region.answer", role="answer", flow="absolute", slot_ids=()),
            Region(id="region.explanation", role="explanation", flow="absolute", slot_ids=()),
        ),
        slots=(
            TextSlot(
                id="slot.q.symbol",
                prompt="",
                text="□",
                style_role="question",
                x=8.0,
                y=30.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.q.text",
                prompt="",
                text="35. 무게가 100 g보다 더 가벼운 것을 선택하세요.",
                style_role="question",
                x=40.0,
                y=30.0,
                font_size=28,
            ),
            RectSlot(id="slot.box", prompt="", x=178.0, y=50.0, width=226.0, height=206.0),
            TextSlot(
                id="slot.box.label",
                prompt="",
                text="<보기>",
                style_role="label",
                x=200.0,
                y=95.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.box.object",
                prompt="",
                text="연두색 튜브 그림",
                style_role="label",
                x=245.0,
                y=150.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.box.weight",
                prompt="",
                text="100 g",
                style_role="label",
                x=250.0,
                y=225.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.choice.strawberry",
                prompt="",
                text="딸기 그림",
                style_role="label",
                x=478.0,
                y=148.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.choice.pineapple",
                prompt="",
                text="파인애플 그림",
                style_role="label",
                x=638.0,
                y=146.0,
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
    "problem_id": "S3_초등_3_008806",
    "problem_type": "weight_comparison_selection",
    "metadata": {
        "language": "ko",
        "question": "무게가 100 g보다 더 가벼운 것을 선택하세요.",
        "instruction": "무게가 100 g보다 더 가벼운 것을 선택하세요.",
    },
    "domain": {
        "objects": [
            {"id": "obj.reference_weight", "type": "weight", "value": 100, "unit": "g"},
            {"id": "obj.choice.strawberry", "type": "object", "name": "딸기"},
            {"id": "obj.choice.pineapple", "type": "object", "name": "파인애플"},
        ],
        "relations": [],
        "problem_solving": {
            "understand": {
                "given_refs": [
                    "obj.reference_weight",
                    "obj.choice.strawberry",
                    "obj.choice.pineapple",
                ],
                "target_ref": "answer.target",
                "condition_refs": ["rel.compare.weight", "rel.compare.weight.2"],
            },
            "plan": {
                "method": "comparison_selection",
                "description": "기준 무게 100 g과 그림의 대상을 비교하여 더 가벼운 대상을 찾는다.",
            },
            "execute": {"expected_operations": ["compare_with_reference", "select_lighter_object"]},
            "review": {"check_methods": ["selection_matches_comparison_condition"]},
        },
    },
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {"type": "selected_object", "description": "100 g보다 더 가벼운 것"},
        "value": 0,
        "unit": "",
    },
}

SOLVABLE = {
    "schema": "modu.solvable.v1.1",
    "problem_id": "S3_초등_3_008806",
    "problem_type": "weight_comparison_selection",
    "inputs": {
        "total_ticks": 0,
        "target_label": "100 g보다 더 가벼운 것",
        "target_ticks": 0,
        "target_count": 1,
        "unit": "g",
    },
    "given": [
        {"ref": "obj.reference_weight", "value": {"value": 100, "unit": "g"}},
        {"ref": "obj.choice.strawberry", "value": {"name": "딸기"}},
        {"ref": "obj.choice.pineapple", "value": {"name": "파인애플"}},
    ],
    "target": {"ref": "answer.target", "type": "selected_object"},
    "method": "comparison_selection",
    "plan": ["기준 무게 100 g과 각 선택지를 비교한다.", "100 g보다 더 가벼운 대상을 선택한다."],
    "steps": [
        {
            "id": "step.1",
            "expr": "100 g을 기준으로 딸기와 파인애플을 비교한다.",
            "value": "comparison_setup",
        },
        {"id": "step.2", "expr": "100 g보다 더 가벼운 대상을 고른다.", "value": "selection"},
    ],
    "checks": [
        {
            "id": "check.1",
            "expr": "선택이 100 g보다 더 가벼운 대상인지 확인한다.",
            "expected": True,
            "actual": True,
            "pass": True,
        }
    ],
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {"type": "selected_object", "description": "100 g보다 더 가벼운 것"},
        "value": 0,
        "unit": "",
    },
}
