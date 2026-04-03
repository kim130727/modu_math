from __future__ import annotations

from manim import Circle, DashedLine, Line, Polygon, Rectangle, Scene, Text, config


class ManimRenderer:
    def __init__(self, default_text_scale: float = 0.78) -> None:
        # Manim text tends to look larger than SVG text at the same numeric size.
        # Apply a conservative default scale so cross-render output is visually closer.
        self.default_text_scale = default_text_scale

    def render_scene(self, scene: Scene, semantic: dict) -> None:
        render = semantic["render"]
        canvas = render["canvas"]
        scene.camera.background_color = canvas["background"]

        for elem in render["elements"]:
            mob = self._to_mobject(elem, canvas)
            if mob is not None:
                scene.add(mob)

    def _to_mobject(self, elem: dict, canvas: dict):
        t = elem["type"]
        if t == "text":
            return self._text(elem, canvas)
        if t == "rect":
            return self._rect(elem, canvas)
        if t == "line":
            return self._line(elem, canvas)
        if t == "circle":
            return self._circle(elem, canvas)
        if t == "polygon":
            return self._polygon(elem, canvas)
        if t in {"path", "arc", "group", "transform", "image"}:
            raise NotImplementedError(f"manim primitive not yet implemented: {t}")
        raise ValueError(f"unsupported primitive: {t}")

    @staticmethod
    def _px_x(px: float, w: float) -> float:
        return (px / w - 0.5) * config.frame_width

    @staticmethod
    def _px_y(py: float, h: float) -> float:
        return (0.5 - py / h) * config.frame_height

    @staticmethod
    def _px_w(px: float, w: float) -> float:
        return px / w * config.frame_width

    @staticmethod
    def _px_h(px: float, h: float) -> float:
        return px / h * config.frame_height

    def _text(self, e: dict, c: dict) -> Text:
        if "manim_font_size" in e:
            resolved_font_size = float(e["manim_font_size"])
        else:
            resolved_font_size = float(e.get("font_size", 24)) * float(
                e.get("manim_font_scale", self.default_text_scale)
            )

        m = Text(
            e["text"],
            font=e.get("font_family", "Malgun Gothic"),
            font_size=resolved_font_size,
            color=e.get("fill", "#000000"),
        )
        x = self._px_x(float(e["x"]), float(c["width"]))
        y = self._px_y(float(e["y"]), float(c["height"]))
        m.move_to([x, y, 0])
        anchor = str(e.get("anchor", "middle")).lower()
        if anchor == "start":
            m.set_x(x + m.width / 2)
        elif anchor == "end":
            m.set_x(x - m.width / 2)
        return m

    def _rect(self, e: dict, c: dict) -> Rectangle:
        w = self._px_w(float(e["width"]), float(c["width"]))
        h = self._px_h(float(e["height"]), float(c["height"]))
        x = self._px_x(float(e["x"]), float(c["width"])) + w / 2
        y = self._px_y(float(e["y"]), float(c["height"])) - h / 2
        fill = e.get("fill", "none")
        m = Rectangle(
            width=w,
            height=h,
            stroke_color=e.get("stroke", "#000000"),
            stroke_width=e.get("stroke_width", 1),
            fill_color=fill if fill != "none" else e.get("stroke", "#000000"),
            fill_opacity=0.0 if fill == "none" else 1.0,
        )
        m.move_to([x, y, 0])
        return m

    def _line(self, e: dict, c: dict):
        x1 = self._px_x(float(e["x1"]), float(c["width"]))
        y1 = self._px_y(float(e["y1"]), float(c["height"]))
        x2 = self._px_x(float(e["x2"]), float(c["width"]))
        y2 = self._px_y(float(e["y2"]), float(c["height"]))
        if "dasharray" in e:
            return DashedLine(
                [x1, y1, 0],
                [x2, y2, 0],
                color=e.get("stroke", "#000000"),
                stroke_width=e.get("stroke_width", 1),
                dash_length=max(0.03, self._px_w(float(str(e["dasharray"]).split()[0]), float(c["width"]))),
            )
        return Line([x1, y1, 0], [x2, y2, 0], color=e.get("stroke", "#000000"), stroke_width=e.get("stroke_width", 1))

    def _circle(self, e: dict, c: dict) -> Circle:
        cx = self._px_x(float(e["cx"]), float(c["width"]))
        cy = self._px_y(float(e["cy"]), float(c["height"]))
        r = self._px_w(float(e["r"]), float(c["width"]))
        fill = e.get("fill", "none")
        m = Circle(
            radius=r,
            stroke_color=e.get("stroke", "#000000"),
            stroke_width=e.get("stroke_width", 1),
            fill_color=fill if fill != "none" else e.get("stroke", "#000000"),
            fill_opacity=0.0 if fill == "none" else 1.0,
        )
        m.move_to([cx, cy, 0])
        return m

    def _polygon(self, e: dict, c: dict) -> Polygon:
        pts = []
        for p in e["points"]:
            pts.append([
                self._px_x(float(p[0]), float(c["width"])),
                self._px_y(float(p[1]), float(c["height"])),
                0,
            ])
        fill = e.get("fill", "none")
        return Polygon(
            *pts,
            stroke_color=e.get("stroke", "#000000"),
            stroke_width=e.get("stroke_width", 1),
            fill_color=fill if fill != "none" else e.get("stroke", "#000000"),
            fill_opacity=0.0 if fill == "none" else 1.0,
        )
