from __future__ import annotations
from modu_math.dsl import Canvas, ProblemTemplate, RectSlot, Region, TextSlot


def build_problem_template() -> ProblemTemplate:
    return ProblemTemplate(
        id="S3_초등_3_008876",
        title="무게가 두 번째로 가벼운 것의 이름",
        canvas=Canvas(width=944, height=426, coordinate_mode="logical"),
        regions=(
            Region(
                id="region.stem",
                role="stem",
                flow="absolute",
                slot_ids=("slot.qmark", "slot.qnum", "slot.question"),
            ),
            Region(
                id="region.objects",
                role="body",
                flow="absolute",
                slot_ids=(
                    "slot.obj.baseball",
                    "slot.lb.baseball",
                    "slot.obj.eraser",
                    "slot.lb.eraser",
                    "slot.obj.chair",
                    "slot.lb.chair",
                ),
            ),
            Region(id="region.answer", role="answer", flow="absolute", slot_ids=()),
        ),
        slots=(
            TextSlot(
                id="slot.qmark",
                prompt="",
                text="□",
                style_role="question",
                x=6.0,
                y=30.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.qnum",
                prompt="",
                text="31.",
                style_role="question",
                x=31.0,
                y=30.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.question",
                prompt="",
                text="무게가 두 번째로 가벼운 것의 이름을 선택해 보세요.",
                style_role="question",
                x=80.0,
                y=30.0,
                font_size=28,
            ),
            RectSlot(
                id="slot.obj.baseball",
                prompt="",
                x=270.0,
                y=142.0,
                width=34.0,
                height=34.0,
                fill="none",
                stroke="none",
            ),
            TextSlot(
                id="slot.lb.baseball",
                prompt="",
                text="야구공",
                style_role="label",
                x=252.0,
                y=272.0,
                font_size=28,
            ),
            RectSlot(
                id="slot.obj.eraser",
                prompt="",
                x=470.0,
                y=146.0,
                width=38.0,
                height=26.0,
                fill="none",
                stroke="none",
            ),
            TextSlot(
                id="slot.lb.eraser",
                prompt="",
                text="지우개",
                style_role="label",
                x=451.0,
                y=272.0,
                font_size=28,
            ),
            RectSlot(
                id="slot.obj.chair",
                prompt="",
                x=646.0,
                y=62.0,
                width=84.0,
                height=98.0,
                fill="none",
                stroke="none",
            ),
            TextSlot(
                id="slot.lb.chair",
                prompt="",
                text="의자",
                style_role="label",
                x=668.0,
                y=272.0,
                font_size=28,
            ),
        ),
        diagrams=(),
        groups=(),
        constraints=(),
        tags=("비교", "무게", "순서"),
    )


PROBLEM_TEMPLATE = build_problem_template()

SEMANTIC_OVERRIDE = {
    "problem_id": "S3_초등_3_008876",
    "problem_type": "comparison_order",
    "metadata": {
        "language": "ko",
        "question": "무게가 두 번째로 가벼운 것의 이름을 선택해 보세요.",
        "instruction": "세 물건의 무게 순서를 비교해 두 번째로 가벼운 대상을 고른다.",
    },
    "domain": {
        "objects": [
            {"id": "obj.baseball", "type": "object", "name": "야구공"},
            {"id": "obj.eraser", "type": "object", "name": "지우개"},
            {"id": "obj.chair", "type": "object", "name": "의자"},
        ],
        "relations": [],
        "problem_solving": {
            "understand": {
                "given_refs": ["obj.baseball", "obj.eraser", "obj.chair"],
                "target_ref": "answer.target",
                "condition_refs": ["rel.weight_order"],
            },
            "plan": {
                "method": "order_by_weight",
                "description": "무게의 상대적 순서를 읽어 두 번째로 가벼운 대상을 찾는다.",
            },
            "execute": {"expected_operations": ["compare_weights", "identify_second_lightest"]},
            "review": {"check_methods": ["order_consistency_check"]},
        },
    },
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {"type": "selected_name", "description": "두 번째로 가벼운 것의 이름"},
        "value": "야구공",
        "unit": "",
    },
}

SOLVABLE = {
    "schema": "modu.solvable.v1.1",
    "problem_id": "S3_초등_3_008876",
    "problem_type": "comparison_order",
    "inputs": {
        "total_ticks": 3,
        "target_label": "두 번째로 가벼운 것의 이름",
        "target_ticks": 2,
        "target_count": 1,
        "unit": "",
    },
    "given": [
        {"ref": "obj.baseball", "value": {"name": "야구공"}},
        {"ref": "obj.eraser", "value": {"name": "지우개"}},
        {"ref": "obj.chair", "value": {"name": "의자"}},
        {"ref": "rel.weight_order", "value": {"chain": ["지우개", "야구공", "의자"]}},
    ],
    "target": {"ref": "answer.target", "type": "selected_name"},
    "method": "order_by_weight",
    "plan": [
        "세 물건의 무게 순서를 비교한다.",
        "가장 가벼운 것부터 차례대로 읽어 두 번째 항목을 찾는다.",
    ],
    "steps": [
        {"id": "step.1", "expr": "지우개<야구공<의자", "value": ["지우개", "야구공", "의자"]},
        {"id": "step.2", "expr": "두 번째로 가벼운 것", "value": "야구공"},
    ],
    "checks": [
        {
            "id": "check.1",
            "expr": "순서가 가벼운 것부터 무거운 것까지인지 확인",
            "expected": ["지우개", "야구공", "의자"],
            "actual": ["지우개", "야구공", "의자"],
            "pass": True,
        }
    ],
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {"type": "selected_name", "description": "두 번째로 가벼운 것의 이름"},
        "value": "야구공",
        "unit": "",
    },
}
