from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

TAXONOMY_JSON_PATH = Path(__file__).parent / "taxonomy.json"


@dataclass(frozen=True)
class TaxonomyTag:
    key: str
    name_ko: str
    domain: str
    grade: int | None
    parent_key: str | None
    description: str
    type: str  # "concept" | "skill"

    def to_dict(self) -> dict[str, Any]:
        return {
            "key": self.key,
            "name_ko": self.name_ko,
            "domain": self.domain,
            "grade": self.grade,
            "parent_key": self.parent_key,
            "description": self.description,
            "type": self.type,
        }


class TaxonomyRegistry:
    def __init__(self, path: Path = TAXONOMY_JSON_PATH) -> None:
        self._path = path
        self._tags: dict[str, TaxonomyTag] = {}
        self._load()

    def _load(self) -> None:
        if not self._path.exists():
            return
        data = json.loads(self._path.read_text(encoding="utf-8"))
        for item in data.get("tags", []):
            tag = TaxonomyTag(
                key=item["key"],
                name_ko=item["name_ko"],
                domain=item["domain"],
                grade=item.get("grade"),
                parent_key=item.get("parent_key"),
                description=item.get("description", ""),
                type=item.get("type", "concept"),
            )
            self._tags[tag.key] = tag

    def get(self, key: str) -> TaxonomyTag | None:
        return self._tags.get(key)

    def contains(self, key: str) -> bool:
        return key in self._tags

    def list_tags(self, tag_type: str | None = None) -> list[TaxonomyTag]:
        if tag_type is None:
            return list(self._tags.values())
        return [tag for tag in self._tags.values() if tag.type == tag_type]

    def get_name_ko(self, key: str) -> str:
        tag = self.get(key)
        return tag.name_ko if tag else key


_default_registry: TaxonomyRegistry | None = None


def get_taxonomy_registry() -> TaxonomyRegistry:
    global _default_registry
    if _default_registry is None:
        _default_registry = TaxonomyRegistry()
    return _default_registry
