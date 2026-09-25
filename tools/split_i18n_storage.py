"""Migrate legacy *.i18n.json bundles into locale, layout, and review files."""
from __future__ import annotations

import argparse
from copy import deepcopy
from dataclasses import fields, is_dataclass
import json
from pathlib import Path

from modu_math.dsl.localization import IDENTIFIER_FIELDS, object_id
from modu_math.dsl.problem_store import atomic_write, locale_path, override_path, review_path
from modu_math.dsl.variants import apply_differences, decode, snapshot


def _collect_strings(source, target, path, result, *, field_name=None):
    if source == target or field_name in IDENTIFIER_FIELDS:
        return
    if isinstance(source, str) and isinstance(target, str):
        result[".".join(path)] = {"source": source, "translation": target}
        return
    if isinstance(source, dict) and isinstance(target, dict):
        for key in source.keys() & target.keys():
            _collect_strings(source[key], target[key], [*path, key], result, field_name=key)
        return
    if isinstance(source, (list, tuple)) and isinstance(target, (list, tuple)):
        source_ids = {object_id(item): item for item in source if object_id(item)}
        target_ids = {object_id(item): item for item in target if object_id(item)}
        if source_ids and target_ids:
            for key in source_ids.keys() & target_ids.keys():
                _collect_strings(source_ids[key], target_ids[key], [*path, key], result,
                                 field_name=field_name)
        else:
            for index, (left, right) in enumerate(zip(source, target)):
                _collect_strings(left, right, [*path, str(index)], result,
                                 field_name=field_name)
        return
    if is_dataclass(source) and is_dataclass(target) and type(source) is type(target):
        for field in fields(source):
            _collect_strings(getattr(source, field.name), getattr(target, field.name),
                             [*path, field.name], result, field_name=field.name)


def migrate_document(document: Path) -> list[Path]:
    data = json.loads(document.read_text(encoding="utf-8-sig"))
    canonical = document.with_name(document.name.removesuffix(".i18n.json") + ".dsl.py")
    root = canonical.parent.parent
    virtual = root / "uk" / canonical.name
    base = snapshot(canonical.read_text(encoding="utf-8-sig"), canonical)
    localized = data.get("languages", {}).get("uk", {})
    current = apply_differences(base, localized.get("delta", {}).get("changes", []))
    uk_overrides = deepcopy(localized.get("editor_overrides", {"version": 1}))

    strings = deepcopy(localized.get("translation_catalog", {}))
    changed_strings = {}
    for name, root_name in (("PROBLEM_TEMPLATE", "template"),
                            ("SEMANTIC_OVERRIDE", "semantic"),
                            ("SOLVABLE", "solvable")):
        if name in base and name in current:
            _collect_strings(decode(base[name]), decode(current[name]), [root_name], changed_strings)
    for key, entry in changed_strings.items():
        previous = strings.get(key)
        if isinstance(previous, dict) and previous.get("translation") == entry["translation"]:
            entry.update({key: value for key, value in previous.items()
                          if key not in {"source", "translation"}})
        strings[key] = entry

    strings = {
        key: value for key, value in strings.items()
        if value.get("source") != value.get("translation")
    }
    catalog = {
        "version": 1,
        "problem_id": canonical.name.removesuffix(".dsl.py"),
        "source_language": "ko",
        "target_language": "uk",
        "strings": dict(sorted(strings.items())),
    }
    base_template = decode(base["PROBLEM_TEMPLATE"])
    current_template = decode(current["PROBLEM_TEMPLATE"])
    base_slots = {slot.id: slot for slot in base_template.slots}
    current_slots = {slot.id: slot for slot in current_template.slots}
    geometry_fields = {
        "x", "y", "width", "height", "font_size", "max_width", "align",
        "valign", "line_height", "anchor", "fill", "transform",
    }
    slot_overrides = uk_overrides.setdefault("slots", {})
    for slot_id in base_slots.keys() & current_slots.keys():
        before, after = base_slots[slot_id], current_slots[slot_id]
        for field in fields(before):
            if field.name in geometry_fields and getattr(before, field.name) != getattr(after, field.name):
                slot_overrides.setdefault(slot_id, {})[field.name] = getattr(after, field.name)
    if not slot_overrides:
        uk_overrides.pop("slots", None)
    outputs = []
    for path, payload in (
        (locale_path(virtual, "uk"), catalog),
        (override_path(canonical, "ko"), data.get("editor_overrides", {"version": 1})),
        (override_path(virtual, "uk"), uk_overrides),
    ):
        atomic_write(path, (json.dumps(payload, ensure_ascii=False, indent=2) + "\n").encode())
        outputs.append(path)

    review = current.get("EDITOR_ANSWER_REVIEW")
    if review is not None and review != base.get("EDITOR_ANSWER_REVIEW"):
        path = review_path(virtual, "uk")
        atomic_write(path, (json.dumps(decode(review), ensure_ascii=False, indent=2) + "\n").encode())
        outputs.append(path)

    provenance = data.get("provenance")
    if provenance:
        project = locale_path(virtual, "uk").parents[2]
        path = project / ".modu-cache" / "provenance" / document.name
        atomic_write(path, (json.dumps(provenance, ensure_ascii=False, indent=2) + "\n").encode())
    return outputs


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", type=Path, nargs="?", default=Path("examples/problems"))
    parser.add_argument("--delete", action="store_true", help="Delete legacy documents after migration.")
    args = parser.parse_args(argv)
    documents = sorted((args.root / "ko").rglob("*.i18n.json"))
    outputs = [path for document in documents for path in migrate_document(document)]
    if args.delete:
        for document in documents:
            document.unlink()
    print({"documents": len(documents), "outputs": len(outputs), "deleted": len(documents) if args.delete else 0})
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
