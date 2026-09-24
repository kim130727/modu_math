"""Virtual localized DSLs: one authored Python source plus JSON field differences."""

from __future__ import annotations

from copy import deepcopy
from dataclasses import fields, is_dataclass
import json
import os
from pathlib import Path
from pprint import pformat
from types import SimpleNamespace

from modu_math import dsl
from modu_math.dsl.exporter import _render_problem_template_source

SUFFIX = ".locale-delta.json"
EXPORTS = (
    "SEMANTIC_OVERRIDE",
    "SEMANTIC_ANSWER",
    "SOLVABLE",
    "EDITOR_CHOICE_GROUPS",
    "EDITOR_ANSWER_REVIEW",
    "TUTOR_RENDERER_FLOW",
)


def delta_path(path: Path) -> Path:
    from .problem_store import section, location
    info = location(path)
    if info and info[1] != "ko":
        stored = section(path, "delta")
        if stored is not None:
            return stored
    return path.with_name(path.name.removesuffix(".dsl.py") + SUFFIX)


def available(path: Path) -> bool:
    return path.is_file() or delta_path(path).is_file()


def encode(value):
    if is_dataclass(value):
        return {
            "$type": type(value).__name__,
            **{
                field.name: encode(getattr(value, field.name))
                for field in fields(value)
            },
        }
    if isinstance(value, (tuple, list)):
        ids = [
            getattr(item, "id", None) if not isinstance(item, dict) else item.get("id")
            for item in value
        ]
        if (
            value
            and all(isinstance(key, str) for key in ids)
            and len(set(ids)) == len(ids)
        ):
            return {
                "$sequence": "tuple" if isinstance(value, tuple) else "list",
                "$order": ids,
                "$items": {key: encode(item) for key, item in zip(ids, value)},
            }
        if isinstance(value, tuple):
            return {"$tuple": [encode(item) for item in value]}
        return [encode(item) for item in value]
    if isinstance(value, dict):
        return {key: encode(item) for key, item in value.items()}
    if value is None or isinstance(value, (str, int, float, bool)):
        return value
    raise TypeError(f"Unsupported localized value: {type(value).__name__}")


def decode(value):
    if isinstance(value, list):
        return [decode(item) for item in value]
    if not isinstance(value, dict):
        return value
    if "$type" in value:
        cls = getattr(dsl, value["$type"])
        if not is_dataclass(cls):
            raise ValueError("Invalid DSL data class")
        return cls(
            **{key: decode(item) for key, item in value.items() if key != "$type"}
        )
    if "$sequence" in value:
        items = [decode(value["$items"][key]) for key in value["$order"]]
        return tuple(items) if value["$sequence"] == "tuple" else items
    if "$tuple" in value:
        return tuple(decode(item) for item in value["$tuple"])
    return {key: decode(item) for key, item in value.items()}


def snapshot(source: str, path: Path) -> dict:
    namespace = {"__file__": str(path), "__name__": "modu_variant"}
    exec(compile(source, str(path), "exec"), namespace)
    template = namespace.get("PROBLEM_TEMPLATE")
    if template is None:
        template = namespace["build_problem_template"]()
    result = {"PROBLEM_TEMPLATE": encode(template)}
    for name in EXPORTS:
        if name in namespace:
            result[name] = encode(namespace[name])
    if "SOLVABLE" not in result and "build_solvable" in namespace:
        result["SOLVABLE"] = encode(namespace["build_solvable"]())
    if "SEMANTIC_OVERRIDE" not in result and "SEMANTIC" in namespace:
        result["SEMANTIC_OVERRIDE"] = encode(namespace["SEMANTIC"])
    return result


def differences(base, target, path=()):
    if base == target:
        return []
    if isinstance(base, dict) and isinstance(target, dict):
        changes = []
        for key in sorted(base.keys() | target.keys()):
            current = (*path, key)
            if key not in target:
                changes.append({"path": current, "delete": True, "source": base[key]})
            elif key not in base:
                changes.append({"path": current, "value": target[key]})
            else:
                changes.extend(differences(base[key], target[key], current))
        return changes
    if isinstance(base, list) and isinstance(target, list) and len(base) == len(target):
        return [
            change
            for index, (left, right) in enumerate(zip(base, target))
            for change in differences(left, right, (*path, index))
        ]
    return [{"path": path, "source": base, "value": target}]


