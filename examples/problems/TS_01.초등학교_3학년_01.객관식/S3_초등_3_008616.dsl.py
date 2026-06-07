from __future__ import annotations

from dataclasses import dataclass

from modu_math.dsl import (
    Canvas,
    CircleSlot,
    PathSlot,
    PolygonSlot,
    ProblemTemplate,
    RectSlot,
    Region,
    TextSlot,
)


CharacterSlot = CircleSlot | PathSlot | PolygonSlot | RectSlot | TextSlot


@dataclass(frozen=True)
class SpeakerSpec:
    key: str
    cx: float
    bubble_cy: float
    head_cy: float
    text: str
    name: str
    hair: str
    shirt: str
    bow: str | None = None
    pigtails: bool = False
    bubble_width: float = 178
    bubble_height: float = 82
    tail_y: float | None = None
    name_width: float = 72


def speech_balloon_slots(
    prefix: str,
    *,
    cx: float,
    cy: float,
    width: float,
    height: float,
    tail_x: float,
    tail_y: float,
    text: str,
) -> tuple[PathSlot, PolygonSlot, TextSlot]:
    rx = width / 2
    ry = height / 2
    d = (
        f"M {cx - rx} {cy} "
        f"C {cx - rx} {cy - ry * 0.72}, {cx - rx * 0.62} {cy - ry}, {cx} {cy - ry} "
        f"C {cx + rx * 0.62} {cy - ry}, {cx + rx} {cy - ry * 0.72}, {cx + rx} {cy} "
        f"C {cx + rx} {cy + ry * 0.72}, {cx + rx * 0.62} {cy + ry}, {cx} {cy + ry} "
        f"C {cx - rx * 0.62} {cy + ry}, {cx - rx} {cy + ry * 0.72}, {cx - rx} {cy} Z"
    )
    return (
        PathSlot(
            id=f"{prefix}.bubble",
            prompt="",
            d=d,
            stroke="#222222",
            stroke_width=1.6,
            fill="#ffffff",
        ),
        PolygonSlot(
            id=f"{prefix}.tail",
            prompt="",
            points=((tail_x - 10, cy + ry - 6), (tail_x + 10, cy + ry - 6), (tail_x, tail_y)),
            stroke="#222222",
            stroke_width=1.4,
            fill="#ffffff",
        ),
        TextSlot(
            id=f"{prefix}.text",
            prompt="",
            text=text,
            style_role="speech",
            x=cx,
            y=cy - 9,
            font_size=24,
            anchor="middle",
        ),
    )


def person_slots(
    prefix: str,
    *,
    cx: float,
    head_cy: float,
    hair: str,
    shirt: str,
    bow: str | None = None,
    pigtails: bool = False,
) -> tuple[CharacterSlot, ...]:
    face = "#ffd9ad"
    slots: list[CharacterSlot] = [
        PolygonSlot(
            id=f"{prefix}.body",
            prompt="",
            points=((cx - 28, head_cy + 73), (cx + 28, head_cy + 73), (cx + 18, head_cy + 37), (cx - 18, head_cy + 37)),
            stroke="none",
            fill=shirt,
        ),
        CircleSlot(
            id=f"{prefix}.head",
            prompt="",
            cx=cx,
            cy=head_cy,
            r=28,
            stroke="none",
            fill=face,
        ),
        PathSlot(
            id=f"{prefix}.hair.cap",
            prompt="",
            d=(
                f"M {cx - 28} {head_cy - 1} "
                f"C {cx - 26} {head_cy - 30}, {cx + 25} {head_cy - 35}, {cx + 29} {head_cy - 1} "
                f"C {cx + 10} {head_cy - 17}, {cx - 12} {head_cy - 10}, {cx - 28} {head_cy - 1} Z"
            ),
            stroke="none",
            fill=hair,
        ),
        CircleSlot(id=f"{prefix}.eye.left", prompt="", cx=cx - 10, cy=head_cy + 4, r=2.3, stroke="none", fill="#2b2118"),
        CircleSlot(id=f"{prefix}.eye.right", prompt="", cx=cx + 10, cy=head_cy + 4, r=2.3, stroke="none", fill="#2b2118"),
        PathSlot(
            id=f"{prefix}.smile",
            prompt="",
            d=f"M {cx - 7} {head_cy + 16} Q {cx} {head_cy + 22} {cx + 7} {head_cy + 16}",
            stroke="#b86e39",
            stroke_width=1.3,
            fill="none",
        ),
    ]
    if pigtails:
        slots.extend(
            [
                PathSlot(
                    id=f"{prefix}.tail.left",
                    prompt="",
                    d=f"M {cx - 27} {head_cy - 3} C {cx - 52} {head_cy + 1}, {cx - 38} {head_cy + 42}, {cx - 50} {head_cy + 48}",
                    stroke=hair,
                    stroke_width=7,
                    fill="none",
                ),
                PathSlot(
                    id=f"{prefix}.tail.right",
                    prompt="",
                    d=f"M {cx + 27} {head_cy - 3} C {cx + 52} {head_cy + 1}, {cx + 38} {head_cy + 42}, {cx + 50} {head_cy + 48}",
                    stroke=hair,
                    stroke_width=7,
                    fill="none",
                ),
            ]
        )
    if bow:
        slots.extend(
            [
                PolygonSlot(
                    id=f"{prefix}.bow.left",
                    prompt="",
                    points=((cx - 7, head_cy + 43), (cx - 26, head_cy + 35), (cx - 14, head_cy + 56)),
                    stroke="none",
                    fill=bow,
                ),
                PolygonSlot(
                    id=f"{prefix}.bow.right",
                    prompt="",
                    points=((cx + 7, head_cy + 43), (cx + 26, head_cy + 35), (cx + 14, head_cy + 56)),
                    stroke="none",
                    fill=bow,
                ),
            ]
        )
    return tuple(slots)


