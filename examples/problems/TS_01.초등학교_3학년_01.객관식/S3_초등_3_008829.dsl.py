from __future__ import annotations
from modu_math.dsl import Canvas, ProblemTemplate, Region, TextSlot, RectSlot, CircleSlot, LineSlot


def build_problem_template() -> ProblemTemplate:
    return ProblemTemplate(
        id="S3_초등_3_008829",
        title="알맞은 단위를 골라 선택하세요",
        canvas=Canvas(width=768, height=384, coordinate_mode="logical"),
        regions=(
            Region(
                id="region.top",
                role="stem",
                flow="absolute",
                slot_ids=("slot.qmark", "slot.qnum", "slot.instruction"),
            ),
            Region(
                id="region.diagram",
                role="diagram",
                flow="absolute",
                slot_ids=(
                    "slot.drum.body",
                    "slot.drum.rim.top",
                    "slot.drum.rim.mid1",
                    "slot.drum.rim.mid2",
                    "slot.drum.cap",
                    "slot.drum.highlight",
                ),
            ),
            Region(
                id="region.middle",
                role="stem",
                flow="absolute",
                slot_ids=(
                    "slot.main_sentence_1",
                    "slot.main_sentence_2",
                    "slot.unit.mL",
                    "slot.unit.L",
                ),
            ),
            Region(id="region.bottom", role="support", flow="absolute", slot_ids=()),
        ),
        slots=(
            TextSlot(
                id="slot.qmark",
                prompt="",
                text="□",
                style_role="question",
                x=12.0,
                y=34.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.qnum",
                prompt="",
                text="62.",
                style_role="question",
                x=42.0,
                y=34.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.instruction",
                prompt="",
                text="알맞은 단위를 골라 선택하세요.",
                style_role="question",
                x=92.0,
                y=34.0,
                font_size=28,
            ),
            RectSlot(id="slot.drum.body", prompt="", x=442.0, y=62.0, width=84.0, height=124.0),
            CircleSlot(
                id="slot.drum.rim.top", prompt="", cx=484.0, cy=68.0, r=42.0, fill="#D0D0D0"
            ),
            LineSlot(id="slot.drum.rim.mid1", prompt="", x1=442.0, y1=112.0, x2=526.0, y2=112.0),
            LineSlot(id="slot.drum.rim.mid2", prompt="", x1=442.0, y1=147.0, x2=526.0, y2=147.0),
            CircleSlot(id="slot.drum.cap", prompt="", cx=509.0, cy=64.0, r=6.0, fill="#BFBFBF"),
            LineSlot(id="slot.drum.highlight", prompt="", x1=470.0, y1=78.0, x2=470.0, y2=175.0),
            TextSlot(
                id="slot.main_sentence_1",
                prompt="",
                text="드럼통의 들이는 약 100(",
                style_role="question",
                x=240.0,
                y=256.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.unit.mL",
                prompt="",
                text="mL",
                style_role="question",
                x=450.0,
                y=256.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.main_sentence_2",
                prompt="",
                text=",",
                style_role="question",
                x=482.0,
                y=256.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.unit.L",
                prompt="",
                text="L",
                style_role="question",
                x=506.0,
                y=256.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.main_sentence_3",
                prompt="",
                text=")입니다.",
                style_role="question",
                x=540.0,
                y=256.0,
                font_size=28,
            ),
        ),
        diagrams=(),
        groups=(),
        constraints=(),
        tags=("단위", "용량", "선택형"),
    )


PROBLEM_TEMPLATE = build_problem_template()

SEMANTIC_OVERRIDE = {
    "problem_id": "S3_초등_3_008829",
    "problem_type": "unit_selection",
    "metadata": {
        "language": "ko",
        "question": "드럼통의 들이에 알맞은 단위를 고르는 문제",
        "instruction": "알맞은 단위를 골라 선택하세요.",
    },
    "domain": {
        "objects": [
            {"id": "obj.barrel", "type": "container", "name": "드럼통", "quantity": "capacity"},
            {"id": "obj.quantity", "type": "number", "value": 100},
            {"id": "obj.units", "type": "unit_choices", "choices": ["mL", "L"]},
        ],
        "relations": [],
        "problem_solving": {
            "understand": {
                "given_refs": ["obj.barrel", "obj.quantity", "obj.units"],
                "target_ref": "answer.target",
                "condition_refs": ["rel.choose_bigger_unit"],
            },
            "plan": {
                "method": "unit_selection",
                "description": "용량이 큰 물건에 어울리는 단위를 고른다.",
            },
            "execute": {"expected_operations": ["compare_units", "select_appropriate_unit"]},
            "review": {"check_methods": ["context_fit_check"]},
        },
    },
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {"type": "selected_unit", "description": "드럼통의 들이에 알맞은 단위"},
        "value": "L",
        "unit": "L",
    },
}

SOLVABLE = {
    "schema": "modu.solvable.v1.1",
    "problem_id": "S3_초등_3_008829",
    "problem_type": "unit_selection",
    "inputs": {
        "total_ticks": 0,
        "target_label": "드럼통의 들이에 알맞은 단위",
        "target_ticks": 0,
        "target_count": 1,
        "unit": "L",
    },
    "given": [
        {"ref": "obj.barrel", "value": {"name": "드럼통", "quantity": "capacity"}},
        {"ref": "obj.quantity", "value": 100},
        {"ref": "obj.units", "value": ["mL", "L"]},
    ],
    "target": {"ref": "answer.target", "type": "selected_unit"},
    "method": "unit_selection",
    "plan": ["드럼통의 들이에 어울리는 단위를 고른다.", "보기 중 더 큰 용량 단위를 선택한다."],
    "steps": [{"id": "step.1", "expr": "100과 보기 단위(mL, L)를 비교한다.", "value": "L"}],
    "checks": [
        {
            "id": "check.1",
            "expr": "드럼통은 작은 용량 단위 mL보다 큰 단위가 어울리는가?",
            "expected": "L",
            "actual": "L",
            "pass": True,
        }
    ],
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {"type": "selected_unit", "description": "드럼통의 들이에 알맞은 단위"},
        "value": "L",
        "unit": "L",
    },
}
