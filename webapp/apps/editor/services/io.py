from __future__ import annotations

import json
import re
from pathlib import Path, PurePosixPath
from typing import Any

from django.conf import settings


_SAFE_SEGMENT_RE = re.compile(r"[^a-zA-Z0-9_-]+")

_VISUAL_KEYS = {
    "x",
    "y",
    "x1",
    "y1",
    "x2",
    "y2",
    "cx",
    "cy",
    "r",
    "rx",
    "ry",
    "width",
    "height",
    "points",
    "path",
    "d",
    "anchor",
    "alignment",
    "z_index",
    "z_order",
    "fill",
    "stroke",
    "stroke_width",
    "stroke-linecap",
    "stroke-linejoin",
    "stroke_dasharray",
    "stroke-dasharray",
    "font_family",
    "font_size",
    "font_weight",
    "font_style",
    "font-family",
    "font-size",
    "font-weight",
    "font-style",
    "opacity",
    "transform",
    "background",
    "viewBox",
    "style",
}

_SEMANTIC_ONLY_KEYS = {
    "semantic_role",
    "answer_ref",
    "domain_ref",
    "question_ref",
    "is_correct",
    "correct",
}


def _store_root() -> Path:
    return Path(settings.PROBLEM_STORE_ROOT)


def _sanitize_segment(seg: str) -> str:
    cleaned = _SAFE_SEGMENT_RE.sub("_", seg.strip())
    return cleaned.strip("_") or "untitled"


def normalize_problem_id(problem_id: str) -> str:
    text = (problem_id or "").replace("\\", "/").strip("/")
    if not text:
        return "untitled_problem"
    parts = [p for p in text.split("/") if p and p != "."]
    safe_parts = [_sanitize_segment(p) for p in parts if p != ".."]
    return "/".join(safe_parts) or "untitled_problem"


def _safe_rel_problem_id(problem_id: str) -> str:
    normalized = normalize_problem_id(problem_id)
    p = PurePosixPath(normalized)
    if p.is_absolute() or ".." in p.parts:
        return "untitled_problem"
    return p.as_posix()


def _id_from_candidate(path: Path, root: Path) -> str | None:
    rel = path.relative_to(root).as_posix()
    parts = rel.split("/")
    if path.name == "semantic.json":
        return "/".join(parts[:-1]) or None
    if len(parts) >= 4 and parts[-3:] == ["output", "json", parts[-1]] and path.name.endswith(".semantic.json"):
        return "/".join(parts[:-3]) or None
    if path.name.endswith(".semantic.json"):
        return "/".join(parts[:-1]) or None
    if len(parts) >= 4 and parts[-3:] == ["input", "json", "semantic_final.json"]:
        return "/".join(parts[:-3]) or None
    return None


def _discover_candidates() -> dict[str, Path]:
    root = _store_root()
    root.mkdir(parents=True, exist_ok=True)

    # 우선순위: semantic.json > output/json/*.semantic.json > input/json/semantic_final.json
    collected: dict[str, tuple[int, Path]] = {}

    def put(path: Path, priority: int) -> None:
        problem_id = _id_from_candidate(path, root)
        if not problem_id:
            return
        prev = collected.get(problem_id)
        if prev is None or priority < prev[0]:
            collected[problem_id] = (priority, path)

    for path in root.rglob("semantic.json"):
        put(path, 1)
    for path in root.rglob("*.semantic.json"):
        if path.name == "semantic.json":
            continue
        put(path, 2)
    for path in root.rglob("semantic_final.json"):
        put(path, 3)

    return {k: v[1] for k, v in collected.items()}


def semantic_path(problem_id: str) -> Path:
    root = _store_root()
    safe_id = _safe_rel_problem_id(problem_id)
    known = _discover_candidates().get(safe_id)
    if known is not None:
        return known
    return root / safe_id / "semantic.json"


def _bundle_path_from_semantic(semantic_file: Path, bundle_kind: str, problem_id: str) -> Path:
    safe_rel = normalize_problem_id(problem_id)
    base_segment = safe_rel.split("/")[-1] if "/" in safe_rel else safe_rel
    safe_file_id = base_segment.replace("/", "_")
    name = semantic_file.name
    if name == "semantic.json":
        return semantic_file.with_name(f"{bundle_kind}.json")
    if name.endswith(".semantic.json"):
        return semantic_file.with_name(name.replace(".semantic.json", f".{bundle_kind}.json"))
    if name == "semantic_final.json":
        return semantic_file.with_name(f"{safe_file_id}.{bundle_kind}.json")
    return semantic_file.with_name(f"{semantic_file.stem}.{bundle_kind}.json")


