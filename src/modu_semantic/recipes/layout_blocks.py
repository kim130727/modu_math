from __future__ import annotations

from ..primitives import Line, Rect, Text


def problem_box(id: str, x: float, y: float, width: float, height: float) -> Rect:
    return Rect(
        id=id,
        x=x,
        y=y,
        width=width,
        height=height,
        stroke="#222222",
        fill="#FFFFFF",
        semantic_role="problem_box",
    )


def choice_row(
    id_prefix: str,
    x: float,
    y: float,
    choices: list[str],
    *,
    gap: float = 80,
    font_size: int = 18,
) -> list[Text]:
    items: list[Text] = []
    for index, label in enumerate(choices):
        items.append(
            Text(
                id=f"{id_prefix}_{index + 1}",
                x=x + (gap * index),
                y=y,
                text=label,
                font_size=font_size,
                semantic_role="choice",
            )
        )
    return items


def figure_area(
    id: str,
    x: float,
    y: float,
    width: float,
    height: float,
    *,
    label: str | None = None,
) -> list[object]:
    elements: list[object] = [
        Rect(
            id=id,
            x=x,
            y=y,
            width=width,
            height=height,
            stroke="#666666",
            fill="none",
            semantic_role="figure_area",
        )
    ]
    if label:
        elements.append(
            Text(
                id=f"{id}_label",
                x=x + 8,
                y=y + 20,
                text=label,
                font_size=14,
                semantic_role="figure_area_label",
            )
        )
    return elements


def blank_answer(id: str, x: float, y: float, *, width: float = 56, height: float = 26) -> Rect:
    return Rect(
        id=id,
        x=x,
        y=y,
        width=width,
        height=height,
        stroke="#000000",
        fill="#FFFFFF",
        semantic_role="blank_answer",
    )


def fraction_strip(
    id_prefix: str,
    x: float,
    y: float,
    *,
    segments: int,
    total_width: float,
    height: float = 28,
) -> list[Rect]:
    if segments <= 0:
        raise ValueError("segments must be positive")
    segment_width = total_width / segments
    return [
        Rect(
            id=f"{id_prefix}_{index + 1}",
            x=x + (segment_width * index),
            y=y,
            width=segment_width,
            height=height,
            stroke="#444444",
            fill="#FFFFFF",
            semantic_role="fraction_segment",
        )
        for index in range(segments)
    ]


def grid_diagram(
    id_prefix: str,
    x: float,
    y: float,
    *,
    rows: int,
    cols: int,
    cell_size: float,
) -> list[Line]:
    if rows <= 0 or cols <= 0:
        raise ValueError("rows and cols must be positive")

    lines: list[Line] = []
    width = cols * cell_size
    height = rows * cell_size

    for row in range(rows + 1):
        y_pos = y + (row * cell_size)
        lines.append(
            Line(
                id=f"{id_prefix}_h_{row}",
                x1=x,
                y1=y_pos,
                x2=x + width,
                y2=y_pos,
                stroke="#444444",
                semantic_role="grid_line",
            )
        )

    for col in range(cols + 1):
        x_pos = x + (col * cell_size)
        lines.append(
            Line(
                id=f"{id_prefix}_v_{col}",
                x1=x_pos,
                y1=y,
                x2=x_pos,
                y2=y + height,
                stroke="#444444",
                semantic_role="grid_line",
            )
        )

    return lines


ProblemBox = problem_box
ChoiceRow = choice_row
FigureArea = figure_area
BlankAnswer = blank_answer
FractionStrip = fraction_strip
GridDiagram = grid_diagram

__all__ = [
    "problem_box",
    "choice_row",
    "figure_area",
    "blank_answer",
    "fraction_strip",
    "grid_diagram",
    "ProblemBox",
    "ChoiceRow",
    "FigureArea",
    "BlankAnswer",
    "FractionStrip",
    "GridDiagram",
]
