from __future__ import annotations

from typing import Sequence

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


def data_table(
    id_prefix: str,
    x: float,
    y: float,
    *,
    row_labels: Sequence[str],
    column_labels: Sequence[str],
    values: Sequence[Sequence[str]],
    first_col_width: float,
    data_col_widths: Sequence[float],
    row_height: float,
    show_first_col: bool = True,
    corner_header: str | None = None,
    line_color: str = "#777777",
    line_thickness: float = 1.0,
    font_size: float = 17.0,
    font_family: str = "Malgun Gothic",
    text_fill: str = "#222222",
) -> list[object]:
    if len(column_labels) != len(data_col_widths):
        raise ValueError("column_labels and data_col_widths length must match")
    if len(row_labels) != len(values):
        raise ValueError("row_labels and values row count must match")
    for row in values:
        if len(row) != len(column_labels):
            raise ValueError("each values row length must match column_labels length")

    items: list[object] = []
    col_widths = ([first_col_width] if show_first_col else []) + list(data_col_widths)
    data_col_start = 1 if show_first_col else 0
    total_w = sum(col_widths)
    row_count = 1 + len(row_labels)

    x_edges = [x]
    for w in col_widths:
        x_edges.append(x_edges[-1] + w)
    y_edges = [y + (row_height * i) for i in range(row_count + 1)]

    for row_idx, yy in enumerate(y_edges):
        items.append(
            Rect(
                id=f"{id_prefix}_hline_{row_idx}",
                x=x,
                y=yy,
                width=total_w,
                height=line_thickness,
                fill=line_color,
                stroke="none",
                stroke_width=0,
                semantic_role="table_grid_line",
            )
        )

    for col_idx, xx in enumerate(x_edges):
        items.append(
            Rect(
                id=f"{id_prefix}_vline_{col_idx}",
                x=xx,
                y=y,
                width=line_thickness,
                height=row_height * row_count,
                fill=line_color,
                stroke="none",
                stroke_width=0,
                semantic_role="table_grid_line",
            )
        )

    for col_idx, header in enumerate(column_labels):
        col_pos = col_idx + data_col_start
        cx = x_edges[col_pos] + (col_widths[col_pos] / 2.0)
        items.append(
            Text(
                id=f"{id_prefix}_col_{col_idx + 1}",
                x=cx,
                y=y + (row_height * 0.7),
                text=header,
                font_size=font_size,
                font_family=font_family,
                fill=text_fill,
                anchor="middle",
                semantic_role="table_header",
            )
        )

    if show_first_col and corner_header is not None:
        items.append(
            Text(
                id=f"{id_prefix}_corner_header",
                x=x + (first_col_width / 2.0),
                y=y + (row_height * 0.7),
                text=corner_header,
                font_size=font_size,
                font_family=font_family,
                fill=text_fill,
                anchor="middle",
                semantic_role="table_header",
            )
        )

    for row_idx, row_label in enumerate(row_labels):
        cy = y + (row_height * (row_idx + 1.7))
        if show_first_col:
            items.append(
                Text(
                    id=f"{id_prefix}_row_{row_idx + 1}",
                    x=x + (first_col_width / 2.0),
                    y=cy,
                    text=row_label,
                    font_size=font_size,
                    font_family=font_family,
                    fill=text_fill,
                    anchor="middle",
                    semantic_role="table_row_label",
                )
            )
        for col_idx, value in enumerate(values[row_idx]):
            col_pos = col_idx + data_col_start
            cx = x_edges[col_pos] + (col_widths[col_pos] / 2.0)
            items.append(
                Text(
                    id=f"{id_prefix}_cell_r{row_idx + 1}_c{col_idx + 1}",
                    x=cx,
                    y=cy,
                    text=value,
                    font_size=font_size,
                    font_family=font_family,
                    fill=text_fill,
                    anchor="middle",
                    semantic_role="table_cell",
                )
            )

    return items


def dataframe_table(
    id_prefix: str,
    x: float,
    y: float,
    *,
    index: Sequence[str],
    columns: Sequence[str],
    data: Sequence[Sequence[object]],
    row_height: float,
    column_widths: Sequence[float] | None = None,
    index_col_width: float | None = None,
    show_index: bool = True,
    corner_header: str | None = None,
    line_color: str = "#777777",
    line_thickness: float = 1.0,
    font_size: float = 17.0,
    font_family: str = "Malgun Gothic",
    text_fill: str = "#222222",
) -> list[object]:
    if len(index) != len(data):
        raise ValueError("index and data row count must match")
    if any(len(row) != len(columns) for row in data):
        raise ValueError("each data row length must match columns length")

    resolved_col_widths = list(column_widths) if column_widths is not None else [96.0] * len(columns)
    if len(resolved_col_widths) != len(columns):
        raise ValueError("column_widths length must match columns length")

    resolved_index_width = float(index_col_width) if index_col_width is not None else 100.0
    value_rows = [[str(cell) for cell in row] for row in data]

    return data_table(
        id_prefix,
        x,
        y,
        row_labels=list(index),
        column_labels=list(columns),
        values=value_rows,
        first_col_width=resolved_index_width,
        data_col_widths=resolved_col_widths,
        row_height=row_height,
        show_first_col=show_index,
        corner_header=corner_header,
        line_color=line_color,
        line_thickness=line_thickness,
        font_size=font_size,
        font_family=font_family,
        text_fill=text_fill,
    )


ProblemBox = problem_box
ChoiceRow = choice_row
FigureArea = figure_area
BlankAnswer = blank_answer
FractionStrip = fraction_strip
GridDiagram = grid_diagram
DataTable = data_table
DataFrameTable = dataframe_table

__all__ = [
    "problem_box",
    "choice_row",
    "figure_area",
    "blank_answer",
    "fraction_strip",
    "grid_diagram",
    "data_table",
    "dataframe_table",
    "ProblemBox",
    "ChoiceRow",
    "FigureArea",
    "BlankAnswer",
    "FractionStrip",
    "GridDiagram",
    "DataTable",
    "DataFrameTable",
]
