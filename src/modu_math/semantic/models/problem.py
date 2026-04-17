from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class SemanticProblem:
    problem_id: str | None = None
    problem_type: str = "generic"
    metadata: dict[str, Any] = field(default_factory=dict)
    domain: dict[str, Any] = field(default_factory=lambda: {"objects": [], "relations": []})
    answer: dict[str, Any] = field(default_factory=lambda: {"blanks": [], "choices": [], "answer_key": []})

    def set_metadata(self, metadata: dict[str, Any]) -> "SemanticProblem":
        self.metadata = dict(metadata)
        return self

    def set_domain(self, domain: dict[str, Any]) -> "SemanticProblem":
        self.domain = dict(domain)
        return self

    def set_answer(self, *, blanks: list[Any] | None = None, choices: list[Any] | None = None, answer_key: list[Any] | None = None) -> "SemanticProblem":
        self.answer = {
            "blanks": list(blanks) if blanks is not None else [],
            "choices": list(choices) if choices is not None else [],
            "answer_key": list(answer_key) if answer_key is not None else [],
        }
        return self

    def to_dict(self) -> dict[str, Any]:
        return {
            "problem_id": self.problem_id,
            "problem_type": self.problem_type,
            "metadata": self.metadata,
            "domain": self.domain,
            "answer": self.answer,
        }