def speaker_slot_ids(speaker: SpeakerSpec) -> tuple[str, ...]:
    prefix = f"slot.{speaker.key}"
    person_prefix = f"{prefix}.person"
    ids = [
        f"{prefix}.bubble",
        f"{prefix}.tail",
        f"{prefix}.text",
        f"{person_prefix}.body",
        f"{person_prefix}.head",
        f"{person_prefix}.hair.cap",
        f"{person_prefix}.eye.left",
        f"{person_prefix}.eye.right",
        f"{person_prefix}.smile",
    ]
    if speaker.pigtails:
        ids.extend((f"{person_prefix}.tail.left", f"{person_prefix}.tail.right"))
    if speaker.bow:
        ids.extend((f"{person_prefix}.bow.left", f"{person_prefix}.bow.right"))
    ids.extend((f"slot.name.{speaker.key}.box", f"slot.name.{speaker.key}.text"))
    return tuple(ids)


def speaker_group_slot_ids(speakers: tuple[SpeakerSpec, ...]) -> tuple[str, ...]:
    return tuple(slot_id for speaker in speakers for slot_id in speaker_slot_ids(speaker))


def speaker_slots(speaker: SpeakerSpec) -> tuple[CharacterSlot, ...]:
    prefix = f"slot.{speaker.key}"
    tail_y = speaker.tail_y if speaker.tail_y is not None else speaker.head_cy - 55
    return (
        *speech_balloon_slots(
            prefix,
            cx=speaker.cx,
            cy=speaker.bubble_cy,
            width=speaker.bubble_width,
            height=speaker.bubble_height,
            tail_x=speaker.cx,
            tail_y=tail_y,
            text=speaker.text,
        ),
        *person_slots(
            f"{prefix}.person",
            cx=speaker.cx,
            head_cy=speaker.head_cy,
            hair=speaker.hair,
            shirt=speaker.shirt,
            bow=speaker.bow,
            pigtails=speaker.pigtails,
        ),
        RectSlot(
            id=f"slot.name.{speaker.key}.box",
            prompt="",
            x=speaker.cx - speaker.name_width / 2,
            y=383,
            width=speaker.name_width,
            height=36,
            rx=9,
            ry=9,
            stroke="#6fcf83",
            stroke_width=2,
            fill="#e9f7dd",
        ),
        TextSlot(
            id=f"slot.name.{speaker.key}.text",
            prompt="",
            text=speaker.name,
            style_role="label",
            x=speaker.cx,
            y=409,
            font_size=25,
            anchor="middle",
        ),
    )


def speaker_group_slots(speakers: tuple[SpeakerSpec, ...]) -> tuple[CharacterSlot, ...]:
    return tuple(slot for speaker in speakers for slot in speaker_slots(speaker))


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
