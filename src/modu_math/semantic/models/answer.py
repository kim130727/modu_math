from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class SemanticAnswer:
    blanks: list[dict[str, Any]] = field(default_factory=list)
    choices: list[dict[str, Any]] = field(default_factory=list)
    answer_key: list[dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "blanks": [dict(item) for item in self.blanks],
            "choices": [dict(item) for item in self.choices],
            "answer_key": [dict(item) for item in self.answer_key],
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "SemanticAnswer":
        def _as_dict_list(value: Any) -> list[dict[str, Any]]:
            if not isinstance(value, list):
                return []
            return [dict(item) for item in value if isinstance(item, dict)]

        return cls(
            blanks=_as_dict_list(data.get("blanks")),
            choices=_as_dict_list(data.get("choices")),
            answer_key=_as_dict_list(data.get("answer_key")),
        )
