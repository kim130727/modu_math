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
    semantic_order = profile.get("semantic_root_order", ["problem_id", "problem_type", "metadata", "domain", "render", "answer"])
    semantic = _reorder_by_profile(data, semantic_order)

    domain = semantic.get("domain")
    domain_order = profile.get("domain_order")
    if isinstance(domain, dict) and isinstance(domain_order, list):
        semantic["domain"] = _reorder_by_profile(domain, domain_order)

    render = semantic.get("render")
    if isinstance(render, dict):
        render_order = profile.get("render_order", ["canvas", "elements"])
        if isinstance(render_order, list):
            semantic["render"] = _reorder_by_profile(render, render_order)
        else:
            semantic["render"] = render
        canvas = semantic["render"].get("canvas")
        if isinstance(canvas, dict):
            canvas_order = profile.get("canvas_order", ["width", "height", "background"])
            if isinstance(canvas_order, list):
                semantic["render"]["canvas"] = _reorder_by_profile(canvas, canvas_order)

    answer = semantic.get("answer")
    if isinstance(answer, dict):
        answer_order = profile.get("answer_order", ["blanks", "choices", "answer_key"])
        if isinstance(answer_order, list):
            semantic["answer"] = _reorder_by_profile(answer, answer_order)

    return semantic


def canonicalize_layout_json(data: dict[str, Any]) -> dict[str, Any]:
    profile = load_contract_json("canonical_order_profile.json")
    return _reorder_by_profile(data, profile["layout_root_order"])

