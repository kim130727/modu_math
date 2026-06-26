from __future__ import annotations
from modu_math.dsl import Canvas, ProblemTemplate, Region, RectSlot, TextSlot, ImageSlot


def build_problem_template() -> ProblemTemplate:
    return ProblemTemplate(
        id="S3_초등_3_008744",
        title="들이 비교",
        canvas=Canvas(width=940, height=460, coordinate_mode="logical"),
        regions=(
            Region(
                id="region.stem",
                role="stem",
                flow="absolute",
                slot_ids=("slot.q1", "slot.q2", "slot.q1.copy1", "slot.inserted.image.1"),
            ),
            Region(
                id="region.diagram",
                role="diagram",
                flow="absolute",
                slot_ids=("slot.diagram.arrow",),
            ),
            Region(id="region.choice", role="choice", flow="absolute", slot_ids=()),
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
                text="그림과 같이 ㉮ 물병에 물을 가득 채운 후 ㉯ 물병에 옮겨 담아",
                style_role="question",
                x=6.0,
                y=26.0,
                font_size=28,
            ),
            TextSlot(
                id="slot.q2",
                prompt="",
                text="들이가 더 많은 것은 ( ㉮ 물병, ㉯ 물병 )입니다.",
                style_role="question",
                x=14,
                y=411,
                font_size=30,
                fill="#111111",
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
                id="slot.q6", prompt="", text="", style_role="label", x=560.0, y=90.0, font_size=28
            ),
            TextSlot(
                id="slot.q7", prompt="", text="", style_role="label", x=0.0, y=0.0, font_size=28
            ),
            TextSlot(
                id="slot.q8", prompt="", text="", style_role="label", x=0.0, y=0.0, font_size=28
            ),
            TextSlot(
                id="slot.q1.copy1",
                prompt="",
                text="㉮ 물병과 ㉯ 물병의 들이를 비교하려고 합니다. 알맞은 말을 선택하세요.",
                x=6,
                y=71,
                font_size=28,
                fill="#111111",
            ),
            ImageSlot(
                id="slot.inserted.image.1",
                prompt="",
                href="data:image/png;base64,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",
                x=265,
                y=100,
                width=280,
                height=265,
                preserve_aspect_ratio="xMidYMid meet",
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
