from __future__ import annotations

import math
from collections.abc import Sequence
from typing import Literal

from .models import CircleSlot, LineSlot, PathSlot, PolygonSlot

CircleFoldStage = Literal["circle", "half", "opened_horizontal", "folded_diagonal", "opened_cross"]
PaperFoldingSlot = CircleSlot | LineSlot | PathSlot | PolygonSlot


def _fmt(value: float) -> str:
    return f"{value:.3f}".rstrip("0").rstrip(".")


def _arrow_slots(prefix: str, *, x1: float, y1: float, x2: float, y2: float, stroke: str) -> tuple[PaperFoldingSlot, ...]:
    angle = math.atan2(y2 - y1, x2 - x1)
    head = 12.0
    spread = math.radians(28)
    p1 = (x2, y2)
    p2 = (x2 - head * math.cos(angle - spread), y2 - head * math.sin(angle - spread))
    p3 = (x2 - head * math.cos(angle + spread), y2 - head * math.sin(angle + spread))
    return (
        LineSlot(id=f"{prefix}.body", prompt="", x1=x1, y1=y1, x2=x2, y2=y2, stroke=stroke, stroke_width=8.0),
        PolygonSlot(id=f"{prefix}.head", prompt="", points=(p1, p2, p3), stroke=stroke, stroke_width=0.0, fill=stroke),
    )


def circle_paper_slot(
    prefix: str,
    *,
    cx: float,
    cy: float,
    r: float,
    fill: str = "#DFF2F0",
    stroke: str = "#00AFA8",
    stroke_width: float = 1.5,
) -> CircleSlot:
    return CircleSlot(id=f"{prefix}.paper", prompt="", cx=cx, cy=cy, r=r, fill=fill, stroke=stroke, stroke_width=stroke_width)


def folded_half_circle_slots(
    prefix: str,
    *,
    cx: float,
    cy: float,
    r: float,
    fill: str = "#DFF2F0",
    stroke: str = "#00AFA8",
    stroke_width: float = 1.5,
) -> tuple[PaperFoldingSlot, ...]:
    d = (
        f"M {_fmt(cx - r)} {_fmt(cy)} "
        f"C {_fmt(cx - r * 0.96)} {_fmt(cy + r * 0.62)}, {_fmt(cx - r * 0.48)} {_fmt(cy + r * 0.92)}, {_fmt(cx)} {_fmt(cy + r * 0.92)} "
        f"C {_fmt(cx + r * 0.48)} {_fmt(cy + r * 0.92)}, {_fmt(cx + r * 0.96)} {_fmt(cy + r * 0.62)}, {_fmt(cx + r)} {_fmt(cy)} "
        f"L {_fmt(cx - r)} {_fmt(cy)} Z"
    )
    crease_d = f"M {_fmt(cx - r * 0.82)} {_fmt(cy + r * 0.1)} C {_fmt(cx - r * 0.3)} {_fmt(cy + r * 1.12)}, {_fmt(cx + r * 0.45)} {_fmt(cy + r * 1.04)}, {_fmt(cx + r * 0.85)} {_fmt(cy + r * 0.08)}"
    return (
        PathSlot(id=f"{prefix}.paper", prompt="", d=d, fill=fill, stroke=stroke, stroke_width=stroke_width),
        PathSlot(id=f"{prefix}.edge", prompt="", d=crease_d, fill="none", stroke=stroke, stroke_width=1.2),
    )


def opened_circle_with_fold_slots(
    prefix: str,
    *,
    cx: float,
    cy: float,
    r: float,
    angle: float = 0.0,
    fill: str = "#DFF2F0",
    stroke: str = "#00AFA8",
    stroke_width: float = 1.5,
    dash: str = "5 4",
) -> tuple[PaperFoldingSlot, ...]:
    rad = math.radians(angle)
    dx = r * math.cos(rad)
    dy = r * math.sin(rad)
    return (
        circle_paper_slot(prefix, cx=cx, cy=cy, r=r, fill=fill, stroke=stroke, stroke_width=stroke_width),
        LineSlot(
            id=f"{prefix}.fold_line",
            prompt="",
            x1=cx - dx,
            y1=cy - dy,
            x2=cx + dx,
            y2=cy + dy,
            stroke=stroke,
            stroke_width=1.2,
            stroke_dasharray=dash,
        ),
    )


