from __future__ import annotations

from typing import Any

from modu_semantic_archive.normalizer import normalize_semantic
from modu_semantic_archive.orderer import order_semantic


def canonicalize_and_validate(semantic: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(semantic, dict):
        raise ValueError("semantic payload must be an object")
    canonical = normalize_semantic(semantic)
    canonical = order_semantic(canonical)
    if not canonical.get("problem_id"):
        raise ValueError("problem_id is required")
    if not canonical.get("problem_type"):
        raise ValueError("problem_type is required")
    if "render" in canonical and not isinstance(canonical.get("render"), dict):
        raise ValueError("render must be an object when present")
    if "answer" in canonical and not isinstance(canonical.get("answer"), dict):
        raise ValueError("answer must be an object when present")
    return canonical
