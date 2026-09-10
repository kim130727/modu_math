from __future__ import annotations

from .models.base import TextSlot


def columnar_number_slots(
    *,
    id_prefix: str,
    value: str | int,
    right_x: float,
    y: float,
    column_width: float,
    prompt: str = "",
    style_role: str = "diagram",
    font_size: int | None = 28,
    fill: str = "#111111",
    semantic_role: str | None = "diagram_label",
) -> tuple[TextSlot, ...]:
    """Place each digit in a fixed right-aligned arithmetic column.

    Spaces must never be used to align columnar arithmetic: their rendered
    width changes with the active font and preview engine. The generated slot
    identity is based on place-from-right (0=ones, 1=tens, ...), so editor
    overrides also remain stable when a row is rebuilt.
    """
    if not isinstance(id_prefix, str) or not id_prefix.strip():
        raise ValueError("columnar_number_slots requires a non-empty id_prefix")
    text = str(value)
    if not text or any(not character.isdigit() for character in text):
        raise ValueError("columnar_number_slots value must contain digits only")
    if float(column_width) <= 0:
        raise ValueError("columnar_number_slots column_width must be positive")

    last_index = len(text) - 1
    return tuple(
        TextSlot(
            id=f"{id_prefix}.place.{last_index - index}",
            prompt=prompt,
            text=digit,
            style_role=style_role,
            x=float(right_x) - (last_index - index) * float(column_width),
            y=float(y),
            anchor="middle",
            font_size=font_size,
            fill=fill,
            semantic_role=semantic_role,
        )
        for index, digit in enumerate(text)
    )
