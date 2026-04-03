from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any


@dataclass(slots=True)
class BuildContext:
    problem_id: str
    problem_type: str
    source_file: str
    grade_band: str = "unknown"
    language: str = "ko-KR"


@dataclass(slots=True)
class SemanticDocument:
    data: dict[str, Any]


class BaseProblemBuilder(ABC):
    problem_type: str

    @abstractmethod
    def build_domain(self, raw_problem: dict[str, Any]) -> dict[str, Any]:
        raise NotImplementedError

    @abstractmethod
    def build_render(self, raw_problem: dict[str, Any], domain: dict[str, Any]) -> dict[str, Any]:
        raise NotImplementedError

    @abstractmethod
    def build_answer(self, raw_problem: dict[str, Any], domain: dict[str, Any]) -> dict[str, Any]:
        raise NotImplementedError

    def build_semantic(self, ctx: BuildContext, raw_problem: dict[str, Any]) -> SemanticDocument:
        domain = self.build_domain(raw_problem)
        render = self.build_render(raw_problem, domain)
        answer = self.build_answer(raw_problem, domain)

        payload = {
            "schema_version": "modu_math.semantic.v3",
            "problem_id": ctx.problem_id,
            "problem_type": ctx.problem_type,
            "metadata": {
                "grade_band": ctx.grade_band,
                "source_file": ctx.source_file,
                "language": ctx.language,
            },
            "domain": domain,
            "render": render,
            "answer": answer,
        }
        return SemanticDocument(data=payload)
