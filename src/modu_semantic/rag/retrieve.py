from __future__ import annotations

from typing import Any

from .index_schema import RagIndexEntry
from .indexer import load_index_jsonl


def score_entry(input_meta: dict[str, Any], entry: RagIndexEntry) -> float:
    score = 0.0

    input_problem_type = str(input_meta.get("problem_type") or "")
    if input_problem_type and input_problem_type == entry.get("problem_type"):
        score += 5.0

    input_layout_pattern = str(input_meta.get("layout_pattern") or "")
    if input_layout_pattern and input_layout_pattern == entry.get("layout_pattern"):
        score += 2.0

    input_topic = str(input_meta.get("topic") or "")
    if input_topic and input_topic == entry.get("topic"):
        score += 2.0

    input_tags = set(input_meta.get("tags") or [])
    entry_tags = set(entry.get("tags") or [])
    score += 1.5 * len(input_tags & entry_tags)

    input_primitives = set(input_meta.get("visual_primitives") or [])
    entry_primitives = set(entry.get("visual_primitives") or [])
    score += 1.2 * len(input_primitives & entry_primitives)

    if bool(entry.get("validation_passed")):
        score += 1.0

    return score


def retrieve_examples_from_entries(
    input_meta: dict[str, Any],
    entries: list[RagIndexEntry],
    *,
    top_k: int = 3,
) -> list[dict[str, Any]]:
    scored: list[dict[str, Any]] = []
    for entry in entries:
        scored.append({"entry": entry, "score": score_entry(input_meta, entry)})

    scored.sort(
        key=lambda item: (
            item["score"],
            bool(item["entry"].get("validation_passed")),
            str(item["entry"].get("problem_id")),
        ),
        reverse=True,
    )

    if top_k <= 0:
        return []
    return scored[:top_k]


def retrieve_examples(
    input_meta: dict[str, Any],
    *,
    index_path: str = "examples/problem/_rag/index.jsonl",
    top_k: int = 3,
) -> list[dict[str, Any]]:
    entries = load_index_jsonl(index_path)
    return retrieve_examples_from_entries(input_meta, entries, top_k=top_k)
