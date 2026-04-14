from __future__ import annotations

from typing import Sequence

from ..primitives import Rect, Text
from ..regions import Region


def add_masked_number_pattern(
    root: Region,
    *,
    aid: str,
    pattern: str,
    columns: Sequence[float],
    y: float,
    blank_ids: Sequence[str] | None = None,
    font_size: float = 17,
    font_family: str = "Malgun Gothic",
    fill: str = "#222222",
    box_size: float = 34,
    box_stroke: str = "#666666",
    box_stroke_width: float = 1.5,
    semantic_role: str = "label",
) -> list[str]:
    token = pattern.replace(" ", "")
    if len(token) > len(columns):
        raise ValueError(f"Pattern '{pattern}' is longer than available columns.")

    aligned_columns = list(columns)[len(columns) - len(token) :]
    blanks_created: list[str] = []
    blank_index = 0

    for i, ch in enumerate(token):
        x = aligned_columns[i]
        if ch == "□":
            if blank_ids is not None and blank_index < len(blank_ids):
                blank_id = blank_ids[blank_index]
            else:
                blank_id = f"{aid}_blank_{blank_index + 1}"
            root.add(
                Rect(
                    id=blank_id,
                    x=x - (box_size / 2.0),
                    y=y - box_size + 7,
                    width=box_size,
                    height=box_size,
                    fill="none",
                    stroke=box_stroke,
                    stroke_width=box_stroke_width,
                    semantic_role="answer_anchor",
                )
            )
            blanks_created.append(blank_id)
            blank_index += 1
            continue

        root.add(
            Text(
                id=f"{aid}_digit_{i + 1}",
                x=x,
                y=y,
                text=ch,
                font_size=font_size,
                font_family=font_family,
                fill=fill,
                anchor="middle",
                semantic_role=semantic_role,
            )
        )

    return blanks_created