def apply_differences(base, changes):
    result = deepcopy(base)
    for change in changes:
        parent = result
        for key in change["path"][:-1]:
            missing = (
                (key not in parent)
                if isinstance(parent, dict)
                else (not isinstance(key, int) or key >= len(parent))
            )
            if missing:
                raise ValueError(
                    f"Source structure changed; review translation at {change['path']}"
                )
            parent = parent[key]
        key = change["path"][-1]
        if change.get("delete"):
            if isinstance(parent, dict):
                parent.pop(key, None)
            else:
                del parent[key]
        else:
            parent[key] = deepcopy(change["value"])
    return result


def source_path(path: Path) -> Path:
    data = json.loads(delta_path(path).read_text(encoding="utf-8"))
    reference = Path(data["source"])
    if reference.is_absolute():
        raise ValueError("Variant source must be relative")
    source = (path.parent / reference).resolve()
    # Variants are siblings under language folders; never follow references outside that root.
    root = next(
        (
            parent.parent
            for parent in path.resolve().parents
            if parent.name in {"en", "ja", "zh", "uk", "km"}
        ),
        path.parent.resolve(),
    )
    if root not in source.parents or not source.is_file() or "ko" not in source.parts:
        raise ValueError(f"Invalid Korean source: {source}")
    return source


def materialized_snapshot(path: Path) -> dict:
    if not delta_path(path).exists():
        return snapshot(path.read_text(encoding="utf-8-sig"), path)
    source = source_path(path)
    base = snapshot(source.read_text(encoding="utf-8-sig"), source)
    data = json.loads(delta_path(path).read_text(encoding="utf-8"))
    return apply_differences(base, data["changes"])


def render_snapshot(data: dict) -> str:
    template = decode(data["PROBLEM_TEMPLATE"])
    source = _render_problem_template_source(
        template,
        function_name="build_problem_template",
        variable_name="PROBLEM_TEMPLATE",
    )
    for name in EXPORTS:
        if name in data:
            source += f"\n{name} = {pformat(decode(data[name]), width=100, sort_dicts=False)}\n"
    return source


def read_source(path: Path) -> str:
    if delta_path(path).exists():
        return render_snapshot(materialized_snapshot(path))
    return path.read_text(encoding="utf-8-sig")


def write_source(path: Path, source: str) -> None:
    if not delta_path(path).exists():
        from .problem_store import atomic_write
        atomic_write(path, source.encode("utf-8"))
        return
    canonical = source_path(path)
    save_variant(path, canonical, snapshot(source, path), preserve_review=True)


def save_variant(
    path: Path, canonical: Path, target: dict, *, preserve_review=False
) -> None:
    base = snapshot(canonical.read_text(encoding="utf-8-sig"), canonical)
    data = {
        "version": 1,
        "source": Path(os.path.relpath(canonical, path.parent)).as_posix(),
        "changes": differences(base, target),
    }
    output = delta_path(path)
    if preserve_review:
        previous = json.loads(output.read_text(encoding="utf-8"))
        old_changes = {tuple(change["path"]): change for change in previous["changes"]}
        for change in data["changes"]:
            old = old_changes.get(tuple(change["path"]))
            if old and "source" in old and old.get("value") == change.get("value"):
                change["source"] = old["source"]
    from .problem_store import JsonSection, atomic_write
    text = json.dumps(data, ensure_ascii=False, indent=2) + "\n"
    if isinstance(output, JsonSection):
        output.write_text(text)
    else:
        atomic_write(output, text.encode("utf-8"))


def load_module(path: Path):
    return SimpleNamespace(
        **{name: decode(value) for name, value in materialized_snapshot(path).items()}
    )


def review_paths(path: Path) -> list[list]:
    """Report translations whose original source value has changed."""
    if not delta_path(path).exists():
        return []
    canonical = source_path(path)
    base = snapshot(canonical.read_text(encoding="utf-8-sig"), canonical)
    data = json.loads(delta_path(path).read_text(encoding="utf-8"))
    review = []
    for change in data["changes"]:
        if "source" not in change:
            continue
        current = base
        try:
            for key in change["path"]:
                current = current[key]
        except (KeyError, IndexError, TypeError):
            review.append(change["path"])
            continue
        if current != change["source"]:
            review.append(change["path"])
    return review
