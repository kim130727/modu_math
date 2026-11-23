"""Resolve the visible problem canvas before either client fits it to a screen."""

import math
import re

from fontTools.pens.boundsPen import BoundsPen
from fontTools.svgLib.path import parse_path

from modu_math.layout.text_layout import text_width


CHOICE_ROLES = {"choice", "choices", "option", "options"}
VISUAL_ROLES = {"canvas", "diagram", "diagram_label", "symbol_label", "label"}
PROMPT_ROLES = {"question", "instruction", "answer_prompt"}
PADDING = 20


def _refs(element):
    return {
        ref for ref in (
            element.get("source_ref"), (element.get("refs") or {}).get("layout_slot_id")
        ) if isinstance(ref, str) and ref
    }


def _bounds(element):
    a = element.get("attributes") or {}
    if a.get("transform"):
        return None

    def number(key, default=0):
        return float(a.get(key, default))

    kind = element.get("type")
    x, y = number("x"), number("y")
    if kind in {"rect", "image", "text_box"}:
        return x, y, x + number("width"), y + number("height")
    if kind == "line":
        x1, y1, x2, y2 = (number(key) for key in ("x1", "y1", "x2", "y2"))
        return min(x1, x2), min(y1, y2), max(x1, x2), max(y1, y2)
    if kind == "circle":
        cx, cy, r = number("cx"), number("cy"), number("r")
        return cx - r, cy - r, cx + r, cy + r
    if kind == "path":
        pen = BoundsPen(None)
        parse_path(a.get("d") or "", pen)
        return pen.bounds
    if kind == "polygon":
        points = a.get("points") or []
        if isinstance(points, str):
            values = [float(value) for value in re.split(r"[\s,]+", points.strip())]
            points = list(zip(values[::2], values[1::2]))
        xs, ys = zip(*points)
        return min(xs), min(ys), max(xs), max(ys)
    if kind == "text":
        size = number("font-size", 18)
        lines = str(element.get("text") or "").split("\n")
        width = max(text_width(line, size) for line in lines)
        anchor = a.get("text-anchor")
        left = x - (width / 2 if anchor == "middle" else width if anchor == "end" else 0)
        return left, y - size, left + width, y + size * (0.35 + 1.35 * (len(lines) - 1))
    return None


def _safe_bounds(element):
    try:
        box = _bounds(element)
        return box if box and all(math.isfinite(value) for value in box) else None
    except (ValueError, TypeError, IndexError, KeyError, ArithmeticError, AssertionError, NotImplementedError):
        return None


def _viewport(elements, view_box, layout):
    canvas = view_box or layout.get("canvas") or {}
    full = {"x": 0, "y": 0, "width": canvas.get("width", 928), "height": canvas.get("height", 426)}
    boxes = [
        _safe_bounds(element) for element in elements
        if element.get("type") not in {"text", "text_box"} or str(element.get("text") or "").strip()
        or (element.get("interaction") or {}).get("role") == "answer"
    ]
    if not boxes or any(box is None for box in boxes):
        return full
    left = min(box[0] for box in boxes) - PADDING
    top = min(box[1] for box in boxes) - PADDING
    return {
        "x": left, "y": top,
        "width": max(1, max(box[2] for box in boxes) + PADDING - left),
        "height": max(1, max(box[3] for box in boxes) + PADDING - top),
    }


def _inside(frame, element):
    bounds = _safe_bounds(element)
    if bounds is None:
        return False
    x = (bounds[0] + bounds[2]) / 2
    y = (bounds[1] + bounds[3]) / 2
    return frame[0] <= x <= frame[2] and frame[1] <= y <= frame[3]