def layout_path(problem_id: str) -> Path:
    sem = semantic_path(problem_id)
    return _bundle_path_from_semantic(sem, "layout", problem_id)


def renderer_path(problem_id: str) -> Path:
    sem = semantic_path(problem_id)
    return _bundle_path_from_semantic(sem, "renderer", problem_id)


def _default_semantic(problem_id: str) -> dict[str, Any]:
    safe_id = _safe_rel_problem_id(problem_id).replace("/", "_")
    return {
        "schema_version": "modu_math.semantic.v3",
        "render_contract_version": "modu_math.render.v1",
        "problem_id": safe_id,
        "problem_type": "generic",
        "metadata": {},
        "domain": {},
        "render": {"elements": []},
        "answer": {"blanks": [], "choices": [], "answer_key": []},
    }


def _default_layout(problem_id: str) -> dict[str, Any]:
    safe_id = _safe_rel_problem_id(problem_id).replace("/", "_")
    return {
        "problem_id": safe_id,
        "canvas": {"width": 1200, "height": 700, "background": "#F6F6F6"},
        "nodes": [],
    }


def _semantic_render_from_layout(layout: dict[str, Any]) -> dict[str, Any]:
    canvas = layout.get("canvas", {}) if isinstance(layout.get("canvas"), dict) else {}
    nodes = layout.get("nodes", [])
    elements: list[dict[str, Any]] = []

    if isinstance(nodes, list):
        for node in nodes:
            if not isinstance(node, dict):
                continue
            ntype = str(node.get("type", ""))
            props = node.get("properties", {}) if isinstance(node.get("properties"), dict) else {}
            element: dict[str, Any] = {"id": str(node.get("id", ""))}
            if "z_order" in node:
                element["z_index"] = node["z_order"]
            if "anchor" in node:
                element["anchor"] = node["anchor"]

            if ntype == "text":
                element["type"] = "formula" if props.get("is_formula") else "text"
                element["x"] = node.get("x", 0)
                element["y"] = node.get("y", 0)
                if props.get("is_formula"):
                    element["expr"] = props.get("text", "")
                else:
                    element["text"] = props.get("text", "")
                for key in ["fill", "stroke", "stroke_width", "font_family", "font_size", "font_weight", "font_style", "opacity", "transform"]:
                    if key in props:
                        element[key] = props[key]
                elements.append(element)
                continue

            shape_type = str(props.get("shape_type", "shape"))
            element["type"] = shape_type
            if shape_type == "line":
                element["x1"] = props.get("x1", node.get("x", 0))
                element["y1"] = props.get("y1", node.get("y", 0))
                if "x2" in props:
                    element["x2"] = props["x2"]
                if "y2" in props:
                    element["y2"] = props["y2"]
            elif shape_type == "circle":
                element["x"] = node.get("x", 0)
                element["y"] = node.get("y", 0)
                if "r" in props:
                    element["r"] = props["r"]
            elif shape_type == "polygon":
                if "points" in props:
                    element["points"] = props["points"]
            else:
                element["x"] = node.get("x", 0)
                element["y"] = node.get("y", 0)
                if "width" in node:
                    element["width"] = node["width"]
                if "height" in node:
                    element["height"] = node["height"]
                if "rx" in props:
                    element["rx"] = props["rx"]
                if "ry" in props:
                    element["ry"] = props["ry"]

            for key in ["fill", "stroke", "stroke_width", "opacity", "transform"]:
                if key in props:
                    element[key] = props[key]
            elements.append(element)

    return {
        "canvas": {
            "width": canvas.get("width", 1200),
            "height": canvas.get("height", 700),
            "background": canvas.get("background", "#F6F6F6"),
        },
        "elements": elements,
    }


