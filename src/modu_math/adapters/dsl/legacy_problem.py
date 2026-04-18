from __future__ import annotations
from typing import Any, Iterable
from pathlib import Path

from ...semantic.models.problem import SemanticProblem
from ...layout.models.canvas import LayoutCanvas
from ...layout.models.node import LayoutNode
from ...pipeline.compile_problem import compile_problem_pipeline
from .legacy_primitives import Element

class Problem:
    def __init__(self, width: int = 800, height: int = 600, background: str = "#F6F6F6", problem_id: str | None = None, problem_type: str = "generic"):
        self.width = width
        self.height = height
        self.background = background
        self.problem_id = problem_id
        self.problem_type = problem_type
        self.title = ""
        self.metadata: dict[str, Any] = {}
        self.domain: dict[str, Any] = {}
        self.answer: dict[str, Any] = {"blanks": [], "choices": [], "answer_key": []}
        self.elements: list[Element] = []

    def set_canvas(self, *, width: float, height: float, background: str | None = None) -> "Problem":
        self.width = int(width)
        self.height = int(height)
        if background is not None:
            self.background = background
        return self

    def add(self, element: Element) -> "Problem":
        self.elements.append(element)
        return self

    def set_metadata(self, metadata: dict[str, Any]) -> "Problem":
        self.metadata = dict(metadata)
        return self

    def set_domain(self, domain: dict[str, Any]) -> "Problem":
        self.domain = dict(domain)
        return self

    def set_answer(self, *, blanks: list[Any], choices: list[Any], answer_key: list[Any]) -> "Problem":
        self.answer = {
            "blanks": list(blanks),
            "choices": list(choices),
            "answer_key": list(answer_key),
        }
        return self

    def save(self, out_prefix: str | Path, **kwargs) -> None:
        """Adapts the legacy save method to the new compile_problem_pipeline."""
        # Build pure semantic problem
        semantic = SemanticProblem(
            problem_id=self.problem_id or "custom_problem",
            problem_type=self.problem_type,
            metadata=self.metadata,
            domain=self.domain,
            answer=self.answer,
        )

        # Build layout canvas and nodes
        canvas = LayoutCanvas(width=self.width, height=self.height, background=self.background)
        nodes: list[LayoutNode] = []
        
        def collect_nodes(elements: Iterable[Element]):
            for elem in elements:
                if hasattr(elem, "to_layout_node"):
                    nodes.append(elem.to_layout_node())
                if hasattr(elem, "children") and elem.children:
                    collect_nodes(elem.children)
        
        collect_nodes(self.elements)

        # Run canonical pipeline
        compile_problem_pipeline(semantic, canvas, nodes, out_prefix)
