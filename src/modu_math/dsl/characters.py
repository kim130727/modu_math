from __future__ import annotations

from dataclasses import dataclass

from .models import CircleSlot, LineSlot, PathSlot, PolygonSlot, RectSlot, TextSlot

CharacterSlot = CircleSlot | LineSlot | PathSlot | PolygonSlot | RectSlot | TextSlot


def character_body_slots(
    prefix: str,
    *,
    cx: float,
    head_cy: float,
    hair: str,
    shirt: str,
    glasses: bool = False,
) -> tuple[CharacterSlot, ...]:
    face = "#ffd8b3"
    slots: list[CharacterSlot] = [
        PolygonSlot(
            id=f"{prefix}.body",
            prompt="",
            points=((cx - 35, head_cy + 95), (cx + 35, head_cy + 95), (cx + 24, head_cy + 42), (cx - 24, head_cy + 42)),
            stroke="none",
            fill=shirt,
        ),
        CircleSlot(id=f"{prefix}.ear.left", prompt="", cx=cx - 31, cy=head_cy + 3, r=9, stroke="none", fill=face),
        CircleSlot(id=f"{prefix}.ear.right", prompt="", cx=cx + 31, cy=head_cy + 3, r=9, stroke="none", fill=face),
        CircleSlot(id=f"{prefix}.head", prompt="", cx=cx, cy=head_cy, r=29, stroke="none", fill=face),
        PathSlot(
            id=f"{prefix}.hair.cap",
            prompt="",
            d=(
                f"M {cx - 29} {head_cy - 1} "
                f"C {cx - 27} {head_cy - 32}, {cx + 28} {head_cy - 35}, {cx + 30} {head_cy - 1} "
                f"C {cx + 15} {head_cy - 18}, {cx + 3} {head_cy - 8}, {cx - 4} {head_cy - 20} "
                f"C {cx - 12} {head_cy - 7}, {cx - 22} {head_cy - 18}, {cx - 29} {head_cy - 1} Z"
            ),
            stroke="none",
            fill=hair,
        ),
        CircleSlot(id=f"{prefix}.eye.left", prompt="", cx=cx - 10, cy=head_cy + 6, r=3.8, stroke="none", fill="#2b2118"),
        CircleSlot(id=f"{prefix}.eye.right", prompt="", cx=cx + 10, cy=head_cy + 6, r=3.8, stroke="none", fill="#2b2118"),
        PathSlot(
            id=f"{prefix}.smile",
            prompt="",
            d=f"M {cx - 8} {head_cy + 18} Q {cx} {head_cy + 25} {cx + 8} {head_cy + 18}",
            stroke="#b76b3a",
            stroke_width=1.6,
            fill="none",
        ),
    ]
    if glasses:
        slots.extend(
            [
                CircleSlot(id=f"{prefix}.glasses.left", prompt="", cx=cx - 11, cy=head_cy + 5, r=13, stroke="#27b7be", stroke_width=3, fill="none"),
                CircleSlot(id=f"{prefix}.glasses.right", prompt="", cx=cx + 11, cy=head_cy + 5, r=13, stroke="#27b7be", stroke_width=3, fill="none"),
                LineSlot(id=f"{prefix}.glasses.bridge", prompt="", x1=cx - 1, y1=head_cy + 5, x2=cx + 1, y2=head_cy + 5, stroke="#27b7be", stroke_width=3),
            ]
        )
    return tuple(slots)


def character_hand_slots(prefix: str, *, card_x: float, card_y: float, card_width: float) -> tuple[CircleSlot, CircleSlot]:
    return (
        CircleSlot(id=f"{prefix}.hand.left", prompt="", cx=card_x - 5, cy=card_y + 31, r=5, stroke="none", fill="#ffd8b3"),
        CircleSlot(id=f"{prefix}.hand.right", prompt="", cx=card_x + card_width + 5, cy=card_y + 31, r=5, stroke="none", fill="#ffd8b3"),
    )


