from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path
from typing import Any


@lru_cache(maxsize=1)
def contract_dir() -> Path:
    return Path(__file__).resolve().parents[2] / "schema" / "contract"


@lru_cache(maxsize=None)
def load_contract_json(filename: str) -> dict[str, Any]:
    path = contract_dir() / filename
    return json.loads(path.read_text(encoding="utf-8-sig"))


def _reorder_by_profile(data: dict[str, Any], order: list[str]) -> dict[str, Any]:
    reordered: dict[str, Any] = {}
    for key in order:
        if key in data:
            reordered[key] = data[key]
    for key, value in data.items():
        if key not in reordered:
            reordered[key] = value
    return reordered


def canonicalize_semantic_json(data: dict[str, Any]) -> dict[str, Any]:
    profile = load_contract_json("canonical_order_profile.json")
    semantic = _reorder_by_profile(data, profile["semantic_root_order"])

    render = semantic.get("render")
    if isinstance(render, dict):
        semantic["render"] = _reorder_by_profile(render, profile["render_order"])
        canvas = semantic["render"].get("canvas")
        if isinstance(canvas, dict):
            semantic["render"]["canvas"] = _reorder_by_profile(canvas, profile["canvas_order"])

    answer = semantic.get("answer")
    if isinstance(answer, dict):
        semantic["answer"] = _reorder_by_profile(answer, profile["answer_order"])

    return semantic


def canonicalize_layout_json(data: dict[str, Any]) -> dict[str, Any]:
    profile = load_contract_json("canonical_order_profile.json")
    return _reorder_by_profile(data, profile["layout_root_order"])

