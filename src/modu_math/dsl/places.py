from __future__ import annotations

from .models import CircleSlot, LineSlot, PathSlot, PolygonSlot, RectSlot

PlaceSlot = CircleSlot | LineSlot | PathSlot | PolygonSlot | RectSlot


def school_slots(prefix: str, *, x: float, y: float, scale: float = 1.0) -> tuple[PlaceSlot, ...]:
    s = float(scale)
    return (
        RectSlot(id=f"{prefix}.yard", prompt="", x=x + 4 * s, y=y + 54 * s, width=86 * s, height=8 * s, rx=4 * s, ry=4 * s, stroke="none", fill="#b7e2b6"),
        RectSlot(id=f"{prefix}.body", prompt="", x=x + 18 * s, y=y + 24 * s, width=60 * s, height=40 * s, stroke="#7f6b4d", stroke_width=1.4 * s, fill="#ffd98a"),
        PolygonSlot(id=f"{prefix}.roof", prompt="", points=((x + 12 * s, y + 26 * s), (x + 48 * s, y + 8 * s), (x + 84 * s, y + 26 * s)), stroke="#9b5738", stroke_width=1.4 * s, fill="#e96f4a"),
        RectSlot(id=f"{prefix}.tower", prompt="", x=x + 39 * s, y=y + 14 * s, width=18 * s, height=50 * s, stroke="#7f6b4d", stroke_width=1.3 * s, fill="#f3c35b"),
        PolygonSlot(id=f"{prefix}.tower.roof", prompt="", points=((x + 35 * s, y + 14 * s), (x + 48 * s, y + 4 * s), (x + 61 * s, y + 14 * s)), stroke="#9b5738", stroke_width=1.2 * s, fill="#e96f4a"),
        LineSlot(id=f"{prefix}.flag.pole", prompt="", x1=x + 48 * s, y1=y + 4 * s, x2=x + 48 * s, y2=y - 10 * s, stroke="#4b5563", stroke_width=1.2 * s),
        PolygonSlot(id=f"{prefix}.flag", prompt="", points=((x + 48 * s, y - 10 * s), (x + 64 * s, y - 5 * s), (x + 48 * s, y),), stroke="#d14343", stroke_width=1 * s, fill="#ff8a8a"),
        CircleSlot(id=f"{prefix}.clock", prompt="", cx=x + 48 * s, cy=y + 29 * s, r=7 * s, stroke="#5b7187", stroke_width=1.2 * s, fill="#f8fbff"),
        LineSlot(id=f"{prefix}.clock.h1", prompt="", x1=x + 48 * s, y1=y + 29 * s, x2=x + 48 * s, y2=y + 25 * s, stroke="#5b7187", stroke_width=1 * s),
        LineSlot(id=f"{prefix}.clock.h2", prompt="", x1=x + 48 * s, y1=y + 29 * s, x2=x + 52 * s, y2=y + 29 * s, stroke="#5b7187", stroke_width=1 * s),
        RectSlot(id=f"{prefix}.door", prompt="", x=x + 42 * s, y=y + 45 * s, width=12 * s, height=19 * s, stroke="#795548", stroke_width=1.1 * s, fill="#8fd3ff"),
        RectSlot(id=f"{prefix}.window.left.top", prompt="", x=x + 25 * s, y=y + 32 * s, width=9 * s, height=8 * s, stroke="#5082a9", stroke_width=1 * s, fill="#dff6ff"),
        RectSlot(id=f"{prefix}.window.left.bottom", prompt="", x=x + 25 * s, y=y + 46 * s, width=9 * s, height=8 * s, stroke="#5082a9", stroke_width=1 * s, fill="#dff6ff"),
        RectSlot(id=f"{prefix}.window.right.top", prompt="", x=x + 62 * s, y=y + 32 * s, width=9 * s, height=8 * s, stroke="#5082a9", stroke_width=1 * s, fill="#dff6ff"),
        RectSlot(id=f"{prefix}.window.right.bottom", prompt="", x=x + 62 * s, y=y + 46 * s, width=9 * s, height=8 * s, stroke="#5082a9", stroke_width=1 * s, fill="#dff6ff"),
    )