def character_body_slot_ids(prefix: str, *, glasses: bool = False) -> tuple[str, ...]:
    ids = (
        f"{prefix}.body",
        f"{prefix}.ear.left",
        f"{prefix}.ear.right",
        f"{prefix}.head",
        f"{prefix}.hair.cap",
        f"{prefix}.eye.left",
        f"{prefix}.eye.right",
        f"{prefix}.smile",
    )
    if glasses:
        ids = (*ids, f"{prefix}.glasses.left", f"{prefix}.glasses.right", f"{prefix}.glasses.bridge")
    return ids


def character_hand_slot_ids(prefix: str) -> tuple[str, str]:
    return (f"{prefix}.hand.left", f"{prefix}.hand.right")


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
    name_y: float = 383
    name_height: float = 36
    name_rx: float = 9
    name_ry: float = 9
    name_stroke: str = "#6fcf83"
    name_fill: str = "#e9f7dd"
    bubble_stroke: str = "#222222"
    bubble_stroke_width: float = 1.6
    tail_half_width: float = 10
    tail_base_dy: float = -6
    tail_stroke_width: float = 1.4
    speech_style_role: str = "speech"
    speech_font_size: int = 24
    speech_text_dy: float = -9
    name_text_dy: float = 26


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
    stroke: str = "#222222",
    stroke_width: float = 1.6,
    tail_half_width: float = 10,
    tail_base_dy: float = -6,
    tail_stroke_width: float = 1.4,
    style_role: str = "speech",
    font_size: int = 24,
    text_dy: float = -9,
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
        PathSlot(id=f"{prefix}.bubble", prompt="", d=d, stroke=stroke, stroke_width=stroke_width, fill="#ffffff"),
        PolygonSlot(
            id=f"{prefix}.tail",
            prompt="",
            points=((tail_x - tail_half_width, cy + ry + tail_base_dy), (tail_x + tail_half_width, cy + ry + tail_base_dy), (tail_x, tail_y)),
            stroke=stroke,
            stroke_width=tail_stroke_width,
            fill="#ffffff",
        ),
        TextSlot(
            id=f"{prefix}.text",
            prompt="",
            text=text,
            style_role=style_role,
            x=cx,
            y=cy + text_dy,
            font_size=font_size,
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
        CircleSlot(id=f"{prefix}.head", prompt="", cx=cx, cy=head_cy, r=28, stroke="none", fill=face),
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
                PolygonSlot(id=f"{prefix}.bow.left", prompt="", points=((cx - 7, head_cy + 43), (cx - 26, head_cy + 35), (cx - 14, head_cy + 56)), stroke="none", fill=bow),
                PolygonSlot(id=f"{prefix}.bow.right", prompt="", points=((cx + 7, head_cy + 43), (cx + 26, head_cy + 35), (cx + 14, head_cy + 56)), stroke="none", fill=bow),
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
            stroke=speaker.bubble_stroke,
            stroke_width=speaker.bubble_stroke_width,
            tail_half_width=speaker.tail_half_width,
            tail_base_dy=speaker.tail_base_dy,
            tail_stroke_width=speaker.tail_stroke_width,
            style_role=speaker.speech_style_role,
            font_size=speaker.speech_font_size,
            text_dy=speaker.speech_text_dy,
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
            height=speaker.name_height,
            rx=speaker.name_rx,
            ry=speaker.name_ry,
            stroke=speaker.name_stroke,
            stroke_width=2,
            fill=speaker.name_fill,
        ),
        TextSlot(
            id=f"slot.name.{speaker.key}.text",
            prompt="",
            text=speaker.name,
            style_role="label",
            x=speaker.cx,
            y=speaker.name_y + speaker.name_text_dy,
            font_size=25,
            anchor="middle",
        ),
    )


def speaker_group_slots(speakers: tuple[SpeakerSpec, ...]) -> tuple[CharacterSlot, ...]:
    return tuple(slot for speaker in speakers for slot in speaker_slots(speaker))
