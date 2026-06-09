from __future__ import annotations
from modu_math.dsl import Canvas, ProblemTemplate, RectSlot, Region, SpeakerSpec, TextSlot, speaker_group_slot_ids, speaker_group_slots


def build_problem_template() -> ProblemTemplate:
    speakers = (
        SpeakerSpec(
            key="opt1",
            cx=222.5,
            bubble_cy=217.5,
            head_cy=325.0,
            text="몫은\n13이야.",
            name="형우",
            hair="#4b1f16",
            shirt="#D7A0D7",
            bubble_width=145.0,
            bubble_height=105.0,
            name_width=82.0,
            name_y=404.0,
            speech_font_size=28,
        ),
        SpeakerSpec(
            key="opt2",
            cx=477.5,
            bubble_cy=217.5,
            head_cy=325.0,
            text="나머지는\n5보다 작아.",
            name="희영",
            hair="#1d1714",
            shirt="#8ED7E6",
            bubble_width=145.0,
            bubble_height=105.0,
            name_width=82.0,
            name_y=404.0,
            speech_font_size=24,
            speech_text_dy=-5,
        ),
        SpeakerSpec(
            key="opt3",
            cx=732.5,
            bubble_cy=217.5,
            head_cy=325.0,
            text="나누어떨어지지\n않아.",
            name="성태",
            hair="#5b3218",
            shirt="#F2C66D",
            bubble_width=180.0,
            bubble_height=105.0,
            name_width=82.0,
            name_y=404.0,
            speech_font_size=24,
            speech_text_dy=-5,
        ),
    )
    return ProblemTemplate(
        id="S3_초등_3_008590",
        title="문제를 바르게 설명한 사람을 선택하세요.",
        canvas=Canvas(width=840, height=630, coordinate_mode="logical"),
        regions=(
            Region(
                id="region.stem",
                role="stem",
                flow="absolute",
                slot_ids=(
                    "slot.q1", "slot.eq.bg", "slot.eq.text", *speaker_group_slot_ids(speakers),
                ),
            ),
        ),
        slots=(
            TextSlot(id="slot.q1", prompt="", text = '문제를 바르게 설명한 사람을 선택하세요.', style_role="question", x = 155, y = 40, font_size = 30),
            RectSlot(id="slot.eq.bg", prompt="", x = 270, y = 70, width = 390, height = 80),
            TextSlot(id="slot.eq.text", prompt="", text = '68 ÷ 5 = □ ⦁⦁⦁ □', style_role="question", x = 355, y = 120, font_size = 30),
            *speaker_group_slots(speakers),
        ),
        diagrams=(), groups=(), constraints=(), tags=("초등", "수학", "나눗셈", "몫", "나머지", "선택형"),
    )


PROBLEM_TEMPLATE = build_problem_template()

SEMANTIC_OVERRIDE = {
    "problem_id": "S3_초등_3_008590",
    "problem_type": "division_explanation_choice",
    "metadata": {"language": "ko", "question": "문제를 바르게 설명한 사람을 선택하는 문항", "instruction": "68 ÷ 5의 결과를 설명한 내용 중 맞는 사람을 선택하세요."},
    "domain": {
        "objects": [
            {"id": "obj.dividend", "type": "number", "value": 68},
            {"id": "obj.divisor", "type": "number", "value": 5},
            {"id": "obj.person.left", "type": "person", "name": "형우"},
            {"id": "obj.person.middle", "type": "person", "name": "희영"},
            {"id": "obj.person.right", "type": "person", "name": "성태"},
        ],
        "relations": [],
        "problem_solving": {
            "understand": {"given_refs": ["obj.dividend", "obj.divisor"], "target_ref": "answer.target", "condition_refs": ["rel.choose_correct_explanation"]},
            "plan": {"method": "division_result_check", "description": "몫과 나머지의 성질을 이용해 맞는 설명을 고른다."},
            "execute": {"expected_operations": ["compute_quotient_remainder", "check_statements", "select_person"]},
            "review": {"check_methods": ["remainder_less_than_divisor", "selected_person_match"]},
        },
    },
    "answer": {"blanks": [], "choices": [], "answer_key": [], "target": {"type": "person_selection", "description": "문제를 바르게 설명한 사람"}, "value": "성태", "unit": ""},
}

SOLVABLE = {
    "schema": "modu.solvable.v1.1",
    "problem_id": "S3_초등_3_008590",
    "problem_type": "division_explanation_choice",
    "inputs": {"total_ticks": 0, "target_label": "문제를 바르게 설명한 사람", "target_ticks": 0, "target_count": 1, "unit": ""},
    "given": [
        {"ref": "obj.dividend", "value": 68},
        {"ref": "obj.divisor", "value": 5},
        {"ref": "obj.person.left", "value": "형우"},
        {"ref": "obj.person.middle", "value": "희영"},
        {"ref": "obj.person.right", "value": "성태"},
    ],
    "target": {"ref": "answer.target", "type": "person_selection"},
    "method": "division_result_check",
    "plan": ["68 ÷ 5의 몫과 나머지를 구한다.", "세 설명과 비교하여 맞는 사람을 고른다."],
    "steps": [
        {"id": "step.1", "expr": "68 ÷ 5", "value": {"quotient": 13, "remainder": 3}},
        {"id": "step.2", "expr": "나머지 < 나누는 수", "value": True},
        {"id": "step.3", "expr": "선택한 사람", "value": "성태"},
    ],
    "checks": [
        {"id": "check.1", "expr": "68 = 5 × 13 + 3", "expected": True, "actual": True, "pass": True},
        {"id": "check.2", "expr": "3 < 5", "expected": True, "actual": True, "pass": True},
    ],
    "answer": {"blanks": [], "choices": [], "answer_key": [], "target": {"type": "person_selection", "description": "문제를 바르게 설명한 사람"}, "value": "성태", "unit": ""},
}