def house_slots(prefix: str, *, x: float, y: float, scale: float = 1.0) -> tuple[PlaceSlot, ...]:
    s = float(scale)
    return (
        RectSlot(id=f"{prefix}.yard", prompt="", x=x + 5 * s, y=y + 48 * s, width=74 * s, height=8 * s, rx=4 * s, ry=4 * s, stroke="none", fill="#b7e2b6"),
        RectSlot(id=f"{prefix}.body", prompt="", x=x + 16 * s, y=y + 23 * s, width=52 * s, height=34 * s, stroke="#8a6240", stroke_width=1.4 * s, fill="#ffe19a"),
        PolygonSlot(id=f"{prefix}.roof", prompt="", points=((x + 9 * s, y + 25 * s), (x + 42 * s, y + 3 * s), (x + 75 * s, y + 25 * s)), stroke="#a64b43", stroke_width=1.4 * s, fill="#ef6b55"),
        RectSlot(id=f"{prefix}.chimney", prompt="", x=x + 58 * s, y=y + 8 * s, width=8 * s, height=16 * s, stroke="#a64b43", stroke_width=1 * s, fill="#ef6b55"),
        RectSlot(id=f"{prefix}.door", prompt="", x=x + 37 * s, y=y + 35 * s, width=12 * s, height=22 * s, stroke="#795548", stroke_width=1 * s, fill="#7cc3ff"),
        RectSlot(id=f"{prefix}.window.left", prompt="", x=x + 23 * s, y=y + 31 * s, width=10 * s, height=10 * s, stroke="#4f91b7", stroke_width=1 * s, fill="#dff6ff"),
        RectSlot(id=f"{prefix}.window.right", prompt="", x=x + 53 * s, y=y + 31 * s, width=10 * s, height=10 * s, stroke="#4f91b7", stroke_width=1 * s, fill="#dff6ff"),
    )


def playground_slots(prefix: str, *, x: float, y: float, scale: float = 1.0) -> tuple[PlaceSlot, ...]:
    s = float(scale)
    return (
        CircleSlot(id=f"{prefix}.ground", prompt="", cx=x + 52 * s, cy=y + 46 * s, r=35 * s, stroke="none", fill="#c9eeb6"),
        RectSlot(id=f"{prefix}.trunk", prompt="", x=x + 13 * s, y=y + 25 * s, width=6 * s, height=28 * s, stroke="none", fill="#a96a3d"),
        CircleSlot(id=f"{prefix}.tree.top", prompt="", cx=x + 16 * s, cy=y + 18 * s, r=13 * s, stroke="none", fill="#7bcf6b"),
        LineSlot(id=f"{prefix}.swing.top", prompt="", x1=x + 42 * s, y1=y + 14 * s, x2=x + 76 * s, y2=y + 14 * s, stroke="#61a66d", stroke_width=2 * s),
        LineSlot(id=f"{prefix}.swing.left", prompt="", x1=x + 42 * s, y1=y + 14 * s, x2=x + 33 * s, y2=y + 56 * s, stroke="#61a66d", stroke_width=2 * s),
        LineSlot(id=f"{prefix}.swing.right", prompt="", x1=x + 76 * s, y1=y + 14 * s, x2=x + 85 * s, y2=y + 56 * s, stroke="#61a66d", stroke_width=2 * s),
        LineSlot(id=f"{prefix}.rope.left", prompt="", x1=x + 54 * s, y1=y + 14 * s, x2=x + 54 * s, y2=y + 38 * s, stroke="#9ca3af", stroke_width=1.2 * s),
        LineSlot(id=f"{prefix}.rope.right", prompt="", x1=x + 64 * s, y1=y + 14 * s, x2=x + 64 * s, y2=y + 38 * s, stroke="#9ca3af", stroke_width=1.2 * s),
        RectSlot(id=f"{prefix}.seat", prompt="", x=x + 50 * s, y=y + 38 * s, width=18 * s, height=4 * s, rx=2 * s, ry=2 * s, stroke="none", fill="#f59e0b"),
        PathSlot(id=f"{prefix}.slide", prompt="", d=f"M {x + 30 * s} {y + 54 * s} C {x + 49 * s} {y + 42 * s}, {x + 61 * s} {y + 34 * s}, {x + 76 * s} {y + 28 * s}", stroke="#f08bb4", stroke_width=4 * s, fill="none"),
        LineSlot(id=f"{prefix}.ladder", prompt="", x1=x + 28 * s, y1=y + 54 * s, x2=x + 38 * s, y2=y + 26 * s, stroke="#60a5fa", stroke_width=2 * s),
    )
