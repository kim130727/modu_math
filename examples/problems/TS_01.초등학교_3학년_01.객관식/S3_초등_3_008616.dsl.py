from __future__ import annotations

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


def build_problem_template() -> ProblemTemplate:
    speakers = (
        SpeakerSpec(
            key="left",
            cx=245,
            bubble_cy=211,
            head_cy=322,
            text="몫이\n10보다 작아.",
            name="근희",
            hair="#c77816",
            shirt="#f5ae12",
            bow="#ffffff",
            pigtails=True,
            tail_y=267,
            name_width=71,
        ),
        SpeakerSpec(
            key="mid",
            cx=486,
            bubble_cy=210,
            head_cy=321,
            text="나머지가 0으로\n나누어떨어져.",
            name="영표",
            hair="#4c3a25",
            shirt="#f5ae12",
            bow="#5da6df",
            tail_y=265,
        ),
        SpeakerSpec(
            key="right",
            cx=724,
            bubble_cy=211,
            head_cy=322,
            text="나머지가\n8보다 작아.",
            name="슬기",
            hair="#9d4136",
            shirt="#c9648f",
            bow="#e33f83",
            bubble_width=180,
            tail_y=267,
            name_width=70,
        ),
    )
    return ProblemTemplate(
        id="S3_초등_3_008616",
        title="문제를 바르게 설명한 사람 찾기",
        canvas=Canvas(width=872, height=650, coordinate_mode="logical"),
        regions=(
            Region(
                id="region.stem",
                role="stem",
                flow="absolute",
                slot_ids=(
                    "slot.q.box",
                    "slot.q.num",
                    "slot.q.text",
                    "slot.eq.box",
                    "slot.eq.text",
                    "slot.eq.blank1",
                    "slot.eq.dots",
                    "slot.eq.blank2",
                    *speaker_group_slot_ids(speakers),
                    "slot.answer.label",
                    "slot.answer.value",
                    "slot.explain.label",
                    "slot.explain.eq",
                    "slot.explain.left",
                    "slot.explain.mid",
                    "slot.explain.right",
                    "slot.explain.final",
                ),
            ),
        ),
        slots=(
            RectSlot(id="slot.q.box", prompt="", x=18, y=15, width=12, height=12, stroke="#333333", stroke_width=1, fill="#ffffff"),
            TextSlot(id="slot.q.num", prompt="", text="86.", style_role="question", x=39, y=28, font_size=25),
            TextSlot(
                id="slot.q.text",
                prompt="",
                text="문제를 바르게 설명한 사람이 누구인지 찾아 선택하세요.",
                style_role="question",
                x=80,
                y=28,
                font_size=27,
            ),
            RectSlot(
                id="slot.eq.box",
                prompt="",
                x=296,
                y=43,
                width=378,
                height=78,
                stroke="#75bd3a",
                stroke_width=2,
                fill="#eef4d8",
            ),
            TextSlot(id="slot.eq.text", prompt="", text="99 ÷ 8 =", style_role="math", x=392, y=91, font_size=25),
            RectSlot(id="slot.eq.blank1", prompt="", x=500, y=70, width=26, height=26, stroke="#111111", stroke_width=2, fill="#f5f7e8"),
            TextSlot(id="slot.eq.dots", prompt="", text="⋯", style_role="math", x=532, y=91, font_size=27),
            RectSlot(id="slot.eq.blank2", prompt="", x=551, y=70, width=26, height=26, stroke="#111111", stroke_width=2, fill="#f5f7e8"),
            *speaker_group_slots(speakers),
            TextSlot(id="slot.answer.label", prompt="", text="(정답)", style_role="body", x=18, y=457, font_size=17),
            TextSlot(id="slot.answer.value", prompt="", text="슬기", style_role="body", x=63, y=457, font_size=22),
            TextSlot(id="slot.explain.label", prompt="", text="(해설)", style_role="body", x=18, y=506, font_size=17),
            TextSlot(id="slot.explain.eq", prompt="", text="99 ÷ 8 = 12⋯3", style_role="math", x=63, y=506, font_size=23),
            TextSlot(id="slot.explain.left", prompt="", text="근희: 몫은 12이므로 10보다 큽니다.", style_role="body", x=37, y=540, font_size=22),
            TextSlot(id="slot.explain.mid", prompt="", text="영표: 나머지는 3이므로 나누어떨어지지 않습니다.", style_role="body", x=37, y=573, font_size=22),
            TextSlot(id="slot.explain.right", prompt="", text="슬기: 나머지는 3이므로 8보다 작습니다.", style_role="body", x=37, y=607, font_size=22),
            TextSlot(id="slot.explain.final", prompt="", text="따라서 문제를 바르게 설명한 사람은 슬기입니다.", style_role="body", x=37, y=641, font_size=22),
        ),
        diagrams=(),
        groups=(),
        constraints=(),
        tags=("division", "remainder", "speech", "characters"),
    )


