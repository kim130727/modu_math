from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from ..compiler_to_layout import compile_problem_template_to_layout
from ..compiler_to_semantic import compile_problem_template_to_semantic
from .templates import ProblemTemplate


@dataclass(frozen=True)
class NormalizedContracts:
    problem_id: str
    semantic: dict[str, Any]
    layout: dict[str, Any]

    def to_dict(self) -> dict[str, Any]:
        return {
            "problem_id": self.problem_id,
            "semantic": self.semantic,
            "layout": self.layout,
        }


def export_problem_template(problem: ProblemTemplate) -> NormalizedContracts:
    semantic = compile_problem_template_to_semantic(problem)
    layout = compile_problem_template_to_layout(problem)
    return NormalizedContracts(problem_id=problem.id, semantic=semantic, layout=layout)
