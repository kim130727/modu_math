"""Resolve explicitly linked translation layouts from authored DSL, never artifacts.

Precedence: shared source DSL + source edits, translated text, local edits.
The link lives in editor_overrides.json so rebuilding cannot erase it.
"""
from __future__ import annotations

from copy import deepcopy
import json
from pathlib import Path
import re
from typing import Any

from modu_math.dsl import compile_problem_template_to_layout
from modu_math.layout.editor_overrides import apply_editor_overrides, prune_editor_overrides


def override_path(dsl_path: Path) -> Path:
    return dsl_path.with_name(dsl_path.name.removesuffix(".dsl.py") + ".editor_overrides.json")


def read_overrides(dsl_path: Path) -> dict[str, Any]:
    path = override_path(dsl_path)
    return json.loads(path.read_text(encoding="utf-8-sig")) if path.exists() else {}


def inherit_layout(localized: dict, source: dict, deleted: set[str]) -> dict:
    """Share geometry by semantic slot ID; keep translations and answer behavior."""
    result = deepcopy(localized)
    source_slots = {slot["id"]: slot for slot in source["slots"]}
    merged = []
    for slot in result["slots"]:
        slot_id = slot["id"]
        if slot_id in deleted:
            continue
        base = source_slots.get(slot_id)
        if base is None:
            merged.append(slot)
            continue
        target = deepcopy(base)
        for key in ("text", "prompt", "placeholder", "font_family", "interaction", "input_style"):
            if key not in slot.get("content", {}):
                continue
            value = slot["content"][key]
            source_value = base["content"].get(key)
            # Numeric spacing is geometry shared by all translations. Prose is
            # always translated, even when only its whitespace differs.
            same_math = (
                key == "text" and isinstance(value, str) and isinstance(source_value, str)
                and re.fullmatch(r"[\d\s+×÷*/=().,−-]+", value)
                and re.sub(r"\s", "", value) == re.sub(r"\s", "", source_value)
            )
            if not same_math:
                target["content"][key] = deepcopy(value)
        merged.append(target)
    # Shared decorative shapes inserted in the editor have no translated text.
    local_ids = {slot["id"] for slot in localized["slots"]}
    merged.extend(deepcopy(slot) for slot in source["slots"]
                  if slot["id"] not in local_ids and slot["kind"] not in {"text", "text_box", "label", "choice", "blank"})
    result["slots"] = merged
    result["canvas"] = deepcopy(source["canvas"])
    valid_ids = {slot["id"] for slot in merged}
    regions = {region["id"]: deepcopy(region) for region in source.get("regions", [])}
    for region in localized.get("regions", []):
        if region["id"] not in regions:
            regions[region["id"]] = deepcopy(region)
        else:
            regions[region["id"]]["slot_ids"].extend(
                sid for sid in region["slot_ids"] if sid not in source_slots)
    for region in regions.values():
        region["slot_ids"] = list(dict.fromkeys(sid for sid in region["slot_ids"] if sid in valid_ids))
    result["regions"] = list(regions.values())
    for key in ("groups", "constraints", "diagrams", "reading_order"):
        if key in source:
            result[key] = deepcopy(source[key])
    return result


def resolve_shared_layout(layout: dict, dsl_path: Path, *, ancestors: tuple[Path, ...] = ()) -> dict:
    path = dsl_path.resolve()
    if path in ancestors:
        raise ValueError(f"Circular layout_source: {path}")
    reference = read_overrides(path).get("layout_source")
    if reference is None:
        return layout
    if not isinstance(reference, str) or not reference.endswith(".dsl.py"):
        raise ValueError("layout_source must name a relative *.dsl.py file")
    if Path(reference).is_absolute():
        raise ValueError("layout_source must be relative to the translated DSL")
    source_path = (path.parent / reference).resolve()
    namespace: dict[str, Any] = {"__file__": str(source_path), "__name__": "modu_shared_layout"}
    exec(compile(source_path.read_text(encoding="utf-8-sig"), str(source_path), "exec"), namespace)
    template = namespace.get("PROBLEM_TEMPLATE")
    if template is None:
        template = namespace["build_problem_template"]()
    source = compile_problem_template_to_layout(template)
    original_ids = {slot["id"] for slot in source["slots"]}
    source = resolve_shared_layout(source, source_path, ancestors=(*ancestors, path))
    overrides, _ = prune_editor_overrides(source, read_overrides(source_path))
    source = apply_editor_overrides(source, overrides)
    deleted = original_ids - {slot["id"] for slot in source["slots"]}
    return inherit_layout(layout, source, deleted)