def _layout_from_semantic_render(problem_id: str, semantic: dict[str, Any]) -> dict[str, Any]:
    render = semantic.get("render", {}) if isinstance(semantic.get("render"), dict) else {}
    canvas = render.get("canvas", {}) if isinstance(render.get("canvas"), dict) else {}
    elements = render.get("elements", [])

    nodes: list[dict[str, Any]] = []
    if isinstance(elements, list):
        for element in elements:
            if not isinstance(element, dict):
                continue
            etype = str(element.get("type", "shape"))
            node: dict[str, Any] = {
                "id": str(element.get("id", "")),
                "x": element.get("x", element.get("x1", 0)),
                "y": element.get("y", element.get("y1", 0)),
            }
            if "width" in element:
                node["width"] = element["width"]
            if "height" in element:
                node["height"] = element["height"]
            if "anchor" in element:
                node["anchor"] = element["anchor"]
            if "z_index" in element:
                node["z_order"] = element["z_index"]

            props: dict[str, Any] = {}
            if etype in {"text", "formula"}:
                node["type"] = "text"
                props["text"] = element.get("expr", "") if etype == "formula" else element.get("text", "")
                if etype == "formula":
                    props["is_formula"] = True
            else:
                node["type"] = "shape"
                props["shape_type"] = etype
                if etype == "line":
                    if "x1" in element:
                        props["x1"] = element["x1"]
                    if "y1" in element:
                        props["y1"] = element["y1"]
                    if "x2" in element:
                        props["x2"] = element["x2"]
                    if "y2" in element:
                        props["y2"] = element["y2"]
                if etype == "circle" and "r" in element:
                    props["r"] = element["r"]
                if etype == "polygon" and "points" in element:
                    props["points"] = element["points"]
                if etype == "rect":
                    if "rx" in element:
                        props["rx"] = element["rx"]
                    if "ry" in element:
                        props["ry"] = element["ry"]

            for key in ["fill", "stroke", "stroke_width", "font_family", "font_size", "font_weight", "font_style", "opacity", "transform"]:
                if key in element:
                    props[key] = element[key]

            node["properties"] = props
            nodes.append(node)

    return {
        "problem_id": semantic.get("problem_id", normalize_problem_id(problem_id).replace("/", "_")),
        "canvas": {
            "width": canvas.get("width", 1200),
            "height": canvas.get("height", 700),
            "background": canvas.get("background", "#F6F6F6"),
        },
        "nodes": nodes,
    }


def _renderer_from_layout(layout: dict[str, Any]) -> dict[str, Any]:
    canvas = layout.get("canvas", {}) if isinstance(layout.get("canvas"), dict) else {}
    nodes = layout.get("nodes", [])
    elements: list[dict[str, Any]] = []

    if isinstance(nodes, list):
        ordered_nodes = sorted([n for n in nodes if isinstance(n, dict)], key=lambda n: n.get("z_order", 0))
        for node in ordered_nodes:
            nid = str(node.get("id", ""))
            ntype = str(node.get("type", ""))
            props = node.get("properties", {}) if isinstance(node.get("properties"), dict) else {}

            if ntype == "text":
                attrs: dict[str, Any] = {
                    "x": node.get("x", 0),
                    "y": node.get("y", 0),
                }
                if "anchor" in node:
                    attrs["text-anchor"] = node["anchor"]
                for key in ["fill", "stroke", "stroke_width", "font_family", "font_size", "font_weight", "font_style", "opacity", "transform"]:
                    if key in props:
                        attrs[key.replace("_", "-")] = props[key]
                if props.get("is_formula"):
                    attrs["data-formula"] = props.get("text", "")
                    attrs["class"] = "formula-placeholder"
                elements.append(
                    {
                        "id": nid,
                        "type": "text",
                        "attributes": attrs,
                        "text": str(props.get("text", "")),
                    }
                )
                continue

            shape_type = str(props.get("shape_type", "shape"))
            attrs: dict[str, Any] = {}
            for key in ["fill", "stroke", "stroke_width", "opacity", "transform"]:
                if key in props:
                    attrs[key.replace("_", "-")] = props[key]

            if shape_type == "rect":
                attrs["x"] = node.get("x", 0)
                attrs["y"] = node.get("y", 0)
                if "width" in node:
                    attrs["width"] = node["width"]
                if "height" in node:
                    attrs["height"] = node["height"]
                if "rx" in props:
                    attrs["rx"] = props["rx"]
                if "ry" in props:
                    attrs["ry"] = props["ry"]
            elif shape_type == "circle":
                attrs["cx"] = node.get("x", 0)
                attrs["cy"] = node.get("y", 0)
                if "r" in props:
                    attrs["r"] = props["r"]
            elif shape_type == "line":
                attrs["x1"] = props.get("x1", node.get("x", 0))
                attrs["y1"] = props.get("y1", node.get("y", 0))
                if "x2" in props:
                    attrs["x2"] = props["x2"]
                if "y2" in props:
                    attrs["y2"] = props["y2"]
            elif shape_type == "polygon":
                if "points" in props:
                    attrs["points"] = props["points"]
            else:
                attrs["x"] = node.get("x", 0)
                attrs["y"] = node.get("y", 0)
                if "width" in node:
                    attrs["width"] = node["width"]
                if "height" in node:
                    attrs["height"] = node["height"]

            elements.append({"id": nid, "type": shape_type, "attributes": attrs})

    renderer: dict[str, Any] = {
        "problem_id": layout.get("problem_id", ""),
        "view_box": {
            "width": canvas.get("width", 1200),
            "height": canvas.get("height", 700),
            "background": canvas.get("background", "#F6F6F6"),
        },
        "elements": elements,
    }
    return renderer


