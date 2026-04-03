from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(slots=True)
class SemanticV3:
    schema_version: str
    problem_id: str
    problem_type: str
    metadata: dict[str, Any]
    domain: dict[str, Any]
    render: dict[str, Any]
    answer: dict[str, Any]

    @classmethod
    def from_dict(cls, payload: dict[str, Any]) -> "SemanticV3":
        return cls(
            schema_version=payload["schema_version"],
            problem_id=payload["problem_id"],
            problem_type=payload["problem_type"],
            metadata=payload["metadata"],
            domain=payload["domain"],
            render=payload["render"],
            answer=payload["answer"],
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "schema_version": self.schema_version,
            "problem_id": self.problem_id,
            "problem_type": self.problem_type,
            "metadata": self.metadata,
            "domain": self.domain,
            "render": self.render,
            "answer": self.answer,
        }
