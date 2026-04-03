from __future__ import annotations

from manim import BLACK, BOLD, DashedLine, Line, Mobject, NORMAL, Rectangle, RoundedRectangle, Scene, Text, config


def render_manim_from_semantic(scene: Scene, semantic: dict) -> None:
    """
    Render Manim mobjects from semantic payload.

    Shared renderer keeps problem files thin and aligned with semantic-first
    migration strategy.
    """
    canvas = semantic["canvas"]
    scene.camera.background_color = canvas["background"]

    for element in semantic["elements"]:
        manim_obj = _element_to_mobject(element, canvas)
        if manim_obj is not None:
            scene.add(manim_obj)


def _element_to_mobject(element: dict, canvas: dict) -> Mobject | None:
    elem_type = element["type"]

    if elem_type == "text":
        return _build_text_mobject(element, canvas)

    if elem_type == "rect":
        return _build_rect_mobject(element, canvas)

    if elem_type == "line":
        return _build_line_mobject(element, canvas)

    return None


def _px_to_scene_x(x: float, canvas_width: float) -> float:
    return (x / canvas_width - 0.5) * config.frame_width


def _px_to_scene_y(y: float, canvas_height: float) -> float:
    return (0.5 - y / canvas_height) * config.frame_height


def _px_to_scene_w(width: float, canvas_width: float) -> float:
    return width / canvas_width * config.frame_width


def _px_to_scene_h(height: float, canvas_height: float) -> float:
    return height / canvas_height * config.frame_height


def _build_text_mobject(element: dict, canvas: dict) -> Text:
    font_weight = str(element.get("font_weight", "normal")).lower()
    weight = BOLD if font_weight == "bold" else NORMAL

    text = Text(
        element["text"],
        font=element.get("font_family", "Malgun Gothic"),
        font_size=element.get("font_size", 24),
        color=element.get("fill", BLACK),
        weight=weight,
    )

    x = _px_to_scene_x(float(element["x"]), float(canvas["width"]))
    y = _px_to_scene_y(float(element["y"]), float(canvas["height"]))

    anchor = element.get("anchor", "middle")
    text.move_to([x, y, 0])

    if anchor == "start":
        # SVG start anchor means left-aligned baseline x.
        text.set_x(x + text.width / 2)

    return text


def _build_rect_mobject(element: dict, canvas: dict) -> Mobject:
    width = _px_to_scene_w(float(element["width"]), float(canvas["width"]))
    height = _px_to_scene_h(float(element["height"]), float(canvas["height"]))
    x = _px_to_scene_x(float(element["x"]), float(canvas["width"])) + width / 2
    y = _px_to_scene_y(float(element["y"]), float(canvas["height"])) - height / 2

    stroke_color = element.get("stroke", "#000000")
    stroke_width = float(element.get("stroke_width", 1))
    fill = element.get("fill", "none")

    if float(element.get("rx", 0)) > 0:
        corner_radius = _px_to_scene_w(float(element.get("rx", 0)), float(canvas["width"]))
        shape: Mobject = RoundedRectangle(
            corner_radius=corner_radius,
            width=width,
            height=height,
            stroke_color=stroke_color,
            stroke_width=stroke_width,
            fill_color=fill if fill != "none" else stroke_color,
            fill_opacity=1.0 if fill != "none" else 0.0,
        )
    else:
        shape = Rectangle(
            width=width,
            height=height,
            stroke_color=stroke_color,
            stroke_width=stroke_width,
            fill_color=fill if fill != "none" else stroke_color,
            fill_opacity=1.0 if fill != "none" else 0.0,
        )

    shape.move_to([x, y, 0])
    return shape


def _build_line_mobject(element: dict, canvas: dict) -> Mobject:
    start = [
        _px_to_scene_x(float(element["x1"]), float(canvas["width"])),
        _px_to_scene_y(float(element["y1"]), float(canvas["height"])),
        0,
    ]
    end = [
        _px_to_scene_x(float(element["x2"]), float(canvas["width"])),
        _px_to_scene_y(float(element["y2"]), float(canvas["height"])),
        0,
    ]

    color = element.get("stroke", "#000000")
    stroke_width = float(element.get("stroke_width", 1))

    dasharray = element.get("dasharray")
    if dasharray:
        first_dash_px = float(str(dasharray).split()[0])
        dash_length = _px_to_scene_w(first_dash_px, float(canvas["width"]))
        return DashedLine(
            start=start,
            end=end,
            color=color,
            stroke_width=stroke_width,
            dash_length=max(0.03, dash_length),
        )

    return Line(start=start, end=end, color=color, stroke_width=stroke_width)
