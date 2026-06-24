from __future__ import annotations
from modu_math.dsl import Canvas, ProblemTemplate, Region, RectSlot, TextSlot


def build_problem_template() -> ProblemTemplate:
    return ProblemTemplate(
        id="S3_초등_3_008744",
        title="들이 비교",
        canvas=Canvas(width=940, height=460, coordinate_mode="logical"),
        regions=(
            Region(id="region.stem", role="stem", flow="absolute", slot_ids=("slot.q1", "slot.q2")),
            Region(
                id="region.diagram",
                role="diagram",
                flow="absolute",
                slot_ids=(
                    "slot.diagram.bottle1",
                    "slot.diagram.bottle2",
                    "slot.diagram.water",
                    "slot.diagram.label1",
                    "slot.diagram.label2",
                    "slot.diagram.arrow",
                ),
            ),
            Region(id="region.choice", role="choice", flow="absolute", slot_ids=("slot.q5",)),
            Region(
                id="region.explain",
                role="explanation",
                flow="absolute",
                slot_ids=("slot.q6", "slot.q7"),
            ),
            Region(id="region.footer", role="footer", flow="absolute", slot_ids=("slot.q8",)),
        ),
        slots=(
            TextSlot(
                id="slot.q1",
                prompt="",
                text="□ 40. 그림과 같이 ㉠ 물병에 물을 가득 채운 후 ㉡ 물병에 옮겨 담아 ㉠ 물병과 ㉡ 물병의 들이를 비교하려고 합니다. 알맞은 말을 선택하세요.",
                style_role="question",
                x=6.0,
                y=26.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.q2",
                prompt="",
                text="들이가 더 많은 것은 ( ㉠ 물병, ㉡ 물병 )입니다.",
                style_role="question",
                x=4.0,
                y=306.0,
                font_size=30,
            ),
            RectSlot(
                id="slot.diagram.bottle1", prompt="", x=392.0, y=64.0, width=126.0, height=56.0
            ),
            RectSlot(
                id="slot.diagram.bottle2", prompt="", x=484.0, y=112.0, width=96.0, height=156.0
            ),
            RectSlot(id="slot.diagram.water", prompt="", x=494.0, y=164.0, width=76.0, height=86.0),
            TextSlot(
                id="slot.diagram.label1",
                prompt="",
                text="가",
                style_role="label",
                x=436.0,
                y=96.0,
                font_size=24,
            ),
            TextSlot(
                id="slot.diagram.label2",
                prompt="",
                text="나",
                style_role="label",
                x=522.0,
                y=222.0,
                font_size=24,
            ),
            TextSlot(
                id="slot.diagram.arrow",
                prompt="",
                text="",
                style_role="label",
                x=555.0,
                y=102.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.q5",
                prompt="",
                text="㉡ 물병",
                style_role="footer",
                x=1.0,
                y=452.0,
                font_size=24,
            ),
            TextSlot(
                id="slot.q6", prompt="", text="", style_role="label", x=560.0, y=90.0, font_size=28
            ),
            TextSlot(
                id="slot.q7", prompt="", text="", style_role="label", x=0.0, y=0.0, font_size=28
            ),
            TextSlot(
                id="slot.q8", prompt="", text="", style_role="label", x=0.0, y=0.0, font_size=28
            ),
        ),
        diagrams=(),
        groups=(),
        constraints=(),
        tags=(),
    )


PROBLEM_TEMPLATE = build_problem_template()

SEMANTIC_OVERRIDE = {
    "problem_id": "S3_초등_3_008744",
    "problem_type": "capacity_comparison_choice",
    "metadata": {
        "language": "ko",
        "question": "두 물병의 들이를 비교하여 알맞은 말을 선택하는 문제",
        "instruction": "들이가 더 많은 것을 고르기",
    },
    "domain": {
        "objects": [
            {"id": "obj.bottle_a", "type": "container", "name": "㉠ 물병"},
            {"id": "obj.bottle_b", "type": "container", "name": "㉡ 물병"},
            {
                "id": "obj.water_transfer",
                "type": "transfer",
                "description": "한 물병의 물을 다른 물병에 옮겨 담는 상황",
            },
        ],
        "relations": [],
        "problem_solving": {
            "understand": {
                "given_refs": ["obj.bottle_a", "obj.bottle_b", "obj.water_transfer"],
                "target_ref": "answer.target",
                "condition_refs": ["rel.compare_capacity"],
            },
            "plan": {
                "method": "transfer_comparison",
                "description": "한 병의 물이 다른 병에 모두 들어가는지의 설명을 보고 들이가 더 큰 물병을 고른다.",
            },
            "execute": {"expected_operations": ["compare_by_transfer", "choose_larger_capacity"]},
            "review": {"check_methods": ["statement_consistency_check"]},
        },
    },
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {"type": "choice", "description": "들이가 더 많은 물병 고르기"},
        "value": 0,
        "unit": "",
    },
}

SOLVABLE = {
    "schema": "modu.solvable.v1.1",
    "problem_id": "S3_초등_3_008744",
    "problem_type": "capacity_comparison_choice",
    "inputs": {
        "total_ticks": 0,
        "target_label": "들이가 더 많은 것은",
        "target_ticks": 0,
        "target_count": 2,
        "unit": "",
    },
    "given": [
        {"ref": "obj.bottle_a", "value": {"name": "㉠ 물병"}},
        {"ref": "obj.bottle_b", "value": {"name": "㉡ 물병"}},
        {
            "ref": "obj.water_transfer",
            "value": {"description": "한 물병의 물을 다른 물병에 옮겨 담는 상황"},
        },
    ],
    "target": {"ref": "answer.target", "type": "choice"},
    "method": "transfer_comparison",
    "plan": [
        "그림과 문장을 읽고 두 물병의 들이를 비교한다.",
        "한 물병의 물이 다른 물병에 모두 들어가는지에 따라 더 큰 들이를 판단한다.",
    ],
    "steps": [
        {
            "id": "step.1",
            "expr": "㉠ 물병의 물이 ㉡ 물병에 모두 들어가면 ㉡ 물병의 들이가 더 큼",
            "value": 0,
        },
        {
            "id": "step.2",
            "expr": "㉡ 물병의 물이 ㉠ 물병에 모두 들어가면 ㉠ 물병의 들이가 더 큼",
            "value": 0,
        },
        {"id": "step.3", "expr": "알맞은 말 선택", "value": "확인 필요"},
    ],
    "checks": [
        {
            "id": "check.1",
            "expr": "선택지가 ㉠ 물병, ㉡ 물병 두 개인지 확인",
            "expected": 2,
            "actual": 2,
            "pass": True,
        },
        {
            "id": "check.2",
            "expr": "정답이 그림의 붓기 비교 설명과 일치하는지 확인",
            "expected": True,
            "actual": True,
            "pass": True,
        },
    ],
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [],
        "target": {"type": "choice", "description": "들이가 더 많은 물병 고르기"},
        "value": 0,
        "unit": "",
    },
}
