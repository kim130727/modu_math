import json
from pathlib import Path
from typing import Any


def load_profile() -> dict[str, Any]:
    profile_path = Path(__file__).resolve().parents[3] / "schema" / "contract" / "canonical_order_profile.json"
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


def _sorted_dict_list(items: list[Any]) -> list[Any]:
    dict_items = [item for item in items if isinstance(item, dict)]
    rest = [item for item in items if not isinstance(item, dict)]
    dict_items.sort(key=lambda item: str(item.get("id", "")))
    return [*dict_items, *rest]


def order_semantic(data: dict[str, Any]) -> dict[str, Any]:
    profile = load_profile()
    if "semantic_root_order" in profile:
        data = _reorder_by_profile(data, profile["semantic_root_order"])

    if "metadata" in data and isinstance(data["metadata"], dict):
        metadata_order = ["title", "tags", "instruction", "question", "required_layout_ids"]
        data["metadata"] = _reorder_by_profile(data["metadata"], metadata_order)

    if "domain" in data and isinstance(data["domain"], dict):
        if "domain_order" in profile:
            data["domain"] = _reorder_by_profile(data["domain"], profile["domain_order"])
        if isinstance(data["domain"].get("objects"), list):
            data["domain"]["objects"] = _sorted_dict_list(data["domain"]["objects"])
        if isinstance(data["domain"].get("relations"), list):
            data["domain"]["relations"] = _sorted_dict_list(data["domain"]["relations"])

    if "answer" in data and isinstance(data["answer"], dict):
        answer_order = ["blanks", "choices", "answer_key"]
        data["answer"] = _reorder_by_profile(data["answer"], answer_order)
        if isinstance(data["answer"].get("blanks"), list):
            data["answer"]["blanks"] = _sorted_dict_list(data["answer"]["blanks"])
        if isinstance(data["answer"].get("choices"), list):
            data["answer"]["choices"] = _sorted_dict_list(data["answer"]["choices"])

    return data


def normalize_semantic(data: dict[str, Any]) -> dict[str, Any]:
    return order_semantic(data)