def project_canvas(elements, layout, view_box, presentation, schema, prompt):
    region_slots = {}
    for region in layout.get("regions", []):
        for ref in region.get("slot_ids", []):
            region_slots.setdefault(ref, set()).add(region.get("role"))
    slot_roles = {
        slot.get("id"): (slot.get("content") or {}).get("semantic_role")
        or (slot.get("content") or {}).get("style_role")
        for slot in layout.get("slots", [])
    }
    canvas_selection = presentation.get("mode") == "canvas_select"
    canvas_choices = {
        item for choice in presentation.get("canvas_choices", [])
        for item in choice.get("element_ids", [])
    }
    def normalize(value):
        return " ".join(value.split())

    options = [choice for field in schema["fields"] for choice in field.get("choices", [])]
    labels = {normalize(str(choice.get("label", ""))) for choice in options} - {""}
    option_ids = {choice["value"] for choice in options if isinstance(choice.get("value"), str)}
    panel_choices = not canvas_selection and bool(labels)
    prompt_lines = {normalize(line) for line in str(prompt or "").splitlines()} - {""}
    # A frame in the diagram is artwork. Keep the option it contains together
    # with the frame, even when students submit through the answer panel.
    diagram_frames = []
    if panel_choices:
        for element in elements:
            if element.get("type") != "rect" or element.get("interaction"):
                continue
            refs = _refs(element)
            role = (element.get("attributes") or {}).get("data-semantic-role")
            if role not in VISUAL_ROLES and not any(
                slot_roles.get(ref) in VISUAL_ROLES
                or region_slots.get(ref, set()) & VISUAL_ROLES
                for ref in refs
            ):
                continue
            bounds = _safe_bounds(element)
            if bounds:
                diagram_frames.append(bounds)
    kept = []
    hidden = []
    hidden_choices = []
    choice_frames = []
    for element in elements:
        refs = _refs(element)
        roles = {slot_roles.get(ref) for ref in refs}
        roles.add((element.get("attributes") or {}).get("data-semantic-role"))
        regions = set().union(*(region_slots.get(ref, set()) for ref in refs))
        text = str(element.get("text") or "")
        interaction = element.get("interaction") or {}
        selection = interaction.get("type") in {"choice", "select"}
        is_input = interaction.get("role") == "answer" and not selection
        protected = (
            is_input or bool(roles & VISUAL_ROLES) or element.get("id") in canvas_choices
        )
        choice_region = bool(regions & CHOICE_ROLES)
        removed_choice = panel_choices and (
            selection and bool((roles | regions) & CHOICE_ROLES)
            or element.get("type") in {"text", "text_box"} and (
                bool(roles & CHOICE_ROLES)
                or choice_region and (normalize(text) in labels or re.fullmatch(r"[\s(),，]+", text))
            )
        )
        is_option = bool(refs & option_ids) or normalize(text) in labels
        if removed_choice and is_option and any(
            _inside(frame, element) for frame in diagram_frames
        ):
            removed_choice = False
        hidden_text = (
            element.get("type") in {"text", "text_box"}
            and (
                "answer_prompt" in roles
                or (prompt_lines and bool((roles | regions) & PROMPT_ROLES))
                or (not regions & VISUAL_ROLES and normalize(text) in prompt_lines)
            )
        )
        if not protected and (removed_choice or hidden_text):
            hidden.append(element)
            if removed_choice:
                hidden_choices.append(element)
        else:
            kept.append(element)
            if (panel_choices and not protected and not interaction
                    and element.get("type") == "rect"
                    and (choice_region or any(re.search(r"(?:choice|option)", ref, re.I) for ref in refs))):
                choice_frames.append(element)
    for frame in choice_frames:
        bounds = _safe_bounds(frame)
        if bounds and any(_inside(bounds, choice) for choice in hidden_choices) and not any(
            _inside(bounds, element) for element in kept if element is not frame
        ):
            kept.remove(frame)
            hidden.append(frame)
    visible_refs = set().union(*(_refs(element) for element in kept))
    return kept, {
        "hidden_slot_ids": sorted(set().union(*(_refs(element) for element in hidden)) - visible_refs),
        "viewport": _viewport(kept, view_box, layout),
    }
