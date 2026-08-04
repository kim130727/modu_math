from __future__ import annotations

import argparse
import json
import sys
from dataclasses import fields, is_dataclass, replace
from pathlib import Path
from pprint import pformat
from types import ModuleType
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from modu_math.dsl.exporter import _render_problem_template_source
from modu_math_web.editor.services.dsl_format import format_dsl_source

from tools.extract_dsl_localization import (
    SKIP_FIELDS,
    TRANSLATABLE_FIELDS,
    load_dsl_module,
    object_id,
    problem_id_from,
    source_hash,
)


def read_locale(path: Path) -> dict[str, dict[str, str]]:
    loaded = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(loaded, dict):
        raise ValueError(f"Locale JSON must be an object: {path}")

    entries: dict[str, dict[str, str]] = {}
    for key, value in loaded.items():
        if isinstance(key, str) and isinstance(value, dict):
            entries[key] = {
                "source": value.get("source", "") if isinstance(value.get("source", ""), str) else "",
                "source_hash": value.get("source_hash", "")
                if isinstance(value.get("source_hash", ""), str)
                else "",
                "translation": value.get("translation", "")
                if isinstance(value.get("translation", ""), str)
                else "",
                "status": value.get("status", "") if isinstance(value.get("status", ""), str) else "",
            }
    return entries


def translation_for(
    entries: dict[str, dict[str, str]],
    key: str,
    source: str,
    *,
    include_needs_review: bool,
) -> str | None:
    entry = entries.get(key)
    if not entry:
        return None

    translation = entry.get("translation", "")
    if not translation:
        return None

    status = entry.get("status", "")
    if status == "obsolete":
        return None
    if status == "needs_review" and not include_needs_review:
        return None

    expected_hash = entry.get("source_hash", "")
    if expected_hash and expected_hash != source_hash(source):
        return None

    return translation


def apply_translations(
    value: Any,
    entries: dict[str, dict[str, str]],
    path: list[str],
    *,
    field_name: str | None = None,
    include_needs_review: bool = False,
) -> Any:
    if field_name in SKIP_FIELDS:
        return value

    if isinstance(value, str):
        if field_name not in TRANSLATABLE_FIELDS:
            return value
        translation = translation_for(
            entries,
            ".".join(path),
            value,
            include_needs_review=include_needs_review,
        )
        return translation if translation is not None else value

    if isinstance(value, (int, float, bool)) or value is None:
        return value

    if isinstance(value, list):
        return [
            apply_translations(
                item,
                entries,
                [*path, object_id(item) or str(index)],
                field_name=field_name,
                include_needs_review=include_needs_review,
            )
            for index, item in enumerate(value)
        ]

    if isinstance(value, tuple):
        return tuple(
            apply_translations(
                item,
                entries,
                [*path, object_id(item) or str(index)],
                field_name=field_name,
                include_needs_review=include_needs_review,
            )
            for index, item in enumerate(value)
        )

    if isinstance(value, dict):
        return {
            key: apply_translations(
                child,
                entries,
                [*path, key],
                field_name=key,
                include_needs_review=include_needs_review,
            )
            for key, child in value.items()
        }

    if is_dataclass(value) and not isinstance(value, type):
        updates: dict[str, Any] = {}
        for field in fields(value):
            child = getattr(value, field.name)
            updated = apply_translations(
                child,
                entries,
                [*path, field.name],
                field_name=field.name,
                include_needs_review=include_needs_review,
            )
            if updated is not child and updated != child:
                updates[field.name] = updated
        return replace(value, **updates) if updates else value

    return value


