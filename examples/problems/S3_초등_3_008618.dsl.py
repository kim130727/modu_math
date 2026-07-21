from __future__ import annotations

from typing import Any

from modu_math.dsl import (
    Canvas,
    ProblemTemplate,
    RectSlot,
    Region,
    SpeakerSpec,
    TextSlot,
    speaker_group_slot_ids,
    speaker_group_slots,
)


def comparison_speaker(**kwargs: Any) -> SpeakerSpec:
    return SpeakerSpec(
        bubble_height=52,
        tail_half_width=9,
        tail_base_dy=-5,
        bubble_stroke="#f5a000",
        bubble_stroke_width=2,
        tail_stroke_width=1.6,
        speech_style_role="math",
        speech_font_size=28,
        speech_text_dy=8,
        name_width=68,
        name_y=242,
        name_height=34,
        name_rx=8,
        name_ry=8,
        name_stroke="#d58cc3",
        name_fill="#ffffff",
        name_text_dy=25,
        **kwargs,
    )


def build_problem_template() -> ProblemTemplate:
    speakers = (
        comparison_speaker(
            key="left",
            cx = ((246) + (-65.0)) + (-55.0), bubble_cy = ((78) + (30.0)) + (25.0), head_cy = ((164) + (30.0)) + (25.0), text="262÷2",
            name="소진",
            hair="#8b3f24",
            shirt="#f5b22a",
            bow="#ffffff",
            pigtails=True,
            bubble_width=198,
            tail_y = ((122) + (30.0)) + (25.0), name_y = (272.0) + (25.0)),
        comparison_speaker(
            key="mid",
            cx = (486) + (-65.0), bubble_cy = (78) + (30.0), head_cy = (164) + (30.0), text="440÷5",
            name="경수",
            hair="#6b5846",
            shirt="#21a85a",
            bubble_width=190,
            tail_y = (122) + (30.0), name_y = 272.0),
        comparison_speaker(
            key="right",
            cx = (724) + (-65.0), bubble_cy = (78) + (30.0), head_cy = (164) + (30.0), text="552÷6",
            name="태희",
            hair="#725442",
            shirt="#ffd44d",
            bow="#d72b7b",
            pigtails=True,
            bubble_width=190,
            tail_y = (122) + (30.0), name_y = 272.0),
    )
    return ProblemTemplate(
        id="S3_초등_3_008618",
        title="몫이 가장 큰 나눗셈을 말한 사람 선택하기",
        canvas=Canvas(width=886, height=430, coordinate_mode="logical"),
        regions=(
            Region(
                id="region.stem",
                role="stem",
                flow="absolute",
                slot_ids=("slot.qtext",),
            ),
            Region(
                id="region.diagram",
                role="diagram",
                flow="absolute",
                slot_ids=speaker_group_slot_ids(speakers),
            ),
            Region(
                id="region.answer",
                role="answer",
                flow="absolute",
                slot_ids=(
                    
                    
                    
                ),
            ),
        ),
        slots=(
            TextSlot(
                id="slot.qtext",
                prompt="",
                text="몫이 가장 큰 나눗셈을 말한 사람을 선택해 보세요.",
                style_role="question",
                x=84,
                y=30,
                font_size=28,
            ),
            *speaker_group_slots(speakers),
            
            
            
        ),
        diagrams=(),
        groups=(),
        constraints=(),
        tags=("division", "quotient", "comparison", "speech", "characters"),
    )


PROBLEM_TEMPLATE = build_problem_template()

SEMANTIC_OVERRIDE = {
    "problem_id": "S3_초등_3_008618",
    "problem_type": "compare_division_results",
    "metadata": {
        "language": "ko",
        "question": "몫이 가장 큰 나눗셈을 말한 사람을 선택해 보세요.",
        "instruction": "세 나눗셈의 몫을 비교하여 가장 큰 값을 말한 사람을 찾는다.",
    },
    "domain": {
        "objects": [
            {"id": "obj.sojin", "type": "person", "name": "소진"},
            {"id": "obj.gyeongsu", "type": "person", "name": "경수"},
            {"id": "obj.taehee", "type": "person", "name": "태희"},
            {"id": "obj.expr.sojin", "type": "division_expression", "expression": "262 ÷ 2", "speaker": "obj.sojin"},
            {"id": "obj.expr.gyeongsu", "type": "division_expression", "expression": "440 ÷ 5", "speaker": "obj.gyeongsu"},
            {"id": "obj.expr.taehee", "type": "division_expression", "expression": "552 ÷ 6", "speaker": "obj.taehee"},
        ],
        "relations": [
            {"id": "rel.result.sojin", "type": "division_result", "from_id": "obj.expr.sojin", "to_id": "obj.sojin", "quotient": 131},
            {"id": "rel.result.gyeongsu", "type": "division_result", "from_id": "obj.expr.gyeongsu", "to_id": "obj.gyeongsu", "quotient": 88},
            {"id": "rel.result.taehee", "type": "division_result", "from_id": "obj.expr.taehee", "to_id": "obj.taehee", "quotient": 92},
            {"id": "rel.correct_speaker", "type": "max_quotient_speaker", "from_id": "obj.sojin", "to_id": "answer.target"},
        ],
    },
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [{"value": "소진"}],
        "target": {"type": "person_name", "description": "몫이 가장 큰 나눗셈을 말한 사람"},
        "value": "소진",
        "unit": "",
    },
}

SOLVABLE = {
    "schema": "modu.solvable.v1.1",
    "problem_id": "S3_초등_3_008618",
    "problem_type": "compare_division_results",
    "inputs": {
        "target_label": "몫이 가장 큰 나눗셈을 말한 사람",
        "unit": "",
    },
    "given": [
        {"ref": "obj.expr.sojin", "value": {"expression": "262 ÷ 2", "left": 262, "right": 2}},
        {"ref": "obj.expr.gyeongsu", "value": {"expression": "440 ÷ 5", "left": 440, "right": 5}},
        {"ref": "obj.expr.taehee", "value": {"expression": "552 ÷ 6", "left": 552, "right": 6}},
    ],
    "target": {"ref": "answer.target", "type": "person_name"},
    "method": "compare_division_results",
    "plan": [
        "각 나눗셈의 몫을 계산한다.",
        "계산한 몫을 비교하여 가장 큰 값을 찾는다.",
        "그 값을 말한 사람을 고른다.",
    ],
    "steps": [
        {"id": "step.1", "expr": "262 ÷ 2", "value": 131},
        {"id": "step.2", "expr": "440 ÷ 5", "value": 88},
        {"id": "step.3", "expr": "552 ÷ 6", "value": 92},
        {"id": "step.4", "expr": "max(131, 88, 92)", "value": 131},
        {"id": "step.5", "expr": "몫이 가장 큰 나눗셈을 말한 사람", "value": "소진"},
    ],
    "checks": [
        {"id": "check.1", "expr": "131 > 92 > 88", "expected": True, "actual": True, "pass": True},
        {"id": "check.2", "expr": "max(131, 88, 92) == 131", "expected": True, "actual": True, "pass": True},
    ],
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [{"value": "소진"}],
        "target": {"type": "person_name", "description": "몫이 가장 큰 나눗셈을 말한 사람"},
        "value": "소진",
        "unit": "",
    },
}
