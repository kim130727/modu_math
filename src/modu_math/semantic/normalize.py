import json
from pathlib import Path
from typing import Any

def load_profile() -> dict[str, Any]:
    profile_path = Path("c:/projects/modu_math/schema/contract/canonical_order_profile.json")
    if profile_path.exists():
        with open(profile_path, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

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
    profile = load_profile()
    if "semantic_root_order" in profile:
        data = _reorder_by_profile(data, profile["semantic_root_order"])
    
    if "domain" in data and isinstance(data["domain"], dict):
        if "domain_order" in profile:
            data["domain"] = _reorder_by_profile(data["domain"], profile["domain_order"])
            
    return data

def normalize_semantic(data: dict[str, Any]) -> dict[str, Any]:
    # Placeholder for standardizing semantic objects/relations formatting
    return order_semantic(data)