def folded_circle_sector_slots(
    prefix: str,
    *,
    cx: float,
    cy: float,
    r: float,
    angle: float = -58.0,
    fill: str = "#DFF2F0",
    stroke: str = "#00AFA8",
    stroke_width: float = 1.5,
) -> tuple[PaperFoldingSlot, ...]:
    rad = math.radians(angle)
    tip = (cx + r * 0.22 * math.cos(rad), cy + r * 0.22 * math.sin(rad))
    left = (cx - r * 0.38, cy - r * 0.78)
    right = (cx + r * 0.92, cy + r * 0.66)
    d = (
        f"M {_fmt(left[0])} {_fmt(left[1])} "
        f"C {_fmt(cx - r * 0.88)} {_fmt(cy - r * 0.28)}, {_fmt(cx - r * 0.72)} {_fmt(cy + r * 0.76)}, {_fmt(cx + r * 0.18)} {_fmt(cy + r * 0.93)} "
        f"C {_fmt(cx + r * 0.46)} {_fmt(cy + r)}, {_fmt(cx + r * 0.72)} {_fmt(cy + r * 0.86)}, {_fmt(right[0])} {_fmt(right[1])} "
        f"L {_fmt(left[0])} {_fmt(left[1])} Z"
    )
    crease_d = f"M {_fmt(cx - r * 0.85)} {_fmt(cy + r * 0.62)} C {_fmt(cx - r * 0.3)} {_fmt(cy + r * 1.05)}, {_fmt(cx + r * 0.42)} {_fmt(cy + r * 0.98)}, {_fmt(right[0])} {_fmt(right[1])}"
    return (
        PathSlot(id=f"{prefix}.paper", prompt="", d=d, fill=fill, stroke=stroke, stroke_width=stroke_width),
        LineSlot(id=f"{prefix}.crease", prompt="", x1=left[0], y1=left[1], x2=right[0], y2=right[1], stroke=stroke, stroke_width=1.5),
        PathSlot(id=f"{prefix}.edge", prompt="", d=crease_d, fill="none", stroke=stroke, stroke_width=1.2),
        CircleSlot(id=f"{prefix}.guide", prompt="", cx=tip[0], cy=tip[1], r=0.01, fill="none", stroke="none"),
    )


def circle_fold_sequence_slots(
    prefix: str,
    *,
    x: float,
    y: float,
    r: float,
    gap: float,
    stages: Sequence[CircleFoldStage] = ("circle", "half", "opened_horizontal", "folded_diagonal", "opened_cross"),
    show_arrows: bool = True,
    fill: str = "#DFF2F0",
    stroke: str = "#00AFA8",
    stroke_width: float = 1.5,
    arrow_stroke: str = "#9A9A9A",
) -> tuple[PaperFoldingSlot, ...]:
    """Build an editable circle-paper folding sequence from ordinary slots."""
    slots: list[PaperFoldingSlot] = []
    for index, stage in enumerate(stages, start=1):
        cx = x + (index - 1) * gap
        cy = y
        stage_prefix = f"{prefix}.stage{index}"
        if show_arrows and index > 1:
            slots.extend(_arrow_slots(f"{prefix}.arrow{index - 1}", x1=cx - gap + r + 28.0, y1=cy, x2=cx - r - 28.0, y2=cy, stroke=arrow_stroke))
        if stage == "circle":
            slots.append(circle_paper_slot(stage_prefix, cx=cx, cy=cy, r=r, fill=fill, stroke=stroke, stroke_width=stroke_width))
        elif stage == "half":
            slots.extend(folded_half_circle_slots(stage_prefix, cx=cx, cy=cy, r=r, fill=fill, stroke=stroke, stroke_width=stroke_width))
        elif stage == "opened_horizontal":
            slots.extend(opened_circle_with_fold_slots(stage_prefix, cx=cx, cy=cy, r=r, angle=0.0, fill=fill, stroke=stroke, stroke_width=stroke_width))
        elif stage == "folded_diagonal":
            slots.extend(folded_circle_sector_slots(stage_prefix, cx=cx, cy=cy, r=r, fill=fill, stroke=stroke, stroke_width=stroke_width))
        elif stage == "opened_cross":
            slots.extend(opened_circle_with_fold_slots(stage_prefix, cx=cx, cy=cy, r=r, angle=0.0, fill=fill, stroke=stroke, stroke_width=stroke_width))
            slots.append(
                LineSlot(
                    id=f"{stage_prefix}.fold_line2",
                    prompt="",
                    x1=cx - r * 0.48,
                    y1=cy - r * 0.88,
                    x2=cx + r * 0.48,
                    y2=cy + r * 0.88,
                    stroke=stroke,
                    stroke_width=1.2,
                    stroke_dasharray="5 4",
                )
            )
            slots.append(CircleSlot(id=f"{stage_prefix}.center", prompt="", cx=cx, cy=cy, r=max(3.0, r * 0.06), fill="#E11A86", stroke="none"))
        else:
            raise ValueError(f"unsupported circle fold stage: {stage}")
    return tuple(slots)
