from __future__ import annotations

from .models.base import LineSlot, TextSlot


def fraction_slots(
    *,
    id_prefix: str,
    numerator: str,
    denominator: str,
    x: float,
    numerator_y: float,
    denominator_y: float,
    bar_y: float | None = None,
    bar_width: float = 40.0,
    prompt: str = "",
    style_role: str = "body",
    anchor: str = "middle",
    font_size: int | None = 30,
    fill: str = "#222222",
    stroke: str = "#222222",
    stroke_width: float = 2.2,
    semantic_role: str | None = None,
) -> tuple[TextSlot, LineSlot, TextSlot]:
    """
    Build reusable slots for a textual fraction (numerator/bar/denominator).

    This helper keeps the authored DSL compact while preserving canonical
    layout/editor compatibility because it expands to ordinary TextSlot/LineSlot.
    """
    center_bar_y = (numerator_y + denominator_y) * 0.5 if bar_y is None else bar_y
    half_width = max(1.0, float(bar_width) * 0.5)

    return (
        TextSlot(
            id=f"{id_prefix}.num",
            prompt=prompt,
            text=numerator,
            style_role=style_role,
            x=float(x),
            y=float(numerator_y),
            anchor=anchor,
            font_size=font_size,
            fill=fill,
            semantic_role=semantic_role,
        ),
        LineSlot(
            id=f"{id_prefix}.bar",
            prompt=prompt,
            x1=float(x) - half_width,
            y1=float(center_bar_y),
            x2=float(x) + half_width,
            y2=float(center_bar_y),
            stroke=stroke,
            stroke_width=float(stroke_width),
            semantic_role=semantic_role,
        ),
        TextSlot(
            id=f"{id_prefix}.den",
            prompt=prompt,
            text=denominator,
            style_role=style_role,
            x=float(x),
            y=float(denominator_y),
            anchor=anchor,
            font_size=font_size,
            fill=fill,
            semantic_role=semantic_role,
        ),
    )
