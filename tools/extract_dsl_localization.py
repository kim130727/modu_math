from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import re
import sys
from dataclasses import fields, is_dataclass
from pathlib import Path
from types import ModuleType
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))


TRANSLATABLE_FIELDS = {
    "title",
    "text",
    "prompt",
    "placeholder",
    "subject",
    "topic",
    "label",
    "unit",
    "summary",
    "statement",
    "explanation",
    "method",
    "plan",
    "conditions",
    "choices",
    "goal",
}

SKIP_FIELDS = {
    "id",
    "type",
    "ref",
    "schema",
    "problem_id",
    "problem_type",
    "font_family",
    "answer",
    "answer_key",
    "answer_index",
    "expected",
    "actual",
    "value",
    "values",
    "blanks",
    "expr",
    "relation_expr",
    "symbolic",
    "result",
    "uses",
    "from_id",
    "to_id",
    "quantity",
    "count",
    "x",
    "y",
    "x1",
    "y1",
    "x2",
    "y2",
    "cx",
    "cy",
    "r",
    "width",
    "height",
    "points",
    "fill",
    "stroke",
    "text_color",
}

VALID_STATUSES = {"untranslated", "translated", "needs_review", "obsolete"}
COLOR_RE = re.compile(r"^#(?:[0-9a-fA-F]{3}|[0-9a-fA-F]{6}|[0-9a-fA-F]{8})$")
NUMBER_RE = re.compile(r"^[+-]?(?:\d+(?:\.\d*)?|\.\d+)(?:\s*[가-힣A-Za-z%]+)?$")
MATH_RE = re.compile(r"^[\d\s+\-*/=<>≤≥().,\[\]{}:]+$")


def load_dsl_module(path: Path) -> ModuleType:
    source = path.read_text(encoding="utf-8")
    digest = hashlib.sha256(source.encode("utf-8")).hexdigest()[:16]
    spec = importlib.util.spec_from_file_location(f"_modu_dsl_{path.stem}_{digest}", path)
    if spec is None:
        raise ValueError(f"Cannot load DSL module: {path}")
    module = importlib.util.module_from_spec(spec)
    code = compile(source, str(path), "exec")
    exec(code, module.__dict__)
    return module


def problem_id_from(module: ModuleType, dsl_path: Path) -> str:
    template = getattr(module, "PROBLEM_TEMPLATE", None)
    template_id = getattr(template, "id", None)
    if isinstance(template_id, str) and template_id:
        return template_id
    module_id = getattr(module, "PROBLEM_ID", None)
    if isinstance(module_id, str) and module_id:
        return module_id
    name = dsl_path.name
    return name[: -len(".dsl.py")] if name.endswith(".dsl.py") else dsl_path.stem


def object_id(value: Any) -> str | None:
    if isinstance(value, dict):
        raw = value.get("id")
    else:
        raw = getattr(value, "id", None)
    return raw if isinstance(raw, str) and raw else None


def iter_items(value: Any) -> list[tuple[str, Any]]:
    if isinstance(value, dict):
        return list(value.items())
    if is_dataclass(value) and not isinstance(value, type):
        return [(field.name, getattr(value, field.name)) for field in fields(value)]
    return []


def source_hash(source: str) -> str:
    return hashlib.sha256(source.encode("utf-8")).hexdigest()


def add_entry(entries: dict[str, dict[str, str]], key: str, source: str) -> None:
    if not is_translatable_source(source):
        return
    entries[key] = {
        "source": source,
        "source_hash": source_hash(source),
        "translation": "",
        "status": "untranslated",
    }


def is_translatable_source(source: str) -> bool:
    stripped = source.strip()
    if not stripped:
        return False
    if COLOR_RE.fullmatch(stripped):
        return False
    if NUMBER_RE.fullmatch(stripped):
        return False
    if MATH_RE.fullmatch(stripped):
        return False
    return True


