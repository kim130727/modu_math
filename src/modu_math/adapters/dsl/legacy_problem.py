from __future__ import annotations
from typing import Any
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
        """
        Compile and persist semantic/layout/renderer contracts and SVG.

        Backward-compatible options:
        - validate: enables strict cross-layer validation.
        - cross_layer_validate: explicit strict-mode toggle (overrides validate).
        - emit_semantic: when False, do not write `<prefix>.semantic.json`.
        """
        domain_payload = dict(self.domain)
        domain_payload.setdefault("objects", [])
        domain_payload.setdefault("relations", [])

        answer_payload = dict(self.answer)
        answer_payload.setdefault("blanks", [])
        answer_payload.setdefault("choices", [])
        answer_payload.setdefault("answer_key", [])

        # Build pure semantic problem
        semantic = SemanticProblem(
            problem_id=self.problem_id or "custom_problem",
            problem_type=self.problem_type,
            metadata=self.metadata,
            domain=domain_payload,
            answer=answer_payload,
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
        compile_problem_pipeline(
            semantic,
            canvas,
            nodes,
            out_prefix,
            layout_patches=kwargs.get("layout_patches"),
            editor_state=kwargs.get("editor_state"),
            validate=bool(kwargs.get("validate", False)),
            cross_layer_validate=kwargs.get("cross_layer_validate"),
            emit_semantic=bool(kwargs.get("emit_semantic", False)),
        )