def _strip_semantic_visuals(semantic: dict[str, Any]) -> dict[str, Any]:
    out = dict(semantic)
    render = out.get("render")
    if not isinstance(render, dict):
        out["render"] = {"elements": []}
        return out

    new_render = dict(render)
    new_render.pop("canvas", None)
    elements = new_render.get("elements", [])
    clean_elements: list[dict[str, Any]] = []
    if isinstance(elements, list):
        for element in elements:
            if not isinstance(element, dict):
                continue
            clean = {}
            for key, value in element.items():
                if key in _VISUAL_KEYS:
                    continue
                clean[key] = value
            clean_elements.append(clean)
    new_render["elements"] = clean_elements
    out["render"] = new_render
    return out


def list_problems() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for problem_id, path in sorted(_discover_candidates().items(), key=lambda item: item[0]):
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except Exception:
            data = {}
        rows.append(
            {
                "problem_id": problem_id,
                "title": data.get("title") or problem_id,
                "problem_type": data.get("problem_type") or "",
                "path": path,
            }
        )
    return rows


def load_semantic(problem_id: str) -> dict[str, Any]:
    sem_path = semantic_path(problem_id)
    if sem_path.exists():
        semantic = json.loads(sem_path.read_text(encoding="utf-8"))
    else:
        semantic = _default_semantic(problem_id)

    lay_path = layout_path(problem_id)
    if lay_path.exists():
        try:
            layout = json.loads(lay_path.read_text(encoding="utf-8"))
        except Exception:
            layout = _default_layout(problem_id)
    else:
        # Backward compatibility: keep editing possible for legacy semantic-only bundles.
        if isinstance(semantic, dict):
            layout = _layout_from_semantic_render(problem_id, semantic)
        else:
            layout = _default_layout(problem_id)

    if not isinstance(semantic, dict):
        semantic = _default_semantic(problem_id)
    semantic["render"] = _semantic_render_from_layout(layout)
    if not semantic.get("problem_id"):
        semantic["problem_id"] = normalize_problem_id(problem_id).replace("/", "_")
    return semantic


def save_semantic(problem_id: str, semantic: dict[str, Any]) -> Path:
    sem_path = semantic_path(problem_id)
    sem_path.parent.mkdir(parents=True, exist_ok=True)

    semantic_for_editor = dict(semantic) if isinstance(semantic, dict) else _default_semantic(problem_id)
    layout = _layout_from_semantic_render(problem_id, semantic_for_editor)
    renderer = _renderer_from_layout(layout)
    semantic_decoupled = _strip_semantic_visuals(semantic_for_editor)

    # Ensure layout does not carry semantic-only properties.
    nodes = layout.get("nodes", [])
    if isinstance(nodes, list):
        for node in nodes:
            if not isinstance(node, dict):
                continue
            props = node.get("properties", {})
            if isinstance(props, dict):
                for key in list(props.keys()):
                    if key in _SEMANTIC_ONLY_KEYS:
                        props.pop(key, None)

    sem_path.write_text(json.dumps(semantic_decoupled, ensure_ascii=False, indent=2), encoding="utf-8")

    lay_path = layout_path(problem_id)
    lay_path.parent.mkdir(parents=True, exist_ok=True)
    lay_path.write_text(json.dumps(layout, ensure_ascii=False, indent=2), encoding="utf-8")

    ren_path = renderer_path(problem_id)
    ren_path.parent.mkdir(parents=True, exist_ok=True)
    ren_path.write_text(json.dumps(renderer, ensure_ascii=False, indent=2), encoding="utf-8")

    return sem_path
