from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class SemanticMetadata:
    title: str = ""
    tags: list[str] = field(default_factory=list)
    instruction: str | None = None
    question: str | None = None
    required_layout_ids: list[str] = field(default_factory=list)
    extras: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        data: dict[str, Any] = {
            "title": self.title,
            "tags": list(self.tags),
            "required_layout_ids": list(self.required_layout_ids),
            **self.extras,
        }
        if self.instruction is not None:
            data["instruction"] = self.instruction
        if self.question is not None:
            data["question"] = self.question
        return data

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "SemanticMetadata":
        instruction = data.get("instruction")
        question = data.get("question")
        known = {"title", "tags", "instruction", "question", "required_layout_ids"}
        extras = {key: value for key, value in data.items() if key not in known}
        return cls(
            title=str(data.get("title", "")),
            tags=[str(tag) for tag in data.get("tags", []) if isinstance(tag, str)],
            instruction=str(instruction) if isinstance(instruction, str) else None,
            question=str(question) if isinstance(question, str) else None,
            required_layout_ids=[
                str(item) for item in data.get("required_layout_ids", []) if isinstance(item, str)
            ],
            extras=extras,
        )
