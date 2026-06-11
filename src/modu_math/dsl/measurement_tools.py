from __future__ import annotations

from .models import CircleSlot, LineSlot, PathSlot, PolygonSlot, RectSlot, TextSlot

MeasurementToolSlot = CircleSlot | LineSlot | PathSlot | PolygonSlot | RectSlot | TextSlot


def ruler_slots(
    prefix: str,
    *,
    x: float,
    y: float,
    unit_width: float = 30.0,
    units: int = 3,
    height: float = 32.0,
    fill: str = "#DDF6FF",
    stroke: str = "#19B5F2",
) -> tuple[MeasurementToolSlot, ...]:
    width = unit_width * units
    slots: list[MeasurementToolSlot] = [
        RectSlot(id=f"{prefix}.body", prompt="", x=x, y=y, width=width, height=height, fill=fill, stroke=stroke, stroke_width=1.2),
        LineSlot(id=f"{prefix}.top", prompt="", x1=x, y1=y + 8, x2=x + width, y2=y + 8, stroke=stroke, stroke_width=1.1),
    ]

    for i in range(units * 10 + 1):
        tx = x + i * unit_width / 10.0
        if i % 10 == 0:
            tick_h = 12
            stroke_w = 1.0
        elif i % 5 == 0:
            tick_h = 9
            stroke_w = 0.85
        else:
            tick_h = 6
            stroke_w = 0.7
        slots.append(
            LineSlot(
                id=f"{prefix}.tick.{i:02d}",
                prompt="",
                x1=tx,
                y1=y + 8,
                x2=tx,
                y2=y + 8 + tick_h,
                stroke=stroke,
                stroke_width=stroke_w,
            )
        )

    for i in range(units + 1):
        slots.append(
            TextSlot(
                id=f"{prefix}.label.{i}",
                prompt="",
                text=str(i),
                style_role="label",
                x=x + i * unit_width,
                y=y + height - 8,
                font_size=15,
                anchor="middle",
                fill="#333333",
            )
        )
    return tuple(slots)


def compass_slots(
    prefix: str,
    *,
    hinge_x: float,
    hinge_y: float,
    needle_x: float,
    needle_y: float,
    pencil_x: float,
    pencil_y: float,
    scale: float = 1.0,
) -> tuple[MeasurementToolSlot, ...]:
    metal = "#6D7378"
    dark = "#42474B"
    body = "#C7DCE3"
    pencil = "#A9B84B"
    wood = "#E8B55D"

    def lerp(a: float, b: float, t: float) -> float:
        return a + (b - a) * t

    left_mid = (lerp(hinge_x, needle_x, 0.64), lerp(hinge_y, needle_y, 0.64))
    right_mid = (lerp(hinge_x, pencil_x, 0.67), lerp(hinge_y, pencil_y, 0.67))
    pencil_top_y = pencil_y - 78 * scale
    holder_y = pencil_y - 28 * scale

    return (
        LineSlot(id=f"{prefix}.leg.left.outer", prompt="", x1=hinge_x - 4 * scale, y1=hinge_y + 8 * scale, x2=needle_x, y2=needle_y, stroke=dark, stroke_width=1.2),
        LineSlot(id=f"{prefix}.leg.left.inner", prompt="", x1=hinge_x + 1 * scale, y1=hinge_y + 8 * scale, x2=needle_x + 5 * scale, y2=needle_y, stroke=body, stroke_width=3.0),
        LineSlot(id=f"{prefix}.leg.right.outer", prompt="", x1=hinge_x + 4 * scale, y1=hinge_y + 8 * scale, x2=pencil_x, y2=pencil_y - 5 * scale, stroke=dark, stroke_width=1.2),
        LineSlot(id=f"{prefix}.leg.right.inner", prompt="", x1=hinge_x - 1 * scale, y1=hinge_y + 8 * scale, x2=pencil_x - 6 * scale, y2=pencil_y - 18 * scale, stroke=body, stroke_width=3.0),
        CircleSlot(id=f"{prefix}.hinge", prompt="", cx=hinge_x, cy=hinge_y, r=6 * scale, fill="#AEB4B7", stroke=dark, stroke_width=1.0),
        RectSlot(id=f"{prefix}.head", prompt="", x=hinge_x - 5 * scale, y=hinge_y - 17 * scale, width=10 * scale, height=18 * scale, fill="#8B9195", stroke=dark, stroke_width=1.0, rx=2 * scale, ry=2 * scale),
        RectSlot(id=f"{prefix}.knob", prompt="", x=hinge_x - 2 * scale, y=hinge_y - 30 * scale, width=4 * scale, height=12 * scale, fill="#7F8589", stroke=dark, stroke_width=0.8),
        LineSlot(id=f"{prefix}.bar.left", prompt="", x1=left_mid[0], y1=left_mid[1], x2=right_mid[0], y2=right_mid[1], stroke=metal, stroke_width=1.2),
        RectSlot(id=f"{prefix}.clamp", prompt="", x=pencil_x - 7 * scale, y=holder_y - 4 * scale, width=14 * scale, height=8 * scale, fill=metal, stroke=dark, stroke_width=0.8),
        RectSlot(id=f"{prefix}.pencil.body", prompt="", x=pencil_x - 3 * scale, y=pencil_top_y, width=6 * scale, height=75 * scale, fill=pencil, stroke="#879036", stroke_width=0.9),
        PolygonSlot(
            id=f"{prefix}.pencil.tip",
            prompt="",
            points=((pencil_x - 5 * scale, pencil_y - 4 * scale), (pencil_x + 5 * scale, pencil_y - 4 * scale), (pencil_x, pencil_y + 9 * scale)),
            fill=wood,
            stroke="#9E7130",
            stroke_width=0.8,
        ),
        LineSlot(id=f"{prefix}.needle.tip", prompt="", x1=needle_x, y1=needle_y - 8 * scale, x2=needle_x, y2=needle_y + 8 * scale, stroke=dark, stroke_width=1.2),
    )


def compass_on_ruler_slots(
    prefix: str,
    *,
    x: float,
    y: float,
    unit_width: float = 30.0,
    needle_mark: float = 0.0,
    pencil_mark: float = 3.0,
    hinge_offset_x: float = 35.0,
    hinge_y_offset: float = -96.0,
    scale: float = 1.0,
) -> tuple[MeasurementToolSlot, ...]:
    ruler = ruler_slots(f"{prefix}.ruler", x=x, y=y, unit_width=unit_width, units=3)
    needle_x = x + needle_mark * unit_width
    pencil_x = x + pencil_mark * unit_width
    foot_y = y - 8 * scale
    compass = compass_slots(
        f"{prefix}.compass",
        hinge_x=needle_x + hinge_offset_x,
        hinge_y=y + hinge_y_offset,
        needle_x=needle_x,
        needle_y=foot_y,
        pencil_x=pencil_x,
        pencil_y=foot_y,
        scale=scale,
    )
    return (*ruler, *compass)
