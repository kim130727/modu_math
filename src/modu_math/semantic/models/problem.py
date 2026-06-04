from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from .answer import SemanticAnswer
from .domain import SemanticDomain
from .metadata import SemanticMetadata


@dataclass
class SemanticProblem:
    problem_id: str | None = None
    problem_type: str = "generic"
    metadata: SemanticMetadata | dict[str, Any] = field(default_factory=SemanticMetadata)
    domain: SemanticDomain | dict[str, Any] = field(default_factory=SemanticDomain)
    answer: SemanticAnswer | dict[str, Any] = field(default_factory=SemanticAnswer)

    def __post_init__(self) -> None:
        if isinstance(self.metadata, dict):
            self.metadata = SemanticMetadata.from_dict(self.metadata)
        if isinstance(self.domain, dict):
            self.domain = SemanticDomain.from_dict(self.domain)
        if isinstance(self.answer, dict):
            self.answer = SemanticAnswer.from_dict(self.answer)

    def set_metadata(self, metadata: dict[str, Any]) -> "SemanticProblem":
        self.metadata = SemanticMetadata.from_dict(dict(metadata))
        return self

    def set_domain(self, domain: dict[str, Any]) -> "SemanticProblem":
        self.domain = SemanticDomain.from_dict(dict(domain))
        return self

    def set_answer(
        self,
        *,
        blanks: list[Any] | None = None,
        choices: list[Any] | None = None,
        answer_key: list[Any] | None = None,
    ) -> "SemanticProblem":
        self.answer = SemanticAnswer(
            blanks=[dict(item) for item in blanks or [] if isinstance(item, dict)],
            choices=[dict(item) for item in choices or [] if isinstance(item, dict)],
            answer_key=[dict(item) for item in answer_key or [] if isinstance(item, dict)],
        )
        return self

    def to_dict(self) -> dict[str, Any]:
        metadata = self.metadata.to_dict() if isinstance(self.metadata, SemanticMetadata) else dict(self.metadata)
        domain = self.domain.to_dict() if isinstance(self.domain, SemanticDomain) else dict(self.domain)
        answer = self.answer.to_dict() if isinstance(self.answer, SemanticAnswer) else dict(self.answer)
        return {
            "problem_id": self.problem_id,
            "problem_type": self.problem_type,
            "metadata": metadata,
            "domain": domain,
            "answer": answer,
        }
