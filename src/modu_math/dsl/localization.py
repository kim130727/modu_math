"""Apply small, human-editable locale catalogs to canonical problem objects."""
from __future__ import annotations

from dataclasses import fields, is_dataclass, replace
import hashlib
import json
from pathlib import Path
from typing import Any

from modu_math.dsl.symbol_roles import (
    is_protected_symbol_role,
    is_symbol_marker_text,
    localize_jamo_markers,
)


TRANSLATABLE_FIELDS = {
    "title", "text", "prompt", "placeholder", "subject", "topic", "label",
    "unit", "summary", "statement", "explanation", "method", "plan",
    "conditions", "choices", "goal", "question", "instruction", "name",
    "content", "description",
}
IDENTIFIER_FIELDS = {
    "id", "type", "ref", "schema", "problem_id", "problem_type",
    "font_family", "uses", "from_id", "to_id", "slot_ids",
}
SKIP_FIELDS = {
    "id", "type", "ref", "schema", "problem_id", "problem_type",
    "font_family", "answer", "answer_key", "answer_index", "expected",
    "actual", "value", "values", "blanks", "expr", "relation_expr",
    "symbolic", "result", "uses", "from_id", "to_id", "quantity", "count",
    "x", "y", "x1", "y1", "x2", "y2", "cx", "cy", "r", "width",
    "height", "points", "fill", "stroke", "text_color",
}


def source_hash(source: str) -> str:
    return hashlib.sha256(source.encode("utf-8")).hexdigest()


def object_id(value: Any) -> str | None:
    raw = value.get("id") if isinstance(value, dict) else getattr(value, "id", None)
    return raw if isinstance(raw, str) and raw else None


def is_protected_locale_container(value: Any) -> bool:
    role = value.get("semantic_role") if isinstance(value, dict) else getattr(value, "semantic_role", None)
    return is_protected_symbol_role(role if isinstance(role, str) else None)


def read_catalog(path: Path) -> dict[str, dict[str, str]]:
    loaded = json.loads(path.read_text(encoding="utf-8-sig"))
    if isinstance(loaded, dict) and isinstance(loaded.get("strings"), dict):
        loaded = loaded["strings"]
    if not isinstance(loaded, dict):
        raise ValueError(f"Locale catalog must be an object: {path}")
    return {key: value for key, value in loaded.items()
            if isinstance(key, str) and isinstance(value, dict)}


def translation_for(entries, key: str, source: str, *, include_needs_review: bool) -> str | None:
    entry = entries.get(key)
    if not isinstance(entry, dict):
        return None
    translation = entry.get("translation")
    if not isinstance(translation, str) or not translation:
        return None
    status = entry.get("status", "")
    if status == "obsolete" or (status == "needs_review" and not include_needs_review):
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
    locale: str,
    field_name: str | None = None,
    include_needs_review: bool = True,
    symbols_only: bool = False,
) -> Any:
    if field_name in IDENTIFIER_FIELDS:
        return value
    protected = symbols_only or is_protected_locale_container(value) or field_name in SKIP_FIELDS
    if isinstance(value, str):
        # Explicit catalog entries are authoritative, including answers and labels
        # that the automatic extractor intentionally omits.
        translation = translation_for(
            entries, ".".join(path), value,
            include_needs_review=include_needs_review,
        )
        if translation is not None:
            return localize_jamo_markers(translation, locale)
        localized = localize_jamo_markers(value, locale)
        if protected or field_name not in TRANSLATABLE_FIELDS or is_symbol_marker_text(value):
            return localized
        return localized
    if isinstance(value, (int, float, bool)) or value is None:
        return value
    if isinstance(value, list):
        return [apply_translations(item, entries, [*path, object_id(item) or str(index)],
                                   locale=locale, field_name=field_name,
                                   include_needs_review=include_needs_review,
                                   symbols_only=protected)
                for index, item in enumerate(value)]
    if isinstance(value, tuple):
        return tuple(apply_translations(item, entries, [*path, object_id(item) or str(index)],
                                        locale=locale, field_name=field_name,
                                        include_needs_review=include_needs_review,
                                        symbols_only=protected)
                     for index, item in enumerate(value))
    if isinstance(value, dict):
        return {key: apply_translations(child, entries, [*path, key], locale=locale,
                                        field_name=key,
                                        include_needs_review=include_needs_review,
                                        symbols_only=protected)
                for key, child in value.items()}
    if is_dataclass(value) and not isinstance(value, type):
        updates = {}
        for field in fields(value):
            child = getattr(value, field.name)
            updated = apply_translations(child, entries, [*path, field.name],
                                         locale=locale, field_name=field.name,
                                         include_needs_review=include_needs_review,
                                         symbols_only=protected)
            if updated != child:
                updates[field.name] = updated
        return replace(value, **updates) if updates else value
    return value


def collect_translations(
    source: Any,
    target: Any,
    path: list[str],
    entries: dict[str, dict[str, str]],
    *,
    field_name: str | None = None,
) -> None:
    """Record string differences; layout and structure are stored elsewhere."""
    if source == target:
        return
    if isinstance(source, str) and isinstance(target, str):
        if field_name in IDENTIFIER_FIELDS:
            return
        entries[".".join(path)] = {"source": source, "translation": target}
        return
    if type(source) is not type(target):
        return
    if isinstance(source, (list, tuple)):
        source_by_id = {object_id(item): item for item in source if object_id(item)}
        target_by_id = {object_id(item): item for item in target if object_id(item)}
        if source_by_id and set(source_by_id) == set(target_by_id):
            for key in source_by_id:
                collect_translations(source_by_id[key], target_by_id[key], [*path, key], entries,
                                     field_name=field_name)
            return
        if len(source) != len(target):
            return
        for index, (left, right) in enumerate(zip(source, target)):
            collect_translations(left, right, [*path, object_id(left) or str(index)], entries,
                                 field_name=field_name)
        return
    if isinstance(source, dict):
        if set(source) != set(target):
            return
        for key in source:
            collect_translations(source[key], target[key], [*path, key], entries, field_name=key)
        return
    if is_dataclass(source) and not isinstance(source, type):
        for field in fields(source):
            collect_translations(getattr(source, field.name), getattr(target, field.name),
                                 [*path, field.name], entries, field_name=field.name)
        return
    return


def string_values(
    value: Any,
    path: list[str],
    result: dict[str, str],
    *,
    field_name: str | None = None,
) -> None:
    """Index strings with the same stable keys used by extraction and application."""
    if field_name in IDENTIFIER_FIELDS:
        return
    if isinstance(value, str):
        result[".".join(path)] = value
        return
    if isinstance(value, (int, float, bool)) or value is None:
        return
    if isinstance(value, (list, tuple)):
        for index, item in enumerate(value):
            string_values(item, [*path, object_id(item) or str(index)], result,
                          field_name=field_name)
        return
    if isinstance(value, dict):
        for key, child in value.items():
            string_values(child, [*path, key], result, field_name=key)
        return
    if is_dataclass(value) and not isinstance(value, type):
        for field in fields(value):
            string_values(getattr(value, field.name), [*path, field.name], result,
                          field_name=field.name)
