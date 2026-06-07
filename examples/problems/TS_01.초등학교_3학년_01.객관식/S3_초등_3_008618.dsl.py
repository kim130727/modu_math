from __future__ import annotations

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


class SpeakerSpec:
    def __init__(
        self,
        *,
        key: str,
        cx: float,
        bubble_cy: float,
        head_cy: float,
        text: str,
        name: str,
        hair: str,
        shirt: str,
        bow: str | None = None,
        pigtails: bool = False,
        bubble_width: float = 190,
        bubble_height: float = 52,
        tail_y: float | None = None,
        name_width: float = 68,
        name_y: float = 242,
    ) -> None:
        self.key = key
        self.cx = cx
        self.bubble_cy = bubble_cy
        self.head_cy = head_cy
        self.text = text
        self.name = name
        self.hair = hair
        self.shirt = shirt
        self.bow = bow
        self.pigtails = pigtails
        self.bubble_width = bubble_width
        self.bubble_height = bubble_height
        self.tail_y = tail_y
        self.name_width = name_width
        self.name_y = name_y


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
            stroke="#f5a000",
            stroke_width=2,
            fill="#ffffff",
        ),
        PolygonSlot(
            id=f"{prefix}.tail",
            prompt="",
            points=((tail_x - 9, cy + ry - 5), (tail_x + 9, cy + ry - 5), (tail_x, tail_y)),
            stroke="#f5a000",
            stroke_width=1.6,
            fill="#ffffff",
        ),
        TextSlot(
            id=f"{prefix}.text",
            prompt="",
            text=text,
            style_role="math",
            x=cx,
            y=cy + 8,
            font_size=28,
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
            y=speaker.name_y,
            width=speaker.name_width,
            height=34,
            rx=8,
            ry=8,
            stroke="#d58cc3",
            stroke_width=2,
            fill="#ffffff",
        ),
        TextSlot(
            id=f"slot.name.{speaker.key}.text",
            prompt="",
            text=speaker.name,
            style_role="label",
            x=speaker.cx,
            y=speaker.name_y + 25,
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
            cx=246,
            bubble_cy=78,
            head_cy=164,
            text="262÷2",
            name="소진",
            hair="#8b3f24",
            shirt="#f5b22a",
            bow="#ffffff",
            pigtails=True,
            bubble_width=198,
            tail_y=122,
        ),
        SpeakerSpec(
            key="mid",
            cx=486,
            bubble_cy=78,
            head_cy=164,
            text="440÷5",
            name="경수",
            hair="#6b5846",
            shirt="#21a85a",
            bubble_width=190,
            tail_y=122,
        ),
        SpeakerSpec(
            key="right",
            cx=724,
            bubble_cy=78,
            head_cy=164,
            text="552÷6",
            name="태희",
            hair="#725442",
            shirt="#ffd44d",
            bow="#d72b7b",
            pigtails=True,
            bubble_width=190,
            tail_y=122,
        ),
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
                slot_ids=("slot.check", "slot.qnum", "slot.qtext"),
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
                    "slot.answer.label",
                    "slot.answer.value",
                    "slot.explain.label",
                    "slot.explain.text",
                    "slot.explain.final",
                ),
            ),
        ),
        slots=(
            RectSlot(id="slot.check", prompt="", x=17, y=18, width=12, height=12, stroke="#333333", stroke_width=1, fill="#ffffff"),
            TextSlot(id="slot.qnum", prompt="", text="88.", style_role="question", x=40, y=30, font_size=28),
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
            TextSlot(id="slot.answer.label", prompt="", text="(정답)", style_role="body", x=17, y=311, font_size=18),
            TextSlot(id="slot.answer.value", prompt="", text="소진", style_role="body", x=63, y=311, font_size=24),
            TextSlot(id="slot.explain.label", prompt="", text="(해설)", style_role="body", x=17, y=356, font_size=18),
            TextSlot(
                id="slot.explain.text",
                prompt="",
                text="소진: 262 ÷ 2 = 131, 경수: 440 ÷ 5 = 88, 태희: 552 ÷ 6 = 92",
                style_role="body",
                x=63,
                y=356,
                font_size=24,
            ),
            TextSlot(
                id="slot.explain.final",
                prompt="",
                text="따라서 131>92>88이므로 몫이 가장 큰 나눗셈을 말한 사람은 소진입니다.",
                style_role="body",
                x=37,
                y=392,
                font_size=24,
            ),
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