PROBLEM_TEMPLATE = build_problem_template()

SEMANTIC_OVERRIDE = {
    "problem_id": "S3_초등_3_008616",
    "problem_type": "division_reasoning",
    "metadata": {
        "language": "ko",
        "question": "문제를 바르게 설명한 사람이 누구인지 찾아 선택하세요.",
        "instruction": "99를 8로 나눈 몫과 나머지를 확인해 바르게 설명한 사람을 고른다.",
    },
    "domain": {
        "objects": [
            {"id": "obj.dividend", "type": "number", "value": 99},
            {"id": "obj.divisor", "type": "number", "value": 8},
            {"id": "obj.claim.geunhui", "type": "student_claim", "speaker": "근희", "statement": "몫은 10보다 작다."},
            {"id": "obj.claim.yeongpyo", "type": "student_claim", "speaker": "영표", "statement": "나머지는 0으로 나누어떨어진다."},
            {"id": "obj.claim.seulgi", "type": "student_claim", "speaker": "슬기", "statement": "나머지는 8보다 작다."},
        ],
        "relations": [
            {
                "id": "rel.division_result",
                "type": "division_with_remainder",
                "from_id": "obj.dividend",
                "to_id": "obj.divisor",
                "quotient": 12,
                "remainder": 3,
            },
            {
                "id": "rel.correct_speaker",
                "type": "correct_claim",
                "from_id": "obj.claim.seulgi",
                "to_id": "answer.target",
            },
        ],
        "problem_solving": {
            "understand": {
                "given_refs": ["obj.dividend", "obj.divisor", "obj.claim.geunhui", "obj.claim.yeongpyo", "obj.claim.seulgi"],
                "target_ref": "answer.target",
                "condition_refs": ["rel.division_result", "rel.correct_speaker"],
            },
            "plan": {
                "method": "division_with_remainder_check",
                "description": "99를 8로 나눈 몫과 나머지를 구하고 각 설명의 참거짓을 비교한다.",
            },
            "execute": {
                "expected_operations": ["compute_quotient", "compute_remainder", "compare_claims"],
            },
            "review": {
                "check_methods": ["division_identity_check", "remainder_less_than_divisor"],
            },
        },
    },
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [{"value": "슬기"}],
        "target": {"type": "correct_speaker", "description": "문제를 바르게 설명한 사람"},
        "value": "슬기",
        "unit": "",
    },
}

SOLVABLE = {
    "schema": "modu.solvable.v1.1",
    "problem_id": "S3_초등_3_008616",
    "problem_type": "division_reasoning",
    "inputs": {
        "target_label": "문제를 바르게 설명한 사람",
        "dividend": 99,
        "divisor": 8,
        "unit": "",
    },
    "given": [
        {"ref": "obj.dividend", "value": 99},
        {"ref": "obj.divisor", "value": 8},
        {"ref": "obj.claim.geunhui", "value": "몫은 10보다 작다."},
        {"ref": "obj.claim.yeongpyo", "value": "나머지는 0으로 나누어떨어진다."},
        {"ref": "obj.claim.seulgi", "value": "나머지는 8보다 작다."},
    ],
    "target": {"ref": "answer.target", "type": "correct_speaker"},
    "method": "division_with_remainder_check",
    "plan": [
        "99를 8로 나누어 몫과 나머지를 구한다.",
        "각 학생의 설명이 계산 결과와 맞는지 비교한다.",
    ],
    "steps": [
        {"id": "step.1", "expr": "99 ÷ 8", "value": {"quotient": 12, "remainder": 3}},
        {"id": "step.2", "expr": "몫 12는 10보다 작은가?", "value": False},
        {"id": "step.3", "expr": "나머지 3은 0인가?", "value": False},
        {"id": "step.4", "expr": "나머지 3은 8보다 작은가?", "value": True},
    ],
    "checks": [
        {"id": "check.1", "expr": "99 = 8 × 12 + 3", "expected": True, "actual": True, "pass": True},
        {"id": "check.2", "expr": "3 < 8", "expected": True, "actual": True, "pass": True},
    ],
    "answer": {
        "blanks": [],
        "choices": [],
        "answer_key": [{"value": "슬기"}],
        "target": {"type": "correct_speaker", "description": "문제를 바르게 설명한 사람"},
        "value": "슬기",
        "unit": "",
    },
}
