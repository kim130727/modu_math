from __future__ import annotations

from collections.abc import Sequence

from .models import LineSlot, RectSlot, TextSlot

TableSlot = RectSlot | LineSlot | TextSlot


def table_slots(
    prefix: str,
    *,
    x: float,
    y: float,
    col_widths: Sequence[float],
    row_heights: Sequence[float],
    cells: Sequence[Sequence[str]],
    font_size: int = 28,
    padding_x: float = 12,
    col_text_offsets: Sequence[float] | None = None,
    align: str = "left",
    text_dy: float | None = None,
    stroke: str = "#111111",
    stroke_width: float = 1.5,
    fill: str = "none",
    style_role: str = "table",
) -> tuple[TableSlot, ...]:
    """Build a simple editable table from ordinary DSL slots.

    The generated ids follow the editor-friendly convention:
    ``{prefix}.outer``, ``{prefix}.v1``, ``{prefix}.h1``,
    and ``{prefix}.r{row}c{col}``.
    """
    if not col_widths or not row_heights:
        raise ValueError("table_slots requires at least one column and one row")

    width = float(sum(col_widths))
    height = float(sum(row_heights))
    slots: list[TableSlot] = [
        RectSlot(
            id=f"{prefix}.outer",
            prompt="",
            x=x,
            y=y,
            width=width,
            height=height,
            stroke=stroke,
            stroke_width=stroke_width,
            fill=fill,
        )
    ]

    cursor = x
    for index, col_width in enumerate(col_widths[:-1], start=1):
        cursor += float(col_width)
        slots.append(
            LineSlot(
                id=f"{prefix}.v{index}",
                prompt="",
                x1=cursor,
                y1=y,
                x2=cursor,
                y2=y + height,
                stroke=stroke,
                stroke_width=stroke_width,
            )
        )

    cursor = y
    for index, row_height in enumerate(row_heights[:-1], start=1):
        cursor += float(row_height)
        slots.append(
            LineSlot(
                id=f"{prefix}.h{index}",
                prompt="",
                x1=x,
                y1=cursor,
                x2=x + width,
                y2=cursor,
                stroke=stroke,
                stroke_width=stroke_width,
            )
        )

    baseline_dy = text_dy if text_dy is not None else font_size + 2
    row_y = y
    align = align if align in {"left", "center", "right"} else "left"
    for r, row_height in enumerate(row_heights, start=1):
        col_x = x
        row = cells[r - 1] if r - 1 < len(cells) else ()
        for c, col_width in enumerate(col_widths, start=1):
            text = row[c - 1] if c - 1 < len(row) else ""
            if align == "center":
                text_x = col_x + float(col_width) / 2
                anchor = "middle"
            elif align == "right":
                text_x = col_x + float(col_width) - padding_x
                anchor = "end"
            else:
                text_x = col_x + (
                    float(col_text_offsets[c - 1])
                    if col_text_offsets is not None and c - 1 < len(col_text_offsets)
                    else padding_x
                )
                anchor = "start"
            max_width = max(8.0, float(col_width) - padding_x * 2)
            slots.append(
                TextSlot(
                    id=f"{prefix}.r{r}c{c}",
                    prompt="",
                    text=str(text),
                    style_role=style_role,
                    x=text_x,
                    y=row_y + min(float(row_height), baseline_dy),
                    font_size=font_size,
                    max_width=max_width,
                    anchor=anchor,
                )
            )
            col_x += float(col_width)
        row_y += float(row_height)

    return tuple(slots)
