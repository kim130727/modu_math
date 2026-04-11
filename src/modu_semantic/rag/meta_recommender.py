from __future__ import annotations

import re
from pathlib import Path
from typing import Any

from .index_schema import RagIndexEntry
from .indexer import load_index_jsonl


_TOKEN_PATTERN = re.compile(r"[0-9A-Za-z가-힣]+")


def _tokenize(value: str) -> list[str]:
    return [token.lower() for token in _TOKEN_PATTERN.findall(value)]


def infer_problem_id_from_image_path(image_path: str | Path) -> str:
    stem = Path(image_path).stem.strip()
    match = re.search(r"\d{3,}", stem)
    if match:
        return match.group(0)
    return stem


def _entry_by_problem_id(entries: list[RagIndexEntry], problem_id: str) -> RagIndexEntry | None:
    for entry in entries:
        if str(entry.get("problem_id") or "") == problem_id:
            return entry
    return None


def _entry_by_filename_tokens(entries: list[RagIndexEntry], image_path: str | Path) -> RagIndexEntry | None:
    image_tokens = set(_tokenize(Path(image_path).stem))
    if not image_tokens:
        return None

    best: RagIndexEntry | None = None
    best_score = -1
    for entry in entries:
        pid_tokens = set(_tokenize(str(entry.get("problem_id") or "")))
        tag_tokens = set(_tokenize(" ".join(entry.get("tags") or [])))
        score = len(image_tokens & pid_tokens) * 3 + len(image_tokens & tag_tokens)
        if score > best_score:
            best = entry
            best_score = score
    if best_score <= 0:
        return None
    return best


def _merge_tags(base_tags: list[str], extra_tags: list[str]) -> list[str]:
    seen: set[str] = set()
    merged: list[str] = []
    for tag in [*base_tags, *extra_tags]:
        value = str(tag).strip()
        if not value:
            continue
        lowered = value.lower()
        if lowered in seen:
            continue
        seen.add(lowered)
        merged.append(value)
    return merged


def _is_useful_ocr_tag(tag: str) -> bool:
    value = tag.strip()
    if not value:
        return False
    if re.search(r"[가-힣]", value):
        return True
    if value.isdigit():
        return True
    if re.search(r"\d", value):
        return True
    if value.isalpha():
        return len(value) >= 4
    return len(value) >= 3


def recommend_input_meta(
    *,
    explicit_meta: dict[str, Any] | None,
    index_path: str | Path = "examples/problem/_rag/index.jsonl",
    image_path: str | Path | None = None,
) -> dict[str, Any]:
    meta: dict[str, Any] = dict(explicit_meta or {})
    entries = load_index_jsonl(index_path)

    if image_path and not meta.get("problem_id"):
        meta["problem_id"] = infer_problem_id_from_image_path(image_path)

    matched_entry: RagIndexEntry | None = None
    problem_id = str(meta.get("problem_id") or "")
    if problem_id:
        matched_entry = _entry_by_problem_id(entries, problem_id)
    if matched_entry is None and image_path:
        matched_entry = _entry_by_filename_tokens(entries, image_path)
        if matched_entry and not meta.get("problem_id"):
            meta["problem_id"] = str(matched_entry.get("problem_id") or "")

    defaults_from_entry = {
        "problem_type": "unknown",
        "grade": "unknown",
        "topic": "unknown",
        "layout_pattern": "unknown",
        "answer_style": "unknown",
        "visual_primitives": [],
        "tags": [],
    }
    if matched_entry:
        defaults_from_entry.update(
            {
                "problem_type": matched_entry.get("problem_type") or "unknown",
                "grade": matched_entry.get("grade") or "unknown",
                "topic": matched_entry.get("topic") or "unknown",
                "layout_pattern": matched_entry.get("layout_pattern") or "unknown",
                "answer_style": matched_entry.get("answer_style") or "unknown",
                "visual_primitives": list(matched_entry.get("visual_primitives") or []),
                "tags": list(matched_entry.get("tags") or []),
            }
        )

    for key, value in defaults_from_entry.items():
        if key not in meta or meta[key] in (None, "", []):
            meta[key] = value

    if image_path:
        inferred_tags = _tokenize(Path(image_path).stem)
        meta["tags"] = _merge_tags(list(meta.get("tags") or []), inferred_tags)

    if not meta.get("problem_id"):
        meta["problem_id"] = "rag_generated"

    return meta


def tune_meta_from_ocr_features(input_meta: dict[str, Any]) -> dict[str, Any]:
    tuned = dict(input_meta)
    text_lines = [str(line) for line in tuned.get("ocr_text_lines") or []]
    joined = " ".join(text_lines)
    tags = _merge_tags(list(tuned.get("tags") or []), [])
    tags = [tag for tag in tags if _is_useful_ocr_tag(str(tag))]

    if any(op in joined for op in ["×", "x", "X", "÷", "+", "-", "="]):
        tags = _merge_tags(tags, ["equation", "arithmetic"])
    if any(symbol in joined for symbol in ["▲", "△", "■", "□", "●", "○"]):
        tags = _merge_tags(tags, ["shape_number", "symbol_equation"])
    if any(word in joined for word in ["구하", "나타냅", "값", "얼마"]):
        tags = _merge_tags(tags, ["word_problem"])

    if tuned.get("ocr_boxes"):
        primitives = list(tuned.get("visual_primitives") or [])
        primitives = _merge_tags(primitives, ["text"])
        tuned["visual_primitives"] = primitives

    if str(tuned.get("layout_pattern") or "") in {"", "unknown"} and text_lines:
        line_count = len(text_lines)
        if line_count <= 2:
            tuned["layout_pattern"] = "simple"
        elif line_count <= 6:
            tuned["layout_pattern"] = "medium"
        else:
            tuned["layout_pattern"] = "dense"

    if str(tuned.get("problem_type") or "") in {"", "unknown"}:
        tag_set = {str(tag).lower() for tag in tags}
        if "shape_number" in tag_set and "equation" in tag_set:
            tuned["problem_type"] = "shape_number_equation"
        elif "equation" in tag_set:
            tuned["problem_type"] = "arithmetic_equation"
        elif "word_problem" in tag_set:
            tuned["problem_type"] = "word_problem"

    tuned["tags"] = tags
    return tuned