def localized_objects(
    module: ModuleType,
    entries: dict[str, dict[str, str]],
    *,
    include_needs_review: bool,
) -> tuple[Any, dict[str, Any] | None, dict[str, Any] | None]:
    template = getattr(module, "PROBLEM_TEMPLATE", None)
    if template is None:
        raise ValueError("DSL must define PROBLEM_TEMPLATE")

    localized_template = apply_translations(
        template,
        entries,
        ["template"],
        include_needs_review=include_needs_review,
    )

    semantic = getattr(module, "SEMANTIC_OVERRIDE", None)
    if semantic is None:
        semantic = getattr(module, "SEMANTIC", None)
    localized_semantic = None
    if semantic is not None:
        localized_semantic = apply_translations(
            semantic,
            entries,
            ["semantic"],
            include_needs_review=include_needs_review,
        )

    solvable = getattr(module, "SOLVABLE", None)
    localized_solvable = None
    if solvable is not None:
        localized_solvable = apply_translations(
            solvable,
            entries,
            ["solvable"],
            include_needs_review=include_needs_review,
        )

    return localized_template, localized_semantic, localized_solvable


def default_output_path(dsl_path: Path, locale: str) -> Path:
    suffix = f".{locale}.dsl.py"
    if dsl_path.name.endswith(".dsl.py"):
        return dsl_path.with_name(f"{dsl_path.name[:-len('.dsl.py')]}{suffix}")
    return dsl_path.with_name(f"{dsl_path.stem}{suffix}")


def render_localized_source(
    *,
    problem_id: str,
    template: Any,
    semantic: dict[str, Any] | None,
    solvable: dict[str, Any] | None,
) -> str:
    source = _render_problem_template_source(
        template,
        function_name="build_problem_template",
        variable_name="PROBLEM_TEMPLATE",
    ).rstrip()
    parts = [source, "", f"PROBLEM_ID = {problem_id!r}"]

    if semantic is not None:
        parts.extend(["", f"SEMANTIC_OVERRIDE = {pformat(semantic, width=100, sort_dicts=False)}"])
        parts.extend(["", "SEMANTIC = SEMANTIC_OVERRIDE"])

    if solvable is not None:
        parts.extend(["", f"SOLVABLE = {pformat(solvable, width=100, sort_dicts=False)}"])
        parts.extend(["", "SEMANTIC_ANSWER = SOLVABLE.get('answer')"])

    return format_dsl_source("\n".join(parts) + "\n")


def write_output(path: Path, source: str, *, force: bool) -> bool:
    if path.exists():
        current = path.read_text(encoding="utf-8")
        if current == source:
            return False
        if not force:
            raise FileExistsError(f"Output already exists. Use --force to overwrite: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(source, encoding="utf-8", newline="\n")
    return True


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Create a localized ModuMath DSL file from locale JSON.")
    parser.add_argument("--dsl", required=True, help="Source *.dsl.py file.")
    parser.add_argument("--locale-json", required=True, help="Locale JSON created by extract_dsl_localization.py.")
    parser.add_argument("--locale", help="Locale code for the default output filename, e.g. en-US.")
    parser.add_argument("--out", help="Output *.dsl.py path. Defaults to <source>.<locale>.dsl.py.")
    parser.add_argument("--force", action="store_true", help="Overwrite an existing output file.")
    parser.add_argument(
        "--include-needs-review",
        action="store_true",
        help="Apply translations whose status is needs_review. By default they are skipped.",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    dsl_path = Path(args.dsl)
    locale_json_path = Path(args.locale_json)
    locale = args.locale or locale_json_path.parent.name
    out_path = Path(args.out) if args.out else default_output_path(dsl_path, locale)

    module = load_dsl_module(dsl_path)
    entries = read_locale(locale_json_path)
    template, semantic, solvable = localized_objects(
        module,
        entries,
        include_needs_review=args.include_needs_review,
    )
    source = render_localized_source(
        problem_id=problem_id_from(module, dsl_path),
        template=template,
        semantic=semantic,
        solvable=solvable,
    )
    changed = write_output(out_path, source, force=args.force)

    action = "wrote" if changed else "unchanged"
    print(f"{action}: {out_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
