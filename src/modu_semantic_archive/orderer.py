from __future__ import annotations

from typing import Any

from .contracts import canonicalize_layout_json, canonicalize_semantic_json, load_contract_json


def _reorder_by_profile(data: dict[str, Any], order: list[str]) -> dict[str, Any]:
    reordered: dict[str, Any] = {}
    for key in order:
        if key in data:
            reordered[key] = data[key]
    for key, value in data.items():
        if key not in reordered:
            reordered[key] = value
    return reordered


def order_semantic(data: dict[str, Any]) -> dict[str, Any]:
    return canonicalize_semantic_json(data)


def order_layout(data: dict[str, Any]) -> dict[str, Any]:
    return canonicalize_layout_json(data)


def order_layout_diff(data: dict[str, Any]) -> dict[str, Any]:
    profile = load_contract_json("canonical_order_profile.json")
    return _reorder_by_profile(data, profile["layout_diff_root_order"])
