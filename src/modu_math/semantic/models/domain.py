from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

@dataclass
class DomainObject:
    id: str
    type: str
    properties: dict[str, Any] = field(default_factory=dict)
    refs: list[dict[str, str]] = field(default_factory=list)
    layout_required: bool = False

    def to_dict(self) -> dict[str, Any]:
        payload: dict[str, Any] = {
            "id": self.id,
            "type": self.type,
            "properties": self.properties,
        }
        if self.refs:
            payload["refs"] = [dict(ref) for ref in self.refs]
        if self.layout_required:
            payload["layout_required"] = True
        return payload


@dataclass
class DomainRelation:
    id: str
    type: str
    from_id: str
    to_id: str
    properties: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        payload: dict[str, Any] = {
            "id": self.id,
            "type": self.type,
            "from_id": self.from_id,
            "to_id": self.to_id,
        }
        if self.properties:
            payload["properties"] = self.properties
        return payload


@dataclass
class SemanticDomain:
    objects: list[DomainObject] = field(default_factory=list)
    relations: list[DomainRelation] = field(default_factory=list)
    extras: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "objects": [obj.to_dict() for obj in self.objects],
            "relations": [relation.to_dict() for relation in self.relations],
            **self.extras,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "SemanticDomain":
        object_items = data.get("objects", [])
        relation_items = data.get("relations", [])

        objects: list[DomainObject] = []
        if isinstance(object_items, list):
            for item in object_items:
                if not isinstance(item, dict):
                    continue
                refs = item.get("refs", [])
                objects.append(
                    DomainObject(
                        id=str(item.get("id", "")),
                        type=str(item.get("type", "object")),
                        properties=dict(item.get("properties", {})) if isinstance(item.get("properties"), dict) else {},
                        refs=[dict(ref) for ref in refs if isinstance(ref, dict)],
                        layout_required=bool(item.get("layout_required", False)),
                    )
                )

        relations: list[DomainRelation] = []
        if isinstance(relation_items, list):
            for item in relation_items:
                if not isinstance(item, dict):
                    continue
                relations.append(
                    DomainRelation(
                        id=str(item.get("id", "")),
                        type=str(item.get("type", "relation")),
                        from_id=str(item.get("from_id", "")),
                        to_id=str(item.get("to_id", "")),
                        properties=dict(item.get("properties", {})) if isinstance(item.get("properties"), dict) else {},
                    )
                )

        known = {"objects", "relations"}
        extras = {key: value for key, value in data.items() if key not in known}
        return cls(objects=objects, relations=relations, extras=extras)
