from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Iterable

from .adapters import problem_to_ir
from .compiler_json import compile_semantic_json
from .compiler_svg import compile_svg
from .schema import validate_semantic_json


@dataclass
class Problem:
    width: int
    height: int
    background: str = "#F6F6F6"
    problem_id: str | None = None
    problem_type: str = "generic"
    title: str | None = None
    schema_version: str = "modu_math.semantic.v3"
    render_contract_version: str = "modu_math.render.v1"
    elements: list[object] = field(default_factory=list)
    metadata: dict[str, object] = field(default_factory=dict)
    domain: dict[str, object] = field(default_factory=dict)
    answer: dict[str, object] = field(default_factory=lambda: {"blanks": [], "choices": [], "answer_key": []})

    def add(self, element: object) -> "Problem":
        self.elements.append(element)
        return self

    def add_element(self, element: object) -> "Problem":
        return self.add(element)

    def extend(self, elements: Iterable[object]) -> "Problem":
        self.elements.extend(elements)
        return self

    def set_canvas(self, *, width: float, height: float, background: str | None = None) -> "Problem":
        self.width = int(width)
        self.height = int(height)
        if background is not None:
            self.background = background
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

    def update_content(self, element_id: str, content: str) -> "Problem":
        for element in self.elements:
            if getattr(element, "id", None) != element_id:
                continue
            if hasattr(element, "expr"):
                element.expr = content
                return self
            if hasattr(element, "text"):
                element.text = content
                return self
            raise ValueError(f"Element '{element_id}' is not text/formula.")
        raise ValueError(f"Element not found: {element_id}")

    def update_text(self, element_id: str, text: str) -> "Problem":
        # Backward-compatible alias.
        return self.update_content(element_id, text)

    def move(self, element_id: str, *, x: float | None = None, y: float | None = None) -> "Problem":
        for element in self.elements:
            if getattr(element, "id", None) != element_id:
                continue
            if hasattr(element, "x") and x is not None:
                setattr(element, "x", x)
            if hasattr(element, "y") and y is not None:
                setattr(element, "y", y)
            return self
        raise ValueError(f"Element not found: {element_id}")

    def to_semantic_dict(self) -> dict[str, object]:
        return compile_semantic_json(
            self.to_ir(),
            schema_version=self.schema_version,
            render_contract_version=self.render_contract_version,
            title=self.title,
            metadata=self.metadata,
            domain=self.domain,
            answer=self.answer,
        )

    def to_svg(self) -> str:
        return compile_svg(self.to_ir())

    def to_semantic_json(self, *, validate: bool = True) -> dict[str, object]:
        data = self.to_semantic_dict()
        if validate:
            validate_semantic_json(data)
        return data

    def to_semantic(self, *, validate: bool = True) -> dict[str, object]:
        return self.to_semantic_json(validate=validate)

    def validate(self) -> None:
        if self.width <= 0 or self.height <= 0:
            raise ValueError("canvas size must be positive")
        semantic = self.to_semantic_dict()
        validate_semantic_json(semantic)

    def to_ir(self):
        ir_problem = problem_to_ir(self)
        ir_problem.background = self.background
        return ir_problem

    def _to_legacy_ir(self):
        return self.to_ir()

    def save(
        self,
        out_prefix: str | Path,
        *,
        validate: bool = True,
        include_layout_diff: bool | None = None,
        baseline_layout_path: str | Path | None = None,
    ) -> dict[str, Path] | None:
        if include_layout_diff is True or baseline_layout_path is not None:
            raise ValueError("layout/layout_diff export has been removed. Semantic JSON is the single canonical output.")

        out_prefix = Path(out_prefix)
        out_prefix.parent.mkdir(parents=True, exist_ok=True)

        from .output import build_canonical_payloads

        semantic = build_canonical_payloads(
            self._to_legacy_ir(),
            validate=validate,
            semantic_options={
                "schema_version": self.schema_version,
                "render_contract_version": self.render_contract_version,
                "title": self.title,
                "metadata": self.metadata,
                "domain": self.domain,
                "answer": self.answer,
            },
        )
        svg = self.to_svg()

        out_prefix.with_suffix(".semantic.json").write_text(
            json.dumps(semantic, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        out_prefix.with_suffix(".svg").write_text(svg, encoding="utf-8")
        return None

    def save_semantic_json(self, path: str | Path, *, validate: bool = True) -> Path:
        target = Path(path)
        target.parent.mkdir(parents=True, exist_ok=True)
        payload = self.to_semantic_json(validate=validate)
        target.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
        return target

    def save_svg(self, path: str | Path) -> Path:
        target = Path(path)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(self.to_svg(), encoding="utf-8")
        return target