def extract_value(
    value: Any,
    path: list[str],
    entries: dict[str, dict[str, str]],
    *,
    field_name: str | None = None,
) -> None:
    if field_name in SKIP_FIELDS:
        return

    if isinstance(value, str):
        if field_name in TRANSLATABLE_FIELDS:
            add_entry(entries, ".".join(path), value)
        return

    if isinstance(value, (int, float, bool)) or value is None:
        return

    if isinstance(value, (list, tuple)):
        for index, item in enumerate(value):
            item_id = object_id(item)
            item_part = item_id if item_id else str(index)
            extract_value(item, [*path, item_part], entries, field_name=field_name)
        return

    for child_name, child in iter_items(value):
        extract_value(child, [*path, child_name], entries, field_name=child_name)


def extract_localization(module: ModuleType) -> dict[str, dict[str, str]]:
    entries: dict[str, dict[str, str]] = {}

    template = getattr(module, "PROBLEM_TEMPLATE", None)
    if template is not None:
        extract_value(template, ["template"], entries)

    semantic = getattr(module, "SEMANTIC_OVERRIDE", None)
    if semantic is None:
        semantic = getattr(module, "SEMANTIC", None)
    if semantic is not None:
        extract_value(semantic, ["semantic"], entries)

    solvable = getattr(module, "SOLVABLE", None)
    if solvable is not None:
        extract_value(solvable, ["solvable"], entries)

    return {key: entries[key] for key in sorted(entries)}


def merge_entries(
    extracted: dict[str, dict[str, str]],
    existing: dict[str, Any],
) -> dict[str, dict[str, str]]:
    merged: dict[str, dict[str, str]] = {}

    for key, entry in extracted.items():
        previous = existing.get(key)
        if isinstance(previous, dict):
            translation = previous.get("translation", "")
            status = previous.get("status", "untranslated")
            if status not in VALID_STATUSES:
                status = "untranslated"
            if previous.get("source_hash") != entry["source_hash"]:
                status = "needs_review"
            elif status == "obsolete":
                status = "untranslated" if not translation else "translated"
            merged[key] = {
                "source": entry["source"],
                "source_hash": entry["source_hash"],
                "translation": translation if isinstance(translation, str) else "",
                "status": status,
            }
        else:
            merged[key] = entry

    for key in sorted(set(existing) - set(extracted)):
        previous = existing[key]
        if not isinstance(previous, dict):
            continue
        obsolete = {
            "source": previous.get("source", ""),
            "source_hash": previous.get("source_hash", ""),
            "translation": previous.get("translation", ""),
            "status": "obsolete",
        }
        merged[key] = {name: value if isinstance(value, str) else "" for name, value in obsolete.items()}
        merged[key]["status"] = "obsolete"

    return {key: merged[key] for key in sorted(merged)}


def read_existing(path: Path, *, force: bool) -> dict[str, Any]:
    if not path.exists():
        return {}
    try:
        loaded = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        if force:
            return {}
        raise
    if not isinstance(loaded, dict):
        if force:
            return {}
        raise ValueError(f"Existing locale JSON must be an object: {path}")
    return loaded


def write_locale(path: Path, entries: dict[str, dict[str, str]]) -> bool:
    payload = json.dumps(entries, ensure_ascii=False, indent=2) + "\n"
    if path.exists() and path.read_text(encoding="utf-8") == payload:
        return False
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(payload, encoding="utf-8", newline="\n")
    return True


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Extract translatable strings from one ModuMath DSL file.")
    parser.add_argument("--dsl", required=True, help="Path to a single *.dsl.py file.")
    parser.add_argument("--locale", required=True, help="Locale code, e.g. en-US.")
    parser.add_argument("--out", help="Output JSON path. Defaults to locales/<locale>/<problem_id>.locale.json.")
    parser.add_argument("--force", action="store_true", help="Recreate malformed existing JSON instead of failing.")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    dsl_path = Path(args.dsl)
    module = load_dsl_module(dsl_path)
    problem_id = problem_id_from(module, dsl_path)
    out_path = Path(args.out) if args.out else ROOT / "locales" / args.locale / f"{problem_id}.locale.json"

    extracted = extract_localization(module)
    existing = read_existing(out_path, force=args.force)
    merged = merge_entries(extracted, existing)
    changed = write_locale(out_path, merged)

    action = "wrote" if changed else "unchanged"
    print(f"{action}: {out_path} ({len(extracted)} active, {len(merged) - len(extracted)} obsolete)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
